# 📖 API Reference

## Vue d'ensemble

Documentation complète de l'API de l'Orchestrateur Financier CrewAI.

## 🏗️ Architecture des Modules

### Core Modules

#### `main.py` - Point d'entrée principal

```python
def main() -> int:
    """
    Point d'entrée principal de l'application.
    
    Returns:
        int: Code de sortie (0 = succès, 1 = erreur)
    """

def analyze_ticker() -> None:
    """Interface pour analyser un ticker financier."""

def display_metrics() -> None:
    """Affiche les métriques de performance."""

def run_tests() -> None:
    """Lance les tests de validation."""
```

#### `config.py` - Configuration centralisée

```python
class ApplicationConfig(BaseSettings):
    """Configuration principale de l'application."""
    
    app_name: str = "Financial Orchestrator"
    version: str = "1.0.0"
    environment: str = "development"
    google_api_key: Optional[str] = None
    
    def is_production(self) -> bool:
        """Vérifie si l'application est en production."""
    
    def is_development(self) -> bool:
        """Vérifie si l'application est en développement."""

@lru_cache()
def get_config() -> ApplicationConfig:
    """Retourne l'instance unique de configuration (Singleton)."""

class ConfigManager:
    """Gestionnaire de configuration avec méthodes utilitaires."""
    
    @property
    def is_api_configured(self) -> bool:
        """Vérifie si l'API est correctement configurée."""
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Retourne la configuration spécifique d'un agent."""
    
    def validate_configuration(self) -> List[str]:
        """Valide la configuration complète et retourne les erreurs."""
```

---

## 🤖 Agents API

### `agents.py` - Factory et gestion des agents

```python
class AnalysteFinancierAgent:
    """Agent Analyste Financier basé sur la configuration YAML."""
    
    def __init__(self):
        """Initialise l'agent avec configuration YAML et LLM."""
    
    def get_agent(self) -> Agent:
        """Retourne l'instance de l'agent CrewAI."""

class RedacteurStrategiqueAgent:
    """Agent Rédacteur Stratégique basé sur la configuration YAML."""
    
    def __init__(self):
        """Initialise l'agent avec configuration YAML et LLM."""
    
    def get_agent(self) -> Agent:
        """Retourne l'instance de l'agent CrewAI."""

class AgentFactory:
    """Factory pour créer les agents avec leurs configurations."""
    
    @staticmethod
    def create_analyste_financier() -> Agent:
        """Crée et retourne un agent Analyste Financier."""
    
    @staticmethod
    def create_redacteur_strategique() -> Agent:
        """Crée et retourne un agent Rédacteur Stratégique."""
    
    @staticmethod
    def get_all_agents() -> Dict[str, Agent]:
        """Retourne tous les agents configurés."""
```

---

## 🔧 Workflow API

### `workflow.py` - Orchestration des tâches

```python
class FinancialAnalysisWorkflow:
    """Workflow principal pour l'analyse financière."""
    
    def __init__(self):
        """Initialise le workflow avec agents et monitoring."""
    
    def run_analysis(self, ticker: str) -> str:
        """
        Exécute l'analyse financière complète.
        
        Args:
            ticker: Symbole boursier à analyser
            
        Returns:
            str: Rapport final formaté
            
        Raises:
            InvalidTickerError: Si le ticker est invalide
            FinancialDataError: Si les données ne peuvent être récupérées
        """
    
    def _apply_fallback_strategy(self, ticker: str) -> str:
        """Applique la stratégie de fallback en cas d'erreur."""
    
    def _generate_mock_analysis(self, ticker: str) -> str:
        """Génère une analyse mockée pour les démonstrations."""

def run_financial_analysis(ticker: str) -> str:
    """
    Point d'entrée principal pour l'analyse financière.
    
    Args:
        ticker: Symbole boursier à analyser
        
    Returns:
        str: Rapport d'analyse formaté
    """
```

---

## 🛠️ Tools API

### `tools.py` - Outils financiers

