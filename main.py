import pymysql
from neo4j_db import get_connected_attendees, add_connection, connection_exists
from mysql_db import get_attendee_name, attendee_exists

ROOM_CACHE = None


def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="appdbproj",
        port=3306,
        connect_timeout=5
    )


def view_speakers_sessions():
    search = input("Enter speaker name or part of name: ")

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
        print("\nNo speaker match search string.")
    else:
        print("\nSpeaker Sessions")
        print("-" * 40)

        for row in results:
            print(f"Speaker: {row[0]}")
            print(f"Session: {row[1]}")
            print(f"Room: {row[2]}")
            print("-" * 40)

    cursor.close()
    conn.close()


def view_attendees_by_company():
    while True:
        company_input = input("Enter Company ID: ").strip()

        if not company_input.isdigit() or int(company_input) <= 0:
            print("Invalid Company ID. Please enter a number greater than 0.")
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
            print("Company does not exist.")
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
            continue

        print(f"\nAttendees from {company_name}")
        print("-" * 50)

        for attendee in attendees:
            print(f"Name: {attendee[0]}")
            print(f"DOB: {attendee[1]}")
            print(f"Session: {attendee[2]}")
            print(f"Speaker: {attendee[3]}")
            print(f"Room: {attendee[4]}")
            print("-" * 50)

        cursor.close()
        conn.close()
        break


def add_new_attendee():
    attendee_id = input("Enter Attendee ID: ").strip()
    name = input("Enter Attendee Name: ").strip()
    dob = input("Enter DOB (YYYY-MM-DD): ").strip()
    gender = input("Enter Gender (M/F): ").strip().upper()
    company_id = input("Enter Company ID: ").strip()


    if not attendee_id.isdigit():

        print("Invalid Attendee ID.")

        return

    if not company_id.isdigit():

        print("Invalid Company ID.")

        return

    if gender not in ["M", "F"]:
        print("Invalid gender.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT attendeeID FROM attendee WHERE attendeeID = %s",
            (attendee_id,)
        )

        if cursor.fetchone() is not None:
            print("Attendee ID already exists.")
            return

        cursor.execute(
            "SELECT companyID FROM company WHERE companyID = %s",
            (company_id,)
        )

        if cursor.fetchone() is None:
            print("Invalid Company ID.")
            return

        query = """
            INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (attendee_id, name, dob, gender, company_id))
        conn.commit()

        print("Attendee successfully added.")

    except Exception as e:
        print("Database error:", e)

    finally:
        cursor.close()
        conn.close()


def view_connected_attendees():
    attendee_id = input("Enter Attendee ID: ").strip()

    if not attendee_id.isdigit():
        print("Invalid attendee ID.")
        return

    attendee = get_attendee_name(attendee_id)

    if attendee is None:
        print("Attendee does not exist.")
        return

    connections = get_connected_attendees(attendee_id)

    print(f"\nAttendee: {attendee[0]}")

    if not connections:
        print("No connections.")
    else:
        for c in connections:
            print(f"Connected to ID {c['id']}")


def add_attendee_connection():
    id1 = input("Enter first Attendee ID: ").strip()
    id2 = input("Enter second Attendee ID: ").strip()

    if not id1.isdigit() or not id2.isdigit():
        print("Invalid attendee ID.")
        return

    if id1 == id2:
        print("An attendee cannot be connected to themselves.")
        return

    if not attendee_exists(id1) or not attendee_exists(id2):
        print("One or both attendees do not exist.")
        return

    if connection_exists(id1, id2):
        print("These attendees are already connected.")
        return

    add_connection(id1, id2)
    print("Connection successfully added.")


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


def main():
    while True:
        print("\nMENU")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("x - Exit")

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

        elif choice == "x":
            print("Goodbye!")
            break

        else:
            print("Invalid option")


main()