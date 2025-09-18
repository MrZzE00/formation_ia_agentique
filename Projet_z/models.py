"""
Modèles de données avec validation Pydantic.
Assure l'intégrité des données à travers toute l'application.
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator, root_validator
import re


# --- Énumérations ---

class TaskStatus(str, Enum):
    """Statuts possibles pour une tâche."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentRole(str, Enum):
    """Rôles disponibles pour les agents."""
    ANALYST = "analyst"
    WRITER = "writer"
    VALIDATOR = "validator"
    ORCHESTRATOR = "orchestrator"


class ImportanceLevel(str, Enum):
    """Niveaux d'importance pour les tendances."""
    CRITIQUE = "Critique"
    ELEVEE = "Élevée"
    MODEREE = "Modérée"
    FAIBLE = "Faible"


# --- Modèles de Requête ---

class TickerRequest(BaseModel):
    """Modèle pour une requête d'analyse de ticker."""
    
    ticker: str = Field(
        ...,
        min_length=1,
        max_length=5,
        description="Symbole boursier à analyser"
    )
    analysis_depth: str = Field(
        default="standard",
        description="Profondeur d'analyse (quick/standard/deep)"
    )
    include_predictions: bool = Field(
        default=False,
        description="Inclure les prédictions dans l'analyse"
    )
    
    @validator('ticker')
    def validate_ticker(cls, v: str) -> str:
        """
        Valide le format du ticker.
        
        Args:
            v: Ticker à valider
            
        Returns:
            Ticker validé et normalisé
            
        Raises:
            ValueError: Si le ticker est invalide
        """
        # Normaliser en majuscules
        v = v.upper().strip()
        
        # Vérifier le format
        if not re.match(r'^[A-Z]{1,5}$', v):
            raise ValueError(f"Invalid ticker format: {v}")
        
        return v
    
    @validator('analysis_depth')
    def validate_depth(cls, v: str) -> str:
        """Valide la profondeur d'analyse."""
        valid_depths = ["quick", "standard", "deep"]
        if v not in valid_depths:
            raise ValueError(f"analysis_depth must be one of {valid_depths}")
        return v
    
    class Config:
        """Configuration du modèle."""
        schema_extra = {
            "example": {
                "ticker": "AAPL",
                "analysis_depth": "standard",
                "include_predictions": False
            }
        }


# --- Modèles de Données Financières ---

class FinancialTrend(BaseModel):
    """Modèle pour une tendance financière."""
    
    title: str = Field(..., description="Titre de la tendance")
    importance: ImportanceLevel = Field(..., description="Niveau d'importance")
    impact: str = Field(..., description="Description de l'impact")
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Niveau de confiance (0-1)"
    )
    data_points: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Points de données supportant la tendance"
    )
    
    @validator('title')
    def validate_title(cls, v: str) -> str:
        """Valide que le titre n'est pas vide."""
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
    
    def to_xml(self) -> str:
        """
        Convertit la tendance en format XML.
        
        Returns:
            Représentation XML de la tendance
        """
        return f"""
        <tendance>
            <titre>{self.title}</titre>
            <importance>{self.importance.value}</importance>
            <impact>{self.impact}</impact>
            <confiance>{self.confidence}</confiance>
        </tendance>
        """.strip()


