import datetime
from ..database import db

class Transaction(db.Model):
    """Modelo para transações financeiras"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' ou 'expense'
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_frequency = db.Column(db.String(20), nullable=True)  # 'daily', 'weekly', 'monthly', 'yearly'
    tags = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def to_dict(self):
        """Converte o objeto de transação em um dicionário para resposta JSON"""
        tags_list = self.tags.split(',') if self.tags else []
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'description': self.description,
            'amount': self.amount,
            'type': self.type,
            'category': self.category,
            'date': self.date.isoformat(),
            'is_recurring': self.is_recurring,
            'recurrence_frequency': self.recurrence_frequency,
            'tags': tags_list,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 