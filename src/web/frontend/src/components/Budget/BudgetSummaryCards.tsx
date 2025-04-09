import React from 'react';
import {
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Box,
  Flex,
  Progress,
  Text,
  useColorModeValue
} from '@chakra-ui/react';
import { BudgetSummary } from '../../types/Budget';
import { formatCurrency } from '../../utils/formatters';

interface BudgetSummaryCardsProps {
  summary: BudgetSummary;
}

const BudgetSummaryCards: React.FC<BudgetSummaryCardsProps> = ({ summary }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const getProgressColor = (percent: number) => {
    if (percent >= 100) return 'red';
    if (percent >= 75) return 'orange';
    return 'green';
  };

  return (
    <SimpleGrid columns={{ base: 1, md: 3 }} spacing={5}>
      <Box
        p={5}
        bg={cardBg}
        borderRadius="lg"
        boxShadow="sm"
        border="1px"
        borderColor={borderColor}
      >
        <Stat>
          <StatLabel fontSize="md">Orçamento Total</StatLabel>
          <StatNumber fontSize="2xl">{formatCurrency(summary.totalBudget)}</StatNumber>
          <StatHelpText>Valor planejado para todos os orçamentos</StatHelpText>
        </Stat>
      </Box>

      <Box
        p={5}
        bg={cardBg}
        borderRadius="lg"
        boxShadow="sm"
        border="1px"
        borderColor={borderColor}
      >
        <Stat>
          <StatLabel fontSize="md">Total Gasto</StatLabel>
          <StatNumber fontSize="2xl">{formatCurrency(summary.totalSpent)}</StatNumber>
          <StatHelpText>
            {summary.percentUsed.toFixed(0)}% do orçamento utilizado
          </StatHelpText>
          <Progress
            value={summary.percentUsed > 100 ? 100 : summary.percentUsed}
            colorScheme={getProgressColor(summary.percentUsed)}
            size="sm"
            borderRadius="full"
            mt={2}
          />
        </Stat>
      </Box>

      <Box
        p={5}
        bg={cardBg}
        borderRadius="lg"
        boxShadow="sm"
        border="1px"
        borderColor={borderColor}
      >
        <Stat>
          <StatLabel fontSize="md">Restante</StatLabel>
          <StatNumber fontSize="2xl" color={summary.remaining < 0 ? 'red.500' : 'green.500'}>
            {formatCurrency(summary.remaining)}
          </StatNumber>
          <StatHelpText>
            {summary.remaining < 0
              ? 'Orçamento excedido'
              : 'Valor disponível para gastar'}
          </StatHelpText>
        </Stat>
      </Box>

      {summary.budgetsByCategory.length > 0 && (
        <Box
          p={5}
          bg={cardBg}
          borderRadius="lg"
          boxShadow="sm"
          border="1px"
          borderColor={borderColor}
          gridColumn={{ md: 'span 3' }}
          mt={2}
        >
          <Text fontSize="lg" fontWeight="medium" mb={4}>
            Orçamentos por Categoria
          </Text>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
            {summary.budgetsByCategory.map((categoryBudget) => (
              <Box key={categoryBudget.categoryId} p={3} borderRadius="md" bg="gray.50">
                <Flex justify="space-between" mb={2}>
                  <Text fontWeight="medium">{categoryBudget.categoryName}</Text>
                  <Text>
                    {formatCurrency(categoryBudget.spent)} de {formatCurrency(categoryBudget.amount)}
                  </Text>
                </Flex>
                <Progress
                  value={categoryBudget.percentUsed > 100 ? 100 : categoryBudget.percentUsed}
                  colorScheme={getProgressColor(categoryBudget.percentUsed)}
                  size="sm"
                  borderRadius="full"
                />
                <Text fontSize="sm" mt={1} textAlign="right">
                  {categoryBudget.percentUsed.toFixed(0)}% utilizado
                </Text>
              </Box>
            ))}
          </SimpleGrid>
        </Box>
      )}
    </SimpleGrid>
  );
};

export default BudgetSummaryCards; 