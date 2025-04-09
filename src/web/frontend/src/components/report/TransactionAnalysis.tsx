import React from 'react';
import {
  Box,
  SimpleGrid,
  Flex,
  Text,
  Heading,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Divider,
  useColorModeValue
} from '@chakra-ui/react';
import { TransactionAnalysis as TransactionAnalysisType } from '../../types/Report';
import { formatCurrency } from '../../utils/formatters';

interface TransactionAnalysisProps {
  analysis: TransactionAnalysisType;
}

const TransactionAnalysis: React.FC<TransactionAnalysisProps> = ({ analysis }) => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  const {
    largestIncome,
    largestExpense,
    averageDailyExpense,
    averageTransactionAmount,
    transactionCount
  } = analysis;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  return (
    <Box p={5} bg={bgColor} borderRadius="lg" boxShadow="sm" border="1px" borderColor={borderColor}>
      <Heading size="md" mb={4}>Análise de Transações</Heading>
      
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={6}>
        <Box>
          <Text fontWeight="medium" mb={2}>Maior Receita</Text>
          <Box p={3} borderRadius="md" bg="green.50" borderLeft="4px solid" borderLeftColor="green.500">
            <Flex justify="space-between" mb={1}>
              <Text fontWeight="bold" color="green.700">{formatCurrency(largestIncome.amount)}</Text>
              <Text fontSize="sm" color="gray.600">{formatDate(largestIncome.date)}</Text>
            </Flex>
            <Text fontSize="sm" color="gray.700">{largestIncome.description}</Text>
            <Text fontSize="xs" color="gray.500">Categoria: {largestIncome.category}</Text>
          </Box>
        </Box>
        
        <Box>
          <Text fontWeight="medium" mb={2}>Maior Despesa</Text>
          <Box p={3} borderRadius="md" bg="red.50" borderLeft="4px solid" borderLeftColor="red.500">
            <Flex justify="space-between" mb={1}>
              <Text fontWeight="bold" color="red.700">{formatCurrency(largestExpense.amount)}</Text>
              <Text fontSize="sm" color="gray.600">{formatDate(largestExpense.date)}</Text>
            </Flex>
            <Text fontSize="sm" color="gray.700">{largestExpense.description}</Text>
            <Text fontSize="xs" color="gray.500">Categoria: {largestExpense.category}</Text>
          </Box>
        </Box>
      </SimpleGrid>
      
      <Divider my={4} />
      
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
        <Stat>
          <StatLabel>Média de Gastos Diários</StatLabel>
          <StatNumber fontSize="xl">{formatCurrency(averageDailyExpense)}</StatNumber>
          <StatHelpText>Por dia no período selecionado</StatHelpText>
        </Stat>
        
        <Stat>
          <StatLabel>Valor Médio por Transação</StatLabel>
          <StatNumber fontSize="xl">{formatCurrency(averageTransactionAmount)}</StatNumber>
          <StatHelpText>Média de todas as transações</StatHelpText>
        </Stat>
        
        <Stat>
          <StatLabel>Total de Transações</StatLabel>
          <StatNumber fontSize="xl">{transactionCount.total}</StatNumber>
          <StatHelpText>
            {transactionCount.income} receitas, {transactionCount.expense} despesas
          </StatHelpText>
        </Stat>
      </SimpleGrid>
    </Box>
  );
};

export default TransactionAnalysis; 