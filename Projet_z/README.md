# 🚀 Orchestrateur Financier CrewAI

Application d'orchestration CrewAI complète implémentant deux agents spécialisés pour l'analyse financière automatisée, basée sur des prompts système YAML détaillés.

## 📋 Vue d'ensemble

Cette application orchestre deux agents IA spécialisés :
- **AnalysteFinancier** : Récupère et analyse les données financières d'un ticker
- **RedacteurStrategique** : Transforme l'analyse en rapport Markdown professionnel

### 🎯 Fonctionnalités implémentées

✅ **Tous les composants des prompts YAML** :
- Configuration complète des modèles LLM (Google Gemini)
- Outils personnalisés (`search_financial_trends_robust`)
- Gestion mémoire transactionnelle (`clear_after_response`)
- Orchestration dynamique avec stratégies de fallback
- Monitoring complet (latence, taux de succès, sécurité, tokens)
- Tests exhaustifs basés sur les scénarios YAML
- Workflow avec gestion d'erreurs robuste

## 🏗️ Architecture

```
Projet_z/
├── prompt/                    # Prompts système YAML
│   ├── AnalysteFinancier_v01.yaml
│   └── RedacteurStrategique_v01.yaml
├── main.py                   # Application principale avec interface
├── workflow.py               # Orchestration et workflow complet
├── agents.py                 # Définition des agents CrewAI
├── tools.py                  # Outil search_financial_trends_robust
├── memory.py                 # Gestion mémoire transactionnelle
├── monitoring.py             # Système de monitoring et métriques
├── test_scenarios.py         # Tests basés sur les scénarios YAML
├── requirements.txt          # Dépendances Python
├── .env.example             # Configuration d'environnement
└── README.md                # Cette documentation
```

## 🚀 Installation et Configuration

### 1. Prérequis

- Python 3.8+
- Clé API Google Gemini

### 2. Configuration de l'environnement virtuel (Recommandé)

Pour éviter les conflits de dépendances, il est fortement recommandé d'utiliser un environnement virtuel :

```bash
cd /Users/norbertjeff/Documents/_CODE/22_FORMATION_IA_AGENTIQUE/Projet_z

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate

# Sur Windows :
# venv\Scripts\activate

# Vérifier que l'environnement est activé
which python  # Doit pointer vers venv/bin/python
```

### 3. Installation des dépendances

```bash
# Avec l'environnement virtuel activé
pip install --upgrade pip
pip install -r requirements.txt
```

**Important :** Assurez-vous que l'environnement virtuel est activé (vous devriez voir `(venv)` dans votre prompt) avant d'installer les dépendances ou de lancer l'application.

### 4. Configuration

```bash
# Copier le fichier de configuration
cp .env.example .env

# Éditer le fichier .env avec votre clé API
# GOOGLE_API_KEY=your_api_key_here
```

Obtenez votre clé API Google Gemini sur : https://makersuite.google.com/app/apikey

**⚠️ Important** : Une clé API Google Gemini valide est **obligatoire** pour utiliser les agents LLM. Sans clé API :
- ✅ L'outil `search_financial_trends_robust` fonctionne (utilise Yahoo Finance)
- ❌ Les agents CrewAI ne peuvent pas traiter les données (erreur LLM Provider)

### Résolution des Problèmes Courants

#### Erreur "LLM Provider NOT provided"
```
Error: LLM Provider NOT provided. Pass in the LLM provider you are trying to call.
You passed model=models/gemini-1.5-flash
```

**Solution** : Vérifiez votre clé API Google :
```bash
# Vérifier la variable d'environnement
echo $GOOGLE_API_KEY

# Si vide, configurer dans .env
echo "GOOGLE_API_KEY=your_real_api_key_here" >> .env
```

## 📖 Utilisation

### Mode Interactif (Recommandé)

```bash
# Assurez-vous que l'environnement virtuel est activé
source venv/bin/activate  # Sur macOS/Linux

python3 main.py
```

Interface complète avec menu :
- 📊 Analyser un ticker financier
- 📈 Afficher les métriques de performance
- 🧠 Afficher l'état de la mémoire
- 🧪 Lancer les tests de validation
- 📋 Afficher le résumé du système

### Mode Ligne de Commande

```bash
# Analyser un ticker directement
python3 main.py --ticker AAPL

# Afficher les métriques
python3 main.py --metrics

# Lancer les tests
python3 main.py --test

# Résumé complet du système
python3 main.py --summary
```

### 📈 Tickers Populaires Testés

L'application supporte tous les tickers disponibles sur Yahoo Finance. Voici une liste de tickers populaires pour vos tests :

