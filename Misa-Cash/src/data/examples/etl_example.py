from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from ..etl.pipeline import ETLPipeline, ETLConfig
from ..collectors import YFinanceCollector, AlphaVantageCollector
from ..validation import DataValidator, AnomalyDetector
import logging
from ..utils.logger import get_logger

logger = get_logger(__name__)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza os nomes das colunas e formatos dos dados."""
    df = df.copy()
    
    # Padronizar nomes de colunas
    column_mapping = {
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume',
        'Adj Close': 'adj_close'
    }
    df = df.rename(columns=column_mapping)
    
    # Garantir que o índice é datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    return df

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona indicadores técnicos básicos."""
    df = df.copy()
    
    # Médias móveis
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    # Volatilidade
    df['daily_return'] = df['close'].pct_change()
    df['volatility'] = df['daily_return'].rolling(window=20).std()
    
    # Volume médio
    df['volume_sma_20'] = df['volume'].rolling(window=20).mean()
    
    return df

def save_to_csv(df: pd.DataFrame) -> bool:
    """Função de exemplo para salvar dados em CSV."""
    try:
        symbol = df.index.name or 'unknown'
        filename = f"data/processed/{symbol}_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename)
        logger.info(f"Dados salvos em {filename}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar CSV: {str(e)}")
        return False

def test_yfinance_pipeline():
    """Testa a pipeline ETL com dados do Yahoo Finance."""
    # Configurar pipeline
    config = ETLConfig(
        max_workers=4,
        batch_size=5,
        validate_data=True,
        detect_anomalies=True
    )
    pipeline = ETLPipeline(config)
    
    # Adicionar transformações
    pipeline.add_transformer(normalize_columns)
    pipeline.add_transformer(add_technical_indicators)
    
    # Preparar parâmetros para extração
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    batch_params = [
        {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'interval': '1d'
        }
        for symbol in symbols
    ]
    
    # Criar coletor
    collector = YFinanceCollector()
    
    # Executar pipeline
    logger.info("Iniciando pipeline com Yahoo Finance")
    stats = pipeline.process(
        extractor=collector.get_daily_data,
        loader=save_to_csv,
        batch_params=batch_params
    )
    
    return stats

def test_alphavantage_pipeline():
    """Testa a pipeline ETL com dados do Alpha Vantage."""
    # Configurar pipeline
    config = ETLConfig(
        max_workers=2,  # Limitado devido à API
        batch_size=2,
        validate_data=True,
        detect_anomalies=True
    )
    pipeline = ETLPipeline(config)
    
    # Adicionar transformações
    pipeline.add_transformer(normalize_columns)
    pipeline.add_transformer(add_technical_indicators)
    
    # Preparar parâmetros para extração
    symbols = ['IBM', 'TSLA']  # Limitado para exemplo
    
    batch_params = [
        {'symbol': symbol, 'outputsize': 'full'}
        for symbol in symbols
    ]
    
    # Criar coletor
    collector = AlphaVantageCollector()
    
    # Executar pipeline
    logger.info("Iniciando pipeline com Alpha Vantage")
    stats = pipeline.process(
        extractor=collector.get_daily_data,
        loader=save_to_csv,
        batch_params=batch_params
    )
    
    return stats

def main():
    """Função principal para testar a pipeline ETL."""
    logger.info("Iniciando testes da pipeline ETL")
    
    try:
        # Testar com Yahoo Finance
        yf_stats = test_yfinance_pipeline()
        logger.info("Estatísticas Yahoo Finance:")
        logger.info(f"- Taxa de sucesso: {yf_stats['success_rate']:.2%}")
        logger.info(f"- Items processados: {yf_stats['processed_items']}")
        
        # Testar com Alpha Vantage
        av_stats = test_alphavantage_pipeline()
        logger.info("Estatísticas Alpha Vantage:")
        logger.info(f"- Taxa de sucesso: {av_stats['success_rate']:.2%}")
        logger.info(f"- Items processados: {av_stats['processed_items']}")
        
    except Exception as e:
        logger.error(f"Erro nos testes: {str(e)}")
        raise

if __name__ == "__main__":
    main() 