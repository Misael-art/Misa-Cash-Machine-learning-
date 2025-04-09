"""
Módulo para coleta de dados de transações financeiras.
"""
import pandas as pd
from typing import Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

class DataCollector:
    """Classe base para coletar dados de diferentes fontes."""
    
    def __init__(self):
        self.data = None
        
    def collect(self) -> pd.DataFrame:
        """Método base para coleta de dados."""
        raise NotImplementedError("Método deve ser implementado pelas subclasses")
    
    def save_to_csv(self, filepath: str) -> None:
        """Salva dados coletados em um arquivo CSV."""
        if self.data is None:
            raise ValueError("Nenhum dado foi coletado ainda")
        self.data.to_csv(filepath, index=False)
        logger.info(f"Dados salvos em {filepath}")


class DatabaseCollector(DataCollector):
    """Coleta dados do banco de dados da aplicação."""
    
    def __init__(self, connection_string: str):
        super().__init__()
        self.connection_string = connection_string
        
    def collect(self, query: str = None, table: str = None) -> pd.DataFrame:
        """
        Coleta dados do banco de dados usando uma query SQL ou tabela.
        
        Args:
            query: Query SQL para execução (opcional)
            table: Nome da tabela para seleção (se query não for fornecida)
            
        Returns:
            DataFrame com os dados coletados
        """
        try:
            if query:
                self.data = pd.read_sql(query, self.connection_string)
            elif table:
                self.data = pd.read_sql(f"SELECT * FROM {table}", self.connection_string)
            else:
                raise ValueError("É necessário fornecer uma query ou nome de tabela")
                
            logger.info(f"Coletados {len(self.data)} registros")
            return self.data
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados: {e}")
            raise


class ApiCollector(DataCollector):
    """Coleta dados da API da aplicação."""
    
    def __init__(self, api_url: str, auth_token: Optional[str] = None):
        super().__init__()
        self.api_url = api_url
        self.auth_token = auth_token
        self.headers = {}
        
        if auth_token:
            self.headers['Authorization'] = f"Bearer {auth_token}"
    
    def collect(self, endpoint: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Coleta dados de um endpoint da API.
        
        Args:
            endpoint: Endpoint da API para coleta
            params: Parâmetros para requisição (opcional)
            
        Returns:
            DataFrame com os dados coletados
        """
        import requests
        
        try:
            url = f"{self.api_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Se a resposta for uma lista de dicionários, converte diretamente para DataFrame
            if isinstance(data, list):
                self.data = pd.DataFrame(data)
            # Se for um dicionário com uma chave de dados (comum em APIs paginadas)
            elif isinstance(data, dict) and any(key in data for key in ['data', 'results', 'items']):
                for key in ['data', 'results', 'items']:
                    if key in data:
                        self.data = pd.DataFrame(data[key])
                        break
            else:
                self.data = pd.DataFrame([data])
                
            logger.info(f"Coletados {len(self.data)} registros da API")
            return self.data
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados da API: {e}")
            raise 