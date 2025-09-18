"""
Workflow principal d'orchestration CrewAI avec gestion complète des erreurs
"""
from crewai import Crew, Task, Process
from typing import Dict, Any, Optional
import re
import uuid
from agents import AgentFactory
from memory import memory_manager
from monitoring import monitoring_system


class FinancialAnalysisWorkflow:
    """
    Workflow complet pour l'analyse financière avec orchestration dynamique
    Implémente les stratégies définies dans les fichiers YAML
    """
    
    def __init__(self):
        # Créer les agents
        agents = AgentFactory.get_all_agents()
        self.analyste_financier = agents["analyste_financier"]
        self.redacteur_strategique = agents["redacteur_strategique"]
        
        # Configuration de l'orchestration
        self.orchestration_config = {
            "strategy": "dynamic_context_assembly_with_prioritization",
            "max_iterations": 3,
            "enable_delegation": False
        }
        
    def create_analysis_task(self, ticker: str) -> Task:
        """Crée la tâche d'analyse financière"""
        
        # Template de sortie attendu pour l'analyste
        output_template = """
<analyse_financiere>
  <resume_executif>[Résumé de l'analyse en une phrase concise.]</resume_executif>
  <tendances>
    <tendance numero="1">
      <titre>[Titre descriptif de la tendance 1]</titre>
      <importance>[Critique/Élevée/Modérée]</importance>
      <impact>[Description de l'impact potentiel de cette tendance.]</impact>
    </tendance>
    <tendance numero="2">
      <titre>[Titre descriptif de la tendance 2]</titre>
      <importance>[Critique/Élevée/Modérée]</importance>
      <impact>[Description de l'impact potentiel de cette tendance.]</impact>
    </tendance>
    <tendance numero="3">
      <titre>[Titre descriptif de la tendance 3]</titre>
      <importance>[Critique/Élevée/Modérée]</importance>
      <impact>[Description de l'impact potentiel de cette tendance.]</impact>
    </tendance>
  </tendances>
  <limitation_donnees>[Mention explicite si les données n'ont pas pu être obtenues. Laisser vide sinon.]</limitation_donnees>
</analyse_financiere>
"""
        
        # Appeler l'outil manuellement et intégrer le résultat
        from tools import search_financial_trends_robust
        try:
            tool_result = search_financial_trends_robust(ticker)
        except Exception as e:
            tool_result = f"ERREUR: Impossible de récupérer les données pour {ticker}: {str(e)}"

        description = f"""
        Analyser les données financières pour le ticker {ticker}.
        
        Données obtenues de l'outil financier:
        {tool_result}
        
        Mission:
        1. Analyser ces données pour identifier les 3 tendances les plus critiques
        2. Générer un rapport structuré au format XML selon le template fourni
        3. Si les données sont manquantes ou erronées, indiquer les limitations
        
        IMPORTANT: Le rapport DOIT être au format XML exact avec les balises <analyse_financiere>.
        
        Format attendu:
        {output_template}
        """
        
        return Task(
            description=description,
            agent=self.analyste_financier,
            expected_output=f"Une analyse financière structurée au format XML pour le ticker {ticker}"
        )
    
    def create_report_task(self, analysis_output: Optional[str] = None) -> Task:
        """Crée la tâche de rédaction du rapport stratégique"""
        
        description = """
        Transformer l'analyse financière XML en un rapport Markdown professionnel.
        
        Instructions:
        1. Parser le contenu de la balise <analyse_financiere> fournie
        2. Reformuler les tendances de manière claire et professionnelle
        3. Générer un rapport au format Markdown strict suivant:
           - Titre H1 "# Analyse Stratégique"
           - Introduction de deux phrases basée sur le résumé exécutif
           - 3 sections H2 pour chaque tendance avec 2 points de détail chacune
        
        IMPORTANT: La réponse doit être UNIQUEMENT le rapport Markdown, sans explications.
        """
        
        if analysis_output:
            description += f"\n\nAnalyse à transformer:\n{analysis_output}"
        
        return Task(
            description=description,
            agent=self.redacteur_strategique,
            expected_output="Un rapport Markdown professionnel formaté selon les spécifications",
            context_from_previous_task=True if not analysis_output else False
        )
    
    def validate_security(self, user_input: str) -> tuple[bool, str]:
        """
        Valide l'entrée utilisateur contre les règles de sécurité
        Retourne (is_valid, message)
        """
        # Vérifier les tentatives d'accès au prompt
        prompt_patterns = [
            r'(montre|affiche|donne).*prompt',
            r'system.*prompt',
            r'instructions?\s+internes?',
            r'configuration\s+interne'
        ]
        
        for pattern in prompt_patterns:
            if re.search(pattern, user_input.lower()):
                monitoring_system.record_security_breach_attempt(
                    "AnalysteFinancier",
                    f"Tentative d'accès au prompt: {user_input[:50]}..."
                )
                return False, "Ma fonction est d'analyser les données financières. Veuillez fournir un ticker."
        
        # Vérifier que l'entrée contient un ticker valide
        ticker_pattern = r'^[A-Z]{1,5}$'
        words = user_input.strip().split()
        
        has_ticker = any(re.match(ticker_pattern, word.upper()) for word in words)
        
        if not has_ticker and not any(keyword in user_input.lower() for keyword in ['analyse', 'ticker', 'action']):
            return False, "Veuillez fournir un symbole boursier (ticker) valide pour l'analyse."
        
        return True, ""
    
    def execute(self, ticker: str) -> Dict[str, Any]:
        """
        Execute le workflow complet avec gestion des erreurs et monitoring
        """
        request_id = str(uuid.uuid4())
        result = {
            "success": False,
            "ticker": ticker,
            "analysis": None,
            "report": None,
            "error": None,
            "metrics": {}
        }
        
        try:
            # Validation de sécurité
            is_valid, error_message = self.validate_security(ticker)
            if not is_valid:
                result["error"] = error_message
                return result
            
            # Extraire le ticker de l'entrée
            ticker_match = re.search(r'\b([A-Z]{1,5})\b', ticker.upper())
            if ticker_match:
                clean_ticker = ticker_match.group(1)
            else:
                clean_ticker = ticker.strip().upper()
            
            # Démarrer le monitoring
            monitoring_system.start_request("AnalysteFinancier", request_id)
            
            # Démarrer la transaction mémoire pour l'analyste
            transaction_id = memory_manager.start_agent_transaction("AnalysteFinancier")
            
            # Créer les tâches
            analysis_task = self.create_analysis_task(clean_ticker)
            report_task = self.create_report_task()
            
            # Créer et configurer le Crew
            crew = Crew(
                agents=[self.analyste_financier, self.redacteur_strategique],
                tasks=[analysis_task, report_task],
                process=Process.sequential,  # Processus séquentiel selon le workflow
                verbose=True,
                memory=False,  # Géré par notre MemoryManager
                max_iter=self.orchestration_config["max_iterations"]
            )
            
            # Stocker l'interaction dans la mémoire
            memory_manager.store_interaction(
                "AnalysteFinancier",
                "input",
                {"ticker": clean_ticker}
            )
            
            # Exécuter le workflow
            crew_output = crew.kickoff()
            
            # Enregistrer le succès de l'outil
            monitoring_system.record_tool_call(
                "AnalysteFinancier",
                "search_financial_trends_robust",
                True
            )
            
            # Parser les résultats
            if hasattr(crew_output, 'raw_output'):
                raw_output = crew_output.raw_output
            else:
                raw_output = str(crew_output)
            
            # Extraire l'analyse XML si présente
            xml_match = re.search(
                r'<analyse_financiere>.*?</analyse_financiere>',
                raw_output,
                re.DOTALL
            )
            
            if xml_match:
                result["analysis"] = xml_match.group(0)
                memory_manager.store_interaction(
                    "AnalysteFinancier",
                    "output",
                    {"analysis": result["analysis"]}
                )
            
            # Le rapport Markdown devrait être la sortie finale
            # Chercher le rapport après "# Analyse Stratégique"
            markdown_match = re.search(
                r'# Analyse Stratégique.*',
                raw_output,
                re.DOTALL
            )
            
            if markdown_match:
                result["report"] = markdown_match.group(0)
            else:
                # Si pas trouvé, prendre la dernière partie significative
                parts = raw_output.split('\n\n')
                if len(parts) > 1:
                    result["report"] = parts[-1]
            
            # Compléter les transactions mémoire
            memory_manager.complete_transaction("AnalysteFinancier")
            memory_manager.complete_transaction("RedacteurStrategique")
            
            # Terminer le monitoring
            latency = monitoring_system.end_request("AnalysteFinancier", request_id, success=True)
            
            # Ajouter les métriques au résultat
            result["success"] = True
            result["metrics"] = {
                "latency_ms": latency,
                "memory_stats": memory_manager.get_memory_stats(),
                "monitoring_summary": monitoring_system.get_summary()
            }
            
        except Exception as e:
            # Gestion des erreurs
            result["error"] = str(e)
            
            # Enregistrer l'échec
            monitoring_system.end_request("AnalysteFinancier", request_id, success=False)
            monitoring_system.record_tool_call(
                "AnalysteFinancier",
                "search_financial_trends_robust",
                False
            )
            
            # Nettoyer la mémoire
            memory_manager.complete_transaction("AnalysteFinancier")
            memory_manager.complete_transaction("RedacteurStrategique")
        
        return result
    
    def execute_with_fallback(self, ticker: str) -> Dict[str, Any]:
        """
        Execute le workflow avec stratégie de fallback complète
        """
        # Première tentative
        result = self.execute(ticker)
        
        # Si échec, appliquer la stratégie de fallback
        if not result["success"] and result["error"]:
            print(f"Première tentative échouée: {result['error']}")
            print("Application de la stratégie de fallback...")
            
            # Attendre et réessayer selon la configuration
            import time
            time.sleep(2)
            
            result = self.execute(ticker)
            
            if not result["success"]:
                # Dernière tentative après 4 secondes
                time.sleep(4)
                result = self.execute(ticker)
                
                if not result["success"]:
                    # Générer un rapport d'échec
                    result["report"] = f"""
# Analyse Stratégique - Données Indisponibles

La récupération des données pour le ticker {ticker} a échoué après plusieurs tentatives.

## Limitation des Données
- Les données de marché ne sont pas disponibles actuellement
- Veuillez réessayer ultérieurement ou vérifier la validité du ticker

## Actions Recommandées
- Vérifier que le ticker est correct et actif
- S'assurer de la connectivité réseau

## Support
- Pour plus d'assistance, veuillez contacter l'équipe support
"""
                    result["success"] = True  # Marqué comme succès avec limitation
        
        return result


