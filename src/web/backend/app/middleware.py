from flask import request, jsonify, g
from functools import wraps
from .models import User

def jwt_required(f):
    """Decorador que requer um token JWT válido para acessar uma rota"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Verifica se o token está no cabeçalho Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token de autenticação não fornecido'}), 401
        
        # Verifica o token
        user = User.verify_token(token)
        if not user:
            return jsonify({'error': 'Token inválido ou expirado'}), 401
        
        # Armazena o usuário atual no contexto g do Flask
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function 