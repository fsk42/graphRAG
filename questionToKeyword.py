import openai
from openai import OpenAI
import os
import dotenv
from dotenv import load_dotenv, find_dotenv
import re
import json

# Beispiel-Text, aus dem Triplets extrahiert werden sollen.
# Du kannst diesen Text ersetzen oder dynamisch befüllen.
chunk = """
        What has happened to Ukrainian energy facilities?
        """

# Lade Umgebungsvariablen (z.B. OPENAI_API_KEY) aus einer .env
_ = load_dotenv(find_dotenv())


openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def get_completion(prompt, model='gpt-3.5-turbo'):
    """
    Sendet einen Prompt an das OpenAI-API und gibt das Completion-Resultat zurück.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=500,
    )
    return completion.choices[0].message.content

def generate_cypher_queries():
    
    #multiple or singe of noun?
    prompt = f"""
    extract the most significant keywords from the question below. 
    For each keyword also return different conjugations of the word. 
    Return them as a list of plain keywords simply separated by a comma. 

    Question: {chunk}

    """
    # 1) Hole die Triplets von GPT
    keywords = get_completion(prompt)
    # 2) Erstelle daraus Cypher-Queries
    
    return keywords



answer = generate_cypher_queries()
print(answer)
