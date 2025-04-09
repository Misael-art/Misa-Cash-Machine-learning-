import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from './ThemeContext';
import { AuthProvider } from './AuthContext';
import { TransactionProvider } from './TransactionContext';
import { ToastProvider } from './ToastContext';
import { CategoryProvider } from './CategoryContext';
import { BudgetProvider } from './BudgetContext';
import { ReportProvider } from './ReportContext';

interface AppProviderProps {
  children: React.ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <ToastProvider>
          <AuthProvider>
            <CategoryProvider>
              <TransactionProvider>
                <BudgetProvider>
                  <ReportProvider>
                    {children}
                  </ReportProvider>
                </BudgetProvider>
              </TransactionProvider>
            </CategoryProvider>
          </AuthProvider>
        </ToastProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}; 