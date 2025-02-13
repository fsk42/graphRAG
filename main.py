from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Default-Verbindungsparameter (oder aus .env)
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
from Taiwan_apiAnfrageGPT import generate_cypher_queries

if __name__ == "__main__":
    # 1) Generiere eine Liste einzelner Cypher-Statements
    cypher_queries = generate_cypher_queries()

    # 2) Führe sie in einer Schleife aus
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
