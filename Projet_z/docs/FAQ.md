# ❓ FAQ - Questions Fréquemment Posées

## 🚀 Installation et Configuration

### Q: Comment installer l'application ?

**R:** Suivez ces étapes :

```bash
# 1. Cloner le repository
git clone [url-du-repo]
cd Projet_z

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
# Éditer .env avec votre clé API Google
```

### Q: Où obtenir une clé API Google Gemini ?

**R:** 
1. Allez sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create API Key"
4. Copiez la clé dans votre fichier `.env`

### Q: L'application fonctionne-t-elle sans clé API ?

**R:** Oui, l'application a un mode fallback qui génère des analyses mockées pour les démonstrations et tests. Cependant, pour une utilisation réelle, une clé API est nécessaire.

---

## 🔧 Utilisation

### Q: Comment analyser un ticker ?

**R:** Plusieurs options :

```bash
# Mode interactif
python main.py

# Mode direct
python main.py --ticker AAPL

# Mode avec options
python main.py --ticker MSFT --metrics
```

### Q: Quels tickers sont supportés ?

**R:** Tous les tickers boursiers disponibles sur Yahoo Finance :
- Actions US : AAPL, MSFT, GOOGL, TSLA, etc.
- Actions internationales : ASML, NESN.SW, etc.
- Indices : ^GSPC (S&P 500), ^DJI (Dow Jones), etc.
- Cryptos : BTC-USD, ETH-USD, etc.

### Q: Que faire si l'analyse est lente ?

**R:** L'analyse peut prendre 5-10 secondes. Si c'est plus long :

1. Vérifiez votre connexion internet
2. Vérifiez que la clé API est valide
3. Consultez les logs : `tail -f logs/financial_orchestrator.log`
4. Réduisez la complexité dans la configuration

---

## 🏗️ Architecture et Code

### Q: Comment ajouter un nouvel agent ?

**R:** Créez une nouvelle classe d'agent :

```python
# 1. Créer le fichier YAML de configuration
# prompt/NouvelAgent_v01.yaml

# 2. Créer la classe d'agent
class NouvelAgent:
    def __init__(self):
        config_path = Path(__file__).parent / "prompt" / "NouvelAgent_v01.yaml"
        self.config = load_agent_config(str(config_path))
        # ... configuration LLM et agent

# 3. Ajouter à la factory
class AgentFactory:
    @staticmethod
    def create_nouvel_agent() -> Agent:
        return NouvelAgent().get_agent()
```

### Q: Comment personnaliser les prompts ?

**R:** Éditez les fichiers YAML dans le dossier `prompt/` :

```yaml
# prompt/AnalysteFinancier_v01.yaml
goal_and_instructions:
  system_prompt: |
    Tu es un analyste financier expert...
    [Votre prompt personnalisé]
```

### Q: Comment ajouter de nouveaux outils ?

**R:** Créez un nouvel outil avec le décorateur `@tool` :

```python
from crewai_tools import tool

@tool("mon_outil_custom")
def mon_outil_custom(ticker: str) -> str:
    """
    Description de votre outil.
    
    Args:
        ticker: Symbole boursier
        
    Returns:
        str: Résultat formaté
    """
    # Votre logique ici
    return "Résultat"
```

---

## 🐛 Dépannage

### Q: Erreur "API key not valid"

**R:** Solutions possibles :

1. **Vérifiez la clé API** :
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GOOGLE_API_KEY'))"
   ```

2. **Regénérez une nouvelle clé** sur Google AI Studio

3. **Vérifiez les quotas** de votre compte Google

4. **Testez la clé manuellement** :
   ```bash
   curl "https://generativelanguage.googleapis.com/v1beta/models?key=VOTRE_CLE"
   ```

### Q: Erreur "Module not found"

**R:** 
```bash
# Réinstallez les dépendances
pip install --force-reinstall -r requirements.txt

# Vérifiez l'environnement virtuel
which python
# Doit pointer vers venv/bin/python
```

### Q: L'application se bloque/timeout

**R:** 
1. **Augmentez les timeouts** dans `config.py`
2. **Vérifiez les logs** : `tail -f logs/financial_orchestrator_errors.log`
3. **Testez avec un ticker simple** : AAPL
4. **Redémarrez en mode debug** : `python main.py --debug`

### Q: Problèmes de performance

**R:** 
1. **Réduisez max_tokens** dans la configuration LLM
2. **Désactivez le mode verbose** : `verbose=False`
3. **Nettoyez la mémoire** : Redémarrez l'application
4. **Vérifiez l'espace disque** pour les logs

---

## 📊 Monitoring et Logs

### Q: Comment interpréter les métriques ?

**R:** Les métriques principales :

- **Latence** : Temps de réponse (objectif < 5000ms)
- **Taux de succès** : % de requêtes réussies (objectif > 80%)
- **Tokens utilisés** : Consommation API (surveiller les coûts)
- **Violations sécurité** : Tentatives d'injection (doit être 0)

### Q: Où sont stockés les logs ?

**R:** Structure des logs :

```
logs/
├── financial_orchestrator.log      # Logs principaux
├── financial_orchestrator_errors.log  # Erreurs uniquement
monitoring_logs/
├── metrics_20240101.json          # Métriques du jour
└── alerts_20240101.json           # Alertes du jour
```

### Q: Comment activer les logs JSON ?

**R:** Dans `.env` :
```bash
ENABLE_JSON_LOGS=true
LOG_LEVEL=INFO
```

Ou programmatiquement :
```python
from logger_config import setup_logging
logger = setup_logging(enable_json=True)
```

---

## 🧪 Tests et Développement

### Q: Comment lancer les tests ?

**R:** 
```bash
# Tests simples
python -m pytest

