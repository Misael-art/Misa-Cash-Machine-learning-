import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Divider,
  FormControl,
  FormControlLabel,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Stack,
  Switch,
  TextField,
  Typography,
  useTheme,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import ptBR from 'date-fns/locale/pt-BR';
import { format, subDays, subMonths } from 'date-fns';
import { useAuth } from '../../contexts/AuthContext';
import { useToast } from '../../contexts/ToastContext';
import { api } from '../../services/api';
import Loading from '../../components/Loading';
import ErrorMessage from '../../components/ErrorMessage';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import PrintIcon from '@mui/icons-material/Print';
import DateRangeIcon from '@mui/icons-material/DateRange';
import FilterListIcon from '@mui/icons-material/FilterList';
import { BarChartOutlined as ChartIcon } from '@mui/icons-material';
import { useCategories } from '../../contexts/CategoryContext';
import ChartComponent from '../../components/ChartComponent';
import { formatCurrency } from '../../utils/formatters';

type Period = 'last7days' | 'last30days' | 'last90days' | 'lastYear' | 'custom';
type ReportCategory = { id: number; name: string; income: number; expenses: number; transactions: number };

interface ReportSummary {
  period: {
    start_date: string;
    end_date: string;
    days: number;
  };
  income: {
    current: number;
    previous: number;
    change_percentage: number;
  };
  expenses: {
    current: number;
    previous: number;
    change_percentage: number;
  };
  balance: {
    current: number;
    previous: number;
    change_percentage: number;
  };
  transaction_count: number;
}

interface ReportData {
  summary: ReportSummary;
  categories: {
    top_expenses: ReportCategory[];
    top_income: ReportCategory[];
    all: ReportCategory[];
  };
  time_series: { date: string; income: number; expenses: number; balance: number }[];
  analysis: {
    avg_daily_expense: number;
    avg_transaction_value: number;
    most_expensive_day: string | null;
    highest_income_day: string | null;
  };
}

