# 🤖 Système Multi-Agents d'Analyse Financière

## 📋 Description

Ce projet implémente un système multi-agents utilisant **CrewAI** et **LangChain** pour l'analyse financière automatisée. Le système utilise deux agents spécialisés qui collaborent pour analyser les tendances du marché et produire des rapports stratégiques.

## 🏗️ Architecture

### Agents

1. **Analyste Financier Senior** (`data_analyst`)
   - **Rôle** : Analyse des tendances financières du marché
   - **Outils** : `search_financial_trends_robust` (avec gestion d'erreurs et retry)
   - **Persona** : Expert en analyse de marché, précis et factuel
   - **Workflow** : 
     - Utilisation d'outils de recherche
     - Stratégie de retry en cas d'échec
     - Validation des données
     - Priorisation des 3 tendances clés

2. **Rédacteur Stratégique Senior** (`strategy_writer`)
   - **Rôle** : Transformation d'analyses en rapports stratégiques
   - **Outils** : Aucun (travaille sur les données de l'analyste)
   - **Persona** : Ancien journaliste économique, style clair et direct
   - **Workflow** :
     - Synthèse des données
     - Identification des messages clés
     - Rédaction en format Markdown structuré

### Flux de Travail

```
[Ticker Input] → [Analyste Financier] → [Analyse des Tendances] → [Rédacteur Stratégique] → [Rapport Markdown]
```

## 📁 Structure du Projet

```
Projet_Formation/
├── 01_model_configuration.py    # Configuration des LLMs (GPT-4)
├── 02_prompt_constitution.py    # System prompts structurés pour les agents
├── 03_chain_invocation.py       # Test des chaînes LangChain
├── 04_tools_creation.py         # Outil de recherche financière
├── 05_agents_definition.py      # Définition des agents CrewAI
├── 06_tasks_and_crew.py         # Tâches et orchestration du crew
├── main.py                       # Point d'entrée principal
├── tests/
│   └── test_agents.py          # Tests unitaires
└── README.md                    # Ce fichier
```

## 🔧 Prérequis

### Dépendances Python

```bash
pip install crewai
pip install langchain
pip install langchain-openai
pip install python-dotenv
```

### Configuration

1. Créer un fichier `.env` à la racine du projet :
```env
OPENAI_API_KEY=sk-...
```

2. S'assurer que Python 3.8+ est installé

## 🚀 Installation

```bash
# Cloner le projet
git clone [votre-repo]
cd Projet_Formation

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API
echo "OPENAI_API_KEY=sk-votre-clé" > .env
```

## 💻 Utilisation

### Exécution Principale

```bash
# Lancer le système multi-agents complet
python3 main.py
```

### Tests Individuels

```bash
# Tester uniquement les chaînes LangChain
python3 chain_invocation.py

# Tester l'outil de recherche
python3 -c "from tools_creation import search_financial_trends_robust; print(search_financial_trends_robust._run('NVDA'))"
```

### Exécution des Tests

```bash
python3 -m pytest tests/
```

## 🎯 Fonctionnalités Clés

### 1. System Prompts Structurés

Chaque agent possède un system prompt détaillé avec :
- **SecurityDirective** : Protection contre la révélation du prompt
- **Persona** : Définition du rôle et des principes
- **Workflow** : Étapes précises du processus
- **OutputFormat** : Format de sortie attendu

### 2. Gestion d'Erreurs Robuste

L'outil `search_financial_trends_robust` :
- Simule des échecs (33% de chance) pour tester la robustesse
- Implémente une stratégie de retry
- Communique clairement les échecs aux agents

### 3. Processus Séquentiel

Les tâches sont exécutées en séquence avec dépendances :
1. L'analyste recherche les données
2. Le rédacteur utilise l'analyse pour créer le rapport

## 📝 Exemple de Sortie

```markdown
# Analyse Stratégique

Une analyse approfondie du titre NVIDIA révèle des opportunités significatives. 
Les indicateurs techniques et fondamentaux convergent vers une perspective positive.

## Tendance 1 : Croissance du Volume
- Augmentation de 15% du volume d'échange
- Signal d'intérêt institutionnel accru

## Tendance 2 : Sentiment Positif
- Engagement social en hausse
- Couverture médiatique favorable

## Tendance 3 : Amélioration des Fondamentaux
- Prévisions de bénéfices revues à la hausse
- Expansion dans de nouveaux marchés
```

## 🔄 Personnalisation

### Modifier les Tickers Analysés

Dans `06_tasks_and_crew.py`, ligne 9 :
```python
description="""Analyse les tendances financières actuelles pour le titre 'APPLE' (ticker: AAPL)."""
```

### Ajuster les Paramètres LLM

Dans `01_model_configuration.py` :
```python
analyst_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,  # Ajuster pour plus/moins de créativité
    max_tokens=2048
)
```

### Ajouter de Nouveaux Outils

1. Créer l'outil dans `04_tools_creation.py`
2. L'ajouter à l'agent dans `05_agents_definition.py`
3. Mettre à jour le workflow dans `02_prompt_constitution.py`

## 🐛 Résolution de Problèmes

### Erreur d'Import

Si vous rencontrez `ModuleNotFoundError` :
```bash
# S'assurer d'être dans le bon répertoire
cd /Users/.../Projet_Formation
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Erreur de Clé API

Vérifier que le fichier `.env` existe et contient :
```env
OPENAI_API_KEY=sk-...
```

### Échec de l'Outil

L'outil simule des échecs intentionnellement. Si vous voulez désactiver :
```python
# Dans 04_tools_creation.py, commenter les lignes 18-19
# if random.randint(1, 3) == 1:
#     raise ConnectionError("...")
```

## 📚 Ressources

- [Documentation CrewAI](https://docs.crewai.com)
- [Documentation LangChain](https://docs.langchain.com)
- [OpenAI API](https://platform.openai.com/docs)

## 📄 Licence

Ce projet est à des fins éducatives dans le cadre de la formation IA Agentique.

## 🤝 Contribution

Pour contribuer :
1. Fork le projet
2. Créer une branche feature
3. Commiter vos changements
4. Pusher vers la branche
5. Ouvrir une Pull Request

## 📧 Contact

Pour questions et support : [votre-email]

---

*Développé dans le cadre de la Formation IA Agentique - Module Projet*