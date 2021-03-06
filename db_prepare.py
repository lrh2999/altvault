import sqlite3
import sys
import pyodbc

# User
import DBstructure
import config


def DBsearch(keyword):
    # Search records by Part Number coloumn
    findkey = ('%'+keyword+'%',)
    cursor.execute("SELECT * FROM components WHERE \"Part Number\" LIKE ?", findkey)
    for rec in cursor.fetchall():
        print(rec)
        print()

def sqlite_prep():
    try:
        conn = sqlite3.connect("lenkov_altium_lib.db")
        cursor = conn.cursor()
        cursor.execute("SELECT comment FROM components")
    except Exception:
        print("Wrong database")
        sys.exit(0)

    DBsearch("STM32")

    # Create dict from coloumns
    field = {}
    for col in cursor.description:
        field[col[0].replace(' ', '_')] = None

    # Fill the fields
    field["Part_Number"] = "852"
    field["Comment"] = "qwerty"

    # Assembly a record (NOT USE IN PRODUCTION !!!)
    colNames = ""
    dictNames = ""
    for col in cursor.description:
        colNames += "`{}`, ".format(col[0])
        dictNames += ":{}, ".format(col[0].replace(' ', '_')) # Not from field{} because keys may have a different order

    # THE FOLLOWING STRING MUST HARDCODED IN PRODUCTION !!! NO STRING OPERATORS !!!
    insert_skeleton = "INSERT INTO components ({}) VALUES ({})".format(colNames[:-2], dictNames[:-2])
    print(insert_skeleton)

    # Make a record
    cursor.execute(insert_skeleton, field)
    conn.commit()

    print()
    DBsearch(field["Part_Number"])

    conn.close()

def generate_query():
    for i in DBstructure.colNames:
        print('?,', end='')

def cern_path():
    # Connect to target single table Database
    targetCon = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+config.DB_path)
    targetCur = targetCon.cursor()
    query = '''UPDATE components
               SET [Library Path]   = \'CERN\\\' & [Library Path]
                  ,[Footprint Path] = \'CERN\\\' & [Footprint Path]
               WHERE Author LIKE \'%CERN%\''''
    targetCur.execute(query)
    targetCur.commit()
    targetCon.close()

### MAIN ###
cern_path()
