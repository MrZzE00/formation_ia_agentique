"""
Module de gestion des exceptions personnalisées.
Implémente une hiérarchie d'exceptions claire et informative.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import traceback


class FinancialOrchestratorError(Exception):
    """
    Classe de base pour toutes les exceptions de l'application.
    Fournit un contexte riche pour le debugging et le monitoring.
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None
    ):
        """
        Initialise l'exception avec un contexte détaillé.
        
        Args:
            message: Message d'erreur descriptif
            error_code: Code d'erreur unique pour identification
            context: Contexte additionnel (variables, état, etc.)
            original_exception: Exception originale si c'est un wrapper
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.context = context or {}
        self.original_exception = original_exception
        self.timestamp = datetime.utcnow()
        self.traceback = traceback.format_exc() if original_exception else None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'exception en dictionnaire pour logging/API.
        
        Returns:
            Dict contenant toutes les informations de l'exception
        """
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
            "original_error": str(self.original_exception) if self.original_exception else None,
            "traceback": self.traceback
        }
    
    def __str__(self) -> str:
        """Représentation string détaillée de l'exception."""
        parts = [f"[{self.error_code}] {self.message}"]
        if self.context:
            parts.append(f"Context: {self.context}")
        if self.original_exception:
            parts.append(f"Caused by: {self.original_exception}")
        return " | ".join(parts)


# --- Exceptions de Configuration ---

class ConfigurationError(FinancialOrchestratorError):
    """Erreur de configuration de l'application."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        """
        Initialise une erreur de configuration.
        
        Args:
            message: Description de l'erreur
            config_key: Clé de configuration problématique
            **kwargs: Arguments additionnels pour la classe parent
        """
        context = kwargs.pop("context", {})
        context["config_key"] = config_key
        super().__init__(
            message=message,
            error_code="CONFIG_ERROR",
            context=context,
            **kwargs
        )


class MissingAPIKeyError(ConfigurationError):
    """Clé API manquante ou invalide."""
    
    def __init__(self, api_name: str = "Google API"):
        """
        Initialise l'erreur de clé API manquante.
        
        Args:
            api_name: Nom de l'API concernée
        """
        super().__init__(
            message=f"{api_name} key is missing or invalid",
            config_key="api_key",
            context={"api_name": api_name}
        )


# --- Exceptions d'Agent ---

class AgentError(FinancialOrchestratorError):
    """Erreur liée à un agent CrewAI."""
    
    def __init__(self, agent_name: str, message: str, **kwargs):
        """
        Initialise une erreur d'agent.
        
        Args:
            agent_name: Nom de l'agent concerné
            message: Description de l'erreur
            **kwargs: Arguments additionnels
        """
        context = kwargs.pop("context", {})
        context["agent_name"] = agent_name
        super().__init__(
            message=message,
            error_code="AGENT_ERROR",
            context=context,
            **kwargs
        )


class AgentExecutionError(AgentError):
    """Erreur lors de l'exécution d'une tâche par un agent."""
    
    def __init__(self, agent_name: str, task_name: str, reason: str, **kwargs):
        """
        Initialise une erreur d'exécution d'agent.
        
        Args:
            agent_name: Nom de l'agent
            task_name: Nom de la tâche
            reason: Raison de l'échec
            **kwargs: Arguments additionnels
        """
        message = f"Agent '{agent_name}' failed to execute task '{task_name}': {reason}"
        context = kwargs.pop("context", {})
        context.update({"task_name": task_name, "failure_reason": reason})
        super().__init__(
            agent_name=agent_name,
            message=message,
            context=context,
            **kwargs
        )


class AgentTimeoutError(AgentError):
    """Timeout lors de l'exécution d'un agent."""
    
    def __init__(self, agent_name: str, timeout_seconds: int):
        """
        Initialise une erreur de timeout.
        
        Args:
            agent_name: Nom de l'agent
            timeout_seconds: Délai de timeout en secondes
        """
        super().__init__(
            agent_name=agent_name,
            message=f"Agent '{agent_name}' timed out after {timeout_seconds} seconds",
            context={"timeout_seconds": timeout_seconds}
        )


# --- Exceptions d'Outils ---

class ToolError(FinancialOrchestratorError):
    """Erreur liée à un outil."""
    
    def __init__(self, tool_name: str, message: str, **kwargs):
        """
        Initialise une erreur d'outil.
        
        Args:
            tool_name: Nom de l'outil
            message: Description de l'erreur
            **kwargs: Arguments additionnels
        """
        context = kwargs.pop("context", {})
        context["tool_name"] = tool_name
        super().__init__(
            message=message,
            error_code="TOOL_ERROR",
            context=context,
            **kwargs
        )


class FinancialDataError(ToolError):
    """Erreur lors de la récupération de données financières."""
    
    def __init__(self, ticker: str, reason: str, **kwargs):
        """
        Initialise une erreur de données financières.
        
        Args:
            ticker: Symbole boursier
            reason: Raison de l'échec
            **kwargs: Arguments additionnels
        """
        message = f"Failed to fetch financial data for {ticker}: {reason}"
        context = kwargs.pop("context", {})
        context.update({"ticker": ticker, "failure_reason": reason})
        super().__init__(
            tool_name="financial_tool",
            message=message,
            context=context,
            **kwargs
        )


# --- Exceptions de Sécurité ---

class SecurityError(FinancialOrchestratorError):
    """Erreur de sécurité détectée."""
    
    def __init__(self, message: str, threat_type: str, **kwargs):
        """
        Initialise une erreur de sécurité.
        
        Args:
            message: Description de la menace
            threat_type: Type de menace (injection, extraction, etc.)
            **kwargs: Arguments additionnels
        """
        context = kwargs.pop("context", {})
        context["threat_type"] = threat_type
        super().__init__(
            message=message,
            error_code="SECURITY_ERROR",
            context=context,
            **kwargs
        )


class PromptInjectionError(SecurityError):
    """Tentative d'injection de prompt détectée."""
    
    def __init__(self, user_input: str, detected_pattern: str):
        """
        Initialise une erreur d'injection de prompt.
        
        Args:
            user_input: Input utilisateur malveillant
            detected_pattern: Pattern de détection qui a matché
        """
        super().__init__(
            message="Prompt injection attempt detected",
            threat_type="prompt_injection",
            context={
                "user_input": user_input[:100],  # Tronquer pour sécurité
                "detected_pattern": detected_pattern
            }
        )


