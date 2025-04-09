from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from ..validation.schema import DataValidator
from ..validation.anomaly_detector import AnomalyDetector, AnomalyConfig
from ..collectors import YFinanceCollector
from ..utils.logger import get_logger

logger = get_logger(__name__)

def print_validation_results(symbol: str, validation_result, anomaly_result):
    """
    Imprime resultados da validação de forma formatada.
    
    Args:
        symbol (str): Símbolo do ativo
        validation_result: Resultado da validação
        anomaly_result: Resultado da detecção de anomalias
    """
    print(f"\n=== Resultados de Validação para {symbol} ===")
    
    # Resultado da validação básica
    print("\nValidação Básica:")
    print(f"Status: {'Válido' if validation_result.is_valid else 'Inválido'}")
    
    if validation_result.errors:
        print("\nErros encontrados:")
        for error in validation_result.errors:
            print(f"- {error['message']}")
            
    if validation_result.warnings:
        print("\nAvisos:")
        for warning in validation_result.warnings:
            print(f"- {warning['message']}")
    
    # Estatísticas básicas
    stats = validation_result.stats
    print("\nEstatísticas:")
    print(f"Total de registros: {stats['total_rows']}")
    print("\nPreços:")
    print(f"- Média: {stats['price_stats']['mean']:.2f}")
    print(f"- Desvio Padrão: {stats['price_stats']['std']:.2f}")
    print(f"- Min: {stats['price_stats']['min']:.2f}")
    print(f"- Max: {stats['price_stats']['max']:.2f}")
    
    # Resultado das anomalias
    print("\nDetecção de Anomalias:")
    print(f"Total de anomalias: {anomaly_result.stats['total_anomalies']}")
    print(f"- Anomalias de preço: {anomaly_result.stats['price_anomalies']}")
    print(f"- Anomalias de volume: {anomaly_result.stats['volume_anomalies']}")
    print(f"- Anomalias de padrão: {anomaly_result.stats['pattern_anomalies']}")
    
    if anomaly_result.anomalies:
        print("\nDetalhes das Anomalias:")
        for anomaly in anomaly_result.anomalies[:5]:  # Mostrar apenas as 5 primeiras
            print(f"\nTipo: {anomaly['type']}")
            print(f"Data: {anomaly['timestamp']}")
            if 'value' in anomaly:
                print(f"Valor: {anomaly['value']:.2f}")
            if 'z_score' in anomaly:
                print(f"Z-Score: {anomaly['z_score']:.2f}")

def test_data_validation():
    """Testa o sistema de validação de dados."""
    logger.info("Iniciando teste de validação de dados")
    
    # Configurar coletor
    collector = YFinanceCollector()
    
    # Configurar validador e detector
    validator = DataValidator()
    detector = AnomalyDetector(
        config=AnomalyConfig(
            price_std_threshold=3.0,
            volume_std_threshold=4.0,
            price_jump_threshold=0.1,
            volume_jump_threshold=2.0
        )
    )
    
    # Definir período de análise
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # 3 meses de dados
    
    # Lista de símbolos para teste
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    for symbol in symbols:
        logger.info(f"Analisando dados de {symbol}")
        
        try:
            # Coletar dados
            df = collector.get_daily_data(symbol, start_date, end_date)
            
            if df is not None and not df.empty:
                # Validação básica
                validation_result = validator.validate_dataframe(df)
                
                # Detecção de anomalias
                anomaly_result = detector.detect(df)
                
                # Imprimir resultados
                print_validation_results(symbol, validation_result, anomaly_result)
                
            else:
                logger.warning(f"Nenhum dado encontrado para {symbol}")
                
        except Exception as e:
            logger.error(f"Erro ao processar {symbol}: {str(e)}")

def test_synthetic_data():
    """Testa o sistema com dados sintéticos."""
    logger.info("Iniciando teste com dados sintéticos")
    
    # Criar dados sintéticos com anomalias
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    n = len(dates)
    
    # Dados base
    base_price = 100
    trend = np.linspace(0, 20, n)  # Tendência de alta
    noise = np.random.normal(0, 1, n)  # Ruído gaussiano
    
    df = pd.DataFrame({
        'open': base_price + trend + noise,
        'close': base_price + trend + np.random.normal(0, 1, n),
        'high': base_price + trend + np.abs(np.random.normal(0, 2, n)),
        'low': base_price + trend - np.abs(np.random.normal(0, 2, n)),
        'volume': np.random.normal(1000000, 100000, n)
    }, index=dates)
    
    # Adicionar algumas anomalias
    # Spike de preço
    spike_idx = np.random.randint(0, n, 3)
    df.loc[df.index[spike_idx], 'close'] *= 1.5
    
    # Volume anormal
    volume_spike_idx = np.random.randint(0, n, 3)
    df.loc[df.index[volume_spike_idx], 'volume'] *= 3
    
    # Validar dados sintéticos
    validator = DataValidator()
    detector = AnomalyDetector()
    
    validation_result = validator.validate_dataframe(df)
    anomaly_result = detector.detect(df)
    
    print_validation_results('SYNTHETIC', validation_result, anomaly_result)

def main():
    """Função principal."""
    try:
        # Testar com dados reais
        test_data_validation()
        
        # Testar com dados sintéticos
        test_synthetic_data()
        
    except Exception as e:
        logger.error(f"Erro durante os testes: {str(e)}")
        raise

if __name__ == "__main__":
    main() 