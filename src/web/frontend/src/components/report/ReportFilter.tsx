import React, { useState } from 'react';
import {
  Box,
  Flex,
  FormControl,
  FormLabel,
  Input,
  Select,
  Checkbox,
  Button,
  HStack,
  VStack,
  Divider,
  useColorModeValue
} from '@chakra-ui/react';
import { FiFilter, FiRefreshCw } from 'react-icons/fi';
import { useReport } from '../../contexts/ReportContext';
import { useCategory } from '../../contexts/CategoryContext';
import { ReportFilter as ReportFilterType } from '../../types/Report';

interface PredefinedPeriod {
  label: string;
  startDate: Date;
  endDate: Date;
}

const ReportFilter: React.FC = () => {
  const { filter, updateFilter, resetFilter, generateReport, loading } = useReport();
  const { categories } = useCategory();
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);

  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const getPredefinedPeriods = (): { [key: string]: PredefinedPeriod } => {
    const today = new Date();
    const thisMonth = {
      label: 'Este Mês',
      startDate: new Date(today.getFullYear(), today.getMonth(), 1),
      endDate: today
    };

    const lastMonth = {
      label: 'Mês Passado',
      startDate: new Date(today.getFullYear(), today.getMonth() - 1, 1),
      endDate: new Date(today.getFullYear(), today.getMonth(), 0)
    };

    const thisYear = {
      label: 'Este Ano',
      startDate: new Date(today.getFullYear(), 0, 1),
      endDate: today
    };

    const lastThreeMonths = {
      label: 'Últimos 3 Meses',
      startDate: new Date(today.getFullYear(), today.getMonth() - 3, today.getDate()),
      endDate: today
    };

    const lastSixMonths = {
      label: 'Últimos 6 Meses',
      startDate: new Date(today.getFullYear(), today.getMonth() - 6, today.getDate()),
      endDate: today
    };

    return {
      thisMonth,
      lastMonth,
      thisYear,
      lastThreeMonths,
      lastSixMonths
    };
  };

  const handlePeriodChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const periodKey = e.target.value;
    if (periodKey === 'custom') return; // Não alterar datas para período personalizado

    const periods = getPredefinedPeriods();
    const selectedPeriod = periods[periodKey];

    if (selectedPeriod) {
      updateFilter({
        startDate: selectedPeriod.startDate.toISOString().split('T')[0],
        endDate: selectedPeriod.endDate.toISOString().split('T')[0]
      });
    }
  };

  const handleCategoryChange = (categoryId: string, isChecked: boolean) => {
    let newCategories: string[];
    
    if (isChecked) {
      newCategories = [...selectedCategories, categoryId];
    } else {
      newCategories = selectedCategories.filter(id => id !== categoryId);
    }
    
    setSelectedCategories(newCategories);
    updateFilter({ categoryIds: newCategories.length > 0 ? newCategories : undefined });
  };

  const handleApplyFilters = () => {
    generateReport(filter);
  };

  const handleResetFilters = () => {
    resetFilter();
    setSelectedCategories([]);
  };

  return (
    <Box p={4} bg={bgColor} borderRadius="lg" boxShadow="sm" border="1px" borderColor={borderColor}>
      <VStack spacing={4} align="stretch">
        <Flex justifyContent="space-between" alignItems="center">
          <FormControl>
            <FormLabel>Período Predefinido</FormLabel>
            <Select onChange={handlePeriodChange} defaultValue="thisMonth">
              <option value="thisMonth">Este Mês</option>
              <option value="lastMonth">Mês Passado</option>
              <option value="thisYear">Este Ano</option>
              <option value="lastThreeMonths">Últimos 3 Meses</option>
              <option value="lastSixMonths">Últimos 6 Meses</option>
              <option value="custom">Personalizado</option>
            </Select>
          </FormControl>
        </Flex>

        <Flex gap={4} flexDir={{ base: 'column', md: 'row' }}>
          <FormControl>
            <FormLabel>Data Inicial</FormLabel>
            <Input
              type="date"
              value={filter.startDate}
              onChange={(e) => updateFilter({ startDate: e.target.value })}
            />
          </FormControl>
          <FormControl>
            <FormLabel>Data Final</FormLabel>
            <Input
              type="date"
              value={filter.endDate}
              onChange={(e) => updateFilter({ endDate: e.target.value })}
            />
          </FormControl>
        </Flex>

        <Divider my={2} />

        <FormControl>
          <FormLabel>Agrupar Por</FormLabel>
          <Select 
            value={filter.groupBy || 'day'} 
            onChange={(e) => updateFilter({ groupBy: e.target.value as 'day' | 'week' | 'month' | 'category' })}
          >
            <option value="day">Dia</option>
            <option value="week">Semana</option>
            <option value="month">Mês</option>
            <option value="category">Categoria</option>
          </Select>
        </FormControl>

        <Flex gap={4}>
          <FormControl>
            <FormLabel>Tipo de Transação</FormLabel>
            <HStack>
              <Checkbox 
                isChecked={filter.includeIncome} 
                onChange={(e) => updateFilter({ includeIncome: e.target.checked })}
              >
                Receitas
              </Checkbox>
              <Checkbox 
                isChecked={filter.includeExpense} 
                onChange={(e) => updateFilter({ includeExpense: e.target.checked })}
              >
                Despesas
              </Checkbox>
            </HStack>
          </FormControl>
        </Flex>

        <Divider my={2} />

        <FormControl>
          <FormLabel>Categorias</FormLabel>
          <Flex flexWrap="wrap" gap={2}>
            {categories.map(category => (
              <Checkbox
                key={category.id}
                isChecked={selectedCategories.includes(category.id)}
                onChange={(e) => handleCategoryChange(category.id, e.target.checked)}
              >
                {category.name}
              </Checkbox>
            ))}
          </Flex>
        </FormControl>

        <Flex justifyContent="flex-end" gap={2}>
          <Button 
            leftIcon={<FiRefreshCw />} 
            onClick={handleResetFilters}
            variant="outline"
          >
            Limpar
          </Button>
          <Button 
            leftIcon={<FiFilter />} 
            colorScheme="teal" 
            onClick={handleApplyFilters}
            isLoading={loading}
            loadingText="Gerando"
          >
            Aplicar Filtros
          </Button>
        </Flex>
      </VStack>
    </Box>
  );
};

export default ReportFilter; 