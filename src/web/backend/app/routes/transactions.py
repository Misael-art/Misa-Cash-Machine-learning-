from flask import request, jsonify, g
from flask_jwt_extended import jwt_required
import datetime
from models.transaction import Transaction

@api_bp.route('/transactions/summary', methods=['GET'])
@jwt_required
def get_transactions_summary():
    """Endpoint para obter o resumo das transações para o dashboard"""
    # Obter o ID do usuário do token JWT
    user_id = g.current_user
    
    # Obter o período de análise dos parâmetros da URL
    period = request.args.get('period', 'month')
    
    # Calcular a data inicial com base no período
    end_date = datetime.datetime.now()
    if period == 'week':
        start_date = end_date - datetime.timedelta(days=7)
    elif period == 'month':
        start_date = end_date - datetime.timedelta(days=30)
    elif period == 'year':
        start_date = end_date - datetime.timedelta(days=365)
    else:
        return jsonify({'error': 'Período inválido. Utilize week, month ou year.'}), 400
    
    # Consultar transações no período
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()
    
    # Calcular totais
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense
    
    # Calcular resumo por categoria
    categories = {}
    for transaction in transactions:
        if transaction.category not in categories:
            categories[transaction.category] = 0
        categories[transaction.category] += transaction.amount
    
    # Calcular percentual de cada categoria
    total = total_income if len(transactions) == 0 else sum(categories.values())
    categories_summary = []
    for category, amount in categories.items():
        percentage = (amount / total * 100) if total > 0 else 0
        categories_summary.append({
            'category': category,
            'total': amount,
            'percentage': percentage
        })
    
    # Ordenar categorias pelo valor (maior para menor)
    categories_summary.sort(key=lambda x: x['total'], reverse=True)
    
    # Obter transações recentes (5 mais recentes)
    recent_transactions = Transaction.query.filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.date.desc()).limit(5).all()
    
    return jsonify({
        'success': True,
        'totalIncome': total_income,
        'totalExpense': total_expense,
        'balance': balance,
        'categoriesSummary': categories_summary,
        'recentTransactions': [t.to_dict() for t in recent_transactions]
    }), 200

@api_bp.route('/transactions/charts', methods=['GET'])
@jwt_required
def get_charts_data():
    """Endpoint para obter dados para os gráficos do dashboard"""
    # Obter o ID do usuário do token JWT
    user_id = g.current_user
    
    # Obter parâmetros da URL
    chart_type = request.args.get('type', 'timeline')
    period = request.args.get('period', 'month')
    transaction_type = request.args.get('transaction_type', 'all')
    
    # Validar parâmetros
    if chart_type not in ['category', 'timeline', 'comparison']:
        return jsonify({'error': 'Tipo de gráfico inválido'}), 400
    
    if period not in ['week', 'month', 'year']:
        return jsonify({'error': 'Período inválido'}), 400
    
    if transaction_type not in ['income', 'expense', 'all']:
        return jsonify({'error': 'Tipo de transação inválido'}), 400
    
    # Calcular a data inicial com base no período
    end_date = datetime.datetime.now()
    if period == 'week':
        start_date = end_date - datetime.timedelta(days=7)
        format_string = '%a'  # Abreviação do dia da semana
        interval = datetime.timedelta(days=1)
    elif period == 'month':
        start_date = end_date - datetime.timedelta(days=30)
        format_string = '%d/%m'  # Dia/Mês
        interval = datetime.timedelta(days=5)
    elif period == 'year':
        start_date = end_date - datetime.timedelta(days=365)
        format_string = '%b'  # Abreviação do mês
        interval = datetime.timedelta(days=30)
    
    # Preparar resposta padrão
    response = {
        'success': True,
        'labels': [],
        'datasets': []
    }
    
    # Filtrar transações por período e tipo (se especificado)
    query = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    )
    
    if transaction_type != 'all':
        query = query.filter(Transaction.type == transaction_type)
    
    transactions = query.order_by(Transaction.date).all()
    
    # Gráfico de linha do tempo / comparativo
    if chart_type in ['timeline', 'comparison']:
        # Criar intervalos de datas
        intervals = []
        current_date = start_date
        while current_date <= end_date:
            intervals.append({
                'start': current_date,
                'end': current_date + interval,
                'label': current_date.strftime(format_string)
            })
            current_date += interval
        
        # Gerar labels
        response['labels'] = [interval['label'] for interval in intervals]
        
        if chart_type == 'timeline':
            # Para timeline, mostrar uma série para cada tipo
            income_data = [0] * len(intervals)
            expense_data = [0] * len(intervals)
            
            # Agrupar transações por intervalo
            for t in transactions:
                for i, interval in enumerate(intervals):
                    if interval['start'] <= t.date <= interval['end']:
                        if t.type == 'income':
                            income_data[i] += t.amount
                        else:
                            expense_data[i] += t.amount
            
            response['datasets'] = [
                {
                    'label': 'Receitas',
                    'data': income_data,
                    'backgroundColor': 'rgba(76, 175, 80, 0.2)',
                    'borderColor': '#4caf50',
                    'borderWidth': 2
                },
                {
                    'label': 'Despesas',
                    'data': expense_data,
                    'backgroundColor': 'rgba(244, 67, 54, 0.2)',
                    'borderColor': '#f44336',
                    'borderWidth': 2
                }
            ]
        
        else:  # comparison
            # Para comparativo, mostrar uma única série
            data = [0] * len(intervals)
            
            # Agrupar transações por intervalo
            for t in transactions:
                for i, interval in enumerate(intervals):
                    if interval['start'] <= t.date <= interval['end']:
                        if t.type == 'income':
                            data[i] += t.amount
                        else:
                            data[i] -= t.amount
            
            response['datasets'] = [
                {
                    'label': 'Saldo',
                    'data': data,
                    'backgroundColor': [
                        'rgba(76, 175, 80, 0.2)' if value >= 0 else 'rgba(244, 67, 54, 0.2)'
                        for value in data
                    ],
                    'borderColor': [
                        '#4caf50' if value >= 0 else '#f44336'
                        for value in data
                    ],
                    'borderWidth': 2
                }
            ]
    
    # Gráfico de categorias
    elif chart_type == 'category':
        # Agrupar por categoria
        categories = {}
        for t in transactions:
            if t.category not in categories:
                categories[t.category] = 0
            categories[t.category] += t.amount
        
        # Ordenar por valor
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        labels = [cat[0] for cat in sorted_categories]
        data = [cat[1] for cat in sorted_categories]
        
        # Limitar a 10 categorias para melhor visualização
        if len(labels) > 10:
            other_sum = sum(data[9:])
            labels = labels[:9] + ['Outros']
            data = data[:9] + [other_sum]
        
        response['labels'] = labels
        
        # Cores para o gráfico de categorias
        colors = [
            '#ff6384', '#ff9f40', '#ffcd56', '#36a2eb', '#4bc0c0', 
            '#9966ff', '#c9cbcf', '#8a2be2', '#ff7f50', '#20b2aa'
        ]
        
        response['datasets'] = [
            {
                'label': 'Valor por Categoria',
                'data': data,
                'backgroundColor': colors[:len(labels)],
                'borderWidth': 1
            }
        ]
    
    return jsonify(response), 200 