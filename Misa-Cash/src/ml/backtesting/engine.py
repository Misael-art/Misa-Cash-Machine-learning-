from typing import Optional, List, Dict, Any, Callable, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass
from datetime import datetime
import logging
from ..utils.logger import get_logger
from ..data.indicators import TechnicalIndicators, IndicatorConfig

logger = get_logger(__name__)

@dataclass
class BacktestConfig:
    """Configuração para backtesting."""
    
    initial_capital: float = 100000.0  # Capital inicial
    position_size: float = 0.1  # Tamanho da posição (% do capital)
    max_positions: int = 5  # Número máximo de posições simultâneas
    stop_loss: float = 0.02  # Stop loss (%)
    take_profit: float = 0.05  # Take profit (%)
    commission: float = 0.001  # Comissão por operação (%)
    slippage: float = 0.001  # Slippage estimado (%)
    use_fractional: bool = True  # Permite posições fracionárias
    
@dataclass
class TradeInfo:
    """Informações sobre uma operação."""
    
    symbol: str  # Símbolo negociado
    entry_date: datetime  # Data de entrada
    entry_price: float  # Preço de entrada
    position_type: str  # 'long' ou 'short'
    size: float  # Tamanho da posição
    stop_loss: float  # Preço do stop loss
    take_profit: float  # Preço do take profit
    exit_date: Optional[datetime] = None  # Data de saída
    exit_price: Optional[float] = None  # Preço de saída
    pnl: Optional[float] = None  # Resultado da operação
    exit_reason: Optional[str] = None  # Razão do fechamento

