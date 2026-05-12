# Applied Databases Project
# Conference Management System

import pymysql
from neo4j_db import get_connected_attendees, add_connection, connection_exists, driver
from mysql_db import get_attendee_name, attendee_exists
from datetime import datetime

ROOM_CACHE = None

# ---------- MYSQL Connection ---------
def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="appdbproj",
        port=3306,
        connect_timeout=5
    )

# ---------- 1. View Speakers & Sessions ----------
def view_speakers_sessions():

    search = input("\nEnter speaker name: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT s.speakerName, s.sessionTitle, r.roomName
        FROM session s
        JOIN room r ON s.roomID = r.roomID
        WHERE s.speakerName LIKE %s
    """

    cursor.execute(query, (f"%{search}%",))
    results = cursor.fetchall()

    if not results:
        print("\nNo speakers found of that name")
        print("-" * 55)

    else:
        print(f"\nSession Details For : {search}")
        print("-" * 55)

        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]}")

    cursor.close()
    conn.close()

# ---------- 2. View Attendees By Company ----------
def view_attendees_by_company():
    while True:
        company_input = input("Enter Company ID: ").strip()

        if not company_input.isdigit() or int(company_input) <= 0:
            print("Invalid Company ID")
            continue

        company_id = int(company_input)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT companyName FROM company WHERE companyID = %s",
            (company_id,)
        )

        company = cursor.fetchone()

        if company is None:
            print(f"Company with ID {company_id} doesn't exist")
            cursor.close()
            conn.close()
            continue

        company_name = company[0]

        query = """
            SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, r.roomName
            FROM attendee a
            JOIN registration reg ON a.attendeeID = reg.attendeeID
            JOIN session s ON reg.sessionID = s.sessionID
            JOIN room r ON s.roomID = r.roomID
            WHERE a.attendeeCompanyID = %s
        """

        cursor.execute(query, (company_id,))
        attendees = cursor.fetchall()

        if not attendees:
            print(f"No attendees found for {company_name}.")
            cursor.close()
            conn.close()
            break

        print(f"\n{company_name} Attendees")
        print("-" * 100)

        for attendee in attendees:
            print(
                f"{attendee[0]} | "
                f"{attendee[1]} | "
                f"{attendee[2]} | "
                f"{attendee[3]} | "
                f"{attendee[4]}"
            )

        cursor.close()
        conn.close()
        break


# ---------- 3. Add New Attendee ----------
def add_new_attendee():

    attendee_id = input("Enter Attendee ID: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT attendeeID FROM attendee WHERE attendeeID = %s",
            (attendee_id,)
        )

        if cursor.fetchone() is not None:
            print(f"*** ERROR *** Attendee ID: {attendee_id} already exists")
            return

        name = input("Enter Attendee Name: ").strip()
        dob = input("Enter DOB (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            print("*** ERROR *** Incorrect date value. Use YYYY-MM-DD format")
            return

        gender = input("Enter Gender (Male/Female): ").strip().capitalize()

        if gender not in ["Male", "Female"]:
            print("*** ERROR *** Gender must be Male or Female")
            return

        company_id = input("Enter Company ID: ").strip()

        if not company_id.isdigit():
            print(f"*** ERROR *** Company ID: {company_id} does not exist")
            return

        cursor.execute(
            "SELECT companyID FROM company WHERE companyID = %s",
            (company_id,)
        )

        if cursor.fetchone() is None:
            print(f"*** ERROR *** Company ID: {company_id} does not exist")
            return

        query = """
            INSERT INTO attendee
            (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (attendee_id, name, dob, gender, company_id))
        conn.commit()

        print("Attendee successfully added")

    except Exception as e:
        print("*** ERROR ***", e)

    finally:
        cursor.close()
        conn.close()


# ---------- 4. View Connected Attendees ----------
def view_connected_attendees():
    attendee_id = input("Enter Attendee ID: ").strip()

    if not attendee_id.isdigit():
        print("***ERROR*** Invalid attendee ID")
        return

    attendee = get_attendee_name(attendee_id)

    if attendee is None:
        print("***ERROR *** Attendee does not exist")
        return

    connections = get_connected_attendees(attendee_id)

    print(f"\nAttendee Name: {attendee[0]}")
    print("-" * 22)

    if not connections:
        print("No connections.")
    else:
        print("These attendees are connected:")

        for c in connections:
            connected_attendee = get_attendee_name(c["id"])

            if connected_attendee:
                print(f"{c['id']} | {connected_attendee[0]}")


# ---------- 5. Add Attendee Connection ----------
def add_attendee_connection():

    while True:
        id1 = input("Enter Attendee 1 ID: ").strip()
        id2 = input("Enter Attendee 2 ID: ").strip()

        if not id1.isdigit() or not id2.isdigit():
            print("*** ERROR *** Attendee IDs must be numbers")
            continue

        if id1 == id2:
            print("*** ERROR *** An attendee cannot connect to him/herself")
            continue

        if not attendee_exists(id1) or not attendee_exists(id2):
            print("*** ERROR *** One or both attendees do not exist")
            continue

        if connection_exists(id1, id2):
            print("*** ERROR *** Attendees are already connected")
            continue

        add_connection(id1, id2)
        print(f"Attendee {id1} is now connected to Attendee {id2}")
        break

# ---------- 6. View Rooms----------
def view_rooms():
    global ROOM_CACHE

    if ROOM_CACHE is None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT roomID, roomName, capacity FROM room")
        ROOM_CACHE = cursor.fetchall()

        cursor.close()
        conn.close()

    print("\nRooms")
    print("-" * 40)

    for room in ROOM_CACHE:
        print(f"Room ID: {room[0]}")
        print(f"Room Name: {room[1]}")
        print(f"Capacity: {room[2]}")
        print("-" * 40)


# ---------- 7. Innovation: Conference Dashboard ----------
def view_conference_dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM attendee")
        total_attendees = cursor.fetchone()[0]

        cursor.execute("""
            SELECT s.sessionTitle, COUNT(reg.attendeeID) AS registrations
            FROM session s
            LEFT JOIN registration reg ON s.sessionID = reg.sessionID
            GROUP BY s.sessionID, s.sessionTitle
            ORDER BY registrations DESC
            LIMIT 1
        """)
        top_session = cursor.fetchone()

        cursor.execute("""
            SELECT c.companyName, COUNT(a.attendeeID) AS attendees
            FROM company c
            LEFT JOIN attendee a ON c.companyID = a.attendeeCompanyID
            GROUP BY c.companyID, c.companyName
            ORDER BY attendees DESC
            LIMIT 1
        """)
        top_company = cursor.fetchone()

        print("\n" + "-" * 55)
        print("                 CONFERENCE DASHBOARD")
        print("-" * 55)

        print(f"Total Attendees        : {total_attendees}")

        if top_session:
            print(f"Most Popular Session   : {top_session[0]}")
            print(f"Session Registrations  : {top_session[1]}")
        else:
            print("Most Popular Session   : N/A")
            print("Session Registrations  : 0")

        if top_company:
            print(f"Top Company            : {top_company[0]}")
            print(f"Company Attendee Count : {top_company[1]}")
        else:
            print("Top Company            : N/A")
            print("Company Attendee Count : 0")

        print("-" * 55)

    except Exception as e:
        print("*** ERROR ***", e)

    finally:
        cursor.close()
        conn.close()


# ---------- 8.Innovation:Delete Attendee ----------
def delete_attendee():

    attendee_id = input("Enter Attendee ID to delete: ").strip()

    if not attendee_id.isdigit():
        print("*** ERROR *** Attendee ID must be numeric")
        return

    if not attendee_exists(attendee_id):
        print(f"*** ERROR *** Attendee ID: {attendee_id} does not exist")
        return

    confirm = input(f"Are you sure you want to delete attendee {attendee_id}? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Delete cancelled.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
       
        cursor.execute(
            "DELETE FROM registration WHERE attendeeID = %s",
            (attendee_id,)
        )

        cursor.execute(
            "DELETE FROM attendee WHERE attendeeID = %s",
            (attendee_id,)
        )

        conn.commit()

        with driver.session() as session:
            query = """
            MATCH (a:Attendee {AttendeeID: $id})
            DETACH DELETE a
            """

            session.run(query, id=int(attendee_id))

        print(f"Attendee {attendee_id} successfully deleted.")

    except Exception as e:
        print("*** ERROR ***", e)

    finally:
        cursor.close()
        conn.close()


# -------- Main Menu --------
def main():

    while True:

        print("\nConference Management")
        print("-" * 22)

        print("\nMENU")
        print("====")
        
        print("1 - View Speakers and Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("7 - View Conference Dashboard")
        print("8 - Delete Attendee")
        print("x - Exit application")

        choice = input("Choice: ").strip().lower()

        if choice == "1":
            view_speakers_sessions()

        elif choice == "2":
            view_attendees_by_company()

        elif choice == "3":
            add_new_attendee()

        elif choice == "4":
            view_connected_attendees()

        elif choice == "5":
            add_attendee_connection()

        elif choice == "6":
            view_rooms()
            
        elif choice == "7":
            view_conference_dashboard()

        elif choice == "8":
            delete_attendee()    

        elif choice == "x":
            print("Goodbye!")
            break

        else:
            print("Invalid option")


main()



