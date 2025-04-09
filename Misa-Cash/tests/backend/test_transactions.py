import pytest
from fastapi import status
from datetime import datetime

def test_create_transaction(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    transaction_data = {
        "amount": 1000.50,
        "type": "INCOME",
        "category": "SALARY",
        "description": "Monthly salary",
        "date": datetime.now().isoformat()
    }
    
    response = client.post(
        "/api/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json=transaction_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["amount"] == transaction_data["amount"]
    assert response.json()["type"] == transaction_data["type"]
    assert response.json()["category"] == transaction_data["category"]
    assert response.json()["user_id"] == test_user["id"]

def test_get_transaction(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar uma transação primeiro
    transaction_data = {
        "amount": 1000.50,
        "type": "INCOME",
        "category": "SALARY",
        "description": "Monthly salary",
        "date": datetime.now().isoformat()
    }
    create_response = client.post(
        "/api/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json=transaction_data
    )
    transaction_id = create_response.json()["id"]
    
    # Buscar a transação criada
    response = client.get(
        f"/api/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == transaction_id
    assert response.json()["amount"] == transaction_data["amount"]

def test_list_transactions(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar várias transações
    transactions = [
        {
            "amount": 1000.50,
            "type": "INCOME",
            "category": "SALARY",
            "description": "Monthly salary",
            "date": datetime.now().isoformat()
        },
        {
            "amount": 500.00,
            "type": "EXPENSE",
            "category": "RENT",
            "description": "Monthly rent",
            "date": datetime.now().isoformat()
        }
    ]
    
    for transaction in transactions:
        client.post(
            "/api/transactions/",
            headers={"Authorization": f"Bearer {token}"},
            json=transaction
        )
    
    # Listar todas as transações
    response = client.get(
        "/api/transactions/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= len(transactions)

def test_update_transaction(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar uma transação
    transaction_data = {
        "amount": 1000.50,
        "type": "INCOME",
        "category": "SALARY",
        "description": "Monthly salary",
        "date": datetime.now().isoformat()
    }
    create_response = client.post(
        "/api/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json=transaction_data
    )
    transaction_id = create_response.json()["id"]
    
    # Atualizar a transação
    update_data = {
        "amount": 1100.50,
        "description": "Updated salary"
    }
    response = client.put(
        f"/api/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["amount"] == update_data["amount"]
    assert response.json()["description"] == update_data["description"]

def test_delete_transaction(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar uma transação
    transaction_data = {
        "amount": 1000.50,
        "type": "INCOME",
        "category": "SALARY",
        "description": "Monthly salary",
        "date": datetime.now().isoformat()
    }
    create_response = client.post(
        "/api/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json=transaction_data
    )
    transaction_id = create_response.json()["id"]
    
    # Deletar a transação
    response = client.delete(
        f"/api/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verificar se a transação foi realmente excluída
    get_response = client.get(
        f"/api/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_get_transaction_summary(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar várias transações
    transactions = [
        {
            "amount": 1000.50,
            "type": "INCOME",
            "category": "SALARY",
            "description": "Monthly salary",
            "date": datetime.now().isoformat()
        },
        {
            "amount": 500.00,
            "type": "EXPENSE",
            "category": "RENT",
            "description": "Monthly rent",
            "date": datetime.now().isoformat()
        }
    ]
    
    for transaction in transactions:
        client.post(
            "/api/transactions/",
            headers={"Authorization": f"Bearer {token}"},
            json=transaction
        )
    
    # Obter resumo das transações
    response = client.get(
        "/api/transactions/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "total_income" in response.json()
    assert "total_expenses" in response.json()
    assert "balance" in response.json()
    assert response.json()["total_income"] >= 1000.50
    assert response.json()["total_expenses"] >= 500.00
    assert response.json()["balance"] >= 500.50 