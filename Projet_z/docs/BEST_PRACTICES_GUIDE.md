# 📚 GUIDE DES BONNES PRATIQUES - Formation Excellence Python

## Table des Matières
1. [Standards de Code](#standards-de-code)
2. [Architecture et Organisation](#architecture-et-organisation)
3. [Gestion des Erreurs](#gestion-des-erreurs)
4. [Logging et Monitoring](#logging-et-monitoring)
5. [Tests et Qualité](#tests-et-qualité)
6. [Sécurité](#sécurité)
7. [Performance](#performance)
8. [Documentation](#documentation)

---

## 1. Standards de Code 📝

### Type Hints Obligatoires
```python
# ❌ MAUVAIS
def calculate_price(amount, tax_rate):
    return amount * (1 + tax_rate)

# ✅ BON
def calculate_price(amount: float, tax_rate: float) -> float:
    """Calcule le prix TTC à partir du montant HT et du taux de taxe."""
    return amount * (1 + tax_rate)
```

### Docstrings Format Google
```python
def analyze_ticker(
    ticker: str,
    depth: str = "standard",
    include_predictions: bool = False
) -> FinancialAnalysis:
    """
    Analyse un ticker boursier avec la profondeur spécifiée.
    
    Args:
        ticker: Symbole boursier (ex: "AAPL")
        depth: Niveau d'analyse ("quick", "standard", "deep")
        include_predictions: Inclure les prédictions ML
        
    Returns:
        FinancialAnalysis: Analyse complète avec tendances
        
    Raises:
        InvalidTickerError: Si le ticker n'est pas valide
        FinancialDataError: Si les données ne peuvent être récupérées
        
    Example:
        >>> analysis = analyze_ticker("AAPL", depth="deep")
        >>> print(analysis.executive_summary)
    """
```

### Constantes et Configuration
```python
# ❌ MAUVAIS
def fetch_data(ticker):
    time.sleep(2)  # Magic number
    if retries > 3:  # Magic number
        raise Exception("Failed")

# ✅ BON
from config import config

def fetch_data(ticker: str) -> dict:
    time.sleep(config.tools_config["financial_tool"]["retry_delays"][0])
    if retries > config.tools_config["financial_tool"]["max_retries"]:
        raise FinancialDataError(ticker, "Max retries exceeded")
```

---

## 2. Architecture et Organisation 🏗️

### Structure de Projet
```
projet/
├── src/                    # Code source
│   ├── agents/            # Agents CrewAI
│   ├── tools/             # Outils custom
│   ├── workflows/         # Orchestration
│   ├── models/            # Modèles Pydantic
│   ├── exceptions/        # Exceptions custom
│   └── utils/             # Utilitaires
├── tests/                  # Tests unitaires
├── config/                 # Configuration
├── logs/                   # Logs (gitignored)
├── docs/                   # Documentation
└── scripts/                # Scripts utilitaires
```

### Séparation des Responsabilités
```python
# ❌ MAUVAIS - Classe qui fait tout
class FinancialSystem:
    def fetch_data(self): ...
    def analyze(self): ...
    def save_to_db(self): ...
    def send_email(self): ...
    def generate_pdf(self): ...

# ✅ BON - Une responsabilité par classe
class DataFetcher:
    def fetch(self, ticker: str) -> RawData: ...

class Analyzer:
    def analyze(self, data: RawData) -> Analysis: ...

class Repository:
    def save(self, analysis: Analysis) -> None: ...

class NotificationService:
    def notify(self, analysis: Analysis) -> None: ...
```

---

## 3. Gestion des Erreurs 🚨

### Exceptions Spécifiques
```python
# ❌ MAUVAIS
try:
    data = fetch_financial_data(ticker)
except Exception as e:
    print(f"Error: {e}")

# ✅ BON
try:
    data = fetch_financial_data(ticker)
except InvalidTickerError as e:
    logger.warning(f"Invalid ticker provided: {e.context['ticker']}")
    return create_error_response(e)
except FinancialDataError as e:
    logger.error(f"Failed to fetch data: {e.to_dict()}")
    return apply_fallback_strategy(ticker)
except Exception as e:
    logger.critical(f"Unexpected error: {e}", exc_info=True)
    raise FinancialOrchestratorError(
        "System error occurred",
        original_exception=e
    )
```

### Pattern de Retry Intelligent
```python
from typing import TypeVar, Callable
import time

T = TypeVar('T')

def retry_with_exponential_backoff(
    func: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0
) -> T:
    """
    Retry une fonction avec backoff exponentiel.
    
    Args:
        func: Fonction à exécuter
        max_attempts: Nombre maximum de tentatives
        base_delay: Délai de base en secondes
        
    Returns:
        Résultat de la fonction
        
    Raises:
        Exception: Après épuisement des tentatives
    """
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = base_delay * (2 ** attempt)
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s")
            time.sleep(delay)
```

---

## 4. Logging et Monitoring 📊

### Logging Structuré
```python
# ❌ MAUVAIS
print(f"Processing ticker: {ticker}")
print("Error occurred!")

# ✅ BON
from logger_config import get_logger

logger = get_logger(__name__)

logger.info(
    "Processing ticker",
    extra={
        "ticker": ticker,
        "request_id": request_id,
        "user_id": user_id
    }
)

logger.error(
    "Analysis failed",
    extra={
        "ticker": ticker,
        "error_code": "ANALYSIS_TIMEOUT",
        "duration_ms": duration
    },
    exc_info=True
)
```

### Métriques et Monitoring
```python
from functools import wraps
from monitoring import monitoring_system

def with_monitoring(operation_name: str):
    """Décorateur pour monitorer les opérations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                monitoring_system.record_success(
                    operation_name,
                    duration_ms=(time.time() - start_time) * 1000
                )
                return result
            except Exception as e:
                monitoring_system.record_failure(
                    operation_name,
                    error=str(e),
                    duration_ms=(time.time() - start_time) * 1000
                )
                raise
        return wrapper
    return decorator

@with_monitoring("financial_analysis")
def analyze_financial_data(ticker: str) -> Analysis:
    # Votre code ici
    pass
```

---

## 5. Tests et Qualité 🧪

### Structure des Tests
```python
# test_financial_analyzer.py
import pytest
from unittest.mock import Mock, patch
from models import FinancialAnalysis

class TestFinancialAnalyzer:
    """Tests pour l'analyseur financier."""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture pour créer un analyzer."""
        return FinancialAnalyzer()
    
    @pytest.fixture
    def mock_data(self):
        """Fixture pour les données mockées."""
        return {
            "ticker": "AAPL",
            "price": 150.0,
            "volume": 1000000
        }
    
    def test_analyze_valid_ticker(self, analyzer, mock_data):
        """Test l'analyse d'un ticker valide."""
        # Arrange
        with patch('yfinance.Ticker') as mock_ticker:
            mock_ticker.return_value.info = mock_data
            
            # Act
            result = analyzer.analyze("AAPL")
            
            # Assert
            assert isinstance(result, FinancialAnalysis)
            assert result.ticker == "AAPL"
            assert len(result.trends) >= 1
    
    def test_analyze_invalid_ticker_raises_error(self, analyzer):
        """Test qu'un ticker invalide lève une exception."""
        # Act & Assert
        with pytest.raises(InvalidTickerError) as exc_info:
            analyzer.analyze("INVALID123")
        
        assert "not a valid stock ticker" in str(exc_info.value)
    
    @pytest.mark.parametrize("ticker,expected", [
        ("AAPL", True),
        ("MSFT", True),
        ("123", False),
        ("TOOLONG", False),
    ])
    def test_ticker_validation(self, analyzer, ticker, expected):
        """Test la validation des tickers avec différents cas."""
        assert analyzer.is_valid_ticker(ticker) == expected
```

### Tests de Performance
```python
import pytest
import time

def test_analysis_performance(benchmark):
    """Test que l'analyse respecte les contraintes de performance."""
    analyzer = FinancialAnalyzer()
    
    # Le benchmark de pytest mesure automatiquement
    result = benchmark(analyzer.analyze, "AAPL")
    
    # Assertions sur le résultat
    assert result is not None
    
    # Vérifier les statistiques de performance
    assert benchmark.stats['mean'] < 2.0  # Moins de 2 secondes en moyenne
```

---

## 6. Sécurité 🔒

### Validation des Entrées
```python
from models import TickerRequest
from exceptions import ValidationError

def validate_user_input(user_input: str) -> str:
    """
    Valide et sanitise l'entrée utilisateur.
    
    Args:
        user_input: Entrée brute de l'utilisateur
        
    Returns:
        Entrée validée et sanitisée
        
    Raises:
        ValidationError: Si l'entrée est invalide
        PromptInjectionError: Si injection détectée
    """
    # Validation Pydantic
    try:
        request = TickerRequest(ticker=user_input)
    except Exception as e:
        raise ValidationError("ticker", user_input, str(e))
    
    # Détection d'injection
    injection_patterns = config.security.malicious_patterns
    for pattern in injection_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            raise PromptInjectionError(user_input, pattern)
    
    return request.ticker
```

### Gestion des Secrets
```python
# ❌ MAUVAIS
API_KEY = "sk-1234567890abcdef"

# ✅ BON
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise MissingAPIKeyError("API_KEY")
```

---

## 7. Performance ⚡

### Mise en Cache
```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedDataFetcher:
    def __init__(self, cache_ttl: int = 300):
        self.cache_ttl = cache_ttl
        self.cache = {}
    
    def fetch(self, ticker: str) -> dict:
        """Récupère les données avec cache."""
        cache_key = ticker
        
        # Vérifier le cache
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                logger.debug(f"Cache hit for {ticker}")
                return data
        
        # Récupérer les nouvelles données
        logger.debug(f"Cache miss for {ticker}, fetching...")
        data = self._fetch_from_source(ticker)
        
        # Mettre en cache
        self.cache[cache_key] = (data, datetime.now())
        return data
```

### Traitement Asynchrone
```python
import asyncio
from typing import List

async def analyze_multiple_tickers(tickers: List[str]) -> List[Analysis]:
    """Analyse plusieurs tickers en parallèle."""
    tasks = [analyze_ticker_async(ticker) for ticker in tickers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Gérer les erreurs
    analyses = []
    for ticker, result in zip(tickers, results):
        if isinstance(result, Exception):
            logger.error(f"Failed to analyze {ticker}: {result}")
            analyses.append(create_error_analysis(ticker, result))
        else:
            analyses.append(result)
    
    return analyses
```

---

## 8. Documentation 📖

### README Structure
```markdown
# Project Name

## 🚀 Quick Start
Commandes essentielles pour démarrer rapidement

## 📋 Prerequisites
- Python 3.11+
- Dependencies list

## 🔧 Installation
Step-by-step installation

## 💡 Usage
Examples with code snippets

## 🏗️ Architecture
High-level architecture diagram

## 🧪 Testing
How to run tests

## 📊 Performance
Benchmarks and optimization tips

## 🔒 Security
Security considerations

## 📝 Contributing
How to contribute

## 📄 License
License information
```

### Commentaires de Code
```python
# ❌ MAUVAIS
# Increment x
x += 1

# ✅ BON (quand nécessaire)
# Applique la formule de Black-Scholes pour calculer le prix de l'option
# Référence: https://en.wikipedia.org/wiki/Black–Scholes_model
option_price = black_scholes(S, K, T, r, sigma)
```

---

## 🎯 Checklist Qualité

### Avant de Commiter
- [ ] Tests passent (`pytest`)
- [ ] Coverage > 80% (`pytest --cov`)
- [ ] Pas de warnings pylint (`pylint src/`)
- [ ] Code formaté (`black .`)
- [ ] Imports triés (`isort .`)
- [ ] Type hints vérifiés (`mypy src/`)
- [ ] Documentation à jour
- [ ] Pas de secrets dans le code

### Revue de Code
- [ ] Single Responsibility respectée
- [ ] DRY (Don't Repeat Yourself)
- [ ] KISS (Keep It Simple, Stupid)
- [ ] YAGNI (You Aren't Gonna Need It)
- [ ] Gestion d'erreurs appropriée
- [ ] Tests couvrent les cas limites
- [ ] Performance acceptable
- [ ] Sécurité validée

---

## 🔧 Outils Recommandés

### Développement
- **IDE**: VS Code avec extensions Python
- **Formatter**: Black
- **Linter**: Pylint + Flake8
- **Type Checker**: Mypy
- **Test Runner**: Pytest

### Monitoring
- **APM**: DataDog, New Relic
- **Logs**: ELK Stack, Datadog Logs
- **Metrics**: Prometheus + Grafana

### CI/CD
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: black --check .
      - run: isort --check-only .
      - run: pylint src/
      - run: mypy src/
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v2
```

---

## 📚 Ressources Formation

### Livres Essentiels
1. "Clean Code" - Robert C. Martin
2. "Design Patterns" - Gang of Four
3. "Effective Python" - Brett Slatkin
4. "Python Tricks" - Dan Bader

### Cours en Ligne
1. Python Best Practices (Real Python)
2. Design Patterns in Python (Udemy)
3. Test-Driven Development with Python

### Communautés
- Python Discord
- r/Python
- Stack Overflow
- Dev.to Python

---

*Ce guide est conçu pour garantir l'excellence du code dans un contexte de formation professionnelle.*