import React from 'react';
import TransactionChart from './TransactionChart';

interface CategoryData {
  category: string;
  total: number;
  percentage: number;
}

interface CategoryDistributionProps {
  data: CategoryData[];
  type: 'income' | 'expense' | 'all';
  onTypeChange: (type: 'income' | 'expense' | 'all') => void;
}

/**
 * Componente para exibir a distribuição de gastos/receitas por categoria.
 */
const CategoryDistribution: React.FC<CategoryDistributionProps> = ({ 
  data, 
  type, 
  onTypeChange 
}) => {
  // Cores para as categorias de despesas
  const expenseColors = [
    '#ff6384', '#ff9f40', '#ffcd56', '#36a2eb', '#4bc0c0', 
    '#9966ff', '#c9cbcf', '#8a2be2', '#ff7f50', '#20b2aa'
  ];
  
  // Cores para as categorias de receitas
  const incomeColors = [
    '#36a2eb', '#4bc0c0', '#9966ff', '#ffcd56', '#ff9f40'
  ];
  
  // Seleciona as cores com base no tipo
  const colors = type === 'income' ? incomeColors : expenseColors;
  
  // Prepara os dados para o gráfico
  const chartData = {
    labels: data.map(item => item.category),
    datasets: [
      {
        label: type === 'income' ? 'Receitas' : 'Despesas',
        data: data.map(item => item.total),
        backgroundColor: colors,
        borderWidth: 1
      }
    ]
  };
  
  return (
    <div className="category-distribution">
      <div className="category-distribution-header">
        <h3>Distribuição por Categoria</h3>
        <div className="type-selector">
          <button
            className={`type-button ${type === 'expense' ? 'active' : ''}`}
            onClick={() => onTypeChange('expense')}
          >
            Despesas
          </button>
          <button
            className={`type-button ${type === 'income' ? 'active' : ''}`}
            onClick={() => onTypeChange('income')}
          >
            Receitas
          </button>
        </div>
      </div>
      
      <div className="chart-and-legend">
        <div className="chart-container">
          <TransactionChart
            data={chartData}
            type="doughnut"
            title=""
            height={250}
            showLegend={false}
          />
        </div>
        
        <div className="category-legend">
          {data.map((item, index) => (
            <div key={item.category} className="category-item">
              <div className="category-color" style={{ backgroundColor: colors[index % colors.length] }}></div>
              <div className="category-name">{item.category}</div>
              <div className="category-percentage">{item.percentage.toFixed(1)}%</div>
              <div className="category-total">
                {new Intl.NumberFormat('pt-BR', {
                  style: 'currency',
                  currency: 'BRL'
                }).format(item.total)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CategoryDistribution; 