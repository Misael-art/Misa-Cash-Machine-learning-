"""
Ponto de entrada para execução direta do módulo ML.
"""
import argparse
import logging
import os
import sys
import pandas as pd
from .api.ml_service import MLService

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_parser():
    """Configura o parser de argumentos de linha de comando."""
    parser = argparse.ArgumentParser(description='Serviço de Machine Learning para o Misa-Cash')
    
    subparsers = parser.add_subparsers(dest='command', help='Comando a executar')
    
    # Parser para comando de treinamento
    train_parser = subparsers.add_parser('train', help='Treinar modelos de ML')
    train_parser.add_argument(
        '--data', '-d', 
        required=True,
        help='Caminho para arquivo CSV com dados de transações'
    )
    train_parser.add_argument(
        '--models', '-m',
        nargs='+',
        choices=['expense_predictor', 'anomaly_detector', 'category_classifier', 'all'],
        default=['all'],
        help='Modelos a serem treinados'
    )
    train_parser.add_argument(
        '--output', '-o',
        default='models',
        help='Diretório para salvar modelos treinados'
    )
    
    # Parser para comando de previsão
    predict_parser = subparsers.add_parser('predict', help='Fazer previsões com modelos treinados')
    predict_parser.add_argument(
        '--data', '-d',
        help='Caminho para arquivo CSV com dados de transações para análise'
    )
    predict_parser.add_argument(
        '--months', '-m',
        type=int,
        default=3,
        help='Número de meses para previsão de gastos'
    )
    predict_parser.add_argument(
        '--model-dir', '-md',
        default='models',
        help='Diretório com modelos treinados'
    )
    predict_parser.add_argument(
        '--output', '-o',
        default='predictions',
        help='Diretório para salvar resultados das previsões'
    )
    predict_parser.add_argument(
        '--type', '-t',
        choices=['expenses', 'anomalies', 'categories', 'insights', 'all'],
        default='all',
        help='Tipo de previsão a ser realizada'
    )
    
    return parser

def train_models(args):
    """Treina modelos de ML com dados fornecidos."""
    try:
        # Verificar se arquivo de dados existe
        if not os.path.exists(args.data):
            logger.error(f"Arquivo de dados não encontrado: {args.data}")
            return False
            
        # Carregar dados
        logger.info(f"Carregando dados de {args.data}")
        transactions = pd.read_csv(args.data)
        logger.info(f"Dados carregados: {len(transactions)} transações")
        
        # Criar diretório de saída se não existir
        os.makedirs(args.output, exist_ok=True)
        
        # Inicializar serviço ML
        ml_service = MLService(models_dir=args.output)
        
        # Preparar dados para modelos
        models_data = ml_service.prepare_data_for_models(transactions)
        
        # Determinar quais modelos treinar
        models_to_train = args.models
        if 'all' in models_to_train:
            models_to_train = ['expense_predictor', 'anomaly_detector', 'category_classifier']
        
        # Treinar modelos selecionados
        for model in models_to_train:
            if model == 'expense_predictor' and 'expense_predictor' in models_data:
                logger.info("Treinando preditor de gastos...")
                metrics = ml_service.train_expense_predictor(models_data['expense_predictor'])
                logger.info(f"Preditor de gastos treinado. MAE: {metrics['mae']:.2f}, RMSE: {metrics['rmse']:.2f}")
                
            elif model == 'anomaly_detector' and 'anomaly_detector' in models_data:
                logger.info("Treinando detector de anomalias...")
                result = ml_service.train_anomaly_detector(models_data['anomaly_detector'])
                logger.info(
                    f"Detector de anomalias treinado. "
                    f"Anomalias detectadas: {result['anomalies_detected']} "
                    f"({result['anomaly_ratio']*100:.1f}%)"
                )
                
            elif model == 'category_classifier' and 'category_classifier' in models_data:
                if models_data['category_classifier'].empty:
                    logger.warning("Dados para treinamento do classificador estão vazios. Pulando.")
                    continue
                    
                logger.info("Treinando classificador de categorias...")
                metrics = ml_service.train_category_classifier(models_data['category_classifier'])
                logger.info(
                    f"Classificador de categorias treinado. "
                    f"Acurácia: {metrics['accuracy']:.4f}"
                )
        
        logger.info(f"Todos os modelos selecionados foram treinados e salvos em {args.output}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao treinar modelos: {e}")
        return False

