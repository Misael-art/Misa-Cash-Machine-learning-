"""
Módulo de Agendamento de Tarefas de Machine Learning.

Este módulo implementa agendamento periódico de tarefas usando Celery e Redis:
- Retreinamento semanal de modelos de previsão
- Análise diária de padrões de gastos
- Detecção horária de anomalias
- Geração diária de insights financeiros
"""

import os
import logging
import json
import time
import threading
from datetime import datetime, timedelta
import redis
from celery import Celery, Task
from celery.signals import task_failure, task_success, worker_ready
from celery.schedules import crontab

from src.ml.models.expense_predictor import ExpensePredictor
from src.ml.models.pattern_analyzer import SpendingPatternAnalyzer
from src.ml.models.anomaly_detector import AnomalyDetector
from src.ml.models.insight_generator import InsightGenerator
from src.ml.utils.notification_manager import NotificationManager

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuração Redis
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

# Configuração Celery
BROKER_URL = os.environ.get('CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')

# Inicialização do Celery
app = Celery('ml_tasks', broker=BROKER_URL, backend=RESULT_BACKEND)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=False,
)

# Configuração de tarefas agendadas
app.conf.beat_schedule = {
    'train_models_weekly': {
        'task': 'src.ml.api.scheduler.train_models',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Domingo às 2:00 AM
        'args': ()
    },
    'analyze_patterns_daily': {
        'task': 'src.ml.api.scheduler.analyze_spending_patterns',
        'schedule': crontab(hour=4, minute=0),  # Diariamente às 4:00 AM
        'args': ()
    },
    'detect_anomalies_hourly': {
        'task': 'src.ml.api.scheduler.detect_spending_anomalies',
        'schedule': crontab(minute=15),  # A cada hora (XX:15)
        'args': ()
    },
    'generate_insights_daily': {
        'task': 'src.ml.api.scheduler.generate_insights',
        'schedule': crontab(hour=5, minute=0),  # Diariamente às 5:00 AM
        'args': ()
    }
}

# Classe base para tarefas com mecanismo de lock
class LockingTask(Task):
    """
    Tarefa base com mecanismo de travamento para evitar execuções simultâneas.
    
    Usa Redis para implementar um sistema de trava que garante que apenas uma 
    instância de cada tarefa seja executada por vez, independente do número de workers.
    """
    abstract = True  # Não registra como tarefa
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
    
    def get_lock_id(self, task_id, args=None, kwargs=None):
        """Gera um ID de trava baseado no nome da tarefa e argumentos."""
        task_name = self.__class__.__name__
        return f"lock:{task_name}"
    
    def acquire_lock(self, lock_id, timeout=3600):  # 1 hora de timeout por padrão
        """
        Tenta adquirir uma trava para a execução da tarefa.
        
        Args:
            lock_id: ID da trava
            timeout: Tempo em segundos até a trava expirar automaticamente
            
        Returns:
            bool: True se a trava foi adquirida com sucesso, False caso contrário
        """
        lock_acquired = self.redis_client.set(
            lock_id, 
            datetime.now().isoformat(),
            nx=True,  # Só define se não existir
            ex=timeout  # Expira após timeout segundos
        )
        return bool(lock_acquired)
    
    def release_lock(self, lock_id):
        """Libera uma trava para permitir nova execução."""
        self.redis_client.delete(lock_id)
    
    def __call__(self, *args, **kwargs):
        """Executa a tarefa com mecanismo de travamento."""
        lock_id = self.get_lock_id(self.request.id, args, kwargs)
        
        # Tenta adquirir trava
        if not self.acquire_lock(lock_id):
            logger.info(f"Tarefa {self.__class__.__name__} já está em execução. Ignorando.")
            return {"status": "skipped", "reason": "task_already_running"}
        
        logger.info(f"Iniciando execução da tarefa {self.__class__.__name__}")
        try:
            # Executa a tarefa
            result = super(LockingTask, self).__call__(*args, **kwargs)
            return result
        finally:
            # Libera a trava ao finalizar (mesmo em caso de erro)
            self.release_lock(lock_id)
            logger.info(f"Finalizando execução da tarefa {self.__class__.__name__}")

