from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.budget import Budget
from app.models.transaction import Transaction
from app.models.category import Category
from app import db
from datetime import datetime
from sqlalchemy import func, and_

budget_bp = Blueprint('budgets', __name__)

@budget_bp.route('/budgets', methods=['GET'])
@jwt_required()
def get_budgets():
    """Get all budgets for the current user"""
    current_user_id = get_jwt_identity()
    
    budgets = Budget.query.filter_by(user_id=current_user_id).all()
    
    result = []
    for budget in budgets:
        # Get the category name
        category = Category.query.get(budget.category_id)
        category_name = category.name if category else None
        
        # Calculate amount spent within this budget's period
        spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.category_id == budget.category_id,
            Transaction.type == 'expense',
            Transaction.date >= budget.start_date,
            Transaction.date <= budget.end_date
        ).scalar() or 0
        
        result.append({
            'id': budget.id,
            'name': budget.name,
            'amount': float(budget.amount),
            'spent': float(spent),
            'categoryId': budget.category_id,
            'categoryName': category_name,
            'startDate': budget.start_date.isoformat(),
            'endDate': budget.end_date.isoformat(),
            'createdAt': budget.created_at.isoformat(),
            'updatedAt': budget.updated_at.isoformat() if budget.updated_at else None
        })
    
    return jsonify(result)

@budget_bp.route('/budgets/<budget_id>', methods=['GET'])
@jwt_required()
def get_budget(budget_id):
    """Get a specific budget by ID"""
    current_user_id = get_jwt_identity()
    
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user_id).first()
    
    if not budget:
        return jsonify({'message': 'Budget not found'}), 404
    
    # Get the category name
    category = Category.query.get(budget.category_id)
    category_name = category.name if category else None
    
    # Calculate amount spent within this budget's period
    spent = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user_id,
        Transaction.category_id == budget.category_id,
        Transaction.type == 'expense',
        Transaction.date >= budget.start_date,
        Transaction.date <= budget.end_date
    ).scalar() or 0
    
    return jsonify({
        'id': budget.id,
        'name': budget.name,
        'amount': float(budget.amount),
        'spent': float(spent),
        'categoryId': budget.category_id,
        'categoryName': category_name,
        'startDate': budget.start_date.isoformat(),
        'endDate': budget.end_date.isoformat(),
        'createdAt': budget.created_at.isoformat(),
        'updatedAt': budget.updated_at.isoformat() if budget.updated_at else None
    })

