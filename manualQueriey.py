from neo4j import GraphDatabase

# Verbindungsparameter
uri = "bolt://localhost:7687"  # Standard-Bolt-Port
username = "neo4j"             # Standard-Benutzername
password = "Trüffelöl"     # Ersetze dies durch das Passwort, das du beim Anlegen des DBMS festgelegt hast

# Verbindung herstellen
driver = GraphDatabase.driver(uri, auth=(username, password))

# Funktion zum Erstellen von Knoten
def create_nodes():
    with driver.session() as session:
        session.run("""
                    
         
        MERGE (a:Person {name: 'Russian_forces'})
        MERGE (b:Person {name: 'Ukrainian_energy_infrastructure'})
        MERGE (a)-[:TARGETING]->(b)
        

        MERGE (c:Person {name: 'Russian_forces'})
        MERGE (d:Person {name: 'Ukrainian_air_defense_umbrella'})
        MERGE (c)-[:EXPLOITING]->(d)
        

        """)
        print("russland knoten erstellt!")

# löschen: MATCH (n)
#          DETACH DELETE n;

# Funktion zum Abfragen der Knoten
def query_nodes():
    with driver.session() as session:
        result = session.run("MATCH (n:Person) RETURN n.name AS name, n.age AS age")
        print("Abfrageergebnisse:")
        for record in result:
            print(f"Name: {record['name']}, Alter: {record['age']}")

# Beispielknoten erstellen
create_nodes()

# Beispielknoten abfragen
query_nodes()

# Verbindung schließen, wenn du fertig bist
driver.close()
