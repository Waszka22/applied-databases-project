# ---------- MySQL Database Connection ----------
import pymysql


def get_connection():

    # Create connection to MySQL database
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="appdbproj",
        port=3306,
        connect_timeout=5
    )


# ---------- Get Attendee Name ----------
def get_attendee_name(attendee_id):

    # Connect to MySQL database
    conn = get_connection()
    # Create cursor object
    cursor = conn.cursor()
    # SQL query to retrieve attendee name by ID
    cursor.execute(
        "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
        (attendee_id,)
    )

    attendee = cursor.fetchone()

    # Close database connection
    cursor.close()
    conn.close()

    return attendee


# ---------- Check If Attendee Exists ----------
def attendee_exists(attendee_id):
    # Connect to MySQL database
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT attendeeID FROM attendee WHERE attendeeID = %s",
        (attendee_id,)
    )

    result = cursor.fetchone()
    # Close database connection
    cursor.close()
    conn.close()

    return result is not None


# ---------- Get Attendees By Company ----------
def get_attendees_by_company(company_id: int):

    """
    Returns a list of attendees belonging to a specific company.

    """
    # Connect to MySQL database
    conn = get_connection()
    # Create cursor object
    cursor = conn.cursor()
    cursor.execute(

        "SELECT attendeeID, attendeeName FROM attendee WHERE attendeeCompanyID = %s",

        (company_id,)

    )

    results = cursor.fetchall()

    # Close database connection
    cursor.close()
    conn.close()

    return results