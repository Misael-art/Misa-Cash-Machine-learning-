import functools
from typing import Callable, Optional
import pandas as pd
from .redis_cache import RedisCache

def cache_data(
    data_type: str,
    expire_seconds: int = 3600,
    cache_instance: Optional[RedisCache] = None
):
    """
    Decorador para cache de dados financeiros.
    
    Args:
        data_type (str): Tipo de dados ('daily' ou 'intraday')
        expire_seconds (int): Tempo de expiração em segundos
        cache_instance (RedisCache, opcional): Instância do cache
        
    Returns:
        Callable: Função decorada
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Obter ou criar instância do cache
            cache = cache_instance or RedisCache()
            
            # Extrair parâmetros relevantes
            symbol = args[0] if args else kwargs.get('symbol')
            interval = kwargs.get('interval') if data_type == 'intraday' else None
            
            # Obter nome do coletor da classe
            collector_name = self.__class__.__name__.lower()
            
            # Tentar obter do cache
            cached_data = cache.get(
                collector=collector_name,
                symbol=symbol,
                data_type=data_type,
                interval=interval
            )
            
            if cached_data is not None:
                return cached_data
                
            # Se não estiver em cache, buscar dados
            data = func(self, *args, **kwargs)
            
            # Armazenar em cache se dados foram obtidos
            if isinstance(data, pd.DataFrame) and not data.empty:
                cache.set(
                    collector=collector_name,
                    symbol=symbol,
                    data_type=data_type,
                    data=data,
                    interval=interval,
                    expire_seconds=expire_seconds
                )
                
            return data
            
        return wrapper
    return decorator 