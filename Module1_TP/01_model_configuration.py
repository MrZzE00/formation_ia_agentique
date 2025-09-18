# model_configuration.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Charge les variables d'environnement (votre clé API)
load_dotenv()
# Assurez-vous d'avoir un fichier .env avec GOOGLE_API_KEY="votre_clé_ici"

print("--- Configuration des Modèles LLM avec Google Gemini ---")

# Configuration pour l'Analyste de Données (précis et factuel)
analyst_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Modèle Google Gemini 1.5 Flash
    temperature=0.1,           # Très factuel, peu de créativité
    max_tokens=2048,           # Limite de tokens appropriée
    top_p=0.8,                 # Nucleus sampling pour plus de précision
    top_k=40                   # Top-k sampling
)

# Configuration pour le Rédacteur Stratégique (fluide et naturel)
writer_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Modèle Google Gemini 1.5 Flash
    temperature=0.3,           # Légèrement plus créatif pour un style engageant
    max_tokens=2048,           # Limite de tokens appropriée
    top_p=0.9,                 # Plus de diversité pour la rédaction
    top_k=40                   # Top-k sampling
)

print("✅ Modèle Gemini pour l'Analyste configuré.")
print("✅ Modèle Gemini pour le Rédacteur configuré.")

# Configuration des API keys pour LiteLLM (utilisé par certains frameworks)
if os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")