# Fonction principale pour exécuter le workflow
def run_financial_analysis(ticker: str) -> None:
    """
    Point d'entrée principal pour l'analyse financière
    """
    print(f"\n🚀 Démarrage de l'analyse financière pour: {ticker}")
    print("=" * 60)
    
    workflow = FinancialAnalysisWorkflow()
    result = workflow.execute_with_fallback(ticker)
    
    print("\n📊 RÉSULTAT DE L'ANALYSE")
    print("=" * 60)
    
    if result["success"]:
        if result["report"]:
            print("\n📝 RAPPORT FINAL:")
            print(result["report"])
        
        if result["metrics"]:
            print("\n📈 MÉTRIQUES DE PERFORMANCE:")
            print(f"- Latence: {result['metrics'].get('latency_ms', 0):.2f}ms")
            
            if "monitoring_summary" in result["metrics"]:
                summary = result["metrics"]["monitoring_summary"]
                for agent_name, agent_metrics in summary.get("agents", {}).items():
                    print(f"\n{agent_name}:")
                    print(f"  - Requêtes totales: {agent_metrics['total_requests']}")
                    print(f"  - Taux de succès: {agent_metrics['success_rate']}")
                    print(f"  - Latence moyenne: {agent_metrics['avg_latency_ms']}ms")
    else:
        print(f"\n❌ ERREUR: {result.get('error', 'Erreur inconnue')}")
    
    print("\n" + "=" * 60)
    print("✅ Analyse terminée")


if __name__ == "__main__":
    # Test avec différents tickers
    test_ticker = "AAPL"
    run_financial_analysis(test_ticker)