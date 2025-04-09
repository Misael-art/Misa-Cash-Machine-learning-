import { Trade, BacktestResult } from '@/types';
import { CHART_COLORS } from '@/constants';
import { formatDate, formatCurrency, formatPercentage } from './format';

// Configuração padrão para gráficos de linha
export const getLineChartConfig = (data: any[], xKey: string, yKey: string) => {
  return {
    data,
    xAxis: {
      dataKey: xKey,
      tickFormatter: (value: string) => formatDate(value),
    },
    yAxis: {
      tickFormatter: (value: number) => formatCurrency(value),
    },
    tooltip: {
      formatter: (value: number) => formatCurrency(value),
    },
  };
};

// Configuração para gráfico de performance
export const getPerformanceChartConfig = (trades: Trade[]) => {
  const cumulativeReturns = trades.reduce((acc: any[], trade) => {
    const lastReturn = acc.length > 0 ? acc[acc.length - 1].value : 0;
    return [
      ...acc,
      {
        date: trade.timestamp,
        value: lastReturn + trade.pnl,
      },
    ];
  }, []);

  return {
    data: cumulativeReturns,
    xAxis: {
      dataKey: 'date',
      tickFormatter: (value: string) => formatDate(value),
    },
    yAxis: {
      tickFormatter: (value: number) => formatCurrency(value),
    },
    tooltip: {
      formatter: (value: number) => formatCurrency(value),
    },
  };
};

// Configuração para gráfico de drawdown
export const getDrawdownChartConfig = (trades: Trade[]) => {
  let peak = 0;
  const drawdowns = trades.reduce((acc: any[], trade) => {
    const currentValue = acc.length > 0 ? acc[acc.length - 1].value + trade.pnl : trade.pnl;
    if (currentValue > peak) {
      peak = currentValue;
    }
    const drawdown = ((peak - currentValue) / peak) * 100;
    return [
      ...acc,
      {
        date: trade.timestamp,
        value: drawdown,
      },
    ];
  }, []);

  return {
    data: drawdowns,
    xAxis: {
      dataKey: 'date',
      tickFormatter: (value: string) => formatDate(value),
    },
    yAxis: {
      tickFormatter: (value: number) => formatPercentage(value),
    },
    tooltip: {
      formatter: (value: number) => formatPercentage(value),
    },
  };
};

// Configuração para gráfico de distribuição de retornos
export const getReturnsDistributionConfig = (trades: Trade[]) => {
  const returns = trades.map((trade) => trade.pnlPercentage);
  const min = Math.min(...returns);
  const max = Math.max(...returns);
  const step = (max - min) / 10;
  const distribution = Array(10).fill(0);

  returns.forEach((ret) => {
    const index = Math.min(Math.floor((ret - min) / step), 9);
    distribution[index]++;
  });

  const data = distribution.map((count, index) => ({
    range: `${formatPercentage(min + index * step)} - ${formatPercentage(min + (index + 1) * step)}`,
    count,
  }));

  return {
    data,
    xAxis: {
      dataKey: 'range',
    },
    yAxis: {
      dataKey: 'count',
    },
    tooltip: {
      formatter: (value: number) => `${value} trades`,
    },
  };
};

// Configuração para gráfico de comparação de estratégias
export const getStrategyComparisonConfig = (results: BacktestResult[]) => {
  const data = results.map((result) => ({
    name: result.strategyId,
    return: result.totalReturn,
    sharpe: result.sharpeRatio,
    winRate: result.winRate,
    drawdown: result.maxDrawdown,
  }));

  return {
    data,
    xAxis: {
      dataKey: 'name',
    },
    yAxis: [
      {
        dataKey: 'return',
        tickFormatter: (value: number) => formatPercentage(value),
      },
      {
        dataKey: 'sharpe',
        tickFormatter: (value: number) => value.toFixed(2),
      },
      {
        dataKey: 'winRate',
        tickFormatter: (value: number) => formatPercentage(value),
      },
      {
        dataKey: 'drawdown',
        tickFormatter: (value: number) => formatPercentage(value),
      },
    ],
    tooltip: {
      formatter: (value: number, name: string) => {
        switch (name) {
          case 'return':
            return formatPercentage(value);
          case 'sharpe':
            return value.toFixed(2);
          case 'winRate':
          case 'drawdown':
            return formatPercentage(value);
          default:
            return value;
        }
      },
    },
  };
}; 