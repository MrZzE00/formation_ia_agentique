"""
Application principale - Interface simple pour l'orchestration CrewAI
"""
import os
import argparse
from dotenv import load_dotenv
from workflow import run_financial_analysis, FinancialAnalysisWorkflow
from monitoring import monitoring_system
from memory import memory_manager


def setup_environment():
    """Configure l'environnement et les variables nécessaires"""
    # Charger les variables d'environnement
    load_dotenv()
    
    # Vérifier la présence de la clé API Google
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  ATTENTION: Variable d'environnement GOOGLE_API_KEY non trouvée")
        print("   Créez un fichier .env avec: GOOGLE_API_KEY=your_api_key_here")
        print("   Ou exportez la variable: export GOOGLE_API_KEY=your_api_key_here")
        return False
    
    return True


def display_banner():
    """Affiche la bannière de l'application"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════╗
║                    🚀 ORCHESTRATEUR FINANCIER CREWAI                    ║
║                                                                          ║
║  Agents: AnalysteFinancier + RedacteurStrategique                       ║
║  Tools:  search_financial_trends_robust                                 ║
║  Memory: Transactional Buffer (clear_after_response)                    ║
║  Monitoring: Latency, Success Rate, Security, Token Efficiency          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def display_menu():
    """Affiche le menu interactif"""
    menu = """
🔧 OPTIONS DISPONIBLES:

1. 📊 Analyser un ticker financier
2. 📈 Afficher les métriques de performance  
3. 🧠 Afficher l'état de la mémoire
4. 🧪 Lancer les tests de validation
5. 📋 Afficher le résumé du système
6. ❌ Quitter

Choisissez une option (1-6): """
    return input(menu).strip()


def analyze_ticker():
    """Interface pour analyser un ticker"""
    print("\n" + "="*60)
    print("📊 ANALYSE DE TICKER FINANCIER")
    print("="*60)
    
    ticker = input("\nEntrez le ticker à analyser (ex: AAPL, MSFT, GOOGL): ").strip().upper()
    
    if not ticker:
        print("❌ Ticker requis!")
        return
    
    # Validation basique du format ticker
    if not ticker.isalpha() or len(ticker) > 5:
        print("❌ Format de ticker invalide (1-5 lettres attendues)")
        return
    
    print(f"\n🔄 Analyse de {ticker} en cours...")
    
    try:
        run_financial_analysis(ticker)
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")


def display_metrics():
    """Affiche les métriques de performance"""
    print("\n" + "="*60)
    print("📈 MÉTRIQUES DE PERFORMANCE")
    print("="*60)
    
    summary = monitoring_system.get_summary()
    
    print(f"\n🕐 Temps de fonctionnement: {summary['uptime_formatted']}")
    print(f"⚡ Uptime en secondes: {summary['uptime_seconds']:.2f}")
    
    print(f"\n👥 STATISTIQUES PAR AGENT:")
    print("-" * 40)
    
    for agent_name, metrics in summary["agents"].items():
        print(f"\n🤖 {agent_name}:")
        print(f"   • Requêtes totales: {metrics['total_requests']}")
        print(f"   • Taux de succès: {metrics['success_rate']}")
        print(f"   • Latence moyenne: {metrics['avg_latency_ms']}ms")
        print(f"   • Taux succès outils: {metrics['tool_success_rate']}")
        print(f"   • Tentatives violation: {metrics['security_breaches']}")
        print(f"   • Tokens utilisés: {metrics['tokens_used']}")


def display_memory_status():
    """Affiche l'état de la mémoire"""
    print("\n" + "="*60)
    print("🧠 ÉTAT DE LA MÉMOIRE")
    print("="*60)
    
    memory_stats = memory_manager.get_memory_stats()
    
    print(f"\n📊 STATISTIQUES GÉNÉRALES:")
    print(f"   • Transactions traitées: {memory_stats['transactions_processed']}")
    print(f"   • Buffers nettoyés: {memory_stats['buffers_cleared']}")
    print(f"   • Buffers actifs: {memory_stats['active_buffers']}")
    print(f"   • Dernière activité: {memory_stats['last_activity'] or 'Aucune'}")
    
    print(f"\n💾 DÉTAILS DES BUFFERS:")
    if memory_stats['buffer_details']:
        for agent_name, buffer_size in memory_stats['buffer_details'].items():
            print(f"   • {agent_name}: {buffer_size} entrées")
    else:
        print("   • Aucun buffer actif")


