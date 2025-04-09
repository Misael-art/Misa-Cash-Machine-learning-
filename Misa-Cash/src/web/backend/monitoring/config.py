from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Any, List
import time

# Métricas de Requisições
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total de requisições HTTP',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Latência das requisições HTTP',
    ['method', 'endpoint']
)

# Métricas de Negócio
TRANSACTION_COUNT = Counter(
    'transactions_total',
    'Total de transações',
    ['type', 'status']
)

TRANSACTION_AMOUNT = Histogram(
    'transaction_amount',
    'Valor das transações',
    ['type']
)

# Métricas de Sistema
MEMORY_USAGE = Gauge(
    'memory_usage_bytes',
    'Uso de memória em bytes'
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'Uso de CPU em percentual'
)

# Métricas de Cache
CACHE_HITS = Counter(
    'cache_hits_total',
    'Total de hits no cache',
    ['cache_type']
)

CACHE_MISSES = Counter(
    'cache_misses_total',
    'Total de misses no cache',
    ['cache_type']
)

# Métricas de Banco de Dados
DB_CONNECTIONS = Gauge(
    'db_connections',
    'Número de conexões com o banco de dados'
)

DB_QUERY_DURATION = Histogram(
    'db_query_duration_seconds',
    'Duração das queries do banco de dados',
    ['query_type']
)

# Alertas
ALERT_THRESHOLDS = {
    'request_latency': 1.0,  # segundos
    'error_rate': 0.05,      # 5%
    'memory_usage': 0.9,     # 90%
    'cpu_usage': 0.8,        # 80%
    'db_connections': 100,   # conexões
}

def track_request_latency(func):
    """Decorator para medir latência de requisições"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            status = 'success'
            return result
        except Exception as e:
            status = 'error'
            raise e
        finally:
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(
                method=kwargs.get('method', 'unknown'),
                endpoint=kwargs.get('endpoint', 'unknown')
            ).observe(duration)
            REQUEST_COUNT.labels(
                method=kwargs.get('method', 'unknown'),
                endpoint=kwargs.get('endpoint', 'unknown'),
                status=status
            ).inc()
    return wrapper

def check_alerts(metrics: Dict[str, Any]) -> List[str]:
    """Verifica se alguma métrica ultrapassou os limites"""
    alerts = []
    
    if metrics.get('request_latency', 0) > ALERT_THRESHOLDS['request_latency']:
        alerts.append(f"Latência alta: {metrics['request_latency']}s")
    
    error_rate = metrics.get('error_count', 0) / metrics.get('request_count', 1)
    if error_rate > ALERT_THRESHOLDS['error_rate']:
        alerts.append(f"Taxa de erro alta: {error_rate:.2%}")
    
    if metrics.get('memory_usage', 0) > ALERT_THRESHOLDS['memory_usage']:
        alerts.append(f"Uso de memória alto: {metrics['memory_usage']:.2%}")
    
    if metrics.get('cpu_usage', 0) > ALERT_THRESHOLDS['cpu_usage']:
        alerts.append(f"Uso de CPU alto: {metrics['cpu_usage']:.2%}")
    
    if metrics.get('db_connections', 0) > ALERT_THRESHOLDS['db_connections']:
        alerts.append(f"Muitas conexões com o banco: {metrics['db_connections']}")
    
    return alerts 