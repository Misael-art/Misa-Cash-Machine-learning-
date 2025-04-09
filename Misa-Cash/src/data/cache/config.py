from typing import Dict, Optional
from dataclasses import dataclass
import os

@dataclass
class RedisConfig:
    """Configuração do Redis."""
    
    host: str = 'localhost'
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    ssl: bool = False
    socket_timeout: int = 5
    retry_on_timeout: bool = True
    max_connections: int = 10
    encoding: str = 'utf-8'
    
    @classmethod
    def from_env(cls) -> 'RedisConfig':
        """
        Cria configuração a partir de variáveis de ambiente.
        
        Returns:
            RedisConfig: Configuração do Redis
        """
        return cls(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            password=os.getenv('REDIS_PASSWORD'),
            ssl=bool(os.getenv('REDIS_SSL', False)),
            socket_timeout=int(os.getenv('REDIS_SOCKET_TIMEOUT', 5)),
            retry_on_timeout=bool(os.getenv('REDIS_RETRY_ON_TIMEOUT', True)),
            max_connections=int(os.getenv('REDIS_MAX_CONNECTIONS', 10))
        )
        
    def to_dict(self) -> Dict:
        """
        Converte configuração para dicionário.
        
        Returns:
            Dict: Configuração em formato de dicionário
        """
        return {
            'host': self.host,
            'port': self.port,
            'db': self.db,
            'password': self.password,
            'ssl': self.ssl,
            'socket_timeout': self.socket_timeout,
            'retry_on_timeout': self.retry_on_timeout,
            'max_connections': self.max_connections,
            'encoding': self.encoding
        }
        
    def get_url(self) -> str:
        """
        Gera URL de conexão Redis.
        
        Returns:
            str: URL de conexão
        """
        auth = f":{self.password}@" if self.password else ""
        protocol = "rediss" if self.ssl else "redis"
        return f"{protocol}://{auth}{self.host}:{self.port}/{self.db}" 