# Handlers para eventos de tarefas
@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    """Handler para falhas em tarefas."""
    logger.error(f"Tarefa {sender.name} com ID {task_id} falhou: {str(exception)}")

@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    """Handler para sucesso em tarefas."""
    task_name = sender.name if hasattr(sender, 'name') else 'Unknown'
    logger.info(f"Tarefa {task_name} concluída com sucesso: {result}")

@worker_ready.connect
def worker_ready_handler(**kwargs):
    """Handler para quando o worker estiver pronto."""
    logger.info("Worker Celery inicializado e pronto para processar tarefas")

# Definição das tarefas agendadas
@app.task(base=LockingTask, bind=True)
def train_models(self):
    """
    Tarefa para treinar/atualizar os modelos de previsão.
    
    Executa semanalmente para incorporar novos dados às previsões.
    """
    logger.info("Iniciando treinamento dos modelos de previsão")
    notification_manager = NotificationManager()
    start_time = time.time()
    
    try:
        # Notifica início do treinamento
        for user_id in [1, 2, 3]:  # Em produção, buscar usuários ativos da base
            notification_manager.send_model_training_notification(
                user_id=user_id,
                status='in_progress'
            )
        
        predictor = ExpensePredictor()
        metrics = predictor.train_models()
        
        duration = time.time() - start_time
        
        # Notifica sucesso
        for user_id in [1, 2, 3]:  # Em produção, buscar usuários ativos da base
            notification_manager.send_model_training_notification(
                user_id=user_id,
                status='success',
                metrics=metrics,
                duration=duration
            )
        
        return {
            "status": "success",
            "duration": f"{duration:.2f}s",
            "metrics": metrics
        }
        
    except Exception as e:
        logger.exception("Erro durante o treinamento dos modelos")
        
        # Notifica erro
        for user_id in [1, 2, 3]:  # Em produção, buscar usuários da base
            notification_manager.send_model_training_notification(
                user_id=user_id,
                status='error',
                metrics={"error": str(e)}
            )
        
        return {
            "status": "error",
            "error": str(e)
        }

@app.task(base=LockingTask, bind=True)
def analyze_spending_patterns(self):
    """
    Tarefa para analisar padrões de gastos dos usuários.
    
    Executa diariamente para identificar padrões em transações recentes.
    """
    logger.info("Iniciando análise de padrões de gastos")
    notification_manager = NotificationManager()
    
    try:
        analyzer = SpendingPatternAnalyzer()
        
        # Obtém todos os IDs de usuário ativos
        # Em produção, buscar da base de dados
        user_ids = [1, 2, 3]
        
        results = {}
        
        for user_id in user_ids:
            logger.info(f"Analisando padrões para usuário {user_id}")
            
            # Analisa padrões para o usuário atual
            patterns = analyzer.analyze_patterns(user_id=user_id)
            
            if patterns and len(patterns) > 0:
                # Notifica sobre os padrões encontrados
                notification_manager.send_pattern_notification(
                    user_id=user_id,
                    patterns=patterns
                )
                
                results[f"user_{user_id}"] = {
                    "patterns_found": len(patterns),
                    "patterns": patterns
                }
            else:
                results[f"user_{user_id}"] = {
                    "patterns_found": 0
                }
        
        return {
            "status": "success",
            "results": results
        }
        
    except Exception as e:
        logger.exception("Erro durante a análise de padrões de gastos")
        return {
            "status": "error",
            "error": str(e)
        }

