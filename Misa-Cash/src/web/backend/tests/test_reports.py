import json
import pytest
from datetime import datetime, timedelta

def test_generate_monthly_report(client, authenticated_headers):
    """Test de geração de relatório mensal"""
    # Criar algumas transações para o relatório
    test_transactions = [
        {
            "type": "income",
            "amount": 1000.00,
            "category": "salary",
            "description": "Monthly salary",
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 200.00,
            "category": "food",
            "description": "Groceries",
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 300.00,
            "category": "utilities",
            "description": "Electricity bill",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    ]
    
    # Adicionar transações
    for transaction in test_transactions:
        response = client.post(
            "/api/transactions",
            data=json.dumps(transaction),
            headers=authenticated_headers,
            content_type="application/json"
        )
        assert response.status_code == 201
    
    # Gerar relatório mensal
    current_month = datetime.now().month
    current_year = datetime.now().year
    response = client.get(
        f"/api/reports/monthly?month={current_month}&year={current_year}",
        headers=authenticated_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verificar estrutura do relatório
    assert "total_income" in data
    assert "total_expenses" in data
    assert "net_balance" in data
    assert "categories" in data
    
    # Verificar valores esperados
    assert data["total_income"] == 1000.00
    assert data["total_expenses"] == 500.00
    assert data["net_balance"] == 500.00
    
    # Verificar categorias
    assert len(data["categories"]) >= 2  # pelo menos as duas categorias de despesa
    
    # Verificar que 'food' e 'utilities' estão nas categorias
    food_category = next((c for c in data["categories"] if c["name"] == "food"), None)
    utilities_category = next((c for c in data["categories"] if c["name"] == "utilities"), None)
    
    assert food_category is not None
    assert utilities_category is not None
    assert food_category["amount"] == 200.00
    assert utilities_category["amount"] == 300.00

def test_generate_yearly_report(client, authenticated_headers):
    """Test de geração de relatório anual"""
    # Criar algumas transações para o relatório em diferentes meses
    current_date = datetime.now()
    test_transactions = [
        {
            "type": "income",
            "amount": 5000.00,
            "category": "salary",
            "description": "January salary",
            "date": datetime(current_date.year, 1, 15).strftime("%Y-%m-%d")
        },
        {
            "type": "income",
            "amount": 5000.00,
            "category": "salary",
            "description": "February salary",
            "date": datetime(current_date.year, 2, 15).strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 800.00,
            "category": "rent",
            "description": "January rent",
            "date": datetime(current_date.year, 1, 5).strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 800.00,
            "category": "rent",
            "description": "February rent",
            "date": datetime(current_date.year, 2, 5).strftime("%Y-%m-%d")
        }
    ]
    
    # Adicionar transações
    for transaction in test_transactions:
        response = client.post(
            "/api/transactions",
            data=json.dumps(transaction),
            headers=authenticated_headers,
            content_type="application/json"
        )
        assert response.status_code == 201
    
    # Gerar relatório anual
    current_year = datetime.now().year
    response = client.get(
        f"/api/reports/yearly?year={current_year}",
        headers=authenticated_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verificar estrutura do relatório
    assert "total_income" in data
    assert "total_expenses" in data
    assert "net_balance" in data
    assert "months" in data
    
    # Verificar valores esperados (considerando apenas as transações que adicionamos)
    assert data["total_income"] >= 10000.00
    assert data["total_expenses"] >= 1600.00
    assert data["net_balance"] >= 8400.00
    
    # Verificar dados mensais
    assert len(data["months"]) == 12  # Deve ter dados para todos os meses
    
    # Verificar janeiro e fevereiro especificamente
    january = data["months"][0]  # assumindo ordem cronológica
    february = data["months"][1]
    
    assert january["income"] >= 5000.00
    assert january["expenses"] >= 800.00
    assert february["income"] >= 5000.00
    assert february["expenses"] >= 800.00

def test_generate_category_report(client, authenticated_headers):
    """Test de geração de relatório por categoria"""
    # Criar algumas transações para o relatório em diferentes categorias
    test_transactions = [
        {
            "type": "expense",
            "amount": 150.00,
            "category": "food",
            "description": "Restaurant",
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 250.00,
            "category": "food",
            "description": "Groceries",
            "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 50.00,
            "category": "entertainment",
            "description": "Movie tickets",
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 100.00,
            "category": "entertainment",
            "description": "Concert tickets",
            "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        }
    ]
    
    # Adicionar transações
    for transaction in test_transactions:
        response = client.post(
            "/api/transactions",
            data=json.dumps(transaction),
            headers=authenticated_headers,
            content_type="application/json"
        )
        assert response.status_code == 201
    
    # Gerar relatório para categoria "food"
    current_month = datetime.now().month
    current_year = datetime.now().year
    response = client.get(
        f"/api/reports/category/food?month={current_month}&year={current_year}",
        headers=authenticated_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verificar estrutura do relatório
    assert "category" in data
    assert "total_amount" in data
    assert "transactions" in data
    
    # Verificar valores esperados
    assert data["category"] == "food"
    assert data["total_amount"] >= 400.00  # Pelo menos as duas transações que adicionamos
    assert len(data["transactions"]) >= 2

def test_generate_comparison_report(client, authenticated_headers):
    """Test de geração de relatório comparativo entre períodos"""
    # Criar transações para dois meses diferentes
    current_date = datetime.now()
    last_month_date = current_date - timedelta(days=30)
    
    test_transactions = [
        # Mês atual
        {
            "type": "income",
            "amount": 5000.00,
            "category": "salary",
            "description": "Current month salary",
            "date": current_date.strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 1500.00,
            "category": "rent",
            "description": "Current month rent",
            "date": current_date.strftime("%Y-%m-%d")
        },
        # Mês anterior
        {
            "type": "income",
            "amount": 5000.00,
            "category": "salary",
            "description": "Last month salary",
            "date": last_month_date.strftime("%Y-%m-%d")
        },
        {
            "type": "expense",
            "amount": 1200.00,
            "category": "rent",
            "description": "Last month rent",
            "date": last_month_date.strftime("%Y-%m-%d")
        }
    ]
    
    # Adicionar transações
    for transaction in test_transactions:
        response = client.post(
            "/api/transactions",
            data=json.dumps(transaction),
            headers=authenticated_headers,
            content_type="application/json"
        )
        assert response.status_code == 201
    
    # Gerar relatório comparativo
    current_month = current_date.month
    current_year = current_date.year
    last_month = last_month_date.month
    last_year = last_month_date.year
    
    response = client.get(
        f"/api/reports/comparison?period1_month={last_month}&period1_year={last_year}&period2_month={current_month}&period2_year={current_year}",
        headers=authenticated_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verificar estrutura do relatório
    assert "period1" in data
    assert "period2" in data
    assert "differences" in data
    
    # Verificar valores esperados
    assert data["period1"]["total_income"] >= 5000.00
    assert data["period1"]["total_expenses"] >= 1200.00
    assert data["period2"]["total_income"] >= 5000.00
    assert data["period2"]["total_expenses"] >= 1500.00
    
    # Verificar diferenças
    assert "income_change" in data["differences"]
    assert "expenses_change" in data["differences"]
    assert "net_balance_change" in data["differences"]
    
    # A despesa deve ter aumentado
    assert data["differences"]["expenses_change"] >= 300.00 