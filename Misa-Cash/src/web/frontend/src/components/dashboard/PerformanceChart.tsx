import React from 'react';
import { Box, Heading, useColorMode } from '@chakra-ui/react';
import { Card } from '../ui';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

interface DataPoint {
  date: string;
  value: number;
  benchmark?: number;
}

interface PerformanceChartProps {
  title: string;
  data: DataPoint[];
  height?: number;
  showBenchmark?: boolean;
  isLoading?: boolean;
}

const PerformanceChart: React.FC<PerformanceChartProps> = ({
  title,
  data,
  height = 400,
  showBenchmark = true,
  isLoading = false,
}) => {
  const { colorMode } = useColorMode();
  const isDark = colorMode === 'dark';

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
    });
  };

  const formatValue = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  if (isLoading) {
    return (
      <Card>
        <Box h={height} w="full" bg={isDark ? 'gray.700' : 'gray.100'} borderRadius="lg" />
      </Card>
    );
  }

  return (
    <Card>
      <Heading size="md" mb="4">
        {title}
      </Heading>
      <Box h={height}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke={isDark ? 'gray.600' : 'gray.200'}
            />
            <XAxis
              dataKey="date"
              tickFormatter={formatDate}
              stroke={isDark ? 'gray.400' : 'gray.600'}
            />
            <YAxis
              tickFormatter={formatValue}
              stroke={isDark ? 'gray.400' : 'gray.600'}
            />
            <Tooltip
              formatter={formatValue}
              labelFormatter={formatDate}
              contentStyle={{
                backgroundColor: isDark ? 'gray.800' : 'white',
                border: 'none',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="value"
              name="Portfólio"
              stroke="#0ea5e9"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 8 }}
            />
            {showBenchmark && (
              <Line
                type="monotone"
                dataKey="benchmark"
                name="Benchmark"
                stroke={isDark ? 'gray.400' : 'gray.600'}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 8 }}
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </Box>
    </Card>
  );
};

export default PerformanceChart; 