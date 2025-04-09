import React from 'react';
import BudgetCard from './BudgetCard';

interface Budget {
  id: number;
  name: string;
  category: string;
  amount: number;
  spent: number;
  period: string;
}

interface BudgetsListProps {
  budgets: Budget[];
  onEdit: (budget: Budget) => void;
  onDelete: (budgetId: number) => void;
}

const BudgetsList: React.FC<BudgetsListProps> = ({ budgets, onEdit, onDelete }) => {
  if (budgets.length === 0) {
    return (
      <div className="no-budgets-container">
        <p className="no-budgets-message">Nenhum orçamento encontrado. Crie seu primeiro orçamento!</p>
      </div>
    );
  }

  return (
    <div className="budgets-list">
      {budgets.map(budget => (
        <BudgetCard
          key={budget.id}
          budget={budget}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default BudgetsList; 