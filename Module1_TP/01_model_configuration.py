# model_configuration.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

print("--- Configuration des Modèles LLM avec Google Gemini (Version Corrigée) ---")

# --- APPROCHE RECOMMANDÉE : CONTRÔLE PAR LA TEMPÉRATURE ---

# Configuration pour l'Analyste de Données (précis et factuel)
analyst_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,           # ON NE GARDE QUE CE PARAMÈTRE POUR LE CONTRÔLE
    # top_p et top_k sont laissés à leurs valeurs par défaut (désactivés)
)

# Configuration pour le Rédacteur Stratégique (fluide et naturel)
writer_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,           # ON NE GARDE QUE CE PARAMÈTRE POUR LE CONTRÔLE
)

print("✅ Modèle Gemini pour l'Analyste configuré (via temperature).")
print("✅ Modèle Gemini pour le Rédacteur configuré (via temperature).")

# Pour l'instant, ce fichier ne fait rien de plus que définir les modèles.
# Nous les importerons dans le fichier suivant.