@budget_bp.route('/budgets', methods=['POST'])
@jwt_required()
def create_budget():
    """Create a new budget"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate input
    if not all(key in data for key in ['name', 'amount', 'categoryId', 'startDate', 'endDate']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if category exists
    category = Category.query.filter_by(id=data['categoryId']).first()
    if not category:
        return jsonify({'message': 'Category not found'}), 400
    
    try:
        # Parse dates
        start_date = datetime.fromisoformat(data['startDate'].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(data['endDate'].replace('Z', '+00:00'))
        
        if start_date > end_date:
            return jsonify({'message': 'Start date must be before end date'}), 400
        
        # Create budget
        new_budget = Budget(
            name=data['name'],
            amount=data['amount'],
            category_id=data['categoryId'],
            start_date=start_date,
            end_date=end_date,
            user_id=current_user_id
        )
        
        db.session.add(new_budget)
        db.session.commit()
        
        # Calculate amount spent within this budget's period
        spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.category_id == new_budget.category_id,
            Transaction.type == 'expense',
            Transaction.date >= new_budget.start_date,
            Transaction.date <= new_budget.end_date
        ).scalar() or 0
        
        return jsonify({
            'id': new_budget.id,
            'name': new_budget.name,
            'amount': float(new_budget.amount),
            'spent': float(spent),
            'categoryId': new_budget.category_id,
            'categoryName': category.name,
            'startDate': new_budget.start_date.isoformat(),
            'endDate': new_budget.end_date.isoformat(),
            'createdAt': new_budget.created_at.isoformat(),
            'updatedAt': new_budget.updated_at.isoformat() if new_budget.updated_at else None
        }), 201
    except ValueError as e:
        return jsonify({'message': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating budget: {str(e)}'}), 500

@budget_bp.route('/budgets/<budget_id>', methods=['PUT'])
@jwt_required()
def update_budget(budget_id):
    """Update an existing budget"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user_id).first()
    
    if not budget:
        return jsonify({'message': 'Budget not found'}), 404
    
    try:
        if 'name' in data:
            budget.name = data['name']
        
        if 'amount' in data:
            budget.amount = data['amount']
        
        if 'categoryId' in data:
            # Check if category exists
            category = Category.query.filter_by(id=data['categoryId']).first()
            if not category:
                return jsonify({'message': 'Category not found'}), 400
            budget.category_id = data['categoryId']
        
        if 'startDate' in data:
            budget.start_date = datetime.fromisoformat(data['startDate'].replace('Z', '+00:00'))
        
        if 'endDate' in data:
            budget.end_date = datetime.fromisoformat(data['endDate'].replace('Z', '+00:00'))
        
        if budget.start_date > budget.end_date:
            return jsonify({'message': 'Start date must be before end date'}), 400
        
        budget.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Get the category name
        category = Category.query.get(budget.category_id)
        category_name = category.name if category else None
        
        # Calculate amount spent within this budget's period
        spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.category_id == budget.category_id,
            Transaction.type == 'expense',
            Transaction.date >= budget.start_date,
            Transaction.date <= budget.end_date
        ).scalar() or 0
        
        return jsonify({
            'id': budget.id,
            'name': budget.name,
            'amount': float(budget.amount),
            'spent': float(spent),
            'categoryId': budget.category_id,
            'categoryName': category_name,
            'startDate': budget.start_date.isoformat(),
            'endDate': budget.end_date.isoformat(),
            'createdAt': budget.created_at.isoformat(),
            'updatedAt': budget.updated_at.isoformat() if budget.updated_at else None
        })
    except ValueError as e:
        return jsonify({'message': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating budget: {str(e)}'}), 500

@budget_bp.route('/budgets/<budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget(budget_id):
    """Delete a budget"""
    current_user_id = get_jwt_identity()
    
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user_id).first()
    
    if not budget:
        return jsonify({'message': 'Budget not found'}), 404
    
    try:
        db.session.delete(budget)
        db.session.commit()
        return jsonify({'message': 'Budget deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deleting budget: {str(e)}'}), 500

@budget_bp.route('/budgets/summary', methods=['GET'])
@jwt_required()
def get_budget_summary():
    """Get a summary of all budgets for the current user"""
    current_user_id = get_jwt_identity()
    
    # Get all active budgets
    current_date = datetime.utcnow().date()
    budgets = Budget.query.filter(
        Budget.user_id == current_user_id,
        Budget.start_date <= current_date,
        Budget.end_date >= current_date
    ).all()
    
    total_budget = sum(float(budget.amount) for budget in budgets)
    
    # Calculate total spent
    total_spent = 0
    budget_by_category = []
    
    for budget in budgets:
        # Get spent amount for this budget's category and period
        spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.category_id == budget.category_id,
            Transaction.type == 'expense',
            Transaction.date >= budget.start_date,
            Transaction.date <= budget.end_date
        ).scalar() or 0
        
        spent = float(spent)
        total_spent += spent
        
        # Get category name
        category = Category.query.get(budget.category_id)
        category_name = category.name if category else 'Unknown Category'
        
        # Calculate remaining and percent used for this category
        budget_amount = float(budget.amount)
        remaining = budget_amount - spent
        percent_used = (spent / budget_amount * 100) if budget_amount > 0 else 0
        
        budget_by_category.append({
            'categoryId': budget.category_id,
            'categoryName': category_name,
            'amount': budget_amount,
            'spent': spent,
            'remaining': remaining,
            'percentUsed': percent_used
        })
    
    # Calculate overall remaining and percent used
    remaining = total_budget - total_spent
    percent_used = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    return jsonify({
        'totalBudget': total_budget,
        'totalSpent': total_spent,
        'remaining': remaining,
        'percentUsed': percent_used,
        'budgetsByCategory': budget_by_category
    }) 