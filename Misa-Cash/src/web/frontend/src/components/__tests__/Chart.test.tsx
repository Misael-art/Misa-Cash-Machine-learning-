import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Chart from '../Chart';

const mockData = {
  labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
  datasets: [
    {
      label: 'Vendas',
      data: [12, 19, 3, 5, 2, 3],
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    },
  ],
};

const mockOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Vendas por Mês',
    },
  },
};

describe('Chart Component', () => {
  it('renderiza corretamente com dados e opções', () => {
    render(<Chart type="line" data={mockData} options={mockOptions} />);
    expect(screen.getByRole('img')).toBeInTheDocument();
  });

  it('renderiza corretamente com título', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        title="Gráfico de Vendas"
      />
    );
    expect(screen.getByText('Gráfico de Vendas')).toBeInTheDocument();
  });

  it('renderiza corretamente com descrição', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        description="Análise de vendas mensais"
      />
    );
    expect(screen.getByText('Análise de vendas mensais')).toBeInTheDocument();
  });

  it('renderiza corretamente com loading', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        loading
      />
    );
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renderiza corretamente com erro', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        error="Erro ao carregar gráfico"
      />
    );
    expect(screen.getByText('Erro ao carregar gráfico')).toBeInTheDocument();
  });

  it('renderiza corretamente com tipo de gráfico personalizado', () => {
    render(<Chart type="bar" data={mockData} options={mockOptions} />);
    expect(screen.getByRole('img')).toHaveAttribute('data-chart-type', 'bar');
  });

  it('renderiza corretamente com altura personalizada', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        height={400}
      />
    );
    expect(screen.getByRole('img')).toHaveStyle({ height: '400px' });
  });

  it('renderiza corretamente com largura personalizada', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        width={600}
      />
    );
    expect(screen.getByRole('img')).toHaveStyle({ width: '600px' });
  });

  it('renderiza corretamente com padding personalizado', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        padding="p-8"
      />
    );
    expect(screen.getByRole('img').parentElement).toHaveClass('p-8');
  });

  it('renderiza corretamente com background personalizado', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        background="bg-gray-100"
      />
    );
    expect(screen.getByRole('img').parentElement).toHaveClass('bg-gray-100');
  });

  it('renderiza corretamente com borda personalizada', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        border="border-2 border-blue-500"
      />
    );
    expect(screen.getByRole('img').parentElement).toHaveClass('border-2', 'border-blue-500');
  });

  it('renderiza corretamente com sombra personalizada', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        shadow="shadow-xl"
      />
    );
    expect(screen.getByRole('img').parentElement).toHaveClass('shadow-xl');
  });

  it('renderiza corretamente com overflow personalizado', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        overflow="overflow-auto"
      />
    );
    expect(screen.getByRole('img').parentElement).toHaveClass('overflow-auto');
  });

  it('renderiza corretamente com cursor personalizado', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        cursor="cursor-pointer"
      />
    );
    expect(screen.getByRole('img').parentElement).toHaveClass('cursor-pointer');
  });

  it('renderiza corretamente com transição personalizada', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={mockOptions}
        transition="transition-all duration-300"
      />
    );
    expect(screen.getByRole('img').parentElement).toHaveClass('transition-all', 'duration-300');
  });

  it('renderiza corretamente com interatividade personalizada', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={{
          ...mockOptions,
          interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false,
          },
        }}
      />
    );
    expect(screen.getByRole('img')).toHaveAttribute('data-interaction-mode', 'nearest');
  });

  it('renderiza corretamente com animação personalizada', () => {
    render(
      <Chart
        type="line"
        data={mockData}
        options={{
          ...mockOptions,
          animation: {
            duration: 2000,
            easing: 'easeInOutQuart',
          },
        }}
      />
    );
    expect(screen.getByRole('img')).toHaveAttribute('data-animation-duration', '2000');
  });
}); 