def make_predictions(args):
    """Faz previsões com modelos treinados."""
    try:
        # Verificar se diretório de modelos existe
        if not os.path.exists(args.model_dir):
            logger.error(f"Diretório de modelos não encontrado: {args.model_dir}")
            return False
            
        # Criar diretório de saída se não existir
        os.makedirs(args.output, exist_ok=True)
        
        # Inicializar serviço ML
        ml_service = MLService(models_dir=args.model_dir)
        
        # Verificar quais previsões fazer
        predictions_to_make = [args.type]
        if args.type == 'all':
            predictions_to_make = ['expenses', 'anomalies', 'categories', 'insights']
        
        # Para alguns tipos de previsão, precisamos de dados
        if ('anomalies' in predictions_to_make or 
            'categories' in predictions_to_make or 
            'insights' in predictions_to_make):
            
            if not args.data:
                logger.error("Arquivo de dados necessário para análise de anomalias, categorias ou insights")
                return False
                
            if not os.path.exists(args.data):
                logger.error(f"Arquivo de dados não encontrado: {args.data}")
                return False
                
            # Carregar dados
            logger.info(f"Carregando dados de {args.data}")
            transactions = pd.read_csv(args.data)
            logger.info(f"Dados carregados: {len(transactions)} transações")
        
        # Fazer previsões conforme solicitado
        for prediction_type in predictions_to_make:
            if prediction_type == 'expenses':
                if ml_service.expense_predictor is None:
                    logger.warning("Modelo de previsão de gastos não encontrado. Pulando.")
                    continue
                    
                logger.info(f"Gerando previsão de gastos para {args.months} meses...")
                result = ml_service.predict_monthly_expenses(months_ahead=args.months)
                
                # Salvar resultados
                predictions_df = pd.DataFrame(result['predictions'])
                predictions_path = os.path.join(args.output, 'expenses_prediction.csv')
                predictions_df.to_csv(predictions_path, index=False)
                
                # Salvar visualização se disponível
                if result['visualization']:
                    import base64
                    viz_path = os.path.join(args.output, 'expenses_chart.png')
                    with open(viz_path, 'wb') as f:
                        f.write(base64.b64decode(result['visualization']))
                        
                logger.info(f"Previsão de gastos salva em {predictions_path}")
                
            elif prediction_type == 'anomalies':
                if ml_service.anomaly_detector is None:
                    logger.warning("Modelo de detecção de anomalias não encontrado. Pulando.")
                    continue
                    
                logger.info("Detectando anomalias nas transações...")
                result = ml_service.detect_transaction_anomalies(transactions)
                
                # Salvar resultados
                anomalies_df = pd.DataFrame(result['anomalies'])
                if not anomalies_df.empty:
                    anomalies_path = os.path.join(args.output, 'anomalies.csv')
                    anomalies_df.to_csv(anomalies_path, index=False)
                    
                    # Salvar visualização se disponível
                    if result['visualization']:
                        import base64
                        viz_path = os.path.join(args.output, 'anomalies_chart.png')
                        with open(viz_path, 'wb') as f:
                            f.write(base64.b64decode(result['visualization']))
                            
                    logger.info(
                        f"Detectadas {result['anomalies_count']} anomalias em {result['total_transactions']} transações. "
                        f"Resultados salvos em {anomalies_path}"
                    )
                else:
                    logger.info("Nenhuma anomalia detectada nas transações.")
                    
            elif prediction_type == 'categories':
                if ml_service.category_classifier is None:
                    logger.warning("Modelo de classificação de categorias não encontrado. Pulando.")
                    continue
                    
                logger.info("Classificando transações...")
                result = ml_service.batch_classify_transactions(transactions)
                
                # Salvar resultados
                categories_path = os.path.join(args.output, 'predicted_categories.csv')
                result.to_csv(categories_path, index=False)
                
                logger.info(f"Classificação de categorias salva em {categories_path}")
                
            elif prediction_type == 'insights':
                logger.info("Gerando insights financeiros...")
                result = ml_service.generate_financial_insights(transactions)
                
                # Salvar resultados
                insights_path = os.path.join(args.output, 'financial_insights.txt')
                with open(insights_path, 'w') as f:
                    f.write("=== MÉTRICAS FINANCEIRAS ===\n")
                    f.write(f"Receita Total: R$ {result['metrics']['total_income']:.2f}\n")
                    f.write(f"Despesas Totais: R$ {result['metrics']['total_expenses']:.2f}\n")
                    f.write(f"Saldo: R$ {result['metrics']['balance']:.2f}\n")
                    f.write(f"Taxa de Economia: {result['metrics']['savings_rate']:.1f}%\n\n")
                    
                    f.write("=== INSIGHTS ===\n")
                    for insight in result['insights']:
                        f.write(f"- {insight}\n")
                    f.write("\n")
                    
                    f.write("=== RECOMENDAÇÕES ===\n")
                    for recommendation in result['recommendations']:
                        f.write(f"- {recommendation}\n")
                        
                logger.info(f"Insights financeiros salvos em {insights_path}")
                
                # Salvar também em JSON para facilitar uso programático
                import json
                insights_json_path = os.path.join(args.output, 'financial_insights.json')
                with open(insights_json_path, 'w') as f:
                    json.dump(result, f, indent=4)
        
        logger.info(f"Todas as previsões solicitadas foram concluídas e salvas em {args.output}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao fazer previsões: {e}")
        return False

def main():
    """Função principal."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 1
        
    if args.command == 'train':
        success = train_models(args)
    elif args.command == 'predict':
        success = make_predictions(args)
    else:
        parser.print_help()
        return 1
        
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main()) 