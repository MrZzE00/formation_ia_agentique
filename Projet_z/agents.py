"""
Définition des agents CrewAI basés sur les prompts YAML
"""
import yaml
from pathlib import Path
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import SearchFinancialTrendsRobust
import os


def load_agent_config(config_path: str) -> dict:
    """Charge la configuration d'un agent depuis un fichier YAML"""
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


class AnalysteFinancierAgent:
    """Agent Analyste Financier basé sur la configuration YAML"""
    
    def __init__(self):
        # Charger la configuration
        config_path = Path(__file__).parent / "prompt" / "AnalysteFinancier_v01.yaml"
        self.config = load_agent_config(str(config_path))
        
        # Initialiser le modèle LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.config['core_model']['model_name'],
            temperature=self.config['core_model']['parameters']['temperature'],
            max_tokens=self.config['core_model']['parameters']['max_tokens'],
            top_p=self.config['core_model']['parameters']['top_p'],
            top_k=self.config['core_model']['parameters']['top_k']
        )
        
        # Créer l'outil financier
        self.financial_tool = SearchFinancialTrendsRobust()
        
        # Extraire le system prompt complet
        system_prompt = self.config['goal_and_instructions']['system_prompt']
        
        # Créer l'agent CrewAI
        self.agent = Agent(
            role="Analyste Financier Senior",
            goal=self.config['goal_and_instructions']['overall_goal'],
            backstory="""Je suis un analyste financier senior avec 15 ans d'expérience dans l'analyse 
            des marchés financiers. Ma spécialité est d'identifier les tendances critiques 
            et de fournir des analyses objectives basées sur des données factuelles.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.financial_tool],
            llm=self.llm,
            max_iter=self.config['orchestration']['max_iterations'],
            memory=True,  # Active la mémoire transactionnelle
            system_template=system_prompt
        )
    
    def get_agent(self) -> Agent:
        """Retourne l'instance de l'agent CrewAI"""
        return self.agent


class RedacteurStrategiqueAgent:
    """Agent Rédacteur Stratégique basé sur la configuration YAML"""
    
    def __init__(self):
        # Charger la configuration
        config_path = Path(__file__).parent / "prompt" / "RedacteurStrategique_v01.yaml"
        self.config = load_agent_config(str(config_path))
        
        # Initialiser le modèle LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.config['core_model']['model_name'],
            temperature=self.config['core_model']['parameters']['temperature'],
            max_tokens=self.config['core_model']['parameters']['max_tokens'],
            top_p=self.config['core_model']['parameters']['top_p'],
            top_k=self.config['core_model']['parameters']['top_k']
        )
        
        # Extraire le system prompt complet
        system_prompt = self.config['goal_and_instructions']['system_prompt']
        
        # Créer l'agent CrewAI
        self.agent = Agent(
            role="Rédacteur Stratégique Senior",
            goal=self.config['goal_and_instructions']['overall_goal'],
            backstory="""Je suis un rédacteur stratégique senior spécialisé dans la transformation 
            d'analyses complexes en rapports clairs et actionnables pour les décideurs. 
            Mon expertise est de traduire le jargon technique en insights business compréhensibles.""",
            verbose=True,
            allow_delegation=False,
            tools=[],  # Pas d'outils pour cet agent
            llm=self.llm,
            memory=True,  # Active la mémoire transactionnelle
            system_template=system_prompt
        )
    
    def get_agent(self) -> Agent:
        """Retourne l'instance de l'agent CrewAI"""
        return self.agent


class AgentFactory:
    """Factory pour créer les agents avec leurs configurations"""
    
    @staticmethod
    def create_analyste_financier() -> Agent:
        """Crée et retourne un agent Analyste Financier"""
        return AnalysteFinancierAgent().get_agent()
    
    @staticmethod
    def create_redacteur_strategique() -> Agent:
        """Crée et retourne un agent Rédacteur Stratégique"""
        return RedacteurStrategiqueAgent().get_agent()
    
    @staticmethod
    def get_all_agents() -> dict:
        """Retourne tous les agents configurés"""
        return {
            "analyste_financier": AgentFactory.create_analyste_financier(),
            "redacteur_strategique": AgentFactory.create_redacteur_strategique()
        }