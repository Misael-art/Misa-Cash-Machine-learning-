import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Chart from '../../components/Chart';
import Button from '../../components/Button';
import Input from '../../components/Input';
import Select from '../../components/Select';
import Card from '../../components/Card';

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

describe('Chart Integration', () => {
  it('integra corretamente Chart com Card e controles', async () => {
    const onTypeChange = jest.fn();
    const onPeriodChange = jest.fn();

    render(
      <Card title="Análise de Vendas">
        <div className="controls">
          <Select
            label="Tipo de Gráfico"
            options={[
              { value: 'line', label: 'Linha' },
              { value: 'bar', label: 'Barra' },
              { value: 'pie', label: 'Pizza' },
            ]}
            onChange={(e) => onTypeChange(e.target.value)}
          />
          <Select
            label="Período"
            options={[
              { value: 'day', label: 'Diário' },
              { value: 'week', label: 'Semanal' },
              { value: 'month', label: 'Mensal' },
            ]}
            onChange={(e) => onPeriodChange(e.target.value)}
          />
        </div>
        <Chart
          type="line"
          data={mockData}
          options={mockOptions}
        />
      </Card>
    );

    expect(screen.getByText('Análise de Vendas')).toBeInTheDocument();
    expect(screen.getByText('Tipo de Gráfico')).toBeInTheDocument();
    expect(screen.getByText('Período')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('Tipo de Gráfico'), {
      target: { value: 'bar' },
    });
    expect(onTypeChange).toHaveBeenCalledWith('bar');

    fireEvent.change(screen.getByLabelText('Período'), {
      target: { value: 'week' },
    });
    expect(onPeriodChange).toHaveBeenCalledWith('week');
  });

  it('integra corretamente Chart com filtros dinâmicos', async () => {
    const onFilterChange = jest.fn();
    const [startDate, setStartDate] = React.useState('2024-01-01');
    const [endDate, setEndDate] = React.useState('2024-12-31');

    render(
      <div>
        <div className="filters">
          <Input
            type="date"
            label="Data Inicial"
            value={startDate}
            onChange={(e) => {
              setStartDate(e.target.value);
              onFilterChange({ startDate: e.target.value, endDate });
            }}
          />
          <Input
            type="date"
            label="Data Final"
            value={endDate}
            onChange={(e) => {
              setEndDate(e.target.value);
              onFilterChange({ startDate, endDate: e.target.value });
            }}
          />
        </div>
        <Chart
          type="line"
          data={mockData}
          options={mockOptions}
        />
      </div>
    );

    fireEvent.change(screen.getByLabelText('Data Inicial'), {
      target: { value: '2024-02-01' },
    });
    expect(onFilterChange).toHaveBeenCalledWith({
      startDate: '2024-02-01',
      endDate: '2024-12-31',
    });

    fireEvent.change(screen.getByLabelText('Data Final'), {
      target: { value: '2024-06-30' },
    });
    expect(onFilterChange).toHaveBeenCalledWith({
      startDate: '2024-02-01',
      endDate: '2024-06-30',
    });
  });

  it('integra corretamente Chart com exportação de dados', async () => {
    const onExport = jest.fn();

    render(
      <div>
        <Chart
          type="line"
          data={mockData}
          options={mockOptions}
        />
        <div className="actions">
          <Button
            onClick={() => onExport('pdf')}
            variant="primary"
          >
            Exportar PDF
          </Button>
          <Button
            onClick={() => onExport('excel')}
            variant="secondary"
          >
            Exportar Excel
          </Button>
        </div>
      </div>
    );

    fireEvent.click(screen.getByText('Exportar PDF'));
    expect(onExport).toHaveBeenCalledWith('pdf');

    fireEvent.click(screen.getByText('Exportar Excel'));
    expect(onExport).toHaveBeenCalledWith('excel');
  });

  it('integra corretamente Chart com múltiplos datasets e controles', async () => {
    const [selectedDatasets, setSelectedDatasets] = React.useState(['vendas']);
    const multiData = {
      labels: ['Jan', 'Fev', 'Mar'],
      datasets: [
        {
          label: 'Vendas',
          id: 'vendas',
          data: [10, 20, 30],
        },
        {
          label: 'Custos',
          id: 'custos',
          data: [5, 10, 15],
        },
        {
          label: 'Lucro',
          id: 'lucro',
          data: [5, 10, 15],
        },
      ],
    };

    render(
      <Card>
        <div className="controls">
          {multiData.datasets.map((dataset) => (
            <label key={dataset.id}>
              <input
                type="checkbox"
                checked={selectedDatasets.includes(dataset.id)}
                onChange={(e) => {
                  if (e.target.checked) {
                    setSelectedDatasets([...selectedDatasets, dataset.id]);
                  } else {
                    setSelectedDatasets(selectedDatasets.filter(id => id !== dataset.id));
                  }
                }}
              />
              {dataset.label}
            </label>
          ))}
        </div>
        <Chart
          type="line"
          data={{
            ...multiData,
            datasets: multiData.datasets.filter(d => selectedDatasets.includes(d.id)),
          }}
          options={mockOptions}
        />
      </Card>
    );

    expect(screen.getByLabelText('Vendas')).toBeChecked();
    expect(screen.getByLabelText('Custos')).not.toBeChecked();
    expect(screen.getByLabelText('Lucro')).not.toBeChecked();

    fireEvent.click(screen.getByLabelText('Custos'));
    expect(selectedDatasets).toContain('custos');
  });

  it('integra corretamente Chart com comparação de períodos', async () => {
    const [compareEnabled, setCompareEnabled] = React.useState(false);
    const [period1, setPeriod1] = React.useState('2024-01');
    const [period2, setPeriod2] = React.useState('2023-01');

    render(
      <Card>
        <div className="controls">
          <label>
            <input
              type="checkbox"
              checked={compareEnabled}
              onChange={(e) => setCompareEnabled(e.target.checked)}
            />
            Comparar Períodos
          </label>
          
          <Input
            type="month"
            label="Período 1"
            value={period1}
            onChange={(e) => setPeriod1(e.target.value)}
          />

          {compareEnabled && (
            <Input
              type="month"
              label="Período 2"
              value={period2}
              onChange={(e) => setPeriod2(e.target.value)}
            />
          )}
        </div>

        <Chart
          type="line"
          data={{
            ...mockData,
            datasets: compareEnabled
              ? [
                  { ...mockData.datasets[0], label: `Vendas ${period1}` },
                  { ...mockData.datasets[0], label: `Vendas ${period2}` },
                ]
              : mockData.datasets,
          }}
          options={mockOptions}
        />
      </Card>
    );

    expect(screen.getByLabelText('Comparar Períodos')).not.toBeChecked();
    expect(screen.getByLabelText('Período 1')).toBeInTheDocument();
    expect(screen.queryByLabelText('Período 2')).not.toBeInTheDocument();

    fireEvent.click(screen.getByLabelText('Comparar Períodos'));
    expect(screen.getByLabelText('Período 2')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('Período 1'), {
      target: { value: '2024-02' },
    });
    expect(period1).toBe('2024-02');
  });
}); 