```python
@tool("search_financial_trends_robust")
def search_financial_trends_robust(ticker: str) -> str:
    """
    Outil robuste de recherche de tendances financières.
    
    Args:
        ticker: Symbole boursier (ex: "AAPL", "MSFT")
        
    Returns:
        str: Données financières formatées avec tendances identifiées
        
    Example:
        >>> result = search_financial_trends_robust("AAPL")
        >>> print(result)
        Tendances financières identifiées:
        
        Tendance 1:
          Titre: Variation du prix sur 30 jours: 3.17%
          Importance: Modérée
          Impact: Le titre a gagné 3.17% sur le dernier mois...
    """

def get_financial_data_yfinance(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Récupère les données financières via yfinance.
    
    Args:
        ticker: Symbole boursier
        
    Returns:
        Optional[Dict]: Données financières ou None si erreur
    """

def generate_mock_financial_data(ticker: str) -> Dict[str, Any]:
    """
    Génère des données financières mockées pour les tests.
    
    Args:
        ticker: Symbole boursier
        
    Returns:
        Dict: Données mockées réalistes
    """
```

---

## 📊 Monitoring API

### `monitoring.py` - Système de monitoring

```python
class MonitoringSystem:
    """Système de monitoring complet pour l'application."""
    
    def __init__(self):
        """Initialise le système avec métriques et alertes."""
    
    def start_operation(self, agent_name: str, operation: str) -> str:
        """
        Démarre le monitoring d'une opération.
        
        Args:
            agent_name: Nom de l'agent
            operation: Type d'opération
            
        Returns:
            str: ID unique de l'opération
        """
    
    def record_success(self, agent_name: str, operation_id: str, duration_ms: float):
        """Enregistre le succès d'une opération."""
    
    def record_failure(self, agent_name: str, operation_id: str, error: str):
        """Enregistre l'échec d'une opération."""
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Retourne un résumé des métriques.
        
        Returns:
            Dict contenant:
            - uptime_seconds: Temps de fonctionnement
            - uptime_formatted: Temps formaté
            - agents: Métriques par agent
        """
    
    def trigger_alert(self, agent_name: str, alert_type: str, message: str, context: Dict = None):
        """Déclenche une alerte."""
    
    def save_metrics_to_file(self):
        """Sauvegarde les métriques dans un fichier JSON."""

# Instance globale
monitoring_system = MonitoringSystem()
```

---

## 🧠 Memory API

### `memory.py` - Gestion de la mémoire

```python
class MemoryManager:
    """Gestionnaire de mémoire transactionnelle pour les agents."""
    
    def __init__(self):
        """Initialise le gestionnaire avec buffer transactionnel."""
    
    def store_conversation(self, agent_name: str, user_input: str, agent_response: str):
        """
        Stocke une conversation dans le buffer.
        
        Args:
            agent_name: Nom de l'agent
            user_input: Entrée utilisateur
            agent_response: Réponse de l'agent
        """
    
    def get_context(self, agent_name: str) -> List[Dict[str, Any]]:
        """
        Récupère le contexte pour un agent.
        
        Args:
            agent_name: Nom de l'agent
            
        Returns:
            List: Historique des conversations
        """
    
    def clear_memory(self, agent_name: str = None):
        """Nettoie la mémoire (agent spécifique ou globale)."""
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques de mémoire.
        
        Returns:
            Dict contenant:
            - transactions_processed: Nombre total de transactions
            - buffers_cleared: Nombre de nettoyages
            - active_buffers: Buffers actuellement actifs
            - last_activity: Dernière activité
            - buffer_details: Détails par agent
        """

# Instance globale
memory_manager = MemoryManager()
```

---

## 📋 Models API

### `models.py` - Modèles de données Pydantic

