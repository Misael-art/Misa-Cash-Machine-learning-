import json
import pytest
from datetime import date, datetime

from app import create_app, db
from app.models import Transaction

@pytest.fixture
def app():
    """Cria e configura uma instância da aplicação para os testes."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    
    # Cria o contexto da aplicação
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de teste para fazer requisições à API."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner para os comandos da CLI."""
    return app.test_cli_runner()

def test_health_check(client):
    """Testa se a rota de health check está funcionando."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'online'

def test_create_transaction(client):
    """Testa a criação de uma transação."""
    transaction_data = {
        'description': 'Salário',
        'amount': 5000.0,
        'type': 'income',
        'date': date.today().isoformat(),
        'category': 'Trabalho'
    }
    
    response = client.post(
        '/api/transactions',
        data=json.dumps(transaction_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert response.json['description'] == transaction_data['description']
    assert response.json['amount'] == transaction_data['amount']
    assert response.json['type'] == transaction_data['type']
    assert 'id' in response.json

def test_get_transaction(client):
    """Testa a obtenção de uma transação específica."""
    # Primeiro, cria uma transação
    transaction_data = {
        'description': 'Mercado',
        'amount': 150.0,
        'type': 'expense',
        'date': date.today().isoformat(),
        'category': 'Alimentação'
    }
    
    response = client.post(
        '/api/transactions',
        data=json.dumps(transaction_data),
        content_type='application/json'
    )
    
    transaction_id = response.json['id']
    
    # Agora, obtém a transação criada
    response = client.get(f'/api/transactions/{transaction_id}')
    
    assert response.status_code == 200
    assert response.json['id'] == transaction_id
    assert response.json['description'] == transaction_data['description']
    assert response.json['amount'] == transaction_data['amount']
    assert response.json['type'] == transaction_data['type']

def test_list_transactions(client):
    """Testa a listagem de todas as transações."""
    # Cria algumas transações
    transactions = [
        {
            'description': 'Salário',
            'amount': 5000.0,
            'type': 'income',
            'date': date.today().isoformat(),
            'category': 'Trabalho'
        },
        {
            'description': 'Aluguel',
            'amount': 1200.0,
            'type': 'expense',
            'date': date.today().isoformat(),
            'category': 'Moradia'
        }
    ]
    
    for transaction in transactions:
        client.post(
            '/api/transactions',
            data=json.dumps(transaction),
            content_type='application/json'
        )
    
    # Obtém a lista de transações
    response = client.get('/api/transactions')
    
    assert response.status_code == 200
    assert len(response.json) == len(transactions)

def test_update_transaction(client):
    """Testa a atualização de uma transação."""
    # Primeiro, cria uma transação
    transaction_data = {
        'description': 'Internet',
        'amount': 100.0,
        'type': 'expense',
        'date': date.today().isoformat(),
        'category': 'Serviços'
    }
    
    response = client.post(
        '/api/transactions',
        data=json.dumps(transaction_data),
        content_type='application/json'
    )
    
    transaction_id = response.json['id']
    
    # Atualiza a transação
    updated_data = {
        'description': 'Internet e TV',
        'amount': 150.0
    }
    
    response = client.put(
        f'/api/transactions/{transaction_id}',
        data=json.dumps(updated_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert response.json['id'] == transaction_id
    assert response.json['description'] == updated_data['description']
    assert response.json['amount'] == updated_data['amount']
    # Os campos não atualizados devem permanecer iguais
    assert response.json['type'] == transaction_data['type']
    assert response.json['category'] == transaction_data['category']

def test_delete_transaction(client):
    """Testa a remoção de uma transação."""
    # Primeiro, cria uma transação
    transaction_data = {
        'description': 'Jantar fora',
        'amount': 80.0,
        'type': 'expense',
        'date': date.today().isoformat(),
        'category': 'Alimentação'
    }
    
    response = client.post(
        '/api/transactions',
        data=json.dumps(transaction_data),
        content_type='application/json'
    )
    
    transaction_id = response.json['id']
    
    # Remove a transação
    response = client.delete(f'/api/transactions/{transaction_id}')
    
    assert response.status_code == 200
    assert 'message' in response.json
    
    # Verifica se a transação foi realmente removida
    response = client.get(f'/api/transactions/{transaction_id}')
    assert response.status_code == 404

def test_get_transaction_summary(client):
    """Testa o resumo das transações."""
    # Cria algumas transações
    transactions = [
        {
            'description': 'Salário',
            'amount': 5000.0,
            'type': 'income',
            'date': date.today().isoformat(),
            'category': 'Trabalho'
        },
        {
            'description': 'Aluguel',
            'amount': 1200.0,
            'type': 'expense',
            'date': date.today().isoformat(),
            'category': 'Moradia'
        },
        {
            'description': 'Freelance',
            'amount': 1000.0,
            'type': 'income',
            'date': date.today().isoformat(),
            'category': 'Trabalho'
        }
    ]
    
    for transaction in transactions:
        client.post(
            '/api/transactions',
            data=json.dumps(transaction),
            content_type='application/json'
        )
    
    # Obtém o resumo
    response = client.get('/api/transactions/summary')
    
    assert response.status_code == 200
    assert response.json['income'] == 6000.0  # 5000 + 1000
    assert response.json['expense'] == 1200.0
    assert response.json['balance'] == 4800.0  # 6000 - 1200 