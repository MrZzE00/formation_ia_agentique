"""
Outils personnalisés pour l'orchestration CrewAI
"""
import time
import random
from typing import Dict, Any, Optional
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import yfinance as yf
from datetime import datetime, timedelta


class FinancialSearchInput(BaseModel):
    """Input pour l'outil de recherche de tendances financières"""
    ticker_symbol: str = Field(description="Le symbole boursier à rechercher, ex: 'GOOGL', 'AAPL'")


class SearchFinancialTrendsRobust(BaseTool):
    """Outil robuste pour rechercher les tendances financières d'un ticker"""
    
    name: str = "search_financial_trends_robust"
    description: str = "Recherche et retourne les 3 principales tendances financières (actualités, métriques, sentiment de marché) pour un symbole boursier (ticker) donné."
    args_schema: type[BaseModel] = FinancialSearchInput
    
    def _run(self, ticker_symbol: str) -> str:
        """
        Execute la recherche des tendances financières avec gestion d'erreur robuste
        """
        max_retries = 3
        retry_delays = [0, 2, 4]  # Délais en secondes pour les tentatives
        
        for attempt in range(max_retries):
            try:
                # Simulation d'appel API avec possibilité d'échec (pour tests)
                if ticker_symbol == "XYZ_INVALID":
                    raise Exception("Ticker invalide")
                
                # Récupération des données réelles via yfinance
                ticker = yf.Ticker(ticker_symbol.upper())
                
                # Obtenir les informations de base
                info = ticker.info
                history = ticker.history(period="1mo")
                
                if history.empty:
                    raise Exception(f"Aucune donnée disponible pour {ticker_symbol}")
                
                # Analyser les tendances
                trends = self._analyze_trends(ticker_symbol, info, history)
                
                # Formater le résultat
                result = self._format_trends(trends)
                
                return result
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delays[attempt + 1])
                    continue
                else:
                    return f"ERREUR: La récupération des données pour le ticker {ticker_symbol} a échoué après plusieurs tentatives. Détails: {str(e)}"
    
    def _analyze_trends(self, ticker: str, info: Dict, history: Any) -> list:
        """Analyse les données pour extraire les tendances clés"""
        trends = []
        
        # Tendance 1: Performance du prix
        if not history.empty:
            start_price = history['Close'].iloc[0]
            end_price = history['Close'].iloc[-1]
            price_change = ((end_price - start_price) / start_price) * 100
            
            trends.append({
                "titre": f"Variation du prix sur 30 jours: {price_change:.2f}%",
                "importance": "Critique" if abs(price_change) > 10 else "Élevée" if abs(price_change) > 5 else "Modérée",
                "impact": f"Le titre {'a gagné' if price_change > 0 else 'a perdu'} {abs(price_change):.2f}% sur le dernier mois, indiquant une {'tendance haussière' if price_change > 0 else 'pression baissière'}."
            })
        
        # Tendance 2: Volume de trading
        if not history.empty:
            avg_volume = history['Volume'].mean()
            recent_volume = history['Volume'].iloc[-5:].mean()
            volume_change = ((recent_volume - avg_volume) / avg_volume) * 100
            
            trends.append({
                "titre": f"Activité du volume: {volume_change:.1f}% vs moyenne",
                "importance": "Élevée" if abs(volume_change) > 50 else "Modérée",
                "impact": f"Le volume récent est {'supérieur' if volume_change > 0 else 'inférieur'} de {abs(volume_change):.1f}% à la moyenne, suggérant {'un intérêt accru' if volume_change > 0 else 'un intérêt réduit'}."
            })
        
        # Tendance 3: Volatilité
        if not history.empty:
            returns = history['Close'].pct_change().dropna()
            volatility = returns.std() * (252 ** 0.5) * 100  # Volatilité annualisée
            
            trends.append({
                "titre": f"Volatilité annualisée: {volatility:.1f}%",
                "importance": "Critique" if volatility > 40 else "Élevée" if volatility > 25 else "Modérée",
                "impact": f"La volatilité de {volatility:.1f}% indique un {'risque élevé' if volatility > 30 else 'risque modéré'} pour les investisseurs."
            })
        
        return trends[:3]  # Retourner seulement les 3 premières tendances
    
    def _format_trends(self, trends: list) -> str:
        """Formate les tendances pour l'agent"""
        result = "Tendances financières identifiées:\n\n"
        
        for i, trend in enumerate(trends, 1):
            result += f"Tendance {i}:\n"
            result += f"  Titre: {trend['titre']}\n"
            result += f"  Importance: {trend['importance']}\n"
            result += f"  Impact: {trend['impact']}\n\n"
        
        return result