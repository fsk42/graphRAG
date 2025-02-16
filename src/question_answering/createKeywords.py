import os
import re
import json

# Importiere die OpenAI-Funktion aus dem api_call-Modul
from api.api_call import get_completion

def generate_keywords(question: str) -> str:
    """
    Extrahiert die wichtigsten Stichwörter aus der gestellten Frage.
    Die Schlüsselwörter werden als kommagetrennte Liste zurückgegeben.
    
    :param question: Die vom Benutzer gestellte Frage.
    :return: Ein String mit den extrahierten Schlüsselwörtern, getrennt durch Kommas.
    """
    # Erstelle einen Prompt, der GPT anweist, die relevantesten Schlüsselwörter zu extrahieren
    prompt = f"""
    Extrahiere die wichtigsten Stichwörter aus der folgenden Frage.
    Für jedes Stichwort sollen auch verschiedene Konjugationsformen zurückgegeben werden.
    Gib die Schlüsselwörter als kommagetrennte Liste aus.

    Frage: {question}
    """
    # Rufe die Funktion auf, um die Schlüsselwörter zu erhalten
    keywords = get_completion(prompt)
    return keywords

if __name__ == "__main__":
    # Beispieltest: Zeige die generierten Schlüsselwörter an
    print(generate_keywords("Who is the president of the United States?"))
