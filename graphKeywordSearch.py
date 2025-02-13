# graphKeywordSearch.py

import os
from dotenv import load_dotenv, find_dotenv
from neo4j import GraphDatabase

# Importiere die Funktion generate_keywords aus questionToKeyword.py
from questionToKeyword import generate_keywords

_ = load_dotenv(find_dotenv())

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

driver = GraphDatabase.driver(uri, auth=(username, password))

def search_nodes_by_keywords(keywords):
    """
    Durchsucht die Knoten, deren `n.name` eines der Stichwörter enthält,
    und gibt für jeden Knoten alle gerichteten Relationen + Nachbarknoten zurück.
    Die Richtung wird immer exakt so ausgegeben, wie sie in Neo4j gespeichert ist:
      (start_node) --[:RELATION]--> (end_node).
    """
    results_text = ""

    with driver.session() as session:
        for keyword in keywords:
            # 1) Alle Knoten finden, die das Keyword enthalten
            matching_nodes = session.run(
                """
                MATCH (n)
                WHERE toLower(n.name) CONTAINS toLower($kw)
                RETURN DISTINCT n
                """,
                kw=keyword
            ).values()

            results_text += f"\n\n--- Ergebnisse für Stichwort: '{keyword}' ---\n"

            if not matching_nodes:
                results_text += "Keine passenden Knoten gefunden.\n"
                continue

            # 2) Für jeden dieser Knoten alle Relationen + Nachbarn abfragen
            for (found_node,) in matching_nodes:
                node_name = found_node["name"]
                
                # Hole alle Relationen, an denen dieser Knoten beteiligt ist
                # Egal ob in Richtung (n)->(m) oder (m)->(n)
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

                # 3) Beziehungen mit korrekter Richtung ausgeben
                for (rel_obj, start_node, end_node) in records:
                    start_name = start_node["name"]
                    end_name   = end_node["name"]
                    rel_type   = rel_obj.type

                    # Hier wird immer die tatsächliche Richtung aus Neo4j abgebildet
                    results_text += f"{start_name} --[:{rel_type}]--> {end_name}\n"

    return results_text


if __name__ == "__main__":
    # Statt fester Stichwörter, rufe generate_keywords() auf
    keywords_str = generate_keywords()
    # Es wird angenommen, dass generate_keywords() eine kommaseparierte Zeichenkette zurückgibt.
    keywords = [keyword.strip() for keyword in keywords_str.split(",")]

    result_text = search_nodes_by_keywords(keywords)

    with open("search_results.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    print("Ergebnisse in 'search_results.txt' gespeichert.")
    driver.close()
