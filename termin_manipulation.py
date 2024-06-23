import sqlite3
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import date, timedelta


def termin_creation(slot_id, pat_id):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to DB")

        # Update Slots table
        update_query = """ UPDATE Slots SET slotStatus = (?) WHERE slotID = (?) """
        slot_id_tuple = (0, slot_id)
        cursor.execute(update_query, slot_id_tuple)
        print('Slots table is updated')

        # Create termin record
        create_query = """ INSERT INTO Termins (patId, slotID, status) VALUES (?, ?, ?) """
        insert_tuple = (pat_id, slot_id, 1)
        cursor.execute(create_query, insert_tuple)
        print('Termin was added to the Termins table')

        cursor.execute(""" SELECT DISTINCT docID FROM TerminInfo WHERE slotID = (?)""", (slot_id,))
        doc_id_tuple = cursor.fetchall()
        doc_id = doc_id_tuple[0][0]

        sqliteConnection.commit()
        cursor.close()


        termin_status_changing_storing(slot_id, 'pat', pat_id, 'create')
        termin_status_changing_storing(slot_id, 'doc', doc_id, 'create')

    except sqlite3.Error as error:
        print("Failed to create termin.", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def termin_cancelation(termID):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to DB")

        cursor.execute(""" SELECT DISTINCT * FROM TerminInfo WHERE termID = (?) """, (termID,))
        termin_tuple = cursor.fetchall()

        cursor.execute(""" DELETE FROM Termins WHERE termID = (?) """, (termID,))
        print('Termin was removed to the table')

        sqliteConnection.commit()

        cursor.close()

        slot_id = termin_tuple[0][8]
        pat_id = termin_tuple[0][1]
        doc_id = termin_tuple[0][4]

        termin_status_changing_storing(slot_id, 'pat', pat_id, 'delete')
        termin_status_changing_storing(slot_id, 'doc', doc_id, 'delete')

    except sqlite3.Error as error:
        print("Failed to delete termin", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insert_summary(patID, slotID, status, summary_path):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to DB")

        sqlite_insert_blob_query = """ INSERT INTO Termins ( patID, slotID, status, summary) VALUES (?, ?, ?, ?)"""
        summary = convertToBinaryData(summary_path)
        data_tuple = (patID, slotID, status, summary)

        cursor.execute(sqlite_insert_blob_query, data_tuple)

        sqliteConnection.commit()
        print("Summary inserted successfully as a BLOB into a Termins table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into Termins table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def create_prescription(termID, type, **kwargs):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to DB")

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
        print("Prescription file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into Prescriptions table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def attach_file_to_termin(termID, file_path):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to DB")

        file = convertToBinaryData(file_path)
        cursor.execute(""" INSERT INTO TerminAttachedFiles(termID, file) VALUES (?, ?)""", (termID, file))

        sqliteConnection.commit()
        print("File inserted successfully as a BLOB into a TerminAtachedFiles table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into TerminAttachedFiles table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def add_text(record, mode):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    if mode == 'medicine':
        # insType: 0 - green; 1 - red; 2 - blue
        if record[-1] == 0:
            can.drawString(50, 580, 'DAK Gesundheit')
            can.drawString(50, 540, record[2])  # Patient Surname
            can.drawString(100, 540, record[1])  # Patient Name
            can.drawString(260, 525, record[3])  # Patient Birthdate
            can.drawString(270, 430, record[9])  # Date
            can.drawString(50, 375, record[-4] + ', ' + record[-2] + ', ' + record[-3])  # Medicine name
            can.drawString(425, 320, f'Dr. {record[5]} {record[6]}')  # Doctors Name and Surname
            can.drawString(375, 300, record[8])  # Doctor's Address

        elif record[-1] == 1:
            can.drawString(50, 580, 'DAK Gesundheit')
            can.drawString(50, 540, record[2])  # Patient Surname
            can.drawString(100, 540, record[1])  # Patient Name
            can.drawString(270, 525, record[3])  # Patient Birthdate
            can.drawString(270, 430, record[9])  # Date
            can.drawString(50, 375, record[-4] + ', ' + record[-2] + ', ' + record[-3])  # Medicine name
            can.drawString(425, 330, f'Dr. {record[5]} {record[6]}')  # Doctors Name and Surname
            can.drawString(375, 310, record[8])  # Doctor's Address

        elif record[-1] == 2:
            can.drawString(50, 580, 'Allianz AG')
            can.drawString(50, 540, record[2])  # Patient Surname
            can.drawString(100, 540, record[1])  # Patient Name
            can.drawString(270, 525, record[3])  # Patient Birthdate
            can.drawString(270, 430, record[9])  # Date
            can.drawString(50, 375, record[-4] + ', ' + record[-2] + ', ' + record[-3])  # Medicine name
            can.drawString(425, 330, f'Dr. {record[5]} {record[6]}')  # Doctors Name and Surname
            can.drawString(375, 310, record[8])  # Doctor's Address
        else:
            raise 'Wrong index. Should 0,1 or 2'

    elif mode == 'redirection':
        # Patient information
        can.drawString(30, 595, 'DAK Gesundheit')
        can.drawString(50, 540, record[2])  # Patient Surname
        can.drawString(110, 540, record[1])  # Patient Name
        can.drawString(185, 550, record[3])  # Patient Birthdate
        can.drawString(185, 490, record[9])  # Date

        # Redirected doctor information
        can.drawString(320, 535, f'{record[-1]}, {record[-3]} {record[-2]}')  # Redirected doctor type, Name Surname

        # Doctor who gives the redirection
        can.setFont("Helvetica", 8)  # Adjust the font size to fit the address in the box
        address_text = f'Dr. {record[5]} {record[6]}\n{record[8]}'
        text_object = can.beginText(440, 265)  # Starting position for the address
        text_object.setTextOrigin(440, 280)  # Fine-tune this to fit the box perfectly
        for line in address_text.split('\n'):
            text_object.textLine(line)
        can.drawText(text_object)

    else:
        raise "Wrong type of prescription! It should be either 'medicine' or 'redirection'"

    can.save()
    packet.seek(0)
    return packet


def prescription_to_pdf(record, mode):
    if mode == 'medicine':
        templates_name = ['green', 'red', 'blue']
        template_path = 'Prescription_templates/' + templates_name[record[0][-1]] + '.pdf'
        output_file_path = f'Prescriptions/prescription_{record[0][0]}.pdf'

    elif mode == 'redirection':
        template_path = 'Prescription_templates/redirection.pdf'
        output_file_path = f'Prescriptions/redirection_{record[0][0]}.pdf'

    else:
        raise "Wrong type of prescription! It should be either 'medicine' or 'redirection'"

    with open(template_path, 'rb') as template_file:
        original_pdf = PyPDF2.PdfReader(template_file)
        output_pdf = PyPDF2.PdfWriter()

        # Create an overlay PDF with the text
        overlay_packet = add_text(record[0], mode)
        overlay_pdf = PyPDF2.PdfReader(overlay_packet)

        # Iterate through each page and merge the overlay
        for page_num in range(len(original_pdf.pages)):
            page = original_pdf.pages[page_num]
            if page_num < len(overlay_pdf.pages):
                overlay_page = overlay_pdf.pages[0]
                page.merge_page(overlay_page)
            output_pdf.add_page(page)


        # Write the output PDF to a file
        with open(output_file_path, 'wb') as prescription:
            output_pdf.write(prescription)

    print(f'{mode} file was created')
    return output_file_path


def create_prescription_pdf(presID):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()
        print("Connected to DB")


        # Take information from Prescriptions
        cursor.execute(""" SELECT * FROM Prescriptions WHERE presID = (?) """, (presID,))
        prs_info = cursor.fetchall()

        if prs_info[0][2] == 'medicine':
            mode = 'medicine'
            prescription_info_query = """ SELECT DISTINCT mi.presID, ti.patName, ti.patSurname, p.dateOfBirth, p.email, ti.docName, ti.docSurname, d.type, ti.locAddress, ti.slotDate, mi.medName, mi.medDose, mi.medCompany, mi.insType FROM MedicineInfo mi JOIN TerminInfo ti ON ti.termID = mi.termID JOIN Doctors d ON ti.docID = d.docID JOIN Patients p ON ti.patID = p.patID WHERE presID = (?) """
            cursor.execute(prescription_info_query, (presID,))

        elif prs_info[0][2] == 'redirection':
            mode = 'redirection'
            cursor.execute(""" SELECT DISTINCT p.presID, ti.patName, ti.patSurname, p.dateOfBirth, p.email, ti.docName, ti.docSurname, d1.type, ti.locAddress, ti.slotDate, d.name, d.surname, d.type FROM Prescriptions p JOIN Redirections r ON p.presID = r.preID JOIN Doctors d ON d.docID = r.docID JOIN TerminInfo ti ON ti.termID = p.termID  JOIN Doctors d1 ON ti.docID = d1.docID  JOIN Patients p ON ti.patID = p.patID WHERE p.presID = (?) """, (presID,))

        else:
            raise "Wrong type of prescription! It should be either 'medicine' or 'redirection'"

        output_file_path = prescription_to_pdf(cursor.fetchall(), mode)

        sqliteConnection.commit()

        attach_file_to_termin(prs_info[0][1], output_file_path)

        print("Prescription creating proccess is finished successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to create prescription", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def upcoming_termin_reminder(user_type, user_id):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()

        print("Connected to DB")

        next_day_date = date.today() + timedelta(days=1)
        formatted_next_day_date = next_day_date.strftime("%Y-%m-%d")

        # formatted_next_day_date = '2024-06-25'

        if user_type == 'doc':
            update_query = f""" SELECT DISTINCT patName, patSurname, docName, docSurname, locAddress, slotTime FROM TerminInfo WHERE docID = (?) AND slotDate = (?) """
        else:
            update_query = f""" SELECT DISTINCT patName, patSurname, docName, docSurname, locAddress, slotTime FROM TerminInfo WHERE patID = (?) AND slotDate = (?)"""

        user_id_tuple = (user_id, formatted_next_day_date)
        cursor.execute(update_query, user_id_tuple)
        termins = [list(tup) for tup in cursor.fetchall()]

        if len(termins) != 0:
            messages = [f'You have an appointment tomorrow! Patient: {term[0]} {term[1]} Time:{term[-1]}, Location:{term[-2]}, Doctor: {term[2]} {term[3]}' for term in termins]
            for message in messages:
                cursor.execute(""" INSERT INTO Notification(userType, userID, message) VALUES (?,?,?)  """, (user_type, user_id, message))

        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to create list of upcoming termins", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def termin_status_changing_storing(slot_id, user_type, user_id, event):
    try:
        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()

        print("Connected to DB")

        if user_type == 'doc':
            update_query = f""" SELECT DISTINCT patName, patSurname, docName, docSurname, locAddress, slotTime FROM TerminInfo WHERE slotID = (?) """''
        else:
            update_query = f""" SELECT DISTINCT patName, patSurname, docName, docSurname, locAddress, slotTime FROM TerminInfo WHERE slotID = (?)"""

        user_id_tuple = (slot_id, )
        cursor.execute(update_query, user_id_tuple)
        termin = list(cursor.fetchall())
        termin = termin[0]

        if event == 'delete':
            message = f'Your appointment has been deleted! Patient: {termin[0]} {termin[1]} Time:{termin[-1]}, Location:{termin[-2]}, Doctor: {termin[2]} {termin[3]}'
        elif event == 'create':
            message = f'You have new appointment! Patient: {termin[0]} {termin[1]} Time:{termin[-1]}, Location:{termin[-2]}, Doctor: {termin[2]} {termin[3]}'

        cursor.execute(""" INSERT INTO Notification(userType, userID, message) VALUES (?,?,?)  """, (user_type, user_id,message))

        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to change termin status", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def check_notification(user_id, user_type):
    try:
        upcoming_termin_reminder(user_type, user_id)

        sqliteConnection = sqlite3.connect('Test.db')
        cursor = sqliteConnection.cursor()

        print("Connected to DB")

        cursor.execute(""" SELECT DISTINCT notID, message FROM Notification WHERE userType = (?) AND userID = (?) """, (user_type, user_id))
        notifications = [list(tup) for tup in cursor.fetchall()]

        for notification in notifications:
            cursor.execute(""" DELETE FROM Notification WHERE notID = (?) """, (notification[0],))

        sqliteConnection.commit()
        cursor.close()

        return notifications

    except sqlite3.Error as error:
        print("Failed to check notifications", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


check_notification(1, 'pat')
check_notification(1, 'doc')