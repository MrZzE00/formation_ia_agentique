# ⚙️ Guide de Configuration

## Vue d'ensemble

Ce guide détaille toutes les options de configuration de l'Orchestrateur Financier CrewAI.

## 📁 Fichiers de Configuration

### 1. **Variables d'Environnement** (`.env`)

```bash
# Configuration principale
GOOGLE_API_KEY=your_google_api_key_here

# Logging
LOG_LEVEL=INFO
ENABLE_JSON_LOGS=false

# Monitoring  
ENABLE_MONITORING=true
ENABLE_MONITORING_PERSISTENCE=true

# Mémoire
ENABLE_MEMORY_PERSISTENCE=false

# Environnement
ENVIRONMENT=development

# Tests
TEST_MODE=false
```

### 2. **Configuration Centralisée** (`config.py`)

La configuration utilise Pydantic pour la validation automatique :

```python
from config import get_config

config = get_config()
print(config.app_name)  # "Financial Orchestrator"
print(config.llm.temperature)  # 0.1
```

## 🔧 Configuration par Module

### LLM Configuration

```python
class LLMConfig(BaseSettings):
    model_name: str = "gemini/gemini-1.5-flash"
    temperature: float = 0.1  # 0.0 (déterministe) à 1.0 (créatif)
    max_tokens: int = 2048    # Limite de tokens par réponse
    top_p: float = 0.9        # Nucleus sampling
    top_k: int = 40           # Top-k sampling
```

**Recommandations par cas d'usage :**
- **Analyse factuelle** : `temperature=0.1, top_p=0.8`
- **Rédaction créative** : `temperature=0.3, top_p=0.9`
- **Données critiques** : `temperature=0.0, top_p=0.7`

### Agents Configuration

```python
class AgentConfig(BaseSettings):
    max_iterations: int = 3          # Nombre max d'itérations par agent
    allow_delegation: bool = False   # Délégation entre agents
    verbose: bool = True             # Mode debug
    memory_enabled: bool = True      # Mémoire transactionnelle
    
    # Stratégies d'orchestration disponibles
    available_strategies: List[str] = [
        "sequential",                              # Séquentiel
        "dynamic_context_assembly_with_prioritization",  # Dynamique (défaut)
        "parallel_with_validation"                 # Parallèle
    ]
```

### Monitoring Configuration

```python
class MonitoringConfig(BaseSettings):
    enable_monitoring: bool = True
    enable_persistence: bool = True
    log_directory: Path = Path("monitoring_logs")
    
    # Seuils d'alertes
    alert_thresholds: Dict[str, Any] = {
        "max_latency_ms": 5000,      # Latence max acceptable
        "min_success_rate": 0.8,     # Taux de succès minimum
        "max_memory_mb": 500,        # Mémoire max
        "max_tokens_per_request": 4000  # Tokens max par requête
    }
    
    # Métriques trackées
    tracked_metrics: List[str] = [
        "response_latency",
        "task_completion_rate", 
        "tool_call_success_rate",
        "security_breach_attempts",
        "token_efficiency"
    ]
```

### Security Configuration

```python
class SecurityConfig(BaseSettings):
    enable_security_checks: bool = True
    
    # Patterns de détection malveillante
    malicious_patterns: List[str] = [
        r'(montre|affiche|donne).*prompt',
        r'system.*prompt',
        r'ignore.*instruction',
        r'bypass.*security'
    ]
    
    # Rate limiting
    rate_limit_enabled: bool = True
    max_requests_per_minute: int = 60
    max_requests_per_hour: int = 1000
```

## 🌍 Configuration par Environnement

### Development

```python
# .env.development
ENVIRONMENT=development
LOG_LEVEL=DEBUG
ENABLE_JSON_LOGS=false
ENABLE_MONITORING=true
TEST_MODE=false
```

### Staging

```python
# .env.staging  
ENVIRONMENT=staging
LOG_LEVEL=INFO
ENABLE_JSON_LOGS=true
ENABLE_MONITORING=true
TEST_MODE=false
```

### Production

```python
# .env.production
ENVIRONMENT=production
LOG_LEVEL=WARNING
ENABLE_JSON_LOGS=true
ENABLE_MONITORING=true
ENABLE_MONITORING_PERSISTENCE=true
TEST_MODE=false
```

### Testing

```python
# .env.testing
ENVIRONMENT=testing
LOG_LEVEL=DEBUG
ENABLE_MONITORING=false
TEST_MODE=true
GOOGLE_API_KEY=test_key_for_demo
```

## 🏗️ Configuration Avancée

### Custom Configuration Manager

```python
from config import ConfigManager

config_manager = ConfigManager()

# Vérifications de santé
if not config_manager.is_api_configured:
    raise MissingAPIKeyError("Google API")

if not config_manager.is_monitoring_enabled:
    print("⚠️ Monitoring désactivé")

# Configuration spécifique par agent
analyst_config = config_manager.get_agent_config("analyste_financier")
tool_config = config_manager.get_tool_config("financial_tool")
```

### Validation de Configuration

