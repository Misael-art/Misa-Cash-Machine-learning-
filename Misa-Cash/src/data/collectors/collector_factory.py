from typing import Dict, Optional
from .base_collector import BaseCollector
from .alpha_vantage_collector import AlphaVantageCollector
from .yfinance_collector import YFinanceCollector

class CollectorFactory:
    """Fábrica para criar instâncias de coletores de dados."""
    
    @staticmethod
    def create_collector(collector_type: str, config: Optional[Dict] = None) -> BaseCollector:
        """
        Cria uma instância do coletor especificado.
        
        Args:
            collector_type (str): Tipo do coletor ('alpha_vantage' ou 'yfinance')
            config (Dict, opcional): Configurações específicas do coletor
            
        Returns:
            BaseCollector: Instância do coletor
            
        Raises:
            ValueError: Se o tipo de coletor não for suportado
        """
        collectors = {
            'alpha_vantage': AlphaVantageCollector,
            'yfinance': YFinanceCollector
        }
        
        collector_class = collectors.get(collector_type.lower())
        if not collector_class:
            raise ValueError(f"Tipo de coletor não suportado: {collector_type}")
            
        return collector_class(config) 