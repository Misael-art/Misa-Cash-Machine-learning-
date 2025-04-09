from typing import List, Dict, Optional, Union
import numpy as np
import pandas as pd
from scipy import stats
from dataclasses import dataclass
import logging
from ..utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class RiskMetrics:
    """Métricas de risco."""
    var_95: float  # Value at Risk (95%)
    var_99: float  # Value at Risk (99%)
    cvar_95: float  # Conditional VaR (95%)
    beta: float  # Beta do mercado
    volatility: float  # Volatilidade anualizada
    downside_risk: float  # Risco de baixa
    correlation: float  # Correlação com benchmark

@dataclass
class ReturnMetrics:
    """Métricas de retorno."""
    total_return: float  # Retorno total
    annual_return: float  # Retorno anualizado
    cagr: float  # Taxa de crescimento anual composta
    risk_free_return: float  # Retorno livre de risco
    excess_return: float  # Retorno excedente
    risk_adjusted_return: float  # Retorno ajustado ao risco

@dataclass
class RobustnessMetrics:
    """Métricas de robustez."""
    stability_score: float  # Score de estabilidade
    consistency_score: float  # Score de consistência
    regime_performance: Dict[str, float]  # Performance em diferentes regimes
    parameter_sensitivity: float  # Sensibilidade a parâmetros
    data_sensitivity: float  # Sensibilidade a dados

@dataclass
class DrawdownMetrics:
    """Métricas de drawdown."""
    max_drawdown: float  # Máximo drawdown
    avg_drawdown: float  # Drawdown médio
    max_drawdown_duration: int  # Duração máxima do drawdown
    avg_drawdown_duration: int  # Duração média do drawdown
    recovery_factor: float  # Fator de recuperação
    ulcer_index: float  # Índice Ulcer

@dataclass
class TradeMetrics:
    """Métricas de trade."""
    total_trades: int  # Total de trades
    winning_trades: int  # Trades vencedores
    losing_trades: int  # Trades perdedores
    win_rate: float  # Taxa de acerto
    profit_factor: float  # Fator de lucro
    avg_win: float  # Ganho médio
    avg_loss: float  # Perda média
    largest_win: float  # Maior ganho
    largest_loss: float  # Maior perda
    avg_holding_period: float  # Período médio de holding
    expectancy: float  # Expectativa matemática

