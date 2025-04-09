from typing import Dict, List, Any, Callable, Optional, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass
from datetime import datetime, timedelta
import itertools
import logging
from ..utils.logger import get_logger
from ..backtesting import BacktestEngine, BacktestConfig
from ..data.indicators import IndicatorConfig

logger = get_logger(__name__)

@dataclass
class OptimizationConfig:
    """Configuração para otimização de estratégias."""
    
    # Parâmetros gerais
    metric: str = 'sharpe_ratio'  # Métrica a ser otimizada
    maximize: bool = True  # Se True, maximiza a métrica; se False, minimiza
    
    # Grid Search
    param_grid: Dict[str, List[Any]] = None  # Grid de parâmetros para busca
    
    # Otimização Genética
    population_size: int = 50  # Tamanho da população
    generations: int = 30  # Número de gerações
    mutation_rate: float = 0.1  # Taxa de mutação
    crossover_rate: float = 0.8  # Taxa de crossover
    
    # Walk Forward
    train_size: int = 252  # Tamanho do período de treino (dias)
    test_size: int = 126  # Tamanho do período de teste (dias)
    step_size: int = 21  # Tamanho do passo para walk forward (dias)

class StrategyOptimizer:
    """Otimizador de estratégias de trading."""
    
    def __init__(
        self,
        config: Optional[OptimizationConfig] = None,
        backtest_config: Optional[BacktestConfig] = None,
        indicator_config: Optional[IndicatorConfig] = None
    ):
        """
        Inicializa o otimizador.
        
        Args:
            config (OptimizationConfig): Configuração da otimização
            backtest_config (BacktestConfig): Configuração do backtesting
            indicator_config (IndicatorConfig): Configuração dos indicadores
        """
        self.config = config or OptimizationConfig()
        self.backtest_engine = BacktestEngine(backtest_config, indicator_config)
    
    def grid_search(
        self,
        data: pd.DataFrame,
        strategy_template: Callable,
        param_grid: Dict[str, List[Any]]
    ) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """
        Realiza grid search para encontrar os melhores parâmetros.
        
        Args:
            data (pd.DataFrame): Dados históricos
            strategy_template (Callable): Template da estratégia
            param_grid (Dict[str, List[Any]]): Grid de parâmetros
            
        Returns:
            Tuple[Dict[str, Any], Dict[str, float]]: Melhores parâmetros e resultados
        """
        best_params = None
        best_score = float('-inf') if self.config.maximize else float('inf')
        results = {}
        
        # Gerar todas as combinações de parâmetros
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        
        for values in itertools.product(*param_values):
            params = dict(zip(param_names, values))
            
            # Criar estratégia com parâmetros atuais
            strategy = lambda x, state: strategy_template(x, state, **params)
            
            # Executar backtesting
            backtest_results = self.backtest_engine.run(data, strategy)
            score = backtest_results[self.config.metric]
            
            # Atualizar melhor resultado
            if (self.config.maximize and score > best_score) or \
               (not self.config.maximize and score < best_score):
                best_score = score
                best_params = params.copy()
            
            results[str(params)] = score
            
            logger.info(f"Testando parâmetros: {params}")
            logger.info(f"Score: {score:.4f}")
        
        return best_params, results
    
    def genetic_optimize(
        self,
        data: pd.DataFrame,
        strategy_template: Callable,
        param_bounds: Dict[str, Tuple[float, float]]
    ) -> Tuple[Dict[str, Any], List[float]]:
        """
        Realiza otimização genética dos parâmetros.
        
        Args:
            data (pd.DataFrame): Dados históricos
            strategy_template (Callable): Template da estratégia
            param_bounds (Dict[str, Tuple[float, float]]): Limites dos parâmetros
            
        Returns:
            Tuple[Dict[str, Any], List[float]]: Melhores parâmetros e histórico
        """
        def create_individual():
            """Cria um indivíduo aleatório."""
            return {
                name: np.random.uniform(low, high)
                for name, (low, high) in param_bounds.items()
            }
        
        def fitness(individual):
            """Calcula o fitness de um indivíduo."""
            strategy = lambda x, state: strategy_template(x, state, **individual)
            results = self.backtest_engine.run(data, strategy)
            return results[self.config.metric]
        
        def crossover(parent1, parent2):
            """Realiza crossover entre dois indivíduos."""
            child = {}
            for param in param_bounds:
                if np.random.random() < self.config.crossover_rate:
                    child[param] = parent1[param]
                else:
                    child[param] = parent2[param]
            return child
        
        def mutate(individual):
            """Realiza mutação em um indivíduo."""
            for param, (low, high) in param_bounds.items():
                if np.random.random() < self.config.mutation_rate:
                    individual[param] = np.random.uniform(low, high)
            return individual
        
        # Inicializar população
        population = [create_individual() for _ in range(self.config.population_size)]
        best_fitness = float('-inf') if self.config.maximize else float('inf')
        best_individual = None
        fitness_history = []
        
        # Evolução
        for generation in range(self.config.generations):
            # Avaliar população
            fitness_scores = [fitness(ind) for ind in population]
            
            # Atualizar melhor indivíduo
            generation_best_idx = np.argmax(fitness_scores) if self.config.maximize \
                else np.argmin(fitness_scores)
            generation_best_fitness = fitness_scores[generation_best_idx]
            
            if (self.config.maximize and generation_best_fitness > best_fitness) or \
               (not self.config.maximize and generation_best_fitness < best_fitness):
                best_fitness = generation_best_fitness
                best_individual = population[generation_best_idx].copy()
            
            fitness_history.append(best_fitness)
            
            logger.info(f"Geração {generation + 1}/{self.config.generations}")
            logger.info(f"Melhor fitness: {best_fitness:.4f}")
            
            # Seleção
            sorted_indices = np.argsort(fitness_scores)
            if not self.config.maximize:
                sorted_indices = sorted_indices[::-1]
            
            # Criar nova população
            new_population = []
            elite_size = self.config.population_size // 10
            
            # Elitismo
            for i in range(elite_size):
                new_population.append(population[sorted_indices[i]].copy())
            
            # Crossover e Mutação
            while len(new_population) < self.config.population_size:
                parent1 = population[np.random.choice(sorted_indices[:20])]
                parent2 = population[np.random.choice(sorted_indices[:20])]
                child = crossover(parent1, parent2)
                child = mutate(child)
                new_population.append(child)
            
            population = new_population
        
        return best_individual, fitness_history
    
    def walk_forward_analysis(
        self,
        data: pd.DataFrame,
        strategy_template: Callable,
        param_optimizer: Callable
    ) -> List[Dict[str, Any]]:
        """
        Realiza análise walk-forward.
        
        Args:
            data (pd.DataFrame): Dados históricos
            strategy_template (Callable): Template da estratégia
            param_optimizer (Callable): Função de otimização de parâmetros
            
        Returns:
            List[Dict[str, Any]]: Resultados da análise
        """
        results = []
        total_periods = len(data)
        current_idx = 0
        
        while current_idx + self.config.train_size + self.config.test_size <= total_periods:
            # Dividir dados em treino e teste
            train_data = data.iloc[current_idx:current_idx + self.config.train_size]
            test_data = data.iloc[
                current_idx + self.config.train_size:
                current_idx + self.config.train_size + self.config.test_size
            ]
            
            # Otimizar parâmetros no conjunto de treino
            best_params = param_optimizer(train_data)
            
            # Testar parâmetros otimizados
            strategy = lambda x, state: strategy_template(x, state, **best_params)
            test_results = self.backtest_engine.run(test_data, strategy)
            
            # Registrar resultados
            period_results = {
                'train_start': train_data.index[0],
                'train_end': train_data.index[-1],
                'test_start': test_data.index[0],
                'test_end': test_data.index[-1],
                'parameters': best_params,
                'train_score': test_results[self.config.metric],
                'test_score': test_results[self.config.metric]
            }
            
            results.append(period_results)
            logger.info(f"Período: {period_results['test_start']} - {period_results['test_end']}")
            logger.info(f"Score teste: {period_results['test_score']:.4f}")
            
            # Avançar para próximo período
            current_idx += self.config.step_size
        
        return results 