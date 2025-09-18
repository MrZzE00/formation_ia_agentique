"""
Module de configuration centralisée de l'application.
Utilise Pydantic pour la validation et le pattern Singleton pour garantir une instance unique.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from pydantic import BaseSettings, Field, validator
from functools import lru_cache
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class LLMConfig(BaseSettings):
    """Configuration pour les modèles de langage."""
    
    model_name: str = Field(default="gemini/gemini-1.5-flash", description="Nom du modèle LLM")
    temperature: float = Field(default=0.1, ge=0.0, le=1.0, description="Température du modèle")
    max_tokens: int = Field(default=2048, gt=0, description="Nombre maximum de tokens")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p sampling")
    top_k: int = Field(default=40, gt=0, description="Top-k sampling")
    
    @validator('temperature')
    def validate_temperature(cls, v):
        """Valide que la température est dans une plage raisonnable."""
        if not 0 <= v <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        return v


class AgentConfig(BaseSettings):
    """Configuration pour les agents CrewAI."""
    
    max_iterations: int = Field(default=3, gt=0, description="Nombre maximum d'itérations")
    allow_delegation: bool = Field(default=False, description="Permet la délégation entre agents")
    verbose: bool = Field(default=True, description="Mode verbose pour debug")
    memory_enabled: bool = Field(default=True, description="Active la mémoire transactionnelle")
    
    # Stratégies disponibles
    available_strategies: List[str] = Field(
        default=[
            "sequential",
            "dynamic_context_assembly_with_prioritization",
            "parallel_with_validation"
        ]
    )
    default_strategy: str = Field(default="dynamic_context_assembly_with_prioritization")


class MonitoringConfig(BaseSettings):
    """Configuration pour le système de monitoring."""
    
    enable_monitoring: bool = Field(default=True, description="Active le monitoring")
    enable_persistence: bool = Field(default=True, description="Persiste les métriques")
    log_directory: Path = Field(default=Path("monitoring_logs"), description="Répertoire des logs")
    
    # Seuils d'alertes
    alert_thresholds: Dict[str, Any] = Field(
        default={
            "max_latency_ms": 5000,
            "min_success_rate": 0.8,
            "max_memory_mb": 500,
            "max_tokens_per_request": 4000
        }
    )
    
    # Métriques à collecter
    tracked_metrics: List[str] = Field(
        default=[
            "response_latency",
            "task_completion_rate",
            "tool_call_success_rate",
            "security_breach_attempts",
            "token_efficiency"
        ]
    )


class SecurityConfig(BaseSettings):
    """Configuration de sécurité."""
    
    enable_security_checks: bool = Field(default=True, description="Active les vérifications de sécurité")
    
    # Patterns de détection de tentatives malveillantes
    malicious_patterns: List[str] = Field(
        default=[
            r'(montre|affiche|donne).*prompt',
            r'system.*prompt',
            r'ignore.*instruction',
            r'bypass.*security',
            r'execute.*command',
            r'import.*os.*system'
        ]
    )
    
    # Limite de taux pour prévenir les abus
    rate_limit_enabled: bool = Field(default=True)
    max_requests_per_minute: int = Field(default=60, gt=0)
    max_requests_per_hour: int = Field(default=1000, gt=0)


class MemoryConfig(BaseSettings):
    """Configuration du système de mémoire."""
    
    memory_type: str = Field(default="transactional_buffer", description="Type de mémoire")
    clear_after_response: bool = Field(default=True, description="Nettoie après chaque réponse")
    enable_persistence: bool = Field(default=False, description="Persiste la mémoire")
    max_buffer_size: int = Field(default=1000, gt=0, description="Taille maximale du buffer")
    persistence_directory: Path = Field(default=Path("memory_store"), description="Répertoire de persistance")


class ApplicationConfig(BaseSettings):
    """Configuration principale de l'application avec pattern Singleton."""
    
    # Informations générales
    app_name: str = Field(default="Financial Orchestrator", description="Nom de l'application")
    version: str = Field(default="1.0.0", description="Version de l'application")
    environment: str = Field(default="development", description="Environnement (development/staging/production)")
    
    # Clés API
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    
    # Sous-configurations
    llm: LLMConfig = Field(default_factory=LLMConfig)
    agents: AgentConfig = Field(default_factory=AgentConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    
    # Configuration des outils
    tools_config: Dict[str, Any] = Field(
        default={
            "financial_tool": {
                "max_retries": 3,
                "retry_delays": [2, 4, 8],  # Exponential backoff
                "cache_ttl": 300,  # 5 minutes
                "timeout": 30
            }
        }
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Niveau de logging")
    enable_json_logs: bool = Field(default=False, description="Active les logs JSON")
    
    class Config:
        """Configuration Pydantic."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    @validator('google_api_key')
    def validate_api_key(cls, v):
        """Valide que la clé API est présente en production."""
        if not v and os.getenv("ENVIRONMENT") == "production":
            raise ValueError("GOOGLE_API_KEY is required in production")
        return v
    
    @validator('environment')
    def validate_environment(cls, v):
        """Valide l'environnement."""
        valid_envs = ["development", "staging", "production", "testing"]
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v
    
    def is_production(self) -> bool:
        """Vérifie si l'application est en production."""
        return self.environment == "production"
    
    def is_development(self) -> bool:
        """Vérifie si l'application est en développement."""
        return self.environment == "development"
    
    def get_log_config(self) -> Dict[str, Any]:
        """Retourne la configuration de logging."""
        return {
            "app_name": self.app_name,
            "log_level": self.log_level,
            "enable_json": self.enable_json_logs,
            "log_dir": self.monitoring.log_directory
        }


@lru_cache()
def get_config() -> ApplicationConfig:
    """
    Retourne l'instance unique de configuration (Singleton pattern).
    
    Returns:
        ApplicationConfig: Configuration de l'application
        
    Example:
        >>> config = get_config()
        >>> print(config.app_name)
        Financial Orchestrator
    """
    return ApplicationConfig()


# Alias pour faciliter l'import
config = get_config()


class ConfigManager:
    """
    Gestionnaire de configuration avec méthodes utilitaires.
    Implémente le pattern Facade pour simplifier l'accès à la configuration.
    """
    
    def __init__(self):
        """Initialise le gestionnaire avec la configuration."""
        self._config = get_config()
    
    @property
    def is_api_configured(self) -> bool:
        """Vérifie si l'API est correctement configurée."""
        return bool(self._config.google_api_key)
    
    @property
    def is_monitoring_enabled(self) -> bool:
        """Vérifie si le monitoring est activé."""
        return self._config.monitoring.enable_monitoring
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Retourne la configuration spécifique d'un agent.
        
        Args:
            agent_name: Nom de l'agent
            
        Returns:
            Dict contenant la configuration de l'agent
        """
        return {
            "llm_config": self._config.llm.dict(),
            "max_iterations": self._config.agents.max_iterations,
            "verbose": self._config.agents.verbose,
            "memory": self._config.agents.memory_enabled
        }
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """
        Retourne la configuration d'un outil spécifique.
        
        Args:
            tool_name: Nom de l'outil
            
        Returns:
            Dict contenant la configuration de l'outil
        """
        return self._config.tools_config.get(
            tool_name,
            {"max_retries": 3, "timeout": 30}
        )
    
    def validate_configuration(self) -> List[str]:
        """
        Valide la configuration complète et retourne les erreurs.
        
        Returns:
            Liste des erreurs de configuration
        """
        errors = []
        
        # Vérifier la clé API
        if not self._config.google_api_key:
            errors.append("GOOGLE_API_KEY not configured")
        
        # Vérifier les répertoires
        if self._config.monitoring.enable_persistence:
            if not self._config.monitoring.log_directory.exists():
                try:
                    self._config.monitoring.log_directory.mkdir(parents=True)
                except Exception as e:
                    errors.append(f"Cannot create log directory: {e}")
        
        # Vérifier les seuils
        if self._config.monitoring.alert_thresholds["max_latency_ms"] < 100:
            errors.append("Max latency threshold too low (< 100ms)")
        
        return errors


# Instance globale du gestionnaire
config_manager = ConfigManager()