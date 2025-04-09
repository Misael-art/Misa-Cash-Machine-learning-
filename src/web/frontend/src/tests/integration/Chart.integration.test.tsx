import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Box, Card, CardContent, CardHeader, Grid, Select, MenuItem, FormControl, InputLabel, Button, Checkbox, FormControlLabel } from '@mui/material';
import ChartComponent from '../../components/ChartComponent';

// Mock do Chart.js para evitar erros de renderização em testes
jest.mock('chart.js', () => ({
  Chart: jest.fn(),
  registerables: [],
  register: jest.fn(),
  CategoryScale: jest.fn(),
  LinearScale: jest.fn(),
  PointElement: jest.fn(),
  LineElement: jest.fn(),
  BarElement: jest.fn(),
  Title: jest.fn(),
  Tooltip: jest.fn(),
  Legend: jest.fn(),
  ArcElement: jest.fn(),
  DoughnutController: jest.fn(),
  PieController: jest.fn(),
  RadialLinearScale: jest.fn(),
}));

jest.mock('react-chartjs-2', () => ({
  Bar: () => <div data-testid="bar-chart">Bar Chart</div>,
  Line: () => <div data-testid="line-chart">Line Chart</div>,
  Pie: () => <div data-testid="pie-chart">Pie Chart</div>,
  Doughnut: () => <div data-testid="doughnut-chart">Doughnut Chart</div>,
}));

// Dados de exemplo para os gráficos
const mockChartData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Despesas',
      data: [12, 19, 3, 5, 2, 3],
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
    },
    {
      label: 'Receitas',
      data: [15, 12, 6, 8, 10, 5],
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
    },
  ],
};

