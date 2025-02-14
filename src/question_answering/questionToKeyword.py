# src/question_answering/questionToKeyword.py

import os
import re
import json

# Anstelle von openai und load_dotenv
from src.api.api_call import get_completion

# Beispiel-Text
chunk = """
        What has happened to Ukrainian energy facilities?
        """

def generate_keywords():
    prompt = f"""
    extract the most significant keywords from the question below. 
    For each keyword also return different conjugations of the word. 
    Return them as a list of plain keywords simply separated by a comma. 

    Question: {chunk}
    """
    # Aufruf der ausgelagerten Funktion
    keywords = get_completion(prompt)
    return keywords

if __name__ == "__main__":
    answer = generate_keywords()
    print(answer)
