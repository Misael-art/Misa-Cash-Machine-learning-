import React from 'react';

interface BudgetSummaryCardProps {
  title: string;
  value: number | string;
  icon: string;
  iconClass: string;
  percentageChange?: number;
  isCurrency?: boolean;
  isPercentage?: boolean;
}

const BudgetSummaryCard: React.FC<BudgetSummaryCardProps> = ({
  title,
  value,
  icon,
  iconClass,
  percentageChange,
  isCurrency = false,
  isPercentage = false,
}) => {
  // Formatação de valores monetários
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  // Formatação de percentuais
  const formatPercentage = (value: number): string => {
    return `${value.toFixed(1)}%`;
  };

  // Formatação do valor de acordo com o tipo
  const formattedValue = typeof value === 'number' 
    ? (isCurrency 
        ? formatCurrency(value) 
        : (isPercentage 
            ? formatPercentage(value) 
            : value.toString()))
    : value;

  // Determina a classe e ícone para o percentual de mudança
  const getPercentageChangeClass = () => {
    if (!percentageChange) return '';
    return percentageChange > 0 ? 'percentage-positive' : 'percentage-negative';
  };

  const getPercentageChangeIcon = () => {
    if (!percentageChange) return '';
    return percentageChange > 0 ? 'fa-arrow-up' : 'fa-arrow-down';
  };

  return (
    <div className="summary-card">
      <div className="summary-card-header">
        <div className={`summary-card-icon ${iconClass}`}>
          <i className={`fas ${icon}`}></i>
        </div>
        <h3 className="summary-card-title">{title}</h3>
      </div>
      <div className="summary-card-value">{formattedValue}</div>
      {percentageChange !== undefined && (
        <div className={`summary-card-percentage ${getPercentageChangeClass()}`}>
          <i className={`fas ${getPercentageChangeIcon()}`}></i>
          <span>{Math.abs(percentageChange).toFixed(1)}% em relação ao período anterior</span>
        </div>
      )}
    </div>
  );
};

export default BudgetSummaryCard; 