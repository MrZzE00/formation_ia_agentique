# agents_definition.py
from crewai import Agent
from tools_creation import search_financial_trends_robust
from prompt_constitution import analyst_system_prompt_template, writer_system_prompt_template
from model_configuration import analyst_crewai_llm, writer_crewai_llm

print("--- Définition des Agents ---")

# Agent 1 : L'Analyste de Données (avec son outil et system prompt)
data_analyst = Agent(
    role="Analyste Financier Senior",
    goal="""Analyser les tendances financières du marché pour un titre boursier donné
    et fournir un résumé concis des 3 tendances les plus importantes.""",
    backstory="""Expert reconnu dans l'analyse de données de marché, vous avez un talent
    pour déceler les signaux importants dans un flot d'informations. Votre analyse est
    toujours précise, factuelle et directement exploitable.""",
    tools=[search_financial_trends_robust],         # L'agent a accès à cet outil
    llm=analyst_crewai_llm,
    system_template=analyst_system_prompt_template, # Ajout du system prompt structuré
    verbose=True,                                   # Affiche la chaîne de pensée de l'agent (ReAct)
    allow_delegation=False,
    max_iter=3,                                     # Limite les itérations pour éviter les boucles
    memory=False                                    # Mémoire désactivée pour simplifier la formation
)

# Agent 2 : Le Rédacteur Stratégique (sans outil mais avec system prompt)
strategy_writer = Agent(
    role="Rédacteur Stratégique Senior",
    goal="""Rédiger un rapport stratégique clair et percutant basé sur une analyse
    financière, en suivant un format Markdown précis.""",
    backstory="""Vous êtes un ancien journaliste économique réputé pour votre capacité à
    transformer des données complexes en récits stratégiques. Votre style est direct,
    informatif et parfaitement adapté à un public de décideurs.""",
    llm=writer_crewai_llm,
    system_template=writer_system_prompt_template,  # Ajout du system prompt structuré
    verbose=True,
    allow_delegation=False,
    max_iter=2,                                     # Moins d'itérations pour la rédaction
    memory=False                                    # Mémoire désactivée pour simplifier la formation
)

print("✅ Agent 'Analyste de Données'")
print("✅ Agent 'Rédacteur Stratégique'")