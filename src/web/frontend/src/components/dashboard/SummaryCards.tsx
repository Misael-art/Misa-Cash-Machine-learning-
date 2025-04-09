import React from 'react';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

interface SummaryCardsProps {
  totalIncome: number;
  totalExpense: number;
  balance: number;
  period: 'week' | 'month' | 'year';
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
};

const getPeriodLabel = (period: 'week' | 'month' | 'year'): string => {
  const currentDate = new Date();
  
  switch (period) {
    case 'week':
      return `Semana de ${format(currentDate, 'd', { locale: ptBR })} de ${format(currentDate, 'MMMM', { locale: ptBR })}`;
    case 'month':
      return format(currentDate, 'MMMM yyyy', { locale: ptBR });
    case 'year':
      return format(currentDate, 'yyyy');
    default:
      return '';
  }
};

const SummaryCards: React.FC<SummaryCardsProps> = ({ 
  totalIncome, 
  totalExpense, 
  balance,
  period
}) => {
  const periodLabel = getPeriodLabel(period);
  
  return (
    <div className="summary-cards">
      <div className="summary-period">
        <h3>{periodLabel}</h3>
      </div>
      
      <div className="cards-container">
        <div className="summary-card income">
          <div className="card-icon">
            <i className="fas fa-arrow-circle-up"></i>
          </div>
          <div className="card-content">
            <h4>Receitas</h4>
            <p className="amount">{formatCurrency(totalIncome)}</p>
          </div>
        </div>
        
        <div className="summary-card expense">
          <div className="card-icon">
            <i className="fas fa-arrow-circle-down"></i>
          </div>
          <div className="card-content">
            <h4>Despesas</h4>
            <p className="amount">{formatCurrency(totalExpense)}</p>
          </div>
        </div>
        
        <div className={`summary-card balance ${balance >= 0 ? 'positive' : 'negative'}`}>
          <div className="card-icon">
            <i className={`fas fa-${balance >= 0 ? 'wallet' : 'exclamation-triangle'}`}></i>
          </div>
          <div className="card-content">
            <h4>Saldo</h4>
            <p className="amount">{formatCurrency(balance)}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SummaryCards; 