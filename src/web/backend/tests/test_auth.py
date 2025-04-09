import json
import pytest
import time
from datetime import datetime

from web.backend.app import create_app, db
from web.backend.app.models import User

@pytest.fixture
def app():
    """Cria e configura uma instância da aplicação para os testes."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-key'
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

@pytest.fixture
def test_user(app):
    """Cria um usuário de teste."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user

def test_register_user(client):
    """Testa o registro de um novo usuário."""
    user_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpassword123'
    }
    
    response = client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = response.json
    assert 'message' in data
    assert 'user_id' in data
    assert 'token' in data
    
    # Verifica se o usuário foi realmente criado
    with client.application.app_context():
        user = User.query.filter_by(email='new@example.com').first()
        assert user is not None
        assert user.username == 'newuser'
        assert user.check_password('newpassword123')

def test_register_with_existing_email(client, test_user):
    """Testa o registro com um email já existente."""
    user_data = {
        'username': 'anotheruser',
        'email': 'test@example.com',  # Email já existente
        'password': 'password123'
    }
    
    response = client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Email já está em uso' in response.json['error']

def test_register_with_missing_fields(client):
    """Testa o registro com campos obrigatórios ausentes."""
    user_data = {
        'username': 'incomplete',
        # Email ausente
        'password': 'password123'
    }
    
    response = client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Campo obrigatório' in response.json['error']

def test_login_success(client, test_user):
    """Testa login com credenciais válidas."""
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = response.json
    assert 'token' in data
    assert 'user' in data
    assert data['user']['username'] == 'testuser'
    assert data['user']['email'] == 'test@example.com'

def test_login_invalid_credentials(client, test_user):
    """Testa login com credenciais inválidas."""
    # Senha incorreta
    login_data = {
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    assert 'error' in response.json
    assert 'Credenciais inválidas' in response.json['error']
    
    # Email incorreto
    login_data = {
        'email': 'nonexistent@example.com',
        'password': 'password123'
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    assert 'error' in response.json
    assert 'Credenciais inválidas' in response.json['error']

def test_get_profile(client, test_user):
    """Testa a obtenção do perfil do usuário logado utilizando a rota /me."""
    # Primeiro faz login para obter o token
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    login_response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    token = login_response.json['token']
    
    # Tenta obter o perfil com o token na rota /me
    response = client.get(
        '/api/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = response.json
    assert data['success'] is True
    assert 'user' in data
    assert data['user']['username'] == 'testuser'
    assert data['user']['email'] == 'test@example.com'

def test_unauthorized_access(client):
    """Testa acesso sem token de autenticação."""
    response = client.get('/api/auth/me')
    
    assert response.status_code == 401
    assert 'error' in response.json
    assert 'Token de autenticação ausente' in response.json['error']

def test_invalid_token(client):
    """Testa acesso com token inválido."""
    response = client.get(
        '/api/auth/me',
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    
    assert response.status_code == 401
    assert 'error' in response.json
    assert 'Token inválido' in response.json['error']

def test_change_password(client, test_user):
    """Testa a alteração de senha."""
    # Primeiro faz login para obter o token
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    login_response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    token = login_response.json['token']
    
    # Tenta alterar a senha
    password_data = {
        'current_password': 'password123',
        'new_password': 'newpassword456'
    }
    
    response = client.post(
        '/api/auth/change-password',
        data=json.dumps(password_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    assert 'message' in response.json
    assert 'Senha alterada com sucesso' in response.json['message']
    
    # Verifica se a nova senha está funcionando
    login_data = {
        'email': 'test@example.com',
        'password': 'newpassword456'
    }
    
    login_response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert login_response.status_code == 200
    assert 'token' in login_response.json

def test_change_password_incorrect_current(client, test_user):
    """Testa a alteração de senha com senha atual incorreta."""
    # Primeiro faz login para obter o token
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    login_response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    token = login_response.json['token']
    
    # Tenta alterar a senha com a senha atual incorreta
    password_data = {
        'current_password': 'wrongpassword',
        'new_password': 'newpassword456'
    }
    
    response = client.post(
        '/api/auth/change-password',
        data=json.dumps(password_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Senha atual incorreta' in response.json['error']

def test_token_expiration(client, test_user, app):
    """Testa a expiração do token."""
    # Configura a aplicação com um tempo de expiração curto para o teste
    app.config['JWT_EXPIRATION_SECONDS'] = 1  # 1 segundo
    
    # Faz login para obter o token
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    login_response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    token = login_response.json['token']
    
    # Espera o token expirar
    time.sleep(2)
    
    # Tenta acessar um recurso protegido
    response = client.get(
        '/api/auth/profile',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 401
    assert 'error' in response.json
    assert 'Token expirado' in response.json['error']

def test_get_me(client, test_user):
    """Testa a rota /me para obter o perfil do usuário logado através do token JWT."""
    # Primeiro faz login para obter o token
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    login_response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert login_response.status_code == 200
    token = login_response.json['token']
    
    # Acessa a rota /me com o token obtido
    response = client.get(
        '/api/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = response.json
    assert data['success'] is True
    assert 'user' in data
    assert data['user']['username'] == 'testuser'
    assert data['user']['email'] == 'test@example.com'
    
    # Testa acesso sem token de autenticação
    no_auth_response = client.get('/api/auth/me')
    assert no_auth_response.status_code == 401
    assert 'error' in no_auth_response.json
    
    # Testa acesso com token inválido
    invalid_token_response = client.get(
        '/api/auth/me',
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    assert invalid_token_response.status_code == 401
    assert 'error' in invalid_token_response.json 