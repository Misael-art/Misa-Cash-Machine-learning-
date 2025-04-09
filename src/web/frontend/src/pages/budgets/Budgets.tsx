import React, { useState } from 'react';
import {
  Box,
  Button,
  Flex,
  Heading,
  Text,
  useDisclosure,
  SimpleGrid,
  Progress,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Badge,
  Divider,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  IconButton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Spinner,
  Alert,
  AlertIcon,
  HStack
} from '@chakra-ui/react';
import { FiPlus, FiMoreVertical, FiEdit2, FiTrash2 } from 'react-icons/fi';
import { useBudget } from '../../contexts/BudgetContext';
import { useCategory } from '../../contexts/CategoryContext';
import BudgetFormModal from '../../components/budget/BudgetFormModal';
import BudgetDeleteModal from '../../components/budget/BudgetDeleteModal';
import { formatCurrency } from '../../utils/formatters';
import BudgetSummaryCards from '../../components/budget/BudgetSummaryCards';

const Budgets: React.FC = () => {
  const { budgets, summary, loading, summaryLoading, error } = useBudget();
  const { categories } = useCategory();
  
  const [selectedBudget, setSelectedBudget] = useState<string | null>(null);
  
  const {
    isOpen: isFormOpen,
    onOpen: onFormOpen,
    onClose: onFormClose
  } = useDisclosure();
  
  const {
    isOpen: isDeleteOpen,
    onOpen: onDeleteOpen,
    onClose: onDeleteClose
  } = useDisclosure();

  const handleAddBudget = () => {
    setSelectedBudget(null);
    onFormOpen();
  };

  const handleEditBudget = (id: string) => {
    setSelectedBudget(id);
    onFormOpen();
  };

  const handleDeleteBudget = (id: string) => {
    setSelectedBudget(id);
    onDeleteOpen();
  };

  const getBudgetStatus = (spent: number, amount: number) => {
    const percentUsed = (spent / amount) * 100;
    
    if (percentUsed >= 100) return 'danger';
    if (percentUsed >= 75) return 'warning';
    return 'success';
  };

  const getColorScheme = (status: string) => {
    switch (status) {
      case 'danger': return 'red';
      case 'warning': return 'orange';
      case 'success': return 'green';
      default: return 'blue';
    }
  };

  return (
    <Box p={4}>
      <Flex justify="space-between" align="center" mb={6}>
        <Heading size="lg">Orçamentos</Heading>
        <Button
          leftIcon={<FiPlus />}
          colorScheme="teal"
          onClick={handleAddBudget}
          isDisabled={loading}
        >
          Novo Orçamento
        </Button>
      </Flex>

      {error && (
        <Alert status="error" mb={6} borderRadius="md">
          <AlertIcon />
          {error}
        </Alert>
      )}

      {/* Resumo dos Orçamentos */}
      {summaryLoading ? (
        <Flex justify="center" my={8}>
          <Spinner size="xl" />
        </Flex>
      ) : summary ? (
        <BudgetSummaryCards summary={summary} />
      ) : null}

      <Divider my={6} />

      {/* Lista de Orçamentos */}
      {loading ? (
        <Flex justify="center" my={8}>
          <Spinner size="xl" />
        </Flex>
      ) : budgets.length > 0 ? (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
          {budgets.map((budget) => {
            const status = getBudgetStatus(budget.spent, budget.amount);
            const percentUsed = (budget.spent / budget.amount) * 100;
            const colorScheme = getColorScheme(status);
            const category = categories.find(c => c.id === budget.categoryId);
            
            return (
              <Card key={budget.id} boxShadow="md" borderRadius="lg">
                <CardHeader pb={2}>
                  <Flex justify="space-between" align="center">
                    <Heading size="md">{budget.name}</Heading>
                    <Menu>
                      <MenuButton
                        as={IconButton}
                        icon={<FiMoreVertical />}
                        variant="ghost"
                        size="sm"
                        aria-label="Opções"
                      />
                      <MenuList>
                        <MenuItem 
                          icon={<FiEdit2 />} 
                          onClick={() => handleEditBudget(budget.id)}
                        >
                          Editar
                        </MenuItem>
                        <MenuItem 
                          icon={<FiTrash2 />} 
                          onClick={() => handleDeleteBudget(budget.id)}
                          color="red.500"
                        >
                          Excluir
                        </MenuItem>
                      </MenuList>
                    </Menu>
                  </Flex>
                  <HStack mt={2}>
                    <Badge colorScheme={colorScheme}>
                      {status === 'danger' ? 'Excedido' : 
                       status === 'warning' ? 'Alerta' : 'Dentro do limite'}
                    </Badge>
                    {category && (
                      <Badge colorScheme="purple">{category.name}</Badge>
                    )}
                  </HStack>
                </CardHeader>
                
                <CardBody py={2}>
                  <Progress 
                    value={percentUsed > 100 ? 100 : percentUsed} 
                    colorScheme={colorScheme}
                    size="sm"
                    borderRadius="full"
                    mb={3}
                  />
                  
                  <Stat>
                    <StatLabel>Total Gasto</StatLabel>
                    <StatNumber>{formatCurrency(budget.spent)}</StatNumber>
                    <StatHelpText>
                      de {formatCurrency(budget.amount)} ({percentUsed.toFixed(0)}%)
                    </StatHelpText>
                  </Stat>
                </CardBody>
                
                <CardFooter pt={0}>
                  <Text fontSize="sm" color="gray.500">
                    {new Date(budget.startDate).toLocaleDateString()} - {new Date(budget.endDate).toLocaleDateString()}
                  </Text>
                </CardFooter>
              </Card>
            );
          })}
        </SimpleGrid>
      ) : (
        <Flex
          direction="column"
          align="center"
          justify="center"
          p={8}
          bg="gray.50"
          borderRadius="lg"
        >
          <Text fontSize="lg" mb={4}>
            Nenhum orçamento encontrado
          </Text>
          <Button
            leftIcon={<FiPlus />}
            colorScheme="teal"
            onClick={handleAddBudget}
          >
            Criar Orçamento
          </Button>
        </Flex>
      )}

      {/* Modais */}
      <BudgetFormModal
        isOpen={isFormOpen}
        onClose={onFormClose}
        budgetId={selectedBudget}
      />
      
      <BudgetDeleteModal
        isOpen={isDeleteOpen}
        onClose={onDeleteClose}
        budgetId={selectedBudget}
      />
    </Box>
  );
};

export default Budgets; 