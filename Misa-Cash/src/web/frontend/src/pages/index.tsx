import React from 'react';
import {
  Box,
  Grid,
  Heading,
  Text,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  useColorMode,
} from '@chakra-ui/react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

// Dados de exemplo
const performanceData = [
  { date: '2024-01-01', value: 1000 },
  { date: '2024-01-02', value: 1020 },
  { date: '2024-01-03', value: 1015 },
  { date: '2024-01-04', value: 1040 },
  { date: '2024-01-05', value: 1065 },
  { date: '2024-01-06', value: 1055 },
  { date: '2024-01-07', value: 1080 },
];

const Dashboard: React.FC = () => {
  const { colorMode } = useColorMode();

  return (
    <Box>
      {/* Cabeçalho */}
      <Box mb="8">
        <Heading size="lg" mb="2">
          Dashboard
        </Heading>
        <Text color="gray.500">
          Visão geral do desempenho e métricas principais
        </Text>
      </Box>

      {/* Cards de Métricas */}
      <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing="4" mb="8">
        <Box
          p="6"
          bg={colorMode === 'light' ? 'white' : 'gray.800'}
          borderRadius="xl"
          boxShadow="base"
          className="hover:shadow-lg transition-shadow"
        >
          <Stat>
            <StatLabel>Retorno Total</StatLabel>
            <StatNumber>8.5%</StatNumber>
            <StatHelpText>
              <StatArrow type="increase" />
              2.1% desde ontem
            </StatHelpText>
          </Stat>
        </Box>

        <Box
          p="6"
          bg={colorMode === 'light' ? 'white' : 'gray.800'}
          borderRadius="xl"
          boxShadow="base"
          className="hover:shadow-lg transition-shadow"
        >
          <Stat>
            <StatLabel>Sharpe Ratio</StatLabel>
            <StatNumber>1.85</StatNumber>
            <StatHelpText>
              <StatArrow type="increase" />
              0.3 desde ontem
            </StatHelpText>
          </Stat>
        </Box>

        <Box
          p="6"
          bg={colorMode === 'light' ? 'white' : 'gray.800'}
          borderRadius="xl"
          boxShadow="base"
          className="hover:shadow-lg transition-shadow"
        >
          <Stat>
            <StatLabel>Drawdown Máximo</StatLabel>
            <StatNumber>-12.3%</StatNumber>
            <StatHelpText>
              <StatArrow type="decrease" />
              2.5% desde ontem
            </StatHelpText>
          </Stat>
        </Box>

        <Box
          p="6"
          bg={colorMode === 'light' ? 'white' : 'gray.800'}
          borderRadius="xl"
          boxShadow="base"
          className="hover:shadow-lg transition-shadow"
        >
          <Stat>
            <StatLabel>Win Rate</StatLabel>
            <StatNumber>62.5%</StatNumber>
            <StatHelpText>
              <StatArrow type="increase" />
              1.2% desde ontem
            </StatHelpText>
          </Stat>
        </Box>
      </SimpleGrid>

      {/* Gráfico de Performance */}
      <Box
        p="6"
        bg={colorMode === 'light' ? 'white' : 'gray.800'}
        borderRadius="xl"
        boxShadow="base"
        mb="8"
      >
        <Heading size="md" mb="6">
          Performance do Portfólio
        </Heading>
        <Box h="400px">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={performanceData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke={colorMode === 'light' ? '#e2e8f0' : '#2d3748'}
              />
              <XAxis
                dataKey="date"
                stroke={colorMode === 'light' ? '#4a5568' : '#a0aec0'}
              />
              <YAxis
                stroke={colorMode === 'light' ? '#4a5568' : '#a0aec0'}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: colorMode === 'light' ? 'white' : '#1a202c',
                  border: 'none',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                }}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#0ea5e9"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </Box>

      {/* Grid de Informações Adicionais */}
      <Grid templateColumns={{ base: '1fr', lg: 'repeat(2, 1fr)' }} gap="4">
        {/* Estratégias Ativas */}
        <Box
          p="6"
          bg={colorMode === 'light' ? 'white' : 'gray.800'}
          borderRadius="xl"
          boxShadow="base"
        >
          <Heading size="md" mb="4">
            Estratégias Ativas
          </Heading>
          <SimpleGrid columns={2} spacing="4">
            <Box>
              <Text color="gray.500" fontSize="sm">
                Total de Estratégias
              </Text>
              <Text fontSize="2xl" fontWeight="bold">
                8
              </Text>
            </Box>
            <Box>
              <Text color="gray.500" fontSize="sm">
                Estratégias Lucrativas
              </Text>
              <Text fontSize="2xl" fontWeight="bold" color="green.500">
                6
              </Text>
            </Box>
          </SimpleGrid>
        </Box>

        {/* Trades Recentes */}
        <Box
          p="6"
          bg={colorMode === 'light' ? 'white' : 'gray.800'}
          borderRadius="xl"
          boxShadow="base"
        >
          <Heading size="md" mb="4">
            Trades Recentes
          </Heading>
          <SimpleGrid columns={2} spacing="4">
            <Box>
              <Text color="gray.500" fontSize="sm">
                Trades Hoje
              </Text>
              <Text fontSize="2xl" fontWeight="bold">
                12
              </Text>
            </Box>
            <Box>
              <Text color="gray.500" fontSize="sm">
                Win Rate Hoje
              </Text>
              <Text fontSize="2xl" fontWeight="bold" color="green.500">
                75%
              </Text>
            </Box>
          </SimpleGrid>
        </Box>
      </Grid>
    </Box>
  );
};

export default Dashboard; 