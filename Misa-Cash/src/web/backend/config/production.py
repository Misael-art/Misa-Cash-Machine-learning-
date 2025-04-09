import os
from typing import Dict, Any

# Configurações do Banco de Dados
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'misacash'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'pool_size': int(os.getenv('DB_POOL_SIZE', 20)),
    'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 10)),
    'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30)),
    'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 1800)),
}

# Configurações de Cache
CACHE_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': int(os.getenv('REDIS_DB', 0)),
    'password': os.getenv('REDIS_PASSWORD', ''),
    'ttl': int(os.getenv('CACHE_TTL', 3600)),
}

# Configurações de Segurança
SECURITY_CONFIG = {
    'secret_key': os.getenv('SECRET_KEY', ''),
    'algorithm': 'HS256',
    'access_token_expire_minutes': int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)),
    'refresh_token_expire_days': int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', 7)),
    'password_hash_algorithm': 'bcrypt',
    'cors_origins': os.getenv('CORS_ORIGINS', '').split(','),
}

# Configurações de Logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'json',
            'filename': '/var/log/misacash/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'level': 'INFO'
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO'
    }
}

# Configurações de Email
EMAIL_CONFIG = {
    'host': os.getenv('SMTP_HOST', ''),
    'port': int(os.getenv('SMTP_PORT', 587)),
    'username': os.getenv('SMTP_USERNAME', ''),
    'password': os.getenv('SMTP_PASSWORD', ''),
    'use_tls': True,
    'from_email': os.getenv('FROM_EMAIL', 'noreply@misacash.com'),
    'from_name': 'Misa Cash'
}

# Configurações de Monitoramento
MONITORING_CONFIG = {
    'prometheus_port': int(os.getenv('PROMETHEUS_PORT', 9090)),
    'grafana_port': int(os.getenv('GRAFANA_PORT', 3000)),
    'alert_manager_port': int(os.getenv('ALERT_MANAGER_PORT', 9093)),
}

# Configurações de Rate Limiting
RATE_LIMIT_CONFIG = {
    'default': '100/minute',
    'auth': '5/minute',
    'api': '1000/minute'
}

# Configurações de Backup
BACKUP_CONFIG = {
    'schedule': '0 0 * * *',  # Diário à meia-noite
    'retention_days': 30,
    'storage_path': '/var/backups/misacash',
    'compress': True
}

# Configurações de CDN
CDN_CONFIG = {
    'enabled': True,
    'domain': os.getenv('CDN_DOMAIN', ''),
    'api_key': os.getenv('CDN_API_KEY', ''),
    'api_secret': os.getenv('CDN_API_SECRET', '')
}

def get_config() -> Dict[str, Any]:
    """Retorna todas as configurações em um único dicionário"""
    return {
        'database': DATABASE_CONFIG,
        'cache': CACHE_CONFIG,
        'security': SECURITY_CONFIG,
        'logging': LOGGING_CONFIG,
        'email': EMAIL_CONFIG,
        'monitoring': MONITORING_CONFIG,
        'rate_limit': RATE_LIMIT_CONFIG,
        'backup': BACKUP_CONFIG,
        'cdn': CDN_CONFIG
    } 