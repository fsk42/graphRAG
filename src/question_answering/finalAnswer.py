# src/question_answering/finalAnswer.py

import os
import re
import json

# Statt import openai... usw. nur noch:
from src.api.api_call import get_completion

def generate_answer(question, relations):
    """
    Formuliert eine Antwort auf Basis der übergebenen Frage und der im Knowledge Graph gefundenen Relationen.
    Dabei werden im Prompt nur die gültigen Relationseinträge verwendet.
    """
    # Filtere nur die Zeilen, die gültige Relationseinträge enthalten.
    filtered_relations = "\n".join(
        line for line in relations.splitlines() if "--[:" in line and "-->" in line
    )
    
    prompt = f"""
Answer the following question:

Question: {question}

Relations from the Knowledge Graph:
{filtered_relations}

Provide a clear and concise answer.
    """
    
    # Ausgabe des generierten Prompts in der Konsole
    print("=== Generierter Prompt ===")
    print(prompt)
    print("==========================")
    
    # API-Aufruf über die ausgelagerte Funktion
    answer = get_completion(prompt)
    return answer

# Testaufruf (wird nur ausgeführt, wenn finalAnswer.py direkt gestartet wird)
if __name__ == "__main__":
    test_question = "What has happened to Ukrainian energy facilities?"
    test_relations = """
--- Ergebnisse für Stichwort: 'happened' ---
Keine passenden Knoten gefunden.

--- Ergebnisse für Stichwort: 'facilities' ---
Russian_Ministry_of_Defense_(MoD) --[:TARGETED]--> Ukrainian_energy_facilities_and_defense_industrial_enterprises
Russian_forces --[:TARGETING]--> Ukrainian_energy_facilities
Russian_forces --[:HEAVILY_TARGETED]--> Ukrainian_energy_facilities
Russia --[:CAUSING_SIGNIFICANT_DAMAGE_TO]--> Ukraine_s_energy_facilities
    """
    print(generate_answer(test_question, test_relations))
