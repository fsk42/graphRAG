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

relations = """
            Russian_Ministry_of_Defense_(MoD) --[:TARGETED]--> Ukrainian_energy_facilities_and_defense_industrial_enterprises
            Russian_forces --[:TARGETING]--> Ukrainian_energy_facilities
            Russian_forces --[:HEAVILY_TARGETED]--> Ukrainian_energy_facilities
            Russia --[:CAUSING_SIGNIFICANT_DAMAGE_TO]--> Ukraine_s_energy_facilities
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

def generate_answer():
    
    #multiple or singe of noun?
    prompt = f"""
    answer the following question 

    question:

    Question: {chunk}

    Relations from the knowledge Graph :

    Relations: {relations}

    """
    # 1) Hole die Triplets von GPT
    answer = get_completion(prompt)
    # 2) Erstelle daraus Cypher-Queries
    
    return answer



answer = generate_answer()
print(answer)
