"""Modelo de machine learning para detecção de anomalias em transações financeiras.

Este módulo implementa algoritmos para identificar transações potencialmente 
anômalas ou fraudulentas com base em padrões históricos.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
import logging
import joblib
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from datetime import datetime, timedelta

# Configuração de logging
logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detector de anomalias em transações financeiras.
    
    Implementa vários algoritmos não supervisionados para identificar
    transações que fogem do padrão normal do usuário.
    """
    
    def __init__(self, model_type: str = 'isolation_forest', model_path: str = None):
        """Inicializa o detector de anomalias.
        
        Args:
            model_type: Tipo de modelo ('isolation_forest', 'local_outlier_factor', 'one_class_svm')
            model_path: Caminho opcional para carregar um modelo salvo
        """
        self.model = None
        self.scaler = StandardScaler()
        self.model_type = model_type
        self.threshold = -0.5  # Limiar de decisão para anomalias (ajustável)
        self.features = []
        self.categorical_cols = []
        self.numerical_cols = []
        self.is_fitted = False
        
        # Carrega o modelo se o caminho for fornecido
        if model_path and os.path.exists(model_path):
            self.load(model_path)
        else:
            self._setup_model()
    
    def _setup_model(self):
        """Configura o modelo com base no tipo especificado."""
        if self.model_type == 'isolation_forest':
            self.model = IsolationForest(
                n_estimators=100,
                max_samples='auto',
                contamination='auto',
                random_state=42
            )
        elif self.model_type == 'local_outlier_factor':
            self.model = LocalOutlierFactor(
                n_neighbors=20,
                contamination='auto',
                novelty=True
            )
        elif self.model_type == 'one_class_svm':
            self.model = OneClassSVM(
                nu=0.1,
                gamma='scale'
            )
        else:
            error_msg = f"Tipo de modelo não suportado: {self.model_type}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Modelo de detecção de anomalias ({self.model_type}) configurado")
    
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
            self.scaler = model_data.get('scaler', StandardScaler())
            self.model_type = model_data.get('model_type', self.model_type)
            self.threshold = model_data.get('threshold', self.threshold)
            self.features = model_data.get('features', [])
            self.categorical_cols = model_data.get('categorical_cols', [])
            self.numerical_cols = model_data.get('numerical_cols', [])
            self.is_fitted = model_data.get('is_fitted', False)
            
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
        if not self.is_fitted:
            logger.error("Não é possível salvar: modelo não treinado")
            return False
        
        try:
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Salva o modelo e metadados
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'model_type': self.model_type,
                'threshold': self.threshold,
                'features': self.features,
                'categorical_cols': self.categorical_cols,
                'numerical_cols': self.numerical_cols,
                'is_fitted': self.is_fitted
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
            data: DataFrame com dados de transações.
            
        Returns:
            DataFrame com features preparadas.
        """
        # Cria cópia para não modificar o original
        df = data.copy()
        
        # Verifica se as colunas necessárias existem
        required_cols = ['valor', 'data']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            error_msg = f"Colunas ausentes: {', '.join(missing_cols)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Converte coluna de data se não for datetime
        if not pd.api.types.is_datetime64_dtype(df['data']):
            try:
                df['data'] = pd.to_datetime(df['data'])
            except Exception as e:
                error_msg = f"Erro ao converter coluna 'data' para datetime: {str(e)}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        
        # Extrai características temporais
        df['dia_da_semana'] = df['data'].dt.dayofweek
        df['dia_do_mes'] = df['data'].dt.day
        df['mes'] = df['data'].dt.month
        df['hora'] = df['data'].dt.hour if 'hora' in df['data'].dt else 12  # Valor padrão se não tiver hora
        
        # Adiciona recursos especiais
        df['dias_desde_ultima_transacao'] = 0
        df = df.sort_values('data')
        
        # Calcula dias desde a última transação
        if len(df) > 1:
            dates = df['data'].values
            deltas = np.zeros(len(dates))
            
            for i in range(1, len(dates)):
                delta = (dates[i] - dates[i-1]).astype('timedelta64[D]').astype(int)
                deltas[i] = min(delta, 30)  # limita a 30 dias para evitar outliers extremos
            
            df['dias_desde_ultima_transacao'] = deltas
        
        # Se tiver categoria, cria one-hot encoding
        if 'categoria' in df.columns and 'categoria' not in self.categorical_cols:
            self.categorical_cols.append('categoria')
            
        # One-hot encoding para categorias
        for col in self.categorical_cols:
            if col in df.columns:
                dummies = pd.get_dummies(df[col], prefix=col, dummy_na=True)
                df = pd.concat([df, dummies], axis=1)
        
        # Identifica colunas numéricas se não foram definidas
        if not self.numerical_cols:
            self.numerical_cols = ['valor', 'dias_desde_ultima_transacao', 
                                  'dia_da_semana', 'dia_do_mes', 'mes', 'hora']
            # Filtra apenas as que existem no DataFrame
            self.numerical_cols = [col for col in self.numerical_cols if col in df.columns]
        
        # Define todas as features
        dummy_cols = [col for col in df.columns if any(col.startswith(f"{cat}_") for cat in self.categorical_cols)]
        self.features = self.numerical_cols + dummy_cols
        
        # Seleciona apenas as colunas de interesse
        return df[self.features].copy()
    
    def fit(self, data: pd.DataFrame) -> None:
        """Treina o modelo com dados históricos.
        
        Args:
            data: DataFrame com dados históricos de transações.
        """
        logger.info(f"Treinando modelo de detecção de anomalias ({self.model_type}) com {len(data)} registros")
        
        # Verifica se há dados suficientes
        if len(data) < 10:
            error_msg = f"Dados insuficientes para treino: {len(data)} registros (mínimo 10)"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Prepara as features
        X = self._prepare_features(data)
        
        # Normaliza dados numéricos
        X_scaled = self.scaler.fit_transform(X)
        
        # Treina o modelo
        self.model.fit(X_scaled)
        self.is_fitted = True
        
        # Para LocalOutlierFactor, que não tem método predict, precisamos definir o modelo novamente
        if self.model_type == 'local_outlier_factor':
            # Salva as pontuações do treino para uso futuro
            decision_scores = self.model.decision_function(X_scaled)
            # Recria o modelo com novalty=True para permitir previsões em novos dados
            self.model = LocalOutlierFactor(
                n_neighbors=20,
                contamination='auto',
                novelty=True
            )
            self.model.fit(X_scaled)
        
        logger.info(f"Modelo de detecção de anomalias treinado com sucesso")
    
    def predict(self, data: pd.DataFrame, threshold: Optional[float] = None) -> pd.DataFrame:
        """Identifica anomalias nos dados.
        
        Args:
            data: DataFrame com dados para verificar anomalias.
            threshold: Limiar opcional para classificar como anomalia.
            
        Returns:
            DataFrame com os dados originais e colunas adicionais indicando anomalias.
        """
        if not self.is_fitted:
            error_msg = "Modelo não treinado. Execute o método 'fit' primeiro."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Define threshold se fornecido
        if threshold is not None:
            self.threshold = threshold
        
        # Cria uma cópia dos dados originais
        result_df = data.copy()
        
        # Prepara as features
        try:
            X = self._prepare_features(data)
            
            # Verifica se temos todas as features necessárias
            missing_features = [f for f in self.features if f not in X.columns]
            if missing_features:
                # Adiciona colunas faltantes com zeros
                for feat in missing_features:
                    X[feat] = 0
            
            # Seleciona as colunas na ordem correta
            X = X[self.features]
            
            # Normaliza dados
            X_scaled = self.scaler.transform(X)
            
            # Faz predições
            if hasattr(self.model, 'decision_function'):
                # Para modelos com decision_function (OneClassSVM, IsolationForest)
                anomaly_scores = self.model.decision_function(X_scaled)
                is_anomaly = anomaly_scores < self.threshold
            elif hasattr(self.model, 'predict'):
                # Para modelos com predict diretamente (retorna 1 para normal, -1 para anomalia)
                predictions = self.model.predict(X_scaled)
                is_anomaly = predictions == -1
                # Tenta obter scores se disponível
                if hasattr(self.model, 'score_samples'):
                    anomaly_scores = self.model.score_samples(X_scaled)
                else:
                    anomaly_scores = np.zeros(len(is_anomaly))
            else:
                error_msg = f"Modelo {self.model_type} não suporta previsão"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            # Adiciona resultados ao DataFrame
            result_df['anomalia'] = is_anomaly
            result_df['score_anomalia'] = anomaly_scores
            
            # Adiciona nível de confiança (0 a 1, maior = mais anômalo)
            min_score = np.min(anomaly_scores)
            max_score = np.max(anomaly_scores)
            if min_score != max_score:
                result_df['confianca_anomalia'] = (max_score - anomaly_scores) / (max_score - min_score)
            else:
                result_df['confianca_anomalia'] = 0.0
            
            # Conta quantas anomalias foram encontradas
            n_anomalies = sum(is_anomaly)
            logger.info(f"Detecção concluída: {n_anomalies} anomalias encontradas em {len(data)} transações")
            
            return result_df
            
        except Exception as e:
            error_msg = f"Erro ao detectar anomalias: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def set_threshold(self, threshold: float) -> None:
        """Ajusta o limiar de detecção de anomalias.
        
        Args:
            threshold: Novo limiar para classificação (valores menores = mais sensível)
        """
        if threshold > 1.0 or threshold < -1.0:
            logger.warning(f"Threshold {threshold} fora do intervalo recomendado [-1.0, 1.0]")
        
        self.threshold = threshold
        logger.info(f"Threshold de anomalia ajustado para {threshold}")
    
    def explain_anomaly(self, transaction: pd.Series) -> Dict[str, Any]:
        """Explica por que uma transação foi considerada anômala.
        
        Args:
            transaction: Series com dados da transação.
            
        Returns:
            Dicionário com explicações sobre a anomalia.
        """
        if not self.is_fitted:
            error_msg = "Modelo não treinado. Execute o método 'fit' primeiro."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Prepara a transação para explicação
        transaction_df = pd.DataFrame([transaction])
        prepared_df = self._prepare_features(transaction_df)
        
        # Adiciona features faltantes com zeros
        for feat in self.features:
            if feat not in prepared_df.columns:
                prepared_df[feat] = 0
        
        # Seleciona as features na ordem correta
        prepared_df = prepared_df[self.features]
        
        # Normaliza dados
        X_scaled = self.scaler.transform(prepared_df)
        
        # Verifica se é realmente uma anomalia
        if hasattr(self.model, 'decision_function'):
            anomaly_score = self.model.decision_function(X_scaled)[0]
            is_anomaly = anomaly_score < self.threshold
        else:
            prediction = self.model.predict(X_scaled)[0]
            is_anomaly = prediction == -1
            if hasattr(self.model, 'score_samples'):
                anomaly_score = self.model.score_samples(X_scaled)[0]
            else:
                anomaly_score = 0.0
        
        # Se não for anomalia, retorna mensagem simples
        if not is_anomaly:
            return {
                'is_anomaly': False,
                'message': 'Esta transação não foi classificada como anômala.',
                'score': float(anomaly_score),
                'threshold': float(self.threshold)
            }
        
        # Para modelos baseados em árvores, tenta obter a importância das features
        feature_contributions = {}
        try:
            if self.model_type == 'isolation_forest' and hasattr(self.model, 'estimators_'):
                # Obtém a profundidade média da transação em cada árvore
                depths = []
                for tree in self.model.estimators_:
                    # Extrai a árvore e encontra o caminho
                    depths.append(self._get_tree_path_length(tree, X_scaled[0]))
                
                # Calcula a contribuição das features nas árvores
                features_used = {f: 0 for f in self.features}
                for tree in self.model.estimators_:
                    feature_indices = self._get_tree_feature_indices(tree)
                    for idx in feature_indices:
                        if 0 <= idx < len(self.features):
                            features_used[self.features[idx]] += 1
                
                # Normaliza as contribuições
                total = sum(features_used.values())
                if total > 0:
                    feature_contributions = {f: count/total for f, count in features_used.items()}
        except Exception as e:
            logger.warning(f"Erro ao calcular contribuições de features: {str(e)}")
        
        # Preparação da explicação
        explanation = {
            'is_anomaly': True,
            'score': float(anomaly_score),
            'threshold': float(self.threshold),
            'feature_contributions': feature_contributions
        }
        
        # Analisa os fatores que podem ter contribuído para a anomalia
        reasons = []
        
        # 1. Valor da transação
        if 'valor' in transaction:
            valor = transaction['valor']
            if valor > 0:  # é uma despesa
                quantile_99 = self._get_feature_quantile('valor', 0.99)
                quantile_95 = self._get_feature_quantile('valor', 0.95)
                
                if valor > quantile_99:
                    reasons.append(f"Valor muito alto (maior que 99% das transações anteriores)")
                elif valor > quantile_95:
                    reasons.append(f"Valor acima do normal (maior que 95% das transações anteriores)")
        
        # 2. Tempo desde a última transação
        if 'dias_desde_ultima_transacao' in prepared_df:
            dias = prepared_df['dias_desde_ultima_transacao'].iloc[0]
            if dias > 14:
                reasons.append(f"Intervalo incomum desde a última transação ({int(dias)} dias)")
        
        # 3. Categoria incomum (se disponível)
        if 'categoria' in transaction:
            categoria = transaction['categoria']
            # Verifica se é uma categoria raramente usada
            category_col = f"categoria_{categoria}"
            if category_col in feature_contributions and feature_contributions[category_col] > 0.1:
                reasons.append(f"Categoria '{categoria}' é incomum no seu histórico")
        
        # 4. Hora do dia incomum (se disponível)
        if 'hora' in prepared_df:
            hora = prepared_df['hora'].iloc[0]
            if hora < 6 or hora > 22:
                reasons.append(f"Horário incomum (hora {int(hora)})")
        
        # 5. Dia do mês incomum (pagamentos geralmente em datas fixas)
        if 'dia_do_mes' in prepared_df:
            dia = prepared_df['dia_do_mes'].iloc[0]
            if dia > 28:
                reasons.append(f"Data de pagamento incomum (dia {int(dia)} do mês)")
        
        # Se não encontrou razões específicas, dá uma explicação genérica
        if not reasons:
            reasons.append("Padrão de transação diferente do seu histórico habitual")
        
        # Adiciona as razões à explicação
        explanation['reasons'] = reasons
        explanation['message'] = "Esta transação foi classificada como anômala pois: " + "; ".join(reasons)
        
        return explanation
    
    def _get_feature_quantile(self, feature_name: str, quantile: float) -> float:
        """Obtém o quantil de uma feature com base no treino."""
        try:
            # Aqui assumimos que temos acesso aos dados originais do treino
            # Em uma implementação real, seria necessário armazenar estatísticas durante o fit
            return 999999.0  # Valor alto de exemplo
        except:
            return 999999.0  # Valor padrão caso não seja possível calcular
    
    def _get_tree_path_length(self, tree, x):
        """Calcula o comprimento do caminho de uma amostra na árvore."""
        try:
            return 0  # Simplificação - em um caso real precisa acessar a implementação interna da árvore
        except:
            return 0
    
    def _get_tree_feature_indices(self, tree):
        """Obtém os índices de features usados em uma árvore."""
        try:
            return []  # Simplificação - em um caso real precisa acessar a implementação interna da árvore
        except:
            return []
    
    def get_top_anomalies(self, data: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """Identifica as principais anomalias no conjunto de dados.
        
        Args:
            data: DataFrame com dados para verificar.
            top_n: Número de anomalias principais a retornar.
            
        Returns:
            DataFrame com as principais anomalias.
        """
        # Prediz anomalias em todos os dados
        result = self.predict(data)
        
        # Filtra apenas as anomalias e ordena pelo score
        anomalies = result[result['anomalia'] == True]
        top_anomalies = anomalies.sort_values('confianca_anomalia', ascending=False).head(top_n)
        
        return top_anomalies 