class PerformanceMetrics:
    """Calculadora de métricas de performance."""
    
    def __init__(
        self,
        returns: pd.Series,
        benchmark_returns: Optional[pd.Series] = None,
        risk_free_rate: float = 0.03,
        trading_days: int = 252
    ):
        """
        Inicializa o calculador de métricas.
        
        Args:
            returns (pd.Series): Série de retornos
            benchmark_returns (pd.Series): Série de retornos do benchmark
            risk_free_rate (float): Taxa livre de risco anual
            trading_days (int): Dias de trading por ano
        """
        self.returns = returns
        self.benchmark_returns = benchmark_returns
        self.risk_free_rate = risk_free_rate
        self.trading_days = trading_days
        self.daily_rf_rate = (1 + risk_free_rate) ** (1/trading_days) - 1
    
    def calculate_risk_metrics(self) -> RiskMetrics:
        """Calcula métricas de risco."""
        returns = self.returns.values
        
        # VaR e CVaR
        var_95 = np.percentile(returns, 5)
        var_99 = np.percentile(returns, 1)
        cvar_95 = returns[returns <= var_95].mean()
        
        # Beta e correlação
        if self.benchmark_returns is not None:
            covariance = np.cov(returns, self.benchmark_returns.values)[0][1]
            benchmark_variance = np.var(self.benchmark_returns.values)
            beta = covariance / benchmark_variance
            correlation = np.corrcoef(returns, self.benchmark_returns.values)[0][1]
        else:
            beta = 1.0
            correlation = 1.0
        
        # Volatilidade e downside risk
        volatility = returns.std() * np.sqrt(self.trading_days)
        downside_returns = returns[returns < 0]
        downside_risk = downside_returns.std() * np.sqrt(self.trading_days)
        
        return RiskMetrics(
            var_95=var_95,
            var_99=var_99,
            cvar_95=cvar_95,
            beta=beta,
            volatility=volatility,
            downside_risk=downside_risk,
            correlation=correlation
        )
    
    def calculate_return_metrics(self) -> ReturnMetrics:
        """Calcula métricas de retorno."""
        returns = self.returns.values
        
        # Retornos totais e anualizados
        total_return = (1 + returns).prod() - 1
        n_years = len(returns) / self.trading_days
        annual_return = (1 + total_return) ** (1/n_years) - 1
        
        # CAGR
        cagr = (1 + total_return) ** (1/n_years) - 1
        
        # Retornos excedentes
        total_rf_return = (1 + self.daily_rf_rate) ** len(returns) - 1
        excess_return = total_return - total_rf_return
        
        # Retorno ajustado ao risco (Sharpe Ratio anualizado)
        volatility = returns.std() * np.sqrt(self.trading_days)
        risk_adjusted_return = (annual_return - self.risk_free_rate) / volatility
        
        return ReturnMetrics(
            total_return=total_return,
            annual_return=annual_return,
            cagr=cagr,
            risk_free_return=total_rf_return,
            excess_return=excess_return,
            risk_adjusted_return=risk_adjusted_return
        )
    
    def calculate_robustness_metrics(
        self,
        regime_returns: Optional[Dict[str, pd.Series]] = None,
        param_results: Optional[List[float]] = None,
        data_results: Optional[List[float]] = None
    ) -> RobustnessMetrics:
        """
        Calcula métricas de robustez.
        
        Args:
            regime_returns: Retornos em diferentes regimes de mercado
            param_results: Resultados com diferentes parâmetros
            data_results: Resultados com diferentes amostras de dados
        """
        returns = self.returns.values
        
        # Estabilidade (baseada na autocorrelação)
        stability = np.abs(pd.Series(returns).autocorr(1))
        
        # Consistência (baseada no sinal dos retornos)
        signs = np.sign(returns)
        consistency = np.mean(signs[1:] == signs[:-1])
        
        # Performance em diferentes regimes
        regime_performance = {}
        if regime_returns:
            for regime, regime_rets in regime_returns.items():
                regime_performance[regime] = regime_rets.mean()
        
        # Sensibilidade a parâmetros
        param_sensitivity = 0.0
        if param_results:
            param_sensitivity = np.std(param_results) / np.mean(param_results)
        
        # Sensibilidade a dados
        data_sensitivity = 0.0
        if data_results:
            data_sensitivity = np.std(data_results) / np.mean(data_results)
        
        return RobustnessMetrics(
            stability_score=stability,
            consistency_score=consistency,
            regime_performance=regime_performance,
            parameter_sensitivity=param_sensitivity,
            data_sensitivity=data_sensitivity
        )
    
    def calculate_drawdown_metrics(self) -> DrawdownMetrics:
        """Calcula métricas de drawdown."""
        returns = self.returns.values
        cumulative = (1 + returns).cumprod()
        
        # Cálculo de drawdowns
        rolling_max = np.maximum.accumulate(cumulative)
        drawdowns = cumulative / rolling_max - 1
        
        # Métricas de drawdown
        max_drawdown = np.min(drawdowns)
        avg_drawdown = np.mean(drawdowns[drawdowns < 0])
        
        # Duração dos drawdowns
        is_drawdown = drawdowns < 0
        drawdown_starts = np.where(np.diff(is_drawdown.astype(int)) == 1)[0] + 1
        drawdown_ends = np.where(np.diff(is_drawdown.astype(int)) == -1)[0] + 1
        
        if len(drawdown_starts) > 0 and len(drawdown_ends) > 0:
            durations = drawdown_ends - drawdown_starts
            max_duration = np.max(durations)
            avg_duration = np.mean(durations)
        else:
            max_duration = 0
            avg_duration = 0
        
        # Recovery factor e Ulcer index
        total_return = cumulative[-1] - 1
        recovery_factor = np.abs(total_return / max_drawdown) if max_drawdown != 0 else np.inf
        ulcer_index = np.sqrt(np.mean(np.square(drawdowns)))
        
        return DrawdownMetrics(
            max_drawdown=max_drawdown,
            avg_drawdown=avg_drawdown,
            max_drawdown_duration=max_duration,
            avg_drawdown_duration=avg_duration,
            recovery_factor=recovery_factor,
            ulcer_index=ulcer_index
        )
    
    def calculate_trade_metrics(
        self,
        trades: List[Dict[str, Union[str, float, int]]]
    ) -> TradeMetrics:
        """
        Calcula métricas de trade.
        
        Args:
            trades: Lista de trades com informações de entrada/saída
        """
        if not trades:
            return TradeMetrics(
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0.0,
                profit_factor=0.0,
                avg_win=0.0,
                avg_loss=0.0,
                largest_win=0.0,
                largest_loss=0.0,
                avg_holding_period=0.0,
                expectancy=0.0
            )
        
        # Separar trades vencedores e perdedores
        pnls = [trade.get('pnl', 0) for trade in trades]
        winning_pnls = [pnl for pnl in pnls if pnl > 0]
        losing_pnls = [pnl for pnl in pnls if pnl <= 0]
        
        # Calcular métricas básicas
        total_trades = len(trades)
        winning_trades = len(winning_pnls)
        losing_trades = len(losing_pnls)
        
        # Win rate e profit factor
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        total_wins = sum(winning_pnls) if winning_pnls else 0
        total_losses = abs(sum(losing_pnls)) if losing_pnls else 0
        profit_factor = total_wins / total_losses if total_losses > 0 else np.inf
        
        # Médias e extremos
        avg_win = np.mean(winning_pnls) if winning_pnls else 0
        avg_loss = np.mean(losing_pnls) if losing_pnls else 0
        largest_win = max(winning_pnls) if winning_pnls else 0
        largest_loss = min(losing_pnls) if losing_pnls else 0
        
        # Período médio de holding
        holding_periods = []
        for trade in trades:
            entry_date = pd.to_datetime(trade.get('entry_date'))
            exit_date = pd.to_datetime(trade.get('exit_date'))
            if entry_date and exit_date:
                holding_periods.append((exit_date - entry_date).days)
        
        avg_holding_period = np.mean(holding_periods) if holding_periods else 0
        
        # Expectativa matemática
        expectancy = (win_rate * avg_win) - ((1 - win_rate) * abs(avg_loss))
        
        return TradeMetrics(
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            profit_factor=profit_factor,
            avg_win=avg_win,
            avg_loss=avg_loss,
            largest_win=largest_win,
            largest_loss=largest_loss,
            avg_holding_period=avg_holding_period,
            expectancy=expectancy
        )
    
    def calculate_all_metrics(
        self,
        trades: Optional[List[Dict[str, Union[str, float, int]]]] = None,
        regime_returns: Optional[Dict[str, pd.Series]] = None,
        param_results: Optional[List[float]] = None,
        data_results: Optional[List[float]] = None
    ) -> Dict[str, Union[RiskMetrics, ReturnMetrics, RobustnessMetrics, DrawdownMetrics, TradeMetrics]]:
        """
        Calcula todas as métricas disponíveis.
        
        Args:
            trades: Lista de trades para métricas de trading
            regime_returns: Retornos em diferentes regimes
            param_results: Resultados com diferentes parâmetros
            data_results: Resultados com diferentes amostras
            
        Returns:
            Dict com todas as métricas calculadas
        """
        try:
            metrics = {
                'risk': self.calculate_risk_metrics(),
                'return': self.calculate_return_metrics(),
                'robustness': self.calculate_robustness_metrics(
                    regime_returns, param_results, data_results
                ),
                'drawdown': self.calculate_drawdown_metrics()
            }
            
            if trades:
                metrics['trade'] = self.calculate_trade_metrics(trades)
            
            return metrics
        
        except Exception as e:
            logger.error(f"Erro ao calcular métricas: {str(e)}")
            return {} 