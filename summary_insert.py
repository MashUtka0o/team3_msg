import sqlite3


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


# insertBLOB(1, "Smith", "E:\pynative\Python\photos\smith.jpg", "E:\pynative\Python\photos\smith_resume.txt")
insertBLOB(1, 5, 1, 'sum1.pdf')
