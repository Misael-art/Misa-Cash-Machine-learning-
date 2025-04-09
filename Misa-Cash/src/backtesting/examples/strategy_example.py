from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from ..engine import BacktestEngine, BacktestConfig
from ...data.indicators import IndicatorConfig
from ...data.collectors import YFinanceCollector
import logging
from ...utils.logger import get_logger
import matplotlib.pyplot as plt
import seaborn as sns

logger = get_logger(__name__)

def sma_crossover_strategy(data: pd.DataFrame, state: dict) -> list:
    """
    Estratégia de cruzamento de médias móveis.
    
    Args:
        data (pd.DataFrame): DataFrame com dados e indicadores
        state (dict): Estado atual do backtesting
        
    Returns:
        list: Lista de sinais de trading
    """
    if len(data) < 50:  # Precisamos de pelo menos 50 períodos
        return []
    
    current = data.iloc[-1]
    previous = data.iloc[-2]
    
    signals = []
    symbol = data.index.name or 'unknown'
    
    # Verificar cruzamento das médias
    if previous['sma_20'] <= previous['sma_50'] and current['sma_20'] > current['sma_50']:
        # Cruzamento para cima (compra)
        signals.append({
            'type': 'entry',
            'symbol': symbol,
            'position_type': 'long'
        })
    elif previous['sma_20'] >= previous['sma_50'] and current['sma_20'] < current['sma_50']:
        # Cruzamento para baixo (venda)
        for position in state['positions']:
            if position.symbol == symbol and position.position_type == 'long':
                signals.append({
                    'type': 'exit',
                    'symbol': symbol
                })
    
    return signals

def plot_backtest_results(results: dict, symbol: str):
    """
    Plota os resultados do backtesting.
    
    Args:
        results (dict): Resultados do backtesting
        symbol (str): Símbolo analisado
    """
    # Configurar estilo
    plt.style.use('seaborn')
    
    # Criar figura com subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), height_ratios=[2, 1])
    
    # Plot da curva de equity
    equity_curve = results['equity_curve']
    ax1.plot(equity_curve.index, equity_curve['equity'], label='Equity', color='blue')
    ax1.set_title(f'Resultados do Backtesting - {symbol}')
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Equity')
    ax1.grid(True)
    ax1.legend()
    
    # Plot do drawdown
    peak = equity_curve['equity'].expanding(min_periods=1).max()
    drawdown = (equity_curve['equity'] - peak) / peak
    ax2.fill_between(drawdown.index, drawdown.values * 100, 0, color='red', alpha=0.3)
    ax2.set_title('Drawdown (%)')
    ax2.set_xlabel('Data')
    ax2.set_ylabel('Drawdown %')
    ax2.grid(True)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar figura
    plt.savefig(f'data/backtest_results_{symbol}.png')
    plt.close()

def print_statistics(results: dict):
    """
    Imprime estatísticas do backtesting.
    
    Args:
        results (dict): Resultados do backtesting
    """
    logger.info("\nEstatísticas do Backtesting:")
    logger.info(f"Total de Trades: {results['total_trades']}")
    logger.info(f"Trades Vencedores: {results['winning_trades']}")
    logger.info(f"Trades Perdedores: {results['losing_trades']}")
    logger.info(f"Taxa de Acerto: {results['win_rate']:.2%}")
    logger.info(f"Profit Factor: {results['profit_factor']:.2f}")
    logger.info(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    logger.info(f"Máximo Drawdown: {results['max_drawdown']:.2%}")
    logger.info(f"Retorno Total: {results['total_return']:.2%}")

def main():
    """Função principal para testar o backtesting."""
    # Configurar backtesting
    config = BacktestConfig(
        initial_capital=100000.0,
        position_size=0.1,
        stop_loss=0.02,
        take_profit=0.05
    )
    
    # Configurar indicadores
    indicator_config = IndicatorConfig(
        ma_windows=[20, 50, 200],
        rsi_period=14,
        bb_period=20
    )
    
    # Criar engine
    engine = BacktestEngine(config, indicator_config)
    
    # Preparar dados
    collector = YFinanceCollector()
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for symbol in symbols:
        try:
            logger.info(f"\nTestando estratégia em {symbol}")
            
            # Obter dados
            data = collector.get_daily_data(
                symbol=symbol,
                start=start_date,
                end=end_date
            )
            
            if data is None or data.empty:
                logger.error(f"Sem dados para {symbol}")
                continue
            
            # Executar backtesting
            results = engine.run(data, sma_crossover_strategy)
            
            # Imprimir estatísticas
            print_statistics(results)
            
            # Plotar resultados
            plot_backtest_results(results, symbol)
            
            # Resetar engine para próximo símbolo
            engine.reset()
            
        except Exception as e:
            logger.error(f"Erro ao testar {symbol}: {str(e)}")
            continue

if __name__ == "__main__":
    main() 