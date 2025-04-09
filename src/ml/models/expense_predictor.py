"""Modelo de machine learning para previsão de despesas futuras.

Este módulo implementa um modelo para prever gastos futuros com base 
em dados históricos de transações financeiras.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
import logging
from datetime import datetime, timedelta
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

# Configuração de logging
logger = logging.getLogger(__name__)


class ExpensePredictor:
    """Modelo para prever despesas futuras com base em histórico.
    
    Implementa algoritmos de séries temporais e regressão para
    prever gastos em períodos futuros.
    """
    
    def __init__(self, model_path: str = None):
        """Inicializa o preditor de despesas.
        
        Args:
            model_path: Caminho opcional para carregar um modelo salvo.
        """
        self.model = None
        self.scaler = MinMaxScaler()
        self.features = ['mes_do_ano', 'ano']
        self.target = 'valor'
        self.model_type = 'random_forest'  # default
        self.train_errors = {}
        self.model_path = model_path
        
        # Carrega o modelo se o caminho for fornecido
        if model_path and os.path.exists(model_path):
            self.load(model_path)
    
    def load(self, model_path: str) -> bool:
        """Carrega o modelo e metadados do disco.
        
        Args:
            model_path: Caminho para o arquivo do modelo salvo.
            
        Returns:
            Booleano indicando sucesso.
        """
        try:
            model_data = joblib.load(model_path)
            self.model = model_data.get('model')
            self.scaler = model_data.get('scaler', MinMaxScaler())
            self.features = model_data.get('features', self.features)
            self.train_errors = model_data.get('train_errors', {})
            self.model_type = model_data.get('model_type', self.model_type)
            logger.info(f"Modelo carregado com sucesso de {model_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar modelo de {model_path}: {str(e)}")
            return False
    
    def save(self, model_path: str) -> bool:
        """Salva o modelo e metadados no disco.
        
        Args:
            model_path: Caminho para salvar o modelo.
            
        Returns:
            Booleano indicando sucesso.
        """
        if self.model is None:
            logger.error("Não é possível salvar: modelo não treinado")
            return False
        
        try:
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Salva o modelo e metadados
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'features': self.features,
                'train_errors': self.train_errors,
                'model_type': self.model_type
            }
            joblib.dump(model_data, model_path)
            logger.info(f"Modelo salvo com sucesso em {model_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar modelo em {model_path}: {str(e)}")
            return False
    
    def _prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepara as features para o modelo.
        
        Args:
            data: DataFrame com dados de despesas mensais.
            
        Returns:
            DataFrame com features preparadas.
        """
        # Cria cópia para não modificar o original
        df = data.copy()
        
        # Verifica se as colunas necessárias existem
        required_cols = ['mes', 'valor']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Colunas ausentes: {', '.join(missing_cols)}")
        
        # Extrai características temporais se não existirem
        if 'mes_do_ano' not in df.columns:
            df['mes_do_ano'] = df['mes'].dt.month
        
        if 'ano' not in df.columns:
            df['ano'] = df['mes'].dt.year
        
        # Adiciona recursos cíclicos para capturar a sazonalidade mensal
        df['mes_seno'] = np.sin(2 * np.pi * df['mes_do_ano'] / 12)
        df['mes_cosseno'] = np.cos(2 * np.pi * df['mes_do_ano'] / 12)
        
        # Adiciona tendência linear
        min_date = df['mes'].min()
        df['meses_desde_inicio'] = df['mes'].apply(lambda x: ((x.year - min_date.year) * 12 + x.month - min_date.month))
        
        # Adiciona lag de 1 mês se houver dados suficientes
        if len(df) > 1:
            df['valor_mes_anterior'] = df['valor'].shift(1)
            df['valor_mes_anterior'] = df['valor_mes_anterior'].fillna(df['valor'].mean())
        
        return df
    
    def train(self, data: pd.DataFrame, model_type: str = 'random_forest') -> Dict[str, Any]:
        """Treina o modelo com dados históricos.
        
        Args:
            data: DataFrame com dados históricos de despesas mensais.
            model_type: Tipo de modelo ('linear', 'ridge', 'random_forest').
            
        Returns:
            Dicionário com métricas de desempenho do treino.
        """
        logger.info(f"Treinando modelo de previsão de despesas ({model_type}) com {len(data)} registros")
        
        # Verifica se há dados suficientes
        if len(data) < 3:
            error_msg = f"Dados insuficientes para treino: {len(data)} registros (mínimo 3)"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Seleciona o tipo de modelo
        self.model_type = model_type
        if model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'ridge':
            self.model = Ridge(alpha=1.0)
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Tipo de modelo não suportado: {model_type}")
        
        # Prepara as features
        df = self._prepare_features(data)
        
        # Seleciona features para o modelo
        if 'mes_seno' in df.columns and 'mes_cosseno' in df.columns:
            self.features = ['mes_do_ano', 'ano', 'mes_seno', 'mes_cosseno', 'meses_desde_inicio']
            if 'valor_mes_anterior' in df.columns:
                self.features.append('valor_mes_anterior')
        
        X = df[self.features].values
        y = df[self.target].values
        
        # Normaliza os dados
        X_scaled = self.scaler.fit_transform(X)
        
        # Treina o modelo
        self.model.fit(X_scaled, y)
        
        # Avalia o modelo no conjunto de treino
        y_pred = self.model.predict(X_scaled)
        
        # Calcula métricas
        mse = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        
        # Armazena erros
        self.train_errors = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2
        }
        
        logger.info(f"Modelo treinado com sucesso. RMSE: {rmse:.2f}, MAE: {mae:.2f}, R²: {r2:.2f}")
        
        return self.train_errors
    
    def predict(self, data: pd.DataFrame, n_future_months: int = 3) -> pd.DataFrame:
        """Prevê despesas para meses futuros.
        
        Args:
            data: DataFrame com dados históricos de despesas.
            n_future_months: Número de meses futuros para prever.
            
        Returns:
            DataFrame com previsões para os meses futuros.
        """
        if self.model is None:
            error_msg = "Modelo não treinado. Execute o método 'train' primeiro."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Cria uma cópia e prepara os dados
        df = data.copy()
        df = self._prepare_features(df)
        
        # Obtém o último mês disponível nos dados
        last_month = df['mes'].max()
        
        # Cria DataFrame para meses futuros
        future_months = [last_month + pd.DateOffset(months=i+1) for i in range(n_future_months)]
        future_df = pd.DataFrame({'mes': future_months})
        
        # Adiciona features temporais
        future_df['mes_do_ano'] = future_df['mes'].dt.month
        future_df['ano'] = future_df['mes'].dt.year
        future_df['mes_seno'] = np.sin(2 * np.pi * future_df['mes_do_ano'] / 12)
        future_df['mes_cosseno'] = np.cos(2 * np.pi * future_df['mes_do_ano'] / 12)
        
        # Calcula meses desde o início
        min_date = df['mes'].min()
        future_df['meses_desde_inicio'] = future_df['mes'].apply(
            lambda x: ((x.year - min_date.year) * 12 + x.month - min_date.month)
        )
        
        # Adiciona valor do mês anterior como feature (começa com o último valor conhecido)
        last_value = df['valor'].iloc[-1]
        future_values = []
        
        # Faz previsão iterativa (mês a mês)
        for i in range(n_future_months):
            # Copia as features para um mês
            month_features = future_df.iloc[i:i+1].copy()
            
            # Adiciona valor do mês anterior
            if 'valor_mes_anterior' in self.features:
                if i == 0:
                    month_features['valor_mes_anterior'] = last_value
                else:
                    month_features['valor_mes_anterior'] = future_values[-1]
            
            # Seleciona e escala as features
            X = month_features[self.features].values
            X_scaled = self.scaler.transform(X)
            
            # Faz a previsão
            prediction = self.model.predict(X_scaled)[0]
            future_values.append(prediction)
        
        # Adiciona previsões ao DataFrame
        future_df['valor_previsto'] = future_values
        
        # Adiciona intervalo de confiança baseado no MAE do treino
        if 'mae' in self.train_errors:
            mae = self.train_errors['mae']
            future_df['valor_minimo'] = future_df['valor_previsto'] - mae
            future_df['valor_maximo'] = future_df['valor_previsto'] + mae
            
            # Garante que os valores mínimos não sejam negativos (a menos que seja crédito)
            future_df['valor_minimo'] = future_df['valor_minimo'].clip(lower=0)
        
        # Seleciona colunas relevantes para o resultado
        result_df = future_df[['mes', 'valor_previsto'] + 
                            (['valor_minimo', 'valor_maximo'] if 'mae' in self.train_errors else [])]
        
        logger.info(f"Previsão gerada para {n_future_months} meses futuros")
        return result_df
    
    def evaluate(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """Avalia o modelo com dados de teste.
        
        Args:
            test_data: DataFrame com dados de teste.
            
        Returns:
            Dicionário com métricas de desempenho.
        """
        if self.model is None:
            error_msg = "Modelo não treinado. Execute o método 'train' primeiro."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Prepara os dados de teste
        df = self._prepare_features(test_data)
        
        # Verifica se todas as features necessárias estão presentes
        for feature in self.features:
            if feature not in df.columns:
                error_msg = f"Feature ausente nos dados de teste: {feature}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        
        # Seleciona features e alvo
        X = df[self.features].values
        y = df[self.target].values
        
        # Normaliza os dados
        X_scaled = self.scaler.transform(X)
        
        # Faz previsões
        y_pred = self.model.predict(X_scaled)
        
        # Calcula métricas
        mse = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        
        # Prepara resultado
        eval_metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2
        }
        
        logger.info(f"Avaliação em dados de teste: RMSE: {rmse:.2f}, MAE: {mae:.2f}, R²: {r2:.2f}")
        return eval_metrics
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Retorna a importância de cada feature para o modelo.
        
        Returns:
            Dicionário com importância de cada feature.
        """
        if self.model is None:
            error_msg = "Modelo não treinado. Execute o método 'train' primeiro."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Verifica se o modelo suporta feature_importance
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            result = dict(zip(self.features, importances))
            return result
        elif hasattr(self.model, 'coef_'):
            importances = np.abs(self.model.coef_)
            result = dict(zip(self.features, importances))
            return result
        else:
            logger.warning(f"Modelo {self.model_type} não suporta importância de features.")
            return {feature: 0.0 for feature in self.features}
    
    def predict_next_month_expense(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prevê despesas para o próximo mês.
        
        Args:
            data: DataFrame com dados históricos de despesas.
            
        Returns:
            Dicionário com previsão para o próximo mês.
        """
        # Faz a previsão apenas para o próximo mês
        prediction_df = self.predict(data, n_future_months=1)
        
        # Extrai o resultado
        result = {
            'data_previsao': datetime.now().strftime('%Y-%m-%d'),
            'mes_previsto': prediction_df['mes'][0].strftime('%Y-%m'),
            'valor_previsto': float(prediction_df['valor_previsto'][0]),
        }
        
        # Adiciona intervalo de confiança se disponível
        if 'valor_minimo' in prediction_df.columns:
            result['valor_minimo'] = float(prediction_df['valor_minimo'][0])
            result['valor_maximo'] = float(prediction_df['valor_maximo'][0])
        
        return result 