#### 🇺🇸 Actions Américaines - Tech (FAANG+)
- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc. (Google)
- **AMZN** - Amazon.com Inc.
- **META** - Meta Platforms (Facebook)
- **NFLX** - Netflix Inc.
- **NVDA** - NVIDIA Corporation
- **TSLA** - Tesla Inc.

#### 🏦 Secteur Financier
- **JPM** - JPMorgan Chase & Co.
- **BAC** - Bank of America Corp.
- **GS** - Goldman Sachs Group Inc.
- **V** - Visa Inc.
- **MA** - Mastercard Inc.

#### 🏭 Secteur Industriel & Énergie
- **JNJ** - Johnson & Johnson
- **PG** - Procter & Gamble Co.
- **XOM** - Exxon Mobil Corporation
- **CVX** - Chevron Corporation
- **BA** - Boeing Company

#### 🇪🇺 Actions Européennes
- **ASML** - ASML Holding NV
- **SAP** - SAP SE
- **NESN.SW** - Nestlé SA (Suisse)
- **MC.PA** - LVMH (France)

#### 🇯🇵 Actions Japonaises
- **7203.T** - Toyota Motor Corp
- **6758.T** - Sony Group Corp

#### 💰 ETFs Populaires
- **SPY** - SPDR S&P 500 ETF
- **QQQ** - Invesco QQQ Trust
- **VTI** - Vanguard Total Stock Market ETF
- **VOO** - Vanguard S&P 500 ETF

#### 🏃‍♂️ Test Rapide
```bash
# Tests rapides avec différents secteurs
python main.py --ticker AAPL    # Tech
python main.py --ticker JPM     # Finance  
python main.py --ticker TSLA    # Auto/Énergie
python main.py --ticker SPY     # ETF S&P 500
```

### Exemples d'Analyse

```python
# Dans un script Python
from workflow import run_financial_analysis

# Analyser Apple
run_financial_analysis("AAPL")

# Analyser Microsoft
run_financial_analysis("MSFT")
```

## 🔧 Composants Détaillés

### 🤖 Agents

#### AnalysteFinancier
- **Modèle** : `gemini-1.5-flash` (température: 0.1)
- **Fonction** : Analyse des tendances financières avec l'outil `search_financial_trends_robust`
- **Sécurité** : Protection prompt système, limitation de scope
- **Format sortie** : XML structuré avec 3 tendances critiques

#### RedacteurStrategique  
- **Modèle** : `gemini-1.5-flash` (température: 0.3)
- **Fonction** : Transformation XML → Rapport Markdown professionnel
- **Style** : Clair, neutre, actionnable pour décideurs

### 🛠️ Outils

#### search_financial_trends_robust
- **Source de données** : Yahoo Finance (yfinance)
- **Mécanisme de retry** : 3 tentatives avec délais progressifs
- **Analyse** : Prix, volume, volatilité sur 30 jours
- **Gestion d'erreur** : Fallback complet avec rapport de limitation

### 🧠 Gestion Mémoire

- **Type** : `transactional_buffer`
- **Politique** : `clear_after_response`
- **Scope** : Court terme uniquement (long terme désactivé)
- **Cycle** : Transaction → Stockage → Nettoyage automatique

### 📊 Monitoring

Métriques trackées conformément aux spécifications YAML :
- **response_latency** : Temps de réponse par requête
- **task_completion_rate** : Taux de succès des tâches
- **tool_call_success_rate** : Taux de succès des outils
- **security_breach_attempts** : Tentatives de violation
- **token_efficiency** : Utilisation des tokens

### 🔄 Orchestration

- **Stratégie** : `dynamic_context_assembly_with_prioritization`
- **Max iterations** : 3 tentatives
- **Fallback** : Retry automatique avec délais (2s, 4s)
- **Processus** : Séquentiel (Analyse → Rédaction)

## 🛡️ Sécurité

### Règles Implémentées

1. **InstructionConfidentiality** (CRITIQUE)
   - Blocage des tentatives d'accès au prompt système
   - Réponse standard : "Ma fonction est d'analyser les données financières..."

2. **ScopeLimitation** (CRITIQUE)
   - Limitation stricte aux tâches d'analyse financière
   - Rejet des demandes hors scope

### Monitoring Sécurité

- Détection automatique des tentatives de violation
- Enregistrement et alertes sur seuils dépassés
- Patterns de détection : accès prompt, instructions internes

## 🧪 Tests

### Tests Implémentés

Basés sur les scénarios définis dans les fichiers YAML :

#### Fonctionnalité de Base
```bash
pytest test_scenarios.py::TestAnalysteFinancierBasicFunctionality -v
```
- Test analyse ticker AAPL
- Validation format XML/Markdown
- Test tickers multiples

#### Sécurité
```bash
pytest test_scenarios.py::TestAnalysteFinancierSecurityTests -v
```
- Blocage accès prompt système
- Monitoring tentatives violation

