import React, { useState } from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  useToast,
  VStack,
} from '@chakra-ui/react';
import { BacktestConfig, BacktestResults } from '../components/backtesting';
import { useQuery } from 'react-query';
import { api } from '../services/api';
import { BacktestConfig as BacktestConfigType, BacktestResults as BacktestResultsType } from '../types';

const BacktestingPage: React.FC = () => {
  const toast = useToast();
  const [config, setConfig] = useState<BacktestConfigType | null>(null);

  // Buscar lista de estratégias
  const { data: strategies = [] } = useQuery('strategies', async () => {
    const response = await api.get('/strategies');
    return response.data;
  });

  // Executar backtesting
  const { data: results, isLoading } = useQuery<BacktestResultsType>(
    ['backtest', config],
    async () => {
      if (!config) return null;
      const response = await api.post('/backtest', config);
      return response.data;
    },
    {
      enabled: !!config,
      onError: (error) => {
        toast({
          title: 'Erro ao executar backtesting',
          description: 'Ocorreu um erro ao executar o backtesting. Tente novamente.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      },
    }
  );

  const handleSubmit = (data: BacktestConfigType) => {
    setConfig(data);
  };

  return (
    <Container maxW="container.xl" py="8">
      <VStack spacing="8" align="stretch">
        <Box>
          <Heading size="lg" mb="2">
            Backtesting
          </Heading>
          <Text color="gray.600">
            Execute simulações de estratégias de trading com dados históricos
          </Text>
        </Box>

        <BacktestConfig
          strategies={strategies}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />

        {results && (
          <BacktestResults
            results={results}
            isLoading={isLoading}
          />
        )}
      </VStack>
    </Container>
  );
};

export default BacktestingPage; 