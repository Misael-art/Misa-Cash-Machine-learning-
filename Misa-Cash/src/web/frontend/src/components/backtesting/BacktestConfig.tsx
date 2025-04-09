import React from 'react';
import {
  Box,
  Heading,
  Text,
  Flex,
  useColorMode,
  FormControl,
  FormLabel,
  FormErrorMessage,
  Input,
  Select,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Button,
} from '@chakra-ui/react';
import { Card } from '../ui';
import { useForm, Controller } from 'react-hook-form';

interface BacktestConfigData {
  strategy: string;
  symbol: string;
  timeframe: string;
  startDate: string;
  endDate: string;
  initialCapital: number;
  commission: number;
  slippage: number;
  positionSize: number;
  riskManagement: {
    stopLoss: number;
    takeProfit: number;
    maxDrawdown: number;
  };
}

interface BacktestConfigProps {
  strategies: { id: string; name: string }[];
  onSubmit: (data: BacktestConfigData) => void;
  isLoading?: boolean;
}

const BacktestConfig: React.FC<BacktestConfigProps> = ({
  strategies,
  onSubmit,
  isLoading = false,
}) => {
  const { colorMode } = useColorMode();
  const isDark = colorMode === 'dark';

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<BacktestConfigData>({
    defaultValues: {
      strategy: '',
      symbol: '',
      timeframe: '1d',
      startDate: '',
      endDate: '',
      initialCapital: 100000,
      commission: 0.1,
      slippage: 0.1,
      positionSize: 1,
      riskManagement: {
        stopLoss: 2,
        takeProfit: 4,
        maxDrawdown: 10,
      },
    },
  });

  return (
    <Card>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Heading size="md" mb="6">
          Configuração do Backtesting
        </Heading>

        <Flex direction="column" gap="6">
          {/* Estratégia e Ativo */}
          <Box>
            <Text fontWeight="medium" mb="4">
              Estratégia e Ativo
            </Text>
            <Flex direction="column" gap="4">
              <FormControl isInvalid={!!errors.strategy}>
                <FormLabel>Estratégia</FormLabel>
                <Select
                  {...register('strategy', { required: 'Estratégia é obrigatória' })}
                >
                  <option value="">Selecione uma estratégia</option>
                  {strategies.map((strategy) => (
                    <option key={strategy.id} value={strategy.id}>
                      {strategy.name}
                    </option>
                  ))}
                </Select>
                <FormErrorMessage>
                  {errors.strategy?.message}
                </FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.symbol}>
                <FormLabel>Ativo</FormLabel>
                <Input
                  {...register('symbol', { required: 'Ativo é obrigatório' })}
                  placeholder="Símbolo do ativo"
                />
                <FormErrorMessage>
                  {errors.symbol?.message}
                </FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.timeframe}>
                <FormLabel>Timeframe</FormLabel>
                <Select
                  {...register('timeframe', { required: 'Timeframe é obrigatório' })}
                >
                  <option value="1m">1 minuto</option>
                  <option value="5m">5 minutos</option>
                  <option value="15m">15 minutos</option>
                  <option value="30m">30 minutos</option>
                  <option value="1h">1 hora</option>
                  <option value="4h">4 horas</option>
                  <option value="1d">1 dia</option>
                </Select>
                <FormErrorMessage>
                  {errors.timeframe?.message}
                </FormErrorMessage>
              </FormControl>
            </Flex>
          </Box>

          {/* Período */}
          <Box>
            <Text fontWeight="medium" mb="4">
              Período
            </Text>
            <Flex direction="column" gap="4">
              <FormControl isInvalid={!!errors.startDate}>
                <FormLabel>Data Inicial</FormLabel>
                <Input
                  type="date"
                  {...register('startDate', { required: 'Data inicial é obrigatória' })}
                />
                <FormErrorMessage>
                  {errors.startDate?.message}
                </FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!errors.endDate}>
                <FormLabel>Data Final</FormLabel>
                <Input
                  type="date"
                  {...register('endDate', { required: 'Data final é obrigatória' })}
                />
                <FormErrorMessage>
                  {errors.endDate?.message}
                </FormErrorMessage>
              </FormControl>
            </Flex>
          </Box>

          {/* Capital e Custos */}
          <Box>
            <Text fontWeight="medium" mb="4">
              Capital e Custos
            </Text>
            <Flex direction="column" gap="4">
              <FormControl>
                <FormLabel>Capital Inicial (R$)</FormLabel>
                <Controller
                  name="initialCapital"
                  control={control}
                  render={({ field }) => (
                    <NumberInput min={1000} step={1000} {...field}>
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  )}
                />
              </FormControl>

              <FormControl>
                <FormLabel>Comissão (%)</FormLabel>
                <Controller
                  name="commission"
                  control={control}
                  render={({ field }) => (
                    <NumberInput min={0} max={1} step={0.01} {...field}>
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  )}
                />
              </FormControl>

              <FormControl>
                <FormLabel>Slippage (%)</FormLabel>
                <Controller
                  name="slippage"
                  control={control}
                  render={({ field }) => (
                    <NumberInput min={0} max={1} step={0.01} {...field}>
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  )}
                />
              </FormControl>

              <FormControl>
                <FormLabel>Tamanho da Posição (%)</FormLabel>
                <Controller
                  name="positionSize"
                  control={control}
                  render={({ field }) => (
                    <NumberInput min={0.1} max={100} step={0.1} {...field}>
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  )}
                />
              </FormControl>
            </Flex>
          </Box>

          {/* Gerenciamento de Risco */}
          <Box>
            <Text fontWeight="medium" mb="4">
              Gerenciamento de Risco
            </Text>
            <Flex direction="column" gap="4">
              <FormControl>
                <FormLabel>Stop Loss (%)</FormLabel>
                <Controller
                  name="riskManagement.stopLoss"
                  control={control}
                  render={({ field }) => (
                    <NumberInput min={0.1} max={10} step={0.1} {...field}>
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  )}
                />
              </FormControl>

              <FormControl>
                <FormLabel>Take Profit (%)</FormLabel>
                <Controller
                  name="riskManagement.takeProfit"
                  control={control}
                  render={({ field }) => (
                    <NumberInput min={0.1} max={20} step={0.1} {...field}>
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  )}
                />
              </FormControl>

              <FormControl>
                <FormLabel>Drawdown Máximo (%)</FormLabel>
                <Controller
                  name="riskManagement.maxDrawdown"
                  control={control}
                  render={({ field }) => (
                    <NumberInput min={1} max={50} {...field}>
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  )}
                />
              </FormControl>
            </Flex>
          </Box>

          {/* Botões */}
          <Flex justify="flex-end">
            <Button
              type="submit"
              variant="primary"
              isLoading={isLoading}
            >
              Executar Backtesting
            </Button>
          </Flex>
        </Flex>
      </form>
    </Card>
  );
};

export default BacktestConfig; 