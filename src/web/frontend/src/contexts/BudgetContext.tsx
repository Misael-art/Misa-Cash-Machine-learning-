import React, { createContext, useContext, ReactNode, useState, useCallback, useEffect } from 'react';
import { 
  Budget, 
  BudgetFilters,
  listBudgets, 
  getBudget,
  createBudget,
  updateBudget,
  deleteBudget,
  getBudgetsSummary
} from '../services/budgets';
import { BudgetSummary } from '../types/Budget';
import { budgetService } from '../services/budgetService';
import { useAuth } from './AuthContext';
import { useToast } from '../hooks/useToast';

interface BudgetContextType {
  budgets: Budget[];
  loading: boolean;
  error: string | null;
  filters: BudgetFilters;
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
  summary: BudgetSummary | null;
  fetchBudgets: (newFilters?: BudgetFilters) => Promise<void>;
  fetchBudget: (id: number) => Promise<Budget | null>;
  addBudget: (budget: Omit<Budget, 'id' | 'spent' | 'created_at' | 'updated_at'>) => Promise<Budget | null>;
  editBudget: (id: number, budget: Partial<Budget>) => Promise<Budget | null>;
  removeBudget: (id: number) => Promise<boolean>;
  fetchSummary: () => Promise<void>;
  setBudgetFilters: (newFilters: BudgetFilters) => void;
  resetFilters: () => void;
  createBudget: (budget: Omit<Budget, 'id' | 'createdAt' | 'updatedAt' | 'spent'>) => Promise<void>;
  updateBudget: (id: string, budget: Partial<Budget>) => Promise<void>;
  deleteBudget: (id: string) => Promise<void>;
  refreshBudgets: () => Promise<void>;
}

const BudgetContext = createContext<BudgetContextType | undefined>(undefined);

interface BudgetProviderProps {
  children: ReactNode;
}

