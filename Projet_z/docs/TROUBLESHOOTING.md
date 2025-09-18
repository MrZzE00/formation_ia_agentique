# 🔧 Guide de Dépannage

## Vue d'ensemble

Ce guide vous aide à résoudre les problèmes les plus courants de l'Orchestrateur Financier CrewAI.

## 🚨 Problèmes Critiques

### 1. Application ne démarre pas

#### Symptôme
```bash
$ python main.py
Traceback (most recent call last):
  File "main.py", line X, in <module>
    ImportError: No module named 'crewai'
```

#### Solutions
```bash
# 1. Vérifier l'environnement virtuel
which python
# Doit pointer vers venv/bin/python

# 2. Activer l'environnement
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Réinstaller les dépendances
pip install -r requirements.txt

# 4. Vérifier l'installation
python -c "import crewai; print('CrewAI OK')"
```

### 2. Erreur de clé API

#### Symptôme
```
❌ LLM Call Failed
Error: litellm.AuthenticationError: geminiException - API key not valid
```

#### Diagnostic
```bash
# Vérifier la clé API
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('API Key:', bool(os.getenv('GOOGLE_API_KEY')))
print('Length:', len(os.getenv('GOOGLE_API_KEY', '')))
"

# Tester la clé directement
curl "https://generativelanguage.googleapis.com/v1beta/models?key=VOTRE_CLE"
```

#### Solutions
1. **Regénérer la clé** sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Vérifier le fichier .env** :
   ```bash
   cat .env | grep GOOGLE_API_KEY
   ```
3. **Vérifier les quotas** Google Cloud

### 3. Timeout lors de l'analyse

#### Symptôme
```
🕐 Analysis timed out after 300 seconds
```

#### Solutions
```python
# 1. Augmenter le timeout dans config.py
class AgentConfig(BaseSettings):
    timeout_seconds: int = 600  # 10 minutes au lieu de 5

# 2. Réduire la complexité
class LLMConfig(BaseSettings):
    max_tokens: int = 1024  # Réduire de 2048 à 1024
    max_iterations: int = 2  # Réduire de 3 à 2
```

---

## 🔍 Diagnostic Systématique

### Script de Diagnostic Automatique

```bash
#!/bin/bash
# diagnostic.sh

echo "=== DIAGNOSTIC ORCHESTRATEUR FINANCIER ==="

# 1. Version Python
echo "Python Version:"
python --version

# 2. Environnement virtuel
echo -e "\nEnvironnement virtuel:"
which python

# 3. Dépendances critiques
echo -e "\nDépendances critiques:"
python -c "
import sys
modules = ['crewai', 'pydantic', 'yfinance', 'dotenv', 'yaml']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError:
        print(f'❌ {module} - MANQUANT')
"

# 4. Configuration
echo -e "\nConfiguration:"
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

configs = {
    'GOOGLE_API_KEY': bool(os.getenv('GOOGLE_API_KEY')),
    'LOG_LEVEL': os.getenv('LOG_LEVEL', 'Not set'),
    'ENVIRONMENT': os.getenv('ENVIRONMENT', 'Not set')
}

for key, value in configs.items():
    print(f'{key}: {value}')
"

# 5. Test de base
echo -e "\nTest de base:"
python -c "
try:
    from config import get_config
    config = get_config()
    print('✅ Configuration OK')
except Exception as e:
    print(f'❌ Configuration ERROR: {e}')
"

echo -e "\n=== FIN DIAGNOSTIC ==="
```

### Niveaux de Logging pour Debug

```python
# Dans .env pour debug approfondi
LOG_LEVEL=DEBUG
ENABLE_JSON_LOGS=false

# Logging spécifique par module
import logging

# Activer logs CrewAI
logging.getLogger('crewai').setLevel(logging.DEBUG)

# Activer logs LiteLLM
logging.getLogger('litellm').setLevel(logging.DEBUG)

# Activer logs requests
logging.getLogger('requests').setLevel(logging.DEBUG)
```

---

## 🐛 Problèmes Fréquents

### 1. Performance Dégradée

#### Symptôme
- Analyses > 10 secondes
- Mémoire qui augmente
- CPU élevé

#### Diagnostic
```python
# Profiler la performance
import time
import psutil
import tracemalloc

def profile_analysis():
    tracemalloc.start()
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024
    
    # Votre analyse ici
    result = run_financial_analysis("AAPL")
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Temps: {end_time - start_time:.2f}s")
    print(f"Mémoire: {end_memory - start_memory:.2f}MB")
    print(f"Peak mémoire: {peak / 1024 / 1024:.2f}MB")
```

