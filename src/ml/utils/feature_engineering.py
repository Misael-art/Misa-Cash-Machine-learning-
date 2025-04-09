"""
Utilitários para engenharia de características para modelos de predição financeira.

Este módulo contém funções para extrair, transformar e preparar recursos
para modelos de machine learning financeiros, especialmente para predição de despesas.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


def extract_date_features(df, date_column='date'):
    """
    Extrai características temporais de uma coluna de data.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        date_column (str): Nome da coluna contendo as datas
        
    Returns:
        pd.DataFrame: DataFrame com as características temporais adicionadas
    """
    # Garantir que a coluna de data seja do tipo datetime
    if df[date_column].dtype != 'datetime64[ns]':
        df[date_column] = pd.to_datetime(df[date_column])
    
    # Cópia para não modificar o original
    result_df = df.copy()
    
    # Extrair características de data
    result_df['year'] = df[date_column].dt.year
    result_df['month'] = df[date_column].dt.month
    result_df['day'] = df[date_column].dt.day
    result_df['day_of_week'] = df[date_column].dt.dayofweek
    result_df['day_of_year'] = df[date_column].dt.dayofyear
    result_df['week_of_year'] = df[date_column].dt.isocalendar().week
    result_df['is_month_start'] = df[date_column].dt.is_month_start.astype(int)
    result_df['is_month_end'] = df[date_column].dt.is_month_end.astype(int)
    result_df['is_quarter_start'] = df[date_column].dt.is_quarter_start.astype(int)
    result_df['is_quarter_end'] = df[date_column].dt.is_quarter_end.astype(int)
    result_df['is_year_start'] = df[date_column].dt.is_year_start.astype(int)
    result_df['is_year_end'] = df[date_column].dt.is_year_end.astype(int)
    result_df['is_weekend'] = (df[date_column].dt.dayofweek >= 5).astype(int)
    
    # Características cíclicas para o mês e dia da semana (usando transformação seno-cosseno)
    result_df['month_sin'] = np.sin(2 * np.pi * df[date_column].dt.month / 12)
    result_df['month_cos'] = np.cos(2 * np.pi * df[date_column].dt.month / 12)
    result_df['day_of_week_sin'] = np.sin(2 * np.pi * df[date_column].dt.dayofweek / 7)
    result_df['day_of_week_cos'] = np.cos(2 * np.pi * df[date_column].dt.dayofweek / 7)
    
    return result_df


def add_lag_features(df, target_column, lag_periods=[1, 2, 3], group_columns=None):
    """
    Adiciona características de lag para uma coluna alvo.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        target_column (str): Nome da coluna alvo para criar lags
        lag_periods (list): Lista com os períodos de lag a serem criados
        group_columns (list): Lista de colunas para agrupar (para dados de várias entidades)
        
    Returns:
        pd.DataFrame: DataFrame com as características de lag adicionadas
    """
    result_df = df.copy()
    
    if group_columns is not None:
        for lag in lag_periods:
            lag_col_name = f"{target_column}_lag_{lag}"
            result_df[lag_col_name] = result_df.groupby(group_columns)[target_column].shift(lag)
    else:
        for lag in lag_periods:
            lag_col_name = f"{target_column}_lag_{lag}"
            result_df[lag_col_name] = result_df[target_column].shift(lag)
            
    return result_df


def add_rolling_features(df, target_column, windows=[7, 14, 30], functions=['mean', 'std', 'min', 'max'], 
                         group_columns=None):
    """
    Adiciona características de janela móvel (rolling window) para uma coluna alvo.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        target_column (str): Nome da coluna alvo
        windows (list): Lista com os tamanhos das janelas
        functions (list): Lista com as funções a serem aplicadas
        group_columns (list): Lista de colunas para agrupar (para dados de várias entidades)
        
    Returns:
        pd.DataFrame: DataFrame com as características de janela móvel adicionadas
    """
    result_df = df.copy()
    
    # Mapeamento de funções
    func_map = {
        'mean': lambda x: x.mean(),
        'std': lambda x: x.std(),
        'min': lambda x: x.min(),
        'max': lambda x: x.max(),
        'median': lambda x: x.median(),
        'sum': lambda x: x.sum(),
        'count': lambda x: x.count()
    }
    
    for window in windows:
        for func_name in functions:
            if func_name not in func_map:
                continue
                
            func = func_map[func_name]
            col_name = f"{target_column}_roll_{window}_{func_name}"
            
            if group_columns is not None:
                result_df[col_name] = result_df.groupby(group_columns)[target_column].transform(
                    lambda x: x.rolling(window=window, min_periods=1).apply(func)
                )
            else:
                result_df[col_name] = result_df[target_column].rolling(window=window, min_periods=1).apply(func)
                
    return result_df


def add_cyclical_features(df, column, period):
    """
    Transforma uma coluna cíclica em características seno e cosseno.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        column (str): Nome da coluna cíclica
        period (int): Período do ciclo (ex: 12 para meses, 7 para dias da semana)
        
    Returns:
        pd.DataFrame: DataFrame com as características cíclicas adicionadas
    """
    result_df = df.copy()
    sin_col = f"{column}_sin"
    cos_col = f"{column}_cos"
    
    result_df[sin_col] = np.sin(2 * np.pi * df[column] / period)
    result_df[cos_col] = np.cos(2 * np.pi * df[column] / period)
    
    return result_df


def encode_categorical_features(df, categorical_columns, drop_original=True, handle_unknown='ignore'):
    """
    Codifica características categóricas usando one-hot encoding.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        categorical_columns (list): Lista de colunas categóricas para codificar
        drop_original (bool): Se deve eliminar as colunas originais
        handle_unknown (str): Como lidar com categorias desconhecidas ('ignore' ou 'error')
        
    Returns:
        pd.DataFrame: DataFrame com as características categóricas codificadas
        OneHotEncoder: Encoder treinado para uso futuro
    """
    result_df = df.copy()
    
    # Criação e treinamento do encoder
    encoder = OneHotEncoder(sparse=False, handle_unknown=handle_unknown)
    encoded_features = encoder.fit_transform(result_df[categorical_columns])
    
    # Obter nomes das colunas codificadas
    feature_names = []
    for i, col in enumerate(categorical_columns):
        categories = encoder.categories_[i]
        for category in categories:
            feature_names.append(f"{col}_{category}")
    
    # Criar dataframe com as características codificadas
    encoded_df = pd.DataFrame(encoded_features, columns=feature_names, index=result_df.index)
    
    # Combinar com o dataframe original
    result_df = pd.concat([result_df, encoded_df], axis=1)
    
    # Remover colunas originais se solicitado
    if drop_original:
        result_df = result_df.drop(columns=categorical_columns)
    
    return result_df, encoder


def handle_missing_values(df, numeric_strategy='mean', categorical_strategy='most_frequent'):
    """
    Preenche valores ausentes em colunas numéricas e categóricas.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        numeric_strategy (str): Estratégia para preencher valores ausentes em colunas numéricas
        categorical_strategy (str): Estratégia para preencher valores ausentes em colunas categóricas
        
    Returns:
        pd.DataFrame: DataFrame com valores ausentes preenchidos
        dict: Dicionário com os imputadores para uso futuro
    """
    result_df = df.copy()
    
    # Separar colunas numéricas e categóricas
    numeric_columns = result_df.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = result_df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    imputadores = {}
    
    # Preencher valores ausentes em colunas numéricas
    if numeric_columns:
        numeric_imputer = SimpleImputer(strategy=numeric_strategy)
        result_df[numeric_columns] = numeric_imputer.fit_transform(result_df[numeric_columns])
        imputadores['numeric'] = numeric_imputer
    
    # Preencher valores ausentes em colunas categóricas
    if categorical_columns:
        categorical_imputer = SimpleImputer(strategy=categorical_strategy)
        result_df[categorical_columns] = categorical_imputer.fit_transform(result_df[categorical_columns])
        imputadores['categorical'] = categorical_imputer
    
    return result_df, imputadores


def normalize_features(df, columns_to_scale=None, scaler_type='standard'):
    """
    Normaliza características numéricas.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        columns_to_scale (list): Lista de colunas para normalizar (se None, todas as numéricas)
        scaler_type (str): Tipo de normalização ('standard', 'minmax', etc.)
        
    Returns:
        pd.DataFrame: DataFrame com características normalizadas
        object: Scaler treinado para uso futuro
    """
    result_df = df.copy()
    
    # Se nenhuma coluna for especificada, usar todas as numéricas
    if columns_to_scale is None:
        columns_to_scale = result_df.select_dtypes(include=['number']).columns.tolist()
    
    # Usar apenas colunas existentes
    columns_to_scale = [col for col in columns_to_scale if col in result_df.columns]
    
    if not columns_to_scale:
        return result_df, None
    
    # Criar e treinar o scaler
    scaler = StandardScaler()  # Por enquanto, apenas StandardScaler é suportado
    
    # Aplicar o scaler
    result_df[columns_to_scale] = scaler.fit_transform(result_df[columns_to_scale])
    
    return result_df, scaler


def aggregate_features_by_category(df, group_column, agg_columns, agg_functions=None):
    """
    Agrega características por categoria.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        group_column (str): Coluna para agrupar
        agg_columns (list): Lista de colunas para agregar
        agg_functions (dict): Dicionário com as funções de agregação por coluna
        
    Returns:
        pd.DataFrame: DataFrame com as agregações por categoria
    """
    if agg_functions is None:
        agg_functions = {}
        for col in agg_columns:
            if df[col].dtype in ['int64', 'float64']:
                agg_functions[col] = ['mean', 'sum', 'min', 'max', 'std']
            else:
                agg_functions[col] = ['count', 'nunique']
    
    # Realizar a agregação
    agg_df = df.groupby(group_column).agg(agg_functions)
    
    # Achatar os nomes das colunas para formato mais fácil de usar
    agg_df.columns = ['_'.join(col).strip() for col in agg_df.columns.values]
    
    # Resetar o índice para ter o group_column como coluna
    agg_df = agg_df.reset_index()
    
    return agg_df


def create_interaction_features(df, feature_pairs, interaction_type='multiply'):
    """
    Cria características de interação entre pares de colunas.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados
        feature_pairs (list): Lista de tuplas com pares de colunas para interação
        interaction_type (str): Tipo de interação ('multiply', 'divide', 'add', 'subtract')
        
    Returns:
        pd.DataFrame: DataFrame com as características de interação adicionadas
    """
    result_df = df.copy()
    
    operations = {
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / (y + 1e-8),  # Evitar divisão por zero
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y
    }
    
    operation = operations.get(interaction_type, operations['multiply'])
    
    for col1, col2 in feature_pairs:
        if col1 in result_df.columns and col2 in result_df.columns:
            # Garantir que ambas as colunas são numéricas
            if pd.api.types.is_numeric_dtype(result_df[col1]) and pd.api.types.is_numeric_dtype(result_df[col2]):
                interaction_name = f"{col1}_{interaction_type}_{col2}"
                result_df[interaction_name] = operation(result_df[col1], result_df[col2])
    
    return result_df 