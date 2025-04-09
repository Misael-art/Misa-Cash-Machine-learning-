from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.user import User
from app import db
from datetime import datetime, timedelta
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import tempfile
from sqlalchemy import func, desc
import json
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/generate', methods=['POST'])
@jwt_required()
def generate_report():
    """
    Gera um relatório financeiro baseado em parâmetros de data e filtros opcionais
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validação dos dados de entrada
    if not data or 'start_date' not in data or 'end_date' not in data:
        return jsonify({'error': 'Datas inicial e final são obrigatórias'}), 400
    
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        
        # Adiciona 1 dia ao end_date para incluir transações do último dia
        end_date = end_date + timedelta(days=1)
        
        if start_date >= end_date:
            return jsonify({'error': 'A data inicial deve ser anterior à data final'}), 400
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    # Filtros opcionais
    include_income = data.get('include_income', True)
    include_expenses = data.get('include_expenses', True)
    category_ids = data.get('category_ids', [])
    
    # Buscar transações do período
    query = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date < end_date
    )
    
    # Aplicar filtros opcionais
    if not include_income:
        query = query.filter(Transaction.amount < 0)
    if not include_expenses:
        query = query.filter(Transaction.amount > 0)
    if category_ids:
        query = query.filter(Transaction.category_id.in_(category_ids))
    
    transactions = query.all()
    
    # Calcular período anterior (mesmo número de dias)
    days_diff = (end_date - start_date).days
    prev_start_date = start_date - timedelta(days=days_diff)
    prev_end_date = start_date
    
    # Buscar transações do período anterior para comparação
    prev_query = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= prev_start_date,
        Transaction.date < prev_end_date
    )
    
    prev_transactions = prev_query.all()
    
    # Calcular métricas do período atual
    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
    balance = total_income - total_expenses
    
    # Calcular métricas do período anterior
    prev_total_income = sum(t.amount for t in prev_transactions if t.amount > 0)
    prev_total_expenses = sum(abs(t.amount) for t in prev_transactions if t.amount < 0)
    prev_balance = prev_total_income - prev_total_expenses
    
    # Calcular variações percentuais
    income_change_pct = ((total_income - prev_total_income) / prev_total_income * 100) if prev_total_income > 0 else 0
    expense_change_pct = ((total_expenses - prev_total_expenses) / prev_total_expenses * 100) if prev_total_expenses > 0 else 0
    balance_change_pct = ((balance - prev_balance) / abs(prev_balance) * 100) if prev_balance != 0 else 0
    
    # Agrupar transações por categoria
    category_summary = {}
    for t in transactions:
        category_id = t.category_id
        if category_id not in category_summary:
            category = Category.query.get(category_id)
            category_name = category.name if category else "Sem categoria"
            category_summary[category_id] = {
                'id': category_id,
                'name': category_name,
                'income': 0,
                'expenses': 0,
                'transactions': 0
            }
        
        if t.amount > 0:
            category_summary[category_id]['income'] += t.amount
        else:
            category_summary[category_id]['expenses'] += abs(t.amount)
        
        category_summary[category_id]['transactions'] += 1
    
    # Ordenar categorias por despesa
    top_expense_categories = sorted(
        [cat for cat in category_summary.values() if cat['expenses'] > 0],
        key=lambda x: x['expenses'],
        reverse=True
    )[:5]
    
    # Ordenar categorias por receita
    top_income_categories = sorted(
        [cat for cat in category_summary.values() if cat['income'] > 0],
        key=lambda x: x['income'],
        reverse=True
    )[:5]
    
    # Agrupar transações por data para série temporal
    date_summary = {}
    for t in transactions:
        date_str = t.date.strftime('%Y-%m-%d')
        if date_str not in date_summary:
            date_summary[date_str] = {'income': 0, 'expenses': 0, 'balance': 0}
        
        if t.amount > 0:
            date_summary[date_str]['income'] += t.amount
        else:
            date_summary[date_str]['expenses'] += abs(t.amount)
        
        date_summary[date_str]['balance'] = date_summary[date_str]['income'] - date_summary[date_str]['expenses']
    
    # Ordenar série temporal
    time_series = [{'date': date, **values} for date, values in sorted(date_summary.items())]
    
    # Estruturar o relatório
    report = {
        'summary': {
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': (end_date - timedelta(days=1)).strftime('%Y-%m-%d'),
                'days': days_diff
            },
            'income': {
                'current': round(total_income, 2),
                'previous': round(prev_total_income, 2),
                'change_percentage': round(income_change_pct, 2)
            },
            'expenses': {
                'current': round(total_expenses, 2),
                'previous': round(prev_total_expenses, 2),
                'change_percentage': round(expense_change_pct, 2)
            },
            'balance': {
                'current': round(balance, 2),
                'previous': round(prev_balance, 2),
                'change_percentage': round(balance_change_pct, 2)
            },
            'transaction_count': len(transactions)
        },
        'categories': {
            'top_expenses': top_expense_categories,
            'top_income': top_income_categories,
            'all': list(category_summary.values())
        },
        'time_series': time_series,
        'analysis': {
            'avg_daily_expense': round(total_expenses / days_diff if days_diff > 0 else 0, 2),
            'avg_transaction_value': round(sum(abs(t.amount) for t in transactions) / len(transactions) if transactions else 0, 2),
            'most_expensive_day': max(time_series, key=lambda x: x['expenses'])['date'] if time_series else None,
            'highest_income_day': max(time_series, key=lambda x: x['income'])['date'] if time_series else None
        }
    }
    
    return jsonify(report)

@reports_bp.route('/reports/export/pdf', methods=['POST'])
@jwt_required()
def export_pdf():
    """
    Gera e exporta um relatório financeiro em formato PDF
    """
    # Obter dados do relatório
    report_data = generate_report().get_json()
    
    # Criar um arquivo PDF temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        pdf_path = temp_file.name
    
    # Configurar o documento PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title = Paragraph(f"Relatório Financeiro: {report_data['summary']['period']['start_date']} a {report_data['summary']['period']['end_date']}", styles['Heading1'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Resumo financeiro
    summary_title = Paragraph("Resumo Financeiro", styles['Heading2'])
    elements.append(summary_title)
    elements.append(Spacer(1, 6))
    
    summary_data = [
        ["Métrica", "Valor Atual", "Valor Anterior", "Variação (%)"],
        ["Receitas", f"R$ {report_data['summary']['income']['current']}", 
         f"R$ {report_data['summary']['income']['previous']}", 
         f"{report_data['summary']['income']['change_percentage']}%"],
        ["Despesas", f"R$ {report_data['summary']['expenses']['current']}", 
         f"R$ {report_data['summary']['expenses']['previous']}", 
         f"{report_data['summary']['expenses']['change_percentage']}%"],
        ["Saldo", f"R$ {report_data['summary']['balance']['current']}", 
         f"R$ {report_data['summary']['balance']['previous']}", 
         f"{report_data['summary']['balance']['change_percentage']}%"]
    ]
    
    summary_table = Table(summary_data, colWidths=[120, 100, 100, 100])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 12))
    
    # Principais categorias de despesa
    if report_data['categories']['top_expenses']:
        expense_title = Paragraph("Top 5 Categorias de Despesa", styles['Heading2'])
        elements.append(expense_title)
        elements.append(Spacer(1, 6))
        
        expense_data = [["Categoria", "Valor", "Qtd. Transações"]]
        for cat in report_data['categories']['top_expenses']:
            expense_data.append([
                cat['name'], 
                f"R$ {cat['expenses']}", 
                str(cat['transactions'])
            ])
        
        expense_table = Table(expense_data, colWidths=[200, 120, 100])
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(expense_table)
        elements.append(Spacer(1, 12))
    
    # Análise
    analysis_title = Paragraph("Análise de Transações", styles['Heading2'])
    elements.append(analysis_title)
    elements.append(Spacer(1, 6))
    
    analysis_data = [
        ["Métrica", "Valor"],
        ["Despesa média diária", f"R$ {report_data['analysis']['avg_daily_expense']}"],
        ["Valor médio por transação", f"R$ {report_data['analysis']['avg_transaction_value']}"],
        ["Dia com maior despesa", report_data['analysis']['most_expensive_day'] or 'N/A'],
        ["Dia com maior receita", report_data['analysis']['highest_income_day'] or 'N/A']
    ]
    
    analysis_table = Table(analysis_data, colWidths=[200, 220])
    analysis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(analysis_table)
    
    # Construir o PDF
    doc.build(elements)
    
    return send_file(pdf_path, as_attachment=True, 
                    attachment_filename=f"relatorio_financeiro_{report_data['summary']['period']['start_date']}_a_{report_data['summary']['period']['end_date']}.pdf", 
                    mimetype='application/pdf')

@reports_bp.route('/reports/export/excel', methods=['POST'])
@jwt_required()
def export_excel():
    """
    Gera e exporta um relatório financeiro em formato Excel
    """
    # Obter dados do relatório
    report_data = generate_report().get_json()
    
    # Criar arquivo Excel em memória
    output = BytesIO()
    
    # Criar um Excel writer usando pandas
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Planilha de Resumo
        summary_df = pd.DataFrame({
            'Métrica': ['Receitas', 'Despesas', 'Saldo'],
            'Valor Atual': [
                report_data['summary']['income']['current'],
                report_data['summary']['expenses']['current'],
                report_data['summary']['balance']['current']
            ],
            'Valor Anterior': [
                report_data['summary']['income']['previous'],
                report_data['summary']['expenses']['previous'],
                report_data['summary']['balance']['previous']
            ],
            'Variação (%)': [
                report_data['summary']['income']['change_percentage'],
                report_data['summary']['expenses']['change_percentage'],
                report_data['summary']['balance']['change_percentage']
            ]
        })
        
        summary_df.to_excel(writer, sheet_name='Resumo', index=False)
        
        # Planilha de Categorias
        if report_data['categories']['all']:
            categories_df = pd.DataFrame([
                {
                    'Nome': cat['name'],
                    'Receitas': cat['income'],
                    'Despesas': cat['expenses'],
                    'Transações': cat['transactions']
                } for cat in report_data['categories']['all']
            ])
            
            categories_df.to_excel(writer, sheet_name='Categorias', index=False)
        
        # Planilha de Série Temporal
        if report_data['time_series']:
            time_series_df = pd.DataFrame([
                {
                    'Data': ts['date'],
                    'Receitas': ts['income'],
                    'Despesas': ts['expenses'],
                    'Saldo': ts['balance']
                } for ts in report_data['time_series']
            ])
            
            time_series_df.to_excel(writer, sheet_name='Série Temporal', index=False)
        
        # Planilha de Análise
        analysis_df = pd.DataFrame({
            'Métrica': [
                'Despesa média diária',
                'Valor médio por transação',
                'Dia com maior despesa',
                'Dia com maior receita'
            ],
            'Valor': [
                report_data['analysis']['avg_daily_expense'],
                report_data['analysis']['avg_transaction_value'],
                report_data['analysis']['most_expensive_day'] or 'N/A',
                report_data['analysis']['highest_income_day'] or 'N/A'
            ]
        })
        
        analysis_df.to_excel(writer, sheet_name='Análise', index=False)
    
    # Resetar o ponteiro do arquivo
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        attachment_filename=f"relatorio_financeiro_{report_data['summary']['period']['start_date']}_a_{report_data['summary']['period']['end_date']}.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ) 