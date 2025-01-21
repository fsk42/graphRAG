import openai
from openai import OpenAI
import os
import dotenv
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def get_completion(prompt, model='gpt-3.5-turbo'):
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=250,
    )
    return completion.choices[0].message.content

# Create a prompt for generating Cypher queries for node creation
def generate_cypher_queries():
    prompt = """
    Erstelle eine Cypher-Abfrage, um die folgenden Knoten zu erstellen:
    - Person Marie, Alter 30
    - Person Bob, Alter 25
    - Person Charlie, Alter 35
    Verbinde Marie mit Bob und Bob mit Charlie mit der Beziehung :KNOWS.
    Gib die Abfragen in Cypher zurück.
    """
    return get_completion(prompt)

# Example usage: Generate Cypher queries
cypher_queries = generate_cypher_queries()
print(cypher_queries)
