# main.py
from tasks_and_crew import strategic_crew

def run_mission():
    """Lance la mission du Crew et affiche le résultat."""
    print("--- Lancement du Crew d'Analyse Stratégique ---")
    print("-----------------------------------------------")

    # .kickoff() démarre la mission
    result = strategic_crew.kickoff()

    print("\n\n-----------------------------------------------")
    print("--- Résultat Final de la Mission ---")
    print("-----------------------------------------------")
    print(result)

if __name__ == "__main__":
    run_mission()