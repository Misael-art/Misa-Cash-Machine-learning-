"""Módulo para processamento de dados para os modelos de Machine Learning.

Este módulo fornece funcionalidades para preparação, limpeza, 
transformação e validação de dados para uso nos modelos de ML.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
from datetime import datetime, timedelta
import logging

# Configuração de logging
logger = logging.getLogger(__name__)


class DataProcessor:
    """Classe para processamento de dados financeiros para ML.
    
    Responsável por transformar dados brutos em formato adequado
    para treinamento e inferência dos modelos de ML.
    """
    
    def __init__(self):
        """Inicializa o processador de dados."""
        self.categorical_columns = ['categoria', 'tipo']
        self.numerical_columns = ['valor']
        self.datetime_columns = ['data']
        self.text_columns = ['descricao']
    
    def validate_data(self, data: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Valida se o DataFrame contém as colunas necessárias.
        
        Args:
            data: DataFrame a ser validado.
            
        Returns:
            Tupla com booleano indicando se é válido e lista de erros.
        """
        errors = []
        required_columns = ['data', 'valor']
        
        for col in required_columns:
            if col not in data.columns:
                errors.append(f"Coluna obrigatória ausente: {col}")
        
        # Verifica tipos de dados
        if 'data' in data.columns and not pd.api.types.is_datetime64_any_dtype(data['data']):
            try:
                pd.to_datetime(data['data'])
            except:
                errors.append("Coluna 'data' não pode ser convertida para datetime")
        
        if 'valor' in data.columns:
            try:
                pd.to_numeric(data['valor'])
            except:
                errors.append("Coluna 'valor' não pode ser convertida para numérico")
        
        return len(errors) == 0, errors
    
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Limpa o DataFrame, tratando valores ausentes e formatando dados.
        
        Args:
            data: DataFrame a ser limpo.
            
        Returns:
            DataFrame limpo.
        """
        logger.info(f"Limpando dados: {len(data)} linhas iniciais")
        
        # Cria uma cópia para não modificar o original
        df = data.copy()
        
        # Converte colunas de datas
        for col in self.datetime_columns:
            if col in df.columns and not pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Converte colunas numéricas
        for col in self.numerical_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Trata valores ausentes
        for col in self.numerical_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Remove linhas com data ausente
        if 'data' in df.columns:
            df = df.dropna(subset=['data'])
        
        # Converte categorias para minúsculas
        for col in self.categorical_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower()
        
        # Limpa espaços em excesso em textos
        for col in self.text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        logger.info(f"Dados limpos: {len(df)} linhas finais")
        return df
    
    def prepare_expense_prediction_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepara dados para o modelo de previsão de gastos.
        
        Args:
            data: DataFrame com dados brutos.
            
        Returns:
            DataFrame com dados agregados por mês para previsão.
        """
        logger.info("Preparando dados para previsão de gastos")
        
        # Valida e limpa os dados
        is_valid, errors = self.validate_data(data)
        if not is_valid:
            error_msg = "; ".join(errors)
            logger.error(f"Dados inválidos: {error_msg}")
            raise ValueError(f"Dados inválidos: {error_msg}")
        
        df = self.clean_data(data)
        
        # Agrega os gastos por mês
        df['mes'] = df['data'].dt.to_period('M')
        
        # Seleciona gastos (valores negativos)
        df_gastos = df[df['valor'] < 0].copy()
        df_gastos['valor'] = df_gastos['valor'].abs()
        
        # Agrega por mês
        monthly_data = df_gastos.groupby('mes')['valor'].sum().reset_index()
        monthly_data['mes'] = monthly_data['mes'].dt.to_timestamp()
        
        # Ordena por data
        monthly_data = monthly_data.sort_values('mes')
        
        # Adiciona características temporais
        monthly_data['mes_do_ano'] = monthly_data['mes'].dt.month
        monthly_data['ano'] = monthly_data['mes'].dt.year
        
        # Preenche meses faltantes se houver mais de 6 meses de dados
        if len(monthly_data) > 6:
            min_date = monthly_data['mes'].min()
            max_date = monthly_data['mes'].max()
            all_months = pd.date_range(start=min_date, end=max_date, freq='MS')
            
            # Cria um DataFrame com todos os meses
            full_range = pd.DataFrame({'mes': all_months})
            
            # Mescla com os dados reais
            monthly_data = pd.merge(full_range, monthly_data, on='mes', how='left')
            
            # Preenche valores ausentes com a média
            monthly_data['valor'] = monthly_data['valor'].fillna(monthly_data['valor'].mean())
            
            # Recalcula as características temporais
            monthly_data['mes_do_ano'] = monthly_data['mes'].dt.month
            monthly_data['ano'] = monthly_data['mes'].dt.year
        
        logger.info(f"Dados preparados para previsão: {len(monthly_data)} meses")
        return monthly_data
    
    def prepare_anomaly_detection_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepara dados para o modelo de detecção de anomalias.
        
        Args:
            data: DataFrame com dados brutos.
            
        Returns:
            DataFrame com features para detecção de anomalias.
        """
        logger.info("Preparando dados para detecção de anomalias")
        
        # Valida e limpa os dados
        is_valid, errors = self.validate_data(data)
        if not is_valid:
            error_msg = "; ".join(errors)
            logger.error(f"Dados inválidos: {error_msg}")
            raise ValueError(f"Dados inválidos: {error_msg}")
        
        df = self.clean_data(data)
        
        # Extrai features relevantes para anomalias
        
        # 1. Valor absoluto da transação
        df['valor_abs'] = df['valor'].abs()
        
        # 2. Dia do mês
        df['dia_do_mes'] = df['data'].dt.day
        
        # 3. Dia da semana (0 = segunda, 6 = domingo)
        df['dia_da_semana'] = df['data'].dt.dayofweek
        
        # 4. Mês do ano
        df['mes_do_ano'] = df['data'].dt.month
        
        # 5. Categorias codificadas se disponível
        if 'categoria' in df.columns:
            # One-hot encoding para categorias
            categories = pd.get_dummies(df['categoria'], prefix='cat')
            df = pd.concat([df, categories], axis=1)
        
        # 6. Flag para fins de semana
        df['fim_de_semana'] = df['dia_da_semana'].isin([5, 6]).astype(int)
        
        # 7. Estatísticas por categoria se disponível
        if 'categoria' in df.columns:
            # Valor médio por categoria
            category_means = df.groupby('categoria')['valor_abs'].mean()
            df['cat_valor_medio'] = df['categoria'].map(category_means)
            
            # Desvio do valor médio da categoria
            df['desvio_categoria'] = df['valor_abs'] - df['cat_valor_medio']
        
        # Remove colunas não numéricas para o modelo
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Garante que não há valores ausentes
        numeric_df = numeric_df.fillna(0)
        
        logger.info(f"Dados preparados para anomalias: {len(numeric_df)} linhas, {numeric_df.shape[1]} features")
        
        # Para debug: mostra as primeiras 5 linhas com as novas features
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Exemplo de features: {numeric_df.head(5).to_dict()}")
        
        return numeric_df
    
    def prepare_category_classification_data(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Prepara dados para o modelo de classificação de categorias.
        
        Args:
            data: DataFrame com dados brutos.
            
        Returns:
            Tupla com DataFrame processado e lista de categorias únicas.
        """
        logger.info("Preparando dados para classificação de categorias")
        
        # Verifica se existem as colunas necessárias
        if 'descricao' not in data.columns or 'categoria' not in data.columns:
            error_msg = "Dados devem conter as colunas 'descricao' e 'categoria'"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        df = data.copy()
        
        # Limpa as descrições
        df['descricao'] = df['descricao'].astype(str).str.lower().str.strip()
        
        # Limpa as categorias
        df['categoria'] = df['categoria'].astype(str).str.lower().str.strip()
        
        # Remove linhas com descrições ou categorias vazias
        df = df[df['descricao'].str.len() > 0]
        df = df[df['categoria'].str.len() > 0]
        
        # Lista de categorias únicas
        unique_categories = df['categoria'].unique().tolist()
        
        # Seleciona apenas as colunas relevantes
        result_df = df[['descricao', 'categoria']]
        
        logger.info(f"Dados preparados para classificação: {len(result_df)} linhas, {len(unique_categories)} categorias")
        
        return result_df, unique_categories
    
    def split_time_series_data(self, data: pd.DataFrame, 
                              test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Divide dados temporais em conjuntos de treino e teste.
        
        Args:
            data: DataFrame com dados temporais ordenados.
            test_size: Proporção para o conjunto de teste.
            
        Returns:
            Tupla com DataFrames de treino e teste.
        """
        n = len(data)
        train_size = int(n * (1 - test_size))
        
        train_data = data.iloc[:train_size].copy()
        test_data = data.iloc[train_size:].copy()
        
        logger.info(f"Divisão de dados: {len(train_data)} treino, {len(test_data)} teste")
        
        return train_data, test_data
    
    def normalize_data(self, train_data: pd.DataFrame, 
                      test_data: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
        """Normaliza dados numéricos usando min-max scaling.
        
        Args:
            train_data: DataFrame com dados de treinamento.
            test_data: DataFrame opcional com dados de teste.
            
        Returns:
            Tupla com dados normalizados e parâmetros de normalização.
        """
        # Identifica colunas numéricas
        numeric_cols = train_data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Inicializa dicionário para armazenar parâmetros
        params = {}
        
        # Cria cópias para não modificar os originais
        train_normalized = train_data.copy()
        test_normalized = test_data.copy() if test_data is not None else None
        
        # Normaliza cada coluna numérica
        for col in numeric_cols:
            min_val = train_data[col].min()
            max_val = train_data[col].max()
            
            # Evita divisão por zero
            if max_val == min_val:
                continue
            
            # Armazena parâmetros
            params[col] = {'min': min_val, 'max': max_val}
            
            # Normaliza dados de treino
            train_normalized[col] = (train_data[col] - min_val) / (max_val - min_val)
            
            # Normaliza dados de teste se fornecidos
            if test_normalized is not None:
                test_normalized[col] = (test_data[col] - min_val) / (max_val - min_val)
                
                # Garante que valores fora do intervalo sejam limitados a [0,1]
                test_normalized[col] = test_normalized[col].clip(0, 1)
        
        if test_normalized is not None:
            return train_normalized, test_normalized, params
        else:
            return train_normalized, None, params
    
    def add_temporal_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Adiciona características temporais ao DataFrame.
        
        Args:
            data: DataFrame com coluna de data.
            
        Returns:
            DataFrame com características temporais adicionadas.
        """
        if 'data' not in data.columns:
            raise ValueError("DataFrame deve conter a coluna 'data'")
        
        # Cria cópia para não modificar o original
        df = data.copy()
        
        # Garante que a coluna data é datetime
        if not pd.api.types.is_datetime64_any_dtype(df['data']):
            df['data'] = pd.to_datetime(df['data'])
        
        # Adiciona features temporais
        df['dia_do_mes'] = df['data'].dt.day
        df['mes_do_ano'] = df['data'].dt.month
        df['dia_da_semana'] = df['data'].dt.dayofweek
        df['fim_de_semana'] = df['dia_da_semana'].isin([5, 6]).astype(int)
        df['trimestre'] = df['data'].dt.quarter
        df['ano'] = df['data'].dt.year
        
        # Features cíclicas para mês e dia da semana
        df['mes_seno'] = np.sin(2 * np.pi * df['mes_do_ano'] / 12)
        df['mes_cosseno'] = np.cos(2 * np.pi * df['mes_do_ano'] / 12)
        df['semana_seno'] = np.sin(2 * np.pi * df['dia_da_semana'] / 7)
        df['semana_cosseno'] = np.cos(2 * np.pi * df['dia_da_semana'] / 7)
        
        return df
    
    def extract_text_features(self, data: pd.DataFrame, text_column: str = 'descricao') -> pd.DataFrame:
        """Extrai características simples de texto.
        
        Args:
            data: DataFrame com coluna de texto.
            text_column: Nome da coluna de texto.
            
        Returns:
            DataFrame com características de texto adicionadas.
        """
        if text_column not in data.columns:
            raise ValueError(f"DataFrame deve conter a coluna '{text_column}'")
        
        # Cria cópia para não modificar o original
        df = data.copy()
        
        # Garante que a coluna é do tipo string
        df[text_column] = df[text_column].astype(str)
        
        # Extrai características simples
        df[f'{text_column}_comprimento'] = df[text_column].str.len()
        df[f'{text_column}_palavras'] = df[text_column].str.split().str.len()
        df[f'{text_column}_tem_numeros'] = df[text_column].str.contains('\d').astype(int)
        
        # Detecta padrões comuns em descrições de transações
        df[f'{text_column}_tem_pix'] = df[text_column].str.contains('pix|transferencia', case=False).astype(int)
        df[f'{text_column}_tem_pagamento'] = df[text_column].str.contains('pagamento|pag ', case=False).astype(int)
        df[f'{text_column}_tem_compra'] = df[text_column].str.contains('compra|loja|loj |mercado', case=False).astype(int)
        df[f'{text_column}_tem_supermercado'] = df[text_column].str.contains('super|merc|mercado', case=False).astype(int)
        df[f'{text_column}_tem_restaurante'] = df[text_column].str.contains('rest|food|restaurante|lanche', case=False).astype(int)
        df[f'{text_column}_tem_transporte'] = df[text_column].str.contains('uber|99|taxi|transporte', case=False).astype(int)
        
        return df
    
    def aggregate_data_by_period(self, data: pd.DataFrame, period: str = 'M') -> pd.DataFrame:
        """Agrega dados por período temporal.
        
        Args:
            data: DataFrame com coluna de data.
            period: Período para agregação ('D'=diário, 'W'=semanal, 'M'=mensal, 'Q'=trimestral).
            
        Returns:
            DataFrame com dados agregados.
        """
        if 'data' not in data.columns or 'valor' not in data.columns:
            raise ValueError("DataFrame deve conter as colunas 'data' e 'valor'")
        
        # Cria cópia para não modificar o original
        df = data.copy()
        
        # Garante que a coluna data é datetime
        if not pd.api.types.is_datetime64_any_dtype(df['data']):
            df['data'] = pd.to_datetime(df['data'])
        
        # Converte período para formato pandas
        period_map = {'D': 'D', 'W': 'W', 'M': 'M', 'Q': 'Q', 'Y': 'Y'}
        if period not in period_map:
            raise ValueError(f"Período inválido: {period}. Use D, W, M, Q ou Y")
        
        # Agrega por período
        df['periodo'] = df['data'].dt.to_period(period_map[period])
        
        # Agregações
        agg_df = df.groupby('periodo').agg(
            valor_total=('valor', 'sum'),
            valor_medio=('valor', 'mean'),
            contagem=('valor', 'count')
        ).reset_index()
        
        # Converte período para timestamp
        agg_df['data'] = agg_df['periodo'].dt.to_timestamp()
        agg_df = agg_df.drop('periodo', axis=1)
        
        return agg_df
    
    def prepare_all_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepara todos os conjuntos de dados para os diversos modelos.
        
        Args:
            data: DataFrame com dados brutos.
            
        Returns:
            Dicionário com dados preparados para cada modelo.
        """
        logger.info(f"Preparando todos os conjuntos de dados: {len(data)} registros")
        
        result = {}
        
        # Dados para previsão de gastos
        try:
            expense_data = self.prepare_expense_prediction_data(data)
            result['expense_prediction'] = expense_data
        except Exception as e:
            logger.error(f"Erro ao preparar dados para previsão de gastos: {str(e)}")
            result['expense_prediction'] = None
        
        # Dados para detecção de anomalias
        try:
            anomaly_data = self.prepare_anomaly_detection_data(data)
            result['anomaly_detection'] = anomaly_data
        except Exception as e:
            logger.error(f"Erro ao preparar dados para detecção de anomalias: {str(e)}")
            result['anomaly_detection'] = None
        
        # Dados para classificação de categorias
        try:
            if 'descricao' in data.columns and 'categoria' in data.columns:
                category_data, categories = self.prepare_category_classification_data(data)
                result['category_classification'] = category_data
                result['unique_categories'] = categories
            else:
                logger.warning("Dados não contêm colunas necessárias para classificação de categorias")
                result['category_classification'] = None
                result['unique_categories'] = []
        except Exception as e:
            logger.error(f"Erro ao preparar dados para classificação de categorias: {str(e)}")
            result['category_classification'] = None
            result['unique_categories'] = []
        
        # Dados para análise de padrões de gastos
        try:
            # Agrega por diferentes períodos
            result['daily_agg'] = self.aggregate_data_by_period(data, 'D')
            result['weekly_agg'] = self.aggregate_data_by_period(data, 'W')
            result['monthly_agg'] = self.aggregate_data_by_period(data, 'M')
        except Exception as e:
            logger.error(f"Erro ao preparar dados para análise de padrões: {str(e)}")
        
        logger.info("Preparação de todos os conjuntos de dados concluída")
        return result 