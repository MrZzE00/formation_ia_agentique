# main.py
import sys
from 06_tasks_and_crew import strategic_crew

def run_mission(ticker="NVDA"):
    """Lance la mission du Crew et affiche le résultat."""
    print(f"--- Lancement du Crew d'Analyse Stratégique pour {ticker} ---")
    print("-----------------------------------------------")

    # .kickoff() démarre la mission avec le ticker spécifié
    result = strategic_crew.kickoff(inputs={"ticker": ticker})

    print("\n\n-----------------------------------------------")
    print("--- Résultat Final de la Mission ---")
    print("-----------------------------------------------")
    print(result)

if __name__ == "__main__":
    # Récupère le ticker depuis les arguments de ligne de commande
    ticker = sys.argv[1] if len(sys.argv) > 1 else "NVDA"
    print(f"🎯 Analyse du ticker: {ticker}")
    run_mission(ticker)