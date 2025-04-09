import { Budget, BudgetSummary } from '../types/Budget';
import { api } from './api';

export const budgetService = {
  async create(budget: Omit<Budget, 'id' | 'createdAt' | 'updatedAt' | 'spent'>): Promise<Budget> {
    const response = await api.post<Budget>('/budgets', budget);
    return response.data;
  },

  async getAll(): Promise<Budget[]> {
    const response = await api.get<Budget[]>('/budgets');
    return response.data;
  },

  async getById(id: string): Promise<Budget> {
    const response = await api.get<Budget>(`/budgets/${id}`);
    return response.data;
  },

  async update(id: string, budget: Partial<Budget>): Promise<Budget> {
    const response = await api.put<Budget>(`/budgets/${id}`, budget);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/budgets/${id}`);
  },

  async getSummary(): Promise<BudgetSummary> {
    const response = await api.get<BudgetSummary>('/budgets/summary');
    return response.data;
  }
}; 