const Reports: React.FC = () => {
  const theme = useTheme();
  const { isAuthenticated } = useAuth();
  const { showToast } = useToast();
  const { categories } = useCategories();
  
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [reportData, setReportData] = useState<ReportData | null>(null);
  
  // Filtros
  const [period, setPeriod] = useState<Period>('last30days');
  const [startDate, setStartDate] = useState<Date | null>(subDays(new Date(), 30));
  const [endDate, setEndDate] = useState<Date | null>(new Date());
  const [includeIncome, setIncludeIncome] = useState<boolean>(true);
  const [includeExpenses, setIncludeExpenses] = useState<boolean>(true);
  const [selectedCategories, setSelectedCategories] = useState<number[]>([]);
  const [showFilters, setShowFilters] = useState<boolean>(false);
  
  // Gerar relatório
  const generateReport = async () => {
    if (!isAuthenticated) {
      showToast('Você precisa estar autenticado para gerar relatórios', 'error');
      return;
    }
    
    if (!startDate || !endDate) {
      showToast('Selecione datas válidas', 'error');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.post('/api/reports/generate', {
        start_date: format(startDate, 'yyyy-MM-dd'),
        end_date: format(endDate, 'yyyy-MM-dd'),
        include_income: includeIncome,
        include_expenses: includeExpenses,
        category_ids: selectedCategories.length > 0 ? selectedCategories : undefined
      });
      
      setReportData(response.data);
    } catch (err: any) {
      console.error('Erro ao gerar relatório:', err);
      setError(err.response?.data?.error || 'Não foi possível gerar o relatório');
      showToast('Erro ao gerar relatório', 'error');
    } finally {
      setLoading(false);
    }
  };
  
  // Exportar relatório
  const exportReport = async (format: 'pdf' | 'excel') => {
    if (!isAuthenticated) {
      showToast('Você precisa estar autenticado para exportar relatórios', 'error');
      return;
    }
    
    if (!startDate || !endDate) {
      showToast('Selecione datas válidas', 'error');
      return;
    }
    
    try {
      const response = await api.post(
        `/api/reports/export/${format}`,
        {
          start_date: format === 'pdf' ? format(startDate, 'yyyy-MM-dd') : startDate.toISOString().split('T')[0],
          end_date: format === 'pdf' ? format(endDate, 'yyyy-MM-dd') : endDate.toISOString().split('T')[0],
          include_income: includeIncome,
          include_expenses: includeExpenses,
          category_ids: selectedCategories.length > 0 ? selectedCategories : undefined
        },
        { responseType: 'blob' }
      );
      
      // Criar URL do blob e iniciar download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `relatorio_financeiro_${format(startDate, 'yyyy-MM-dd')}_a_${format(endDate, 'yyyy-MM-dd')}.${format === 'pdf' ? 'pdf' : 'xlsx'}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      showToast(`Relatório exportado com sucesso em formato ${format.toUpperCase()}`, 'success');
    } catch (err) {
      console.error(`Erro ao exportar relatório como ${format}:`, err);
      showToast(`Erro ao exportar relatório como ${format.toUpperCase()}`, 'error');
    }
  };
  
  // Alterar período
  const handlePeriodChange = (newPeriod: Period) => {
    setPeriod(newPeriod);
    const today = new Date();
    
    switch (newPeriod) {
      case 'last7days':
        setStartDate(subDays(today, 7));
        setEndDate(today);
        break;
      case 'last30days':
        setStartDate(subDays(today, 30));
        setEndDate(today);
        break;
      case 'last90days':
        setStartDate(subDays(today, 90));
        setEndDate(today);
        break;
      case 'lastYear':
        setStartDate(subMonths(today, 12));
        setEndDate(today);
        break;
      case 'custom':
        // Mantém as datas atuais
        break;
    }
  };
  
  // Preparar dados para o gráfico de barras
  const prepareBarChartData = () => {
    if (!reportData?.categories?.top_expenses) return null;
    
    return {
      labels: reportData.categories.top_expenses.map(cat => cat.name),
      datasets: [
        {
          label: 'Despesas',
          data: reportData.categories.top_expenses.map(cat => cat.expenses),
          backgroundColor: theme.palette.error.main,
        },
      ],
    };
  };
  
  // Preparar dados para o gráfico de linha
  const prepareLineChartData = () => {
    if (!reportData?.time_series) return null;
    
    return {
      labels: reportData.time_series.map(item => item.date),
      datasets: [
        {
          label: 'Receitas',
          data: reportData.time_series.map(item => item.income),
          borderColor: theme.palette.success.main,
          backgroundColor: 'transparent',
          tension: 0.4,
        },
        {
          label: 'Despesas',
          data: reportData.time_series.map(item => item.expenses),
          borderColor: theme.palette.error.main,
          backgroundColor: 'transparent',
          tension: 0.4,
        },
        {
          label: 'Saldo',
          data: reportData.time_series.map(item => item.balance),
          borderColor: theme.palette.primary.main,
          backgroundColor: 'transparent',
          tension: 0.4,
        },
      ],
    };
  };
  
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Relatórios Financeiros
        </Typography>
        
        <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
          <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
            <Typography variant="h6" component="h2">
              <DateRangeIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              Período
            </Typography>
            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel id="period-select-label">Período</InputLabel>
              <Select
                labelId="period-select-label"
                value={period}
                label="Período"
                onChange={(e) => handlePeriodChange(e.target.value as Period)}
              >
                <MenuItem value="last7days">Últimos 7 dias</MenuItem>
                <MenuItem value="last30days">Últimos 30 dias</MenuItem>
                <MenuItem value="last90days">Últimos 90 dias</MenuItem>
                <MenuItem value="lastYear">Último ano</MenuItem>
                <MenuItem value="custom">Personalizado</MenuItem>
              </Select>
            </FormControl>
            
            {period === 'custom' && (
              <>
                <DatePicker 
                  label="Data inicial"
                  value={startDate}
                  onChange={(newValue) => setStartDate(newValue)}
                />
                <DatePicker 
                  label="Data final"
                  value={endDate}
                  onChange={(newValue) => setEndDate(newValue)}
                  minDate={startDate || undefined}
                />
              </>
            )}
            
            <IconButton 
              color="primary" 
              onClick={() => setShowFilters(!showFilters)}
              aria-label="Mostrar filtros"
            >
              <FilterListIcon />
            </IconButton>
            
            <Button 
              variant="contained" 
              onClick={generateReport}
              startIcon={<ChartIcon />}
            >
              Gerar Relatório
            </Button>
          </Stack>
          
          {showFilters && (
            <Box sx={{ mb: 2, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
              <Typography variant="subtitle1" gutterBottom>
                Filtros Adicionais
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Stack direction="row" spacing={2}>
                    <FormControlLabel
                      control={
                        <Switch 
                          checked={includeIncome} 
                          onChange={(e) => setIncludeIncome(e.target.checked)} 
                        />
                      }
                      label="Incluir receitas"
                    />
                    <FormControlLabel
                      control={
                        <Switch 
                          checked={includeExpenses} 
                          onChange={(e) => setIncludeExpenses(e.target.checked)} 
                        />
                      }
                      label="Incluir despesas"
                    />
                  </Stack>
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth>
                    <InputLabel id="categories-select-label">Categorias</InputLabel>
                    <Select
                      labelId="categories-select-label"
                      multiple
                      value={selectedCategories}
                      onChange={(e) => setSelectedCategories(e.target.value as number[])}
                      label="Categorias"
                      renderValue={(selected) => {
                        if (selected.length === 0) {
                          return 'Todas as categorias';
                        }
                        return selected.map(id => 
                          categories?.find(cat => cat.id === id)?.name || ''
                        ).join(', ');
                      }}
                    >
                      {categories?.map((category) => (
                        <MenuItem key={category.id} value={category.id}>
                          {category.name}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
            </Box>
          )}
          
          <Stack direction="row" spacing={1} justifyContent="flex-end">
            <Button 
              startIcon={<PictureAsPdfIcon />}
              onClick={() => exportReport('pdf')}
              disabled={!reportData}
            >
              Exportar PDF
            </Button>
            <Button 
              startIcon={<FileDownloadIcon />}
              onClick={() => exportReport('excel')}
              disabled={!reportData}
            >
              Exportar Excel
            </Button>
            <Button 
              startIcon={<PrintIcon />}
              onClick={() => window.print()}
              disabled={!reportData}
            >
              Imprimir
            </Button>
          </Stack>
        </Paper>
        
        {loading && <Loading />}
        {error && <ErrorMessage message={error} />}
        
        {reportData && (
          <div className="report-content">
            <Grid container spacing={3}>
              {/* Cards de Resumo */}
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" color="success.main" gutterBottom>
                      Receitas
                    </Typography>
                    <Typography variant="h4">
                      {formatCurrency(reportData.summary.income.current)}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      color={reportData.summary.income.change_percentage >= 0 ? 'success.main' : 'error.main'}
                    >
                      {reportData.summary.income.change_percentage >= 0 ? '▲' : '▼'} 
                      {Math.abs(reportData.summary.income.change_percentage)}% em relação ao período anterior
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" color="error.main" gutterBottom>
                      Despesas
                    </Typography>
                    <Typography variant="h4">
                      {formatCurrency(reportData.summary.expenses.current)}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      color={reportData.summary.expenses.change_percentage <= 0 ? 'success.main' : 'error.main'}
                    >
                      {reportData.summary.expenses.change_percentage >= 0 ? '▲' : '▼'} 
                      {Math.abs(reportData.summary.expenses.change_percentage)}% em relação ao período anterior
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" color="primary.main" gutterBottom>
                      Saldo
                    </Typography>
                    <Typography variant="h4">
                      {formatCurrency(reportData.summary.balance.current)}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      color={reportData.summary.balance.change_percentage >= 0 ? 'success.main' : 'error.main'}
                    >
                      {reportData.summary.balance.change_percentage >= 0 ? '▲' : '▼'} 
                      {Math.abs(reportData.summary.balance.change_percentage)}% em relação ao período anterior
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              {/* Gráficos */}
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2, height: '100%' }}>
                  <Typography variant="h6" gutterBottom>
                    Despesas por Categoria
                  </Typography>
                  {prepareBarChartData() && (
                    <Box sx={{ height: 300, mt: 2 }}>
                      <ChartComponent
                        type="bar"
                        data={prepareBarChartData()!}
                      />
                    </Box>
                  )}
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2, height: '100%' }}>
                  <Typography variant="h6" gutterBottom>
                    Transações por Data
                  </Typography>
                  {prepareLineChartData() && (
                    <Box sx={{ height: 300, mt: 2 }}>
                      <ChartComponent
                        type="line"
                        data={prepareLineChartData()!}
                      />
                    </Box>
                  )}
                </Paper>
              </Grid>
              
              {/* Análise */}
              <Grid item xs={12}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Análise de Transações
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6} md={3}>
                      <Card variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          Despesa média diária
                        </Typography>
                        <Typography variant="h6">
                          {formatCurrency(reportData.analysis.avg_daily_expense)}
                        </Typography>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Card variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          Valor médio por transação
                        </Typography>
                        <Typography variant="h6">
                          {formatCurrency(reportData.analysis.avg_transaction_value)}
                        </Typography>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Card variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          Dia com maior despesa
                        </Typography>
                        <Typography variant="h6">
                          {reportData.analysis.most_expensive_day 
                            ? format(new Date(reportData.analysis.most_expensive_day), 'dd/MM/yyyy')
                            : 'N/A'
                          }
                        </Typography>
                      </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Card variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          Dia com maior receita
                        </Typography>
                        <Typography variant="h6">
                          {reportData.analysis.highest_income_day 
                            ? format(new Date(reportData.analysis.highest_income_day), 'dd/MM/yyyy')
                            : 'N/A'
                          }
                        </Typography>
                      </Card>
                    </Grid>
                  </Grid>
                </Paper>
              </Grid>
              
              {/* Categorias Top */}
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Top 5 Categorias de Despesa
                  </Typography>
                  {reportData.categories.top_expenses.length > 0 ? (
                    <Stack spacing={1} divider={<Divider />}>
                      {reportData.categories.top_expenses.map((category) => (
                        <Stack 
                          key={category.id} 
                          direction="row" 
                          justifyContent="space-between" 
                          alignItems="center"
                          spacing={2}
                        >
                          <Typography>{category.name}</Typography>
                          <Box>
                            <Typography color="error.main" fontWeight="bold">
                              {formatCurrency(category.expenses)}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {category.transactions} transações
                            </Typography>
                          </Box>
                        </Stack>
                      ))}
                    </Stack>
                  ) : (
                    <Typography color="text.secondary">
                      Nenhuma despesa no período
                    </Typography>
                  )}
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Top 5 Categorias de Receita
                  </Typography>
                  {reportData.categories.top_income.length > 0 ? (
                    <Stack spacing={1} divider={<Divider />}>
                      {reportData.categories.top_income.map((category) => (
                        <Stack 
                          key={category.id} 
                          direction="row" 
                          justifyContent="space-between" 
                          alignItems="center"
                          spacing={2}
                        >
                          <Typography>{category.name}</Typography>
                          <Box>
                            <Typography color="success.main" fontWeight="bold">
                              {formatCurrency(category.income)}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {category.transactions} transações
                            </Typography>
                          </Box>
                        </Stack>
                      ))}
                    </Stack>
                  ) : (
                    <Typography color="text.secondary">
                      Nenhuma receita no período
                    </Typography>
                  )}
                </Paper>
              </Grid>
            </Grid>
          </div>
        )}
      </Container>
    </LocalizationProvider>
  );
};

export default Reports; 