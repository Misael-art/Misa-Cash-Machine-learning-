from datetime import datetime, timedelta
import time
from typing import Dict
import pandas as pd

from ..cache import RedisCache
from ..collectors import AlphaVantageCollector, YFinanceCollector
from ..utils.logger import get_logger

logger = get_logger(__name__)

def print_metrics(metrics: Dict) -> None:
    """
    Imprime métricas do cache de forma formatada.
    
    Args:
        metrics (Dict): Métricas para imprimir
    """
    print("\n=== Métricas do Cache ===")
    
    # Estatísticas gerais
    stats = metrics['stats']
    print("\nEstatísticas:")
    print(f"- Total de requisições: {stats['total_requests']}")
    print(f"- Hits: {stats['hits']}")
    print(f"- Misses: {stats['misses']}")
    print(f"- Taxa de hits: {stats['hit_rate']:.2%}")
    
    # Memória
    memory = metrics['memory']
    print("\nUso de Memória:")
    print(f"- Usado: {memory['used_memory']} bytes")
    print(f"- Pico: {memory['used_memory_peak']} bytes")
    print(f"- Fragmentação: {memory['mem_fragmentation_ratio']:.2f}")
    
    # Chaves
    keys = metrics['keys']
    print("\nEstatísticas de Chaves:")
    print(f"- Total: {keys['total_keys']}")
    print(f"- Com expiração: {keys['expires']}")
    if keys['expires'] > 0:
        print(f"- TTL médio: {keys['avg_ttl']:.0f} segundos")
        
def test_cache_operations():
    """Testa operações básicas do cache."""
    logger.info("Iniciando teste de operações do cache")
    
    # Inicializar cache com configuração personalizada
    cache_config = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'socket_timeout': 5
    }
    
    cache = RedisCache(config=cache_config)
    
    # Verificar saúde
    health = cache.health_check()
    logger.info(f"Status do cache: {health['status']}")
    
    # Limpar cache anterior
    cache.clear_all()
    
    # Criar dados de exemplo
    data = pd.DataFrame({
        'open': [100, 101, 102],
        'high': [105, 106, 107],
        'low': [98, 99, 100],
        'close': [103, 104, 105],
        'volume': [1000, 1100, 1200]
    })
    
    # Testar operações básicas
    logger.info("Testando operações básicas")
    
    # Set
    cache.set('test', 'AAPL', 'daily', data)
    
    # Get (hit)
    result = cache.get('test', 'AAPL', 'daily')
    assert not result.empty, "Dados não encontrados no cache"
    
    # Get (miss)
    result = cache.get('test', 'GOOGL', 'daily')
    assert result is None, "Dados encontrados quando não deveriam existir"
    
    # Delete
    cache.delete('test', 'AAPL', 'daily')
    result = cache.get('test', 'AAPL', 'daily')
    assert result is None, "Dados ainda existem após delete"
    
    logger.info("Operações básicas concluídas com sucesso")
    
def test_collectors_with_cache():
    """Testa coletores com cache."""
    logger.info("Iniciando teste dos coletores com cache")
    
    # Configurar coletores
    av_config = {'api_key': 'sua_chave_aqui'}  # Substitua pela sua chave
    av_collector = AlphaVantageCollector(config=av_config)
    
    yf_collector = YFinanceCollector()
    
    # Datas para teste
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Testar Alpha Vantage
    logger.info("Testando Alpha Vantage com cache")
    
    # Primeira chamada (miss)
    data1 = av_collector.get_daily_data('AAPL', start_date, end_date)
    time.sleep(1)  # Pequena pausa para evitar rate limit
    
    # Segunda chamada (hit)
    data2 = av_collector.get_daily_data('AAPL', start_date, end_date)
    
    # Testar Yahoo Finance
    logger.info("Testando Yahoo Finance com cache")
    
    # Primeira chamada (miss)
    data3 = yf_collector.get_daily_data('MSFT', start_date, end_date)
    
    # Segunda chamada (hit)
    data4 = yf_collector.get_daily_data('MSFT', start_date, end_date)
    
    # Verificar métricas
    cache = RedisCache()
    metrics = cache.get_metrics()
    print_metrics(metrics)
    
    logger.info("Testes dos coletores concluídos com sucesso")
    
def main():
    """Função principal."""
    try:
        # Testar operações básicas
        test_cache_operations()
        
        # Testar coletores
        test_collectors_with_cache()
        
    except Exception as e:
        logger.error(f"Erro durante os testes: {str(e)}")
        raise
        
if __name__ == "__main__":
    main() 