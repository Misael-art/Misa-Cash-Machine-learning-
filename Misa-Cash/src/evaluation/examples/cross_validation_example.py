import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import logging

from ...data.collectors import YFinanceCollector
from ...technical import TechnicalIndicators, IndicatorConfig
from ..cross_validation import CrossValidator
from ...utils.logger import get_logger

logger = get_logger(__name__)

def sma_rsi_strategy(
    data: pd.DataFrame,
    state: Dict,
    fast_period: int = 20,
    slow_period: int = 50,
    rsi_period: int = 14,
    rsi_buy: float = 30,
    rsi_sell: float = 70
) -> List[Dict]:
    """
    Estratégia de exemplo usando SMA e RSI.
    
    Args:
        data: DataFrame com dados históricos
        state: Estado atual da estratégia
        fast_period: Período da média móvel rápida
        slow_period: Período da média móvel lenta
        rsi_period: Período do RSI
        rsi_buy: Nível de sobrevenda do RSI
        rsi_sell: Nível de sobrecompra do RSI
    """
    if len(data) < max(fast_period, slow_period, rsi_period):
        return []
    
    # Calcular indicadores
    config = IndicatorConfig()
    indicators = TechnicalIndicators(config)
    
    df = data.copy()
    df['sma_fast'] = indicators.sma(df['Close'], fast_period)
    df['sma_slow'] = indicators.sma(df['Close'], slow_period)
    df['rsi'] = indicators.rsi(df['Close'], rsi_period)
    
    current = df.iloc[-1]
    previous = df.iloc[-2]
    
    signals = []
    positions = state.get('positions', [])
    
    # Lógica de entrada
    if (
        current['sma_fast'] > current['sma_slow'] and
        previous['sma_fast'] <= previous['sma_slow'] and
        current['rsi'] < rsi_buy and
        not positions
    ):
        signals.append({
            'type': 'buy',
            'price': current['Close'],
            'size': 1.0,
            'stop_loss': current['Close'] * 0.95,
            'take_profit': current['Close'] * 1.10
        })
    
    # Lógica de saída
    elif (
        (current['sma_fast'] < current['sma_slow'] and
        previous['sma_fast'] >= previous['sma_slow']) or
        current['rsi'] > rsi_sell
    ) and positions:
        signals.append({
            'type': 'sell',
            'price': current['Close'],
            'size': 1.0
        })
    
    return signals

def plot_validation_results(result, title: str, filename: str):
    """
    Plota resultados da validação cruzada.
    
    Args:
        result: Resultado da validação
        title: Título do gráfico
        filename: Nome do arquivo para salvar
    """
    metrics = list(result.train_mean.keys())
    n_metrics = len(metrics)
    
    fig, axes = plt.subplots(n_metrics, 1, figsize=(12, 4*n_metrics))
    if n_metrics == 1:
        axes = [axes]
    
    for ax, metric in zip(axes, metrics):
        train_values = [score[metric] for score in result.train_scores]
        test_values = [score[metric] for score in result.test_scores]
        
        # Criar boxplot
        data = [train_values, test_values]
        labels = ['Treino', 'Teste']
        
        sns.boxplot(data=data, ax=ax)
        ax.set_xticklabels(labels)
        ax.set_title(f'{metric} Distribution')
        ax.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'docs/images/{filename}.png')
    plt.close()

def main():
    """Exemplo principal de validação cruzada."""
    try:
        # Configurar logging
        logger.info("Iniciando exemplo de validação cruzada")
        
        # Coletar dados
        symbols = ['AAPL', 'MSFT', 'GOOGL']
        collector = YFinanceCollector()
        start_date = datetime.now() - timedelta(days=365*2)
        end_date = datetime.now()
        
        for symbol in symbols:
            logger.info(f"Processando {symbol}")
            
            # Coletar dados
            data = collector.collect_data(
                symbol,
                start_date,
                end_date,
                interval='1d'
            )
            
            # Configurar validação cruzada
            cv = CrossValidator(
                data=data,
                strategy=sma_rsi_strategy,
                performance_metrics=['sharpe_ratio', 'max_drawdown', 'total_return'],
                min_train_size=252,  # 1 ano
                test_size=63,        # 3 meses
                step_size=21,        # 1 mês
                gap_size=0           # Sem gap
            )
            
            # Parâmetros para testar
            parameters = {
                'fast_period': 20,
                'slow_period': 50,
                'rsi_period': 14,
                'rsi_buy': 30,
                'rsi_sell': 70
            }
            
            # Executar validação com diferentes métodos
            methods = ['expanding', 'sliding', 'monte_carlo']
            
            for method in methods:
                logger.info(f"Executando validação {method} para {symbol}")
                
                result = cv.validate(
                    method=method,
                    parameters=parameters,
                    n_splits=5
                )
                
                # Plotar resultados
                plot_validation_results(
                    result,
                    f"{symbol} - {method.capitalize()} Window Validation",
                    f"{symbol.lower()}_{method}_validation"
                )
                
                # Logar resultados
                logger.info(f"\nResultados para {symbol} usando {method}:")
                for metric in result.train_mean.keys():
                    logger.info(f"\n{metric}:")
                    logger.info(f"Treino: {result.train_mean[metric]:.4f} ± {result.train_std[metric]:.4f}")
                    logger.info(f"Teste: {result.test_mean[metric]:.4f} ± {result.test_std[metric]:.4f}")
        
        logger.info("Exemplo de validação cruzada concluído com sucesso")
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    main() 