"""
Módulo de Machine Learning para o projeto Misa-Cash.

Este módulo contém implementações de algoritmos de aprendizado de máquina
para análise financeira, previsão de gastos, detecção de anomalias e
categorização automática de transações.

Submódulos:
- api: Interface para integração com o backend
- config: Configurações dos modelos
- data: Processamento e preparação de dados
- models: Implementação dos modelos preditivos
- utils: Ferramentas de visualização e análise

Para usar este módulo, importe-o da seguinte forma:
```python
from src.ml import ExpensePredictor
from src.ml.utils import visualization

# Exemplo de uso básico
predictor = ExpensePredictor()
predictor.train(data)
forecast = predictor.predict(future_months=3)
```
"""

# Facilita o acesso direto a componentes importantes
from src.ml.models.expense_predictor import ExpensePredictor
from src.ml.models.anomaly_detector import AnomalyDetector
from src.ml.models.transaction_categorizer import TransactionCategorizer

__all__ = ['ExpensePredictor', 'AnomalyDetector', 'TransactionCategorizer'] 