# model_configuration.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Charge les variables d'environnement (votre clé API)
load_dotenv()
# Assurez-vous d'avoir un fichier .env avec OPENAI_API_KEY="sk-..."

print("--- Configuration des Modèles LLM ---")

# Configuration pour l'Analyste de Données (précis et factuel)
analyst_llm = ChatOpenAI(
    model="gpt-3.5-turbo",    # Modèle moins cher que gpt-4o
    temperature=0.1,          # Très factuel, peu de créativité
    max_tokens=2048,          # Réduit pour économiser les tokens
    model_kwargs={
        "frequency_penalty": 0.2, # Évite de répéter les mêmes mots
        "presence_penalty": 0.0   # N'a pas de pénalité sur les nouveaux sujets
    }
)

# Configuration pour le Rédacteur Stratégique (fluide et naturel)
writer_llm = ChatOpenAI(
    model="gpt-3.5-turbo",    # Modèle moins cher que gpt-4o
    temperature=0.7,          # Plus créatif pour un style engageant
    max_tokens=2048,          # Réduit pour économiser les tokens
)

print("✅ Modèle pour l'Analyste configuré.")
print("✅ Modèle pour le Rédacteur configuré.")
print("\nCe fichier a simplement créé et configuré nos deux 'cerveaux' IA.")

# Pour l'instant, ce fichier ne fait rien de plus que définir les modèles.
# Nous les importerons dans le fichier suivant.