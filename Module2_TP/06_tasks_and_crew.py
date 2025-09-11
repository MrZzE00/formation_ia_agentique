# tasks_and_crew.py
from crewai import Task, Crew, Process
from agents_definition import data_analyst, strategy_writer

print("--- Définition des Tâches et du Crew ---")

# Tâche 1 : Analyse (assignée à l'analyste)
task_analysis = Task(
    description="""Analyse les tendances financières actuelles pour le titre 'NVIDIA' (ticker: NVDA).
    Utilise ton outil pour obtenir les données. Si l'outil échoue, signale-le clairement.""",
    expected_output="""Un résumé de 3 points clés sur les tendances financières de NVIDIA.
    Si les données n'ont pas pu être récupérées, le rapport doit l'indiquer explicitement.""",
    agent=data_analyst
)

# Tâche 2 : Rédaction (assignée au rédacteur)
# Le paramètre 'context' est crucial : il indique que cette tâche dépend du résultat de la tâche d'analyse.
task_writing = Task(
    description="""Rédige un rapport stratégique en Markdown basé sur l'analyse fournie.
    Le rapport doit être structuré avec un titre H1, une introduction et 3 sous-titres H2
    pour chaque tendance clé.""",
    expected_output="""Un rapport complet et formaté en Markdown. Si l'analyse a échoué,
    le rapport doit commencer par un avertissement indiquant le problème de données.""",
    agent=strategy_writer,
    context=[task_analysis] # Dépendance explicite
)

# Assemblage du Crew avec un processus séquentiel
strategic_crew = Crew(
    agents=[data_analyst, strategy_writer],
    tasks=[task_analysis, task_writing],
    process=Process.sequential,
    memory=True,  # Active la mémoire conversationnelle
    verbose=True  # Affiche le détail complet de l'exécution du crew
)

print("✅ Tâches définies.")
print("✅ Crew assemblé et prêt pour la mission.")