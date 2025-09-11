# tools_creation.py
# On simule une API qui peut parfois échouer
import random
from crewai.tools import BaseTool

print("--- Définition des Outils ---")

def _search_financial_trends(ticker: str) -> str:
    """
    Fonction interne qui recherche les tendances financières.
    """
    print(f"INFO: Recherche des tendances pour le ticker '{ticker}'...")
    
    # Simulation d'un appel API qui peut réussir ou échouer
    try:
        # 1 chance sur 3 d'échouer pour la démonstration
        if random.randint(1, 3) == 1:
            raise ConnectionError("Erreur réseau simulée : Le service financier est indisponible.")

        # Si l'appel réussit, on retourne des données fictives
        trends = [
            "hausse du volume d'échange de 15%",
            "sentiment positif sur les réseaux sociaux",
            "prévision de bénéfices revue à la hausse par les analystes"
        ]
        return f"Succès : Les 3 tendances clés pour {ticker} sont : {', '.join(trends)}."

    except ConnectionError as e:
        print(f"ERREUR: L'outil a échoué. Activation du fallback.")
        # Stratégie de fallback : retourner un message d'erreur contrôlé
        # L'agent pourra lire ce message et décider de la suite.
        return f"Échec de l'outil : Impossible de récupérer les données pour {ticker}. Raison : {e}"

# Créer une classe d'outil personnalisée pour CrewAI
class SearchFinancialTrendsTool(BaseTool):
    name: str = "search_financial_trends"
    description: str = "Recherche les dernières tendances financières pour un symbole boursier (ticker) donné. Simule un appel API qui peut parfois échouer pour tester la robustesse de l'agent."
    
    def _run(self, ticker: str) -> str:
        return _search_financial_trends(ticker)

# Instancier l'outil
search_financial_trends_robust = SearchFinancialTrendsTool()

print("✅ Outil 'search_financial_trends_robust' défini.")

# Vous pouvez décommenter les lignes suivantes pour tester l'outil seul
# if __name__ == '__main__':
#     print("\n--- Test de l'outil ---")
#     print(search_financial_trends_robust.invoke({"ticker": "TSLA"}))