from flask import Blueprint, jsonify, request
from .models import Transaction
from . import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Rota para verificar se a API está funcionando."""
    return jsonify({"status": "online"}), 200

@api_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """Obtém todas as transações."""
    transactions = Transaction.query.all()
    return jsonify([t.to_dict() for t in transactions]), 200

@api_bp.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    """Obtém uma transação específica pelo ID."""
    transaction = Transaction.query.get_or_404(id)
    return jsonify(transaction.to_dict()), 200

@api_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """Cria uma nova transação."""
    data = request.get_json()
    
    # Validação básica
    required_fields = ['description', 'amount', 'type', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo obrigatório ausente: {field}"}), 400
    
    transaction = Transaction(
        description=data['description'],
        amount=data['amount'],
        type=data['type'],
        date=data['date'],
        category=data.get('category'),
        notes=data.get('notes')
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify(transaction.to_dict()), 201

@api_bp.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    """Atualiza uma transação existente."""
    transaction = Transaction.query.get_or_404(id)
    data = request.get_json()
    
    if 'description' in data:
        transaction.description = data['description']
    if 'amount' in data:
        transaction.amount = data['amount']
    if 'type' in data:
        transaction.type = data['type']
    if 'date' in data:
        transaction.date = data['date']
    if 'category' in data:
        transaction.category = data['category']
    if 'notes' in data:
        transaction.notes = data['notes']
    
    db.session.commit()
    
    return jsonify(transaction.to_dict()), 200

@api_bp.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    """Remove uma transação."""
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    
    return jsonify({"message": "Transação removida com sucesso"}), 200

@api_bp.route('/transactions/summary', methods=['GET'])
def get_transaction_summary():
    """Retorna um resumo das transações (receitas vs despesas)."""
    income = db.session.query(db.func.sum(Transaction.amount)).\
        filter(Transaction.type == 'income').scalar() or 0
    expense = db.session.query(db.func.sum(Transaction.amount)).\
        filter(Transaction.type == 'expense').scalar() or 0
    
    return jsonify({
        "income": float(income),
        "expense": float(expense),
        "balance": float(income - expense)
    }), 200 