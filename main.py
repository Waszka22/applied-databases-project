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
        print("6 - View Rooms")
        print("x - Exit")

        choice = input("Choice: ").strip().lower()

        if choice == "1":
            view_speakers_sessions()

        elif choice == "6":
            view_rooms()

        elif choice == "x":
            print("Goodbye!")
            break

        else:
            print("Invalid option")


main()