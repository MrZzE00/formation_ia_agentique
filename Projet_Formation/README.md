# 🤖 Système Multi-Agents d'Analyse Financière

## 📋 Description

Ce projet implémente un système multi-agents utilisant **CrewAI** et **LangChain** avec **Google Gemini 1.5 Flash** pour l'analyse financière automatisée. Le système utilise deux agents spécialisés qui collaborent pour analyser les tendances du marché et produire des rapports stratégiques.

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
├── model_configuration.py       # Configuration des LLMs (Gemini 1.5 Flash)
├── prompt_constitution.py       # System prompts structurés pour les agents
├── chain_invocation.py          # Test des chaînes LangChain
├── tools_creation.py            # Outil de recherche financière
├── agents_definition.py         # Définition des agents CrewAI
├── tasks_and_crew.py           # Tâches et orchestration du crew
├── main.py                      # Point d'entrée principal
├── .env                         # Variables d'environnement
├── .env.example                 # Exemple de configuration
└── README.md                    # Ce fichier
```

## 🔧 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Un compte Google pour obtenir une clé API Gemini
- Git pour cloner le projet

## 🚀 Installation Détaillée

### Étape 1 : Cloner le Projet

```bash
# Cloner le dépôt
git clone [votre-repo]

# Se déplacer dans le répertoire du projet
cd Projet_Formation
```

### Étape 2 : Créer un Environnement Virtuel (Recommandé)

```bash
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate

# Sur Windows :
# venv\Scripts\activate
```

### Étape 3 : Installer les Dépendances

```bash
# Méthode 1 : Installation via requirements.txt (RECOMMANDÉ)
pip install -r requirements.txt

# Méthode 2 : Installation manuelle
pip install crewai
pip install langchain
pip install langchain-google-genai
pip install python-dotenv
pip install pytest  # Optionnel, pour les tests
```

### Étape 4 : Configuration des Clés API

1. **Créer le fichier de configuration** :
```bash
# Copier le fichier exemple
cp .env.example .env

# Ou créer directement le fichier .env
touch .env
```

2. **Obtenir une clé API Google Gemini** :
   - Aller sur [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Cliquer sur "Get API Key"
   - Créer une nouvelle clé API
   - Copier la clé générée

3. **Éditer le fichier `.env`** :
```bash
# Ouvrir le fichier avec votre éditeur préféré
nano .env  # ou vim, code, etc.
```

Ajouter vos clés :
```env
GOOGLE_API_KEY=votre_cle_google_api_ici
SERPER_API_KEY=votre_cle_serper_ici  # Optionnel
CHROMA_OPENAI_API_KEY=not_needed_with_gemini
```

### Étape 5 : Vérifier l'Installation

```bash
# Vérifier que toutes les dépendances sont installées
pip list | grep -E "crewai|langchain|dotenv"

# Tester la configuration
python3 -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✅ .env chargé' if os.getenv('GOOGLE_API_KEY') else '❌ Clé API manquante')"

# Tester l'import des modules
python3 -c "import crewai, langchain; print('✅ Modules importés avec succès')"
```

## 💻 Utilisation

### Lancement de l'Application

#### Étape 1 : S'assurer que l'environnement est activé

```bash
# Sur macOS/Linux :
source venv/bin/activate

# Sur Windows :
# venv\Scripts\activate
```

#### Étape 2 : Lancer l'analyse

```bash
# Analyser NVIDIA (par défaut)
python3 main.py

# Analyser un ticker spécifique en argument
python3 main.py AAPL
python3 main.py MSFT
python3 main.py TSLA
python3 main.py GOOGL
```

**Note** : L'application générera un rapport d'analyse financière dans la console. Le processus peut prendre 30-60 secondes selon le ticker analysé.

### Tests Individuels

```bash
# Tester uniquement les chaînes LangChain
python3 chain_invocation.py

# Tester l'outil de recherche
python3 -c "from tools_creation import search_financial_trends_robust; print(search_financial_trends_robust._run('NVDA'))"

# Tester la configuration Gemini
python3 -c "from model_configuration import analyst_llm; print('✅ Gemini configuré')"
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

### ⚙️ Fonctionnement Technique

L'application utilise un système de template dynamique :
- Le ticker est passé via `inputs={"ticker": ticker}` au crew
- La description de la tâche utilise `{ticker}` comme placeholder
- CrewAI remplace automatiquement `{ticker}` par la valeur fournie

### Analyse de Ticker - Guide Complet

```bash
# ✅ MÉTHODE RECOMMANDÉE : Argument en ligne de commande
python3 main.py TICKER_CHOISI

# Exemples pratiques :
python3 main.py NVDA    # NVIDIA
python3 main.py AAPL    # Apple
python3 main.py MSFT    # Microsoft  
python3 main.py TSLA    # Tesla
python3 main.py GOOGL   # Google/Alphabet
python3 main.py AMZN    # Amazon
python3 main.py META    # Meta/Facebook
python3 main.py NFLX    # Netflix

# Si aucun argument fourni, utilise NVDA par défaut
python3 main.py         # Équivalent à python3 main.py NVDA
```

### Tickers Populaires pour Formation

| Ticker | Entreprise | Secteur |
|--------|------------|---------|
| `NVDA` | NVIDIA | Tech/IA |
| `AAPL` | Apple | Tech/Consumer |
| `MSFT` | Microsoft | Tech/Cloud |
| `TSLA` | Tesla | Auto/Électrique |
| `GOOGL` | Google | Tech/Recherche |
| `AMZN` | Amazon | E-commerce/Cloud |
| `META` | Meta | Social Media |

### Ajuster les Paramètres LLM

Dans `model_configuration.py` :
```python
# Pour LangChain
analyst_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.1,  # Ajuster pour plus/moins de créativité
    max_tokens=2048,
    top_p=0.8,
    top_k=40
)

# Pour CrewAI
analyst_crewai_llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.1,
    max_tokens=2048,
    top_p=0.8,
    top_k=40
)
```

### Ajouter de Nouveaux Outils

1. Créer l'outil dans `tools_creation.py`
2. L'ajouter à l'agent dans `agents_definition.py`
3. Mettre à jour le workflow dans `prompt_constitution.py`

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
GOOGLE_API_KEY=your_google_api_key_here
SERPER_API_KEY=your_serper_api_key_here
CHROMA_OPENAI_API_KEY=not_needed_with_gemini
```

Si vous obtenez une erreur d'authentification, vérifiez :
1. Que votre clé Google API est valide
2. Que l'API Gemini est activée dans votre projet Google Cloud

### Échec de l'Outil

L'outil simule des échecs intentionnellement. Si vous voulez désactiver :
```python
# Dans tools_creation.py, commenter les lignes de simulation d'erreur
# if random.randint(1, 3) == 1:
#     raise ConnectionError("...")
```

## 📚 Ressources

- [Documentation CrewAI](https://docs.crewai.com)
- [Documentation LangChain](https://docs.langchain.com)
- [Google AI Studio](https://makersuite.google.com/app/apikey)
- [Documentation Gemini API](https://ai.google.dev/docs)
- [LangChain Google GenAI](https://python.langchain.com/docs/integrations/llms/google_ai)

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