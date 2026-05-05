
from neo4j import GraphDatabase


URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "Korek2204@"  


driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def get_connected_attendees(attendee_id):
    with driver.session() as session:
        query = """
        MATCH (a:Attendee {AttendeeID: $id})
        OPTIONAL MATCH (a)-[:CONNECTED_TO]-(b:Attendee)
        RETURN b.AttendeeID AS id
        """

        result = session.run(query, id=int(attendee_id))

        connections = []
        for record in result:
            if record["id"] is not None:
                connections.append({"id": record["id"]})

        return connections