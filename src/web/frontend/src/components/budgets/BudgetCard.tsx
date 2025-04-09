import React from 'react';
import { FiEdit2, FiTrash2 } from 'react-icons/fi';
import { Budget } from './BudgetsList';
import BudgetProgressBar from './BudgetProgressBar';

interface BudgetCardProps {
  budget: Budget;
  onEdit: (budget: Budget) => void;
  onDelete: (budgetId: string) => void;
}

const BudgetCard: React.FC<BudgetCardProps> = ({ budget, onEdit, onDelete }) => {
  const { id, name, category, amount, spent, period } = budget;
  
  // Calcular porcentagem gasta
  const percentage = amount > 0 ? (spent / amount) * 100 : 0;
  
  // Formatar valores em moeda
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };
  
  // Determinar o status do orçamento com base na porcentagem gasta
  const getStatusInfo = () => {
    if (percentage >= 100) {
      return {
        text: 'Excedido',
        className: 'text-red-600'
      };
    } else if (percentage >= 85) {
      return {
        text: 'Alerta',
        className: 'text-orange-500'
      };
    } else if (percentage >= 50) {
      return {
        text: 'Em progresso',
        className: 'text-blue-600'
      };
    } else {
      return {
        text: 'Controlado',
        className: 'text-green-600'
      };
    }
  };
  
  const { text: statusText, className: statusClassName } = getStatusInfo();
  
  return (
    <div className="bg-white rounded-lg shadow-md p-5 border border-gray-100 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-medium text-gray-800">{name}</h3>
          <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
            {category}
          </span>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onEdit(budget)}
            className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
            aria-label="Editar orçamento"
          >
            <FiEdit2 size={18} />
          </button>
          <button
            onClick={() => onDelete(id)}
            className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
            aria-label="Excluir orçamento"
          >
            <FiTrash2 size={18} />
          </button>
        </div>
      </div>
      
      <div className="mb-4">
        <div className="flex justify-between mb-1">
          <span className="text-sm text-gray-600">Período: {period}</span>
          <span className={`text-sm font-medium ${statusClassName}`}>{statusText}</span>
        </div>
        
        <BudgetProgressBar percentage={percentage} />
        
        <div className="flex justify-between mt-2 text-sm">
          <span className="text-gray-600">Gasto: {formatCurrency(spent)}</span>
          <span className="text-gray-600">Meta: {formatCurrency(amount)}</span>
        </div>
      </div>
      
      <div className="pt-3 border-t border-gray-100">
        <div className="flex justify-between">
          <span className="text-gray-700">Disponível:</span>
          <span className={`font-medium ${spent > amount ? 'text-red-600' : 'text-green-600'}`}>
            {formatCurrency(Math.max(amount - spent, 0))}
          </span>
        </div>
      </div>
    </div>
  );
};

export default BudgetCard; 