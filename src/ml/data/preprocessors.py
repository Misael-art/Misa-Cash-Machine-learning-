"""
Módulo para pré-processamento de dados financeiros.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
import logging
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

logger = logging.getLogger(__name__)

class DataCleaner:
    """Classe para limpeza e tratamento de dados."""
    
    def __init__(self, data: pd.DataFrame = None):
        self.data = data
        
    def set_data(self, data: pd.DataFrame) -> None:
        """Define o DataFrame a ser processado."""
        self.data = data
        
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """Remove linhas duplicadas do DataFrame."""
        if self.data is None:
            raise ValueError("Nenhum dado foi definido")
            
        original_shape = self.data.shape
        self.data = self.data.drop_duplicates(subset=subset)
        
        if original_shape[0] > self.data.shape[0]:
            logger.info(f"Removidas {original_shape[0] - self.data.shape[0]} linhas duplicadas")
            
        return self.data
        
    def handle_missing_values(self, strategy: Dict[str, str] = None) -> pd.DataFrame:
        """
        Trata valores ausentes no DataFrame.
        
        Args:
            strategy: Dicionário com colunas e estratégias ('mean', 'median', 'mode', 'drop', 'zero')
            
        Returns:
            DataFrame processado
        """
        if self.data is None:
            raise ValueError("Nenhum dado foi definido")
            
        if strategy is None:
            # Estratégia padrão: remover linhas com valores ausentes
            original_shape = self.data.shape
            self.data = self.data.dropna()
            logger.info(f"Removidas {original_shape[0] - self.data.shape[0]} linhas com valores ausentes")
        else:
            for column, method in strategy.items():
                if column not in self.data.columns:
                    logger.warning(f"Coluna {column} não encontrada no DataFrame")
                    continue
                    
                if method == 'drop':
                    self.data = self.data.dropna(subset=[column])
                elif method == 'zero':
                    self.data[column] = self.data[column].fillna(0)
                elif method == 'mean':
                    self.data[column] = self.data[column].fillna(self.data[column].mean())
                elif method == 'median':
                    self.data[column] = self.data[column].fillna(self.data[column].median())
                elif method == 'mode':
                    self.data[column] = self.data[column].fillna(self.data[column].mode()[0])
                else:
                    logger.warning(f"Estratégia '{method}' não reconhecida para coluna {column}")
                    
            logger.info(f"Valores ausentes tratados para {len(strategy)} colunas")
                
        return self.data
        
    def convert_types(self, conversions: Dict[str, str]) -> pd.DataFrame:
        """
        Converte tipos de dados das colunas.
        
        Args:
            conversions: Dicionário com colunas e tipos ('int', 'float', 'str', 'datetime')
            
        Returns:
            DataFrame processado
        """
        if self.data is None:
            raise ValueError("Nenhum dado foi definido")
            
        for column, dtype in conversions.items():
            if column not in self.data.columns:
                logger.warning(f"Coluna {column} não encontrada no DataFrame")
                continue
                
            try:
                if dtype == 'int':
                    self.data[column] = pd.to_numeric(self.data[column], errors='coerce').astype('Int64')
                elif dtype == 'float':
                    self.data[column] = pd.to_numeric(self.data[column], errors='coerce')
                elif dtype == 'str':
                    self.data[column] = self.data[column].astype(str)
                elif dtype == 'datetime':
                    self.data[column] = pd.to_datetime(self.data[column], errors='coerce')
                else:
                    self.data[column] = self.data[column].astype(dtype)
                    
                logger.info(f"Coluna {column} convertida para {dtype}")
                
            except Exception as e:
                logger.error(f"Erro ao converter coluna {column} para {dtype}: {e}")
                
        return self.data
        
    def remove_outliers(self, columns: List[str], method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove valores atípicos (outliers) do DataFrame.
        
        Args:
            columns: Lista de colunas numéricas para verificação
            method: Método para detecção ('iqr' ou 'zscore')
            threshold: Limiar para detecção (1.5 para IQR, 3 para z-score)
            
        Returns:
            DataFrame processado
        """
        if self.data is None:
            raise ValueError("Nenhum dado foi definido")
            
        original_shape = self.data.shape
        
        if method == 'iqr':
            for column in columns:
                if column not in self.data.columns or not pd.api.types.is_numeric_dtype(self.data[column]):
                    logger.warning(f"Coluna {column} não encontrada ou não é numérica")
                    continue
                    
                Q1 = self.data[column].quantile(0.25)
                Q3 = self.data[column].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                self.data = self.data[(self.data[column] >= lower_bound) & (self.data[column] <= upper_bound)]
                
        elif method == 'zscore':
            for column in columns:
                if column not in self.data.columns or not pd.api.types.is_numeric_dtype(self.data[column]):
                    logger.warning(f"Coluna {column} não encontrada ou não é numérica")
                    continue
                    
                z_scores = np.abs((self.data[column] - self.data[column].mean()) / self.data[column].std())
                self.data = self.data[z_scores <= threshold]
                
        else:
            logger.error(f"Método {method} não reconhecido para remoção de outliers")
            return self.data
            
        logger.info(f"Removidas {original_shape[0] - self.data.shape[0]} linhas com outliers")
        return self.data


