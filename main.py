from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Verbindungsparameter aus der .env-Datei laden
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")  # Fallback-Wert, falls nicht in der .env-Datei vorhanden
username = os.getenv("NEO4J_USERNAME", "neo4j")        # Fallback-Wert
password = os.getenv("NEO4J_PASSWORD")    # Fallback-Wert

# Verbindung herstellen
driver = GraphDatabase.driver(uri, auth=(username, password))

# Funktion zum Ausführen von Cypher-Abfragen
def run_cypher_queries(cypher_queries):
    with driver.session() as session:
        session.run(cypher_queries)
        print("Beispieldaten erfolgreich erstellt!")

# Beispiel: Cypher-Abfragen von OpenAI generieren und ausführen
from apiAnfrage import generate_cypher_queries

cypher_queries = generate_cypher_queries()
run_cypher_queries(cypher_queries)

# Funktion zum Abfragen der Knoten
def query_nodes():
    with driver.session() as session:
        result = session.run("MATCH (n:Person) RETURN n.name AS name, n.age AS age")
        print("Abfrageergebnisse:")
        for record in result:
            print(f"Name: {record['name']}, Alter: {record['age']}")

# Beispielknoten abfragen
query_nodes()

# Verbindung schließen, wenn du fertig bist
driver.close()