```python
class TickerRequest(BaseModel):
    """Modèle pour une requête d'analyse de ticker."""
    
    ticker: str = Field(..., min_length=1, max_length=5)
    analysis_depth: str = Field(default="standard")
    include_predictions: bool = Field(default=False)
    
    @validator('ticker')
    def validate_ticker(cls, v: str) -> str:
        """Valide le format du ticker."""

class FinancialTrend(BaseModel):
    """Modèle pour une tendance financière."""
    
    title: str = Field(..., description="Titre de la tendance")
    importance: ImportanceLevel = Field(..., description="Niveau d'importance")
    impact: str = Field(..., description="Description de l'impact")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    
    def to_xml(self) -> str:
        """Convertit la tendance en format XML."""

class FinancialAnalysis(BaseModel):
    """Modèle pour une analyse financière complète."""
    
    ticker: str = Field(..., description="Symbole boursier analysé")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    executive_summary: str = Field(..., description="Résumé exécutif")
    trends: List[FinancialTrend] = Field(..., min_items=1, max_items=5)
    data_limitations: Optional[str] = Field(default=None)
    
    def to_xml(self) -> str:
        """Convertit l'analyse complète en XML."""
    
    def to_markdown(self) -> str:
        """Convertit l'analyse en format Markdown."""

class APIResponse(BaseModel):
    """Modèle standard pour les réponses API."""
    
    success: bool = Field(..., description="Indique si la requête a réussi")
    data: Optional[Any] = Field(default=None)
    error: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

## ❌ Exceptions API

### `exceptions.py` - Gestion des erreurs

```python
class FinancialOrchestratorError(Exception):
    """Classe de base pour toutes les exceptions de l'application."""
    
    def __init__(self, message: str, error_code: str = None, 
                 context: Dict[str, Any] = None, original_exception: Exception = None):
        """Initialise l'exception avec un contexte détaillé."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'exception en dictionnaire pour logging/API."""

class ConfigurationError(FinancialOrchestratorError):
    """Erreur de configuration de l'application."""

class MissingAPIKeyError(ConfigurationError):
    """Clé API manquante ou invalide."""

class AgentError(FinancialOrchestratorError):
    """Erreur liée à un agent CrewAI."""

class AgentExecutionError(AgentError):
    """Erreur lors de l'exécution d'une tâche par un agent."""

class ToolError(FinancialOrchestratorError):
    """Erreur liée à un outil."""

class FinancialDataError(ToolError):
    """Erreur lors de la récupération de données financières."""

class SecurityError(FinancialOrchestratorError):
    """Erreur de sécurité détectée."""

class PromptInjectionError(SecurityError):
    """Tentative d'injection de prompt détectée."""

class ValidationError(FinancialOrchestratorError):
    """Erreur de validation de données."""

class InvalidTickerError(ValidationError):
    """Ticker boursier invalide."""

class ExceptionHandler:
    """Gestionnaire centralisé pour le traitement des exceptions."""
    
    @staticmethod
    def handle(exception: Exception, logger=None, reraise: bool = False) -> Dict[str, Any]:
        """Gère une exception de manière standardisée."""
    
    @staticmethod
    def create_user_friendly_message(exception: Exception) -> str:
        """Crée un message user-friendly depuis une exception."""
```

---

## 📝 Logging API

### `logger_config.py` - Configuration du logging

```python
class JSONFormatter(logging.Formatter):
    """Formateur personnalisé pour générer des logs au format JSON."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Formate un enregistrement de log en JSON."""

class ColoredFormatter(logging.Formatter):
    """Formateur avec couleurs pour l'affichage console."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Formate un enregistrement avec des couleurs ANSI."""

def setup_logging(app_name: str = "FinancialOrchestrator", 
                 log_level: str = "INFO",
                 log_dir: Path = None,
                 enable_json: bool = True,
                 enable_console: bool = True,
                 enable_file: bool = True) -> logging.Logger:
    """
    Configure le système de logging pour l'application.
    
    Args:
        app_name: Nom de l'application pour identifier les logs
        log_level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Répertoire pour stocker les fichiers de logs
        enable_json: Active le format JSON pour les logs fichier
        enable_console: Active l'affichage des logs dans la console
        enable_file: Active l'écriture des logs dans des fichiers
        
    Returns:
        logging.Logger: Logger configuré pour l'application
    """