def run_tests():
    """Lance les tests de validation"""
    print("\n" + "="*60)
    print("🧪 TESTS DE VALIDATION")
    print("="*60)
    
    print("\n🔄 Lancement des tests basiques...")
    
    try:
        # Importer et lancer les tests basiques
        from test_scenarios import (
            TestAnalysteFinancierBasicFunctionality,
            TestAnalysteFinancierSecurityTests
        )
        
        # Test de fonctionnalité de base
        print("\n1️⃣ Test de fonctionnalité de base...")
        test_basic = TestAnalysteFinancierBasicFunctionality()
        test_basic.setup_method()
        
        try:
            test_basic.test_analyse_ticker_aapl_success()
            print("   ✅ Test AAPL: SUCCÈS")
        except Exception as e:
            print(f"   ❌ Test AAPL: ÉCHEC - {e}")
        
        # Test de sécurité
        print("\n2️⃣ Test de sécurité...")
        test_security = TestAnalysteFinancierSecurityTests()
        test_security.setup_method()
        
        try:
            test_security.test_direct_prompt_request_blocked()
            print("   ✅ Test sécurité: SUCCÈS")
        except Exception as e:
            print(f"   ❌ Test sécurité: ÉCHEC - {e}")
        
        print(f"\n📋 Pour lancer tous les tests: pytest test_scenarios.py -v")
        
    except ImportError as e:
        print(f"❌ Erreur d'import des tests: {e}")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")


def display_system_summary():
    """Affiche un résumé complet du système"""
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DU SYSTÈME")
    print("="*60)
    
    print(f"\n🏗️ ARCHITECTURE:")
    print(f"   • Framework: CrewAI")
    print(f"   • LLM Provider: Google Gemini")
    print(f"   • Model: gemini-1.5-flash")
    print(f"   • Agents: 2 (AnalysteFinancier, RedacteurStrategique)")
    print(f"   • Outils: 1 (search_financial_trends_robust)")
    
    print(f"\n🔧 CONFIGURATION:")
    print(f"   • Stratégie orchestration: dynamic_context_assembly_with_prioritization")
    print(f"   • Max iterations: 3")
    print(f"   • Mémoire court terme: transactional_buffer")
    print(f"   • Mémoire long terme: désactivée")
    print(f"   • Politique rétention: clear_after_response")
    
    print(f"\n📊 MÉTRIQUES TRACKÉES:")
    print(f"   • Response latency")
    print(f"   • Task completion rate") 
    print(f"   • Tool call success rate")
    print(f"   • Security breach attempts")
    print(f"   • Token efficiency")
    
    print(f"\n🛡️ SÉCURITÉ:")
    print(f"   • Protection prompt système: ✅")
    print(f"   • Limitation de scope: ✅")
    print(f"   • Monitoring tentatives violation: ✅")
    
    # Afficher les métriques actuelles
    display_metrics()
    display_memory_status()


def interactive_mode():
    """Mode interactif principal"""
    while True:
        try:
            choice = display_menu()
            
            if choice == "1":
                analyze_ticker()
            elif choice == "2":
                display_metrics()
            elif choice == "3":
                display_memory_status()
            elif choice == "4":
                run_tests()
            elif choice == "5":
                display_system_summary()
            elif choice == "6":
                print("\n👋 Au revoir!")
                break
            else:
                print("❌ Choix invalide. Veuillez sélectionner 1-6.")
            
            input("\n🔄 Appuyez sur Entrée pour continuer...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            input("\n🔄 Appuyez sur Entrée pour continuer...")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Orchestrateur Financier CrewAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py                    # Mode interactif
  python main.py --ticker AAPL      # Analyse directe
  python main.py --metrics          # Afficher métriques
  python main.py --test             # Lancer tests
        """
    )
    
    parser.add_argument(
        "--ticker", "-t",
        help="Ticker à analyser directement"
    )
    parser.add_argument(
        "--metrics", "-m",
        action="store_true",
        help="Afficher les métriques de performance"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Lancer les tests de validation"
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Afficher le résumé complet du système"
    )
    
    args = parser.parse_args()
    
    # Afficher la bannière
    display_banner()
    
    # Vérifier l'environnement
    if not setup_environment():
        print("\n⚠️  Configuration requise. Veuillez configurer GOOGLE_API_KEY")
        return 1
    
    print("✅ Environnement configuré")
    
    # Mode ligne de commande
    if args.ticker:
        run_financial_analysis(args.ticker)
    elif args.metrics:
        display_metrics()
    elif args.test:
        run_tests()
    elif args.summary:
        display_system_summary()
    else:
        # Mode interactif par défaut
        print("\n🔄 Démarrage du mode interactif...")
        interactive_mode()
    
    return 0


if __name__ == "__main__":
    exit(main())