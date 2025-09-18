"""
Module de monitoring et métriques pour l'orchestration CrewAI
"""
import time
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass, asdict, field
from enum import Enum


class MetricType(Enum):
    """Types de métriques trackées"""
    RESPONSE_LATENCY = "response_latency"
    TASK_COMPLETION_RATE = "task_completion_rate"
    TOOL_CALL_SUCCESS_RATE = "tool_call_success_rate"
    SECURITY_BREACH_ATTEMPTS = "security_breach_attempts"
    TOKEN_EFFICIENCY = "token_efficiency"


@dataclass
class MetricRecord:
    """Enregistrement d'une métrique"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metric_type: str = ""
    agent_name: str = ""
    value: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Métriques de performance agrégées"""
    total_requests: int = 0
    successful_completions: int = 0
    failed_completions: int = 0
    average_latency_ms: float = 0.0
    min_latency_ms: float = float('inf')
    max_latency_ms: float = 0.0
    tool_calls_total: int = 0
    tool_calls_successful: int = 0
    tool_calls_failed: int = 0
    security_breach_attempts: int = 0
    total_tokens_used: int = 0
    
    @property
    def task_completion_rate(self) -> float:
        """Calcule le taux de complétion des tâches"""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_completions / self.total_requests) * 100
    
    @property
    def tool_success_rate(self) -> float:
        """Calcule le taux de succès des appels d'outils"""
        if self.tool_calls_total == 0:
            return 0.0
        return (self.tool_calls_successful / self.tool_calls_total) * 100


