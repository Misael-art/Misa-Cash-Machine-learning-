#!/usr/bin/env python3
import os
import sys
import psycopg2
import redis
import requests
import logging
import psutil
from typing import Dict, List, Any
from datetime import datetime, timedelta

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PerformanceChecker:
    def __init__(self):
        self.db_name = os.getenv('DB_NAME', 'misacash')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_password = os.getenv('DB_PASSWORD', '')
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_password = os.getenv('REDIS_PASSWORD', '')
        self.api_url = os.getenv('API_URL', 'http://localhost:8000')
        
    def check_system_resources(self) -> Dict[str, Any]:
        """Verifica recursos do sistema"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available / (1024 * 1024 * 1024),  # GB
                'disk_usage': disk.percent,
                'disk_available': disk.free / (1024 * 1024 * 1024)  # GB
            }
        except Exception as e:
            logger.error(f"Erro ao verificar recursos do sistema: {str(e)}")
            return {}
    
    def check_database_performance(self) -> Dict[str, Any]:
        """Verifica performance do banco de dados"""
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                host=self.db_host,
                password=self.db_password
            )
            
            with conn.cursor() as cur:
                # Verificar queries lentas
                cur.execute("""
                    SELECT query, calls, total_time/calls as avg_time,
                           rows/calls as avg_rows
                    FROM pg_stat_statements
                    WHERE total_time/calls > 100  -- mais de 100ms
                    ORDER BY total_time/calls DESC
                    LIMIT 10
                """)
                slow_queries = cur.fetchall()
                
                # Verificar índices não utilizados
                cur.execute("""
                    SELECT schemaname, tablename, indexname, idx_scan
                    FROM pg_stat_user_indexes
                    WHERE idx_scan = 0
                    AND idx_isunique IS FALSE
                """)
                unused_indexes = cur.fetchall()
                
                # Verificar estatísticas de cache
                cur.execute("""
                    SELECT sum(heap_blks_read) as heap_read,
                           sum(heap_blks_hit) as heap_hit,
                           sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
                    FROM pg_statio_user_tables
                """)
                cache_stats = cur.fetchone()
                
                return {
                    'slow_queries': [
                        {
                            'query': q[0],
                            'calls': q[1],
                            'avg_time': q[2],
                            'avg_rows': q[3]
                        } for q in slow_queries
                    ],
                    'unused_indexes': [
                        {
                            'schema': i[0],
                            'table': i[1],
                            'index': i[2]
                        } for i in unused_indexes
                    ],
                    'cache_hit_ratio': cache_stats[2] if cache_stats else 0
                }
                
        except Exception as e:
            logger.error(f"Erro ao verificar performance do banco: {str(e)}")
            return {}
        finally:
            if conn:
                conn.close()
    
    def check_cache_performance(self) -> Dict[str, Any]:
        """Verifica performance do cache"""
        try:
            r = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password
            )
            
            info = r.info()
            return {
                'connected_clients': info.get('connected_clients', 0),
                'used_memory_human': info.get('used_memory_human', '0B'),
                'hit_rate': info.get('keyspace_hits', 0) / (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 1)),
                'evicted_keys': info.get('evicted_keys', 0),
                'expired_keys': info.get('expired_keys', 0),
                'total_commands_processed': info.get('total_commands_processed', 0)
            }
            
        except Exception as e:
            logger.error(f"Erro ao verificar performance do cache: {str(e)}")
            return {}
    
    def check_api_performance(self) -> Dict[str, Any]:
        """Verifica performance da API"""
        endpoints = [
            '/api/health',
            '/api/users',
            '/api/transactions',
            '/api/reports/summary'
        ]
        
        results = {}
        for endpoint in endpoints:
            try:
                start_time = datetime.now()
                response = requests.get(f"{self.api_url}{endpoint}")
                duration = (datetime.now() - start_time).total_seconds()
                
                results[endpoint] = {
                    'status_code': response.status_code,
                    'response_time': duration,
                    'success': response.status_code == 200
                }
                
            except Exception as e:
                logger.error(f"Erro ao verificar endpoint {endpoint}: {str(e)}")
                results[endpoint] = {
                    'status_code': 0,
                    'response_time': 0,
                    'success': False,
                    'error': str(e)
                }
        
        return results
    
    def analyze_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analisa os resultados e gera recomendações"""
        recommendations = []
        
        # Análise de recursos do sistema
        if results.get('system', {}).get('cpu_usage', 0) > 80:
            recommendations.append({
                'type': 'system',
                'severity': 'high',
                'message': 'CPU usage is too high. Consider scaling up or optimizing resource usage.'
            })
            
        if results.get('system', {}).get('memory_usage', 0) > 85:
            recommendations.append({
                'type': 'system',
                'severity': 'high',
                'message': 'Memory usage is too high. Consider increasing memory or optimizing memory usage.'
            })
        
        # Análise do banco de dados
        if results.get('database', {}).get('cache_hit_ratio', 1) < 0.9:
            recommendations.append({
                'type': 'database',
                'severity': 'medium',
                'message': 'Database cache hit ratio is low. Consider increasing shared_buffers.'
            })
            
        slow_queries = results.get('database', {}).get('slow_queries', [])
        if slow_queries:
            recommendations.append({
                'type': 'database',
                'severity': 'medium',
                'message': f'Found {len(slow_queries)} slow queries. Consider optimizing or adding indexes.'
            })
        
        # Análise do cache
        cache_hit_rate = results.get('cache', {}).get('hit_rate', 1)
        if cache_hit_rate < 0.8:
            recommendations.append({
                'type': 'cache',
                'severity': 'medium',
                'message': 'Cache hit rate is low. Review cache strategy and TTL settings.'
            })
        
        # Análise da API
        api_results = results.get('api', {})
        slow_endpoints = [
            endpoint for endpoint, data in api_results.items()
            if data.get('response_time', 0) > 1  # mais de 1 segundo
        ]
        if slow_endpoints:
            recommendations.append({
                'type': 'api',
                'severity': 'high',
                'message': f'Found {len(slow_endpoints)} slow endpoints. Review and optimize.'
            })
        
        return recommendations
    
    def run(self) -> bool:
        """Executa todas as verificações de performance"""
        try:
            results = {
                'system': self.check_system_resources(),
                'database': self.check_database_performance(),
                'cache': self.check_cache_performance(),
                'api': self.check_api_performance()
            }
            
            # Analisar resultados
            recommendations = self.analyze_results(results)
            
            # Registrar resultados
            logger.info("=== Relatório de Performance ===")
            
            logger.info("\nRecursos do Sistema:")
            for key, value in results['system'].items():
                logger.info(f"{key}: {value}")
            
            logger.info("\nPerformance do Banco de Dados:")
            for key, value in results['database'].items():
                logger.info(f"{key}: {value}")
            
            logger.info("\nPerformance do Cache:")
            for key, value in results['cache'].items():
                logger.info(f"{key}: {value}")
            
            logger.info("\nPerformance da API:")
            for endpoint, data in results['api'].items():
                logger.info(f"{endpoint}: {data}")
            
            if recommendations:
                logger.warning("\nRecomendações:")
                for rec in recommendations:
                    logger.warning(f"[{rec['severity']}] {rec['type']}: {rec['message']}")
            else:
                logger.info("\nNenhuma recomendação necessária.")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro durante a verificação de performance: {str(e)}")
            return False

if __name__ == '__main__':
    checker = PerformanceChecker()
    success = checker.run()
    sys.exit(0 if success else 1) 