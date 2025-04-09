"""
Endpoints da API de Machine Learning para o Misa-Cash.
"""
from flask import Blueprint, request, jsonify
import pandas as pd
import logging
import json
from .ml_service import MLService

logger = logging.getLogger(__name__)

# Criar blueprint para API de ML
ml_api = Blueprint('ml_api', __name__, url_prefix='/api/ml')

# Instanciar serviço de ML
ml_service = MLService(models_dir='models')

@ml_api.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar status do serviço ML."""
    return jsonify({
        'status': 'ok',
        'models': {
            'expense_predictor': ml_service.expense_predictor is not None,
            'anomaly_detector': ml_service.anomaly_detector is not None,
            'category_classifier': ml_service.category_classifier is not None
        }
    })

@ml_api.route('/train', methods=['POST'])
def train_models():
    """Endpoint para treinar modelos com dados fornecidos."""
    try:
        # Validar requisição
        if not request.is_json:
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        
        if 'transactions' not in data:
            return jsonify({'error': 'Dados de transações não fornecidos'}), 400
            
        # Converter transações para DataFrame
        transactions = pd.DataFrame(data['transactions'])
        
        # Preparar dados para diferentes modelos
        models_data = ml_service.prepare_data_for_models(transactions)
        
        # Treinar modelos conforme solicitado
        results = {}
        models_to_train = data.get('models', ['expense_predictor', 'anomaly_detector', 'category_classifier'])
        
        if 'expense_predictor' in models_to_train and 'expense_predictor' in models_data:
            expense_metrics = ml_service.train_expense_predictor(
                models_data['expense_predictor'],
                target_column=data.get('expense_target_column', 'amount'),
                model_type=data.get('expense_model_type', 'random_forest')
            )
            results['expense_predictor'] = expense_metrics
            
        if 'anomaly_detector' in models_to_train and 'anomaly_detector' in models_data:
            anomaly_info = ml_service.train_anomaly_detector(
                models_data['anomaly_detector'],
                detector_type=data.get('anomaly_detector_type', 'isolation_forest'),
                contamination=data.get('contamination', 0.05)
            )
            results['anomaly_detector'] = anomaly_info
            
        if 'category_classifier' in models_to_train and 'category_classifier' in models_data:
            category_metrics = ml_service.train_category_classifier(
                models_data['category_classifier'],
                description_column=data.get('description_column', 'description'),
                category_column=data.get('category_column', 'category'),
                classifier_type=data.get('classifier_type', 'random_forest')
            )
            results['category_classifier'] = category_metrics
            
        logger.info(f"Modelos treinados com sucesso: {', '.join(results.keys())}")
            
        return jsonify({
            'status': 'success',
            'message': f"Modelos treinados com sucesso: {', '.join(results.keys())}",
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Erro ao treinar modelos: {e}")
        return jsonify({'error': str(e)}), 500

@ml_api.route('/predict/expenses', methods=['GET'])
def predict_expenses():
    """Endpoint para prever gastos futuros."""
    try:
        # Obter parâmetros
        months_ahead = int(request.args.get('months', 3))
        
        if months_ahead < 1 or months_ahead > 24:
            return jsonify({'error': 'Número de meses deve estar entre 1 e 24'}), 400
            
        # Fazer previsão
        result = ml_service.predict_monthly_expenses(months_ahead=months_ahead)
        
        return jsonify({
            'status': 'success',
            'predictions': result['predictions'],
            'visualization': result['visualization']
        })
        
    except Exception as e:
        logger.error(f"Erro ao prever gastos: {e}")
        return jsonify({'error': str(e)}), 500

@ml_api.route('/detect/anomalies', methods=['POST'])
def detect_anomalies():
    """Endpoint para detectar anomalias em transações."""
    try:
        # Validar requisição
        if not request.is_json:
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        
        if 'transactions' not in data:
            return jsonify({'error': 'Dados de transações não fornecidos'}), 400
            
        # Converter transações para DataFrame
        transactions = pd.DataFrame(data['transactions'])
        
        # Detectar anomalias
        result = ml_service.detect_transaction_anomalies(transactions)
        
        return jsonify({
            'status': 'success',
            'total_transactions': result['total_transactions'],
            'anomalies_count': result['anomalies_count'],
            'anomalies': result['anomalies'],
            'visualization': result['visualization']
        })
        
    except Exception as e:
        logger.error(f"Erro ao detectar anomalias: {e}")
        return jsonify({'error': str(e)}), 500

@ml_api.route('/classify/transaction', methods=['POST'])
def classify_transaction():
    """Endpoint para classificar categoria de uma transação."""
    try:
        # Validar requisição
        if not request.is_json:
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        
        if 'description' not in data:
            return jsonify({'error': 'Descrição da transação não fornecida'}), 400
            
        # Classificar transação
        result = ml_service.classify_transaction_category(data['description'])
        
        return jsonify({
            'status': 'success',
            'description': result['description'],
            'category': result['suggested_category'],
            'confidence': result['confidence'],
            'top_categories': result['top_categories']
        })
        
    except Exception as e:
        logger.error(f"Erro ao classificar transação: {e}")
        return jsonify({'error': str(e)}), 500

@ml_api.route('/classify/batch', methods=['POST'])
def classify_batch():
    """Endpoint para classificar categorias de um lote de transações."""
    try:
        # Validar requisição
        if not request.is_json:
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        
        if 'transactions' not in data:
            return jsonify({'error': 'Dados de transações não fornecidos'}), 400
            
        # Converter transações para DataFrame
        transactions = pd.DataFrame(data['transactions'])
        
        description_column = data.get('description_column', 'description')
        
        if description_column not in transactions.columns:
            return jsonify({
                'error': f"Coluna de descrição '{description_column}' não encontrada nas transações"
            }), 400
            
        # Classificar transações
        result = ml_service.batch_classify_transactions(
            transactions,
            description_column=description_column
        )
        
        # Preparar resultados (incluir apenas colunas relevantes)
        output_cols = [description_column, 'predicted_category']
        if 'prediction_confidence' in result.columns:
            output_cols.append('prediction_confidence')
            
        # Incluir id se disponível
        if 'id' in result.columns:
            output_cols.insert(0, 'id')
            
        classifications = result[output_cols].to_dict('records')
        
        return jsonify({
            'status': 'success',
            'total': len(classifications),
            'classifications': classifications
        })
        
    except Exception as e:
        logger.error(f"Erro ao classificar lote de transações: {e}")
        return jsonify({'error': str(e)}), 500

@ml_api.route('/analyze/spending', methods=['POST'])
def analyze_spending():
    """Endpoint para analisar padrões de gastos."""
    try:
        # Validar requisição
        if not request.is_json:
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        
        if 'transactions' not in data:
            return jsonify({'error': 'Dados de transações não fornecidos'}), 400
            
        # Converter transações para DataFrame
        transactions = pd.DataFrame(data['transactions'])
        
        # Analisar padrões de gastos
        result = ml_service.analyze_spending_patterns(transactions)
        
        return jsonify({
            'status': 'success',
            'total_expenses': result['total_expenses'],
            'total_transactions': result['total_transactions'],
            'category_summary': result['category_summary'],
            'visualizations': result['visualizations']
        })
        
    except Exception as e:
        logger.error(f"Erro ao analisar padrões de gastos: {e}")
        return jsonify({'error': str(e)}), 500

@ml_api.route('/insights', methods=['POST'])
def get_insights():
    """Endpoint para obter insights financeiros."""
    try:
        # Validar requisição
        if not request.is_json:
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        
        if 'transactions' not in data:
            return jsonify({'error': 'Dados de transações não fornecidos'}), 400
            
        # Converter transações para DataFrame
        transactions = pd.DataFrame(data['transactions'])
        
        # Gerar insights
        result = ml_service.generate_financial_insights(transactions)
        
        return jsonify({
            'status': 'success',
            'metrics': result['metrics'],
            'insights': result['insights'],
            'recommendations': result['recommendations']
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar insights financeiros: {e}")
        return jsonify({'error': str(e)}), 500 