class MonitoringSystem:
    """
    Système de monitoring centralisé pour tous les agents
    Implémente les métriques définies dans les fichiers YAML
    """
    
    def __init__(self, enable_persistence: bool = True):
        self.enable_persistence = enable_persistence
        self.start_time = time.time()
        
        # Métriques par agent
        self.agent_metrics: Dict[str, PerformanceMetrics] = {
            "AnalysteFinancier": PerformanceMetrics(),
            "RedacteurStrategique": PerformanceMetrics()
        }
        
        # Historique des métriques
        self.metrics_history: List[MetricRecord] = []
        
        # Timers actifs pour mesurer la latence
        self.active_timers: Dict[str, float] = {}
        
        # Configuration des alertes
        self.alert_thresholds = {
            "max_latency_ms": 5000,
            "min_success_rate": 80.0,
            "max_security_breaches": 5
        }
        
        # Créer le répertoire de logs si nécessaire
        if self.enable_persistence:
            self.logs_dir = Path(__file__).parent / "monitoring_logs"
            self.logs_dir.mkdir(exist_ok=True)
    
    def start_request(self, agent_name: str, request_id: str) -> None:
        """Démarre le tracking d'une requête"""
        self.active_timers[request_id] = time.time()
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].total_requests += 1
    
    def end_request(self, agent_name: str, request_id: str, success: bool = True) -> float:
        """Termine le tracking d'une requête et enregistre les métriques"""
        if request_id not in self.active_timers:
            return 0.0
        
        # Calculer la latence
        start_time = self.active_timers.pop(request_id)
        latency_ms = (time.time() - start_time) * 1000
        
        # Mettre à jour les métriques
        if agent_name in self.agent_metrics:
            metrics = self.agent_metrics[agent_name]
            
            if success:
                metrics.successful_completions += 1
            else:
                metrics.failed_completions += 1
            
            # Mettre à jour les statistiques de latence
            metrics.min_latency_ms = min(metrics.min_latency_ms, latency_ms)
            metrics.max_latency_ms = max(metrics.max_latency_ms, latency_ms)
            
            # Calculer la moyenne mobile
            total_completed = metrics.successful_completions + metrics.failed_completions
            if total_completed > 0:
                metrics.average_latency_ms = (
                    (metrics.average_latency_ms * (total_completed - 1) + latency_ms) 
                    / total_completed
                )
            
            # Enregistrer dans l'historique
            self._record_metric(
                MetricType.RESPONSE_LATENCY,
                agent_name,
                latency_ms,
                {"request_id": request_id, "success": success}
            )
            
            # Vérifier les alertes
            self._check_alerts(agent_name, metrics)
        
        return latency_ms
    
    def record_tool_call(self, agent_name: str, tool_name: str, success: bool) -> None:
        """Enregistre un appel d'outil"""
        if agent_name in self.agent_metrics:
            metrics = self.agent_metrics[agent_name]
            metrics.tool_calls_total += 1
            
            if success:
                metrics.tool_calls_successful += 1
            else:
                metrics.tool_calls_failed += 1
            
            self._record_metric(
                MetricType.TOOL_CALL_SUCCESS_RATE,
                agent_name,
                1.0 if success else 0.0,
                {"tool_name": tool_name}
            )
    
    def record_security_breach_attempt(self, agent_name: str, attempt_details: str) -> None:
        """Enregistre une tentative de violation de sécurité"""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].security_breach_attempts += 1
            
            self._record_metric(
                MetricType.SECURITY_BREACH_ATTEMPTS,
                agent_name,
                1.0,
                {"details": attempt_details}
            )
            
            # Alerte immédiate si dépassement du seuil
            if self.agent_metrics[agent_name].security_breach_attempts > self.alert_thresholds["max_security_breaches"]:
                self._trigger_alert(
                    agent_name,
                    "SECURITY",
                    f"Nombre de tentatives de violation dépassé: {self.agent_metrics[agent_name].security_breach_attempts}"
                )
    
    def record_token_usage(self, agent_name: str, tokens_used: int) -> None:
        """Enregistre l'utilisation de tokens"""
        if agent_name in self.agent_metrics:
            self.agent_metrics[agent_name].total_tokens_used += tokens_used
            
            self._record_metric(
                MetricType.TOKEN_EFFICIENCY,
                agent_name,
                float(tokens_used),
                {}
            )
    
    def _record_metric(self, metric_type: MetricType, agent_name: str, value: float, metadata: Dict[str, Any]) -> None:
        """Enregistre une métrique dans l'historique"""
        record = MetricRecord(
            metric_type=metric_type.value,
            agent_name=agent_name,
            value=value,
            metadata=metadata
        )
        self.metrics_history.append(record)
        
        # Persistance si activée
        if self.enable_persistence and len(self.metrics_history) % 10 == 0:
            self._persist_metrics()
    
    def _check_alerts(self, agent_name: str, metrics: PerformanceMetrics) -> None:
        """Vérifie les seuils d'alerte"""
        # Alerte sur la latence
        if metrics.max_latency_ms > self.alert_thresholds["max_latency_ms"]:
            self._trigger_alert(
                agent_name,
                "LATENCY",
                f"Latence maximale dépassée: {metrics.max_latency_ms:.2f}ms"
            )
        
        # Alerte sur le taux de succès
        if metrics.task_completion_rate < self.alert_thresholds["min_success_rate"]:
            self._trigger_alert(
                agent_name,
                "SUCCESS_RATE",
                f"Taux de succès faible: {metrics.task_completion_rate:.2f}%"
            )
    
    def _trigger_alert(self, agent_name: str, alert_type: str, message: str) -> None:
        """Déclenche une alerte"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "type": alert_type,
            "message": message
        }
        
        print(f"⚠️ ALERT [{alert_type}] for {agent_name}: {message}")
        
        # Log l'alerte
        if self.enable_persistence:
            alert_file = self.logs_dir / f"alerts_{datetime.now().strftime('%Y%m%d')}.json"
            alerts = []
            if alert_file.exists():
                with open(alert_file, 'r') as f:
                    alerts = json.load(f)
            alerts.append(alert)
            with open(alert_file, 'w') as f:
                json.dump(alerts, f, indent=2)
    
    def _persist_metrics(self) -> None:
        """Persiste les métriques sur disque"""
        if not self.enable_persistence:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metrics_file = self.logs_dir / f"metrics_{timestamp}.json"
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": time.time() - self.start_time,
            "agent_metrics": {
                name: asdict(metrics) 
                for name, metrics in self.agent_metrics.items()
            },
            "recent_history": [
                asdict(record) 
                for record in self.metrics_history[-100:]  # Garder les 100 dernières
            ]
        }
        
        with open(metrics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des métriques"""
        uptime = time.time() - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "uptime_formatted": self._format_uptime(uptime),
            "agents": {
                name: {
                    "total_requests": metrics.total_requests,
                    "success_rate": f"{metrics.task_completion_rate:.2f}%",
                    "avg_latency_ms": f"{metrics.average_latency_ms:.2f}",
                    "tool_success_rate": f"{metrics.tool_success_rate:.2f}%",
                    "security_breaches": metrics.security_breach_attempts,
                    "tokens_used": metrics.total_tokens_used
                }
                for name, metrics in self.agent_metrics.items()
            }
        }
    
    def _format_uptime(self, seconds: float) -> str:
        """Formate le temps de fonctionnement"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"
    
    def reset(self) -> None:
        """Réinitialise toutes les métriques"""
        self.agent_metrics = {
            "AnalysteFinancier": PerformanceMetrics(),
            "RedacteurStrategique": PerformanceMetrics()
        }
        self.metrics_history.clear()
        self.active_timers.clear()
        self.start_time = time.time()


# Instance globale du système de monitoring
monitoring_system = MonitoringSystem(enable_persistence=True)