# Tests avec coverage
python -m pytest --cov=src --cov-report=html

# Tests spécifiques
python -m pytest test_scenarios.py::TestAnalysteFinancierBasicFunctionality

# Tests en mode verbose
python -m pytest -v -s
```

### Q: Comment créer un test pour un nouvel agent ?

**R:** 
```python
class TestNouvelAgent:
    @pytest.fixture
    def agent(self):
        return NouvelAgent()
    
    def test_agent_creation(self, agent):
        assert agent.get_agent() is not None
    
    @patch('tools.mon_outil_custom')
    def test_agent_with_mock_tool(self, mock_tool, agent):
        mock_tool.return_value = "Test result"
        result = agent.execute_task("test input")
        assert "Test result" in result
```

### Q: Comment débugger un agent qui ne fonctionne pas ?

**R:** 
1. **Activez le mode verbose** : `verbose=True`
2. **Ajoutez des logs** dans votre code :
   ```python
   from logger_config import get_logger
   logger = get_logger(__name__)
   logger.debug(f"Agent state: {agent_state}")
   ```
3. **Testez l'outil séparément** :
   ```python
   from tools import mon_outil_custom
   result = mon_outil_custom("AAPL")
   print(result)
   ```
4. **Vérifiez la configuration YAML**

---

## 🔒 Sécurité

### Q: L'application est-elle sécurisée ?

**R:** Oui, plusieurs couches de sécurité :

- **Validation d'entrée** : Pydantic + regex
- **Détection d'injection** : Patterns malveillants
- **Monitoring sécurité** : Alertes automatiques
- **Pas de secrets en dur** : Variables d'environnement
- **Logs sécurisés** : Pas de données sensibles

### Q: Comment signaler une vulnérabilité ?

**R:** 
1. **NE PAS** créer d'issue publique
2. Envoyez un email à [security@exemple.com]
3. Décrivez la vulnérabilité en détail
4. Attendez une réponse avant divulgation

### Q: Puis-je utiliser l'application en production ?

**R:** Recommandations pour la production :

1. **Environnement** : `ENVIRONMENT=production`
2. **Logs JSON** : `ENABLE_JSON_LOGS=true`
3. **Monitoring** : Configurez des alertes externes
4. **Secrets** : Utilisez un gestionnaire de secrets
5. **HTTPS** : Si exposition web
6. **Backup** : Sauvegardez la configuration et les données

---

## 🎓 Formation et Apprentissage

### Q: Comment utiliser ce projet pour apprendre ?

**R:** Suivez le [Guide de Formation](FORMATION_GUIDE.md) :

1. **Commencez par** : [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Continuez avec** : [BEST_PRACTICES_GUIDE.md](BEST_PRACTICES_GUIDE.md)
3. **Approfondissez** : [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md)
4. **Pratiquez** : Exercices dans le guide de formation

### Q: Quels sont les prérequis pour comprendre le code ?

**R:** 
- **Python intermédiaire** : Classes, décorateurs, type hints
- **Concepts OOP** : Design patterns de base
- **APIs** : Requests, JSON, REST
- **Tests** : Pytest, mocking
- **Optionnel** : CrewAI, Pydantic, LangChain

### Q: Comment contribuer au projet ?

**R:** 
1. **Forkez** le repository
2. **Créez une branche** : `git checkout -b feature/ma-fonctionnalite`
3. **Suivez les bonnes pratiques** du guide
4. **Ajoutez des tests** : Coverage > 80%
5. **Documentez** : Docstrings + README
6. **Créez une PR** avec description détaillée

---

## 📞 Support

### Q: Où obtenir de l'aide ?

**R:** 
1. **Documentation** : Consultez [docs/](.)
2. **Issues GitHub** : Pour bugs et demandes de fonctionnalités
3. **Discussions** : Pour questions générales
4. **Stack Overflow** : Tag `financial-orchestrator`

### Q: Comment signaler un bug ?

**R:** 
1. **Vérifiez** les issues existantes
2. **Créez une issue** avec :
   - Description du problème
   - Étapes pour reproduire
   - Logs d'erreur
   - Version Python et OS
   - Configuration (sans secrets)

### Q: L'application est-elle maintenue ?

**R:** Oui, maintenance active :
- **Mises à jour** : Mensuelles
- **Sécurité** : Patches immédiats
- **Dépendances** : Mises à jour régulières
- **Documentation** : Maintenue à jour

---

## 🔄 Mises à Jour

### Q: Comment mettre à jour l'application ?

**R:** 
```bash
# 1. Sauvegarder la configuration
cp .env .env.backup

# 2. Récupérer les mises à jour
git pull origin main

# 3. Mettre à jour les dépendances
pip install -r requirements.txt --upgrade

# 4. Vérifier la configuration
python -c "from config import get_config; get_config().validate_configuration()"

# 5. Tester
python main.py --test
```

### Q: Comment migrer d'une ancienne version ?

**R:** Consultez le [CHANGELOG.md] pour les breaking changes et les guides de migration spécifiques à chaque version.

---

*Cette FAQ est mise à jour régulièrement. Si votre question n'y figure pas, n'hésitez pas à [créer une issue](../../issues/new).*