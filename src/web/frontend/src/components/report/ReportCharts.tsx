import React from 'react';
import {
  Box,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Heading,
  Text,
  useColorModeValue
} from '@chakra-ui/react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { TimeSeriesData, CategoryDistribution } from '../../types/Report';
import { formatCurrency } from '../../utils/formatters';

interface ReportChartsProps {
  timeSeriesData: TimeSeriesData[];
  categoryDistribution: {
    income: CategoryDistribution[];
    expense: CategoryDistribution[];
  };
}

const COLORS = [
  '#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8',
  '#82CA9D', '#FF6B6B', '#6A7FDB', '#D291BC', '#54DEFD'
];

const ReportCharts: React.FC<ReportChartsProps> = ({
  timeSeriesData,
  categoryDistribution
}) => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const chartFontColor = useColorModeValue('#333', '#EEE');

  const formatYAxis = (value: number) => {
    if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}k`;
    }
    return value;
  };

  const lineChartTooltipFormatter = (value: number) => [formatCurrency(value), ''];

  const pieTooltipFormatter = (value: number, name: string, props: any) => {
    return [`${formatCurrency(value)} (${props.payload.percentage.toFixed(1)}%)`, name];
  };

  return (
    <Box p={5} bg={bgColor} borderRadius="lg" boxShadow="sm" border="1px" borderColor={borderColor}>
      <Tabs isFitted variant="enclosed" colorScheme="teal">
        <TabList mb={4}>
          <Tab>Fluxo de Caixa</Tab>
          <Tab>Distribuição de Despesas</Tab>
          <Tab>Distribuição de Receitas</Tab>
        </TabList>
        
        <TabPanels>
          {/* Gráfico de Fluxo de Caixa */}
          <TabPanel>
            <Heading size="md" mb={4}>Evolução Financeira</Heading>
            <Box height="400px">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={timeSeriesData}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="label" 
                    tick={{ fill: chartFontColor }}
                  />
                  <YAxis 
                    tickFormatter={formatYAxis}
                    tick={{ fill: chartFontColor }}
                  />
                  <Tooltip formatter={lineChartTooltipFormatter} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="income"
                    name="Receitas"
                    stroke="#38A169"
                    activeDot={{ r: 8 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="expense"
                    name="Despesas"
                    stroke="#E53E3E"
                    activeDot={{ r: 8 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="balance"
                    name="Saldo"
                    stroke="#3182CE"
                    activeDot={{ r: 8 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </TabPanel>
          
          {/* Gráfico de Distribuição de Despesas */}
          <TabPanel>
            <Heading size="md" mb={4}>Distribuição de Despesas por Categoria</Heading>
            {categoryDistribution.expense.length > 0 ? (
              <Box height="400px">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={categoryDistribution.expense}
                      cx="50%"
                      cy="50%"
                      labelLine={true}
                      outerRadius={150}
                      fill="#8884d8"
                      dataKey="amount"
                      nameKey="categoryName"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                    >
                      {categoryDistribution.expense.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={pieTooltipFormatter} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            ) : (
              <Text color="gray.500">Sem dados para exibir no período selecionado.</Text>
            )}
          </TabPanel>
          
          {/* Gráfico de Distribuição de Receitas */}
          <TabPanel>
            <Heading size="md" mb={4}>Distribuição de Receitas por Categoria</Heading>
            {categoryDistribution.income.length > 0 ? (
              <Box height="400px">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={categoryDistribution.income}
                      cx="50%"
                      cy="50%"
                      labelLine={true}
                      outerRadius={150}
                      fill="#8884d8"
                      dataKey="amount"
                      nameKey="categoryName"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                    >
                      {categoryDistribution.income.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={pieTooltipFormatter} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            ) : (
              <Text color="gray.500">Sem dados para exibir no período selecionado.</Text>
            )}
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default ReportCharts; 