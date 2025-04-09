from typing import Dict, Optional
from datetime import datetime
import json
from redis import Redis

class CacheMetrics:
    """Gerenciador de métricas do cache."""
    
    def __init__(self, redis_client: Redis):
        """
        Inicializa o gerenciador de métricas.
        
        Args:
            redis_client (Redis): Cliente Redis
        """
        self.client = redis_client
        self.metrics_key = "cache:metrics"
        
    def _get_metrics(self) -> Dict:
        """
        Obtém métricas atuais.
        
        Returns:
            Dict: Métricas do cache
        """
        metrics_data = self.client.get(self.metrics_key)
        if metrics_data:
            return json.loads(metrics_data)
        return {
            'hits': 0,
            'misses': 0,
            'total_requests': 0,
            'last_reset': datetime.now().isoformat()
        }
        
    def _save_metrics(self, metrics: Dict) -> None:
        """
        Salva métricas no Redis.
        
        Args:
            metrics (Dict): Métricas para salvar
        """
        self.client.set(self.metrics_key, json.dumps(metrics))
        
    def record_hit(self) -> None:
        """Registra um hit no cache."""
        metrics = self._get_metrics()
        metrics['hits'] += 1
        metrics['total_requests'] += 1
        self._save_metrics(metrics)
        
    def record_miss(self) -> None:
        """Registra um miss no cache."""
        metrics = self._get_metrics()
        metrics['misses'] += 1
        metrics['total_requests'] += 1
        self._save_metrics(metrics)
        
    def get_hit_rate(self) -> float:
        """
        Calcula taxa de hits.
        
        Returns:
            float: Taxa de hits (0-1)
        """
        metrics = self._get_metrics()
        total = metrics['total_requests']
        if total == 0:
            return 0.0
        return metrics['hits'] / total
        
    def get_stats(self) -> Dict:
        """
        Obtém estatísticas completas.
        
        Returns:
            Dict: Estatísticas do cache
        """
        metrics = self._get_metrics()
        hit_rate = self.get_hit_rate()
        
        return {
            **metrics,
            'hit_rate': hit_rate,
            'current_time': datetime.now().isoformat()
        }
        
    def reset_metrics(self) -> None:
        """Reseta todas as métricas."""
        self.client.delete(self.metrics_key)
        
    def get_memory_usage(self) -> Dict:
        """
        Obtém informações de uso de memória.
        
        Returns:
            Dict: Estatísticas de memória
        """
        info = self.client.info(section='memory')
        return {
            'used_memory': info['used_memory'],
            'used_memory_peak': info['used_memory_peak'],
            'used_memory_lua': info['used_memory_lua'],
            'mem_fragmentation_ratio': info['mem_fragmentation_ratio']
        }
        
    def get_key_stats(self) -> Dict:
        """
        Obtém estatísticas sobre chaves.
        
        Returns:
            Dict: Estatísticas de chaves
        """
        stats = {
            'total_keys': 0,
            'expires': 0,
            'avg_ttl': 0
        }
        
        # Total de chaves
        stats['total_keys'] = len(self.client.keys('*'))
        
        # Chaves com expiração
        for key in self.client.scan_iter("*"):
            ttl = self.client.ttl(key)
            if ttl > 0:
                stats['expires'] += 1
                stats['avg_ttl'] += ttl
                
        if stats['expires'] > 0:
            stats['avg_ttl'] /= stats['expires']
            
        return stats 