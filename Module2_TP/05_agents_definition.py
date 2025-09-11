# agents_definition.py
from crewai import Agent
from tools_creation import search_financial_trends_robust
from model_configuration import analyst_llm, writer_llm
from prompt_constitution import analyst_system_prompt_template, writer_system_prompt_template

print("--- Définition des Agents avec System Prompts ---")

# Agent 1 : L'Analyste de Données (avec son outil et system prompt)
data_analyst = Agent(
    role="Analyste Financier Senior",
    goal="""Analyser les tendances financières du marché pour un titre boursier donné
    et fournir un résumé concis des 3 tendances les plus importantes.""",
    backstory="""Expert reconnu dans l'analyse de données de marché, vous avez un talent
    pour déceler les signaux importants dans un flot d'informations. Votre analyse est
    toujours précise, factuelle et directement exploitable.""",
    tools=[search_financial_trends_robust], # L'agent a accès à cet outil
    llm=analyst_llm,
    system_template=analyst_system_prompt_template, # Ajout du system prompt structuré
    verbose=True, # Affiche la chaîne de pensée de l'agent (ReAct)
    allow_delegation=False
)

# Agent 2 : Le Rédacteur Stratégique (sans outil mais avec system prompt)
strategy_writer = Agent(
    role="Rédacteur Stratégique Senior",
    goal="""Rédiger un rapport stratégique clair et percutant basé sur une analyse
    financière, en suivant un format Markdown précis.""",
    backstory="""Vous êtes un ancien journaliste économique réputé pour votre capacité à
    transformer des données complexes en récits stratégiques. Votre style est direct,
    informatif et parfaitement adapté à un public de décideurs.""",
    llm=writer_llm,
    system_template=writer_system_prompt_template, # Ajout du system prompt structuré
    verbose=True,
    allow_delegation=False
)

print("✅ Agent 'Analyste de Données' défini avec system prompt structuré.")
print("✅ Agent 'Rédacteur Stratégique' défini avec system prompt structuré.")