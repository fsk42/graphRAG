# src/knowledge_graph_creation/createTriplets.py

import os
import re
import json

# Wichtig: Ausgelagerte OpenAI-Funktion
from src.api.api_call import get_completion

def generate_cypher_queries(text):
    """
    1) Erstellt einen Prompt, um aus dem Text in 'text' Triplets zu extrahieren.
    2) Fragt GPT, um Triplets im Format <triplet><subj>...</subj><obj>...</obj><rel>...</rel></triplet> zu bekommen.
    3) Wandelt jedes Triplet in ein Cypher-Statement um.
    4) Gibt die Liste aller generierten Statements zurück.
    """
    prompt = f"""
    Analyze the following text and extract all relevant relationships, 
    formatting them as triplets:

    <triplet><subj>Subject</subj><obj>Object</obj><rel>Relationship</rel></triplet>

    Text: {text}

    Guidelines:
    1. Identify at least 3 distinct, relevant relationships per chunk (1 sentence).
    2. Focus on geopolitical, economic, and diplomatic connections.
    3. Relationships should be clear, concise, and factual.
    4. Include relationships between countries, political figures, organizations, and key concepts.
    5. Use simple, direct phrases for relationships (e.g., "is president of", "shares border with", "opposes", "supports").
    6. Avoid overly verbose or complex relationship descriptions.
    7. Ensure each triplet represents a complete, standalone fact.

    Examples of relationship types to look for:
    - Political leadership
    - Geographical
    - Economic ties
    - Diplomatic stances
    - Military alliances
    - Historical context

    Extract all relevant relationships from the text, prioritizing accuracy and relevance 
    to the text's main themes.
    """

    # GPT-Aufruf über get_completion()
    triplets = get_completion(prompt)
    return generate_cypher_from_triplets(triplets)

def generate_cypher_from_triplets(triplets):
    """
    Parst die Triplets via Regex aus dem GPT-Resultat und 
    baut für jedes Triplet ein einzelnes Cypher-Query-Statement.
    """
    pattern = r"<triplet><subj>(.*?)</subj><obj>(.*?)</obj><rel>(.*?)</rel></triplet>"
    matches = re.findall(pattern, triplets, flags=re.DOTALL)

    cypher_queries = []
    for subj, obj, rel in matches:
        rel_sanitized = sanitize_for_cypher_rel(rel)
        subj_sanitized = sanitize_for_cypher_node(subj)
        obj_sanitized  = sanitize_for_cypher_node(obj)

        subj_escaped = json.dumps(subj_sanitized)
        obj_escaped  = json.dumps(obj_sanitized)

        cypher_query = f"""
            MERGE (a:Person {{name: {subj_escaped}}})
            MERGE (b:Person {{name: {obj_escaped}}})
            MERGE (a)-[:{rel_sanitized}]->(b)
        """
        cypher_queries.append(cypher_query.strip())

    return cypher_queries

def sanitize_for_cypher_rel(input_string):
    out = re.sub(r'[^A-Za-z0-9_]+', '_', input_string)
    return out.upper()

def sanitize_for_cypher_node(input_string):
    out = re.sub(r'[^A-Za-z0-9_]+', '_', input_string)
    return out

# Optionaler Testaufruf
if __name__ == "__main__":
    test_text = "Russia launched missile strikes against Ukraine."
    queries = generate_cypher_queries(test_text)
    print("**Generated Cypher Queries**")
    for q in queries:
        print(q)
