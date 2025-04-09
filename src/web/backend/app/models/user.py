import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db
from flask import current_app

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')  # 'user', 'admin', etc.
    
    # Relacionamentos
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    
    def set_password(self, password):
        """Define a senha para o usuário"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha fornecida corresponde à senha armazenada"""
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """Gera um token JWT para o usuário"""
        payload = {
            'sub': self.id,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
        
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_token(token):
        """Verifica a validade de um token JWT e retorna o ID do usuário"""
        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
            return payload['sub']  # ID do usuário
        except jwt.ExpiredSignatureError:
            return None  # Token expirado
        except jwt.InvalidTokenError:
            return None  # Token inválido
    
    def to_dict(self):
        """Converte o objeto do usuário em um dicionário (para resposta JSON)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active,
            'role': self.role
        } 