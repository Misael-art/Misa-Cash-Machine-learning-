import React from 'react';
import {
  Box,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Divider,
  Text,
  Flex,
  Badge,
  useColorModeValue
} from '@chakra-ui/react';
import { ReportSummary as ReportSummaryType } from '../../types/Report';
import { formatCurrency } from '../../utils/formatters';

interface ReportSummaryProps {
  summary: ReportSummaryType;
}

const ReportSummary: React.FC<ReportSummaryProps> = ({ summary }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  const {
    totalIncome,
    totalExpense,
    netBalance,
    topExpenseCategories,
    topIncomeCategories,
    periodComparison
  } = summary;

  const getChangeType = (value: number) => {
    if (value > 0) return 'increase';
    if (value < 0) return 'decrease';
    return undefined;
  };

  const getChangeColor = (value: number, isPositiveGood = true) => {
    if (value === 0) return undefined;
    
    if (isPositiveGood) {
      return value > 0 ? 'green.500' : 'red.500';
    } else {
      return value > 0 ? 'red.500' : 'green.500';
    }
  };

  return (
    <Box>
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={5} mb={6}>
        <Box p={5} bg={cardBg} borderRadius="lg" boxShadow="sm" border="1px" borderColor={borderColor}>
          <Stat>
            <StatLabel fontSize="md">Receitas Totais</StatLabel>
            <StatNumber fontSize="2xl" color="green.500">{formatCurrency(totalIncome)}</StatNumber>
            <StatHelpText>
              <StatArrow type={getChangeType(periodComparison.percentageChange.income)} />
              {Math.abs(periodComparison.percentageChange.income).toFixed(1)}% do período anterior
            </StatHelpText>
          </Stat>
        </Box>
        
        <Box p={5} bg={cardBg} borderRadius="lg" boxShadow="sm" border="1px" borderColor={borderColor}>
          <Stat>
            <StatLabel fontSize="md">Despesas Totais</StatLabel>
            <StatNumber fontSize="2xl" color="red.500">{formatCurrency(totalExpense)}</StatNumber>
            <StatHelpText>
              <StatArrow 
                type={getChangeType(-periodComparison.percentageChange.expense)} 
              />
              {Math.abs(periodComparison.percentageChange.expense).toFixed(1)}% do período anterior
            </StatHelpText>
          </Stat>
        </Box>
        
        <Box p={5} bg={cardBg} borderRadius="lg" boxShadow="sm" border="1px" borderColor={borderColor}>
          <Stat>
            <StatLabel fontSize="md">Saldo Líquido</StatLabel>
            <StatNumber 
              fontSize="2xl"
              color={netBalance >= 0 ? 'green.500' : 'red.500'}
            >
              {formatCurrency(netBalance)}
            </StatNumber>
            <StatHelpText>
              <StatArrow type={getChangeType(periodComparison.percentageChange.balance)} />
              {Math.abs(periodComparison.percentageChange.balance).toFixed(1)}% do período anterior
            </StatHelpText>
          </Stat>
        </Box>
      </SimpleGrid>

      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
        <Box p={5} bg={cardBg} borderRadius="lg" boxShadow="sm" border="1px" borderColor={borderColor}>
          <Text fontSize="lg" fontWeight="medium" mb={3}>
            Principais Categorias de Despesas
          </Text>
          <Divider mb={3} />
          
          {topExpenseCategories.length > 0 ? (
            <Box>
              {topExpenseCategories.map((category, index) => (
                <Flex 
                  key={category.categoryId} 
                  justify="space-between" 
                  align="center" 
                  mb={2}
                  p={2}
                  bg={index % 2 === 0 ? 'gray.50' : 'transparent'}
                  borderRadius="md"
                >
                  <Flex align="center">
                    <Text>{category.categoryName}</Text>
                    <Badge ml={2} colorScheme="red" variant="outline">
                      {category.percentage.toFixed(1)}%
                    </Badge>
                  </Flex>
                  <Text fontWeight="medium" color="red.500">
                    {formatCurrency(category.amount)}
                  </Text>
                </Flex>
              ))}
            </Box>
          ) : (
            <Text color="gray.500">Nenhuma despesa registrada neste período.</Text>
          )}
        </Box>
        
        <Box p={5} bg={cardBg} borderRadius="lg" boxShadow="sm" border="1px" borderColor={borderColor}>
          <Text fontSize="lg" fontWeight="medium" mb={3}>
            Principais Fontes de Receita
          </Text>
          <Divider mb={3} />
          
          {topIncomeCategories.length > 0 ? (
            <Box>
              {topIncomeCategories.map((category, index) => (
                <Flex 
                  key={category.categoryId} 
                  justify="space-between" 
                  align="center" 
                  mb={2}
                  p={2}
                  bg={index % 2 === 0 ? 'gray.50' : 'transparent'}
                  borderRadius="md"
                >
                  <Flex align="center">
                    <Text>{category.categoryName}</Text>
                    <Badge ml={2} colorScheme="green" variant="outline">
                      {category.percentage.toFixed(1)}%
                    </Badge>
                  </Flex>
                  <Text fontWeight="medium" color="green.500">
                    {formatCurrency(category.amount)}
                  </Text>
                </Flex>
              ))}
            </Box>
          ) : (
            <Text color="gray.500">Nenhuma receita registrada neste período.</Text>
          )}
        </Box>
      </SimpleGrid>
    </Box>
  );
};

export default ReportSummary; 