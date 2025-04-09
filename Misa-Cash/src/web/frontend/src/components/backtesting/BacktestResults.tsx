import React from 'react';
import {
  Box,
  Heading,
  Text,
  SimpleGrid,
  Flex,
  useColorMode,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
} from '@chakra-ui/react';
import { Card } from '../ui';
import { PerformanceChart } from '../dashboard';
import { formatCurrency, formatPercentage } from '../../utils/formatters';
import { BacktestResults as BacktestResultsType } from '../../types';

interface BacktestResultsProps {
  results: BacktestResultsType;
  isLoading?: boolean;
}

const BacktestResults: React.FC<BacktestResultsProps> = ({
  results,
  isLoading = false,
}) => {
  const { colorMode } = useColorMode();
  const isDark = colorMode === 'dark';

  if (isLoading) {
    return (
      <Card>
        <Box p="6">
          <Text>Carregando resultados...</Text>
        </Box>
      </Card>
    );
  }

  return (
    <Box>
      {/* Métricas Principais */}
      <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing="6" mb="6">
        <Card>
          <Box p="4">
            <Text fontSize="sm" color="gray.500">
              Retorno Total
            </Text>
            <Heading size="md" mt="2">
              {formatPercentage(results.totalReturn)}
            </Heading>
            <Badge
              colorScheme={results.totalReturn >= 0 ? 'green' : 'red'}
              mt="2"
            >
              {results.totalReturn >= 0 ? 'Lucro' : 'Prejuízo'}
            </Badge>
          </Box>
        </Card>

        <Card>
          <Box p="4">
            <Text fontSize="sm" color="gray.500">
              Retorno Anualizado
            </Text>
            <Heading size="md" mt="2">
              {formatPercentage(results.annualizedReturn)}
            </Heading>
            <Badge
              colorScheme={results.annualizedReturn >= 0 ? 'green' : 'red'}
              mt="2"
            >
              {results.annualizedReturn >= 0 ? 'Lucro' : 'Prejuízo'}
            </Badge>
          </Box>
        </Card>

        <Card>
          <Box p="4">
            <Text fontSize="sm" color="gray.500">
              Sharpe Ratio
            </Text>
            <Heading size="md" mt="2">
              {results.sharpeRatio.toFixed(2)}
            </Heading>
            <Badge
              colorScheme={results.sharpeRatio >= 1 ? 'green' : 'yellow'}
              mt="2"
            >
              {results.sharpeRatio >= 1 ? 'Bom' : 'Regular'}
            </Badge>
          </Box>
        </Card>

        <Card>
          <Box p="4">
            <Text fontSize="sm" color="gray.500">
              Drawdown Máximo
            </Text>
            <Heading size="md" mt="2">
              {formatPercentage(results.maxDrawdown)}
            </Heading>
            <Badge colorScheme="red" mt="2">
              Risco
            </Badge>
          </Box>
        </Card>
      </SimpleGrid>

      {/* Gráfico de Equity */}
      <Card mb="6">
        <Box p="6">
          <Heading size="md" mb="4">
            Evolução do Patrimônio
          </Heading>
          <PerformanceChart
            data={results.equity}
            height={400}
            showBenchmark={false}
          />
        </Box>
      </Card>

      {/* Métricas de Trades */}
      <Card mb="6">
        <Box p="6">
          <Heading size="md" mb="4">
            Métricas de Trades
          </Heading>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing="6">
            <Box>
              <Text fontSize="sm" color="gray.500">
                Total de Trades
              </Text>
              <Text fontSize="xl" fontWeight="bold">
                {results.totalTrades}
              </Text>
            </Box>

            <Box>
              <Text fontSize="sm" color="gray.500">
                Taxa de Acerto
              </Text>
              <Text fontSize="xl" fontWeight="bold">
                {formatPercentage(results.winRate)}
              </Text>
            </Box>

            <Box>
              <Text fontSize="sm" color="gray.500">
                Fator de Lucro
              </Text>
              <Text fontSize="xl" fontWeight="bold">
                {results.profitFactor.toFixed(2)}
              </Text>
            </Box>

            <Box>
              <Text fontSize="sm" color="gray.500">
                Período Médio
              </Text>
              <Text fontSize="xl" fontWeight="bold">
                {results.averageHoldingPeriod.toFixed(1)} dias
              </Text>
            </Box>
          </SimpleGrid>
        </Box>
      </Card>

      {/* Lista de Trades */}
      <Card>
        <Box p="6">
          <Heading size="md" mb="4">
            Histórico de Trades
          </Heading>
          <Box overflowX="auto">
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Data Entrada</Th>
                  <Th>Data Saída</Th>
                  <Th>Tipo</Th>
                  <Th>Preço Entrada</Th>
                  <Th>Preço Saída</Th>
                  <Th>Quantidade</Th>
                  <Th>P&L</Th>
                  <Th>P&L %</Th>
                </Tr>
              </Thead>
              <Tbody>
                {results.trades.map((trade) => (
                  <Tr key={trade.id}>
                    <Td>{new Date(trade.entryDate).toLocaleDateString()}</Td>
                    <Td>{new Date(trade.exitDate).toLocaleDateString()}</Td>
                    <Td>
                      <Badge
                        colorScheme={trade.type === 'buy' ? 'green' : 'red'}
                      >
                        {trade.type === 'buy' ? 'Compra' : 'Venda'}
                      </Badge>
                    </Td>
                    <Td>{formatCurrency(trade.entryPrice)}</Td>
                    <Td>{formatCurrency(trade.exitPrice)}</Td>
                    <Td>{trade.quantity}</Td>
                    <Td>
                      <Text
                        color={trade.pnl >= 0 ? 'green.500' : 'red.500'}
                      >
                        {formatCurrency(trade.pnl)}
                      </Text>
                    </Td>
                    <Td>
                      <Text
                        color={trade.pnlPercentage >= 0 ? 'green.500' : 'red.500'}
                      >
                        {formatPercentage(trade.pnlPercentage)}
                      </Text>
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>
        </Box>
      </Card>
    </Box>
  );
};

export default BacktestResults; 