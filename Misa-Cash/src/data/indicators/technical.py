from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
from dataclasses import dataclass
import logging
from ..utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class IndicatorConfig:
    """Configuração para cálculo de indicadores."""
    
    # Médias Móveis
    ma_windows: List[int] = (20, 50, 200)  # Períodos para médias móveis
    ema_windows: List[int] = (12, 26)  # Períodos para médias móveis exponenciais
    
    # Volatilidade
    volatility_window: int = 20  # Janela para cálculo de volatilidade
    atr_period: int = 14  # Período para ATR
    
    # Momentum
    rsi_period: int = 14  # Período para RSI
    macd_fast: int = 12  # Período rápido para MACD
    macd_slow: int = 26  # Período lento para MACD
    macd_signal: int = 9  # Período do sinal MACD
    
    # Volume
    volume_ma_windows: List[int] = (20, 50)  # Períodos para médias de volume
    obv_ma_period: int = 20  # Média móvel para OBV
    
    # Bandas de Bollinger
    bb_period: int = 20  # Período para Bandas de Bollinger
    bb_std: float = 2.0  # Número de desvios padrão
    
    # Estocástico
    stoch_k_period: int = 14  # Período %K
    stoch_d_period: int = 3  # Período %D
    stoch_slow: int = 3  # Período Estocástico Lento

class TechnicalIndicators:
    """Biblioteca de indicadores técnicos."""
    
    def __init__(self, config: Optional[IndicatorConfig] = None):
        """
        Inicializa a biblioteca de indicadores.
        
        Args:
            config (IndicatorConfig, opcional): Configuração dos indicadores
        """
        self.config = config or IndicatorConfig()
    
    def calculate_all(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula todos os indicadores técnicos.
        
        Args:
            df (pd.DataFrame): DataFrame com dados OHLCV
            
        Returns:
            pd.DataFrame: DataFrame com todos os indicadores
        """
        result = df.copy()
        
        # Médias Móveis
        result = self.add_moving_averages(result)
        result = self.add_exponential_moving_averages(result)
        
        # Volatilidade
        result = self.add_volatility_indicators(result)
        result = self.add_atr(result)
        
        # Momentum
        result = self.add_rsi(result)
        result = self.add_macd(result)
        
        # Volume
        result = self.add_volume_indicators(result)
        result = self.add_obv(result)
        
        # Bandas de Bollinger
        result = self.add_bollinger_bands(result)
        
        # Estocástico
        result = self.add_stochastic(result)
        
        return result
    
    def add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona médias móveis simples."""
        for window in self.config.ma_windows:
            df[f'sma_{window}'] = df['close'].rolling(window=window).mean()
        return df
    
    def add_exponential_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona médias móveis exponenciais."""
        for window in self.config.ema_windows:
            df[f'ema_{window}'] = df['close'].ewm(span=window, adjust=False).mean()
        return df
    
    def add_volatility_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona indicadores de volatilidade."""
        # Retornos diários
        df['daily_return'] = df['close'].pct_change()
        
        # Volatilidade
        df['volatility'] = df['daily_return'].rolling(
            window=self.config.volatility_window
        ).std()
        
        return df
    
    def add_atr(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona Average True Range (ATR)."""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        
        df['atr'] = true_range.rolling(window=self.config.atr_period).mean()
        return df
    
    def add_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona Relative Strength Index (RSI)."""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.config.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.config.rsi_period).mean()
        
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        return df
    
    def add_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona Moving Average Convergence Divergence (MACD)."""
        exp1 = df['close'].ewm(span=self.config.macd_fast, adjust=False).mean()
        exp2 = df['close'].ewm(span=self.config.macd_slow, adjust=False).mean()
        
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(
            span=self.config.macd_signal, adjust=False
        ).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        return df
    
    def add_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona indicadores de volume."""
        for window in self.config.volume_ma_windows:
            df[f'volume_sma_{window}'] = df['volume'].rolling(window=window).mean()
            
        # Volume Force Index
        df['force_index'] = df['close'].diff() * df['volume']
        df['force_index_ema'] = df['force_index'].ewm(span=13, adjust=False).mean()
        
        return df
    
    def add_obv(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona On Balance Volume (OBV)."""
        df['obv'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
        df['obv_ma'] = df['obv'].rolling(window=self.config.obv_ma_period).mean()
        return df
    
    def add_bollinger_bands(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona Bandas de Bollinger."""
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        
        # Média móvel
        df['bb_middle'] = typical_price.rolling(window=self.config.bb_period).mean()
        
        # Desvio padrão
        bb_std = typical_price.rolling(window=self.config.bb_period).std()
        
        # Bandas superior e inferior
        df['bb_upper'] = df['bb_middle'] + (bb_std * self.config.bb_std)
        df['bb_lower'] = df['bb_middle'] - (bb_std * self.config.bb_std)
        
        # Largura das bandas
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        
        return df
    
    def add_stochastic(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona Oscilador Estocástico."""
        # %K
        lowest_low = df['low'].rolling(window=self.config.stoch_k_period).min()
        highest_high = df['high'].rolling(window=self.config.stoch_k_period).max()
        
        df['stoch_k'] = 100 * (df['close'] - lowest_low) / (highest_high - lowest_low)
        
        # %D
        df['stoch_d'] = df['stoch_k'].rolling(window=self.config.stoch_d_period).mean()
        
        # Estocástico Lento
        df['stoch_slow'] = df['stoch_d'].rolling(
            window=self.config.stoch_slow
        ).mean()
        
        return df
    
    def get_indicator_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula estatísticas dos indicadores.
        
        Args:
            df (pd.DataFrame): DataFrame com indicadores
            
        Returns:
            Dict[str, Any]: Estatísticas calculadas
        """
        stats = {}
        
        # Tendência (baseado nas médias móveis)
        sma_20 = df.get('sma_20')
        sma_50 = df.get('sma_50')
        if sma_20 is not None and sma_50 is not None:
            stats['trend'] = 'up' if sma_20.iloc[-1] > sma_50.iloc[-1] else 'down'
        
        # Força da tendência (baseado no RSI)
        rsi = df.get('rsi')
        if rsi is not None:
            current_rsi = rsi.iloc[-1]
            stats['rsi_signal'] = (
                'overbought' if current_rsi > 70
                else 'oversold' if current_rsi < 30
                else 'neutral'
            )
        
        # Momentum (baseado no MACD)
        macd = df.get('macd')
        macd_signal = df.get('macd_signal')
        if macd is not None and macd_signal is not None:
            stats['macd_signal'] = (
                'bullish' if macd.iloc[-1] > macd_signal.iloc[-1]
                else 'bearish'
            )
        
        # Volatilidade (baseado nas Bandas de Bollinger)
        bb_width = df.get('bb_width')
        if bb_width is not None:
            current_width = bb_width.iloc[-1]
            mean_width = bb_width.mean()
            stats['volatility_state'] = (
                'high' if current_width > mean_width
                else 'low'
            )
        
        return stats 