export interface ReportFilter {
  startDate: string;
  endDate: string;
  categoryIds?: string[];
  includeIncome?: boolean;
  includeExpense?: boolean;
  groupBy?: 'day' | 'week' | 'month' | 'category';
}

export interface ReportSummary {
  totalIncome: number;
  totalExpense: number;
  netBalance: number;
  topExpenseCategories: {
    categoryId: string;
    categoryName: string;
    amount: number;
    percentage: number;
  }[];
  topIncomeCategories: {
    categoryId: string;
    categoryName: string;
    amount: number;
    percentage: number;
  }[];
  periodComparison: {
    currentPeriod: {
      income: number;
      expense: number;
      balance: number;
    };
    previousPeriod: {
      income: number;
      expense: number;
      balance: number;
    };
    percentageChange: {
      income: number;
      expense: number;
      balance: number;
    };
  };
}

export interface TimeSeriesData {
  label: string;
  income: number;
  expense: number;
  balance: number;
}

export interface CategoryDistribution {
  categoryId: string;
  categoryName: string;
  amount: number;
  percentage: number;
  color?: string;
}

export interface TransactionAnalysis {
  largestIncome: {
    amount: number;
    date: string;
    category: string;
    description: string;
  };
  largestExpense: {
    amount: number;
    date: string;
    category: string;
    description: string;
  };
  averageDailyExpense: number;
  averageTransactionAmount: number;
  transactionCount: {
    total: number;
    income: number;
    expense: number;
  };
}

export interface Report {
  summary: ReportSummary;
  timeSeriesData: TimeSeriesData[];
  categoryDistribution: {
    income: CategoryDistribution[];
    expense: CategoryDistribution[];
  };
  transactionAnalysis: TransactionAnalysis;
} 