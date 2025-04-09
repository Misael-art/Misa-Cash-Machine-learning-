import os
import json
import redis
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Any, Dict

from ..utils.logger import get_logger
from .config import RedisConfig
from .metrics import CacheMetrics

logger = get_logger(__name__)

class RedisCache:
    """Gerenciador de cache usando Redis."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa a conexão com Redis.
        
        Args:
            config (Dict, opcional): Configurações do Redis
        """
        # Configuração
        self.config = RedisConfig.from_env() if config is None else RedisConfig(**config)
        
        try:
            # Conexão
            self.client = redis.from_url(
                self.config.get_url(),
                socket_timeout=self.config.socket_timeout,
                retry_on_timeout=self.config.retry_on_timeout,
                max_connections=self.config.max_connections,
                encoding=self.config.encoding
            )
            
            # Métricas
            self.metrics = CacheMetrics(self.client)
            
            logger.info("Conexão com Redis estabelecida com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao conectar ao Redis: {str(e)}")
            raise
            
    def _generate_key(self, collector: str, symbol: str, data_type: str, interval: str = None) -> str:
        """
        Gera uma chave única para o cache.
        
        Args:
            collector (str): Nome do coletor (ex: 'alpha_vantage', 'yfinance')
            symbol (str): Símbolo do ativo
            data_type (str): Tipo de dados ('daily' ou 'intraday')
            interval (str, opcional): Intervalo para dados intraday
            
        Returns:
            str: Chave única para o cache
        """
        key_parts = [collector, symbol, data_type]
        if interval:
            key_parts.append(interval)
        return ':'.join(key_parts)
        
    def _serialize_dataframe(self, df: pd.DataFrame) -> str:
        """
        Serializa um DataFrame para armazenamento.
        
        Args:
            df (pd.DataFrame): DataFrame para serializar
            
        Returns:
            str: DataFrame serializado
        """
        return df.to_json(date_format='iso')
        
    def _deserialize_dataframe(self, data: str) -> pd.DataFrame:
        """
        Deserializa dados para DataFrame.
        
        Args:
            data (str): Dados serializados
            
        Returns:
            pd.DataFrame: DataFrame reconstruído
        """
        return pd.read_json(data)
        
    def get(
        self,
        collector: str,
        symbol: str,
        data_type: str,
        interval: str = None
    ) -> Optional[pd.DataFrame]:
        """
        Obtém dados do cache.
        
        Args:
            collector (str): Nome do coletor
            symbol (str): Símbolo do ativo
            data_type (str): Tipo de dados
            interval (str, opcional): Intervalo para dados intraday
            
        Returns:
            Optional[pd.DataFrame]: DataFrame se encontrado, None caso contrário
        """
        try:
            key = self._generate_key(collector, symbol, data_type, interval)
            data = self.client.get(key)
            
            if data:
                logger.info(f"Cache hit para {key}")
                self.metrics.record_hit()
                return self._deserialize_dataframe(data)
            
            logger.info(f"Cache miss para {key}")
            self.metrics.record_miss()
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter dados do cache: {str(e)}")
            return None
            
    def set(
        self,
        collector: str,
        symbol: str,
        data_type: str,
        data: pd.DataFrame,
        interval: str = None,
        expire_seconds: int = 3600  # 1 hora por padrão
    ) -> bool:
        """
        Armazena dados no cache.
        
        Args:
            collector (str): Nome do coletor
            symbol (str): Símbolo do ativo
            data_type (str): Tipo de dados
            data (pd.DataFrame): Dados para armazenar
            interval (str, opcional): Intervalo para dados intraday
            expire_seconds (int): Tempo de expiração em segundos
            
        Returns:
            bool: True se sucesso, False caso contrário
        """
        try:
            key = self._generate_key(collector, symbol, data_type, interval)
            serialized_data = self._serialize_dataframe(data)
            
            self.client.setex(
                key,
                expire_seconds,
                serialized_data
            )
            
            logger.info(f"Dados armazenados em cache para {key}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao armazenar dados no cache: {str(e)}")
            return False
            
    def delete(
        self,
        collector: str,
        symbol: str,
        data_type: str,
        interval: str = None
    ) -> bool:
        """
        Remove dados do cache.
        
        Args:
            collector (str): Nome do coletor
            symbol (str): Símbolo do ativo
            data_type (str): Tipo de dados
            interval (str, opcional): Intervalo para dados intraday
            
        Returns:
            bool: True se sucesso, False caso contrário
        """
        try:
            key = self._generate_key(collector, symbol, data_type, interval)
            self.client.delete(key)
            logger.info(f"Dados removidos do cache para {key}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover dados do cache: {str(e)}")
            return False
            
    def clear_all(self) -> bool:
        """
        Limpa todo o cache.
        
        Returns:
            bool: True se sucesso, False caso contrário
        """
        try:
            self.client.flushall()
            self.metrics.reset_metrics()
            logger.info("Cache limpo completamente")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {str(e)}")
            return False
            
    def get_metrics(self) -> Dict:
        """
        Obtém métricas do cache.
        
        Returns:
            Dict: Métricas completas
        """
        stats = self.metrics.get_stats()
        memory = self.metrics.get_memory_usage()
        keys = self.metrics.get_key_stats()
        
        return {
            'stats': stats,
            'memory': memory,
            'keys': keys
        }
        
    def health_check(self) -> Dict:
        """
        Verifica saúde do cache.
        
        Returns:
            Dict: Status de saúde
        """
        try:
            # Ping
            self.client.ping()
            
            # Métricas básicas
            metrics = self.get_metrics()
            
            # Info do servidor
            info = self.client.info()
            
            return {
                'status': 'healthy',
                'uptime_seconds': info['uptime_in_seconds'],
                'connected_clients': info['connected_clients'],
                'used_memory': info['used_memory_human'],
                'hit_rate': metrics['stats']['hit_rate'],
                'total_keys': metrics['keys']['total_keys']
            }
            
        except Exception as e:
            logger.error(f"Erro na verificação de saúde: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            } 