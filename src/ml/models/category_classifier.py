"""
Modelo para classificação automática de transações em categorias.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any
import logging
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import matplotlib.pyplot as plt
from datetime import datetime
import os
import re
import unicodedata
import seaborn as sns

logger = logging.getLogger(__name__)

class CategoryClassifier:
    """Modelo para classificação automática de transações em categorias."""
    
    def __init__(self, classifier_type: str = 'random_forest'):
        """
        Inicializa o classificador de categorias.
        
        Args:
            classifier_type: Tipo de classificador a ser usado
                ('random_forest', 'logistic_regression', 'naive_bayes', 'svm')
        """
        self.classifier_type = classifier_type
        self.pipeline = None
        self.classes_ = None
        self.trained = False
        self.metrics = {}
        
        # Configurar modelo
        self._setup_model()
        
    def _setup_model(self) -> None:
        """Configura o modelo com base no tipo escolhido."""
        # Definir o classificador base
        if self.classifier_type == 'random_forest':
            classifier = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                n_jobs=-1,
                random_state=42
            )
        elif self.classifier_type == 'logistic_regression':
            classifier = LogisticRegression(
                C=1.0,
                solver='lbfgs',
                max_iter=200,
                multi_class='auto',
                n_jobs=-1,
                random_state=42
            )
        elif self.classifier_type == 'naive_bayes':
            classifier = MultinomialNB(alpha=1.0)
        elif self.classifier_type == 'svm':
            classifier = SVC(
                C=1.0,
                kernel='linear',
                probability=True,
                random_state=42
            )
        else:
            raise ValueError(f"Tipo de classificador '{self.classifier_type}' não reconhecido")
            
        # Configurar pipeline completo
        self.pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(
                max_features=5000,
                min_df=2,
                max_df=0.85,
                ngram_range=(1, 2),
                sublinear_tf=True
            )),
            ('classifier', classifier)
        ])
        
        logger.info(f"Classificador '{self.classifier_type}' configurado")
        
    def preprocess_text(self, text: str) -> str:
        """
        Pré-processa texto para classificação.
        
        Args:
            text: Texto a ser processado
            
        Returns:
            Texto processado
        """
        if not isinstance(text, str):
            return ""
            
        # Converter para minúsculas
        text = text.lower()
        
        # Remover acentos
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        
        # Remover caracteres especiais
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remover números
        text = re.sub(r'\d+', '', text)
        
        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
        
    def train(self, X: pd.Series, y: pd.Series, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Treina o modelo com os dados fornecidos.
        
        Args:
            X: Series com descrições de transações
            y: Series com categorias
            test_size: Proporção de dados para teste
            
        Returns:
            Dicionário com métricas de avaliação
        """
        if len(X) != len(y):
            raise ValueError(f"Número de amostras inconsistente: X({len(X)}) vs y({len(y)})")
            
        logger.info(f"Treinando classificador '{self.classifier_type}' com {len(X)} transações")
        
        try:
            # Pré-processar textos
            X_processed = X.apply(self.preprocess_text)
            
            # Dividir em treino e teste
            X_train, X_test, y_train, y_test = train_test_split(
                X_processed, y, test_size=test_size, random_state=42, stratify=y
            )
            
            # Treinar modelo
            self.pipeline.fit(X_train, y_train)
            self.trained = True
            
            # Obter classes para predição
            self.classes_ = self.pipeline.classes_
            
            # Avaliar modelo
            y_pred = self.pipeline.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)
            
            self.metrics = {
                'accuracy': accuracy,
                'classification_report': report,
                'test_samples': len(X_test)
            }
            
            logger.info(f"Modelo treinado com acurácia de {accuracy:.4f}")
            
            return self.metrics
            
        except Exception as e:
            logger.error(f"Erro ao treinar classificador: {e}")
            raise
            
    def predict(self, descriptions: Union[str, List[str], pd.Series]) -> np.ndarray:
        """
        Classifica transações com base em suas descrições.
        
        Args:
            descriptions: Texto ou lista de textos de descrições
            
        Returns:
            Array com categorias preditas
        """
        if not self.trained:
            raise ValueError("Classificador não foi treinado ainda")
            
        try:
            # Converter entrada para formato adequado
            if isinstance(descriptions, str):
                descriptions = [descriptions]
            elif isinstance(descriptions, pd.Series):
                descriptions = descriptions.tolist()
                
            # Pré-processar textos
            processed_descriptions = [self.preprocess_text(desc) for desc in descriptions]
            
            # Fazer predição
            predictions = self.pipeline.predict(processed_descriptions)
            
            logger.info(f"Classificadas {len(predictions)} transações")
            
            return predictions
            
        except Exception as e:
            logger.error(f"Erro ao classificar transações: {e}")
            raise
            
    def predict_proba(self, descriptions: Union[str, List[str], pd.Series]) -> np.ndarray:
        """
        Retorna probabilidades de cada categoria para transações.
        
        Args:
            descriptions: Texto ou lista de textos de descrições
            
        Returns:
            Array com probabilidades para cada categoria
        """
        if not self.trained:
            raise ValueError("Classificador não foi treinado ainda")
            
        try:
            # Converter entrada para formato adequado
            if isinstance(descriptions, str):
                descriptions = [descriptions]
            elif isinstance(descriptions, pd.Series):
                descriptions = descriptions.tolist()
                
            # Pré-processar textos
            processed_descriptions = [self.preprocess_text(desc) for desc in descriptions]
            
            # Obter probabilidades
            probas = self.pipeline.predict_proba(processed_descriptions)
            
            logger.info(f"Calculadas probabilidades para {len(probas)} transações")
            
            return probas
            
        except Exception as e:
            logger.error(f"Erro ao calcular probabilidades: {e}")
            raise
            
    def get_top_features(self, n_features: int = 20) -> Dict[str, List[Tuple[str, float]]]:
        """
        Retorna as features mais importantes para cada categoria.
        
        Args:
            n_features: Número de features a retornar por categoria
            
        Returns:
            Dicionário com features mais importantes por categoria
        """
        if not self.trained:
            raise ValueError("Classificador não foi treinado ainda")
            
        try:
            # Obter o vectorizer e o classificador do pipeline
            vectorizer = self.pipeline.named_steps['vectorizer']
            classifier = self.pipeline.named_steps['classifier']
            
            # Obter recursos (palavras/tokens)
            feature_names = vectorizer.get_feature_names_out()
            
            # Para classificadores com coeficientes
            if hasattr(classifier, 'coef_'):
                coefficients = classifier.coef_
                
                top_features = {}
                for i, category in enumerate(self.classes_):
                    # Obter os N termos mais importantes para esta categoria
                    indices = np.argsort(coefficients[i])[::-1][:n_features]
                    top_terms = [(feature_names[idx], coefficients[i][idx]) for idx in indices]
                    top_features[category] = top_terms
                    
            # Para classificadores baseados em árvores
            elif hasattr(classifier, 'feature_importances_'):
                importances = classifier.feature_importances_
                
                # Obter os N termos mais importantes (global)
                indices = np.argsort(importances)[::-1][:n_features]
                top_terms = [(feature_names[idx], importances[idx]) for idx in indices]
                
                # Como importâncias são globais, usamos a mesma para todas as categorias
                top_features = {category: top_terms for category in self.classes_}
                
            else:
                raise AttributeError("Classificador não suporta extração de features importantes")
                
            return top_features
            
        except Exception as e:
            logger.error(f"Erro ao obter features importantes: {e}")
            raise
            
    def save_model(self, filepath: str) -> None:
        """
        Salva o modelo treinado em arquivo.
        
        Args:
            filepath: Caminho para salvar o modelo
        """
        if not self.trained:
            raise ValueError("Classificador não foi treinado ainda")
            
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Salvar modelo e metadados
            joblib.dump({
                'pipeline': self.pipeline,
                'classifier_type': self.classifier_type,
                'classes_': self.classes_,
                'metrics': self.metrics,
                'trained_date': datetime.now().isoformat()
            }, filepath)
            
            logger.info(f"Classificador salvo em {filepath}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar classificador: {e}")
            raise
            
    @classmethod
    def load_model(cls, filepath: str) -> 'CategoryClassifier':
        """
        Carrega um modelo previamente salvo.
        
        Args:
            filepath: Caminho do arquivo do modelo
            
        Returns:
            Instância do CategoryClassifier carregada
        """
        try:
            # Carregar modelo e metadados
            data = joblib.load(filepath)
            
            # Criar nova instância
            classifier = cls(classifier_type=data['classifier_type'])
            classifier.pipeline = data['pipeline']
            classifier.classes_ = data['classes_']
            classifier.metrics = data['metrics']
            classifier.trained = True
            
            logger.info(f"Classificador carregado de {filepath}")
            
            return classifier
            
        except Exception as e:
            logger.error(f"Erro ao carregar classificador: {e}")
            raise
            
    def plot_confusion_matrix(self, X_test: pd.Series, y_test: pd.Series,
                             figsize: Tuple[int, int] = (12, 10)) -> plt.Figure:
        """
        Gera matriz de confusão para o modelo.
        
        Args:
            X_test: Dados de teste (descrições)
            y_test: Categorias reais
            figsize: Tamanho da figura
            
        Returns:
            Objeto Figure do matplotlib
        """
        if not self.trained:
            raise ValueError("Classificador não foi treinado ainda")
            
        try:
            # Pré-processar textos
            X_processed = X_test.apply(self.preprocess_text)
            
            # Fazer predições
            y_pred = self.pipeline.predict(X_processed)
            
            # Calcular matriz de confusão
            cm = confusion_matrix(y_test, y_pred, labels=self.classes_)
            
            # Normalizar
            cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            
            # Criar figura
            fig, ax = plt.subplots(figsize=figsize)
            
            # Plotar matriz
            sns.heatmap(
                cm_normalized, 
                annot=True, 
                fmt='.2f',
                cmap='Blues',
                xticklabels=self.classes_,
                yticklabels=self.classes_
            )
            
            ax.set_title('Matriz de Confusão Normalizada')
            ax.set_ylabel('Categoria Real')
            ax.set_xlabel('Categoria Predita')
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao gerar matriz de confusão: {e}")
            raise
            
    def plot_feature_importance(self, category: Optional[str] = None, 
                              top_n: int = 10) -> plt.Figure:
        """
        Gera gráfico de importância de features.
        
        Args:
            category: Categoria específica (ou None para importância global)
            top_n: Número de features mais importantes a exibir
            
        Returns:
            Objeto Figure do matplotlib
        """
        if not self.trained:
            raise ValueError("Classificador não foi treinado ainda")
            
        try:
            top_features = self.get_top_features(n_features=top_n)
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 8))
            
            if category is not None:
                if category not in top_features:
                    raise ValueError(f"Categoria '{category}' não reconhecida")
                    
                # Extrair features e importâncias
                features = [term for term, _ in top_features[category]]
                importances = [imp for _, imp in top_features[category]]
                
                # Plotar
                y_pos = range(len(features))
                ax.barh(y_pos, importances)
                ax.set_yticks(y_pos)
                ax.set_yticklabels(features)
                ax.set_title(f'Top {top_n} Features para Categoria: {category}')
                
            else:
                # Para importância global, usamos a primeira categoria (arbitrária)
                # quando as importâncias são específicas por classe
                category = list(top_features.keys())[0]
                
                # Extrair features e importâncias
                features = [term for term, _ in top_features[category]]
                importances = [imp for _, imp in top_features[category]]
                
                # Plotar
                y_pos = range(len(features))
                ax.barh(y_pos, importances)
                ax.set_yticks(y_pos)
                ax.set_yticklabels(features)
                ax.set_title(f'Top {top_n} Features Globais')
                
            ax.set_xlabel('Importância Relativa')
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de importância: {e}")
            raise 