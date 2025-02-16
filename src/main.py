# Importiere die Funktionen zur Erstellung des Knowledge Graphs
# und zur Durchführung der Frage-Antwort-Suche
from knowledge_graph_creation.createKnowledgeGraph import create_knowledge_graph
from question_answering.graphKeywordSearch import run_question_answering

def main():
    """
    Hauptfunktion des Programms.
    Zuerst wird der Knowledge Graph aus den vorhandenen Textdateien erstellt.
    Anschließend wird eine Frage vom Benutzer abgefragt und basierend auf den im Graph
    gefundenen Relationen eine Antwort generiert.
    """
    # Erstelle den Knowledge Graph (liest dazu die Dateien im data-Ordner)
    # Der übergebene Parameter wird hier nicht benötigt, daher kann ein leerer String übergeben werden.
    create_knowledge_graph("")
    
    # Jetzt wird die Frage des Benutzers abgefragt
    user_question = input("Geben Sie Ihre Frage ein: ")

    # Führe die Frage-Antwort-Suche im Knowledge Graph durch
    final_answer = run_question_answering(user_question)

    # Gib die finale Antwort aus
    print("\nFinale Antwort:")
    print(final_answer)

if __name__ == "__main__":
    main()