describe('ChartComponent - Testes de Integração', () => {
  test('Integração com Card e Controles (Select para tipo de gráfico e período)', () => {
    // Mock das funções de callback
    const handleChartTypeChange = jest.fn();
    const handlePeriodChange = jest.fn();

    render(
      <Card>
        <CardHeader title="Análise Financeira" />
        <CardContent>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Tipo de Gráfico</InputLabel>
                <Select
                  data-testid="chart-type-select"
                  value="bar"
                  label="Tipo de Gráfico"
                  onChange={(e) => handleChartTypeChange(e.target.value)}
                >
                  <MenuItem value="bar">Barras</MenuItem>
                  <MenuItem value="line">Linha</MenuItem>
                  <MenuItem value="pie">Pizza</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Período</InputLabel>
                <Select
                  data-testid="period-select"
                  value="month"
                  label="Período"
                  onChange={(e) => handlePeriodChange(e.target.value)}
                >
                  <MenuItem value="week">Semana</MenuItem>
                  <MenuItem value="month">Mês</MenuItem>
                  <MenuItem value="year">Ano</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
          <ChartComponent
            type="bar"
            data={mockChartData}
            height={300}
          />
        </CardContent>
      </Card>
    );

    // Verificar se o componente de gráfico está sendo renderizado
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
    
    // Testar a interação com o Select de tipo de gráfico
    fireEvent.mouseDown(screen.getByTestId('chart-type-select'));
    fireEvent.click(screen.getByText('Linha'));
    expect(handleChartTypeChange).toHaveBeenCalledWith('line');
    
    // Testar a interação com o Select de período
    fireEvent.mouseDown(screen.getByTestId('period-select'));
    fireEvent.click(screen.getByText('Ano'));
    expect(handlePeriodChange).toHaveBeenCalledWith('year');
  });

  test('Integração com Filtros Dinâmicos (Input de data para filtrar)', () => {
    // Mock da função de callback para o filtro de data
    const handleFilterChange = jest.fn();

    render(
      <Box>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <FormControl fullWidth>
              <InputLabel shrink>Data Inicial</InputLabel>
              <input
                type="date"
                data-testid="start-date"
                onChange={(e) => handleFilterChange('startDate', e.target.value)}
                style={{ padding: '8px', width: '100%' }}
              />
            </FormControl>
          </Grid>
          <Grid item xs={6}>
            <FormControl fullWidth>
              <InputLabel shrink>Data Final</InputLabel>
              <input
                type="date"
                data-testid="end-date"
                onChange={(e) => handleFilterChange('endDate', e.target.value)}
                style={{ padding: '8px', width: '100%' }}
              />
            </FormControl>
          </Grid>
        </Grid>
        <ChartComponent
          type="line"
          data={mockChartData}
          height={300}
        />
      </Box>
    );

    // Verificar se o componente de gráfico está sendo renderizado
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
    
    // Testar a interação com os inputs de data
    const startDate = screen.getByTestId('start-date');
    fireEvent.change(startDate, { target: { value: '2023-01-01' } });
    expect(handleFilterChange).toHaveBeenCalledWith('startDate', '2023-01-01');
    
    const endDate = screen.getByTestId('end-date');
    fireEvent.change(endDate, { target: { value: '2023-01-31' } });
    expect(handleFilterChange).toHaveBeenCalledWith('endDate', '2023-01-31');
  });

  test('Integração com Exportação de Dados (Botões para exportar PDF e Excel)', () => {
    // Mock das funções de callback para exportação
    const handleExport = jest.fn();

    render(
      <Box>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12}>
            <Button 
              variant="contained" 
              color="primary" 
              onClick={() => handleExport('pdf')}
              data-testid="export-pdf"
            >
              Exportar como PDF
            </Button>
            <Button 
              variant="contained" 
              color="secondary" 
              onClick={() => handleExport('excel')}
              data-testid="export-excel"
              sx={{ ml: 2 }}
            >
              Exportar como Excel
            </Button>
          </Grid>
        </Grid>
        <ChartComponent
          type="bar"
          data={mockChartData}
          height={300}
        />
      </Box>
    );

    // Verificar se o componente de gráfico está sendo renderizado
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
    
    // Testar a interação com os botões de exportação
    fireEvent.click(screen.getByTestId('export-pdf'));
    expect(handleExport).toHaveBeenCalledWith('pdf');
    
    fireEvent.click(screen.getByTestId('export-excel'));
    expect(handleExport).toHaveBeenCalledWith('excel');
  });

  test('Integração com Múltiplos Datasets e Controles', () => {
    // Mock da função de callback para seleção de datasets
    const handleDatasetToggle = jest.fn();
    const mockDatasets = [
      { id: 'expenses', label: 'Despesas', checked: true },
      { id: 'income', label: 'Receitas', checked: true },
      { id: 'savings', label: 'Economias', checked: false }
    ];

    render(
      <Card>
        <CardHeader title="Análise de Dados" />
        <CardContent>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2 }}>
                {mockDatasets.map(dataset => (
                  <FormControlLabel
                    key={dataset.id}
                    control={
                      <Checkbox
                        checked={dataset.checked}
                        onChange={() => handleDatasetToggle(dataset.id)}
                        data-testid={`checkbox-${dataset.id}`}
                      />
                    }
                    label={dataset.label}
                  />
                ))}
              </Box>
            </Grid>
          </Grid>
          <ChartComponent
            type="line"
            data={mockChartData}
            height={300}
          />
        </CardContent>
      </Card>
    );

    // Verificar se o componente de gráfico está sendo renderizado
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
    
    // Testar a interação com as checkboxes
    fireEvent.click(screen.getByTestId('checkbox-expenses'));
    expect(handleDatasetToggle).toHaveBeenCalledWith('expenses');
    
    fireEvent.click(screen.getByTestId('checkbox-income'));
    expect(handleDatasetToggle).toHaveBeenCalledWith('income');
    
    fireEvent.click(screen.getByTestId('checkbox-savings'));
    expect(handleDatasetToggle).toHaveBeenCalledWith('savings');
  });

  test('Integração com Comparação de Períodos', () => {
    // Mock da função de callback para seleção de períodos
    const handlePeriodChange = jest.fn();

    render(
      <Box>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <FormControl fullWidth>
              <InputLabel>Período 1</InputLabel>
              <Select
                data-testid="period1-select"
                value="current-month"
                label="Período 1"
                onChange={(e) => handlePeriodChange('period1', e.target.value)}
              >
                <MenuItem value="current-month">Mês Atual</MenuItem>
                <MenuItem value="previous-month">Mês Anterior</MenuItem>
                <MenuItem value="year-to-date">Ano até Agora</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={6}>
            <FormControl fullWidth>
              <InputLabel>Período 2</InputLabel>
              <Select
                data-testid="period2-select"
                value="previous-month"
                label="Período 2"
                onChange={(e) => handlePeriodChange('period2', e.target.value)}
              >
                <MenuItem value="current-month">Mês Atual</MenuItem>
                <MenuItem value="previous-month">Mês Anterior</MenuItem>
                <MenuItem value="year-to-date">Ano até Agora</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        <ChartComponent
          type="bar"
          data={mockChartData}
          height={300}
        />
      </Box>
    );

    // Verificar se o componente de gráfico está sendo renderizado
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
    
    // Testar a interação com os selects de período
    fireEvent.mouseDown(screen.getByTestId('period1-select'));
    fireEvent.click(screen.getByText('Ano até Agora'));
    expect(handlePeriodChange).toHaveBeenCalledWith('period1', 'year-to-date');
    
    fireEvent.mouseDown(screen.getByTestId('period2-select'));
    fireEvent.click(screen.getByText('Mês Atual'));
    expect(handlePeriodChange).toHaveBeenCalledWith('period2', 'current-month');
  });
}); 