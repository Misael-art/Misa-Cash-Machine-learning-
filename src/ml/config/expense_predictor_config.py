"""
Configurações para o modelo de predição de despesas.

Este módulo contém as configurações padrão e parâmetros para o treinamento,
avaliação e uso do modelo de predição de despesas.
"""

# Configurações de treinamento
TRAINING_CONFIG = {
    # Proporção dos dados a serem usados para teste (0.0 a 1.0)
    'test_size': 0.2,
    
    # Semente aleatória para reprodutibilidade
    'random_state': 42,
    
    # Número de validações cruzadas para a seleção de modelo
    'cv_folds': 5,
    
    # Se deve normalizar os recursos numéricos
    'normalize_features': True,
    
    # Lista de recursos temporais a serem extraídos
    'temporal_features': ['month', 'day_of_week', 'is_weekend', 'is_month_start', 'is_month_end'],
}

# Configurações de modelos
MODEL_CONFIGS = {
    'linear': {
        'fit_intercept': True,
    },
    
    'ridge': {
        'alpha': 1.0,
        'fit_intercept': True,
        'max_iter': 1000,
        'tol': 0.001,
        'solver': 'auto',
    },
    
    'random_forest': {
        'n_estimators': 100,
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'max_features': 'auto',
        'bootstrap': True,
        'n_jobs': -1,
    },
    
    'gradient_boosting': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 3,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'subsample': 1.0,
        'max_features': None,
    },
}

# Configurações para predição
PREDICTION_CONFIG = {
    # Número de meses a serem previstos por padrão
    'default_forecast_periods': 3,
    
    # Se deve calcular intervalos de confiança
    'calculate_confidence_intervals': True,
    
    # Nível de confiança (percentual) para os intervalos de confiança
    'confidence_level': 0.95,
}

# Configurações para avaliação de modelo
EVALUATION_CONFIG = {
    # Métricas a serem calculadas durante a avaliação
    'metrics': ['mse', 'rmse', 'mae', 'r2', 'mape'],
    
    # Se deve gerar visualizações durante a avaliação
    'generate_plots': True,
    
    # Tipos de gráficos a serem gerados
    'plot_types': ['actual_vs_predicted', 'residuals', 'feature_importance'],
}

# Configurações de caminho para modelos salvos
PATH_CONFIG = {
    # Diretório padrão onde os modelos são salvos
    'model_dir': 'models/saved',
    
    # Extensão de arquivo padrão para modelos salvos
    'model_extension': '.joblib',
    
    # Prefixo para nomes de arquivos de modelo
    'model_prefix': 'expense_predictor_',
} 