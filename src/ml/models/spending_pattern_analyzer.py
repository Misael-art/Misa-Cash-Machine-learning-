"""Modelo de machine learning para análise de padrões de gastos.

Este módulo implementa algoritmos para identificar padrões nos gastos 
do usuário, incluindo clustering, sazonalidade e correlações entre categorias.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
import logging
import joblib
import os
from datetime import datetime, timedelta
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns

# Integração com o ExpensePredictor
from .expense_predictor import ExpensePredictor

# Configuração de logging
logger = logging.getLogger(__name__)


class SpendingPatternAnalyzer:
    """Analisador de padrões de gastos em transações financeiras.
    
    Implementa algoritmos de aprendizado não supervisionado para identificar
    padrões de gastos, comportamentos sazonais e correlações entre categorias.
    """
    
    def __init__(self, model_path: str = None):
        """Inicializa o analisador de padrões de gastos.
        
        Args:
            model_path: Caminho opcional para carregar um modelo salvo.
        """
        self.scaler = StandardScaler()
        self.kmeans_model = None
        self.dbscan_model = None
        self.n_clusters = 0
        self.features = []
        self.clusters = None
        self.seasonal_patterns = {}
        self.category_correlations = None
        self.is_fitted = False
        
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
            self.kmeans_model = model_data.get('kmeans_model')
            self.dbscan_model = model_data.get('dbscan_model')
            self.scaler = model_data.get('scaler', StandardScaler())
            self.features = model_data.get('features', [])
            self.n_clusters = model_data.get('n_clusters', 0)
            self.clusters = model_data.get('clusters', None)
            self.seasonal_patterns = model_data.get('seasonal_patterns', {})
            self.category_correlations = model_data.get('category_correlations', None)
            self.is_fitted = True
            logger.info(f"Modelo de análise de padrões carregado com sucesso de {model_path}")
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
        try:
            model_data = {
                'kmeans_model': self.kmeans_model,
                'dbscan_model': self.dbscan_model,
                'scaler': self.scaler,
                'features': self.features,
                'n_clusters': self.n_clusters,
                'clusters': self.clusters,
                'seasonal_patterns': self.seasonal_patterns,
                'category_correlations': self.category_correlations,
                'timestamp': datetime.now().isoformat()
            }
            joblib.dump(model_data, model_path)
            logger.info(f"Modelo de análise de padrões salvo com sucesso em {model_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar modelo em {model_path}: {str(e)}")
            return False
    
    def _prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepara as features para análise de padrões.
        
        Args:
            data: DataFrame com dados de transações.
            
        Returns:
            DataFrame com features preparadas.
        """
        # Cria cópia para não modificar o original
        df = data.copy()
        
        # Verifica se as colunas necessárias existem
        required_cols = ['data', 'valor', 'categoria']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Colunas ausentes: {', '.join(missing_cols)}")
        
        # Converte a data para datetime se não for
        if not pd.api.types.is_datetime64_any_dtype(df['data']):
            df['data'] = pd.to_datetime(df['data'])
        
        # Extrai características temporais
        df['mes'] = df['data'].dt.month
        df['ano'] = df['data'].dt.year
        df['dia_mes'] = df['data'].dt.day
        df['dia_semana'] = df['data'].dt.dayofweek
        df['semana_mes'] = df['data'].dt.isocalendar().week - df['data'].dt.to_period('M').dt.to_timestamp().dt.isocalendar().week + 1
        df['fim_semana'] = df['dia_semana'].apply(lambda x: 1 if x >= 5 else 0)
        df['quinzena'] = df['dia_mes'].apply(lambda x: 1 if x <= 15 else 2)
        
        # Cria período como combinação de ano e mês
        df['periodo'] = df['ano'].astype(str) + '-' + df['mes'].astype(str).str.zfill(2)
        
        # Adiciona características de valor
        df['valor_abs'] = df['valor'].abs()
        df['valor_log'] = np.log1p(df['valor_abs'])  # log(1+x) para lidar com zeros
        
        # One-hot encoding para categorias
        if 'categoria' in df.columns:
            categories_dummies = pd.get_dummies(df['categoria'], prefix='cat')
            df = pd.concat([df, categories_dummies], axis=1)
        
        # Atualiza lista de features
        self.features = ['valor_abs', 'valor_log', 'mes', 'dia_mes', 'dia_semana', 
                        'semana_mes', 'fim_semana', 'quinzena']
        
        # Adiciona colunas de categorias se existirem
        cat_cols = [col for col in df.columns if col.startswith('cat_')]
        self.features.extend(cat_cols)
        
        return df
    
    def find_clusters(self, data: pd.DataFrame, n_clusters: int = 0, 
                      method: str = 'kmeans', 
                      min_samples: int = 5) -> pd.DataFrame:
        """Identifica clusters de comportamento de gastos.
        
        Args:
            data: DataFrame com transações.
            n_clusters: Número de clusters (0 para auto-detecção).
            method: Método de clustering ('kmeans', 'dbscan').
            min_samples: Mínimo de amostras para DBSCAN.
            
        Returns:
            DataFrame com os dados originais e clusters identificados.
        """
        logger.info(f"Iniciando análise de clusters usando método {method}")
        
        # Prepara as features
        df = self._prepare_features(data)
        
        # Seleciona colunas para clustering
        X = df[self.features].copy()
        
        # Escala os dados
        X_scaled = self.scaler.fit_transform(X)
        
        # Determina número ideal de clusters se não especificado
        if method == 'kmeans' and n_clusters <= 0:
            n_clusters = self._find_optimal_clusters(X_scaled, max_clusters=10)
            logger.info(f"Número ideal de clusters determinado: {n_clusters}")
        
        # Aplica algoritmo de clustering
        if method == 'kmeans':
            self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = self.kmeans_model.fit_predict(X_scaled)
            
            # Calcula estatísticas dos clusters
            df['cluster'] = clusters
            self.clusters = df.groupby('cluster').agg({
                'valor_abs': ['mean', 'std', 'min', 'max', 'count'],
                'data': ['min', 'max']
            })
            
            self.n_clusters = n_clusters
            self.is_fitted = True
            
        elif method == 'dbscan':
            # DBSCAN não requer número fixo de clusters
            self.dbscan_model = DBSCAN(eps=0.5, min_samples=min_samples)
            clusters = self.dbscan_model.fit_predict(X_scaled)
            
            # Adiciona resultados ao dataframe
            df['cluster'] = clusters
            
            # Calcula estatísticas dos clusters (excluindo ruído = -1)
            cluster_ids = sorted(list(set(clusters)))
            if -1 in cluster_ids:
                cluster_ids.remove(-1)
            
            self.clusters = df[df['cluster'] != -1].groupby('cluster').agg({
                'valor_abs': ['mean', 'std', 'min', 'max', 'count'],
                'data': ['min', 'max']
            })
            
            self.n_clusters = len(cluster_ids)
            self.is_fitted = True
            
        else:
            raise ValueError(f"Método de clustering não suportado: {method}")
        
        # Adiciona informações de cluster ao resultado
        result_df = data.copy()
        result_df['cluster'] = clusters
        
        logger.info(f"Análise de clusters concluída: {self.n_clusters} padrões identificados")
        return result_df
    
    def _find_optimal_clusters(self, X, max_clusters=10) -> int:
        """Encontra o número ideal de clusters usando o método do cotovelo e silhueta.
        
        Args:
            X: Matriz de features.
            max_clusters: Número máximo de clusters a testar.
            
        Returns:
            Número ideal de clusters.
        """
        from kneed import KneeLocator
        
        # Calcula inércia (soma de distâncias quadradas) para diferentes números de clusters
        inertias = []
        silhouette_scores = []
        
        # Limita o número máximo de clusters ao número de amostras/5 ou max_clusters
        max_possible = min(max_clusters, X.shape[0] // 5)
        k_range = range(2, max_possible + 1)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)
            
            # Calcula score de silhueta se houver instâncias suficientes
            if X.shape[0] > k:
                score = silhouette_score(X, kmeans.labels_)
                silhouette_scores.append(score)
        
        # Detecta o cotovelo na curva de inércia
        try:
            kl = KneeLocator(k_range, inertias, curve='convex', direction='decreasing')
            optimal_k_inertia = kl.elbow
        except:
            # Se falhar, usa regra empírica
            optimal_k_inertia = max(2, len(k_range) // 3)
        
        # Pega o melhor score de silhueta
        if silhouette_scores:
            optimal_k_silhouette = k_range[silhouette_scores.index(max(silhouette_scores))]
        else:
            optimal_k_silhouette = optimal_k_inertia
        
        # Retorna a média dos dois métodos
        return max(2, int((optimal_k_inertia + optimal_k_silhouette) / 2))
    
    def analyze_seasonality(self, data: pd.DataFrame, 
                           period: str = 'M',  # M: mensal, W: semanal, Q: trimestral
                           columns: List[str] = None) -> Dict[str, Any]:
        """Analisa componentes sazonais nos gastos.
        
        Args:
            data: DataFrame com transações.
            period: Período para análise ('M', 'W', 'Q', 'Y').
            columns: Colunas específicas para análise (default: 'valor').
            
        Returns:
            Dicionário com resultados da análise sazonal.
        """
        logger.info(f"Iniciando análise de sazonalidade com período {period}")
        
        # Prepara os dados
        df = data.copy()
        
        # Converte a data para datetime se não for
        if 'data' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['data']):
            df['data'] = pd.to_datetime(df['data'])
        
        # Define colunas para análise
        if columns is None:
            columns = ['valor']
        
        results = {}
        
        # Agrega os dados pelo período especificado
        for col in columns:
            if col not in df.columns:
                logger.warning(f"Coluna {col} não encontrada no DataFrame")
                continue
            
            try:
                # Agrega valores por período
                df_period = df.set_index('data')[col].resample(period).sum()
                
                # Preenche valores ausentes
                df_period = df_period.fillna(df_period.mean())
                
                # Verifica se temos dados suficientes para decomposição
                if len(df_period) < 4:
                    logger.warning(f"Dados insuficientes para análise sazonal de {col} (mínimo 4 períodos)")
                    continue
                
                # Decomposição sazonal
                result = seasonal_decompose(df_period, model='additive', extrapolate_trend='freq')
                
                # Salva componentes
                seasonal_data = {
                    'original': df_period.to_dict(),
                    'trend': result.trend.to_dict(),
                    'seasonal': result.seasonal.to_dict(),
                    'residual': result.resid.to_dict(),
                    'period': period,
                    'seasonal_strength': np.nanvar(result.seasonal) / np.nanvar(result.trend + result.seasonal)
                }
                
                # Detecta picos sazonais
                seasonal_component = result.seasonal.reset_index()
                seasonal_component.columns = ['data', 'valor']
                
                if period == 'M':
                    seasonal_component['mes'] = seasonal_component['data'].dt.month
                    peak_month = seasonal_component.groupby('mes')['valor'].mean().idxmax()
                    trough_month = seasonal_component.groupby('mes')['valor'].mean().idxmin()
                    
                    seasonal_data['peak_period'] = peak_month
                    seasonal_data['trough_period'] = trough_month
                    
                elif period == 'W':
                    seasonal_component['semana'] = seasonal_component['data'].dt.isocalendar().week
                    peak_week = seasonal_component.groupby('semana')['valor'].mean().idxmax()
                    trough_week = seasonal_component.groupby('semana')['valor'].mean().idxmin()
                    
                    seasonal_data['peak_period'] = peak_week
                    seasonal_data['trough_period'] = trough_week
                
                results[col] = seasonal_data
                
            except Exception as e:
                logger.error(f"Erro na análise sazonal de {col}: {str(e)}")
                continue
        
        # Armazena resultados
        self.seasonal_patterns = results
        logger.info(f"Análise de sazonalidade concluída para {len(results)} variáveis")
        
        return results
    
    def analyze_category_correlations(self, data: pd.DataFrame, 
                                     method: str = 'pearson') -> pd.DataFrame:
        """Analisa correlações entre categorias de gastos.
        
        Args:
            data: DataFrame com transações financeiras.
            method: Método de correlação ('pearson', 'spearman').
            
        Returns:
            DataFrame com matriz de correlação entre categorias.
        """
        logger.info(f"Iniciando análise de correlação entre categorias usando método {method}")
        
        # Prepara os dados
        df = data.copy()
        
        # Converte a data para datetime se não for
        if 'data' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['data']):
            df['data'] = pd.to_datetime(df['data'])
        
        # Verifica se temos as colunas necessárias
        if 'categoria' not in df.columns or 'valor' not in df.columns:
            error_msg = "Colunas 'categoria' e 'valor' são necessárias para análise de correlação"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            # Cria tabela pivô: períodos x categorias
            pivot_df = df.pivot_table(
                index=pd.Grouper(key='data', freq='M'),
                columns='categoria',
                values='valor',
                aggfunc='sum',
                fill_value=0
            )
            
            # Garante que temos dados suficientes
            if pivot_df.shape[0] < 3 or pivot_df.shape[1] < 2:
                logger.warning("Dados insuficientes para análise de correlação entre categorias")
                return pd.DataFrame()
            
            # Calcula correlações
            if method == 'pearson':
                corr_matrix = pivot_df.corr(method='pearson')
            elif method == 'spearman':
                corr_matrix = pivot_df.corr(method='spearman')
            else:
                logger.warning(f"Método de correlação não reconhecido: {method}, usando pearson")
                corr_matrix = pivot_df.corr(method='pearson')
            
            # Armazena resultado
            self.category_correlations = corr_matrix
            
            logger.info(f"Análise de correlação concluída para {corr_matrix.shape[0]} categorias")
            return corr_matrix
            
        except Exception as e:
            logger.error(f"Erro na análise de correlação: {str(e)}")
            return pd.DataFrame()
    
    def find_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Executa análise completa de padrões de gastos.
        
        Args:
            data: DataFrame com transações financeiras.
            
        Returns:
            Dicionário com resultados da análise.
        """
        logger.info("Iniciando análise completa de padrões de gastos")
        
        results = {}
        
        # Análise de clusters
        try:
            clusters_df = self.find_clusters(data)
            results['clusters'] = {
                'n_clusters': self.n_clusters,
                'cluster_stats': self.clusters
            }
        except Exception as e:
            logger.error(f"Erro na análise de clusters: {str(e)}")
            results['clusters'] = None
        
        # Análise de sazonalidade
        try:
            seasonal_results = self.analyze_seasonality(data)
            results['seasonality'] = seasonal_results
        except Exception as e:
            logger.error(f"Erro na análise de sazonalidade: {str(e)}")
            results['seasonality'] = None
        
        # Análise de correlação
        try:
            corr_matrix = self.analyze_category_correlations(data)
            
            # Extrai correlações mais fortes
            if not corr_matrix.empty:
                corr_data = corr_matrix.unstack()
                corr_data = corr_data[corr_data < 1.0]  # Remove autocorrelação
                
                # Ordena por valor absoluto
                corr_data = corr_data.abs().sort_values(ascending=False)
                
                # Converte para dicionário
                top_correlations = []
                for (cat1, cat2), corr in corr_data.head(10).items():
                    # Obtém o valor original (com sinal)
                    original_corr = corr_matrix.loc[cat1, cat2]
                    top_correlations.append({
                        'cat1': cat1,
                        'cat2': cat2,
                        'correlation': original_corr,
                        'abs_correlation': corr
                    })
                
                results['correlations'] = {
                    'matrix': corr_matrix,
                    'top_correlations': top_correlations
                }
            else:
                results['correlations'] = None
        except Exception as e:
            logger.error(f"Erro na análise de correlação: {str(e)}")
            results['correlations'] = None
        
        logger.info("Análise de padrões de gastos concluída com sucesso")
        return results
    
    def recommend_insights(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Gera insights baseados na análise de padrões.
        
        Args:
            data: DataFrame com transações.
            
        Returns:
            Lista de insights com descrições e relevância.
        """
        # Primeiro executa a análise completa
        patterns = self.find_patterns(data)
        
        insights = []
        
        # Insights baseados em clusters
        if patterns['clusters'] and 'cluster_stats' in patterns['clusters']:
            clusters = patterns['clusters']['cluster_stats']
            for cluster_id, stats in clusters.reset_index().iterrows():
                if stats[('valor_abs', 'count')] > 5:  # Apenas clusters com pelo menos 5 transações
                    if stats[('valor_abs', 'std')] > stats[('valor_abs', 'mean')] * 0.5:
                        insights.append({
                            'type': 'cluster',
                            'description': f"Identificado grupo de {stats[('valor_abs', 'count')]:.0f} transações com" + 
                                          f" valor médio de R$ {stats[('valor_abs', 'mean')]:.2f} e alta variabilidade.",
                            'relevance': 0.7,
                            'data': {
                                'cluster_id': cluster_id,
                                'count': stats[('valor_abs', 'count')],
                                'mean_value': stats[('valor_abs', 'mean')],
                                'std': stats[('valor_abs', 'std')]
                            }
                        })
        
        # Insights baseados em sazonalidade
        if patterns['seasonality']:
            for col, season_data in patterns['seasonality'].items():
                if season_data['seasonal_strength'] > 0.3:  # Significativa sazonalidade
                    peak_period = season_data.get('peak_period')
                    if peak_period:
                        if season_data['period'] == 'M':
                            month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                                          'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
                            peak_name = month_names[peak_period - 1]
                            insights.append({
                                'type': 'seasonality',
                                'description': f"Gastos tendem a aumentar em {peak_name}.",
                                'relevance': 0.8,
                                'data': {
                                    'variable': col,
                                    'period_type': 'month',
                                    'peak_period': peak_period,
                                    'peak_name': peak_name,
                                    'seasonal_strength': season_data['seasonal_strength']
                                }
                            })
        
        # Insights baseados em correlações
        if patterns['correlations'] and 'top_correlations' in patterns['correlations']:
            for corr in patterns['correlations']['top_correlations'][:3]:  # Top 3 correlações
                corr_val = corr['correlation']
                cat1 = corr['cat1']
                cat2 = corr['cat2']
                
                if abs(corr_val) > 0.7:  # Apenas correlações fortes
                    description = ""
                    if corr_val > 0:
                        description = f"Gastos em '{cat1}' e '{cat2}' tendem a aumentar juntos."
                    else:
                        description = f"Quando gastos em '{cat1}' aumentam, gastos em '{cat2}' tendem a diminuir."
                    
                    insights.append({
                        'type': 'correlation',
                        'description': description,
                        'relevance': 0.75,
                        'data': {
                            'cat1': cat1,
                            'cat2': cat2,
                            'correlation': corr_val
                        }
                    })
        
        # Ordena insights por relevância
        insights.sort(key=lambda x: x['relevance'], reverse=True)
        
        return insights
    
    def integrate_with_expense_predictor(self, data: pd.DataFrame, 
                                        predictor: ExpensePredictor) -> Dict[str, Any]:
        """Integra análise de padrões com o preditor de despesas.
        
        Args:
            data: DataFrame com transações.
            predictor: Instância de ExpensePredictor.
            
        Returns:
            Dicionário com insights integrados.
        """
        logger.info("Integrando análise de padrões com preditor de despesas")
        
        results = {}
        
        # Executa análise de padrões
        patterns = self.find_patterns(data)
        
        # Obtém previsões
        predictions = predictor.predict(data)
        
        # Integra informações de sazonalidade nas previsões
        if patterns['seasonality'] and 'valor' in patterns['seasonality']:
            season_data = patterns['seasonality']['valor']
            
            # Identifica meses com gastos sazonalmente altos
            if 'seasonal' in season_data:
                seasonal_values = pd.Series(season_data['seasonal'])
                high_months = seasonal_values[seasonal_values > 0].index
                
                # Verifica se algum mês previsto está em meses de alto gasto
                high_spending_predictions = []
                for i, row in predictions.iterrows():
                    month = row['mes'].month
                    high_seasonal = any(pd.Timestamp(m).month == month for m in high_months)
                    if high_seasonal:
                        high_spending_predictions.append({
                            'date': row['mes'],
                            'predicted_value': row['valor_previsto'],
                            'reason': 'Historicamente um mês de gastos elevados'
                        })
                
                results['high_spending_months'] = high_spending_predictions
        
        # Adiciona insights de padrões para melhorar as previsões
        insights = self.recommend_insights(data)
        
        # Combina com as previsões
        results['predictions'] = predictions.to_dict(orient='records')
        results['insights'] = insights
        results['combined_insights'] = self._combine_predictions_and_insights(predictions, insights)
        
        logger.info("Integração de análise de padrões e previsões concluída")
        return results
    
    def _combine_predictions_and_insights(self, predictions: pd.DataFrame, 
                                         insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Combina previsões com insights para recomendações mais completas.
        
        Args:
            predictions: DataFrame com previsões.
            insights: Lista de insights da análise de padrões.
            
        Returns:
            Lista de insights combinados.
        """
        combined = []
        
        # Para cada previsão, encontra insights relevantes
        for i, pred in predictions.iterrows():
            month = pred['mes'].month
            
            # Busca insights sazonais para este mês
            seasonal_insights = []
            for insight in insights:
                if insight['type'] == 'seasonality' and 'data' in insight:
                    data = insight['data']
                    if 'period_type' in data and data['period_type'] == 'month':
                        if data['peak_period'] == month:
                            seasonal_insights.append(insight)
            
            # Cria insight combinado
            if seasonal_insights:
                combined.append({
                    'month': pred['mes'],
                    'predicted_value': pred['valor_previsto'],
                    'confidence_interval': (
                        pred['valor_minimo'] if 'valor_minimo' in pred else None,
                        pred['valor_maximo'] if 'valor_maximo' in pred else None
                    ),
                    'seasonal_insights': seasonal_insights,
                    'recommendation': "Prepare-se para gastos sazonalmente elevados neste mês."
                })
            else:
                combined.append({
                    'month': pred['mes'],
                    'predicted_value': pred['valor_previsto'],
                    'confidence_interval': (
                        pred['valor_minimo'] if 'valor_minimo' in pred else None,
                        pred['valor_maximo'] if 'valor_maximo' in pred else None
                    ),
                    'seasonal_insights': [],
                    'recommendation': "Mês com padrão de gastos usual."
                })
        
        return combined 