import React from 'react';
import { Box, Heading, Text, Flex, useColorMode } from '@chakra-ui/react';
import { Card } from '../ui';
import { Badge } from '../ui';
import { FiTrendingUp, FiTrendingDown } from 'react-icons/fi';

interface Strategy {
  id: string;
  name: string;
  symbol: string;
  type: string;
  performance: number;
  trades: number;
  winRate: number;
}

interface ActiveStrategiesProps {
  strategies: Strategy[];
  isLoading?: boolean;
}

const ActiveStrategies: React.FC<ActiveStrategiesProps> = ({
  strategies,
  isLoading = false,
}) => {
  const { colorMode } = useColorMode();
  const isDark = colorMode === 'dark';

  if (isLoading) {
    return (
      <Card>
        <Box h="300px" w="full" bg={isDark ? 'gray.700' : 'gray.100'} borderRadius="lg" />
      </Card>
    );
  }

  return (
    <Card>
      <Heading size="md" mb="4">
        Estratégias Ativas
      </Heading>
      <Box>
        {strategies.length === 0 ? (
          <Text color={isDark ? 'gray.400' : 'gray.600'}>
            Nenhuma estratégia ativa no momento
          </Text>
        ) : (
          <Flex direction="column" gap="4">
            {strategies.map((strategy) => (
              <Box
                key={strategy.id}
                p="4"
                bg={isDark ? 'gray.700' : 'gray.50'}
                borderRadius="lg"
                className="transition-colors"
                _hover={{
                  bg: isDark ? 'gray.600' : 'gray.100',
                }}
              >
                <Flex justify="space-between" align="center" mb="2">
                  <Box>
                    <Text fontWeight="medium">{strategy.name}</Text>
                    <Text fontSize="sm" color={isDark ? 'gray.400' : 'gray.600'}>
                      {strategy.symbol} • {strategy.type}
                    </Text>
                  </Box>
                  <Badge
                    variant={strategy.performance >= 0 ? 'success' : 'danger'}
                    leftIcon={
                      strategy.performance >= 0 ? (
                        <FiTrendingUp />
                      ) : (
                        <FiTrendingDown />
                      )
                    }
                  >
                    {Math.abs(strategy.performance).toFixed(2)}%
                  </Badge>
                </Flex>
                <Flex gap="4" fontSize="sm" color={isDark ? 'gray.400' : 'gray.600'}>
                  <Text>
                    {strategy.trades} operações
                  </Text>
                  <Text>
                    {strategy.winRate.toFixed(1)}% de acerto
                  </Text>
                </Flex>
              </Box>
            ))}
          </Flex>
        )}
      </Box>
    </Card>
  );
};

export default ActiveStrategies; 