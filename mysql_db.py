
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


def get_attendee_name(attendee_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
        (attendee_id,)
    )

    attendee = cursor.fetchone()

    cursor.close()
    conn.close()

    return attendee


def attendee_exists(attendee_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT attendeeID FROM attendee WHERE attendeeID = %s",
        (attendee_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None



def get_attendees_by_company(company_id: int):

    """
    Returns a list of attendees belonging to a specific company.

    """
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT attendeeID, attendeeName FROM attendee WHERE attendeeCompanyID = %s",

        (company_id,)

    )

    results = cursor.fetchall()

    cursor.close()

    conn.close()

    return results