import os
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

from .base_collector import BaseCollector
from ..utils.logger import get_logger
from ..cache.cache_decorator import cache_data

logger = get_logger(__name__)

class AlphaVantageCollector(BaseCollector):
    """Coletor de dados do Alpha Vantage."""
    
    def __init__(self, config: Dict = None):
        """
        Inicializa o coletor do Alpha Vantage.
        
        Args:
            config (Dict): Configurações do coletor
        """
        super().__init__(config)
        self.api_key = config.get('api_key') or os.getenv('API_KEY_ALPHA_VANTAGE')
        if not self.api_key:
            raise ValueError("API_KEY_ALPHA_VANTAGE não encontrada")
            
        self.ts = TimeSeries(key=self.api_key, output_format='pandas')
        self.ti = TechIndicators(key=self.api_key, output_format='pandas')
        
    @cache_data(data_type='daily', expire_seconds=3600)  # Cache por 1 hora
    def get_daily_data(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Obtém dados diários do Alpha Vantage.
        
        Args:
            symbol (str): Símbolo do ativo
            start_date (datetime, opcional): Data inicial
            end_date (datetime, opcional): Data final
            
        Returns:
            pd.DataFrame: DataFrame com os dados diários
        """
        try:
            data, meta_data = self.ts.get_daily(symbol=symbol, outputsize='full')
            
            # Renomear colunas para padrão
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            
            # Filtrar por data se necessário
            if start_date:
                data = data[data.index >= pd.Timestamp(start_date)]
            if end_date:
                data = data[data.index <= pd.Timestamp(end_date)]
                
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
        Obtém dados intraday do Alpha Vantage.
        
        Args:
            symbol (str): Símbolo do ativo
            interval (str): Intervalo dos dados
            limit (int): Número máximo de registros
            
        Returns:
            pd.DataFrame: DataFrame com os dados intraday
        """
        try:
            # Converter intervalo para formato Alpha Vantage
            av_interval = interval.replace('min', '')
            
            data, meta_data = self.ts.get_intraday(
                symbol=symbol,
                interval=av_interval,
                outputsize='full'
            )
            
            # Renomear colunas para padrão
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            
            # Limitar número de registros
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
        # Alpha Vantage não fornece lista de símbolos diretamente
        # Retornando lista vazia por enquanto
        return []
        
    def check_health(self) -> bool:
        """
        Verifica a saúde do coletor.
        
        Returns:
            bool: True se estiver saudável, False caso contrário
        """
        try:
            # Tentar obter dados de um símbolo conhecido
            _, _ = self.ts.get_daily(symbol='AAPL', outputsize='compact')
            return True
        except Exception as e:
            logger.error(f"Erro na verificação de saúde: {str(e)}")
            return False 