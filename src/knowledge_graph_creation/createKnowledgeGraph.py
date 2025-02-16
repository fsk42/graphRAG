# src/knowledge_graph_creation/createKnowledgeGraph.py

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(username, password))

def run_cypher_queries(cypher_queries):
    """
    Führt eine Liste von Cypher-Statements einzeln aus.
    So werden Variablen-Konflikte bei 'a' und 'b' vermieden, 
    und wir umgehen Syntaxfehler durch mehrfaches DECLARE.
    """
    with driver.session() as session:
        for query in cypher_queries:
            session.run(query)
        print("Alle Cypher-Statements erfolgreich ausgeführt!")

# Importiere die Funktion zum Generieren der Queries
from src.knowledge_graph_creation.createTriplets import generate_cypher_queries

if __name__ == "__main__":
    # Pfad zum Datenordner (ggf. anpassen)
    data_folder = os.path.join(os.path.dirname(__file__), "..", "..", "data")

    # Liste alle Dateien im Ordner data/ auf
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_folder, filename)
            print(f"\nVerarbeite Datei: {file_path}")

            # 1) Lese den Text aus der Datei
            with open(file_path, "r", encoding="utf-8") as f:
                text_content = f.read()

            print(text_content)

            # 2) Generiere pro Textdatei neue Cypher-Statements
            cypher_queries = generate_cypher_queries(text_content)
            print(cypher_queries)

            # 3) Führe sie in der DB aus
            run_cypher_queries(cypher_queries)

    # Beispiel: Abfrage der neu erstellten Person-Knoten
    def query_nodes():
        with driver.session() as session:
            result = session.run("MATCH (n:Person) RETURN n.name AS name")
            print("Abfrageergebnisse (Personen):")
            for record in result:
                print(f"Name: {record['name']}")

    query_nodes()
    driver.close()
