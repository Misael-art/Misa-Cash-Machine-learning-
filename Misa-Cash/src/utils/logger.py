import logging
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger.
    
    Args:
        name (str): Nome do logger
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Criar diretório de logs se não existir
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # Configurar logger
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Evitar handlers duplicados
        logger.setLevel(logging.INFO)
        
        # Handler para arquivo
        log_file = os.path.join(log_dir, f'data_collector_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adicionar handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger 