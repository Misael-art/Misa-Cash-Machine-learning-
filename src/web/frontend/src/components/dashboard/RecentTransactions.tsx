import React from 'react';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Transaction } from '../../services/transactions';

interface RecentTransactionsProps {
  transactions: Transaction[];
  maxItems?: number;
  onViewAll?: () => void;
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
};

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  return format(date, 'dd/MM/yyyy', { locale: ptBR });
};

const getTransactionIcon = (type: string, category: string): string => {
  // Ícones com base no tipo e categoria da transação
  const icons: Record<string, Record<string, string>> = {
    income: {
      salary: 'money-bill-wave',
      investment: 'chart-line',
      gift: 'gift',
      default: 'arrow-circle-up'
    },
    expense: {
      food: 'utensils',
      transport: 'car',
      health: 'heartbeat',
      education: 'book',
      housing: 'home',
      entertainment: 'film',
      shopping: 'shopping-cart',
      default: 'arrow-circle-down'
    }
  };

  const categoryIcons = icons[type] || icons.expense;
  return categoryIcons[category] || categoryIcons.default;
};

const RecentTransactions: React.FC<RecentTransactionsProps> = ({
  transactions,
  maxItems = 5,
  onViewAll
}) => {
  return (
    <div className="recent-transactions-container">
      <div className="recent-transactions-header">
        <h3>Transações Recentes</h3>
        {onViewAll && (
          <button className="view-all-button" onClick={onViewAll}>
            Ver todas
          </button>
        )}
      </div>

      {transactions.length === 0 ? (
        <div className="no-transactions">
          <p>Nenhuma transação encontrada.</p>
        </div>
      ) : (
        <div className="transactions-list">
          {transactions.slice(0, maxItems).map((transaction) => (
            <div key={transaction.id} className={`transaction-item ${transaction.type}`}>
              <div className="transaction-icon">
                <i className={`fas fa-${getTransactionIcon(transaction.type, transaction.category)}`}></i>
              </div>
              <div className="transaction-info">
                <div className="transaction-description">{transaction.description}</div>
                <div className="transaction-details">
                  <span className="transaction-category">{transaction.category}</span>
                  <span className="transaction-date">{formatDate(transaction.date)}</span>
                </div>
              </div>
              <div className="transaction-amount">
                {formatCurrency(transaction.amount)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecentTransactions; 