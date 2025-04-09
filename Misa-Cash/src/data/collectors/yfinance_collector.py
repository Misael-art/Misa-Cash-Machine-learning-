from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import yfinance as yf

from .base_collector import BaseCollector
from ..utils.logger import get_logger
from ..cache.cache_decorator import cache_data

logger = get_logger(__name__)

class YFinanceCollector(BaseCollector):
    """Coletor de dados do Yahoo Finance usando yfinance."""
    
    def __init__(self, config: Dict = None):
        """
        Inicializa o coletor do Yahoo Finance.
        
        Args:
            config (Dict): Configurações do coletor
        """
        super().__init__(config)
        
    @cache_data(data_type='daily', expire_seconds=3600)  # Cache por 1 hora
    def get_daily_data(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Obtém dados diários do Yahoo Finance.
        
        Args:
            symbol (str): Símbolo do ativo
            start_date (datetime, opcional): Data inicial
            end_date (datetime, opcional): Data final
            
        Returns:
            pd.DataFrame: DataFrame com os dados diários
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(
                start=start_date,
                end=end_date,
                interval='1d'
            )
            
            # Renomear colunas para padrão
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao obter dados diários para {symbol}: {str(e)}")
            raise
            
    @cache_data(data_type='intraday', expire_seconds=300)  # Cache por 5 minutos
    def get_intraday_data(
        self,
        symbol: str,
        interval: str = "1min",
        limit: int = 1000
    ) -> pd.DataFrame:
        """
        Obtém dados intraday do Yahoo Finance.
        
        Args:
            symbol (str): Símbolo do ativo
            interval (str): Intervalo dos dados
            limit (int): Número máximo de registros
            
        Returns:
            pd.DataFrame: DataFrame com os dados intraday
        """
        try:
            ticker = yf.Ticker(symbol)
            
            # Converter intervalo para formato yfinance
            yf_interval = interval
            
            data = ticker.history(
                period=f"{limit}{interval[-3:]}",  # ex: "1000min"
                interval=yf_interval
            )
            
            # Renomear colunas para padrão
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            
            return data.head(limit)
            
        except Exception as e:
            logger.error(f"Erro ao obter dados intraday para {symbol}: {str(e)}")
            raise
            
    def get_symbols_list(self) -> List[str]:
        """
        Obtém lista de símbolos disponíveis.
        
        Returns:
            List[str]: Lista de símbolos
        """
        try:
            # yfinance não fornece lista completa de símbolos
            # Retornando alguns símbolos populares como exemplo
            return ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
        except Exception as e:
            logger.error(f"Erro ao obter lista de símbolos: {str(e)}")
            return []
        
    def check_health(self) -> bool:
        """
        Verifica a saúde do coletor.
        
        Returns:
            bool: True se estiver saudável, False caso contrário
        """
        try:
            # Tentar obter dados de um símbolo conhecido
            ticker = yf.Ticker('AAPL')
            _ = ticker.history(period='1d')
            return True
        except Exception as e:
            logger.error(f"Erro na verificação de saúde: {str(e)}")
            return False 