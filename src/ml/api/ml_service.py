"""Serviço central de Machine Learning para o Misa-Cash.

Este módulo fornece uma camada de serviço para coordenar os vários modelos
de Machine Learning, incluindo previsão de gastos, detecção de anomalias,
classificação de categorias e análise de padrões de gastos.
"""

import os
import logging
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional, Union

# Importa os modelos específicos
from ..models.expense_predictor import ExpensePredictor
from ..models.anomaly_detector import AnomalyDetector
from ..models.category_classifier import CategoryClassifier
from ..models.spending_pattern_analyzer import SpendingPatternAnalyzer

# Configuração de logging
logger = logging.getLogger(__name__)


class MLService:
    """Serviço central que coordena os modelos de ML do Misa-Cash.
    
    Essa classe fornece uma interface unificada para todas as funcionalidades
    de Machine Learning do sistema, incluindo treinamento de modelos, geração
    de previsões e insights financeiros personalizados.
    """
    
    def __init__(self, models_dir: str = "./models"):
        """Inicializa o serviço de ML.
        
        Args:
            models_dir: Diretório onde os modelos serão salvos/carregados.
        """
        self.models_dir = models_dir
        self._ensure_models_dir()
        
        # Inicializa os modelos
        self.expense_predictor = ExpensePredictor()
        self.anomaly_detector = AnomalyDetector()
        self.category_classifier = CategoryClassifier()
        self.pattern_analyzer = SpendingPatternAnalyzer()
        
        # Status de carregamento dos modelos
        self.models_loaded = {
            'expense_predictor': False,
            'anomaly_detector': False,
            'category_classifier': False,
            'pattern_analyzer': False
        }
        
        # Tenta carregar os modelos existentes
        self.load_models()
    
    def _ensure_models_dir(self) -> None:
        """Garante que o diretório de modelos existe."""
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
            logger.info(f"Diretório de modelos criado: {self.models_dir}")
    
    def load_models(self) -> bool:
        """Carrega todos os modelos treinados do disco.
        
        Returns:
            Booleano indicando sucesso parcial ou total.
        """
        self._ensure_models_dir()
        
        success = True
        
        # ExpensePredictor
        expense_predictor_path = os.path.join(self.models_dir, 'expense_predictor.joblib')
        if os.path.exists(expense_predictor_path):
            try:
                self.expense_predictor = joblib.load(expense_predictor_path)
                self.models_loaded['expense_predictor'] = True
                logger.info(f"Modelo de previsão de despesas carregado de {expense_predictor_path}")
            except Exception as e:
                logger.error(f"Erro ao carregar modelo de previsão: {str(e)}")
                success = False
        
        # AnomalyDetector
        anomaly_detector_path = os.path.join(self.models_dir, 'anomaly_detector.joblib')
        if os.path.exists(anomaly_detector_path):
            try:
                self.anomaly_detector = joblib.load(anomaly_detector_path)
                self.models_loaded['anomaly_detector'] = True
                logger.info(f"Modelo de detecção de anomalias carregado de {anomaly_detector_path}")
            except Exception as e:
                logger.error(f"Erro ao carregar modelo de anomalias: {str(e)}")
                success = False
        
        # CategoryClassifier
        category_classifier_path = os.path.join(self.models_dir, 'category_classifier.joblib')
        if os.path.exists(category_classifier_path):
            try:
                self.category_classifier = joblib.load(category_classifier_path)
                self.models_loaded['category_classifier'] = True
                logger.info(f"Modelo de classificação de categorias carregado de {category_classifier_path}")
            except Exception as e:
                logger.error(f"Erro ao carregar modelo de categorias: {str(e)}")
                success = False
                
        # SpendingPatternAnalyzer
        pattern_analyzer_path = os.path.join(self.models_dir, 'pattern_analyzer.joblib')
        if os.path.exists(pattern_analyzer_path):
            try:
                self.pattern_analyzer.load(pattern_analyzer_path)
                self.models_loaded['pattern_analyzer'] = True
                logger.info(f"Modelo de análise de padrões carregado de {pattern_analyzer_path}")
            except Exception as e:
                logger.error(f"Erro ao carregar modelo de análise de padrões: {str(e)}")
                success = False
        
        return success
    
    def save_models(self) -> bool:
        """Salva todos os modelos treinados no disco.
        
        Returns:
            Booleano indicando sucesso.
        """
        self._ensure_models_dir()
        
        success = True
        
        # ExpensePredictor
        if self.models_loaded['expense_predictor']:
            expense_predictor_path = os.path.join(self.models_dir, 'expense_predictor.joblib')
            try:
                joblib.dump(self.expense_predictor, expense_predictor_path)
                logger.info(f"Modelo de previsão de despesas salvo em {expense_predictor_path}")
            except Exception as e:
                logger.error(f"Erro ao salvar modelo de previsão: {str(e)}")
                success = False
        
        # AnomalyDetector
        if self.models_loaded['anomaly_detector']:
            anomaly_detector_path = os.path.join(self.models_dir, 'anomaly_detector.joblib')
            try:
                joblib.dump(self.anomaly_detector, anomaly_detector_path)
                logger.info(f"Modelo de detecção de anomalias salvo em {anomaly_detector_path}")
            except Exception as e:
                logger.error(f"Erro ao salvar modelo de anomalias: {str(e)}")
                success = False
        
        # CategoryClassifier
        if self.models_loaded['category_classifier']:
            category_classifier_path = os.path.join(self.models_dir, 'category_classifier.joblib')
            try:
                joblib.dump(self.category_classifier, category_classifier_path)
                logger.info(f"Modelo de classificação de categorias salvo em {category_classifier_path}")
            except Exception as e:
                logger.error(f"Erro ao salvar modelo de categorias: {str(e)}")
                success = False
                
        # SpendingPatternAnalyzer
        if self.models_loaded['pattern_analyzer']:
            pattern_analyzer_path = os.path.join(self.models_dir, 'pattern_analyzer.joblib')
            try:
                self.pattern_analyzer.save(pattern_analyzer_path)
                logger.info(f"Modelo de análise de padrões salvo em {pattern_analyzer_path}")
            except Exception as e:
                logger.error(f"Erro ao salvar modelo de análise de padrões: {str(e)}")
                success = False
        
        return success
    
    def prepare_data_for_models(self, transactions: pd.DataFrame) -> Dict[str, Any]:
        """Prepara os dados para treinamento e uso nos diferentes modelos.
        
        Args:
            transactions: DataFrame com transações brutas.
            
        Returns:
            Dicionário com DataFrames preparados para cada modelo.
        """
        # Verifica se temos as colunas mínimas necessárias
        required_cols = ['data', 'valor', 'descricao']
        missing_cols = [col for col in required_cols if col not in transactions.columns]
        if missing_cols:
            error_msg = f"Colunas ausentes: {', '.join(missing_cols)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Cria cópia para não alterar o original
        data = transactions.copy()
        
        # Converte data para datetime
        if not pd.api.types.is_datetime64_any_dtype(data['data']):
            data['data'] = pd.to_datetime(data['data'])
        
        # Adiciona coluna de mês para agregações
        data['mes'] = pd.to_datetime(data['data']).dt.to_period('M').dt.to_timestamp()
        
        # Prepara dados para o ExpensePredictor (agregado por mês)
        expense_data_agg = data.groupby('mes').agg({
            'valor': 'sum'
        }).reset_index()
        
        # Adiciona categorias se não existirem
        if 'categoria' not in data.columns:
            # Se não temos categoria, usamos o modelo para predizer
            if self.models_loaded['category_classifier']:
                data['categoria'] = self.category_classifier.predict(data['descricao'])
            else:
                data['categoria'] = 'DESCONHECIDO'
                
        # Prepara dados para detecção de anomalias (sem agregação)
        anomaly_data = data[['data', 'valor', 'descricao']].copy()
        if 'categoria' in data.columns:
            anomaly_data['categoria'] = data['categoria']
        
        # Dados para classificação de categorias
        classifier_data = data[['descricao', 'categoria']].copy()
        
        return {
            'expense_predictor': expense_data_agg,
            'anomaly_detector': anomaly_data,
            'category_classifier': classifier_data,
            'pattern_analyzer': data,
            'raw_data': data
        }
    
    def train_expense_predictor(self, data: pd.DataFrame) -> Dict[str, float]:
        """Treina o modelo de previsão de gastos.
        
        Args:
            data: DataFrame com dados preparados para o modelo de previsão.
            
        Returns:
            Dicionário com métricas de desempenho do modelo.
        """
        logger.info(f"Treinando modelo de previsão de gastos com {len(data)} registros")
        
        metrics = self.expense_predictor.train(data)
        self.models_loaded['expense_predictor'] = True
        
        # Salva o modelo treinado
        expense_predictor_path = os.path.join(self.models_dir, 'expense_predictor.joblib')
        joblib.dump(self.expense_predictor, expense_predictor_path)
        logger.info(f"Modelo de previsão de gastos salvo em {expense_predictor_path}")
        
        return metrics
    
    def train_anomaly_detector(self, data: pd.DataFrame) -> Dict[str, float]:
        """Treina o modelo de detecção de anomalias.
        
        Args:
            data: DataFrame com dados para o detector de anomalias.
            
        Returns:
            Dicionário com métricas de desempenho.
        """
        logger.info(f"Treinando modelo de detecção de anomalias com {len(data)} registros")
        
        metrics = self.anomaly_detector.fit(data)
        self.models_loaded['anomaly_detector'] = True
        
        # Salva o modelo treinado
        anomaly_detector_path = os.path.join(self.models_dir, 'anomaly_detector.joblib')
        joblib.dump(self.anomaly_detector, anomaly_detector_path)
        logger.info(f"Modelo de detecção de anomalias salvo em {anomaly_detector_path}")
        
        return metrics
    
    def train_category_classifier(self, data: pd.DataFrame) -> Dict[str, float]:
        """Treina o modelo de classificação de categorias.
        
        Args:
            data: DataFrame com textos e categorias para treino.
            
        Returns:
            Dicionário com métricas de desempenho.
        """
        # Verifica se temos as colunas necessárias
        if 'descricao' not in data.columns or 'categoria' not in data.columns:
            raise ValueError("Dados devem ter colunas 'descricao' e 'categoria'")
        
        logger.info(f"Treinando modelo de classificação de categorias com {len(data)} registros")
        
        # Treina o modelo
        metrics = self.category_classifier.train(
            X=data['descricao'], 
            y=data['categoria']
        )
        self.models_loaded['category_classifier'] = True
        
        # Salva o modelo treinado
        category_classifier_path = os.path.join(self.models_dir, 'category_classifier.joblib')
        joblib.dump(self.category_classifier, category_classifier_path)
        logger.info(f"Modelo de classificação de categorias salvo em {category_classifier_path}")
        
        return metrics
        
    def train_pattern_analyzer(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Treina o analisador de padrões de gastos.
        
        Args:
            data: DataFrame com transações.
            
        Returns:
            Dicionário com resultados da análise.
        """
        logger.info(f"Treinando analisador de padrões de gastos com {len(data)} registros")
        
        # Realiza a análise completa
        patterns = self.pattern_analyzer.find_patterns(data)
        self.models_loaded['pattern_analyzer'] = True
        
        # Salva o modelo treinado
        pattern_analyzer_path = os.path.join(self.models_dir, 'pattern_analyzer.joblib')
        self.pattern_analyzer.save(pattern_analyzer_path)
        logger.info(f"Modelo de análise de padrões salvo em {pattern_analyzer_path}")
        
        return patterns
    
    def train_all_models(self, transactions: pd.DataFrame) -> Dict[str, Any]:
        """Treina todos os modelos com o mesmo conjunto de dados.
        
        Args:
            transactions: DataFrame com transações.
            
        Returns:
            Dicionário com resultados do treinamento de cada modelo.
        """
        logger.info(f"Iniciando treinamento de todos os modelos com {len(transactions)} transações")
        
        # Preparar dados para cada modelo
        data_dict = self.prepare_data_for_models(transactions)
        
        results = {}
        
        # Treina modelo de previsão de gastos
        try:
            expense_metrics = self.train_expense_predictor(data_dict['expense_predictor'])
            results['expense_predictor'] = expense_metrics
        except Exception as e:
            logger.error(f"Erro ao treinar modelo de previsão: {str(e)}")
            results['expense_predictor'] = {"error": str(e)}
        
        # Treina detector de anomalias
        try:
            anomaly_metrics = self.train_anomaly_detector(data_dict['anomaly_detector'])
            results['anomaly_detector'] = anomaly_metrics
        except Exception as e:
            logger.error(f"Erro ao treinar detector de anomalias: {str(e)}")
            results['anomaly_detector'] = {"error": str(e)}
        
        # Treina classificador de categorias
        try:
            if 'categoria' in transactions.columns:
                category_metrics = self.train_category_classifier(data_dict['category_classifier'])
                results['category_classifier'] = category_metrics
            else:
                logger.warning("Coluna 'categoria' ausente, pulando treinamento do classificador")
                results['category_classifier'] = {"error": "Dados de categoria ausentes"}
        except Exception as e:
            logger.error(f"Erro ao treinar classificador de categorias: {str(e)}")
            results['category_classifier'] = {"error": str(e)}
            
        # Treina analisador de padrões
        try:
            pattern_results = self.train_pattern_analyzer(data_dict['pattern_analyzer'])
            results['pattern_analyzer'] = pattern_results
        except Exception as e:
            logger.error(f"Erro ao treinar analisador de padrões: {str(e)}")
            results['pattern_analyzer'] = {"error": str(e)}
        
        # Salva todos os modelos
        self.save_models()
        
        logger.info(f"Treinamento de todos os modelos concluído com sucesso")
        return results
    
    def predict_expenses(self, months: int = 3, 
                       transactions: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Prevê gastos para os próximos meses.
        
        Args:
            months: Número de meses futuros para prever.
            transactions: DataFrame opcional com transações recentes para melhorar a previsão.
            
        Returns:
            Dicionário com previsões de gastos.
        """
        if not self.models_loaded['expense_predictor']:
            logger.error("Modelo de previsão de gastos não está carregado")
            raise RuntimeError("Modelo de previsão de gastos não está treinado ou carregado")
        
        if transactions is not None:
            prepared_data = self.prepare_data_for_models(transactions)
            expense_data = prepared_data['expense_predictor']
            # Atualiza o modelo com dados recentes, sem retreinar completamente
            self.expense_predictor.update(expense_data)
        
        logger.info(f"Gerando previsão de gastos para os próximos {months} meses")
        
        predictions = self.expense_predictor.predict(months)
        
        # Formata resultados
        result = {
            'predictions': predictions,
            'confidence_intervals': self.expense_predictor.get_confidence_intervals(predictions),
            'trend': self.expense_predictor.get_trend(predictions)
        }
        
        return result
    
    def analyze_spending_patterns(self, transactions: pd.DataFrame,
                                include_predictions: bool = True) -> Dict[str, Any]:
        """Analisa padrões de gastos e gera insights.
        
        Args:
            transactions: DataFrame com transações.
            include_predictions: Se deve incluir integração com previsões.
            
        Returns:
            Dicionário com resultados da análise de padrões.
        """
        if not self.models_loaded['pattern_analyzer']:
            # Se não temos um modelo carregado, fazemos análise sob demanda
            logger.info("Modelo de análise de padrões não estava carregado, executando análise sob demanda")
            patterns = self.pattern_analyzer.find_patterns(transactions)
            self.models_loaded['pattern_analyzer'] = True
        else:
            # Se já temos um modelo, usamos ele
            patterns = self.pattern_analyzer.find_patterns(transactions)
        
        # Insights de padrões
        insights = self.pattern_analyzer.recommend_insights(transactions)
        
        results = {
            'patterns': patterns,
            'insights': insights
        }
        
        # Integra com previsões se solicitado e temos um preditor carregado
        if include_predictions and self.models_loaded['expense_predictor']:
            integrated_results = self.pattern_analyzer.integrate_with_expense_predictor(
                transactions, self.expense_predictor)
            results['integrated_analysis'] = integrated_results
        
        return results
    
    def detect_anomalies(self, transactions: pd.DataFrame) -> Dict[str, Any]:
        """Detecta transações anômalas.
        
        Args:
            transactions: DataFrame com transações para analisar.
            
        Returns:
            Dicionário com anomalias detectadas e pontuações.
        """
        if not self.models_loaded['anomaly_detector']:
            logger.error("Modelo de detecção de anomalias não está carregado")
            raise RuntimeError("Modelo de detecção de anomalias não está treinado ou carregado")
        
        logger.info(f"Detectando anomalias em {len(transactions)} transações")
        
        prepared_data = self.prepare_data_for_models(transactions)
        anomaly_data = prepared_data['anomaly_detector']
        
        anomalies = self.anomaly_detector.detect(anomaly_data)
        
        # Concatena resultados com dados originais para retornar transações completas
        result_df = pd.concat([transactions, 
                             pd.DataFrame({'is_anomaly': anomalies['is_anomaly'],
                                          'anomaly_score': anomalies['anomaly_score']})], axis=1)
        
        # Filtra apenas anomalias e converte para dicionário
        anomalies_df = result_df[result_df['is_anomaly'] == True]
        anomalies_dict = anomalies_df.to_dict(orient='records')
        
        result = {
            'anomalies': anomalies_dict,
            'anomaly_count': len(anomalies_dict),
            'total_transactions': len(transactions),
            'anomaly_percentage': (len(anomalies_dict) / len(transactions)) * 100 if len(transactions) > 0 else 0
        }
        
        return result
    
    def classify_transaction_category(self, description: str) -> Dict[str, Any]:
        """Classifica a categoria de uma transação com base na descrição.
        
        Args:
            description: Descrição da transação.
            
        Returns:
            Dicionário com categoria sugerida e confiança.
        """
        if not self.models_loaded['category_classifier']:
            logger.error("Modelo de classificação de categorias não está carregado")
            raise RuntimeError("Modelo de classificação de categorias não está treinado ou carregado")
        
        logger.info(f"Classificando categoria para transação: {description}")
        
        result = self.category_classifier.classify(description)
        
        return result
    
    def classify_transactions(self, transactions: pd.DataFrame) -> List[Dict[str, Any]]:
        """Classifica categorias para várias transações.
        
        Args:
            transactions: DataFrame com transações a classificar.
            
        Returns:
            Lista de dicionários com transações e suas categorias sugeridas.
        """
        if not self.models_loaded['category_classifier']:
            logger.error("Modelo de classificação de categorias não está carregado")
            raise RuntimeError("Modelo de classificação de categorias não está treinado ou carregado")
        
        if 'descricao' not in transactions.columns:
            logger.error("Coluna 'descricao' não encontrada nos dados")
            raise ValueError("Os dados devem conter a coluna 'descricao'")
        
        logger.info(f"Classificando categorias para {len(transactions)} transações")
        
        results = []
        for _, row in transactions.iterrows():
            description = row['descricao']
            classification = self.category_classifier.classify(description)
            
            result = {**row.to_dict(), **classification}
            results.append(result)
        
        return results
    
    def generate_insights(self, transactions: pd.DataFrame) -> List[Dict[str, Any]]:
        """Gera insights financeiros personalizados a partir dos dados.
        
        Args:
            transactions: DataFrame com histórico de transações.
            
        Returns:
            Lista de insights financeiros.
        """
        logger.info(f"Gerando insights para {len(transactions)} transações")
        
        insights = []
        
        # Preparar dados
        prepared_data = self.prepare_data_for_models(transactions)
        data = prepared_data['raw_data']
        
        # Adiciona colunas de tempo
        data['mes'] = data['data'].dt.to_period('M')
        data['mes_str'] = data['mes'].astype(str)
        
        # 1. Insight sobre categorias com maiores gastos
        try:
            category_spending = data.groupby('categoria')['valor'].sum().reset_index()
            category_spending = category_spending.sort_values('valor', ascending=False)
            
            if not category_spending.empty:
                top_category = category_spending.iloc[0]['categoria']
                top_amount = category_spending.iloc[0]['valor']
                total_spent = category_spending['valor'].sum()
                percentage = (top_amount / total_spent) * 100
                
                insights.append({
                    'type': 'top_category',
                    'title': 'Categoria com Maior Gasto',
                    'description': f"Sua categoria com maior gasto é '{top_category}', representando {percentage:.1f}% do total.",
                    'importance': 'high',
                    'data': {
                        'category': top_category,
                        'amount': float(top_amount),
                        'percentage': float(percentage)
                    }
                })
        except Exception as e:
            logger.error(f"Erro ao gerar insight de categoria com maior gasto: {str(e)}")
        
        # 2. Insight sobre tendência de gastos
        try:
            monthly_spending = data.groupby('mes')['valor'].sum().reset_index()
            monthly_spending['mes'] = monthly_spending['mes'].dt.to_timestamp()
            
            if len(monthly_spending) > 2:
                last_month = monthly_spending.iloc[-1]['valor']
                prev_month = monthly_spending.iloc[-2]['valor']
                change_pct = ((last_month - prev_month) / prev_month) * 100
                
                trend_desc = "aumentaram" if change_pct > 0 else "diminuíram"
                
                insights.append({
                    'type': 'monthly_trend',
                    'title': 'Tendência de Gastos Mensais',
                    'description': f"Seus gastos {trend_desc} {abs(change_pct):.1f}% em relação ao mês anterior.",
                    'importance': 'high' if abs(change_pct) > 20 else 'medium',
                    'data': {
                        'current_month': float(last_month),
                        'previous_month': float(prev_month),
                        'change_percent': float(change_pct)
                    }
                })
        except Exception as e:
            logger.error(f"Erro ao gerar insight de tendência mensal: {str(e)}")
        
        # 3. Insight sobre gastos recorrentes
        try:
            # Identifica possíveis gastos recorrentes (mesma descrição e valores similares)
            descriptions = data.groupby('descricao')['valor'].agg(['count', 'mean', 'std']).reset_index()
            recurring = descriptions[(descriptions['count'] > 2) & (descriptions['std'] / descriptions['mean'] < 0.1)]
            
            if not recurring.empty:
                top_recurring = recurring.sort_values('mean', ascending=False).iloc[0]
                recurring_name = top_recurring['descricao']
                recurring_value = top_recurring['mean']
                
                insights.append({
                    'type': 'recurring_expense',
                    'title': 'Gasto Recorrente Identificado',
                    'description': f"Identificamos um gasto recorrente em '{recurring_name}' com valor médio de R$ {recurring_value:.2f}.",
                    'importance': 'medium',
                    'data': {
                        'description': recurring_name,
                        'average_amount': float(recurring_value),
                        'occurrences': int(top_recurring['count'])
                    }
                })
        except Exception as e:
            logger.error(f"Erro ao gerar insight de gastos recorrentes: {str(e)}")
        
        # 4. Insight sobre anomalias se o modelo estiver treinado
        if self.models_loaded['anomaly_detector']:
            try:
                anomalies_result = self.detect_anomalies(transactions)
                
                if anomalies_result['anomaly_count'] > 0:
                    insights.append({
                        'type': 'anomalies',
                        'title': 'Transações Atípicas Detectadas',
                        'description': f"Detectamos {anomalies_result['anomaly_count']} transações com padrões atípicos.",
                        'importance': 'high',
                        'data': {
                            'anomaly_count': anomalies_result['anomaly_count'],
                            'anomaly_percentage': float(anomalies_result['anomaly_percentage']),
                            'top_anomalies': anomalies_result['anomalies'][:3] if len(anomalies_result['anomalies']) > 3 else anomalies_result['anomalies']
                        }
                    })
            except Exception as e:
                logger.error(f"Erro ao gerar insight de anomalias: {str(e)}")
        
        # 5. Insight sobre previsão de gastos futuros se o modelo estiver treinado
        if self.models_loaded['expense_predictor']:
            try:
                predictions = self.predict_expenses(3, transactions)
                
                next_month_forecast = predictions['predictions'][0]['valor']
                current_month = data[data['mes'] == data['mes'].max()]['valor'].sum()
                
                change_pct = ((next_month_forecast - current_month) / current_month) * 100 if current_month != 0 else 0
                
                forecast_desc = "aumentar" if change_pct > 5 else "diminuir" if change_pct < -5 else "se manter estável"
                
                insights.append({
                    'type': 'forecast',
                    'title': 'Previsão para o Próximo Mês',
                    'description': f"Seus gastos devem {forecast_desc} no próximo mês. Previsão: R$ {next_month_forecast:.2f}.",
                    'importance': 'high' if abs(change_pct) > 15 else 'medium',
                    'data': {
                        'forecast': float(next_month_forecast),
                        'current': float(current_month),
                        'change_percent': float(change_pct)
                    }
                })
            except Exception as e:
                logger.error(f"Erro ao gerar insight de previsão: {str(e)}")
        
        # 6. Insight sobre dias da semana com maiores gastos
        try:
            weekday_spending = data.groupby('dia_semana')['valor'].sum().reset_index()
            
            if not weekday_spending.empty:
                top_weekday = weekday_spending.sort_values('valor', ascending=False).iloc[0]['dia_semana']
                
                insights.append({
                    'type': 'weekday_pattern',
                    'title': 'Dia da Semana com Maior Gasto',
                    'description': f"Você tende a gastar mais às {top_weekday}s.",
                    'importance': 'low',
                    'data': {
                        'weekday': top_weekday
                    }
                })
        except Exception as e:
            logger.error(f"Erro ao gerar insight de padrão semanal: {str(e)}")
        
        # Ordena insights por importância
        importance_order = {'high': 0, 'medium': 1, 'low': 2}
        insights.sort(key=lambda x: importance_order.get(x.get('importance', 'low'), 3))
        
        return insights
    
    def get_service_health(self) -> Dict[str, Any]:
        """Verifica o estado de saúde do serviço ML.
        
        Returns:
            Dicionário com status dos modelos e outras informações.
        """
        models_status = {name: "loaded" if status else "not_loaded" 
                         for name, status in self.models_loaded.items()}
        
        return {
            'status': 'online',
            'models': models_status,
            'models_dir': self.models_dir,
            'timestamp': datetime.now().isoformat()
        } 