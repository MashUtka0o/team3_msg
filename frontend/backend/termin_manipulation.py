import sqlite3
import datetime


def get_pat_termin(pat_id):
    try:
        sqliteConnection = sqlite3.connect("Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = """SELECT termID, docName, docSurname, slotDate, slotTime,locAddress FROM TerminInfo WHERE patID = (?) AND status = 1"""
        cursor.execute(query, str(pat_id))
        sqliteConnection.commit()
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except sqlite3.Error as error:
        print("Failed to Get Table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def get_free_slots(doc_id):
    return


def get_doc_id(search):
    return


def termin_creation(slot_id, pat_id):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Update Slots table
        update_query = """ UPDATE Slots SET slotStatus = (?) WHERE slotID = (?) """
        slot_id_tuple = (0, slot_id)
        cursor.execute(update_query, slot_id_tuple)
        print('Slots table is updated')

        # Create termin record
        create_query = """ INSERT INTO Termins (patId, slotID, status) VALUES (?, ?, ?) """
        insert_tuple = (pat_id, slot_id, 1)
        cursor.execute(create_query, insert_tuple)
        print('Termin was added to the table')

        sqliteConnection.commit()
        print("File updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def insert_summary(patID, slotID, status, summary_path):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO Termins
                                  ( patID, slotID, status, summary) VALUES (?, ?, ?, ?)"""

        summary = convertToBinaryData(summary_path)
        # Convert data into tuple format
        data_tuple = (patID, slotID, status, summary)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("File inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def create_prescription(termID, type, **kwargs):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        cursor.execute(""" INSERT INTO Prescriptions (termID, type) VALUES (?,?)""", (termID, type))
        presID = cursor.lastrowid
        print("Record added to Prescription table")

        if type == 'medicine':
            medName = kwargs['medName']
            medDose = kwargs['medDose']
            medCompany = kwargs['medCompany']
            insType = kwargs['insType']

            cursor.execute(
                """ INSERT INTO Medicine (PresID, medName, medDose, medCompany, insType) VALUES (?,?,?,?,?) """,
                (presID, medName, medDose, medCompany, insType))
            print("Record added to Medicine table")

        elif type == 'redirection':
            docId = kwargs['docID']
            cursor.execute(""" INSERT INTO Redirections (preID, docID) VALUES (?,?) """, (presID, docId))
            print("Record added to Redirections table")

        else:
            raise "Type is not right. It should be either 'medicine' or 'redirection'"

        sqliteConnection.commit()
        print("File inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