def get_logger(module_name: str) -> logging.Logger:
    """
    Obtient un logger pour un module spécifique.
    
    Args:
        module_name: Nom du module (généralement __name__)
        
    Returns:
        logging.Logger: Logger configuré pour le module
    """

class LoggerAdapter(logging.LoggerAdapter):
    """Adaptateur pour ajouter automatiquement du contexte aux logs."""
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Ajoute le contexte aux logs."""
```

---

## 📊 Usage Examples

### Exemple Complet d'Utilisation

```python
from config import get_config
from logger_config import get_logger
from workflow import run_financial_analysis
from monitoring import monitoring_system
from exceptions import InvalidTickerError, ExceptionHandler

# Configuration
config = get_config()
logger = get_logger(__name__)

# Validation et analyse
try:
    # Valider le ticker
    from models import TickerRequest
    request = TickerRequest(ticker="AAPL")
    
    # Démarrer le monitoring
    op_id = monitoring_system.start_operation("main", "full_analysis")
    
    # Exécuter l'analyse
    logger.info(f"Starting analysis for {request.ticker}")
    result = run_financial_analysis(request.ticker)
    
    # Succès
    monitoring_system.record_success("main", op_id, 2500.0)
    logger.info(f"Analysis completed successfully")
    
    print(result)
    
except InvalidTickerError as e:
    error_details = ExceptionHandler.handle(e, logger)
    print(f"Erreur: {ExceptionHandler.create_user_friendly_message(e)}")
    
except Exception as e:
    error_details = ExceptionHandler.handle(e, logger, reraise=False)
    print("Une erreur inattendue s'est produite")
```

### Exemple de Test Unitaire

```python
import pytest
from unittest.mock import patch, Mock
from models import FinancialAnalysis, TickerRequest
from workflow import FinancialAnalysisWorkflow

class TestFinancialWorkflow:
    @pytest.fixture
    def workflow(self):
        return FinancialAnalysisWorkflow()
    
    @pytest.fixture
    def mock_financial_data(self):
        return {
            "ticker": "AAPL",
            "price": 150.0,
            "volume": 1000000,
            "change_30d": 3.17
        }
    
    @patch('tools.get_financial_data_yfinance')
    def test_successful_analysis(self, mock_get_data, workflow, mock_financial_data):
        # Arrange
        mock_get_data.return_value = mock_financial_data
        
        # Act
        result = workflow.run_analysis("AAPL")
        
        # Assert
        assert "AAPL" in result
        assert "Analyse Stratégique" in result
        mock_get_data.assert_called_once_with("AAPL")
    
    def test_invalid_ticker_raises_error(self, workflow):
        with pytest.raises(InvalidTickerError):
            workflow.run_analysis("INVALID123")
```

---

## 📋 Response Schemas

### Successful Analysis Response

```json
{
  "success": true,
  "data": {
    "ticker": "AAPL",
    "analysis": "# Analyse Stratégique\n\nL'analyse des données financières...",
    "timestamp": "2024-01-01T12:00:00Z",
    "execution_time_ms": 2500,
    "agents_used": ["AnalysteFinancier", "RedacteurStrategique"]
  },
  "error": null,
  "request_id": "req_123456"
}
```

### Error Response

```json
{
  "success": false,
  "data": null,
  "error": "Invalid ticker format: INVALID123",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req_123456"
}
```

---

## 🔧 Configuration Reference

### Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GOOGLE_API_KEY` | string | None | Clé API Google Gemini (requis) |
| `LOG_LEVEL` | string | "INFO" | Niveau de logging |
| `ENVIRONMENT` | string | "development" | Environnement (dev/staging/prod) |
| `ENABLE_MONITORING` | boolean | true | Active le monitoring |
| `ENABLE_JSON_LOGS` | boolean | false | Logs au format JSON |

### Configuration Classes

Voir [CONFIGURATION.md](CONFIGURATION.md) pour la documentation détaillée de la configuration.

---

*Cette documentation est générée automatiquement et maintenue à jour avec le code source.*