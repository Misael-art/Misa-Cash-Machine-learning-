import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  ArcElement,
  ChartData,
  ChartOptions
} from 'chart.js';
import { Bar, Line, Pie, Doughnut } from 'react-chartjs-2';

// Registra os componentes necessários para o Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// Tipos de gráficos disponíveis
export type ChartType = 'bar' | 'line' | 'pie' | 'doughnut';

// Props do componente
interface TransactionChartProps {
  // Dados para o gráfico
  data: {
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      backgroundColor?: string | string[];
      borderColor?: string | string[];
      borderWidth?: number;
    }[];
  };
  // Tipo de gráfico
  type: ChartType;
  // Título do gráfico
  title: string;
  // Altura do gráfico
  height?: number;
  // Mostrar legenda
  showLegend?: boolean;
  // Opções adicionais do gráfico
  options?: ChartOptions<ChartType>;
}

/**
 * Componente de gráfico de transações.
 * Suporta diferentes tipos de gráficos (barra, linha, pizza, rosca).
 */
const TransactionChart: React.FC<TransactionChartProps> = ({
  data,
  type,
  title,
  height = 300,
  showLegend = true,
  options = {}
}) => {
  // Estado para armazenar as opções finais do gráfico
  const [chartOptions, setChartOptions] = useState<ChartOptions<ChartType>>({});
  
  // Configura as opções do gráfico quando as props mudam
  useEffect(() => {
    setChartOptions({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: showLegend,
          position: 'top' as const,
        },
        title: {
          display: !!title,
          text: title,
          font: {
            size: 16,
          }
        },
        tooltip: {
          callbacks: {
            label: function(context: any) {
              const value = context.parsed.y || context.parsed || 0;
              return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
              }).format(value);
            }
          }
        }
      },
      ...options
    });
  }, [title, showLegend, options]);

  // Renderiza o gráfico de acordo com o tipo
  const renderChart = () => {
    switch (type) {
      case 'bar':
        return <Bar data={data} options={chartOptions} height={height} />;
      case 'line':
        return <Line data={data} options={chartOptions} height={height} />;
      case 'pie':
        return <Pie data={data} options={chartOptions} height={height} />;
      case 'doughnut':
        return <Doughnut data={data} options={chartOptions} height={height} />;
      default:
        return <Bar data={data} options={chartOptions} height={height} />;
    }
  };

  return (
    <div className="chart-container" style={{ height }}>
      {renderChart()}
    </div>
  );
};

export default TransactionChart; 