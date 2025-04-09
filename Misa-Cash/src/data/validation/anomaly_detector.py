from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from scipy import stats
from dataclasses import dataclass

@dataclass
class AnomalyConfig:
    """Configuração para detecção de anomalias."""
    
    price_std_threshold: float = 3.0  # Desvios padrão para preços
    volume_std_threshold: float = 4.0  # Desvios padrão para volume
    price_jump_threshold: float = 0.1  # 10% para variações bruscas
    volume_jump_threshold: float = 2.0  # 200% para picos de volume
    min_data_points: int = 30  # Mínimo de pontos para análise
    rolling_window: int = 20  # Janela para médias móveis

@dataclass
class AnomalyResult:
    """Resultado da detecção de anomalias."""
    
    anomalies: List[Dict]
    stats: Dict
    timestamp: pd.Timestamp
    
class AnomalyDetector:
    """Detector de anomalias em dados financeiros."""
    
    def __init__(self, config: Optional[AnomalyConfig] = None):
        """
        Inicializa o detector.
        
        Args:
            config (AnomalyConfig, opcional): Configuração personalizada
        """
        self.config = config or AnomalyConfig()
    
    def _detect_price_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detecta anomalias em preços.
        
        Args:
            df (pd.DataFrame): Dados para análise
            
        Returns:
            List[Dict]: Anomalias encontradas
        """
        anomalies = []
        
        # Calcular médias móveis e desvios
        for col in ['open', 'high', 'low', 'close']:
            rolling_mean = df[col].rolling(window=self.config.rolling_window).mean()
            rolling_std = df[col].rolling(window=self.config.rolling_window).std()
            
            # Detectar outliers baseados em desvio padrão
            z_scores = np.abs((df[col] - rolling_mean) / rolling_std)
            outliers = z_scores > self.config.price_std_threshold
            
            if outliers.any():
                for idx in df[outliers].index:
                    anomalies.append({
                        'timestamp': idx,
                        'type': 'price_outlier',
                        'column': col,
                        'value': float(df.loc[idx, col]),
                        'z_score': float(z_scores[idx]),
                        'mean': float(rolling_mean[idx]),
                        'std': float(rolling_std[idx])
                    })
            
            # Detectar variações bruscas
            returns = df[col].pct_change()
            jumps = np.abs(returns) > self.config.price_jump_threshold
            
            if jumps.any():
                for idx in df[jumps].index:
                    anomalies.append({
                        'timestamp': idx,
                        'type': 'price_jump',
                        'column': col,
                        'value': float(df.loc[idx, col]),
                        'return': float(returns[idx]),
                        'threshold': self.config.price_jump_threshold
                    })
        
        return anomalies
    
    def _detect_volume_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detecta anomalias em volume.
        
        Args:
            df (pd.DataFrame): Dados para análise
            
        Returns:
            List[Dict]: Anomalias encontradas
        """
        anomalies = []
        
        # Calcular médias móveis e desvios para volume
        rolling_mean = df['volume'].rolling(window=self.config.rolling_window).mean()
        rolling_std = df['volume'].rolling(window=self.config.rolling_window).std()
        
        # Detectar outliers baseados em desvio padrão
        z_scores = np.abs((df['volume'] - rolling_mean) / rolling_std)
        outliers = z_scores > self.config.volume_std_threshold
        
        if outliers.any():
            for idx in df[outliers].index:
                anomalies.append({
                    'timestamp': idx,
                    'type': 'volume_outlier',
                    'value': float(df.loc[idx, 'volume']),
                    'z_score': float(z_scores[idx]),
                    'mean': float(rolling_mean[idx]),
                    'std': float(rolling_std[idx])
                })
        
        # Detectar picos de volume
        volume_changes = df['volume'].pct_change()
        jumps = volume_changes > self.config.volume_jump_threshold
        
        if jumps.any():
            for idx in df[jumps].index:
                anomalies.append({
                    'timestamp': idx,
                    'type': 'volume_spike',
                    'value': float(df.loc[idx, 'volume']),
                    'change': float(volume_changes[idx]),
                    'threshold': self.config.volume_jump_threshold
                })
        
        return anomalies
    
    def _detect_pattern_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detecta anomalias em padrões de preço.
        
        Args:
            df (pd.DataFrame): Dados para análise
            
        Returns:
            List[Dict]: Anomalias encontradas
        """
        anomalies = []
        
        # Detectar gaps entre dias
        if df.index.dtype == 'datetime64[ns]':
            gaps = df.index.to_series().diff() > pd.Timedelta(days=3)
            if gaps.any():
                for idx in df[gaps].index:
                    anomalies.append({
                        'timestamp': idx,
                        'type': 'time_gap',
                        'gap_days': float((df.index[df.index.get_loc(idx)] - 
                                        df.index[df.index.get_loc(idx)-1]).days)
                    })
        
        # Detectar padrões incomuns de candlestick
        df['body'] = df['close'] - df['open']
        df['upper_shadow'] = df['high'] - df[['open', 'close']].max(axis=1)
        df['lower_shadow'] = df[['open', 'close']].min(axis=1) - df['low']
        
        # Detectar dojis (corpo muito pequeno com sombras longas)
        body_mean = df['body'].abs().mean()
        shadow_mean = (df['upper_shadow'] + df['lower_shadow']).mean()
        
        dojis = (df['body'].abs() < body_mean * 0.1) & \
                ((df['upper_shadow'] + df['lower_shadow']) > shadow_mean * 2)
        
        if dojis.any():
            for idx in df[dojis].index:
                anomalies.append({
                    'timestamp': idx,
                    'type': 'doji_pattern',
                    'body': float(df.loc[idx, 'body']),
                    'upper_shadow': float(df.loc[idx, 'upper_shadow']),
                    'lower_shadow': float(df.loc[idx, 'lower_shadow'])
                })
        
        return anomalies
    
    def detect(self, df: pd.DataFrame) -> AnomalyResult:
        """
        Detecta todas as anomalias nos dados.
        
        Args:
            df (pd.DataFrame): Dados para análise
            
        Returns:
            AnomalyResult: Resultado da detecção
        """
        if len(df) < self.config.min_data_points:
            raise ValueError(
                f"Mínimo de {self.config.min_data_points} pontos necessários"
            )
        
        # Coletar todas as anomalias
        anomalies = []
        anomalies.extend(self._detect_price_anomalies(df))
        anomalies.extend(self._detect_volume_anomalies(df))
        anomalies.extend(self._detect_pattern_anomalies(df))
        
        # Calcular estatísticas
        stats = {
            'total_anomalies': len(anomalies),
            'price_anomalies': len([a for a in anomalies if 'price' in a['type']]),
            'volume_anomalies': len([a for a in anomalies if 'volume' in a['type']]),
            'pattern_anomalies': len([a for a in anomalies if 'pattern' in a['type']]),
            'analysis_period': {
                'start': df.index[0],
                'end': df.index[-1],
                'days': (df.index[-1] - df.index[0]).days
            }
        }
        
        return AnomalyResult(
            anomalies=anomalies,
            stats=stats,
            timestamp=pd.Timestamp.now()
        ) 