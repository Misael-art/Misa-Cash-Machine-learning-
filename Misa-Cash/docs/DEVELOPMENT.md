# Guia de Desenvolvimento - ML Finance Platform

## 1. Setup do Ambiente

### 1.1 Requisitos
```bash
# Python 3.9+
python --version

# Docker
docker --version

# Git
git --version
```

### 1.2 Configuração Inicial
```bash
# Clonar repositório
git clone https://github.com/your-org/ml-finance-platform.git
cd ml-finance-platform

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 1.3 Variáveis de Ambiente
```bash
# .env
PYTHONPATH=./src
DATABASE_URL=postgresql://user:pass@localhost:5432/mlfinance
REDIS_URL=redis://localhost:6379
API_KEY_YAHOO_FINANCE=your_key_here
API_KEY_ALPHA_VANTAGE=your_key_here
```

## 2. Estrutura do Projeto

### 2.1 Organização de Diretórios
```
ml_finance_platform/
├── data/
│   ├── raw/              # Dados brutos
│   └── processed/        # Dados processados
├── notebooks/            # Jupyter notebooks
├── src/
│   ├── data/            # Processamento de dados
│   ├── features/        # Feature engineering
│   ├── models/          # Modelos ML
│   ├── api/             # API endpoints
│   └── utils/           # Utilitários
├── tests/               # Testes
├── configs/             # Configurações
└── docs/                # Documentação
```

## 3. Padrões de Código

### 3.1 Style Guide
```python
# Exemplo de classe
class DataProcessor:
    """
    Processa dados financeiros.
    
    Attributes:
        source (str): Fonte dos dados
        frequency (str): Frequência dos dados
    """
    
    def __init__(self, source: str, frequency: str = "1d"):
        self.source = source
        self.frequency = frequency
    
    def process_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Processa os dados brutos.
        
        Args:
            data (pd.DataFrame): Dados para processar
            
        Returns:
            pd.DataFrame: Dados processados
        """
        # Implementação
        pass
```

### 3.2 Convenções de Nomenclatura
```python
# Variáveis e funções
snake_case_variable = 1
def process_market_data():
    pass

# Classes
class MarketDataProcessor:
    pass

# Constantes
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
```

## 4. Desenvolvimento

### 4.1 Fluxo de Trabalho Git
```bash
# Criar branch
git checkout -b feature/nova-funcionalidade

# Commit
git add .
git commit -m "feat: adiciona processamento de dados"

# Push
git push origin feature/nova-funcionalidade
```

### 4.2 Testes
```python
# tests/test_data_processor.py
import pytest
from src.data import DataProcessor

def test_data_processor():
    processor = DataProcessor("yahoo")
    data = processor.process_data(sample_data)
    assert data.shape[0] > 0
    assert "close" in data.columns
```

### 4.3 Logging
```python
# src/utils/logger.py
import logging

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

## 5. APIs e Integrações

### 5.1 API Endpoints
```python
# src/api/routes.py
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/api/v1/prediction/{symbol}")
async def get_prediction(symbol: str):
    try:
        prediction = predict_price(symbol)
        return {"symbol": symbol, "prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 5.2 Documentação da API
```yaml
# OpenAPI spec
paths:
  /api/v1/prediction/{symbol}:
    get:
      summary: Obtém previsão para um ativo
      parameters:
        - name: symbol
          in: path
          required: true
          schema:
            type: string
      responses:
        200:
          description: Previsão bem-sucedida
```

## 6. Deploy

### 6.1 Docker
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 6.2 Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mlfinance
    depends_on:
      - db
      - redis

  db:
    image: timescale/timescaledb:latest-pg12
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mlfinance

  redis:
    image: redis:alpine
```

## 7. Monitoramento e Debug

### 7.1 Métricas
```python
# src/utils/metrics.py
from prometheus_client import Counter, Histogram

PREDICTION_REQUESTS = Counter(
    'prediction_requests_total',
    'Total number of prediction requests'
)

PREDICTION_LATENCY = Histogram(
    'prediction_latency_seconds',
    'Time spent processing prediction'
)
```

### 7.2 Logging Avançado
```python
# src/utils/logging.py
import structlog

logger = structlog.get_logger()

def log_prediction(symbol: str, prediction: float, duration: float):
    logger.info(
        "prediction_made",
        symbol=symbol,
        prediction=prediction,
        duration=duration
    )
```

## 8. Melhores Práticas

### 8.1 Segurança
```python
# src/utils/security.py
from cryptography.fernet import Fernet

def encrypt_sensitive_data(data: str) -> str:
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()
```

### 8.2 Performance
```python
# src/utils/optimization.py
from functools import lru_cache

@lru_cache(maxsize=100)
def get_historical_data(symbol: str) -> pd.DataFrame:
    """Cached historical data retrieval"""
    return fetch_data(symbol)
```

## 9. Contribuição

### 9.1 Pull Request Template
```markdown
## Descrição
Descreva as mudanças propostas.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Checklist
- [ ] Testes adicionados
- [ ] Documentação atualizada
- [ ] Código segue style guide
```

### 9.2 Code Review
```markdown
## Critérios de Review
1. Código segue padrões
2. Testes adequados
3. Documentação clara
4. Performance adequada
5. Segurança considerada
```

## 10. Recursos Adicionais

### 10.1 Links Úteis
- [Documentação da API](docs/api.md)
- [Guia de Contribuição](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [FAQ](docs/faq.md)

### 10.2 Contatos
- Tech Lead: tech.lead@company.com
- ML Team: ml.team@company.com
- DevOps: devops@company.com 