import os
import re
import json

# Importiere die OpenAI-Funktion, die im api_call-Modul definiert ist
from api.api_call import get_completion

def generate_cypher_queries(text):
    """
    Extrahiert Triplets aus dem übergebenen Text, indem ein Prompt an GPT gesendet wird.
    Die Triplets werden anschließend in Cypher-Abfragen umgewandelt.
    
    :param text: Der zu verarbeitende Text.
    :return: Eine Liste von Cypher-Abfragen als Strings.
    """
    # Erstelle einen Prompt, der GPT anweist, relevante Triplets zu extrahieren
    prompt = f"""
    Analysiere den folgenden Text und extrahiere alle relevanten Beziehungen,
    formatiert als Triplets im folgenden Format:

    <triplet><subj>Subject</subj><obj>Object</obj><rel>Relationship</rel></triplet>

    Text: {text}

    Richtlinien:
    1. Identifiziere pro Satz mindestens 3 verschiedene, relevante Beziehungen.
    2. Konzentriere dich auf geopolitische, wirtschaftliche und diplomatische Verbindungen.
    3. Die Beziehungen sollen klar, prägnant und faktisch sein.
    4. Berücksichtige Beziehungen zwischen Ländern, politischen Figuren, Organisationen und Schlüsselaspekten.
    5. Verwende einfache, direkte Formulierungen (z.B. "ist Präsident von", "grenzt an", "widersetzt sich", "unterstützt").
    6. Vermeide zu ausführliche oder komplexe Beschreibungen.
    7. Jedes Triplet soll einen vollständigen, eigenständigen Fakt darstellen.

    Beispiele für Beziehungstypen:
    - Politische Führung
    - Geographische Verbindungen
    - Wirtschaftliche Beziehungen
    - Diplomatische Positionen
    - Militärische Allianzen
    - Historische Kontexte

    Extrahiere alle relevanten Beziehungen aus dem Text und priorisiere Genauigkeit und Relevanz.
    """

    # Sende den Prompt an das OpenAI-API und erhalte die Triplets als Antwort
    triplets = get_completion(prompt)
    # Wandle die erhaltenen Triplets in Cypher-Abfragen um
    return generate_cypher_from_triplets(triplets)

def generate_cypher_from_triplets(triplets):
    """
    Parst die von GPT zurückgegebenen Triplets mittels Regex und erstellt
    für jedes Triplet eine einzelne Cypher-Abfrage.
    
    :param triplets: Der von GPT zurückgegebene Text mit Triplets.
    :return: Eine Liste von Cypher-Abfragen.
    """
    # Regex-Muster zum Extrahieren von Subjekt, Objekt und Beziehung
    pattern = r"<triplet><subj>(.*?)</subj><obj>(.*?)</obj><rel>(.*?)</rel></triplet>"
    matches = re.findall(pattern, triplets, flags=re.DOTALL)

    cypher_queries = []
    for subj, obj, rel in matches:
        # Bereinige die Werte für die Verwendung in Cypher-Abfragen
        rel_sanitized = sanitize_for_cypher_rel(rel)
        subj_sanitized = sanitize_for_cypher_node(subj)
        obj_sanitized  = sanitize_for_cypher_node(obj)

        # Escape die Werte als JSON-Strings, um Sonderzeichen korrekt zu behandeln
        subj_escaped = json.dumps(subj_sanitized)
        obj_escaped  = json.dumps(obj_sanitized)

        # Erstelle das Cypher-Statement
        cypher_query = f"""
            MERGE (a:Person {{name: {subj_escaped}}})
            MERGE (b:Person {{name: {obj_escaped}}})
            MERGE (a)-[:{rel_sanitized}]->(b)
        """
        cypher_queries.append(cypher_query.strip())

    return cypher_queries

def sanitize_for_cypher_rel(input_string):
    """
    Bereinigt den Beziehungstext, indem alle nicht alphanumerischen Zeichen durch Unterstriche ersetzt werden.
    Das Ergebnis wird in Großbuchstaben zurückgegeben.
    
    :param input_string: Der ursprüngliche Beziehungstext.
    :return: Der bereinigte Text.
    """
    out = re.sub(r'[^A-Za-z0-9_]+', '_', input_string)
    return out.upper()

def sanitize_for_cypher_node(input_string):
    """
    Bereinigt den Knotennamen, indem alle nicht alphanumerischen Zeichen durch Unterstriche ersetzt werden.
    
    :param input_string: Der ursprüngliche Knotentext.
    :return: Der bereinigte Text.
    """
    out = re.sub(r'[^A-Za-z0-9_]+', '_', input_string)
    return out

# Optionaler Testaufruf, um die Funktionalität zu überprüfen
if __name__ == "__main__":
    test_text = "Russia launched missile strikes against Ukraine."
    queries = generate_cypher_queries(test_text)
    print("**Generierte Cypher-Abfragen**")
    for q in queries:
        print(q)
