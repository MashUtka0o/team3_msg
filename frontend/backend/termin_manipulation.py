import sqlite3
from os import getcwd
import datetime


def get_one_termin(term_id):
    try:
        term_id = str(term_id)
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"SELECT slotDate, slotTime, docName, docSurname, locAddress, patName, patSurname, summary FROM TerminInfo WHERE termID = (?)"

        print(query)
        cursor.execute(query, (term_id,))
        sqliteConnection.commit()
        rows = cursor.fetchall()
        rows = list(dict.fromkeys(rows))
        cursor.close()
        return rows[0]
    except sqlite3.Error as error:
        print("Failed to Get Table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def get_all_files(ter_id):
    try:
        term_id = str(ter_id)
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"SELECT file FROM TerminAttachedFiles WHERE termID = (?)"
        cursor.execute(query, (term_id,))
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


def download_blob_from_db(term_id, mode):
    conn = sqlite3.connect('./backend/Test.db')
    cursor = conn.cursor()

    if mode == 'summary':
        cursor.execute('SELECT termID, summary FROM Termins WHERE TermID = ?', (term_id,))
    elif mode == 'attached':
        cursor.execute('SELECT documentID, file FROM TerminAttachedFiles WHERE TermID = ?', (term_id,))

    row = cursor.fetchone()
    id, data = row
    file_path = f'attached_file_{id}.pdf'

    # Check if a row was returned
    if row:
        # Write the BLOB data to a file
        with open(file_path, 'wb') as file:
            file.write(data)
    else:
        print(f"No file found with ID {term_id}")

    # Close the cursor and connection
    cursor.close()
    conn.close()


def termin_creation(slot_id, pat_id):
    try:
        sqliteConnection = sqlite3.connect('./backend/Test.db')
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
        term_id = cursor.lastrowid
        sqliteConnection.commit()
        print("File updated successfully")
        cursor.close()
        return term_id
    except sqlite3.Error as error:
        print("Failed to update table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def termin_cancelation(termID):
    try:
        sqliteConnection = sqlite3.connect('./backend/Test.db')
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
        sqliteConnection = sqlite3.connect('./backend/Test.db')
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
        sqliteConnection = sqlite3.connect('./backend/Test.db')
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


def attach_file_to_termin(termID, file_path):
    current_dir = getcwd()
    db_path = f'{current_dir}/Test.db'
    try:
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        file = convertToBinaryData(file_path)
        cursor.execute(""" INSERT INTO TerminAttachedFiles(termID, file) VALUES (?, ?)""", (termID, file))
        # cursor.execute(""" SELECT * FROM TerminAttachedFiles """)
        print(cursor.fetchall())

        sqliteConnection.commit()
        print("File inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def show_all_the_tables():
    sqliteConnection = sqlite3.connect('Test.db')
    cursor = sqliteConnection.cursor()
    print("Hello to SQLite")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        print(table[0])

    sqliteConnection.close()


def get_pat_termin(pat_id):
    try:
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = """SELECT termID, docName, docSurname, slotDate, slotTime, locAddress FROM TerminInfo WHERE patID = (?) AND status = 1"""
        cursor.execute(query, str(pat_id))
        sqliteConnection.commit()
        rows = cursor.fetchall()
        rows = list(dict.fromkeys(rows))
        cursor.close()
        return rows
    except sqlite3.Error as error:
        print("Failed to Get Table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def get_loc():
    try:
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = """SELECT * FROM Locations"""
        cursor.execute(query)
        sqliteConnection.commit()
        rows = cursor.fetchall()
        rows = [x[1] for x in rows]
        cursor.close()
        return rows
    except sqlite3.Error as error:
        print("Failed to Get Table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def get_doc_termin(doc_id):
    try:
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = """SELECT termID, patName, patSurname, slotDate, slotTime, locAddress FROM TerminInfo WHERE docID = (?) AND status = 1"""
        cursor.execute(query, str(doc_id))
        sqliteConnection.commit()
        rows = cursor.fetchall()
        rows = list(dict.fromkeys(rows))
        cursor.close()
        return rows
    except sqlite3.Error as error:
        print("Failed to Get Table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
    return


def get_one_patient(patient_id):
    try:
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = """SELECT name, surname, dateOfBirth FROM Patients WHERE patID = (?)"""
        cursor.execute(query, str(patient_id))
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
    return


def get_free_slots(location, doctor):
    try:
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        # sqliteConnection = sqlite3.connect("Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        name_parts = doctor.split(maxsplit=1)  # Split at the last whitespace

        if len(name_parts) < 2:
            first_name = ""
            surname = name_parts[0]
        else:
            first_name = name_parts[0]
            surname = name_parts[1]

        query = """SELECT slotID, slotDate, slotTime FROM DoctorsInfo WHERE name = (?) AND surname = (?) AND slotStatus = 1"""
        cursor.execute(query, (first_name, surname))
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


def get_doctor_type():
    try:
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        # sqliteConnection = sqlite3.connect("Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = """SELECT type FROM Doctors"""
        cursor.execute(query)
        sqliteConnection.commit()
        rows = cursor.fetchall()
        rows = [x[0] for x in rows]
        rows = list(dict.fromkeys(rows))
        cursor.close()
        return rows
    except sqlite3.Error as error:
        print("Failed to Get Table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def get_doc(doc_type):
    try:
        sqliteConnection = sqlite3.connect("./backend/Test.db")
        # sqliteConnection = sqlite3.connect("Test.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        if doc_type:
            query = f"SELECT name,surname FROM Doctors WHERE type IN ({','.join(['?'] * len(doc_type))})"
            cursor.execute(query, doc_type)
        else:
            query = """SELECT name, surname FROM Doctors"""
            cursor.execute(query)
        sqliteConnection.commit()
        rows = cursor.fetchall()
        rows = [x[0] + " " + x[1] for x in rows]
        # rows = [x[0] for x in rows]
        # rows = list(dict.fromkeys(rows))
        cursor.close()
        return rows
    except sqlite3.Error as error:
        print("Failed to Get Table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
