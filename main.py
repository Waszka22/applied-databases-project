import pymysql


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
        print("\nNo speakers found.")
        print("Tip: try a single letter, for example: a")
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


def view_rooms():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT roomID, roomName, capacity FROM room")
    rooms = cursor.fetchall()

    print("\nRooms")
    print("-" * 40)

    for room in rooms:
        print(f"Room ID: {room[0]}")
        print(f"Room Name: {room[1]}")
        print(f"Capacity: {room[2]}")
        print("-" * 40)

    cursor.close()
    conn.close()


def main():
    while True:
        print("\nMENU")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("6 - View Rooms")
        print("x - Exit")

        choice = input("Choice: ").strip().lower()

        if choice == "1":
            view_speakers_sessions()

        elif choice == "2":
            view_attendees_by_company()

        elif choice == "6":
            view_rooms()

        elif choice == "x":
            print("Goodbye!")
            break

        else:
            print("Invalid option")


main()