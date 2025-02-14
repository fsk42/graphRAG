#api_call.py

import openai
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

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

