import os
from dotenv import load_dotenv, find_dotenv
from neo4j import GraphDatabase

# Importiere Funktionen zum Generieren von Schlüsselwörtern und zur Antwortgenerierung
from question_answering.createKeywords import generate_keywords
from question_answering.crateFinalAnswer import generate_answer

# Lade Umgebungsvariablen (z.B. für die Neo4j-Verbindung)
_ = load_dotenv(find_dotenv())

# Lese Verbindungsparameter für Neo4j aus den Umgebungsvariablen
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

# Erstelle den Neo4j-Datenbanktreiber
driver = GraphDatabase.driver(uri, auth=(username, password))

def search_nodes_by_keywords(keywords):
    """
    Durchsucht die Neo4j-Datenbank nach Knoten, deren 'name' eines der angegebenen Schlüsselwörter enthält.
    Für jeden gefundenen Knoten werden alle verbundenen Relationen und Nachbarknoten ermittelt.
    
    :param keywords: Eine Liste von Schlüsselwörtern.
    :return: Ein formatierter Text mit den Suchergebnissen.
    """
    results_text = ""

    with driver.session() as session:
        # Iteriere über alle Schlüsselwörter
        for keyword in keywords:
            # Suche nach Knoten, deren Name das Stichwort (unabhängig von Groß-/Kleinschreibung) enthält
            matching_nodes = session.run(
                """
                MATCH (n)
                WHERE toLower(n.name) CONTAINS toLower($kw)
                RETURN DISTINCT n
                """,
                kw=keyword
            ).values()

            results_text += f"\n\n--- Ergebnisse für Stichwort: '{keyword}' ---\n"

            # Falls keine Knoten gefunden wurden, füge einen entsprechenden Hinweis hinzu
            if not matching_nodes:
                results_text += "Keine passenden Knoten gefunden.\n"
                continue

            # Für jeden gefundenen Knoten:
            for (found_node,) in matching_nodes:
                node_name = found_node["name"]
                
                # Suche nach allen ausgehenden und eingehenden Beziehungen des Knotens
                records = session.run(
                    """
                    MATCH (n)-[r]->(m)
                    WHERE id(n) = $nodeId
                    RETURN r, n AS startNode, m AS endNode
                    UNION
                    MATCH (n)<-[r]-(m)
                    WHERE id(n) = $nodeId
                    RETURN r, m AS startNode, n AS endNode
                    """,
                    nodeId=found_node.id
                ).values()

                if not records:
                    results_text += f"Knoten (kein Nachbar gefunden): {node_name}\n"
                    continue

                # Füge für jede Beziehung eine Zeile mit Startknoten, Beziehungstyp und Endknoten hinzu
                for (rel_obj, start_node, end_node) in records:
                    start_name = start_node["name"]
                    end_name   = end_node["name"]
                    rel_type   = rel_obj.type

                    results_text += f"{start_name} --[:{rel_type}]--> {end_name}\n"

    return results_text

def run_question_answering(user_question):
    """
    Führt den gesamten Frage-Antwort-Prozess durch:
    1. Generiert Schlüsselwörter aus der Frage.
    2. Durchsucht den Knowledge Graph anhand dieser Schlüsselwörter.
    3. Generiert eine finale Antwort basierend auf den gefundenen Relationen.
    
    :param user_question: Die vom Benutzer gestellte Frage.
    :return: Die generierte Antwort.
    """
    # 1) Generiere Schlüsselwörter aus der Frage
    keywords_str = generate_keywords(user_question)
    keywords = [keyword.strip() for keyword in keywords_str.split(",")]

    # 2) Suche im Graphen anhand der generierten Schlüsselwörter
    relations_text = search_nodes_by_keywords(keywords)
    
    # 3) Generiere eine finale Antwort unter Berücksichtigung der gefundenen Relationen
    final_answer = generate_answer(user_question, relations_text)
    
    # Schließe die Datenbankverbindung
    driver.close()

    return final_answer

if __name__ == "__main__":
    # Beispielhafter Direktaufruf der Funktion
    test_question = "What has happened to Ukrainian energy facilities?"
    answer = run_question_answering(test_question)
    print("Test-Antwort:", answer)
