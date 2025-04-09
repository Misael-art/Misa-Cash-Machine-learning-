/**
 * Serviço de orçamentos para interagir com as rotas de orçamentos da API
 */

// Tipo para as respostas da API
interface ApiResponse<T> {
  success?: boolean;
  message?: string;
  error?: string;
  [key: string]: any;
}

// Tipo para orçamento
export interface Budget {
  id?: number;
  user_id: number;
  name: string;
  amount: number;
  spent: number;
  category: string;
  start_date: string;
  end_date: string;
  repeat: boolean;
  repeat_frequency?: 'monthly' | 'quarterly' | 'yearly' | null;
  notifications_enabled: boolean;
  notification_threshold: number; // Percentual (0-100) para notificar quando atingido
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

// Tipo para filtros de orçamentos
export interface BudgetFilters {
  period?: 'current' | 'past' | 'future' | 'all';
  category?: string;
  startDate?: string;
  endDate?: string;
  search?: string;
  page?: number;
  limit?: number;
  sort?: string;
  order?: 'asc' | 'desc';
}

// URL base da API
const API_URL = '/api/budgets';

/**
 * Converte os filtros em parâmetros de consulta para a URL
 */
const buildQueryParams = (filters: BudgetFilters): string => {
  const params = new URLSearchParams();
  
  if (filters.period) params.append('period', filters.period);
  if (filters.category) params.append('category', filters.category);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);
  if (filters.search) params.append('search', filters.search);
  if (filters.page) params.append('page', filters.page.toString());
  if (filters.limit) params.append('limit', filters.limit.toString());
  if (filters.sort) params.append('sort', filters.sort);
  if (filters.order) params.append('order', filters.order);
  
  return params.toString();
};

/**
 * Obtém o token de autenticação do localStorage
 */
const getAuthHeader = (): HeadersInit => {
  const token = localStorage.getItem('authToken');
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
};

/**
 * Lista todos os orçamentos com filtros opcionais
 */
export const listBudgets = async (filters: BudgetFilters = {}): Promise<ApiResponse<{ budgets: Budget[]; total: number; page: number; limit: number }>> => {
  try {
    const queryParams = buildQueryParams(filters);
    const url = `${API_URL}?${queryParams}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: getAuthHeader(),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao listar orçamentos:', error);
    return { success: false, error: 'Ocorreu um erro ao listar os orçamentos.' };
  }
};

/**
 * Obtém um orçamento específico pelo ID
 */
export const getBudget = async (id: number): Promise<ApiResponse<{ budget: Budget }>> => {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'GET',
      headers: getAuthHeader(),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Erro ao obter orçamento com ID ${id}:`, error);
    return { success: false, error: 'Ocorreu um erro ao obter o orçamento.' };
  }
};

/**
 * Cria um novo orçamento
 */
export const createBudget = async (budget: Omit<Budget, 'id' | 'spent' | 'created_at' | 'updated_at'>): Promise<ApiResponse<{ budget: Budget }>> => {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: getAuthHeader(),
      body: JSON.stringify(budget),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao criar orçamento:', error);
    return { success: false, error: 'Ocorreu um erro ao criar o orçamento.' };
  }
};

/**
 * Atualiza um orçamento existente
 */
export const updateBudget = async (id: number, budget: Partial<Budget>): Promise<ApiResponse<{ budget: Budget }>> => {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: getAuthHeader(),
      body: JSON.stringify(budget),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Erro ao atualizar orçamento com ID ${id}:`, error);
    return { success: false, error: 'Ocorreu um erro ao atualizar o orçamento.' };
  }
};

/**
 * Exclui um orçamento pelo ID
 */
export const deleteBudget = async (id: number): Promise<ApiResponse<null>> => {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Erro ao excluir orçamento com ID ${id}:`, error);
    return { success: false, error: 'Ocorreu um erro ao excluir o orçamento.' };
  }
};

/**
 * Obtém um resumo dos orçamentos atuais
 */
export const getBudgetsSummary = async (): Promise<ApiResponse<{
  total_budget: number;
  total_spent: number;
  percentage_used: number;
  budgets_count: number;
  budgets_at_risk: number;
  category_breakdown: { category: string; budget: number; spent: number; percentage: number }[];
}>> => {
  try {
    const response = await fetch(`${API_URL}/summary`, {
      method: 'GET',
      headers: getAuthHeader(),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao obter resumo dos orçamentos:', error);
    return { success: false, error: 'Ocorreu um erro ao obter o resumo dos orçamentos.' };
  }
}; 