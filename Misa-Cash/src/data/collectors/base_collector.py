from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

class BaseCollector(ABC):
    """Interface base para coletores de dados financeiros."""
    
    def __init__(self, config: Dict = None):
        """
        Inicializa o coletor de dados.
        
        Args:
            config (Dict): Configurações específicas do coletor
        """
        self.config = config or {}
        
    @abstractmethod
    def get_daily_data(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Obtém dados diários para um símbolo específico.
        
        Args:
            symbol (str): Símbolo do ativo
            start_date (datetime, opcional): Data inicial
            end_date (datetime, opcional): Data final
            
        Returns:
            pd.DataFrame: DataFrame com os dados diários
        """
        pass
    
    @abstractmethod
    def get_intraday_data(
        self,
        symbol: str,
        interval: str = "1min",
        limit: int = 1000
    ) -> pd.DataFrame:
        """
        Obtém dados intraday para um símbolo específico.
        
        Args:
            symbol (str): Símbolo do ativo
            interval (str): Intervalo dos dados (ex: "1min", "5min", "15min", "30min", "60min")
            limit (int): Número máximo de registros
            
        Returns:
            pd.DataFrame: DataFrame com os dados intraday
        """
        pass
    
    @abstractmethod
    def get_symbols_list(self) -> List[str]:
        """
        Obtém lista de símbolos disponíveis.
        
        Returns:
            List[str]: Lista de símbolos
        """
        pass
    
    @abstractmethod
    def check_health(self) -> bool:
        """
        Verifica a saúde do coletor.
        
        Returns:
            bool: True se estiver saudável, False caso contrário
        """
        pass 