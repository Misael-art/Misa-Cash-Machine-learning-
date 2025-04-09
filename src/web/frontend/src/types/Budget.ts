export interface Budget {
  id: string;
  name: string;
  amount: number;
  spent: number;
  categoryId: string;
  categoryName?: string;
  startDate: string;
  endDate: string;
  createdAt: string;
  updatedAt: string;
}

export interface BudgetFormData {
  name: string;
  amount: number;
  category: string;
  period: 'monthly' | 'quarterly' | 'annual';
  startDate: string;
  endDate: string;
}

export interface BudgetSummary {
  totalBudget: number;
  totalSpent: number;
  remaining: number;
  percentUsed: number;
  budgetsByCategory: {
    categoryId: string;
    categoryName: string;
    amount: number;
    spent: number;
    remaining: number;
    percentUsed: number;
  }[];
} 