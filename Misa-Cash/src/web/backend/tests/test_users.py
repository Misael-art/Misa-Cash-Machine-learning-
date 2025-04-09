import pytest
from fastapi import status

def test_create_user(client):
    user_data = {
        "email": "newuser@example.com",
        "password": "test123",
        "full_name": "New User"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == user_data["email"]
    assert response.json()["full_name"] == user_data["full_name"]
    assert "id" in response.json()

def test_create_user_duplicate_email(client, test_user):
    user_data = {
        "email": test_user["email"],
        "password": "test123",
        "full_name": "Another User"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "já está em uso" in response.json()["detail"]

def test_get_user(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    response = client.get(
        f"/api/users/{test_user['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == test_user["id"]
    assert response.json()["email"] == test_user["email"]
    assert response.json()["full_name"] == test_user["full_name"]

def test_get_user_not_found(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    response = client.get(
        "/api/users/999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_user(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    update_data = {
        "full_name": "Updated Name",
        "password": "newpassword123"
    }
    response = client.put(
        f"/api/users/{test_user['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["full_name"] == update_data["full_name"]
    
    # Verificar se a senha foi atualizada tentando fazer login
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": update_data["password"]
        }
    )
    assert login_response.status_code == status.HTTP_200_OK

def test_delete_user(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    response = client.delete(
        f"/api/users/{test_user['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verificar se o usuário foi realmente excluído
    get_response = client.get(
        f"/api/users/{test_user['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_list_users(client, test_user):
    # Login para obter o token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar mais alguns usuários para testar a listagem
    for i in range(3):
        client.post("/api/users/", json={
            "email": f"user{i}@example.com",
            "password": "test123",
            "full_name": f"Test User {i}"
        })
    
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 4  # O usuário de teste + os 3 criados
    
    # Testar paginação
    response = client.get(
        "/api/users/?skip=0&limit=2",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2 