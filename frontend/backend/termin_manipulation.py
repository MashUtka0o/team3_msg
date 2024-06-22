import sqlite3

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


def termin_cancelation(termID):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        cursor.execute(""" DELETE FROM Termins WHERE termID = (?) """, (termID,))

        print('Termin was removed to the table')

        sqliteConnection.commit()
        print("File updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


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

            cursor.execute(""" INSERT INTO Medicine (PresID, medName, medDose, medCompany, insType) VALUES (?,?,?,?,?) """, (presID, medName, medDose, medCompany, insType))
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


def attach_file_to_termin(termID, file_path):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        file = convertToBinaryData(file_path)
        cursor.execute(""" INSERT INTO TerminAttachedFiles(termID, file) VALUES (?, ?)""", (termID, file))

        sqliteConnection.commit()
        print("File inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")