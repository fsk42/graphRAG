import openai
from openai import OpenAI
import os
import re
import dotenv
from dotenv import load_dotenv, find_dotenv

# Ermittle das Verzeichnis, in dem das aktuelle Skript liegt
script_dir = os.path.dirname(os.path.abspath(__file__))

# Lege den Dateinamen fest (hier "chunk.txt")
chunk_file = os.path.join(script_dir, "chunk.txt")

# Lese den Inhalt der Datei in die Variable "chunk"
with open(chunk_file, "r", encoding="utf-8") as f:
    chunk = f.read()

_ = load_dotenv(find_dotenv())  # .env-Datei laden
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def get_completion(prompt, model='gpt-3.5-turbo'):
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=250,
    )
    return completion.choices[0].message.content

# Beispiel: Prompt für Cypher-Queries
def generate_cypher_queries():
    prompt = f"""
    Analyze the following text and extract all relevant relationships, formatting them as triplets:

    <triplet><subj>Subject</subj><obj>Object</obj><rel>Relationship</rel></triplet>

    Text: {chunk}

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

    Extract all relevant relationships from the text, prioritizing accuracy and relevance to the text's main themes.
    """

    # Antwort von OpenAI einholen
    triplets = get_completion(prompt)
    
    # Cypher-Queries aus den Triplets erstellen
    return generate_cypher_from_triplets(triplets)

def generate_cypher_from_triplets(triplets):
    cypher_queries = []

    # Regex, um Triplets im Antworttext zu finden
    triplet_pattern = r"<triplet><subj>(.*?)</subj><obj>(.*?)</obj><rel>(.*?)</rel></triplet>"
    matches = re.findall(triplet_pattern, triplets)

    for subj, obj, rel in matches:
        # Für jedes Triplet Cypher-Queries generieren
        cypher_query = f"""
        MERGE (a:{subj.replace(' ', '_')} {{name: '{subj}'}})
        MERGE (b:{obj.replace(' ', '_')} {{name: '{obj}'}})
        MERGE (a)-[:{rel.replace(' ', '_').upper()}]->(b)
        """
        cypher_queries.append(cypher_query.strip())

    return "\n".join(cypher_queries)

# Aufruf der Funktionen
if __name__ == "__main__":
    cypher_queries = generate_cypher_queries()
    print("Generated Cypher Queries:")
    print(cypher_queries)
