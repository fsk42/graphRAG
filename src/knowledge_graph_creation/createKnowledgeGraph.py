import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Lade Umgebungsvariablen (z.B. für die Neo4j-Verbindung)
load_dotenv()

# Lese Verbindungsparameter für Neo4j aus den Umgebungsvariablen
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

# Erstelle den Neo4j-Datenbanktreiber
driver = GraphDatabase.driver(uri, auth=(username, password))

# Importiere die Funktion zur Generierung von Cypher-Abfragen
from .createTriplets import generate_cypher_queries

def run_cypher_queries(cypher_queries):
    """
    Führt alle übergebenen Cypher-Abfragen in der Neo4j-Datenbank aus.
    
    :param cypher_queries: Liste von Cypher-Abfragen als Strings.
    """
    with driver.session() as session:
        for query in cypher_queries:
            session.run(query)
        print("Alle Cypher-Statements wurden erfolgreich ausgeführt!")

def query_nodes():
    """
    Führt eine Beispielabfrage aus, um alle Knoten mit Label 'Person' und deren Namen anzuzeigen.
    """
    with driver.session() as session:
        result = session.run("MATCH (n:Person) RETURN n.name AS name")
        print("Abfrageergebnisse (Personen):")
        for record in result:
            print(f"Name: {record['name']}")

def create_knowledge_graph(question: str):
    """
    Erstellt den Knowledge Graph, indem alle Textdateien aus dem data-Ordner verarbeitet werden.
    Für jede Datei werden Triplets generiert und in die Datenbank geschrieben.
    
    :param question: Die vom Benutzer gestellte Frage (wird aktuell nur protokolliert).
    """
    # Bestimme den Pfad zum data-Ordner (zwei Ebenen über dem aktuellen Verzeichnis)
    data_folder = os.path.join(os.path.dirname(__file__), "..", "..", "data")

    # Iteriere über alle .txt-Dateien im data-Ordner
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_folder, filename)
            print(f"\nVerarbeite Datei: {file_path}")

            # Lese den Inhalt der Datei ein
            with open(file_path, "r", encoding="utf-8") as f:
                text_content = f.read()
            print(text_content)

            # Generiere Cypher-Abfragen aus dem Textinhalt
            cypher_queries = generate_cypher_queries(text_content)
            print(cypher_queries)

            # Führe die generierten Cypher-Abfragen in der Neo4j-Datenbank aus
            run_cypher_queries(cypher_queries)

    # Führe eine Beispielabfrage durch, um alle 'Person'-Knoten anzuzeigen
    query_nodes()
    # Schließe die Datenbankverbindung
    driver.close()

if __name__ == "__main__":
    create_knowledge_graph("Beispiel-Frage")
