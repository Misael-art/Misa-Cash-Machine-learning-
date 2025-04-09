import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTransactions } from '../../contexts/TransactionContext';
import { useAuthContext } from '../../contexts/AuthContext';

// Componentes
import SummaryCards from '../../components/dashboard/SummaryCards';
import RecentTransactions from '../../components/dashboard/RecentTransactions';
import TransactionChart from '../../components/dashboard/TransactionChart';
import PeriodSelector from '../../components/dashboard/PeriodSelector';
import CategoryDistribution from '../../components/dashboard/CategoryDistribution';

type Period = 'week' | 'month' | 'year';
type ChartView = 'category' | 'timeline' | 'comparison';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthContext();
  const { 
    loading, 
    error, 
    summary, 
    chartData, 
    fetchSummary, 
    fetchChartData,
    fetchTransactions
  } = useTransactions();

  // Estados locais
  const [period, setPeriod] = useState<Period>('month');
  const [chartType, setChartType] = useState<ChartView>('timeline');
  const [transactionType, setTransactionType] = useState<'income' | 'expense' | 'all'>('expense');

  // Buscar dados quando o período mudar
  useEffect(() => {
    fetchSummary(period);
    fetchChartData('timeline', period, 'all');
    fetchTransactions({ 
      startDate: getStartDateForPeriod(period),
      endDate: new Date().toISOString(),
      limit: 5,
      sort: 'date',
      order: 'desc'
    });
  }, [period, fetchSummary, fetchChartData, fetchTransactions]);

  // Buscar dados do gráfico quando o tipo de transação mudar
  useEffect(() => {
    fetchChartData(chartType, period, transactionType);
  }, [chartType, period, transactionType, fetchChartData]);

  // Função auxiliar para calcular a data inicial com base no período
  const getStartDateForPeriod = (selectedPeriod: Period): string => {
    const today = new Date();
    let startDate = new Date();

    switch (selectedPeriod) {
      case 'week':
        startDate.setDate(today.getDate() - 7);
        break;
      case 'month':
        startDate.setMonth(today.getMonth() - 1);
        break;
      case 'year':
        startDate.setFullYear(today.getFullYear() - 1);
        break;
    }

    return startDate.toISOString();
  };

  // Manipuladores de eventos
  const handlePeriodChange = (newPeriod: Period) => {
    setPeriod(newPeriod);
  };

  const handleChartTypeChange = (newType: ChartView) => {
    setChartType(newType);
  };

  const handleTransactionTypeChange = (newType: 'income' | 'expense' | 'all') => {
    setTransactionType(newType);
  };

  const handleViewAllTransactions = () => {
    navigate('/transactions');
  };

  // Renderização condicional enquanto carrega
  if (loading && !summary) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Carregando dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Dashboard Financeiro</h2>
        <div className="user-welcome">
          Olá, {user?.username || 'Usuário'}!
        </div>
        <PeriodSelector period={period} onChange={handlePeriodChange} />
      </div>

      {error && (
        <div className="dashboard-error">
          <p>{error}</p>
        </div>
      )}

      {summary && (
        <SummaryCards
          totalIncome={summary.totalIncome}
          totalExpense={summary.totalExpense}
          balance={summary.balance}
          period={period}
        />
      )}

      <div className="dashboard-charts">
        <div className="chart-row">
          <div className="chart-card timeline-chart">
            <div className="chart-header">
              <h3>Fluxo de Caixa</h3>
              <div className="chart-type-selector">
                <button
                  className={`chart-type-button ${chartType === 'timeline' ? 'active' : ''}`}
                  onClick={() => handleChartTypeChange('timeline')}
                >
                  Linha do Tempo
                </button>
                <button
                  className={`chart-type-button ${chartType === 'comparison' ? 'active' : ''}`}
                  onClick={() => handleChartTypeChange('comparison')}
                >
                  Comparativo
                </button>
              </div>
            </div>
            {chartData && (
              <TransactionChart
                data={chartData}
                type={chartType === 'timeline' ? 'line' : 'bar'}
                title=""
                height={300}
              />
            )}
          </div>

          <div className="chart-card category-chart">
            {summary && (
              <CategoryDistribution
                data={summary.categoriesSummary.filter(cat => 
                  transactionType === 'all' || 
                  (transactionType === 'income' && cat.category.includes('Receita')) ||
                  (transactionType === 'expense' && !cat.category.includes('Receita'))
                )}
                type={transactionType}
                onTypeChange={handleTransactionTypeChange}
              />
            )}
          </div>
        </div>
      </div>

      <div className="dashboard-recent-transactions">
        {summary && (
          <RecentTransactions
            transactions={summary.recentTransactions}
            maxItems={5}
            onViewAll={handleViewAllTransactions}
          />
        )}
      </div>
    </div>
  );
};

export default Dashboard; 