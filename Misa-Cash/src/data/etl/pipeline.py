from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import logging
from ..utils.logger import get_logger
from ..validation import DataValidator, AnomalyDetector
from ..cache import RedisCache

logger = get_logger(__name__)

@dataclass
class ETLConfig:
    """Configuração para pipeline ETL."""
    
    max_workers: int = 4  # Número máximo de workers para paralelização
    batch_size: int = 1000  # Tamanho do lote para processamento
    retry_attempts: int = 3  # Número de tentativas para operações
    cache_enabled: bool = True  # Se o cache deve ser usado
    validate_data: bool = True  # Se a validação deve ser executada
    detect_anomalies: bool = True  # Se a detecção de anomalias deve ser executada

class ETLPipeline:
    """Pipeline ETL para processamento de dados financeiros."""
    
    def __init__(self, config: Optional[ETLConfig] = None):
        """
        Inicializa a pipeline ETL.
        
        Args:
            config (ETLConfig, opcional): Configuração da pipeline
        """
        self.config = config or ETLConfig()
        self.validator = DataValidator()
        self.anomaly_detector = AnomalyDetector()
        self.cache = RedisCache() if self.config.cache_enabled else None
        self.transformers: List[Callable] = []
        
    def add_transformer(self, func: Callable[[pd.DataFrame], pd.DataFrame]) -> None:
        """
        Adiciona uma função de transformação à pipeline.
        
        Args:
            func (Callable): Função que recebe e retorna um DataFrame
        """
        self.transformers.append(func)
        
    def _extract_batch(
        self,
        extractor: Callable,
        batch_params: List[Dict[str, Any]]
    ) -> List[pd.DataFrame]:
        """
        Extrai um lote de dados em paralelo.
        
        Args:
            extractor (Callable): Função de extração
            batch_params (List[Dict]): Parâmetros para cada extração
            
        Returns:
            List[pd.DataFrame]: Dados extraídos
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = [
                executor.submit(extractor, **params)
                for params in batch_params
            ]
            
            for future in as_completed(futures):
                try:
                    data = future.result()
                    if data is not None and not data.empty:
                        results.append(data)
                except Exception as e:
                    logger.error(f"Erro na extração: {str(e)}")
                    
        return results
    
    def _transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica todas as transformações aos dados.
        
        Args:
            df (pd.DataFrame): Dados para transformar
            
        Returns:
            pd.DataFrame: Dados transformados
        """
        transformed = df.copy()
        
        for transformer in self.transformers:
            try:
                transformed = transformer(transformed)
            except Exception as e:
                logger.error(f"Erro na transformação: {str(e)}")
                raise
                
        return transformed
    
    def _validate_data(self, df: pd.DataFrame) -> bool:
        """
        Valida os dados e detecta anomalias.
        
        Args:
            df (pd.DataFrame): Dados para validar
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if self.config.validate_data:
            validation_result = self.validator.validate_dataframe(df)
            if not validation_result.is_valid:
                logger.warning("Validação falhou:")
                for error in validation_result.errors:
                    logger.warning(f"- {error['message']}")
                return False
            
        if self.config.detect_anomalies:
            anomaly_result = self.anomaly_detector.detect(df)
            if anomaly_result.stats['total_anomalies'] > 0:
                logger.info(f"Anomalias detectadas: {anomaly_result.stats['total_anomalies']}")
                
        return True
    
    def _load_data(
        self,
        df: pd.DataFrame,
        loader: Callable[[pd.DataFrame], bool],
        retry: int = 0
    ) -> bool:
        """
        Carrega os dados com retry em caso de falha.
        
        Args:
            df (pd.DataFrame): Dados para carregar
            loader (Callable): Função de carregamento
            retry (int): Tentativa atual
            
        Returns:
            bool: True se sucesso, False caso contrário
        """
        try:
            return loader(df)
        except Exception as e:
            if retry < self.config.retry_attempts:
                logger.warning(f"Erro no carregamento, tentativa {retry + 1}: {str(e)}")
                return self._load_data(df, loader, retry + 1)
            else:
                logger.error(f"Falha no carregamento após {self.config.retry_attempts} tentativas")
                return False
    
    def process(
        self,
        extractor: Callable,
        loader: Callable[[pd.DataFrame], bool],
        batch_params: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Executa a pipeline ETL completa.
        
        Args:
            extractor (Callable): Função de extração
            loader (Callable): Função de carregamento
            batch_params (List[Dict]): Parâmetros para extração
            
        Returns:
            Dict[str, Any]: Estatísticas do processamento
        """
        start_time = datetime.now()
        stats = {
            'total_batches': 0,
            'processed_items': 0,
            'failed_items': 0,
            'validation_failures': 0,
            'load_failures': 0
        }
        
        # Processar em lotes
        for i in range(0, len(batch_params), self.config.batch_size):
            batch = batch_params[i:i + self.config.batch_size]
            stats['total_batches'] += 1
            
            try:
                # Extração
                logger.info(f"Processando lote {stats['total_batches']}")
                extracted_data = self._extract_batch(extractor, batch)
                
                # Processamento de cada item do lote
                for df in extracted_data:
                    try:
                        # Transformação
                        transformed_df = self._transform_data(df)
                        
                        # Validação
                        if self._validate_data(transformed_df):
                            # Carregamento
                            if self._load_data(transformed_df, loader):
                                stats['processed_items'] += 1
                            else:
                                stats['load_failures'] += 1
                        else:
                            stats['validation_failures'] += 1
                            
                    except Exception as e:
                        logger.error(f"Erro no processamento: {str(e)}")
                        stats['failed_items'] += 1
                        
            except Exception as e:
                logger.error(f"Erro no lote {stats['total_batches']}: {str(e)}")
                stats['failed_items'] += len(batch)
                
        # Calcular estatísticas finais
        end_time = datetime.now()
        stats['duration'] = (end_time - start_time).total_seconds()
        stats['success_rate'] = (
            stats['processed_items'] / 
            (stats['processed_items'] + stats['failed_items'])
            if (stats['processed_items'] + stats['failed_items']) > 0
            else 0
        )
        
        logger.info("Pipeline ETL concluída:")
        logger.info(f"- Tempo total: {stats['duration']:.2f} segundos")
        logger.info(f"- Taxa de sucesso: {stats['success_rate']:.2%}")
        logger.info(f"- Items processados: {stats['processed_items']}")
        logger.info(f"- Falhas: {stats['failed_items']}")
        
        return stats 