class FeatureEngineer:
    """Classe para engenharia de features."""
    
    def __init__(self, data: pd.DataFrame = None):
        self.data = data
        self.features_created = []
        
    def set_data(self, data: pd.DataFrame) -> None:
        """Define o DataFrame a ser processado."""
        self.data = data
        
    def extract_datetime_features(self, datetime_column: str) -> pd.DataFrame:
        """
        Extrai features de uma coluna de data/hora.
        
        Args:
            datetime_column: Nome da coluna com dados de data/hora
            
        Returns:
            DataFrame com novas features
        """
        if self.data is None:
            raise ValueError("Nenhum dado foi definido")
            
        if datetime_column not in self.data.columns:
            logger.warning(f"Coluna {datetime_column} não encontrada no DataFrame")
            return self.data
            
        try:
            # Converter para datetime se não for
            if not pd.api.types.is_datetime64_dtype(self.data[datetime_column]):
                self.data[datetime_column] = pd.to_datetime(self.data[datetime_column], errors='coerce')
                
            # Extrair componentes de data/hora
            self.data[f'{datetime_column}_ano'] = self.data[datetime_column].dt.year
            self.data[f'{datetime_column}_mes'] = self.data[datetime_column].dt.month
            self.data[f'{datetime_column}_dia'] = self.data[datetime_column].dt.day
            self.data[f'{datetime_column}_dia_semana'] = self.data[datetime_column].dt.dayofweek
            self.data[f'{datetime_column}_hora'] = self.data[datetime_column].dt.hour
            
            # Atributos adicionais úteis para análise financeira
            self.data[f'{datetime_column}_fim_semana'] = self.data[datetime_column].dt.dayofweek >= 5
            self.data[f'{datetime_column}_fim_mes'] = self.data[datetime_column].dt.is_month_end
            self.data[f'{datetime_column}_trimestre'] = self.data[datetime_column].dt.quarter
            
            logger.info(f"Features de data/hora extraídas da coluna {datetime_column}")
            
            features_created = [
                f'{datetime_column}_ano', f'{datetime_column}_mes', f'{datetime_column}_dia',
                f'{datetime_column}_dia_semana', f'{datetime_column}_hora',
                f'{datetime_column}_fim_semana', f'{datetime_column}_fim_mes',
                f'{datetime_column}_trimestre'
            ]
            self.features_created.extend(features_created)
            
            return self.data
            
        except Exception as e:
            logger.error(f"Erro ao extrair features de data/hora: {e}")
            return self.data
            
    def create_amount_features(self, amount_column: str) -> pd.DataFrame:
        """
        Cria features baseadas em valores monetários.
        
        Args:
            amount_column: Nome da coluna com valores monetários
            
        Returns:
            DataFrame com novas features
        """
        if self.data is None:
            raise ValueError("Nenhum dado foi definido")
            
        if amount_column not in self.data.columns:
            logger.warning(f"Coluna {amount_column} não encontrada no DataFrame")
            return self.data
            
        try:
            # Valor absoluto
            self.data[f'{amount_column}_abs'] = self.data[amount_column].abs()
            
            # Log do valor (para valores positivos)
            mask = self.data[amount_column] > 0
            self.data[f'{amount_column}_log'] = np.nan
            self.data.loc[mask, f'{amount_column}_log'] = np.log1p(self.data.loc[mask, amount_column])
            
            # Categorização de valores
            self.data[f'{amount_column}_categoria'] = pd.cut(
                self.data[f'{amount_column}_abs'],
                bins=[0, 10, 50, 100, 500, 1000, np.inf],
                labels=['muito_pequeno', 'pequeno', 'medio_baixo', 'medio', 'alto', 'muito_alto']
            )
            
            # Indicador de gasto ou receita
            self.data[f'{amount_column}_tipo'] = np.where(self.data[amount_column] >= 0, 'receita', 'despesa')
            
            logger.info(f"Features de valor monetário criadas a partir da coluna {amount_column}")
            
            features_created = [
                f'{amount_column}_abs', f'{amount_column}_log',
                f'{amount_column}_categoria', f'{amount_column}_tipo'
            ]
            self.features_created.extend(features_created)
            
            return self.data
            
        except Exception as e:
            logger.error(f"Erro ao criar features de valor monetário: {e}")
            return self.data
            
    def aggregate_by_category(self, amount_column: str, category_column: str) -> pd.DataFrame:
        """
        Cria agregações por categoria.
        
        Args:
            amount_column: Nome da coluna com valores monetários
            category_column: Nome da coluna de categoria
            
        Returns:
            DataFrame com novas features
        """
        if self.data is None:
            raise ValueError("Nenhum dado foi definido")
            
        if amount_column not in self.data.columns or category_column not in self.data.columns:
            logger.warning(f"Colunas {amount_column} ou {category_column} não encontradas")
            return self.data
            
        try:
            # Calcular agregações por categoria
            aggs = self.data.groupby(category_column)[amount_column].agg(['mean', 'sum', 'count', 'std'])
            aggs.columns = [f'{category_column}_{amount_column}_{agg}' for agg in aggs.columns]
            
            # Juntar com o DataFrame original
            self.data = self.data.join(aggs, on=category_column)
            
            logger.info(f"Agregações criadas para {category_column} x {amount_column}")
            
            self.features_created.extend(aggs.columns.tolist())
            
            return self.data
            
        except Exception as e:
            logger.error(f"Erro ao criar agregações por categoria: {e}")
            return self.data