```python
# Validation automatique au démarrage
errors = config_manager.validate_configuration()

if errors:
    for error in errors:
        logger.error(f"Configuration error: {error}")
    sys.exit(1)
```

## 🔧 Configuration des Outils

### Financial Tool Configuration

```python
tools_config = {
    "financial_tool": {
        "max_retries": 3,           # Nombre max de retries
        "retry_delays": [2, 4, 8],  # Délais en secondes (exponential backoff)
        "cache_ttl": 300,           # TTL cache en secondes (5 min)
        "timeout": 30,              # Timeout requête en secondes
        "fallback_enabled": True,   # Active le fallback en cas d'échec
        "mock_data_enabled": False  # Active les données mockées
    }
}
```

### Logging Configuration

```python
# Configuration via code
from logger_config import setup_logging

logger = setup_logging(
    app_name="FinancialOrchestrator",
    log_level="INFO",
    log_dir=Path("logs"),
    enable_json=True,        # Logs JSON pour production
    enable_console=True,     # Logs console pour développement
    enable_file=True         # Logs fichiers
)
```

## 📊 Performance Tuning

### Optimisations par Charge

#### **Faible charge** (< 10 req/min)
```python
# Configuration optimisée pour latence
LLMConfig(
    temperature=0.1,
    max_tokens=2048,
    top_p=0.8
)

AgentConfig(
    max_iterations=3,
    verbose=True
)
```

#### **Charge moyenne** (10-100 req/min)
```python
# Configuration équilibrée
LLMConfig(
    temperature=0.1,
    max_tokens=1024,  # Réduit pour performance
    top_p=0.9
)

AgentConfig(
    max_iterations=2,  # Réduit les itérations
    verbose=False      # Moins de logs
)
```

#### **Forte charge** (> 100 req/min)
```python
# Configuration optimisée pour throughput
LLMConfig(
    temperature=0.1,
    max_tokens=512,    # Minimal pour rapidité
    top_p=0.9
)

AgentConfig(
    max_iterations=1,  # Une seule itération
    verbose=False,
    memory_enabled=False  # Désactive mémoire pour performance
)
```

## 🔐 Sécurité de la Configuration

### Protection des Secrets

```python
# ✅ BON - Variables d'environnement
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ❌ MAUVAIS - Hardcodé
GOOGLE_API_KEY = "AIzaSyAz-Kr4..."
```

### Validation des Configurations Sensibles

```python
@validator('google_api_key')
def validate_api_key(cls, v):
    if not v and os.getenv("ENVIRONMENT") == "production":
        raise ValueError("GOOGLE_API_KEY is required in production")
    if v and len(v) < 30:
        raise ValueError("API key seems too short")
    return v
```

## 🧪 Configuration pour Tests

### Mock Configuration

```python
# test_config.py
import pytest
from unittest.mock import patch
from config import get_config

@pytest.fixture
def mock_config():
    with patch.dict(os.environ, {
        'GOOGLE_API_KEY': 'test_key',
        'ENVIRONMENT': 'testing',
        'LOG_LEVEL': 'DEBUG'
    }):
        yield get_config()

def test_with_mock_config(mock_config):
    assert mock_config.environment == "testing"
    assert mock_config.google_api_key == "test_key"
```

### Configuration Overrides

```python
# Override pour tests spécifiques
def test_high_latency_threshold():
    config = get_config()
    config.monitoring.alert_thresholds["max_latency_ms"] = 10000
    
    # Test avec seuil élevé
    assert config.monitoring.alert_thresholds["max_latency_ms"] == 10000
```

## 📋 Checklist Configuration

### Avant Déploiement

- [ ] **API Keys** : Configurées et valides
- [ ] **Environnement** : Correctement défini
- [ ] **Logging** : Niveau approprié configuré
- [ ] **Monitoring** : Activé et testé
- [ ] **Seuils** : Ajustés pour l'environnement
- [ ] **Sécurité** : Patterns de détection actifs
- [ ] **Performance** : Optimisée pour la charge attendue
- [ ] **Backup** : Configuration sauvegardée

### Monitoring Configuration

- [ ] **Métriques** : Toutes les métriques importantes trackées
- [ ] **Alertes** : Seuils configurés et testés
- [ ] **Persistence** : Logs et métriques persistés
- [ ] **Rotation** : Logs avec rotation configurée
- [ ] **Dashboards** : Monitoring visible et actionnable

## 🔧 Dépannage Configuration

### Problèmes Courants

1. **API Key invalide**
   ```bash
   # Vérifier la clé
   python -c "from config import get_config; print(get_config().google_api_key)"
   ```

2. **Configuration non chargée**
   ```bash
   # Vérifier le fichier .env
   ls -la .env
   # Vérifier les variables
   python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
   ```

3. **Validation échoue**
   ```python
   # Debug validation
   from config import get_config
   try:
       config = get_config()
   except Exception as e:
       print(f"Configuration error: {e}")
   ```

## 📚 Ressources

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/usage/settings/)
- [Environment Variables Best Practices](https://12factor.net/config)
- [Configuration Management Patterns](https://microservices.io/patterns/externalized-configuration.html)