# model_configuration.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Charge les variables d'environnement (votre clé API)
load_dotenv()
# Assurez-vous d'avoir un fichier .env avec GOOGLE_API_KEY="votre_clé_ici"

# Configuration des API keys pour LiteLLM (utilisé par CrewAI)
if os.getenv("GOOGLE_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    os.environ["GOOGLE_GENERATIVE_AI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

print("--- Configuration des Modèles LLM avec Google Gemini ---")

# Configuration pour l'Analyste de Données (précis et factuel)
# On l'utilisera DIRECTEMENT dans CrewAI
analyst_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Modèle Google Gemini 1.5 Flash
    temperature=0.2,           # Très factuel, peu de créativité
    max_tokens=2048            # Limite de tokens appropriée
)

# Configuration pour le Rédacteur Stratégique (fluide et naturel)
# On l'utilisera DIRECTEMENT dans CrewAI
writer_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Modèle Google Gemini 1.5 Flash
    temperature=0.7,           # Légèrement plus créatif pour un style engageant
    max_tokens=2048            # Limite de tokens appropriée
)

print("✅ Modèles Gemini configurés (utilisables directement avec CrewAI).")

# Ces objets LangChain peuvent être utilisés directement dans CrewAI
# Plus besoin de créer des objets LLM séparés pour CrewAI