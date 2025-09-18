"""
Configuration de la mémoire pour les agents CrewAI
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path


class TransactionalBuffer:
    """
    Implémentation d'un buffer transactionnel pour la mémoire à court terme
    Conforme aux spécifications YAML: clear_after_response
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.buffer: List[Dict[str, Any]] = []
        self.transaction_id: Optional[str] = None
        
    def start_transaction(self) -> str:
        """Démarre une nouvelle transaction"""
        self.transaction_id = f"{self.agent_name}_{datetime.now().isoformat()}"
        return self.transaction_id
    
    def add_to_buffer(self, data: Dict[str, Any]) -> None:
        """Ajoute des données au buffer de la transaction courante"""
        if self.transaction_id:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "transaction_id": self.transaction_id,
                "data": data
            }
            self.buffer.append(entry)
    
    def get_buffer_content(self) -> List[Dict[str, Any]]:
        """Récupère le contenu du buffer pour la transaction courante"""
        if self.transaction_id:
            return [
                entry for entry in self.buffer 
                if entry.get("transaction_id") == self.transaction_id
            ]
        return []
    
    def clear_after_response(self) -> None:
        """
        Vide le buffer après la réponse (retention_policy: clear_after_response)
        """
        if self.transaction_id:
            # Filtrer pour ne garder que les entrées des autres transactions
            self.buffer = [
                entry for entry in self.buffer 
                if entry.get("transaction_id") != self.transaction_id
            ]
            self.transaction_id = None
    
    def get_all_transactions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Récupère toutes les transactions groupées"""
        transactions = {}
        for entry in self.buffer:
            tid = entry.get("transaction_id")
            if tid not in transactions:
                transactions[tid] = []
            transactions[tid].append(entry)
        return transactions


class MemoryManager:
    """
    Gestionnaire centralisé de la mémoire pour tous les agents
    Gère à la fois la mémoire à court terme (transactionnelle) et long terme (désactivée)
    """
    
    def __init__(self, enable_persistence: bool = False):
        self.enable_persistence = enable_persistence
        self.short_term_memories: Dict[str, TransactionalBuffer] = {}
        self.long_term_enabled = False  # Désactivé selon les specs YAML
        self.memory_stats: Dict[str, Any] = {
            "transactions_processed": 0,
            "buffers_cleared": 0,
            "last_activity": None
        }
        
        # Créer le répertoire de persistance si nécessaire
        if self.enable_persistence:
            self.persistence_dir = Path(__file__).parent / "memory_store"
            self.persistence_dir.mkdir(exist_ok=True)
    
    def get_or_create_buffer(self, agent_name: str) -> TransactionalBuffer:
        """Obtient ou crée un buffer transactionnel pour un agent"""
        if agent_name not in self.short_term_memories:
            self.short_term_memories[agent_name] = TransactionalBuffer(agent_name)
        return self.short_term_memories[agent_name]
    
    def start_agent_transaction(self, agent_name: str) -> str:
        """Démarre une transaction pour un agent"""
        buffer = self.get_or_create_buffer(agent_name)
        transaction_id = buffer.start_transaction()
        self.memory_stats["last_activity"] = datetime.now().isoformat()
        return transaction_id
    
    def store_interaction(self, agent_name: str, interaction_type: str, content: Any) -> None:
        """Stocke une interaction dans la mémoire de l'agent"""
        buffer = self.get_or_create_buffer(agent_name)
        buffer.add_to_buffer({
            "type": interaction_type,
            "content": content,
            "agent": agent_name
        })
    
    def clear_agent_buffer(self, agent_name: str) -> None:
        """
        Vide le buffer d'un agent après réponse
        Implémente la politique retention_policy: clear_after_response
        """
        if agent_name in self.short_term_memories:
            self.short_term_memories[agent_name].clear_after_response()
            self.memory_stats["buffers_cleared"] += 1
    
    def get_agent_memory(self, agent_name: str) -> List[Dict[str, Any]]:
        """Récupère la mémoire courante d'un agent"""
        if agent_name in self.short_term_memories:
            return self.short_term_memories[agent_name].get_buffer_content()
        return []
    
    def complete_transaction(self, agent_name: str) -> None:
        """
        Complete une transaction et applique la politique de rétention
        """
        self.clear_agent_buffer(agent_name)
        self.memory_stats["transactions_processed"] += 1
        
        # Persistance optionnelle
        if self.enable_persistence:
            self._persist_transaction(agent_name)
    
    def _persist_transaction(self, agent_name: str) -> None:
        """Persiste une transaction sur disque (optionnel)"""
        if not self.enable_persistence:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.persistence_dir / f"{agent_name}_{timestamp}.json"
        
        memory_content = self.get_agent_memory(agent_name)
        if memory_content:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(memory_content, f, indent=2, ensure_ascii=False)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de la mémoire"""
        stats = self.memory_stats.copy()
        stats["active_buffers"] = len(self.short_term_memories)
        stats["buffer_details"] = {
            name: len(buffer.buffer) 
            for name, buffer in self.short_term_memories.items()
        }
        return stats
    
    def reset_all(self) -> None:
        """Réinitialise toute la mémoire"""
        for agent_name in list(self.short_term_memories.keys()):
            self.clear_agent_buffer(agent_name)
        self.short_term_memories.clear()
        self.memory_stats = {
            "transactions_processed": 0,
            "buffers_cleared": 0,
            "last_activity": None
        }


# Instance globale du gestionnaire de mémoire
memory_manager = MemoryManager(enable_persistence=False)