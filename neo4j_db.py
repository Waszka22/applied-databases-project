# Neo4j datavase functions for attendee conection

from neo4j import GraphDatabase

# ---------- Neo4j Database Connection ----------
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "Korek2204@"

# Create Neo4j driver connection
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# ---------- Check If Attendee Exists In Neo4j ----------
def attendee_node_exists(attendee_id):
    with driver.session() as session:
        query = """
        MATCH (a:Attendee {AttendeeID: $id})
        RETURN a
        """

        result = session.run(query, id=int(attendee_id))
        return result.single() is not None
    
# ---------- Get Connected Attendees ----------
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

# ---------- Check If Connection Exists ----------
def connection_exists(id1, id2):
    with driver.session() as session:
        query = """
        MATCH (a:Attendee {AttendeeID: $id1})-[:CONNECTED_TO]-(b:Attendee {AttendeeID: $id2})
        RETURN a
        """
        result = session.run(query, id1=int(id1), id2=int(id2))
        return result.single() is not None


# ---------- Add New Connection ----------
def add_connection(id1, id2):
    with driver.session() as session:
        query = """
        MERGE (a:Attendee {AttendeeID: $id1})
        MERGE (b:Attendee {AttendeeID: $id2})
        MERGE (a)-[:CONNECTED_TO]-(b)
        """
        session.run(query, id1=int(id1), id2=int(id2))




  # Ref: https://neo4j.com/docs/python-manual/current/connect/      