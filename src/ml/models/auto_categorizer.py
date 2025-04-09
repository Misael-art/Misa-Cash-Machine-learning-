"""Modelo de machine learning para categorização automática de transações financeiras.

Este módulo implementa algoritmos para classificar transações em categorias
predefinidas com base em descrição, valor, data e outros atributos.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
import logging
import joblib
import os
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer  # Stemmer para português
import string

# Configuração de logging
logger = logging.getLogger(__name__)

# Certificar que os recursos NLTK estão disponíveis
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except Exception as e:
        logger.warning(f"Não foi possível baixar recursos NLTK: {e}")


class TextPreprocessor(BaseEstimator, TransformerMixin):
    """Preprocessador de texto para descrições de transações."""
    
    def __init__(self, language='portuguese', remove_stopwords=True, stem_words=True):
        """Inicializa o preprocessador.
        
        Args:
            language: Idioma para stopwords ('portuguese' ou 'english')
            remove_stopwords: Se deve remover stopwords
            stem_words: Se deve aplicar stemming
        """
        self.language = language
        self.remove_stopwords = remove_stopwords
        self.stem_words = stem_words
        
        # Inicializa recursos de linguagem
        try:
            self.stopwords = set(stopwords.words(language)) if remove_stopwords else set()
            self.stemmer = RSLPStemmer() if stem_words and language == 'portuguese' else None
        except Exception as e:
            logger.warning(f"Erro ao inicializar recursos de linguagem: {e}")
            self.stopwords = set()
            self.stemmer = None
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        """Transforma textos em versões normalizadas.
        
        Args:
            X: Array ou Series com textos
            
        Returns:
            Array com textos processados
        """
        if isinstance(X, pd.Series):
            texts = X.fillna('').values
        else:
            texts = np.array(X).flatten()
            texts = np.where(pd.isnull(texts), '', texts)
        
        processed_texts = []
        
        for text in texts:
            # Converte para string, caso não seja
            if not isinstance(text, str):
                text = str(text)
            
            # Converte para minúsculas
            text = text.lower()
            
            # Remove números e pontuação
            text = re.sub(r'\d+', ' NUM ', text)  # Substitui números por token NUM
            text = ''.join([c if c not in string.punctuation else ' ' for c in text])
            
            # Remove caracteres repetidos
            text = re.sub(r'(.)\1{2,}', r'\1\1', text)  # ex: 'aaaa' -> 'aa'
            
            # Tokenização
            tokens = word_tokenize(text, language=self.language)
            
            # Remove stopwords
            if self.remove_stopwords:
                tokens = [token for token in tokens if token not in self.stopwords]
            
            # Stemming
            if self.stem_words and self.stemmer:
                tokens = [self.stemmer.stem(token) for token in tokens]
            
            # Junta os tokens de volta em texto
            processed_text = ' '.join(tokens)
            
            # Adiciona à lista de resultados
            processed_texts.append(processed_text)
        
        return processed_texts


class AutoCategorizer:
    """Categorizador automático de transações financeiras.
    
    Utiliza algoritmos de classificação para automaticamente atribuir
    categorias a transações com base em sua descrição e atributos.
    """
    
    def __init__(self, model_type: str = 'random_forest', model_path: str = None):
        """Inicializa o categorizador.
        
        Args:
            model_type: Tipo de modelo ('random_forest', 'naive_bayes', 'logistic_regression')
            model_path: Caminho opcional para carregar um modelo salvo
        """
        self.model = None
        self.pipeline = None
        self.model_type = model_type
        self.categories = []
        self.category_map = {}  # Mapeamento de categoria -> índice
        self.reverse_category_map = {}  # Mapeamento de índice -> categoria
        self.is_fitted = False
        self.feature_importance = None
        self.min_confidence = 0.3  # Confiança mínima para classificar
        
        # Carrega o modelo se o caminho for fornecido
        if model_path and os.path.exists(model_path):
            self.load(model_path)
        else:
            self._setup_model()
    
    def _setup_model(self):
        """Configura o modelo com base no tipo especificado."""
        # Preprocessador de texto
        text_preprocessor = TextPreprocessor()
        
        # Vetorizador TF-IDF
        tfidf = TfidfVectorizer(
            max_features=1000,
            min_df=2,
            max_df=0.95,
            ngram_range=(1, 2)
        )
        
        # Pipeline de processamento de texto
        text_pipeline = Pipeline([
            ('preprocessor', text_preprocessor),
            ('tfidf', tfidf)
        ])
        
        # Transformadores para diferentes tipos de colunas
        transformers = [
            ('text', text_pipeline, 'descricao'),
            ('num', StandardScaler(), ['valor']),
        ]
        
        # Transformador de colunas
        col_transformer = ColumnTransformer(
            transformers=transformers,
            remainder='drop'
        )
        
        # Seleção do modelo de classificação
        if self.model_type == 'random_forest':
            classifier = RandomForestClassifier(
                n_estimators=100,
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=1,
                random_state=42,
                class_weight='balanced'
            )
        elif self.model_type == 'naive_bayes':
            classifier = MultinomialNB(alpha=0.1)
        elif self.model_type == 'logistic_regression':
            classifier = LogisticRegression(
                max_iter=1000,
                C=1.0,
                class_weight='balanced',
                random_state=42,
                solver='saga',
                multi_class='multinomial'
            )
        else:
            raise ValueError(f"Tipo de modelo não suportado: {self.model_type}")
        
        # Pipeline completa
        self.pipeline = Pipeline([
            ('features', col_transformer),
            ('classifier', classifier)
        ])
        
        logger.info(f"Categorizador automático ({self.model_type}) configurado")
    
    def _validate_data(self, data: pd.DataFrame):
        """Valida as colunas necessárias no DataFrame."""
        required_cols = ['descricao', 'valor']
        missing_cols = [col for col in required_cols if col not in data.columns]
        
        if missing_cols:
            error_msg = f"Colunas ausentes: {', '.join(missing_cols)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def load(self, model_path: str) -> bool:
        """Carrega o modelo e metadados do disco.
        
        Args:
            model_path: Caminho para o arquivo do modelo salvo.
            
        Returns:
            Booleano indicando sucesso.
        """
        try:
            model_data = joblib.load(model_path)
            self.pipeline = model_data.get('pipeline')
            self.model_type = model_data.get('model_type', self.model_type)
            self.categories = model_data.get('categories', [])
            self.category_map = model_data.get('category_map', {})
            self.reverse_category_map = model_data.get('reverse_category_map', {})
            self.is_fitted = model_data.get('is_fitted', False)
            self.feature_importance = model_data.get('feature_importance', None)
            self.min_confidence = model_data.get('min_confidence', 0.3)
            
            logger.info(f"Categorizador carregado com sucesso de {model_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar categorizador de {model_path}: {str(e)}")
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
                'pipeline': self.pipeline,
                'model_type': self.model_type,
                'categories': self.categories,
                'category_map': self.category_map,
                'reverse_category_map': self.reverse_category_map,
                'is_fitted': self.is_fitted,
                'feature_importance': self.feature_importance,
                'min_confidence': self.min_confidence
            }
            joblib.dump(model_data, model_path)
            logger.info(f"Modelo salvo com sucesso em {model_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar modelo em {model_path}: {str(e)}")
            return False
    
    def fit(self, data: pd.DataFrame, target_col: str = 'categoria') -> Dict[str, Any]:
        """Treina o modelo com dados históricos.
        
        Args:
            data: DataFrame com dados históricos de transações.
            target_col: Nome da coluna com as categorias.
            
        Returns:
            Dicionário com métricas de treinamento.
        """
        logger.info(f"Treinando categorizador automático ({self.model_type}) com {len(data)} registros")
        
        # Validar dados
        self._validate_data(data)
        
        if target_col not in data.columns:
            error_msg = f"Coluna de categoria '{target_col}' não encontrada"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Verifica se há dados suficientes
        if len(data) < 10:
            error_msg = f"Dados insuficientes para treino: {len(data)} registros (mínimo 10)"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Verifica se há categorias suficientes
        unique_categories = data[target_col].dropna().unique()
        if len(unique_categories) < 2:
            error_msg = f"Número insuficiente de categorias: {len(unique_categories)} (mínimo 2)"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Mapeia categorias para índices numéricos
        self.categories = sorted(unique_categories)
        self.category_map = {cat: i for i, cat in enumerate(self.categories)}
        self.reverse_category_map = {i: cat for i, cat in enumerate(self.categories)}
        
        # Prepara os dados
        X = data[['descricao', 'valor']].copy()
        y = data[target_col].map(self.category_map)
        
        # Treina o modelo
        self.pipeline.fit(X, y)
        self.is_fitted = True
        
        # Calcula a importância das features para modelos que suportam
        self._calculate_feature_importance()
        
        # Avalia o modelo usando validação cruzada
        try:
            cv_scores = cross_val_score(self.pipeline, X, y, cv=min(5, len(unique_categories)), 
                                        scoring='accuracy')
            accuracy = cv_scores.mean()
            std_dev = cv_scores.std()
            
            # Faz a previsão no conjunto de treino para estatísticas detalhadas
            y_pred = self.pipeline.predict(X)
            train_accuracy = accuracy_score(y, y_pred)
            f1 = f1_score(y, y_pred, average='weighted')
            
            # Gera relatório de classificação
            report = classification_report(y, y_pred, 
                                          target_names=self.categories, 
                                          output_dict=True)
            
            metrics = {
                'cv_accuracy': float(accuracy),
                'cv_std_dev': float(std_dev),
                'train_accuracy': float(train_accuracy),
                'f1_score': float(f1),
                'n_samples': len(data),
                'n_categories': len(unique_categories),
                'categories': self.categories,
                'classification_report': report
            }
            
            logger.info(f"Modelo treinado com sucesso. Acurácia CV: {accuracy:.4f} ± {std_dev:.4f}")
            return metrics
            
        except Exception as e:
            logger.warning(f"Erro ao avaliar modelo: {str(e)}")
            return {
                'success': True,
                'n_samples': len(data),
                'n_categories': len(unique_categories),
                'categories': self.categories
            }
    
    def _calculate_feature_importance(self):
        """Calcula a importância das features se o modelo suportar."""
        if not self.is_fitted:
            return
        
        try:
            # Para Random Forest, podemos obter feature importance
            if self.model_type == 'random_forest':
                classifier = self.pipeline.named_steps['classifier']
                feature_names = []
                
                # Tenta extrair nomes das features do pipeline
                try:
                    tfidf = self.pipeline.named_steps['features'].transformers_[0][1].named_steps['tfidf']
                    feature_names.extend(tfidf.get_feature_names_out())
                except:
                    pass
                
                # Se não conseguir nomes específicos, usar genéricos
                if not feature_names:
                    feature_names = [f"feature_{i}" for i in range(classifier.feature_importances_.shape[0])]
                
                # Armazena importância mapeada para nomes
                self.feature_importance = {
                    name: importance 
                    for name, importance in zip(
                        feature_names[:len(classifier.feature_importances_)], 
                        classifier.feature_importances_
                    )
                }
            
            # Para regressão logística, usar coeficientes
            elif self.model_type == 'logistic_regression':
                classifier = self.pipeline.named_steps['classifier']
                feature_names = []
                
                try:
                    tfidf = self.pipeline.named_steps['features'].transformers_[0][1].named_steps['tfidf']
                    feature_names.extend(tfidf.get_feature_names_out())
                except:
                    pass
                
                if not feature_names:
                    feature_names = [f"feature_{i}" for i in range(classifier.coef_.shape[1])]
                
                # Para multi-classe, pegamos a média dos coeficientes absolutos
                coef_abs = np.abs(classifier.coef_)
                mean_coef = np.mean(coef_abs, axis=0)
                
                self.feature_importance = {
                    name: importance 
                    for name, importance in zip(
                        feature_names[:len(mean_coef)], 
                        mean_coef
                    )
                }
        
        except Exception as e:
            logger.warning(f"Não foi possível calcular importância das features: {str(e)}")
            self.feature_importance = None
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Categoriza automaticamente as transações.
        
        Args:
            data: DataFrame com transações para categorizar.
            
        Returns:
            DataFrame com as transações e categorias preditas.
        """
        if not self.is_fitted:
            error_msg = "Modelo não treinado. Execute o método 'fit' primeiro."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Validar dados
        self._validate_data(data)
        
        # Cria uma cópia dos dados originais
        result_df = data.copy()
        
        try:
            # Prepara os dados para predição
            X = result_df[['descricao', 'valor']].copy()
            
            # Faz a predição
            y_pred = self.pipeline.predict(X)
            
            # Calcula as probabilidades para medir confiança
            probas = None
            if hasattr(self.pipeline, 'predict_proba'):
                probas = self.pipeline.predict_proba(X)
            
            # Mapeia índices para categorias
            predicted_categories = [self.reverse_category_map.get(idx, 'desconhecido') for idx in y_pred]
            result_df['categoria_sugerida'] = predicted_categories
            
            # Adiciona confiança da predição
            if probas is not None:
                # Pega a probabilidade mais alta para cada predição
                confidence = np.max(probas, axis=1)
                result_df['confianca_categoria'] = confidence
                
                # Marca baixa confiança
                result_df['baixa_confianca'] = confidence < self.min_confidence
            else:
                # Se não tiver probabilidades, assume confiança 1.0
                result_df['confianca_categoria'] = 1.0
                result_df['baixa_confianca'] = False
            
            # Adiciona top categorias alternativas
            if probas is not None and probas.shape[1] > 1:
                top_k = min(3, probas.shape[1])
                for i in range(len(result_df)):
                    top_indices = np.argsort(probas[i])[::-1][:top_k]
                    top_cats = [self.reverse_category_map.get(idx, 'desconhecido') for idx in top_indices]
                    top_probs = [probas[i, idx] for idx in top_indices]
                    
                    result_df.at[i, 'categorias_alternativas'] = [
                        {'categoria': cat, 'confianca': float(prob)} 
                        for cat, prob in zip(top_cats, top_probs)
                    ]
            
            logger.info(f"Categorização concluída para {len(data)} transações")
            return result_df
            
        except Exception as e:
            error_msg = f"Erro ao categorizar transações: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def suggest_categories(self, description: str, amount: float = None) -> List[Dict[str, Any]]:
        """Sugere categorias para uma descrição.
        
        Args:
            description: Descrição da transação.
            amount: Valor opcional da transação.
            
        Returns:
            Lista de categorias sugeridas com pontuações.
        """
        if not self.is_fitted:
            error_msg = "Modelo não treinado. Execute o método 'fit' primeiro."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        try:
            # Prepara um DataFrame para predição
            X = pd.DataFrame({
                'descricao': [description],
                'valor': [amount if amount is not None else 0.0]
            })
            
            # Faz a predição
            if hasattr(self.pipeline, 'predict_proba'):
                probas = self.pipeline.predict_proba(X)[0]
                
                # Organiza as categorias por probabilidade
                suggestions = []
                for i, prob in enumerate(probas):
                    if prob > 0.01:  # apenas sugestões com alguma probabilidade significativa
                        suggestions.append({
                            'categoria': self.reverse_category_map.get(i, 'desconhecido'),
                            'confianca': float(prob),
                            'recomendada': prob >= self.min_confidence
                        })
                
                # Ordena por probabilidade
                suggestions.sort(key=lambda x: x['confianca'], reverse=True)
                
                return suggestions
            else:
                # Se não tiver probabilidades, retorna apenas a predição
                y_pred = self.pipeline.predict(X)[0]
                category = self.reverse_category_map.get(y_pred, 'desconhecido')
                
                return [{
                    'categoria': category,
                    'confianca': 1.0,
                    'recomendada': True
                }]
                
        except Exception as e:
            error_msg = f"Erro ao sugerir categorias: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def set_min_confidence(self, confidence: float) -> None:
        """Define a confiança mínima para sugerir uma categoria.
        
        Args:
            confidence: Valor entre 0 e 1.
        """
        if confidence < 0 or confidence > 1:
            raise ValueError("Confiança deve estar entre 0 e 1")
        
        self.min_confidence = confidence
        logger.info(f"Confiança mínima ajustada para {confidence}")
    
    def get_feature_importance(self, top_n: int = 20) -> List[Dict[str, Any]]:
        """Retorna as features mais importantes para o modelo.
        
        Args:
            top_n: Número de features a retornar.
            
        Returns:
            Lista de dicionários com nome e importância das features.
        """
        if not self.is_fitted or not self.feature_importance:
            error_msg = "Modelo não treinado ou importância de features não disponível."
            logger.error(error_msg)
            return []
        
        # Ordena por importância
        sorted_features = sorted(
            self.feature_importance.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Limita ao top_n
        top_features = sorted_features[:top_n]
        
        # Formata o resultado
        return [{'feature': feat, 'importance': float(imp)} for feat, imp in top_features]
    
    def get_category_distribution(self) -> Dict[str, float]:
        """Retorna a distribuição de categorias no conjunto de treino.
        
        Returns:
            Dicionário com categoria -> porcentagem.
        """
        if not self.is_fitted:
            error_msg = "Modelo não treinado."
            logger.error(error_msg)
            return {}
        
        # Tenta extrair distribuição de classes do modelo
        try:
            if self.model_type == 'random_forest':
                classifier = self.pipeline.named_steps['classifier']
                class_counts = classifier.n_classes_
                total = sum(class_counts)
                
                distribution = {
                    self.reverse_category_map.get(i, 'desconhecido'): count/total 
                    for i, count in enumerate(class_counts)
                }
                
                return distribution
            else:
                # Para outros modelos, retornamos apenas as categorias
                return {cat: 1.0/len(self.categories) for cat in self.categories}
        except:
            # Fallback: distribuição uniforme
            return {cat: 1.0/len(self.categories) for cat in self.categories}
    
    def add_rule(self, pattern: str, category: str) -> bool:
        """Adiciona uma regra manual para categorização.
        
        Args:
            pattern: Expressão regular para correspondência na descrição.
            category: Categoria a ser atribuída.
            
        Returns:
            Booleano indicando sucesso.
        """
        logger.warning("Método add_rule não implementado nesta versão.")
        return False 