class BacktestEngine:
    """Engine de backtesting para estratégias de trading."""
    
    def __init__(
        self,
        config: Optional[BacktestConfig] = None,
        indicator_config: Optional[IndicatorConfig] = None
    ):
        """
        Inicializa o engine de backtesting.
        
        Args:
            config (BacktestConfig, opcional): Configuração do backtesting
            indicator_config (IndicatorConfig, opcional): Configuração dos indicadores
        """
        self.config = config or BacktestConfig()
        self.indicators = TechnicalIndicators(indicator_config)
        self.reset()
        
    def reset(self):
        """Reseta o estado do backtesting."""
        self.capital = self.config.initial_capital
        self.equity = []  # Histórico do patrimônio
        self.positions = []  # Posições abertas
        self.trades = []  # Histórico de trades
        self.current_date = None
        
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepara os dados para backtesting.
        
        Args:
            df (pd.DataFrame): DataFrame com dados OHLCV
            
        Returns:
            pd.DataFrame: DataFrame com indicadores
        """
        # Garantir ordenação por data
        df = df.sort_index()
        
        # Calcular indicadores
        df = self.indicators.calculate_all(df)
        
        return df
    
    def run(
        self,
        df: pd.DataFrame,
        strategy: Callable[[pd.DataFrame, Dict[str, Any]], List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Executa o backtesting.
        
        Args:
            df (pd.DataFrame): DataFrame com dados OHLCV
            strategy (Callable): Função de estratégia que retorna sinais
            
        Returns:
            Dict[str, Any]: Resultados do backtesting
        """
        # Preparar dados
        data = self.prepare_data(df)
        
        # Loop principal
        for index, row in data.iterrows():
            self.current_date = index
            
            # Atualizar posições abertas
            self._update_positions(row)
            
            # Verificar sinais da estratégia
            signals = strategy(data.loc[:index], self._get_state())
            
            # Processar sinais
            for signal in signals:
                self._process_signal(signal, row)
            
            # Registrar equity
            self.equity.append({
                'date': index,
                'equity': self._calculate_equity(row)
            })
        
        # Fechar posições abertas
        self._close_all_positions(data.iloc[-1])
        
        # Calcular estatísticas
        return self._calculate_statistics()
    
    def _update_positions(self, row: pd.Series):
        """Atualiza o estado das posições abertas."""
        for position in self.positions[:]:  # Copiar lista para permitir remoção
            # Verificar stop loss
            if position.position_type == 'long':
                if row['low'] <= position.stop_loss:
                    self._close_position(position, row, position.stop_loss, 'stop_loss')
                    continue
                    
                if row['high'] >= position.take_profit:
                    self._close_position(position, row, position.take_profit, 'take_profit')
                    continue
            else:  # short
                if row['high'] >= position.stop_loss:
                    self._close_position(position, row, position.stop_loss, 'stop_loss')
                    continue
                    
                if row['low'] <= position.take_profit:
                    self._close_position(position, row, position.take_profit, 'take_profit')
                    continue
    
    def _process_signal(self, signal: Dict[str, Any], row: pd.Series):
        """Processa um sinal de trading."""
        signal_type = signal.get('type')
        symbol = signal.get('symbol')
        
        if signal_type == 'entry':
            # Verificar se pode abrir nova posição
            if len(self.positions) >= self.config.max_positions:
                return
                
            # Calcular tamanho da posição
            position_value = self.capital * self.config.position_size
            price = row['close'] * (1 + self.config.slippage)
            size = position_value / price
            
            if not self.config.use_fractional:
                size = np.floor(size)
                if size == 0:
                    return
            
            # Calcular stop loss e take profit
            if signal.get('position_type') == 'long':
                stop_loss = price * (1 - self.config.stop_loss)
                take_profit = price * (1 + self.config.take_profit)
            else:
                stop_loss = price * (1 + self.config.stop_loss)
                take_profit = price * (1 - self.config.take_profit)
            
            # Criar nova posição
            trade = TradeInfo(
                symbol=symbol,
                entry_date=self.current_date,
                entry_price=price,
                position_type=signal.get('position_type'),
                size=size,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            
            self.positions.append(trade)
            
        elif signal_type == 'exit':
            # Encontrar e fechar posição
            for position in self.positions[:]:
                if position.symbol == symbol:
                    self._close_position(
                        position,
                        row,
                        row['close'] * (1 - self.config.slippage),
                        'signal'
                    )
    
    def _close_position(
        self,
        position: TradeInfo,
        row: pd.Series,
        price: float,
        reason: str
    ):
        """Fecha uma posição."""
        position.exit_date = self.current_date
        position.exit_price = price
        position.exit_reason = reason
        
        # Calcular P&L
        if position.position_type == 'long':
            pnl = (position.exit_price - position.entry_price) * position.size
        else:
            pnl = (position.entry_price - position.exit_price) * position.size
            
        # Subtrair comissões
        commission = (
            position.entry_price * position.size * self.config.commission +
            position.exit_price * position.size * self.config.commission
        )
        pnl -= commission
        
        position.pnl = pnl
        self.capital += pnl
        
        # Registrar trade
        self.trades.append(position)
        self.positions.remove(position)
    
    def _close_all_positions(self, row: pd.Series):
        """Fecha todas as posições abertas."""
        for position in self.positions[:]:
            self._close_position(
                position,
                row,
                row['close'] * (1 - self.config.slippage),
                'end_of_test'
            )
    
    def _calculate_equity(self, row: pd.Series) -> float:
        """Calcula o patrimônio atual."""
        equity = self.capital
        
        # Adicionar valor das posições abertas
        for position in self.positions:
            if position.position_type == 'long':
                pnl = (row['close'] - position.entry_price) * position.size
            else:
                pnl = (position.entry_price - row['close']) * position.size
            equity += pnl
        
        return equity
    
    def _get_state(self) -> Dict[str, Any]:
        """Retorna o estado atual do backtesting."""
        return {
            'capital': self.capital,
            'positions': self.positions,
            'trades': self.trades
        }
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calcula estatísticas do backtesting."""
        if not self.trades:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'profit_factor': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'total_return': 0.0
            }
        
        # Criar DataFrame de equity
        equity_df = pd.DataFrame(self.equity).set_index('date')
        
        # Calcular retornos
        returns = equity_df['equity'].pct_change().dropna()
        
        # Estatísticas básicas
        winning_trades = len([t for t in self.trades if t.pnl > 0])
        losing_trades = len([t for t in self.trades if t.pnl <= 0])
        
        gross_profits = sum([t.pnl for t in self.trades if t.pnl > 0])
        gross_losses = abs(sum([t.pnl for t in self.trades if t.pnl <= 0]))
        
        # Calcular drawdown
        peak = equity_df['equity'].expanding(min_periods=1).max()
        drawdown = (equity_df['equity'] - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        # Calcular Sharpe Ratio (assumindo retorno livre de risco = 0)
        sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
        
        return {
            'total_trades': len(self.trades),
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': winning_trades / len(self.trades),
            'profit_factor': gross_profits / gross_losses if gross_losses > 0 else float('inf'),
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_return': (self.capital - self.config.initial_capital) / self.config.initial_capital,
            'equity_curve': equity_df
        } 