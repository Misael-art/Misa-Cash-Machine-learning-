import React from 'react';
import { Box, Flex, Text, Stat, StatLabel, StatNumber, StatHelpText, StatArrow, useColorMode } from '@chakra-ui/react';
import { Card } from '../ui';

interface PerformanceCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeType?: 'increase' | 'decrease';
  prefix?: string;
  suffix?: string;
  format?: 'number' | 'percentage' | 'currency';
  isLoading?: boolean;
}

const PerformanceCard: React.FC<PerformanceCardProps> = ({
  title,
  value,
  change,
  changeType,
  prefix = '',
  suffix = '',
  format = 'number',
  isLoading = false,
}) => {
  const { colorMode } = useColorMode();

  const formatValue = (val: string | number) => {
    if (typeof val === 'string') return val;
    
    switch (format) {
      case 'percentage':
        return `${val.toFixed(2)}%`;
      case 'currency':
        return new Intl.NumberFormat('pt-BR', {
          style: 'currency',
          currency: 'BRL',
        }).format(val);
      case 'number':
      default:
        return new Intl.NumberFormat('pt-BR').format(val);
    }
  };

  return (
    <Card hover={false}>
      <Stat>
        <StatLabel fontSize="sm" color={colorMode === 'light' ? 'gray.600' : 'gray.400'}>
          {title}
        </StatLabel>
        <StatNumber fontSize="2xl" fontWeight="bold" mt="1">
          {isLoading ? (
            <Box h="8" w="24" bg={colorMode === 'light' ? 'gray.200' : 'gray.700'} borderRadius="md" />
          ) : (
            <>
              {prefix}
              {formatValue(value)}
              {suffix}
            </>
          )}
        </StatNumber>
        {change !== undefined && !isLoading && (
          <StatHelpText mb="0">
            <StatArrow
              type={changeType === 'increase' ? 'increase' : 'decrease'}
              color={changeType === 'increase' ? 'green.500' : 'red.500'}
            />
            <Text as="span" ml="1" fontSize="sm">
              {Math.abs(change)}% em relação ao período anterior
            </Text>
          </StatHelpText>
        )}
      </Stat>
    </Card>
  );
};

export default PerformanceCard; 