import { Trade, Strategy, BacktestResult } from '@/types';

// Cálculo de retorno total
export const calculateTotalReturn = (trades: Trade[]): number => {
  return trades.reduce((total, trade) => total + trade.pnl, 0);
};

// Cálculo de taxa de acerto
export const calculateWinRate = (trades: Trade[]): number => {
  if (trades.length === 0) return 0;
  const winningTrades = trades.filter((trade) => trade.pnl > 0);
  return (winningTrades.length / trades.length) * 100;
};

// Cálculo de drawdown máximo
export const calculateMaxDrawdown = (trades: Trade[]): number => {
  let peak = 0;
  let maxDrawdown = 0;
  let currentValue = 0;

  trades.forEach((trade) => {
    currentValue += trade.pnl;
    if (currentValue > peak) {
      peak = currentValue;
    }
    const drawdown = peak - currentValue;
    if (drawdown > maxDrawdown) {
      maxDrawdown = drawdown;
    }
  });

  return maxDrawdown;
};

// Cálculo do índice de Sharpe
export const calculateSharpeRatio = (trades: Trade[], riskFreeRate = 0.02): number => {
  if (trades.length === 0) return 0;

  const returns = trades.map((trade) => trade.pnlPercentage);
  const avgReturn = returns.reduce((sum, ret) => sum + ret, 0) / returns.length;
  const stdDev = Math.sqrt(
    returns.reduce((sum, ret) => sum + Math.pow(ret - avgReturn, 2), 0) / returns.length
  );

  if (stdDev === 0) return 0;

  return (avgReturn - riskFreeRate) / stdDev;
};

// Agrupamento de trades por período
export const groupTradesByPeriod = (trades: Trade[], period: 'day' | 'week' | 'month'): Record<string, Trade[]> => {
  const groupedTrades: Record<string, Trade[]> = {};

  trades.forEach((trade) => {
    const date = new Date(trade.timestamp);
    let key: string;

    switch (period) {
      case 'day':
        key = date.toISOString().split('T')[0];
        break;
      case 'week':
        const weekNumber = Math.ceil((date.getDate() + date.getDay()) / 7);
        key = `${date.getFullYear()}-W${weekNumber}`;
        break;
      case 'month':
        key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        break;
    }

    if (!groupedTrades[key]) {
      groupedTrades[key] = [];
    }
    groupedTrades[key].push(trade);
  });

  return groupedTrades;
};

// Ordenação de estratégias por performance
export const sortStrategiesByPerformance = (
  strategies: Strategy[],
  metric: 'totalReturn' | 'sharpeRatio' | 'winRate' | 'maxDrawdown',
  ascending = false
): Strategy[] => {
  return [...strategies].sort((a, b) => {
    const valueA = a.performance[metric];
    const valueB = b.performance[metric];
    return ascending ? valueA - valueB : valueB - valueA;
  });
};

// Filtragem de resultados de backtest
export const filterBacktestResults = (
  results: BacktestResult[],
  filters: {
    minReturn?: number;
    maxDrawdown?: number;
    minWinRate?: number;
    minSharpeRatio?: number;
  }
): BacktestResult[] => {
  return results.filter((result) => {
    if (filters.minReturn && result.totalReturn < filters.minReturn) return false;
    if (filters.maxDrawdown && result.maxDrawdown > filters.maxDrawdown) return false;
    if (filters.minWinRate && result.winRate < filters.minWinRate) return false;
    if (filters.minSharpeRatio && result.sharpeRatio < filters.minSharpeRatio) return false;
    return true;
  });
}; 