#### Solutions
```python
# 1. Optimiser la configuration LLM
class LLMConfig(BaseSettings):
    max_tokens: int = 512      # Réduire
    temperature: float = 0.0   # Plus déterministe = plus rapide

# 2. Nettoyer la mémoire régulièrement
from memory import memory_manager
memory_manager.clear_memory()

# 3. Désactiver le verbose
class AgentConfig(BaseSettings):
    verbose: bool = False
```

### 2. Erreurs de Validation Pydantic

#### Symptôme
```
pydantic.error_wrappers.ValidationError: 1 validation error for TickerRequest
ticker
  Invalid ticker format: invalid123 (type=value_error)
```

#### Solutions
```python
# Debug validation
from models import TickerRequest
from pydantic import ValidationError

def debug_validation(ticker_input):
    try:
        request = TickerRequest(ticker=ticker_input)
        print(f"✅ Valid: {request.ticker}")
    except ValidationError as e:
        print(f"❌ Invalid: {e}")
        # Afficher détails
        for error in e.errors():
            print(f"  Field: {error['loc']}")
            print(f"  Error: {error['msg']}")
            print(f"  Type: {error['type']}")

# Tester différents formats
test_cases = ["AAPL", "aapl", "123", "TOOLONG", "A-B"]
for case in test_cases:
    debug_validation(case)
```

### 3. Problèmes de Mémoire

#### Symptôme
- `MemoryError`
- Application qui se ferme brutalement
- Swap élevé

#### Diagnostic
```python
# Monitoring mémoire en temps réel
import psutil
import threading
import time

def monitor_memory():
    """Monitore la mémoire en arrière-plan."""
    while True:
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        if memory_mb > 500:  # Seuil d'alerte
            print(f"⚠️ High memory usage: {memory_mb:.2f}MB")
        time.sleep(10)

# Démarrer monitoring
thread = threading.Thread(target=monitor_memory, daemon=True)
thread.start()
```

#### Solutions
```python
# 1. Limiter la taille des buffers
class MemoryConfig(BaseSettings):
    max_buffer_size: int = 100  # Réduire de 1000 à 100

# 2. Forcer le garbage collection
import gc
gc.collect()

# 3. Utiliser des générateurs au lieu de listes
def process_large_data():
    for item in large_dataset:  # Au lieu de [item for item in large_dataset]
        yield process_item(item)
```

---

## 🔧 Outils de Diagnostic

### 1. Health Check Endpoint

```python
# health_check.py
from config import get_config, ConfigManager
from logger_config import get_logger
import requests

def health_check():
    """Vérification complète de santé du système."""
    results = {
        "config": False,
        "api_key": False,
        "google_api": False,
        "dependencies": False,
        "disk_space": False
    }
    
    try:
        # Configuration
        config = get_config()
        config_manager = ConfigManager()
        results["config"] = True
        
        # API Key
        results["api_key"] = config_manager.is_api_configured
        
        # Test Google API
        if results["api_key"]:
            response = requests.get(
                f"https://generativelanguage.googleapis.com/v1beta/models",
                params={"key": config.google_api_key},
                timeout=10
            )
            results["google_api"] = response.status_code == 200
        
        # Dépendances
        import crewai, pydantic, yfinance
        results["dependencies"] = True
        
        # Espace disque
        import shutil
        free_space_gb = shutil.disk_usage(".").free / (1024**3)
        results["disk_space"] = free_space_gb > 1.0  # Au moins 1GB
        
    except Exception as e:
        print(f"Health check error: {e}")
    
    return results

if __name__ == "__main__":
    health = health_check()
    for check, status in health.items():
        emoji = "✅" if status else "❌"
        print(f"{emoji} {check}: {status}")
```

### 2. Log Analyzer

