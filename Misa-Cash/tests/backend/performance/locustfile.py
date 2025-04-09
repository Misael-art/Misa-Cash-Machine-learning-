from locust import HttpUser, task, between
from typing import Dict
import json

class MisaCashUser(HttpUser):
    wait_time = between(1, 3)
    token: str = None
    
    def on_start(self):
        """Login do usuário antes de iniciar os testes"""
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "test123"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.client.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def view_dashboard(self):
        """Teste de acesso ao dashboard"""
        self.client.get("/api/dashboard/summary")
    
    @task(2)
    def list_transactions(self):
        """Teste de listagem de transações"""
        self.client.get("/api/transactions")
    
    @task(2)
    def create_transaction(self):
        """Teste de criação de transação"""
        transaction = {
            "type": "expense",
            "amount": 100.00,
            "category": "food",
            "description": "Test transaction",
            "date": "2024-03-20"
        }
        self.client.post("/api/transactions", json=transaction)
    
    @task(1)
    def generate_report(self):
        """Teste de geração de relatório"""
        self.client.get("/api/reports/monthly")
    
    @task(1)
    def update_profile(self):
        """Teste de atualização de perfil"""
        profile = {
            "name": "Test User",
            "email": "test@example.com"
        }
        self.client.put("/api/users/profile", json=profile) 