from functools import wraps
from flask import request, g, jsonify
from ..models.user import User

def login_required(f):
    """Middleware que verifica se o usuário está autenticado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'message': 'Token de autenticação ausente'}), 401
        
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({'message': 'Formato de token inválido'}), 401
        
        # Decodificar token
        user_id = User.decode_token(token)
        
        # Verificar se o resultado é uma string (mensagem de erro)
        if isinstance(user_id, str):
            return jsonify({'message': user_id}), 401
        
        # Armazenar o ID do usuário no contexto global
        g.user_id = user_id
        
        return f(*args, **kwargs)
    
    return decorated_function 