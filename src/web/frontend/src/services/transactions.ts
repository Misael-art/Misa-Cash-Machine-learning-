/**
 * Serviço de transações para interagir com as rotas de transações da API
 */

// Tipo para as respostas da API
interface ApiResponse<T> {
  success?: boolean;
  message?: string;
  error?: string;
  [key: string]: any;
}

// Tipo para transação
export interface Transaction {
  id?: number;
  user_id: number;
  description: string;
  amount: number;
  type: 'income' | 'expense';
  category: string;
  date: string;
  is_recurring: boolean;
  recurrence_frequency?: 'daily' | 'weekly' | 'monthly' | 'yearly' | null;
  tags?: string[];
  created_at?: string;
  updated_at?: string;
}

// Tipo para filtros de transações
export interface TransactionFilters {
  startDate?: string;
  endDate?: string;
  type?: 'income' | 'expense' | 'all';
  category?: string;
  minAmount?: number;
  maxAmount?: number;
  search?: string;
  page?: number;
  limit?: number;
  sort?: string;
  order?: 'asc' | 'desc';
}

// URL base da API
const API_URL = '/api/transactions';

/**
 * Converte os filtros em parâmetros de consulta para a URL
 */
const buildQueryParams = (filters: TransactionFilters): string => {
  const params = new URLSearchParams();
  
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);
  if (filters.type && filters.type !== 'all') params.append('type', filters.type);
  if (filters.category) params.append('category', filters.category);
  if (filters.minAmount) params.append('min_amount', filters.minAmount.toString());
  if (filters.maxAmount) params.append('max_amount', filters.maxAmount.toString());
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
 * Lista todas as transações com filtros opcionais
 */
export const listTransactions = async (filters: TransactionFilters = {}): Promise<ApiResponse<{ transactions: Transaction[]; total: number; page: number; limit: number }>> => {
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
    console.error('Erro ao listar transações:', error);
    return { success: false, error: 'Ocorreu um erro ao listar as transações.' };
  }
};

/**
 * Obtém uma transação específica pelo ID
 */
export const getTransaction = async (id: number): Promise<ApiResponse<{ transaction: Transaction }>> => {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'GET',
      headers: getAuthHeader(),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Erro ao obter transação com ID ${id}:`, error);
    return { success: false, error: 'Ocorreu um erro ao obter a transação.' };
  }
};

/**
 * Cria uma nova transação
 */
export const createTransaction = async (transaction: Omit<Transaction, 'id' | 'created_at' | 'updated_at'>): Promise<ApiResponse<{ transaction: Transaction }>> => {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: getAuthHeader(),
      body: JSON.stringify(transaction),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao criar transação:', error);
    return { success: false, error: 'Ocorreu um erro ao criar a transação.' };
  }
};

/**
 * Atualiza uma transação existente
 */
export const updateTransaction = async (id: number, transaction: Partial<Transaction>): Promise<ApiResponse<{ transaction: Transaction }>> => {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: getAuthHeader(),
      body: JSON.stringify(transaction),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Erro ao atualizar transação com ID ${id}:`, error);
    return { success: false, error: 'Ocorreu um erro ao atualizar a transação.' };
  }
};

/**
 * Exclui uma transação pelo ID
 */
export const deleteTransaction = async (id: number): Promise<ApiResponse<null>> => {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Erro ao excluir transação com ID ${id}:`, error);
    return { success: false, error: 'Ocorreu um erro ao excluir a transação.' };
  }
};

/**
 * Obtém o resumo das transações para o dashboard
 */
export const getTransactionsSummary = async (period: 'week' | 'month' | 'year' = 'month'): Promise<ApiResponse<{
  totalIncome: number;
  totalExpense: number;
  balance: number;
  categoriesSummary: { category: string; total: number; percentage: number }[];
  recentTransactions: Transaction[];
}>> => {
  try {
    const response = await fetch(`${API_URL}/summary?period=${period}`, {
      method: 'GET',
      headers: getAuthHeader(),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao obter resumo das transações:', error);
    return { success: false, error: 'Ocorreu um erro ao obter o resumo das transações.' };
  }
};

/**
 * Obtém dados para os gráficos do dashboard
 */
export const getChartData = async (
  chartType: 'category' | 'timeline' | 'comparison',
  period: 'week' | 'month' | 'year' = 'month',
  type: 'income' | 'expense' | 'all' = 'all'
): Promise<ApiResponse<{
  labels: string[];
  datasets: { label: string; data: number[]; backgroundColor?: string[] }[];
}>> => {
  try {
    const response = await fetch(`${API_URL}/charts?type=${chartType}&period=${period}&transaction_type=${type}`, {
      method: 'GET',
      headers: getAuthHeader(),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao obter dados para gráficos:', error);
    return { success: false, error: 'Ocorreu um erro ao obter os dados para os gráficos.' };
  }
}; 