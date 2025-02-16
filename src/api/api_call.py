import openai
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

# Lade Umgebungsvariablen aus der .env-Datei, z.B. den OPENAI_API_KEY
_ = load_dotenv(find_dotenv())

# Setze den API-Schlüssel für OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialisiere den OpenAI-Client
client = OpenAI()

def get_completion(prompt, model='gpt-3.5-turbo'):
    """
    Sendet einen gegebenen Prompt an das OpenAI-API und gibt die Antwort zurück.
    
    :param prompt: Der Text, der an das API geschickt wird.
    :param model: Das Modell, das verwendet werden soll (Standard: gpt-3.5-turbo).
    :return: Die Antwort des Modells.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=500,
    )
    # Rückgabe des Inhalts der ersten Wahl
    return completion.choices[0].message.content