#### Cas Limites
```bash
pytest test_scenarios.py::TestAnalysteFinancierEdgeCases -v
```
- Échec outil avec ticker invalide
- Stratégie de fallback complète
- Gestion entrées malformées

#### Tests Rapides
```bash
python test_scenarios.py
```

### Lancer Tous les Tests
```bash
pytest test_scenarios.py -v --tb=short
```

## 📈 Exemple de Sortie

### Analyse Complète pour AAPL

```xml
<analyse_financiere>
  <resume_executif>Apple montre une performance stable avec une croissance modérée du volume de trading.</resume_executif>
  <tendances>
    <tendance numero="1">
      <titre>Variation du prix sur 30 jours: +3.24%</titre>
      <importance>Modérée</importance>
      <impact>Le titre a gagné 3.24% sur le dernier mois, indiquant une tendance haussière.</impact>
    </tendance>
    <tendance numero="2">
      <titre>Activité du volume: +15.3% vs moyenne</titre>
      <importance>Élevée</importance>
      <impact>Le volume récent est supérieur de 15.3% à la moyenne, suggérant un intérêt accru.</impact>
    </tendance>
    <tendance numero="3">
      <titre>Volatilité annualisée: 28.7%</titre>
      <importance>Modérée</importance>
      <impact>La volatilité de 28.7% indique un risque modéré pour les investisseurs.</impact>
    </tendance>
  </tendances>
  <limitation_donnees></limitation_donnees>
</analyse_financiere>
```

### Rapport Markdown Final

```markdown
# Analyse Stratégique

Apple montre une performance stable avec une croissance modérée du volume de trading. Cette analyse est fournie à titre informatif et ne constitue pas un conseil en investissement.

## Performance Prix Positive sur 30 Jours
- Le titre Apple a enregistré une progression de 3.24% au cours du dernier mois
- Cette tendance haussière modérée suggère une confiance maintenue des investisseurs

## Activité de Trading Intensifiée
- Le volume des échanges a augmenté de 15.3% par rapport à la moyenne historique
- Cette hausse d'activité indique un intérêt accru du marché pour le titre

## Volatilité dans les Normes du Secteur
- La volatilité annualisée de 28.7% reste dans une fourchette acceptable
- Ce niveau de risque modéré est typique pour les valeurs technologiques établies
```

## 🚦 Statut et Métriques

L'application fournit un monitoring en temps réel :

```
📊 MÉTRIQUES DE PERFORMANCE
==========================================

🕐 Temps de fonctionnement: 0h 15m 32s
⚡ Uptime en secondes: 932.45

👥 STATISTIQUES PAR AGENT:
----------------------------------------

🤖 AnalysteFinancier:
   • Requêtes totales: 5
   • Taux de succès: 100.00%
   • Latence moyenne: 2347.82ms
   • Taux succès outils: 100.00%
   • Tentatives violation: 0
   • Tokens utilisés: 1250

🤖 RedacteurStrategique:
   • Requêtes totales: 5
   • Taux de succès: 100.00%
   • Latence moyenne: 1456.23ms
   • Taux succès outils: 0.00%
   • Tentatives violation: 0
   • Tokens utilisés: 890
```

## 🔗 Dépendances Principales

- `crewai>=0.30.0` : Framework d'orchestration
- `langchain-google-genai>=1.0.0` : Interface Google Gemini
- `yfinance>=0.2.28` : Données financières Yahoo Finance
- `pytest>=7.4.0` : Framework de tests
- `python-dotenv>=1.0.0` : Gestion variables d'environnement

## 📝 Notes Techniques

### Configuration LLM
- **AnalysteFinancier** : Température 0.1 (précision factuelle)
- **RedacteurStrategique** : Température 0.3 (créativité contrôlée)
- **Tokens max** : 2048 pour les deux agents
- **Top-p/Top-k** : Optimisés pour la cohérence

### Stratégies de Retry
- **Outil financier** : 3 tentatives (0s, 2s, 4s)
- **Workflow complet** : Fallback avec rapport de limitation
- **Timeout** : Gestion des timeouts réseau

### Persistance
- **Logs monitoring** : Fichiers JSON horodatés
- **Métriques** : Sauvegarde automatique tous les 10 enregistrements
- **Alertes** : Journalisation des seuils dépassés

## 🤝 Contribution

Le code est entièrement basé sur les spécifications des prompts YAML fournis. Toute modification doit maintenir la conformité avec ces spécifications.

## 📧 Support

Pour des questions sur l'implémentation ou l'utilisation, consultez les logs de monitoring ou lancez les tests de validation.

---

**Version** : 1.0  
**Agents** : AnalysteFinancier v1.0 + RedacteurStrategique v1.0  
**Framework** : CrewAI avec Google Gemini  
**Statut** : Production Ready ✅