class RateLimitError(SecurityError):
    """Limite de taux dépassée."""
    
    def __init__(self, limit_type: str, limit: int, current: int):
        """
        Initialise une erreur de rate limit.
        
        Args:
            limit_type: Type de limite (per_minute, per_hour)
            limit: Limite configurée
            current: Nombre actuel de requêtes
        """
        super().__init__(
            message=f"Rate limit exceeded: {current}/{limit} {limit_type}",
            threat_type="rate_limit",
            context={
                "limit_type": limit_type,
                "limit": limit,
                "current_count": current
            }
        )


# --- Exceptions de Validation ---

class ValidationError(FinancialOrchestratorError):
    """Erreur de validation de données."""
    
    def __init__(self, field_name: str, value: Any, reason: str):
        """
        Initialise une erreur de validation.
        
        Args:
            field_name: Nom du champ invalide
            value: Valeur rejetée
            reason: Raison du rejet
        """
        super().__init__(
            message=f"Validation failed for '{field_name}': {reason}",
            error_code="VALIDATION_ERROR",
            context={
                "field_name": field_name,
                "invalid_value": str(value)[:100],
                "validation_reason": reason
            }
        )


class InvalidTickerError(ValidationError):
    """Ticker boursier invalide."""
    
    def __init__(self, ticker: str):
        """
        Initialise une erreur de ticker invalide.
        
        Args:
            ticker: Ticker invalide
        """
        super().__init__(
            field_name="ticker",
            value=ticker,
            reason=f"'{ticker}' is not a valid stock ticker symbol"
        )


# --- Gestionnaire d'Exceptions ---

class ExceptionHandler:
    """
    Gestionnaire centralisé pour le traitement des exceptions.
    Fournit des méthodes pour capturer, logger et transformer les exceptions.
    """
    
    @staticmethod
    def handle(exception: Exception, logger=None, reraise: bool = False) -> Dict[str, Any]:
        """
        Gère une exception de manière standardisée.
        
        Args:
            exception: Exception à gérer
            logger: Logger optionnel pour enregistrer l'erreur
            reraise: Si True, relance l'exception après traitement
            
        Returns:
            Dict contenant les détails de l'erreur
            
        Raises:
            L'exception originale si reraise=True
        """
        # Convertir en exception custom si ce n'en est pas une
        if not isinstance(exception, FinancialOrchestratorError):
            exception = FinancialOrchestratorError(
                message=str(exception),
                error_code="UNHANDLED_ERROR",
                original_exception=exception
            )
        
        error_dict = exception.to_dict()
        
        # Logger si disponible
        if logger:
            logger.error(
                f"Exception occurred: {exception.message}",
                extra={"error_details": error_dict}
            )
        
        # Relancer si demandé
        if reraise:
            raise exception
        
        return error_dict
    
    @staticmethod
    def create_user_friendly_message(exception: Exception) -> str:
        """
        Crée un message user-friendly depuis une exception.
        
        Args:
            exception: Exception source
            
        Returns:
            Message formaté pour l'utilisateur final
        """
        if isinstance(exception, MissingAPIKeyError):
            return "La clé API n'est pas configurée. Veuillez vérifier votre fichier .env"
        elif isinstance(exception, InvalidTickerError):
            return "Le symbole boursier fourni n'est pas valide"
        elif isinstance(exception, AgentTimeoutError):
            return "L'analyse prend trop de temps. Veuillez réessayer"
        elif isinstance(exception, PromptInjectionError):
            return "Entrée non autorisée détectée"
        elif isinstance(exception, RateLimitError):
            return "Trop de requêtes. Veuillez patienter avant de réessayer"
        elif isinstance(exception, FinancialDataError):
            return "Impossible de récupérer les données financières actuellement"
        else:
            return "Une erreur inattendue s'est produite. Veuillez réessayer"