class FinancialAnalysis(BaseModel):
    """Modèle pour une analyse financière complète."""
    
    ticker: str = Field(..., description="Symbole boursier analysé")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Horodatage de l'analyse"
    )
    executive_summary: str = Field(..., description="Résumé exécutif")
    trends: List[FinancialTrend] = Field(
        ...,
        min_items=1,
        max_items=5,
        description="Liste des tendances identifiées"
    )
    data_limitations: Optional[str] = Field(
        default=None,
        description="Limitations des données si applicables"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Métadonnées additionnelles"
    )
    
    @validator('trends')
    def validate_trends(cls, v: List[FinancialTrend]) -> List[FinancialTrend]:
        """Valide qu'il y a au moins une tendance critique ou élevée."""
        high_priority = [t for t in v if t.importance in [ImportanceLevel.CRITIQUE, ImportanceLevel.ELEVEE]]
        if not high_priority and len(v) > 0:
            # Au moins une tendance devrait être importante
            v[0].importance = ImportanceLevel.ELEVEE
        return v
    
    @root_validator
    def validate_consistency(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Valide la cohérence globale de l'analyse."""
        trends = values.get('trends', [])
        summary = values.get('executive_summary', '')
        
        # S'assurer que le résumé mentionne au moins une tendance
        if trends and not any(
            keyword in summary.lower() 
            for keyword in ['tendance', 'trend', 'hausse', 'baisse', 'volatilité']
        ):
            values['executive_summary'] = f"{summary} Les tendances identifiées sont détaillées ci-dessous."
        
        return values
    
    def to_xml(self) -> str:
        """
        Convertit l'analyse complète en XML.
        
        Returns:
            Représentation XML de l'analyse
        """
        trends_xml = "\n".join([t.to_xml() for t in self.trends])
        limitations = f"<limitation_donnees>{self.data_limitations}</limitation_donnees>" if self.data_limitations else "<limitation_donnees/>"
        
        return f"""
<analyse_financiere>
    <resume_executif>{self.executive_summary}</resume_executif>
    <tendances>
{trends_xml}
    </tendances>
    {limitations}
</analyse_financiere>
        """.strip()
    
    def to_markdown(self) -> str:
        """
        Convertit l'analyse en format Markdown.
        
        Returns:
            Représentation Markdown de l'analyse
        """
        md = f"# Analyse Financière - {self.ticker}\n\n"
        md += f"*Générée le {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC*\n\n"
        md += f"## Résumé Exécutif\n\n{self.executive_summary}\n\n"
        md += "## Tendances Identifiées\n\n"
        
        for i, trend in enumerate(self.trends, 1):
            md += f"### {i}. {trend.title}\n\n"
            md += f"**Importance:** {trend.importance.value}\n\n"
            md += f"**Impact:** {trend.impact}\n\n"
            md += f"**Confiance:** {trend.confidence:.1%}\n\n"
        
        if self.data_limitations:
            md += f"## Limitations\n\n{self.data_limitations}\n"
        
        return md


# --- Modèles de Tâches et Workflow ---

class TaskDefinition(BaseModel):
    """Modèle pour définir une tâche."""
    
    id: str = Field(..., description="Identifiant unique de la tâche")
    name: str = Field(..., description="Nom de la tâche")
    description: str = Field(..., description="Description détaillée")
    agent_role: AgentRole = Field(..., description="Rôle de l'agent assigné")
    dependencies: List[str] = Field(
        default_factory=list,
        description="IDs des tâches prérequises"
    )
    timeout_seconds: int = Field(
        default=300,
        gt=0,
        description="Timeout en secondes"
    )
    retry_policy: Dict[str, Any] = Field(
        default_factory=lambda: {"max_attempts": 3, "backoff": "exponential"},
        description="Politique de retry"
    )
    
    @validator('name')
    def validate_name(cls, v: str) -> str:
        """Valide le nom de la tâche."""
        if len(v) < 3:
            raise ValueError("Task name must be at least 3 characters")
        return v


class TaskResult(BaseModel):
    """Modèle pour le résultat d'une tâche."""
    
    task_id: str = Field(..., description="ID de la tâche")
    status: TaskStatus = Field(..., description="Statut final")
    result: Optional[Any] = Field(default=None, description="Résultat de la tâche")
    error: Optional[str] = Field(default=None, description="Message d'erreur si échec")
    start_time: datetime = Field(..., description="Heure de début")
    end_time: datetime = Field(..., description="Heure de fin")
    duration_ms: Optional[float] = Field(default=None, description="Durée en millisecondes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées")
    
    @root_validator
    def calculate_duration(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule automatiquement la durée si non fournie."""
        if not values.get('duration_ms'):
            start = values.get('start_time')
            end = values.get('end_time')
            if start and end:
                duration = (end - start).total_seconds() * 1000
                values['duration_ms'] = duration
        return values


# --- Modèles de Monitoring ---

class MetricPoint(BaseModel):
    """Point de métrique pour le monitoring."""
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metric_name: str = Field(..., description="Nom de la métrique")
    value: float = Field(..., description="Valeur de la métrique")
    unit: str = Field(default="count", description="Unité de mesure")
    tags: Dict[str, str] = Field(default_factory=dict, description="Tags additionnels")
    
    @validator('metric_name')
    def validate_metric_name(cls, v: str) -> str:
        """Valide le format du nom de métrique."""
        if not re.match(r'^[a-z_][a-z0-9_]*$', v):
            raise ValueError("Metric name must be snake_case")
        return v


class Alert(BaseModel):
    """Modèle pour une alerte de monitoring."""
    
    alert_type: str = Field(..., description="Type d'alerte")
    severity: str = Field(..., description="Sévérité (info/warning/error/critical)")
    message: str = Field(..., description="Message d'alerte")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    context: Dict[str, Any] = Field(default_factory=dict)
    resolved: bool = Field(default=False, description="Si l'alerte est résolue")
    
    @validator('severity')
    def validate_severity(cls, v: str) -> str:
        """Valide le niveau de sévérité."""
        valid_severities = ["info", "warning", "error", "critical"]
        if v.lower() not in valid_severities:
            raise ValueError(f"Severity must be one of {valid_severities}")
        return v.lower()


# --- Modèles de Réponse API ---

class APIResponse(BaseModel):
    """Modèle standard pour les réponses API."""
    
    success: bool = Field(..., description="Indique si la requête a réussi")
    data: Optional[Any] = Field(default=None, description="Données de la réponse")
    error: Optional[str] = Field(default=None, description="Message d'erreur si échec")
    error_code: Optional[str] = Field(default=None, description="Code d'erreur")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(default=None, description="ID de la requête pour traçabilité")
    
    @root_validator
    def validate_response(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Valide la cohérence de la réponse."""
        success = values.get('success')
        data = values.get('data')
        error = values.get('error')
        
        if success and error:
            raise ValueError("Cannot have both success=True and an error message")
        if not success and not error:
            values['error'] = "Unknown error occurred"
        
        return values
    
    class Config:
        """Configuration du modèle."""
        schema_extra = {
            "example": {
                "success": True,
                "data": {"ticker": "AAPL", "analysis": "..."},
                "error": None,
                "error_code": None,
                "timestamp": "2024-01-01T00:00:00Z",
                "request_id": "req_123456"
            }
        }


# --- Utilitaires de Validation ---

class DataValidator:
    """Classe utilitaire pour validations complexes."""
    
    @staticmethod
    def validate_ticker_list(tickers: List[str]) -> List[str]:
        """
        Valide une liste de tickers.
        
        Args:
            tickers: Liste de symboles boursiers
            
        Returns:
            Liste validée et normalisée
            
        Raises:
            ValueError: Si un ticker est invalide
        """
        validated = []
        for ticker in tickers:
            request = TickerRequest(ticker=ticker)
            validated.append(request.ticker)
        return validated
    
    @staticmethod
    def validate_date_range(start: datetime, end: datetime) -> tuple:
        """
        Valide une plage de dates.
        
        Args:
            start: Date de début
            end: Date de fin
            
        Returns:
            Tuple (start, end) validé
            
        Raises:
            ValueError: Si la plage est invalide
        """
        if start >= end:
            raise ValueError("Start date must be before end date")
        if end > datetime.utcnow():
            raise ValueError("End date cannot be in the future")
        return (start, end)