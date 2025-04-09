from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, g
from functools import wraps
import jwt

from . import db
from .models import User

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    """Decorator para verificar token JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Tenta obter o token do cabeçalho Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header:
            if ' ' in auth_header:
                scheme, token = auth_header.split(' ', 1)
                if scheme.lower() != 'bearer':
                    token = None
            else:
                token = auth_header
        
        if not token:
            return jsonify({'message': 'Token não fornecido'}), 401
        
        try:
            # Verifica se o token é válido
            user = User.verify_auth_token(token)
            if not user:
                return jsonify({'message': 'Token inválido ou expirado'}), 401
            
            # Armazena o usuário autenticado para acesso na view
            g.current_user = user
        except:
            return jsonify({'message': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    """Rota para registrar um novo usuário."""
    data = request.get_json()
    
    # Validação básica
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    # Verifica se o usuário já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'E-mail já cadastrado'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Nome de usuário já utilizado'}), 409
    
    # Cria o novo usuário
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Usuário criado com sucesso',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Rota para autenticar um usuário."""
    data = request.get_json()
    
    # Validação básica
    if not data or (not data.get('email') and not data.get('username')) or not data.get('password'):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    # Localiza o usuário pelo e-mail ou nome de usuário
    user = None
    if data.get('email'):
        user = User.query.filter_by(email=data['email']).first()
    elif data.get('username'):
        user = User.query.filter_by(username=data['username']).first()
        
    # Verifica se o usuário existe e a senha está correta
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Credenciais inválidas'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Conta desativada'}), 403
    
    # Atualiza o último login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Gera o token de autenticação
    token = user.generate_auth_token()
    
    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_user_info():
    """Rota para obter informações do usuário autenticado."""
    return jsonify({
        'user': g.current_user.to_dict()
    }), 200

@auth_bp.route('/change-password', methods=['PUT'])
@token_required
def change_password():
    """Rota para alterar a senha do usuário."""
    data = request.get_json()
    
    if not data or not data.get('current_password') or not data.get('new_password'):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    if not g.current_user.check_password(data['current_password']):
        return jsonify({'message': 'Senha atual incorreta'}), 401
    
    g.current_user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({'message': 'Senha alterada com sucesso'}), 200 