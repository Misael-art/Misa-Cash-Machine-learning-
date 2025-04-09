from flask import Blueprint, request, jsonify, g
from werkzeug.security import check_password_hash
from ..models.user import User
from ..database import db
from ..middleware import jwt_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint para registrar um novo usuário"""
    data = request.get_json()
    
    # Validação dos dados
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    # Verificar se o email já existe
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'E-mail já cadastrado'}), 409
    
    # Verificar se o username já existe
    existing_username = User.query.filter_by(username=data['username']).first()
    if existing_username:
        return jsonify({'message': 'Nome de usuário já cadastrado'}), 409
    
    # Criar novo usuário
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    
    # Adicionar à base de dados
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'Usuário registrado com sucesso',
        'user': new_user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para login de usuário"""
    data = request.get_json()
    
    # Validação dos dados
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    # Buscar usuário pelo email
    user = User.query.filter_by(email=data['email']).first()
    
    # Verificar se o usuário existe e a senha está correta
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Email ou senha inválidos'}), 401
    
    # Verificar se o usuário está ativo
    if not user.is_active:
        return jsonify({'message': 'Conta desativada. Entre em contato com o suporte.'}), 403
    
    # Gerar token JWT
    token = user.generate_token()
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required
def get_me():
    """Rota para obter os dados do usuário logado"""
    # Obter ID do usuário do contexto g (configurado pelo middleware jwt_required)
    user_id = g.current_user
    
    # Buscar o usuário no banco de dados
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    # Retornar os dados do usuário
    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200 