export const BudgetProvider: React.FC<BudgetProviderProps> = ({ children }) => {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<BudgetFilters>({
    period: 'current',
    page: 1,
    limit: 10,
    sort: 'end_date',
    order: 'asc'
  });
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0
  });
  const [summary, setSummary] = useState<BudgetSummary | null>(null);
  const { isAuthenticated } = useAuth();
  const { showToast } = useToast();

  const fetchBudgets = useCallback(async (newFilters?: BudgetFilters) => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    setError(null);
    
    const currentFilters = newFilters ? { ...filters, ...newFilters } : filters;
    
    try {
      const response = await listBudgets(currentFilters);
      
      if (response.success) {
        setBudgets(response.budgets);
        setPagination({
          page: response.page,
          limit: response.limit,
          total: response.total
        });
      } else {
        setError(response.error || 'Erro ao carregar orçamentos');
        showToast('Erro ao carregar orçamentos', 'error');
      }
    } catch (err) {
      setError('Erro ao buscar orçamentos');
      showToast('Erro ao carregar orçamentos', 'error');
    } finally {
      setLoading(false);
    }
  }, [filters, isAuthenticated]);

  const fetchBudget = useCallback(async (id: number): Promise<Budget | null> => {
    if (!isAuthenticated) return null;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await getBudget(id);
      
      if (response.success) {
        return response.budget;
      } else {
        setError(response.error || 'Erro ao carregar orçamento');
        return null;
      }
    } catch (err) {
      setError('Erro ao buscar orçamento');
      return null;
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  const addBudget = useCallback(async (budget: Omit<Budget, 'id' | 'spent' | 'created_at' | 'updated_at'>): Promise<Budget | null> => {
    if (!isAuthenticated) return null;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await createBudget(budget);
      
      if (response.success) {
        // Atualiza a lista de orçamentos
        fetchBudgets();
        // Atualiza o resumo
        fetchSummary();
        return response.budget;
      } else {
        setError(response.error || 'Erro ao criar orçamento');
        showToast('Erro ao criar orçamento', 'error');
        return null;
      }
    } catch (err) {
      setError('Erro ao adicionar orçamento');
      showToast('Erro ao adicionar orçamento', 'error');
      return null;
    } finally {
      setLoading(false);
    }
  }, [fetchBudgets, isAuthenticated]);

  const editBudget = useCallback(async (id: number, budget: Partial<Budget>): Promise<Budget | null> => {
    if (!isAuthenticated) return null;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await updateBudget(id, budget);
      
      if (response.success) {
        // Atualiza a lista de orçamentos
        fetchBudgets();
        // Atualiza o resumo
        fetchSummary();
        return response.budget;
      } else {
        setError(response.error || 'Erro ao atualizar orçamento');
        showToast('Erro ao atualizar orçamento', 'error');
        return null;
      }
    } catch (err) {
      setError('Erro ao editar orçamento');
      showToast('Erro ao editar orçamento', 'error');
      return null;
    } finally {
      setLoading(false);
    }
  }, [fetchBudgets, isAuthenticated]);

  const removeBudget = useCallback(async (id: number): Promise<boolean> => {
    if (!isAuthenticated) return false;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await deleteBudget(id);
      
      if (response.success) {
        // Atualiza a lista de orçamentos
        fetchBudgets();
        // Atualiza o resumo
        fetchSummary();
        return true;
      } else {
        setError(response.error || 'Erro ao excluir orçamento');
        showToast('Erro ao excluir orçamento', 'error');
        return false;
      }
    } catch (err) {
      setError('Erro ao remover orçamento');
      showToast('Erro ao remover orçamento', 'error');
      return false;
    } finally {
      setLoading(false);
    }
  }, [fetchBudgets, isAuthenticated]);

  const fetchSummary = useCallback(async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await getBudgetsSummary();
      
      if (response.success) {
        setSummary({
          total_budget: response.total_budget,
          total_spent: response.total_spent,
          percentage_used: response.percentage_used,
          budgets_count: response.budgets_count,
          budgets_at_risk: response.budgets_at_risk,
          category_breakdown: response.category_breakdown
        });
      } else {
        setError(response.error || 'Erro ao carregar resumo dos orçamentos');
      }
    } catch (err) {
      setError('Erro ao buscar resumo dos orçamentos');
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  const setBudgetFilters = useCallback((newFilters: BudgetFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({
      period: 'current',
      page: 1,
      limit: 10,
      sort: 'end_date',
      order: 'asc'
    });
  }, []);

  const createBudget = async (budgetData: Omit<Budget, 'id' | 'createdAt' | 'updatedAt' | 'spent'>) => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      const newBudget = await budgetService.create(budgetData);
      setBudgets(prev => [...prev, newBudget]);
      fetchSummary(); // Atualiza o resumo após criar
      showToast('Orçamento criado com sucesso', 'success');
    } catch (err) {
      setError('Erro ao criar orçamento');
      showToast('Erro ao criar orçamento', 'error');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const updateBudget = async (id: string, budgetData: Partial<Budget>) => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      const updatedBudget = await budgetService.update(id, budgetData);
      setBudgets(prev => prev.map(budget => 
        budget.id === id ? updatedBudget : budget
      ));
      fetchSummary(); // Atualiza o resumo após editar
      showToast('Orçamento atualizado com sucesso', 'success');
    } catch (err) {
      setError('Erro ao atualizar orçamento');
      showToast('Erro ao atualizar orçamento', 'error');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const deleteBudget = async (id: string) => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      await budgetService.delete(id);
      setBudgets(prev => prev.filter(budget => budget.id !== id));
      fetchSummary(); // Atualiza o resumo após deletar
      showToast('Orçamento excluído com sucesso', 'success');
    } catch (err) {
      setError('Erro ao excluir orçamento');
      showToast('Erro ao excluir orçamento', 'error');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const refreshBudgets = async () => {
    await fetchBudgets();
    await fetchSummary();
  };

  const value: BudgetContextType = {
    budgets,
    loading,
    error,
    filters,
    pagination,
    summary,
    fetchBudgets,
    fetchBudget,
    addBudget,
    editBudget,
    removeBudget,
    fetchSummary,
    setBudgetFilters,
    resetFilters,
    createBudget,
    updateBudget,
    deleteBudget,
    refreshBudgets
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchBudgets();
      fetchSummary();
    }
  }, [isAuthenticated]);

  return (
    <BudgetContext.Provider value={value}>
      {children}
    </BudgetContext.Provider>
  );
};

export const useBudgets = (): BudgetContextType => {
  const context = useContext(BudgetContext);
  
  if (context === undefined) {
    throw new Error('useBudgets deve ser usado dentro de um BudgetProvider');
  }
  
  return context;
}; 