```python
# log_analyzer.py
import json
import re
from pathlib import Path
from collections import Counter, defaultdict

def analyze_logs(log_file="logs/financial_orchestrator.log"):
    """Analyse les logs pour identifier les patterns d'erreurs."""
    
    if not Path(log_file).exists():
        print(f"Log file not found: {log_file}")
        return
    
    errors = []
    warnings = []
    performance_issues = []
    
    with open(log_file, 'r') as f:
        for line in f:
            try:
                # Tenter de parser comme JSON
                log_entry = json.loads(line)
                level = log_entry.get('level', '')
                message = log_entry.get('message', '')
                
                if level == 'ERROR':
                    errors.append(message)
                elif level == 'WARNING':
                    warnings.append(message)
                
                # Détecter problèmes de performance
                if 'latency' in message and 'ms' in message:
                    latency_match = re.search(r'(\d+)ms', message)
                    if latency_match and int(latency_match.group(1)) > 5000:
                        performance_issues.append(message)
                        
            except json.JSONDecodeError:
                # Log format texte standard
                if 'ERROR' in line:
                    errors.append(line.strip())
                elif 'WARNING' in line:
                    warnings.append(line.strip())
    
    # Analyser les patterns
    print("=== ANALYSE DES LOGS ===")
    print(f"Erreurs trouvées: {len(errors)}")
    print(f"Warnings trouvés: {len(warnings)}")
    print(f"Problèmes de performance: {len(performance_issues)}")
    
    if errors:
        error_patterns = Counter(errors)
        print("\nTop erreurs:")
        for error, count in error_patterns.most_common(5):
            print(f"  {count}x: {error[:100]}...")
    
    if performance_issues:
        print(f"\nProblèmes de performance ({len(performance_issues)}):")
        for issue in performance_issues[-3:]:  # 3 derniers
            print(f"  {issue[:100]}...")

if __name__ == "__main__":
    analyze_logs()
```

### 3. Configuration Validator

```python
# validate_config.py
from config import get_config, ConfigManager
from pathlib import Path
import os

def validate_complete_config():
    """Validation exhaustive de la configuration."""
    
    print("=== VALIDATION CONFIGURATION ===")
    
    try:
        config = get_config()
        config_manager = ConfigManager()
        
        # 1. Fichiers requis
        required_files = [
            ".env",
            "prompt/AnalysteFinancier_v01.yaml",
            "prompt/RedacteurStrategique_v01.yaml"
        ]
        
        for file_path in required_files:
            if Path(file_path).exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - MANQUANT")
        
        # 2. Variables d'environnement
        env_vars = {
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "development")
        }
        
        for var, value in env_vars.items():
            if value:
                print(f"✅ {var}: {'*' * min(len(str(value)), 10)}")
            else:
                print(f"❌ {var}: NON DÉFINI")
        
        # 3. Configuration interne
        validation_errors = config_manager.validate_configuration()
        if validation_errors:
            print("\n❌ Erreurs de configuration:")
            for error in validation_errors:
                print(f"  - {error}")
        else:
            print("\n✅ Configuration interne valide")
        
        # 4. Répertoires
        required_dirs = ["logs", "monitoring_logs"]
        for dir_path in required_dirs:
            path = Path(dir_path)
            if path.exists():
                print(f"✅ {dir_path}/")
            else:
                print(f"⚠️ {dir_path}/ - Sera créé automatiquement")
        
    except Exception as e:
        print(f"❌ Erreur de validation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    validate_complete_config()
```

---

## 📊 Métriques de Debug

### Collecte de Métriques Détaillées

```python
# debug_metrics.py
import time
import psutil
from functools import wraps

class DebugMetrics:
    def __init__(self):
        self.metrics = {}
    
    def measure(self, operation_name):
        """Décorateur pour mesurer les performances."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                    error = None
                except Exception as e:
                    result = None
                    success = False
                    error = str(e)
                    raise
                finally:
                    end_time = time.time()
                    end_memory = psutil.Process().memory_info().rss
                    
                    self.metrics[operation_name] = {
                        "duration_ms": (end_time - start_time) * 1000,
                        "memory_delta_mb": (end_memory - start_memory) / 1024 / 1024,
                        "success": success,
                        "error": error,
                        "timestamp": time.time()
                    }
                
                return result
            return wrapper
        return decorator
    
    def report(self):
        """Génère un rapport des métriques."""
        print("=== DEBUG METRICS ===")
        for operation, metrics in self.metrics.items():
            status = "✅" if metrics["success"] else "❌"
            print(f"{status} {operation}:")
            print(f"  Duration: {metrics['duration_ms']:.2f}ms")
            print(f"  Memory: {metrics['memory_delta_mb']:.2f}MB")
            if metrics["error"]:
                print(f"  Error: {metrics['error']}")

# Usage
debug = DebugMetrics()

@debug.measure("financial_analysis")
def debug_financial_analysis(ticker):
    from workflow import run_financial_analysis
    return run_financial_analysis(ticker)

# Test
try:
    result = debug_financial_analysis("AAPL")
    debug.report()
except Exception as e:
    debug.report()
    raise
```

---

## 🆘 Cas d'Urgence

### Mode de Récupération

