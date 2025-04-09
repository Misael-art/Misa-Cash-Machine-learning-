from typing import List, Dict, Callable, Optional, Tuple, Union
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
from ..utils.logger import get_logger
from .metrics import PerformanceMetrics

logger = get_logger(__name__)

@dataclass
class ValidationResult:
    """Resultado da validação cruzada."""
    train_scores: List[Dict[str, float]]  # Scores de treino para cada fold
    test_scores: List[Dict[str, float]]   # Scores de teste para cada fold
    train_mean: Dict[str, float]          # Média dos scores de treino
    train_std: Dict[str, float]           # Desvio padrão dos scores de treino
    test_mean: Dict[str, float]           # Média dos scores de teste
    test_std: Dict[str, float]            # Desvio padrão dos scores de teste
    fold_dates: List[Tuple[datetime, datetime]]  # Datas de cada fold
    parameters: List[Dict]                 # Parâmetros usados em cada fold

class CrossValidator:
    """Sistema de validação cruzada para estratégias de trading."""
    
    def __init__(
        self,
        data: pd.DataFrame,
        strategy: Callable,
        performance_metrics: Optional[List[str]] = None,
        min_train_size: int = 252,  # 1 ano de dados
        test_size: int = 126,       # 6 meses de dados
        step_size: int = 21,        # 1 mês
        gap_size: int = 0           # Sem gap entre treino e teste
    ):
        """
        Inicializa o validador cruzado.
        
        Args:
            data (pd.DataFrame): DataFrame com dados históricos
            strategy (Callable): Função da estratégia
            performance_metrics (List[str]): Lista de métricas a calcular
            min_train_size (int): Tamanho mínimo do conjunto de treino
            test_size (int): Tamanho do conjunto de teste
            step_size (int): Tamanho do passo para walk-forward
            gap_size (int): Tamanho do gap entre treino e teste
        """
        self.data = data
        self.strategy = strategy
        self.performance_metrics = performance_metrics or ['sharpe_ratio', 'max_drawdown', 'total_return']
        self.min_train_size = min_train_size
        self.test_size = test_size
        self.step_size = step_size
        self.gap_size = gap_size
    
    def _calculate_metrics(
        self,
        returns: pd.Series,
        trades: List[Dict]
    ) -> Dict[str, float]:
        """
        Calcula métricas de performance.
        
        Args:
            returns (pd.Series): Série de retornos
            trades (List[Dict]): Lista de trades
            
        Returns:
            Dict[str, float]: Métricas calculadas
        """
        calculator = PerformanceMetrics(returns)
        all_metrics = calculator.calculate_all_metrics(trades=trades)
        
        selected_metrics = {}
        for metric_name in self.performance_metrics:
            for category in all_metrics.values():
                if hasattr(category, metric_name):
                    selected_metrics[metric_name] = getattr(category, metric_name)
                    break
        
        return selected_metrics
    
    def _split_data(
        self,
        start_idx: int,
        train_size: int
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Divide os dados em treino e teste.
        
        Args:
            start_idx (int): Índice inicial
            train_size (int): Tamanho do conjunto de treino
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Dados de treino e teste
        """
        train_end = start_idx + train_size
        test_start = train_end + self.gap_size
        test_end = test_start + self.test_size
        
        train_data = self.data.iloc[start_idx:train_end].copy()
        test_data = self.data.iloc[test_start:test_end].copy()
        
        return train_data, test_data
    
    def expanding_window_split(
        self,
        min_train_size: Optional[int] = None
    ) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Gera splits com janela de treino expansiva.
        
        Args:
            min_train_size (int): Tamanho mínimo do conjunto de treino
            
        Returns:
            List[Tuple[pd.DataFrame, pd.DataFrame]]: Lista de splits
        """
        min_train_size = min_train_size or self.min_train_size
        splits = []
        
        for train_end in range(min_train_size, len(self.data) - self.test_size, self.step_size):
            train_data = self.data.iloc[:train_end].copy()
            test_start = train_end + self.gap_size
            test_data = self.data.iloc[test_start:test_start + self.test_size].copy()
            splits.append((train_data, test_data))
        
        return splits
    
    def sliding_window_split(
        self,
        train_size: Optional[int] = None
    ) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Gera splits com janela deslizante de tamanho fixo.
        
        Args:
            train_size (int): Tamanho fixo do conjunto de treino
            
        Returns:
            List[Tuple[pd.DataFrame, pd.DataFrame]]: Lista de splits
        """
        train_size = train_size or self.min_train_size
        splits = []
        
        for start_idx in range(0, len(self.data) - train_size - self.test_size, self.step_size):
            train_data, test_data = self._split_data(start_idx, train_size)
            splits.append((train_data, test_data))
        
        return splits
    
    def monte_carlo_split(
        self,
        n_splits: int = 5,
        train_size: Optional[int] = None
    ) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Gera splits aleatórios para simulação Monte Carlo.
        
        Args:
            n_splits (int): Número de splits a gerar
            train_size (int): Tamanho do conjunto de treino
            
        Returns:
            List[Tuple[pd.DataFrame, pd.DataFrame]]: Lista de splits
        """
        train_size = train_size or self.min_train_size
        splits = []
        
        max_start = len(self.data) - train_size - self.test_size
        for _ in range(n_splits):
            start_idx = np.random.randint(0, max_start)
            train_data, test_data = self._split_data(start_idx, train_size)
            splits.append((train_data, test_data))
        
        return splits
    
    def _validate_split(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        parameters: Dict
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        Valida um split específico.
        
        Args:
            train_data (pd.DataFrame): Dados de treino
            test_data (pd.DataFrame): Dados de teste
            parameters (Dict): Parâmetros da estratégia
            
        Returns:
            Tuple[Dict[str, float], Dict[str, float]]: Métricas de treino e teste
        """
        # Aplicar estratégia nos dados de treino
        train_strategy = lambda x, state: self.strategy(x, state, **parameters)
        train_returns = pd.Series(0.0, index=train_data.index)
        train_trades = []
        state = {'positions': []}
        
        for i in range(len(train_data)):
            signals = train_strategy(train_data.iloc[:i+1], state.copy())
            if signals:
                # Simular execução dos sinais e atualizar retornos/trades
                pass
        
        # Aplicar estratégia nos dados de teste
        test_strategy = lambda x, state: self.strategy(x, state, **parameters)
        test_returns = pd.Series(0.0, index=test_data.index)
        test_trades = []
        state = {'positions': []}
        
        for i in range(len(test_data)):
            signals = test_strategy(test_data.iloc[:i+1], state.copy())
            if signals:
                # Simular execução dos sinais e atualizar retornos/trades
                pass
        
        # Calcular métricas
        train_metrics = self._calculate_metrics(train_returns, train_trades)
        test_metrics = self._calculate_metrics(test_returns, test_trades)
        
        return train_metrics, test_metrics
    
    def validate(
        self,
        method: str = 'expanding',
        parameters: Union[Dict, List[Dict]] = None,
        n_splits: int = 5,
        train_size: Optional[int] = None
    ) -> ValidationResult:
        """
        Executa validação cruzada.
        
        Args:
            method (str): Método de validação ('expanding', 'sliding', 'monte_carlo')
            parameters (Dict|List[Dict]): Parâmetros da estratégia
            n_splits (int): Número de splits para Monte Carlo
            train_size (int): Tamanho do conjunto de treino
            
        Returns:
            ValidationResult: Resultado da validação
        """
        if isinstance(parameters, dict):
            parameters = [parameters] * n_splits
        elif parameters is None:
            parameters = [{}] * n_splits
        
        # Gerar splits
        if method == 'expanding':
            splits = self.expanding_window_split(train_size)
        elif method == 'sliding':
            splits = self.sliding_window_split(train_size)
        elif method == 'monte_carlo':
            splits = self.monte_carlo_split(n_splits, train_size)
        else:
            raise ValueError(f"Método de validação inválido: {method}")
        
        # Validar cada split
        train_scores = []
        test_scores = []
        fold_dates = []
        
        for (train_data, test_data), params in zip(splits, parameters):
            train_metrics, test_metrics = self._validate_split(train_data, test_data, params)
            
            train_scores.append(train_metrics)
            test_scores.append(test_metrics)
            fold_dates.append((train_data.index[0], test_data.index[-1]))
        
        # Calcular estatísticas
        train_mean = {}
        train_std = {}
        test_mean = {}
        test_std = {}
        
        for metric in self.performance_metrics:
            train_values = [score[metric] for score in train_scores]
            test_values = [score[metric] for score in test_scores]
            
            train_mean[metric] = np.mean(train_values)
            train_std[metric] = np.std(train_values)
            test_mean[metric] = np.mean(test_values)
            test_std[metric] = np.std(test_values)
        
        return ValidationResult(
            train_scores=train_scores,
            test_scores=test_scores,
            train_mean=train_mean,
            train_std=train_std,
            test_mean=test_mean,
            test_std=test_std,
            fold_dates=fold_dates,
            parameters=parameters
        ) 