import React from 'react';
import {
  Box,
  Heading,
  Text,
  Flex,
  useColorMode,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  IconButton,
} from '@chakra-ui/react';
import { Card } from '../ui';
import { Badge } from '../ui';
import { Button } from '../ui';
import {
  FiMoreVertical,
  FiPlay,
  FiPause,
  FiEdit,
  FiTrash2,
  FiBarChart2,
} from 'react-icons/fi';

interface Strategy {
  id: string;
  name: string;
  description: string;
  type: string;
  status: 'active' | 'paused' | 'stopped';
  performance: number;
  trades: number;
  winRate: number;
  lastUpdate: string;
}

interface StrategyListProps {
  strategies: Strategy[];
  onEdit?: (strategy: Strategy) => void;
  onDelete?: (strategy: Strategy) => void;
  onToggleStatus?: (strategy: Strategy) => void;
  onViewPerformance?: (strategy: Strategy) => void;
  isLoading?: boolean;
}

const StrategyList: React.FC<StrategyListProps> = ({
  strategies,
  onEdit,
  onDelete,
  onToggleStatus,
  onViewPerformance,
  isLoading = false,
}) => {
  const { colorMode } = useColorMode();
  const isDark = colorMode === 'dark';

  const getStatusBadge = (status: Strategy['status']) => {
    switch (status) {
      case 'active':
        return <Badge variant="success">Ativa</Badge>;
      case 'paused':
        return <Badge variant="warning">Pausada</Badge>;
      case 'stopped':
        return <Badge variant="danger">Parada</Badge>;
      default:
        return null;
    }
  };

  if (isLoading) {
    return (
      <Card>
        <Box h="400px" w="full" bg={isDark ? 'gray.700' : 'gray.100'} borderRadius="lg" />
      </Card>
    );
  }

  return (
    <Card>
      <Flex justify="space-between" align="center" mb="6">
        <Heading size="md">Estratégias</Heading>
        <Button
          variant="primary"
          leftIcon={<FiPlay />}
          onClick={() => {/* TODO: Implementar criação de estratégia */}}
        >
          Nova Estratégia
        </Button>
      </Flex>
      <Box>
        {strategies.length === 0 ? (
          <Text color={isDark ? 'gray.400' : 'gray.600'}>
            Nenhuma estratégia encontrada
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
                      {strategy.type}
                    </Text>
                  </Box>
                  <Flex align="center" gap="2">
                    {getStatusBadge(strategy.status)}
                    <Menu>
                      <MenuButton
                        as={IconButton}
                        icon={<FiMoreVertical />}
                        variant="ghost"
                        size="sm"
                      />
                      <MenuList>
                        <MenuItem
                          icon={strategy.status === 'active' ? <FiPause /> : <FiPlay />}
                          onClick={() => onToggleStatus?.(strategy)}
                        >
                          {strategy.status === 'active' ? 'Pausar' : 'Ativar'}
                        </MenuItem>
                        <MenuItem
                          icon={<FiBarChart2 />}
                          onClick={() => onViewPerformance?.(strategy)}
                        >
                          Ver Desempenho
                        </MenuItem>
                        <MenuItem
                          icon={<FiEdit />}
                          onClick={() => onEdit?.(strategy)}
                        >
                          Editar
                        </MenuItem>
                        <MenuItem
                          icon={<FiTrash2 />}
                          color="red.500"
                          onClick={() => onDelete?.(strategy)}
                        >
                          Excluir
                        </MenuItem>
                      </MenuList>
                    </Menu>
                  </Flex>
                </Flex>
                <Text fontSize="sm" mb="2" color={isDark ? 'gray.400' : 'gray.600'}>
                  {strategy.description}
                </Text>
                <Flex gap="4" fontSize="sm" color={isDark ? 'gray.400' : 'gray.600'}>
                  <Text>
                    {strategy.trades} operações
                  </Text>
                  <Text>
                    {strategy.winRate.toFixed(1)}% de acerto
                  </Text>
                  <Text>
                    {strategy.performance >= 0 ? '+' : ''}
                    {strategy.performance.toFixed(2)}% de retorno
                  </Text>
                  <Text>
                    Última atualização: {new Date(strategy.lastUpdate).toLocaleDateString('pt-BR')}
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

export default StrategyList; 