#!/bin/bash

echo "Iniciando setup do ambiente ML Finance Platform..."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker não encontrado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose não encontrado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Criar diretórios necessários
echo "Criando estrutura de diretórios..."
mkdir -p src/data/cache
mkdir -p src/data/collectors
mkdir -p src/data/examples
mkdir -p logs

# Iniciar serviços Docker
echo "Iniciando serviços Docker..."
docker-compose down # Garantir que não há containers antigos rodando
docker-compose up -d

# Verificar se os serviços estão rodando
echo "Verificando status dos serviços..."
docker-compose ps

# Aguardar Redis ficar disponível
echo "Aguardando Redis ficar disponível..."
max_attempts=30
attempt=1
while ! docker-compose exec redis redis-cli ping &>/dev/null; do
    if [ $attempt -gt $max_attempts ]; then
        echo "Erro: Redis não ficou disponível após $max_attempts tentativas"
        exit 1
    fi
    echo "Tentativa $attempt de $max_attempts..."
    sleep 1
    ((attempt++))
done

echo "Redis está disponível!"

# Verificar status do Redis Commander
echo "Verificando Redis Commander..."
if curl -s http://localhost:8081 &>/dev/null; then
    echo "Redis Commander está acessível em http://localhost:8081"
else
    echo "Aviso: Redis Commander pode não estar acessível"
fi

echo "Setup concluído com sucesso!"
echo "Para acessar o Redis Commander, abra: http://localhost:8081"
echo "Para verificar os logs: docker-compose logs"
echo "Para parar os serviços: docker-compose down" 