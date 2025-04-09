from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ..optimizer import StrategyOptimizer, OptimizationConfig
from ...backtesting import BacktestConfig
from ...data.indicators import IndicatorConfig
from ...data.collectors import YFinanceCollector
import logging
from ...utils.logger import get_logger

logger = get_logger(__name__)

def sma_crossover_strategy(
    data: pd.DataFrame,
    state: dict,
    fast_period: int = 20,
    slow_period: int = 50,
    rsi_period: int = 14,
    rsi_threshold: float = 30
) -> list:
    """
    Estratégia de cruzamento de médias móveis com filtro de RSI.
    
    Args:
        data (pd.DataFrame): DataFrame com dados e indicadores
        state (dict): Estado atual do backtesting
        fast_period (int): Período da média rápida
        slow_period (int): Período da média lenta
        rsi_period (int): Período do RSI
        rsi_threshold (float): Limite do RSI para compra
        
    Returns:
        list: Lista de sinais de trading
    """
    if len(data) < slow_period:
        return []
    
    current = data.iloc[-1]
    previous = data.iloc[-2]
    
    signals = []
    symbol = data.index.name or 'unknown'
    
    # Verificar cruzamento das médias e RSI
    if (previous[f'sma_{fast_period}'] <= previous[f'sma_{slow_period}'] and 
        current[f'sma_{fast_period}'] > current[f'sma_{slow_period}'] and
        current['rsi'] < rsi_threshold):
        # Cruzamento para cima com RSI sobrevendido
        signals.append({
            'type': 'entry',
            'symbol': symbol,
            'position_type': 'long'
        })
    elif (previous[f'sma_{fast_period}'] >= previous[f'sma_{slow_period}'] and 
          current[f'sma_{fast_period}'] < current[f'sma_{slow_period}']):
        # Cruzamento para baixo
        for position in state['positions']:
            if position.symbol == symbol and position.position_type == 'long':
                signals.append({
                    'type': 'exit',
                    'symbol': symbol
                })
    
    return signals

def plot_optimization_results(results: dict, title: str, filename: str):
    """
    Plota resultados da otimização.
    
    Args:
        results (dict): Resultados da otimização
        title (str): Título do gráfico
        filename (str): Nome do arquivo para salvar
    """
    plt.figure(figsize=(12, 6))
    
    if isinstance(results, dict):
        # Resultados do grid search
        scores = list(results.values())
        plt.plot(range(len(scores)), scores, 'b-')
        plt.xlabel('Combinação de Parâmetros')
        plt.ylabel('Score')
    else:
        # Resultados da otimização genética
        plt.plot(range(len(results)), results, 'r-')
        plt.xlabel('Geração')
        plt.ylabel('Melhor Fitness')
    
    plt.title(title)
    plt.grid(True)
    plt.savefig(f'data/{filename}.png')
    plt.close()

def plot_walk_forward_results(results: list):
    """
    Plota resultados da análise walk-forward.
    
    Args:
        results (list): Resultados da análise walk-forward
    """
    plt.figure(figsize=(15, 8))
    
    # Extrair dados
    dates = [r['test_start'] for r in results]
    train_scores = [r['train_score'] for r in results]
    test_scores = [r['test_score'] for r in results]
    
    # Plotar scores
    plt.plot(dates, train_scores, 'b-', label='Treino')
    plt.plot(dates, test_scores, 'r-', label='Teste')
    
    plt.title('Análise Walk-Forward')
    plt.xlabel('Data')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig('data/walk_forward_results.png')
    plt.close()

def main():
    """Função principal para testar otimização."""
    # Configurações
    optimization_config = OptimizationConfig(
        metric='sharpe_ratio',
        maximize=True,
        population_size=50,
        generations=30,
        train_size=252,
        test_size=126,
        step_size=21
    )
    
    backtest_config = BacktestConfig(
        initial_capital=100000.0,
        position_size=0.1,
        stop_loss=0.02,
        take_profit=0.05
    )
    
    indicator_config = IndicatorConfig(
        ma_windows=[10, 20, 50, 100, 200],
        rsi_period=14
    )
    
    # Criar otimizador
    optimizer = StrategyOptimizer(
        optimization_config,
        backtest_config,
        indicator_config
    )
    
    # Preparar dados
    collector = YFinanceCollector()
    symbol = 'AAPL'
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 2 anos
    
    data = collector.get_daily_data(symbol, start_date, end_date)
    if data is None or data.empty:
        logger.error("Sem dados para otimização")
        return
    
    try:
        # Grid Search
        logger.info("\nExecutando Grid Search...")
        param_grid = {
            'fast_period': [10, 20, 30],
            'slow_period': [40, 50, 60],
            'rsi_period': [10, 14, 20],
            'rsi_threshold': [20, 30, 40]
        }
        
        best_grid_params, grid_results = optimizer.grid_search(
            data,
            sma_crossover_strategy,
            param_grid
        )
        
        logger.info(f"Melhores parâmetros (Grid Search): {best_grid_params}")
        plot_optimization_results(
            grid_results,
            'Resultados Grid Search',
            'grid_search_results'
        )
        
        # Otimização Genética
        logger.info("\nExecutando Otimização Genética...")
        param_bounds = {
            'fast_period': (5, 30),
            'slow_period': (31, 100),
            'rsi_period': (5, 30),
            'rsi_threshold': (20, 40)
        }
        
        best_ga_params, ga_history = optimizer.genetic_optimize(
            data,
            sma_crossover_strategy,
            param_bounds
        )
        
        logger.info(f"Melhores parâmetros (GA): {best_ga_params}")
        plot_optimization_results(
            ga_history,
            'Evolução da Otimização Genética',
            'genetic_optimization_results'
        )
        
        # Walk-Forward Analysis
        logger.info("\nExecutando Análise Walk-Forward...")
        def param_optimizer(train_data):
            """Otimizador para walk-forward."""
            _, results = optimizer.grid_search(
                train_data,
                sma_crossover_strategy,
                param_grid
            )
            return best_grid_params
        
        wfa_results = optimizer.walk_forward_analysis(
            data,
            sma_crossover_strategy,
            param_optimizer
        )
        
        plot_walk_forward_results(wfa_results)
        
        # Calcular médias dos scores
        train_scores = [r['train_score'] for r in wfa_results]
        test_scores = [r['test_score'] for r in wfa_results]
        
        logger.info("\nResultados Walk-Forward:")
        logger.info(f"Score médio treino: {np.mean(train_scores):.4f}")
        logger.info(f"Score médio teste: {np.mean(test_scores):.4f}")
        
    except Exception as e:
        logger.error(f"Erro durante otimização: {str(e)}")

if __name__ == "__main__":
    main() 