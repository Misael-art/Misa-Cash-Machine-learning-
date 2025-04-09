import uuid
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class Budget(db.Model):
    __tablename__ = 'budgets'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='budgets')
    category = db.relationship('Category', backref='budgets')
    
    def __init__(self, name, amount, category_id, start_date, end_date, user_id):
        self.id = uuid.uuid4()
        self.name = name
        self.amount = amount
        self.category_id = category_id
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id
        self.created_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Budget {self.name}>' 