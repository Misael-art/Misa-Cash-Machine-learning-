import React from 'react';

interface BudgetProgressBarProps {
  percentage: number;
}

const BudgetProgressBar: React.FC<BudgetProgressBarProps> = ({ percentage }) => {
  // Garantir que a porcentagem esteja entre 0 e 100
  const safePercentage = Math.min(Math.max(0, percentage), 100);
  
  // Determinar a cor da barra de progresso com base na porcentagem
  const getBarColor = () => {
    if (safePercentage >= 100) {
      return 'bg-red-500';
    } else if (safePercentage >= 85) {
      return 'bg-orange-500';
    } else if (safePercentage >= 50) {
      return 'bg-blue-500';
    } else {
      return 'bg-green-500';
    }
  };
  
  return (
    <div className="w-full bg-gray-200 rounded-full h-2.5 mb-1">
      <div 
        className={`h-2.5 rounded-full ${getBarColor()}`}
        style={{ width: `${safePercentage}%` }}
        role="progressbar"
        aria-valuenow={safePercentage}
        aria-valuemin={0}
        aria-valuemax={100}
      />
    </div>
  );
};

export default BudgetProgressBar; 