from datetime import datetime, timedelta
from ..collectors import CollectorFactory
from ...utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Exemplo de uso dos coletores de dados."""
    
    # Configurar período de dados
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Exemplo com Alpha Vantage
    try:
        logger.info("Testando Alpha Vantage collector...")
        av_collector = CollectorFactory.create_collector('alpha_vantage')
        
        if av_collector.check_health():
            # Obter dados diários
            aapl_daily = av_collector.get_daily_data(
                'AAPL',
                start_date=start_date,
                end_date=end_date
            )
            logger.info(f"Dados diários AAPL (Alpha Vantage):\n{aapl_daily.head()}")
            
            # Obter dados intraday
            aapl_intraday = av_collector.get_intraday_data(
                'AAPL',
                interval='5min',
                limit=10
            )
            logger.info(f"Dados intraday AAPL (Alpha Vantage):\n{aapl_intraday.head()}")
    except Exception as e:
        logger.error(f"Erro com Alpha Vantage collector: {str(e)}")
    
    # Exemplo com Yahoo Finance
    try:
        logger.info("\nTestando Yahoo Finance collector...")
        yf_collector = CollectorFactory.create_collector('yfinance')
        
        if yf_collector.check_health():
            # Obter dados diários
            googl_daily = yf_collector.get_daily_data(
                'GOOGL',
                start_date=start_date,
                end_date=end_date
            )
            logger.info(f"Dados diários GOOGL (Yahoo Finance):\n{googl_daily.head()}")
            
            # Obter dados intraday
            googl_intraday = yf_collector.get_intraday_data(
                'GOOGL',
                interval='5min',
                limit=10
            )
            logger.info(f"Dados intraday GOOGL (Yahoo Finance):\n{googl_intraday.head()}")
            
            # Obter lista de símbolos
            symbols = yf_collector.get_symbols_list()
            logger.info(f"Símbolos disponíveis (Yahoo Finance): {symbols}")
    except Exception as e:
        logger.error(f"Erro com Yahoo Finance collector: {str(e)}")

if __name__ == '__main__':
    main() 