class DataTransformer:
    """Classe para transformação de dados para modelos ML."""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        
    def scale_features(self, data: pd.DataFrame, columns: List[str], 
                      method: str = 'standard', fit: bool = True) -> pd.DataFrame:
        """
        Escala features numéricas.
        
        Args:
            data: DataFrame com os dados
            columns: Lista de colunas para escalar
            method: Método de escala ('standard' ou 'minmax')
            fit: Se deve ajustar ou apenas transformar
            
        Returns:
            DataFrame com colunas escaladas
        """
        result = data.copy()
        
        for col in columns:
            if col not in data.columns:
                logger.warning(f"Coluna {col} não encontrada no DataFrame")
                continue
                
            scaler_key = f"{method}_{col}"
            
            if fit:
                if method == 'standard':
                    self.scalers[scaler_key] = StandardScaler()
                elif method == 'minmax':
                    self.scalers[scaler_key] = MinMaxScaler()
                else:
                    raise ValueError(f"Método de escala '{method}' não reconhecido")
                    
                # Reshape para formato esperado pelo scaler
                result[col] = self.scalers[scaler_key].fit_transform(
                    data[col].values.reshape(-1, 1)
                ).flatten()
            else:
                if scaler_key not in self.scalers:
                    raise ValueError(f"Scaler para {col} com método {method} não encontrado")
                    
                result[col] = self.scalers[scaler_key].transform(
                    data[col].values.reshape(-1, 1)
                ).flatten()
                
        return result
        
    def encode_categorical(self, data: pd.DataFrame, columns: List[str], 
                          method: str = 'onehot', fit: bool = True) -> pd.DataFrame:
        """
        Codifica variáveis categóricas.
        
        Args:
            data: DataFrame com os dados
            columns: Lista de colunas para codificar
            method: Método de codificação ('onehot', 'label', 'ordinal')
            fit: Se deve ajustar ou apenas transformar
            
        Returns:
            DataFrame com colunas codificadas
        """
        result = data.copy()
        
        if method == 'onehot':
            for col in columns:
                if col not in data.columns:
                    logger.warning(f"Coluna {col} não encontrada no DataFrame")
                    continue
                    
                encoder_key = f"onehot_{col}"
                
                if fit:
                    self.encoders[encoder_key] = OneHotEncoder(sparse=False, handle_unknown='ignore')
                    encoded = self.encoders[encoder_key].fit_transform(data[col].values.reshape(-1, 1))
                    
                    categories = self.encoders[encoder_key].categories_[0]
                    encoded_cols = [f"{col}_{cat}" for cat in categories]
                    
                    for i, encoded_col in enumerate(encoded_cols):
                        result[encoded_col] = encoded[:, i]
                        
                    # Remover coluna original
                    result = result.drop(col, axis=1)
                else:
                    if encoder_key not in self.encoders:
                        raise ValueError(f"Encoder para {col} não encontrado")
                        
                    encoded = self.encoders[encoder_key].transform(data[col].values.reshape(-1, 1))
                    
                    categories = self.encoders[encoder_key].categories_[0]
                    encoded_cols = [f"{col}_{cat}" for cat in categories]
                    
                    for i, encoded_col in enumerate(encoded_cols):
                        result[encoded_col] = encoded[:, i]
                        
                    # Remover coluna original
                    result = result.drop(col, axis=1)
                    
        elif method == 'label':
            from sklearn.preprocessing import LabelEncoder
            
            for col in columns:
                if col not in data.columns:
                    logger.warning(f"Coluna {col} não encontrada no DataFrame")
                    continue
                    
                encoder_key = f"label_{col}"
                
                if fit:
                    self.encoders[encoder_key] = LabelEncoder()
                    result[col] = self.encoders[encoder_key].fit_transform(data[col])
                else:
                    if encoder_key not in self.encoders:
                        raise ValueError(f"Encoder para {col} não encontrado")
                        
                    result[col] = self.encoders[encoder_key].transform(data[col])
                    
        else:
            raise ValueError(f"Método de codificação '{method}' não reconhecido")
            
        return result
        
    def prepare_data_for_ml(self, data: pd.DataFrame, 
                           numeric_cols: List[str], 
                           categorical_cols: List[str],
                           target_col: str = None) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """
        Prepara dados para treinamento ou previsão de modelos ML.
        
        Args:
            data: DataFrame com os dados
            numeric_cols: Lista de colunas numéricas
            categorical_cols: Lista de colunas categóricas
            target_col: Coluna alvo (opcional)
            
        Returns:
            DataFrame processado e Series com alvo (se fornecido)
        """
        # Processar colunas numéricas
        processed_data = self.scale_features(data, numeric_cols)
        
        # Processar colunas categóricas
        processed_data = self.encode_categorical(processed_data, categorical_cols)
        
        # Separar target se fornecido
        target = None
        if target_col is not None and target_col in data.columns:
            target = data[target_col]
            if target_col in processed_data.columns:
                processed_data = processed_data.drop(target_col, axis=1)
                
        return processed_data, target 