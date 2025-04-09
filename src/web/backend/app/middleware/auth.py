from functools import wraps
from flask import request, jsonify, g
from ..models.user import User

def token_required(f):
    """
    Decorator para rotas que exigem autenticação por token JWT.
    O token deve ser passado no cabeçalho 'Authorization' como 'Bearer {token}'.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        # Verifica se o cabeçalho de autorização está presente
        if not auth_header:
            return jsonify({
                'message': 'Token não fornecido',
                'error': 'unauthorized'
            }), 401
        
        # Extrai o token do cabeçalho (formato: Bearer {token})
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            return jsonify({
                'message': 'Formato de token inválido. Use: Bearer {token}',
                'error': 'invalid_format'
            }), 401
        
        # Verifica o token
        user_id = User.verify_token(token)
        if not user_id:
            return jsonify({
                'message': 'Token inválido ou expirado',
                'error': 'invalid_token'
            }), 401
        
        # Armazena o ID do usuário no contexto global do Flask
        g.user_id = user_id
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """
    Decorator para rotas que exigem privilégios de administrador.
    Deve ser usado em conjunto com @token_required.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        from ..models.user import User
        from .. import db
        
        # Obtém o usuário do banco de dados
        user = db.session.query(User).filter_by(id=g.user_id).first()
        
        if not user or user.role != 'admin':
            return jsonify({
                'message': 'Acesso negado. Privilégios de administrador necessários.',
                'error': 'forbidden'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated 