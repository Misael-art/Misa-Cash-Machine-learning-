import React, { createContext, useContext, ReactNode, useState, useCallback } from 'react';
import { 
  Transaction, 
  TransactionFilters,
  listTransactions, 
  getTransaction,
  createTransaction,
  updateTransaction,
  deleteTransaction,
  getTransactionsSummary,
  getChartData
} from '../services/transactions';

interface TransactionContextType {
  transactions: Transaction[];
  loading: boolean;
  error: string | null;
  filters: TransactionFilters;
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
  summary: {
    totalIncome: number;
    totalExpense: number;
    balance: number;
    categoriesSummary: { category: string; total: number; percentage: number }[];
    recentTransactions: Transaction[];
  } | null;
  chartData: {
    labels: string[];
    datasets: { label: string; data: number[]; backgroundColor?: string[] }[];
  } | null;
  fetchTransactions: (newFilters?: TransactionFilters) => Promise<void>;
  fetchTransaction: (id: number) => Promise<Transaction | null>;
  addTransaction: (transaction: Omit<Transaction, 'id' | 'created_at' | 'updated_at'>) => Promise<Transaction | null>;
  editTransaction: (id: number, transaction: Partial<Transaction>) => Promise<Transaction | null>;
  removeTransaction: (id: number) => Promise<boolean>;
  fetchSummary: (period: 'week' | 'month' | 'year') => Promise<void>;
  fetchChartData: (
    chartType: 'category' | 'timeline' | 'comparison',
    period: 'week' | 'month' | 'year',
    type: 'income' | 'expense' | 'all'
  ) => Promise<void>;
  setTransactionFilters: (newFilters: TransactionFilters) => void;
  resetFilters: () => void;
}

const TransactionContext = createContext<TransactionContextType | undefined>(undefined);

interface TransactionProviderProps {
  children: ReactNode;
}

export const TransactionProvider: React.FC<TransactionProviderProps> = ({ children }) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<TransactionFilters>({
    page: 1,
    limit: 10,
    type: 'all',
    sort: 'date',
    order: 'desc'
  });
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0
  });
  const [summary, setSummary] = useState<TransactionContextType['summary']>(null);
  const [chartData, setChartData] = useState<TransactionContextType['chartData']>(null);

  const fetchTransactions = useCallback(async (newFilters?: TransactionFilters) => {
    setLoading(true);
    setError(null);
    
    const currentFilters = newFilters ? { ...filters, ...newFilters } : filters;
    
    try {
      const response = await listTransactions(currentFilters);
      
      if (response.success) {
        setTransactions(response.transactions);
        setPagination({
          page: response.page,
          limit: response.limit,
          total: response.total
        });
      } else {
        setError(response.error || 'Erro ao carregar transações');
      }
    } catch (err) {
      setError('Erro ao buscar transações');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const fetchTransaction = useCallback(async (id: number): Promise<Transaction | null> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await getTransaction(id);
      
      if (response.success) {
        return response.transaction;
      } else {
        setError(response.error || 'Erro ao carregar transação');
        return null;
      }
    } catch (err) {
      setError('Erro ao buscar transação');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const addTransaction = useCallback(async (transaction: Omit<Transaction, 'id' | 'created_at' | 'updated_at'>): Promise<Transaction | null> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await createTransaction(transaction);
      
      if (response.success) {
        // Atualiza a lista de transações
        fetchTransactions();
        return response.transaction;
      } else {
        setError(response.error || 'Erro ao criar transação');
        return null;
      }
    } catch (err) {
      setError('Erro ao adicionar transação');
      return null;
    } finally {
      setLoading(false);
    }
  }, [fetchTransactions]);

  const editTransaction = useCallback(async (id: number, transaction: Partial<Transaction>): Promise<Transaction | null> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await updateTransaction(id, transaction);
      
      if (response.success) {
        // Atualiza a lista de transações
        fetchTransactions();
        return response.transaction;
      } else {
        setError(response.error || 'Erro ao atualizar transação');
        return null;
      }
    } catch (err) {
      setError('Erro ao editar transação');
      return null;
    } finally {
      setLoading(false);
    }
  }, [fetchTransactions]);

  const removeTransaction = useCallback(async (id: number): Promise<boolean> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await deleteTransaction(id);
      
      if (response.success) {
        // Atualiza a lista de transações
        fetchTransactions();
        return true;
      } else {
        setError(response.error || 'Erro ao excluir transação');
        return false;
      }
    } catch (err) {
      setError('Erro ao remover transação');
      return false;
    } finally {
      setLoading(false);
    }
  }, [fetchTransactions]);

  const fetchSummary = useCallback(async (period: 'week' | 'month' | 'year' = 'month') => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await getTransactionsSummary(period);
      
      if (response.success) {
        setSummary({
          totalIncome: response.totalIncome,
          totalExpense: response.totalExpense,
          balance: response.balance,
          categoriesSummary: response.categoriesSummary,
          recentTransactions: response.recentTransactions
        });
      } else {
        setError(response.error || 'Erro ao carregar resumo');
      }
    } catch (err) {
      setError('Erro ao buscar resumo das transações');
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchChartData = useCallback(async (
    chartType: 'category' | 'timeline' | 'comparison', 
    period: 'week' | 'month' | 'year' = 'month',
    type: 'income' | 'expense' | 'all' = 'all'
  ) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await getChartData(chartType, period, type);
      
      if (response.success) {
        setChartData({
          labels: response.labels,
          datasets: response.datasets
        });
      } else {
        setError(response.error || 'Erro ao carregar dados do gráfico');
      }
    } catch (err) {
      setError('Erro ao buscar dados para o gráfico');
    } finally {
      setLoading(false);
    }
  }, []);

  const setTransactionFilters = useCallback((newFilters: TransactionFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({
      page: 1,
      limit: 10,
      type: 'all',
      sort: 'date',
      order: 'desc'
    });
  }, []);

  const value = {
    transactions,
    loading,
    error,
    filters,
    pagination,
    summary,
    chartData,
    fetchTransactions,
    fetchTransaction,
    addTransaction,
    editTransaction,
    removeTransaction,
    fetchSummary,
    fetchChartData,
    setTransactionFilters,
    resetFilters
  };

  return (
    <TransactionContext.Provider value={value}>
      {children}
    </TransactionContext.Provider>
  );
};

export const useTransactions = (): TransactionContextType => {
  const context = useContext(TransactionContext);
  
  if (context === undefined) {
    throw new Error('useTransactions deve ser usado dentro de um TransactionProvider');
  }
  
  return context;
}; 