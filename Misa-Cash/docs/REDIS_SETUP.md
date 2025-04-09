# Configuração do Redis

Este documento descreve a configuração e uso do Redis no projeto ML Finance Platform.

## Visão Geral

O Redis é utilizado como sistema de cache para otimizar a recuperação de dados financeiros das APIs externas. A configuração inclui:

- Redis Server: Sistema principal de cache
- Redis Commander: Interface web para gerenciamento do Redis
- Persistência de dados através de volumes Docker
- Rede dedicada para comunicação entre serviços

## Pré-requisitos

- Docker
- Docker Compose

## Configuração

O arquivo `docker-compose.yml` na raiz do projeto contém toda a configuração necessária:

```yaml
version: '3.8'
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
```

### Portas

- Redis Server: 6379
- Redis Commander: 8081

## Uso

### Iniciar os Serviços

```bash
docker-compose up -d
```

### Verificar Status

```bash
docker-compose ps
```

### Acessar Redis Commander

Abra no navegador:
```
http://localhost:8081
```

### Parar os Serviços

```bash
docker-compose down
```

## Monitoramento

### Logs do Redis

```bash
docker-compose logs redis
```

### Métricas do Redis

Acesse o Redis Commander para visualizar:
- Uso de memória
- Chaves armazenadas
- Estatísticas de hit/miss do cache
- Conexões ativas

## Backup e Persistência

Os dados são persistidos através do volume Docker `redis_data`. O Redis está configurado com AOF (Append Only File) para garantir durabilidade dos dados.

## Segurança

Por padrão, o Redis está configurado apenas para acesso local. Para produção, recomenda-se:

1. Configurar senha
2. Habilitar SSL/TLS
3. Restringir acesso por IP
4. Configurar políticas de firewall

## Troubleshooting

### Problemas Comuns

1. Redis não inicia:
   - Verificar se a porta 6379 está livre
   - Verificar logs com `docker-compose logs redis`

2. Problemas de conexão:
   - Confirmar que o serviço está rodando
   - Verificar configurações de rede
   - Testar conexão com `redis-cli`

### Comandos Úteis

```bash
# Testar conexão
redis-cli ping

# Limpar cache
redis-cli FLUSHALL

# Monitorar comandos
redis-cli MONITOR
```

## Integração com o Código

O Redis é integrado através do módulo de cache em `src/data/cache/redis_cache.py`. Exemplo de uso:

```python
from src.data.cache import RedisCache

# Inicializar cache
cache = RedisCache(host='localhost', port=6379)

# Usar decorador de cache
@cache_data(expiration=3600)
def get_stock_data(symbol):
    # ... código para buscar dados ...
```

## Métricas de Performance

Monitor as seguintes métricas para otimização:

- Hit rate do cache
- Latência das operações
- Uso de memória
- Número de conexões
- Comandos por segundo

## Manutenção

### Tarefas Regulares

1. Monitorar uso de memória
2. Verificar logs de erros
3. Atualizar versão do Redis
4. Backup dos dados
5. Limpeza de dados antigos

### Otimização

- Ajustar política de expiração
- Configurar limites de memória
- Otimizar estruturas de dados
- Monitorar padrões de acesso 