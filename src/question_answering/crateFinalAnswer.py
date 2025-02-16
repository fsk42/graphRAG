import os
import re
import json

# Importiere die OpenAI-Funktion aus dem api_call-Modul
from api.api_call import get_completion

def generate_answer(question, relations):
    """
    Formuliert eine Antwort auf die gestellte Frage basierend auf den im Knowledge Graph gefundenen Relationen.
    
    :param question: Die vom Benutzer gestellte Frage.
    :param relations: Ein Text, der die gefundenen Relationen beschreibt.
    :return: Die generierte Antwort.
    """
    # Filtere nur die relevanten Zeilen heraus, in denen Verbindungen dargestellt werden
    filtered_relations = "\n".join(
        line for line in relations.splitlines() if "--[:" in line and "-->" in line
    )
    
    # Erstelle einen Prompt, der sowohl die Frage als auch die relevanten Relationen enthält
    prompt = f"""
    Beantworte bitte folgende Frage:

    Frage: {question}

    Beziehungen aus dem Knowledge Graph:
    {filtered_relations}

    Bitte gib eine klare und prägnante Antwort.
    """
    
    # Debug-Ausgabe: Zeige den generierten Prompt an
    print("=== Generierter Prompt ===")
    print(prompt)
    print("==========================")
    
    # Hole die Antwort von OpenAI
    answer = get_completion(prompt)
    return answer

if __name__ == "__main__":
    # Testaufruf (kann hier mit Dummy-Werten erfolgen)
    pass
