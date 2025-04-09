"""
Gerenciador de Notificações para Sistema de ML.

Este módulo centraliza o envio de notificações e alertas para diferentes canais,
como e-mail, aplicativo móvel, ou notificações do sistema, relacionados a
operações de machine learning como treinamento de modelos, detecção de anomalias,
padrões de gastos e insights.
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import requests
from requests.exceptions import RequestException

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurações de APIs para notificações
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000/api')
API_KEY = os.environ.get('API_KEY', '')
EMAIL_SERVICE_URL = os.environ.get('EMAIL_SERVICE_URL', 'http://localhost:8025/send')


class NotificationManager:
    """
    Gerencia o envio de notificações para diferentes canais.
    
    Implementa métodos para enviar alertas sobre eventos relacionados a
    machine learning, como conclusão de treinamento, detecção de anomalias,
    identificação de padrões e geração de insights.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de notificações."""
        self.api_base_url = API_BASE_URL
        self.api_key = API_KEY
        self.email_service_url = EMAIL_SERVICE_URL
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        logger.info("Gerenciador de notificações inicializado")
    
    def send_model_training_notification(self, 
                                         user_id: int, 
                                         status: str, 
                                         metrics: Dict[str, Any] = None,
                                         duration: float = None) -> bool:
        """
        Envia notificação sobre treinamento de modelo.
        
        Args:
            user_id: ID do usuário para receber a notificação
            status: Status do treinamento ('success', 'error', 'in_progress')
            metrics: Métricas de desempenho do modelo treinado
            duration: Duração do treinamento em segundos
            
        Returns:
            True se a notificação foi enviada com sucesso, False caso contrário
        """
        if metrics is None:
            metrics = {}
        
        notification_data = {
            'user_id': user_id,
            'type': 'model_training',
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': {
                'metrics': metrics
            }
        }
        
        if duration is not None:
            notification_data['details']['duration'] = f"{duration:.2f}s"
        
        # Determina o título e mensagem baseado no status
        if status == 'success':
            notification_data['title'] = 'Modelo de previsão atualizado'
            notification_data['message'] = ('Seu modelo de previsão de despesas foi '
                                          'atualizado com sucesso e está pronto para uso.')
        elif status == 'error':
            notification_data['title'] = 'Falha na atualização do modelo'
            notification_data['message'] = ('Ocorreu um erro ao tentar atualizar seu '
                                          'modelo de previsão. Nossa equipe foi notificada.')
        else:
            notification_data['title'] = 'Atualização de modelo em andamento'
            notification_data['message'] = ('Estamos atualizando seu modelo de previsão '
                                          'com suas transações mais recentes.')
        
        return self._send_notification(notification_data)
    
    def send_anomaly_notification(self, 
                                 user_id: int, 
                                 anomalies: List[Dict[str, Any]],
                                 total_anomalies: int = None) -> bool:
        """
        Envia notificação sobre anomalias detectadas.
        
        Args:
            user_id: ID do usuário para receber a notificação
            anomalies: Lista de anomalias detectadas
            total_anomalies: Número total de anomalias (se diferente do tamanho da lista)
            
        Returns:
            True se a notificação foi enviada com sucesso, False caso contrário
        """
        if total_anomalies is None:
            total_anomalies = len(anomalies)
        
        # Limita o número de anomalias enviadas para não sobrecarregar a notificação
        anomalies_to_send = anomalies[:3]
        
        notification_data = {
            'user_id': user_id,
            'type': 'anomaly_detection',
            'status': 'alert',
            'timestamp': datetime.now().isoformat(),
            'title': f'Detectamos {total_anomalies} transações incomuns',
            'message': 'Algumas transações apresentam padrões incomuns e podem requerer sua atenção.',
            'details': {
                'anomalies': anomalies_to_send,
                'total_anomalies': total_anomalies
            }
        }
        
        # Envia notificação prioritária para anomalias
        notification_data['priority'] = 'high'
        
        # Também envia um e-mail sobre anomalias severas
        if any(a.get('severity', 0) > 0.7 for a in anomalies):
            self._send_email_alert(
                user_id,
                "ALERTA: Transações suspeitas detectadas",
                f"Detectamos {total_anomalies} transações com padrões incomuns em sua conta. "
                f"Por favor, verifique estas transações o mais rápido possível."
            )
        
        return self._send_notification(notification_data)
    
    def send_pattern_notification(self, 
                                 user_id: int, 
                                 patterns: List[Dict[str, Any]],
                                 total_patterns: int = None) -> bool:
        """
        Envia notificação sobre padrões de gastos identificados.
        
        Args:
            user_id: ID do usuário para receber a notificação
            patterns: Lista de padrões identificados
            total_patterns: Número total de padrões (se diferente do tamanho da lista)
            
        Returns:
            True se a notificação foi enviada com sucesso, False caso contrário
        """
        if total_patterns is None:
            total_patterns = len(patterns)
        
        # Limita o número de padrões enviados
        patterns_to_send = patterns[:3]
        
        notification_data = {
            'user_id': user_id,
            'type': 'spending_patterns',
            'status': 'info',
            'timestamp': datetime.now().isoformat(),
            'title': 'Novos padrões de gastos identificados',
            'message': f'Identificamos {total_patterns} padrões em suas despesas que podem ajudar no planejamento financeiro.',
            'details': {
                'patterns': patterns_to_send,
                'total_patterns': total_patterns
            }
        }
        
        return self._send_notification(notification_data)
    
    def send_insight_notification(self, 
                                 user_id: int, 
                                 insights: List[Dict[str, Any]],
                                 total_insights: int = None) -> bool:
        """
        Envia notificação sobre insights financeiros.
        
        Args:
            user_id: ID do usuário para receber a notificação
            insights: Lista de insights financeiros
            total_insights: Número total de insights (se diferente do tamanho da lista)
            
        Returns:
            True se a notificação foi enviada com sucesso, False caso contrário
        """
        if total_insights is None:
            total_insights = len(insights)
        
        # Limita o número de insights enviados
        insights_to_send = insights[:3]
        
        notification_data = {
            'user_id': user_id,
            'type': 'financial_insights',
            'status': 'info',
            'timestamp': datetime.now().isoformat(),
            'title': 'Novos insights financeiros disponíveis',
            'message': f'Temos {total_insights} novos insights sobre suas finanças que podem te ajudar a economizar.',
            'details': {
                'insights': insights_to_send,
                'total_insights': total_insights
            }
        }
        
        return self._send_notification(notification_data)
    
    def _send_notification(self, notification_data: Dict[str, Any]) -> bool:
        """
        Envia uma notificação para o serviço de notificações.
        
        Args:
            notification_data: Dados da notificação a ser enviada
            
        Returns:
            True se a notificação foi enviada com sucesso, False caso contrário
        """
        try:
            endpoint = f"{self.api_base_url}/notifications/send"
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=notification_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Notificação enviada com sucesso: {notification_data['type']}")
                return True
            else:
                logger.warning(
                    f"Falha ao enviar notificação: {response.status_code} - {response.text}"
                )
                return False
                
        except RequestException as e:
            logger.error(f"Erro ao enviar notificação: {str(e)}")
            
            # Fallback: salvar notificação localmente se API indisponível
            self._save_notification_locally(notification_data)
            return False
    
    def _send_email_alert(self, 
                          user_id: int, 
                          subject: str, 
                          body: str) -> bool:
        """
        Envia e-mail de alerta para o usuário.
        
        Args:
            user_id: ID do usuário destinatário
            subject: Assunto do e-mail
            body: Corpo do e-mail
            
        Returns:
            True se o e-mail foi enviado com sucesso, False caso contrário
        """
        try:
            # Obtenção de e-mail do usuário deveria vir de um serviço de dados de usuário
            # Aqui simplificamos com um e-mail fixo + user_id (em produção, buscar da base)
            email = f"user{user_id}@example.com"
            
            email_data = {
                'to': email,
                'subject': subject,
                'body': body,
                'is_html': False
            }
            
            response = requests.post(
                self.email_service_url,
                headers={'Content-Type': 'application/json'},
                json=email_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"E-mail de alerta enviado para usuário {user_id}")
                return True
            else:
                logger.warning(
                    f"Falha ao enviar e-mail: {response.status_code} - {response.text}"
                )
                return False
                
        except RequestException as e:
            logger.error(f"Erro ao enviar e-mail: {str(e)}")
            return False
    
    def _save_notification_locally(self, notification_data: Dict[str, Any]) -> None:
        """
        Salva notificação localmente quando serviço de notificações está indisponível.
        
        Args:
            notification_data: Dados da notificação a ser salva
        """
        try:
            # Assegura que diretório existe
            os.makedirs('logs/notifications', exist_ok=True)
            
            # Cria nome de arquivo baseado no timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'logs/notifications/notification_{timestamp}.json'
            
            # Salva notificação como JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(notification_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Notificação salva localmente em {filename}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar notificação localmente: {str(e)}") 