@app.task(base=LockingTask, bind=True)
def detect_spending_anomalies(self):
    """
    Tarefa para detectar anomalias nas transações dos usuários.
    
    Executa a cada hora para identificar transações suspeitas o mais rápido possível.
    """
    logger.info("Iniciando detecção de anomalias em transações")
    notification_manager = NotificationManager()
    
    try:
        detector = AnomalyDetector()
        
        # Obtém todos os IDs de usuário ativos
        # Em produção, buscar da base de dados
        user_ids = [1, 2, 3]
        
        results = {}
        anomalies_detected = False
        
        for user_id in user_ids:
            logger.info(f"Detectando anomalias para usuário {user_id}")
            
            # Verifica anomalias para o usuário atual
            anomalies = detector.detect_anomalies(user_id=user_id)
            
            if anomalies and len(anomalies) > 0:
                # Notifica sobre as anomalias encontradas
                notification_manager.send_anomaly_notification(
                    user_id=user_id,
                    anomalies=anomalies
                )
                
                results[f"user_{user_id}"] = {
                    "anomalies_found": len(anomalies),
                    "anomalies": anomalies
                }
                
                anomalies_detected = True
            else:
                results[f"user_{user_id}"] = {
                    "anomalies_found": 0
                }
        
        return {
            "status": "success",
            "anomalies_detected": anomalies_detected,
            "results": results
        }
        
    except Exception as e:
        logger.exception("Erro durante a detecção de anomalias")
        return {
            "status": "error",
            "error": str(e)
        }

@app.task(base=LockingTask, bind=True)
def generate_insights(self):
    """
    Tarefa para gerar insights financeiros para os usuários.
    
    Executa diariamente para produzir recomendações personalizadas.
    """
    logger.info("Iniciando geração de insights financeiros")
    notification_manager = NotificationManager()
    
    try:
        generator = InsightGenerator()
        
        # Obtém todos os IDs de usuário ativos
        # Em produção, buscar da base de dados
        user_ids = [1, 2, 3]
        
        results = {}
        
        for user_id in user_ids:
            logger.info(f"Gerando insights para usuário {user_id}")
            
            # Gera insights para o usuário atual
            insights = generator.generate_insights(user_id=user_id)
            
            if insights and len(insights) > 0:
                # Notifica sobre os insights gerados
                notification_manager.send_insight_notification(
                    user_id=user_id,
                    insights=insights
                )
                
                results[f"user_{user_id}"] = {
                    "insights_generated": len(insights),
                    "insights": insights
                }
            else:
                results[f"user_{user_id}"] = {
                    "insights_generated": 0
                }
        
        return {
            "status": "success",
            "results": results
        }
        
    except Exception as e:
        logger.exception("Erro durante a geração de insights")
        return {
            "status": "error",
            "error": str(e)
        }

def run_task_by_name(task_name, *args, **kwargs):
    """
    Executa uma tarefa agendada sob demanda pelo nome.
    
    Args:
        task_name: Nome da tarefa a ser executada
        
    Returns:
        dict: Resultado da execução da tarefa
    """
    logger.info(f"Executando tarefa sob demanda: {task_name}")
    
    task_map = {
        'train_models': train_models,
        'analyze_spending_patterns': analyze_spending_patterns,
        'detect_spending_anomalies': detect_spending_anomalies,
        'generate_insights': generate_insights
    }
    
    if task_name in task_map:
        return task_map[task_name].delay(*args, **kwargs)
    else:
        logger.error(f"Tarefa não encontrada: {task_name}")
        raise ValueError(f"Tarefa '{task_name}' não encontrada no agendador")

def start_scheduler():
    """
    Inicia o agendador Celery (beat) e worker.
    
    Deve ser chamado para iniciar o processamento de tarefas agendadas.
    """
    from celery.bin import worker, beat
    
    # Inicia o worker em um thread separado
    def start_worker():
        worker_instance = worker.worker(app=app)
        worker_instance.run(loglevel='INFO', concurrency=2)
    
    # Inicia o beat em um thread separado
    def start_beat():
        beat_instance = beat.beat(app=app)
        beat_instance.run(loglevel='INFO')
    
    # Inicia threads para worker e beat
    threading.Thread(target=start_worker, daemon=True).start()
    threading.Thread(target=start_beat, daemon=True).start()
    
    logger.info("Agendador Celery iniciado (worker e beat)")

if __name__ == "__main__":
    # Quando executado diretamente, inicia o agendador
    start_scheduler() 