```python
# recovery_mode.py
import os
import sys
from pathlib import Path

def emergency_recovery():
    """Mode de récupération d'urgence."""
    
    print("🆘 MODE DE RÉCUPÉRATION D'URGENCE")
    
    # 1. Sauvegarder la configuration actuelle
    if Path(".env").exists():
        import shutil
        shutil.copy(".env", f".env.backup.{int(time.time())}")
        print("✅ Configuration sauvegardée")
    
    # 2. Reset configuration minimale
    minimal_config = """
# Configuration minimale d'urgence
GOOGLE_API_KEY=test_key_for_demo
LOG_LEVEL=DEBUG
ENVIRONMENT=development
ENABLE_MONITORING=false
TEST_MODE=true
"""
    
    with open(".env.emergency", "w") as f:
        f.write(minimal_config)
    print("✅ Configuration d'urgence créée")
    
    # 3. Test basique
    try:
        from dotenv import load_dotenv
        load_dotenv(".env.emergency")
        
        from config import get_config
        config = get_config()
        print("✅ Configuration d'urgence valide")
        
        # Test simple
        from tools import generate_mock_financial_data
        mock_data = generate_mock_financial_data("TEST")
        print("✅ Génération de données mockées OK")
        
        print("\n🔧 INSTRUCTIONS DE RÉCUPÉRATION:")
        print("1. Utilisez .env.emergency comme base")
        print("2. Ajoutez votre vraie clé API Google")
        print("3. Testez avec: python main.py --test")
        print("4. Restaurez progressivement votre configuration")
        
    except Exception as e:
        print(f"❌ Échec du mode de récupération: {e}")
        print("💡 Contactez le support avec ces informations")

if __name__ == "__main__":
    emergency_recovery()
```

### Script de Réinstallation Complète

```bash
#!/bin/bash
# reinstall.sh

echo "🔄 RÉINSTALLATION COMPLÈTE"

# Sauvegarder
echo "Sauvegarde de la configuration..."
cp .env .env.backup.$(date +%s) 2>/dev/null || echo "Pas de .env à sauvegarder"

# Nettoyer
echo "Nettoyage de l'environnement..."
rm -rf venv
rm -rf logs
rm -rf monitoring_logs
rm -rf __pycache__
find . -name "*.pyc" -delete

# Recréer
echo "Recréation de l'environnement..."
python -m venv venv
source venv/bin/activate

# Réinstaller
echo "Réinstallation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Restaurer configuration
if [ -f .env.backup.* ]; then
    latest_backup=$(ls -t .env.backup.* | head -1)
    cp "$latest_backup" .env
    echo "Configuration restaurée depuis $latest_backup"
fi

# Test
echo "Test de l'installation..."
python -c "from config import get_config; print('✅ Installation OK')"

echo "🎉 Réinstallation terminée"
```

---

## 📞 Escalade du Support

### Informations à Collecter

Avant de contacter le support, collectez ces informations :

```bash
# collect_debug_info.sh
echo "=== INFORMATIONS DE DEBUG ===" > debug_info.txt
echo "Date: $(date)" >> debug_info.txt
echo "User: $(whoami)" >> debug_info.txt
echo "OS: $(uname -a)" >> debug_info.txt
echo "Python: $(python --version)" >> debug_info.txt
echo "Pip: $(pip --version)" >> debug_info.txt

echo -e "\n=== CONFIGURATION ===" >> debug_info.txt
cat .env | sed 's/GOOGLE_API_KEY=.*/GOOGLE_API_KEY=***HIDDEN***/' >> debug_info.txt

echo -e "\n=== DERNIERS LOGS ===" >> debug_info.txt
tail -50 logs/financial_orchestrator_errors.log >> debug_info.txt 2>/dev/null || echo "Pas de logs d'erreur" >> debug_info.txt

echo -e "\n=== MÉTRIQUES RÉCENTES ===" >> debug_info.txt
ls -la monitoring_logs/ >> debug_info.txt 2>/dev/null || echo "Pas de monitoring" >> debug_info.txt

echo "Informations collectées dans debug_info.txt"
```

### Niveaux d'Urgence

1. **🟢 Normal** : Questions générales, améliorations
2. **🟡 Moyen** : Bugs non-bloquants, performance dégradée
3. **🟠 Élevé** : Fonctionnalité cassée, erreurs fréquentes
4. **🔴 Critique** : Application inutilisable, sécurité compromise

---

*Ce guide de dépannage est maintenu à jour avec les problèmes les plus fréquemment rencontrés.*