"""
Module de configuration du système de logging professionnel.
Implémente les bonnes pratiques de logging pour une application Python moderne.
"""

import logging
import logging.handlers
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import sys


class JSONFormatter(logging.Formatter):
    """
    Formateur personnalisé pour générer des logs au format JSON.
    Facilite l'analyse et le monitoring des logs en production.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formate un enregistrement de log en JSON.
        
        Args:
            record: L'enregistrement de log à formater
            
        Returns:
            str: Log formaté en JSON
        """
        log_obj = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }
        
        # Ajouter les informations d'exception si présentes
        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)
            
        # Ajouter les attributs personnalisés
        if hasattr(record, 'extra_data'):
            log_obj['extra'] = record.extra_data
            
        return json.dumps(log_obj)


class ColoredFormatter(logging.Formatter):
    """
    Formateur avec couleurs pour l'affichage console.
    Améliore la lisibilité des logs pendant le développement.
    """
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formate un enregistrement avec des couleurs ANSI.
        
        Args:
            record: L'enregistrement de log à formater
            
        Returns:
            str: Log formaté avec couleurs
        """
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    app_name: str = "FinancialOrchestrator",
    log_level: str = "INFO",
    log_dir: Path = None,
    enable_json: bool = True,
    enable_console: bool = True,
    enable_file: bool = True
) -> logging.Logger:
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
        
    Example:
        >>> logger = setup_logging("MyApp", "DEBUG")
        >>> logger.info("Application started", extra={'user_id': 123})
    """
    
    # Créer le logger principal
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.handlers = []  # Nettoyer les handlers existants
    
    # Configuration du répertoire de logs
    if log_dir is None:
        log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Handler Console avec couleurs
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        console_format = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
    
    # Handler Fichier avec rotation
    if enable_file:
        # Fichier de logs principal avec rotation
        log_file = log_dir / f"{app_name.lower()}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Format JSON ou texte selon configuration
        if enable_json:
            file_formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Fichier séparé pour les erreurs
        error_file = log_dir / f"{app_name.lower()}_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter() if enable_json else file_formatter)
        logger.addHandler(error_handler)
    
    return logger


def get_logger(module_name: str) -> logging.Logger:
    """
    Obtient un logger pour un module spécifique.
    
    Args:
        module_name: Nom du module (généralement __name__)
        
    Returns:
        logging.Logger: Logger configuré pour le module
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.debug("Debug message")
    """
    return logging.getLogger(f"FinancialOrchestrator.{module_name}")


class LoggerAdapter(logging.LoggerAdapter):
    """
    Adaptateur pour ajouter automatiquement du contexte aux logs.
    Utile pour tracer les requêtes à travers l'application.
    """
    
    def __init__(self, logger: logging.Logger, context: Dict[str, Any]):
        """
        Initialise l'adaptateur avec un contexte.
        
        Args:
            logger: Logger de base
            context: Contexte à ajouter à tous les logs
        """
        super().__init__(logger, context)
        
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """
        Ajoute le contexte aux logs.
        
        Args:
            msg: Message de log
            kwargs: Arguments additionnels
            
        Returns:
            tuple: Message et kwargs modifiés
        """
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra'].update(self.extra)
        kwargs['extra']['extra_data'] = kwargs['extra']
        return msg, kwargs


# Configuration par défaut au chargement du module
default_logger = setup_logging()