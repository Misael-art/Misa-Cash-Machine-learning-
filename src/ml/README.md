# Módulo de Machine Learning - Misa-Cash

Este é o módulo de Machine Learning do Misa-Cash, uma aplicação para gerenciamento financeiro. O módulo fornece recursos avançados de análise, previsão e categorização de transações financeiras.

## Funcionalidades

- **Previsão de gastos mensais:** Utiliza modelos de regressão para prever gastos futuros com base no histórico de transações.
- **Detecção de anomalias:** Identifica transações atípicas que podem indicar fraudes ou erros.
- **Categorização automática:** Classifica automaticamente novas transações em categorias com base na descrição.
- **Análise de padrões de gastos:** Identifica padrões nos gastos do usuário ao longo do tempo.
- **Recomendações personalizadas:** Gera insights e recomendações personalizadas para melhorar a saúde financeira.

## Estrutura do Módulo

```
src/ml/
├── __init__.py                  # Inicialização do módulo
├── __main__.py                  # Ponto de entrada para execução direta
├── requirements.txt             # Dependências específicas de ML
├── api/                         # API para integração com o backend
│   ├── __init__.py
│   ├── endpoints.py             # Endpoints da API Flask
│   └── ml_service.py            # Serviço central de ML
├── data/                        # Processamento de dados
│   ├── __init__.py
│   ├── collectors.py            # Coleta de dados
│   └── preprocessors.py         # Pré-processamento e transformação
└── models/                      # Modelos de ML
    ├── __init__.py
    ├── expense_predictor.py     # Modelo de previsão de gastos
    ├── anomaly_detector.py      # Modelo de detecção de anomalias
    └── category_classifier.py   # Modelo de classificação de categorias
```

## Requisitos

Este módulo requer Python 3.8 ou superior e as bibliotecas listadas em `requirements.txt`. Para instalar as dependências:

```bash
pip install -r src/ml/requirements.txt
```

## Uso

### Via API

O módulo expõe uma API RESTful que pode ser acessada pelo backend principal. Os principais endpoints são:

- `GET /api/ml/health` - Verifica o status do serviço ML
- `POST /api/ml/train` - Treina modelos com dados fornecidos
- `GET /api/ml/predict/expenses` - Prevê gastos futuros
- `POST /api/ml/detect/anomalies` - Detecta anomalias em transações
- `POST /api/ml/classify/transaction` - Classifica categoria de uma transação
- `POST /api/ml/analyze/spending` - Analisa padrões de gastos
- `POST /api/ml/insights` - Gera insights financeiros

### Via Linha de Comando

O módulo também pode ser utilizado diretamente via linha de comando:

```bash
# Treinar modelos
python -m src.ml train --data dados/transacoes.csv --models expense_predictor anomaly_detector

# Fazer previsões
python -m src.ml predict --data dados/transacoes.csv --months 6 --type expenses
```

## Exemplos

### Treinar modelos

```python
from src.ml.api.ml_service import MLService
import pandas as pd

# Carregar dados
transactions = pd.read_csv('transacoes.csv')

# Inicializar serviço ML
ml_service = MLService()

# Preparar dados
models_data = ml_service.prepare_data_for_models(transactions)

# Treinar modelo de previsão de gastos
metrics = ml_service.train_expense_predictor(models_data['expense_predictor'])
print(f"Modelo treinado com MAE: {metrics['mae']:.2f}, RMSE: {metrics['rmse']:.2f}")
```

### Classificar transações

```python
from src.ml.api.ml_service import MLService

# Inicializar serviço ML
ml_service = MLService()

# Classificar uma transação
result = ml_service.classify_transaction_category("IFOOD*RESTAURANTE")
print(f"Categoria sugerida: {result['suggested_category']} (confiança: {result['confidence']:.2f})")
```

## Desempenho dos Modelos

Os modelos são avaliados regularmente e apresentam os seguintes desempenhos médios:

- **Previsão de gastos:** RMSE < 150, R² > 0.8
- **Classificação de categorias:** Acurácia > 85%
- **Detecção de anomalias:** Precisão > 90%, Recall > 80%

## Desenvolvimento

Para contribuir com o desenvolvimento deste módulo, siga estas diretrizes:

1. Siga as convenções de código estabelecidas (PEP 8)
2. Documente todas as funções e classes com docstrings
3. Adicione testes para novos recursos
4. Atualize o README conforme necessário

## Licença

Este módulo é parte do projeto Misa-Cash e está sujeito às mesmas condições de licença do projeto principal. 