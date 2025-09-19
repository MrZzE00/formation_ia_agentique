# model_configuration.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import LLM

# Charge les variables d'environnement (votre clé API)
load_dotenv()
# Assurez-vous d'avoir un fichier .env avec GOOGLE_API_KEY="votre_clé_ici"

# Configuration des API keys pour LiteLLM (utilisé par CrewAI)
if os.getenv("GOOGLE_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    os.environ["GOOGLE_GENERATIVE_AI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

print("--- Configuration des Modèles LLM avec Google Gemini ---")

# Configuration pour l'Analyste de Données (précis et factuel)
analyst_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Modèle Google Gemini 1.5 Flash
    temperature=0.2,           # Très factuel, peu de créativité
    max_tokens=2048           # Limite de tokens appropriée
)

# Configuration pour le Rédacteur Stratégique (fluide et naturel)
writer_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Modèle Google Gemini 1.5 Flash
    temperature=0.7,           # Légèrement plus créatif pour un style engageant
    max_tokens=2048           # Limite de tokens appropriée
)

# Configuration LLM pour CrewAI (utilise LiteLLM en arrière-plan)
analyst_crewai_llm = LLM(
    model="gemini/gemini-1.5-flash",  # Format LiteLLM pour Gemini
    temperature=0.2,
    max_tokens=2048
)

writer_crewai_llm = LLM(
    model="gemini/gemini-1.5-flash",  # Format LiteLLM pour Gemini
    temperature=0.7,
    max_tokens=2048
)

print("✅ Modèles Gemini pour LangChain configurés.")
print("✅ Modèles Gemini pour CrewAI configurés.")