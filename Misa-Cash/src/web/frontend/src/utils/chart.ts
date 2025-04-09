import { formatCurrencyBR, formatPercentage, formatDate } from './format';

// Configurações padrão para gráficos
export const defaultChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
      labels: {
        font: {
          family: 'Inter, sans-serif',
        },
      },
    },
    tooltip: {
      mode: 'index' as const,
      intersect: false,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleFont: {
        family: 'Inter, sans-serif',
        size: 14,
      },
      bodyFont: {
        family: 'Inter, sans-serif',
        size: 13,
      },
      padding: 12,
      cornerRadius: 4,
    },
  },
};

// Cores padrão para gráficos
export const chartColors = {
  primary: '#3182CE',
  secondary: '#805AD5',
  success: '#38A169',
  warning: '#D69E2E',
  danger: '#E53E3E',
  info: '#4299E1',
  gray: '#718096',
  colors: [
    '#3182CE',
    '#805AD5',
    '#38A169',
    '#D69E2E',
    '#E53E3E',
    '#4299E1',
    '#718096',
    '#2C5282',
    '#553C9A',
    '#276749',
    '#975A16',
    '#9B2C2C',
    '#2B6CB0',
    '#4A5568',
  ],
};

// Configuração para gráfico de linha
export const getLineChartConfig = (
  labels: string[],
  datasets: { label: string; data: number[]; color?: string }[]
) => {
  return {
    type: 'line' as const,
    data: {
      labels,
      datasets: datasets.map((dataset, index) => ({
        label: dataset.label,
        data: dataset.data,
        borderColor: dataset.color || chartColors.colors[index % chartColors.colors.length],
        backgroundColor: dataset.color || chartColors.colors[index % chartColors.colors.length],
        borderWidth: 2,
        tension: 0.4,
        fill: false,
      })),
    },
    options: {
      ...defaultChartOptions,
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            font: {
              family: 'Inter, sans-serif',
            },
          },
        },
        y: {
          grid: {
            color: 'rgba(0, 0, 0, 0.1)',
          },
          ticks: {
            font: {
              family: 'Inter, sans-serif',
            },
            callback: (value: number) => formatCurrencyBR(value),
          },
        },
      },
    },
  };
};

// Configuração para gráfico de barras
export const getBarChartConfig = (
  labels: string[],
  datasets: { label: string; data: number[]; color?: string }[]
) => {
  return {
    type: 'bar' as const,
    data: {
      labels,
      datasets: datasets.map((dataset, index) => ({
        label: dataset.label,
        data: dataset.data,
        backgroundColor: dataset.color || chartColors.colors[index % chartColors.colors.length],
        borderWidth: 0,
        borderRadius: 4,
      })),
    },
    options: {
      ...defaultChartOptions,
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            font: {
              family: 'Inter, sans-serif',
            },
          },
        },
        y: {
          grid: {
            color: 'rgba(0, 0, 0, 0.1)',
          },
          ticks: {
            font: {
              family: 'Inter, sans-serif',
            },
            callback: (value: number) => formatCurrencyBR(value),
          },
        },
      },
    },
  };
};

// Configuração para gráfico de pizza
export const getPieChartConfig = (
  labels: string[],
  data: number[],
  colors?: string[]
) => {
  return {
    type: 'pie' as const,
    data: {
      labels,
      datasets: [
        {
          data,
          backgroundColor: colors || chartColors.colors,
          borderWidth: 0,
        },
      ],
    },
    options: {
      ...defaultChartOptions,
      plugins: {
        ...defaultChartOptions.plugins,
        tooltip: {
          ...defaultChartOptions.plugins.tooltip,
          callbacks: {
            label: (context: any) => {
              const label = context.label || '';
              const value = context.raw || 0;
              const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
              const percentage = ((value / total) * 100).toFixed(1);
              return `${label}: ${formatCurrencyBR(value)} (${percentage}%)`;
            },
          },
        },
      },
    },
  };
};

// Configuração para gráfico de dispersão
export const getScatterChartConfig = (
  datasets: { label: string; data: { x: number; y: number }[]; color?: string }[]
) => {
  return {
    type: 'scatter' as const,
    data: {
      datasets: datasets.map((dataset, index) => ({
        label: dataset.label,
        data: dataset.data,
        backgroundColor: dataset.color || chartColors.colors[index % chartColors.colors.length],
        borderColor: dataset.color || chartColors.colors[index % chartColors.colors.length],
        borderWidth: 1,
        pointRadius: 4,
        pointHoverRadius: 6,
      })),
    },
    options: {
      ...defaultChartOptions,
      scales: {
        x: {
          type: 'linear' as const,
          position: 'bottom' as const,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)',
          },
          ticks: {
            font: {
              family: 'Inter, sans-serif',
            },
          },
        },
        y: {
          grid: {
            color: 'rgba(0, 0, 0, 0.1)',
          },
          ticks: {
            font: {
              family: 'Inter, sans-serif',
            },
          },
        },
      },
    },
  };
};

// Configuração para gráfico de área
export const getAreaChartConfig = (
  labels: string[],
  datasets: { label: string; data: number[]; color?: string }[]
) => {
  return {
    type: 'line' as const,
    data: {
      labels,
      datasets: datasets.map((dataset, index) => ({
        label: dataset.label,
        data: dataset.data,
        borderColor: dataset.color || chartColors.colors[index % chartColors.colors.length],
        backgroundColor: dataset.color || chartColors.colors[index % chartColors.colors.length],
        borderWidth: 2,
        tension: 0.4,
        fill: true,
      })),
    },
    options: {
      ...defaultChartOptions,
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            font: {
              family: 'Inter, sans-serif',
            },
          },
        },
        y: {
          grid: {
            color: 'rgba(0, 0, 0, 0.1)',
          },
          ticks: {
            font: {
              family: 'Inter, sans-serif',
            },
            callback: (value: number) => formatCurrencyBR(value),
          },
        },
      },
    },
  };
}; 