import React from 'react';

type Period = 'week' | 'month' | 'year';

interface PeriodSelectorProps {
  period: Period;
  onChange: (period: Period) => void;
}

/**
 * Componente para selecionar o período de visualização do dashboard
 */
const PeriodSelector: React.FC<PeriodSelectorProps> = ({ period, onChange }) => {
  return (
    <div className="period-selector">
      <div className="period-selector-label">
        Visualizar por:
      </div>
      <div className="period-selector-buttons">
        <button
          className={`period-button ${period === 'week' ? 'active' : ''}`}
          onClick={() => onChange('week')}
        >
          Semana
        </button>
        <button
          className={`period-button ${period === 'month' ? 'active' : ''}`}
          onClick={() => onChange('month')}
        >
          Mês
        </button>
        <button
          className={`period-button ${period === 'year' ? 'active' : ''}`}
          onClick={() => onChange('year')}
        >
          Ano
        </button>
      </div>
    </div>
  );
};

export default PeriodSelector; 