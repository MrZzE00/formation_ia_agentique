# chain_invocation.py

print("--- Invocation des Chaînes avec System Prompts ---")

# Importation des objets que nous avons créés dans les fichiers précédents
from model_configuration import analyst_llm, writer_llm
from prompt_constitution import analyst_prompt, writer_prompt

# Création des chaînes (Chains) pour les deux agents
# Chaîne pour l'Analyste
analyst_chain = analyst_prompt | analyst_llm

# Chaîne pour le Rédacteur
writer_chain = writer_prompt | writer_llm

print("🔗 Chaîne de l'Analyste créée (Prompt structuré + LLM).")
print("🔗 Chaîne du Rédacteur créée (Prompt structuré + LLM).")

# Test 1: Invocation de la chaîne de l'Analyste
print("\n--- TEST 1: AGENT ANALYSTE ---")
print("🚀 Invocation de la chaîne de l'Analyste pour le ticker NVDA...")

analyst_response = analyst_chain.invoke({"ticker": "NVDA"})
print("\n--- RÉPONSE DE L'AGENT ANALYSTE ---")
print(analyst_response.content)
print("------------------------------------")

# Test 2: Invocation de la chaîne du Rédacteur avec l'output de l'Analyste
print("\n--- TEST 2: AGENT RÉDACTEUR ---")

# Simulation de l'output de l'agent Analyste (ou utilisation de analyst_response.content)
analyse_de_test = """
- Tendance 1 : Le volume des ventes a augmenté de 15% au T3, principalement dû au lancement du produit 'Atlas'.
- Tendance 2 : L'engagement sur les réseaux sociaux a diminué de 5%, un point de vigilance pour le marketing.
- Tendance 3 : Le coût d'acquisition client a baissé de 10%, améliorant la rentabilité.
- Tendance 4 : Le feedback client mentionne des problèmes de livraison dans la région Est.
"""

print("🚀 Invocation de la chaîne du Rédacteur avec des données de test...")

writer_response = writer_chain.invoke({"analyse_brute": analyse_de_test})

print("\n--- RÉPONSE DE L'AGENT RÉDACTEUR ---")
print(writer_response.content)
print("------------------------------------")

print("\n✅ Les deux chaînes avec system prompts structurés fonctionnent correctement.")