import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { TransactionProvider } from './contexts/TransactionContext';
import { BudgetProvider } from './contexts/BudgetContext';
import PrivateRoute from './components/PrivateRoute';

// Páginas
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Profile from './pages/Profile';
import Dashboard from './pages/dashboard/Dashboard';
import Transactions from './pages/transactions/Transactions';
import Budgets from './pages/budgets/Budgets';

// Componente principal da aplicação
const App: React.FC = () => {
  return (
    <AuthProvider>
      <TransactionProvider>
        <BudgetProvider>
          <Router>
            <div className="app-container">
              <Routes>
                {/* Rotas públicas */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                
                {/* Rotas protegidas */}
                <Route 
                  path="/profile" 
                  element={
                    <PrivateRoute>
                      <Profile />
                    </PrivateRoute>
                  } 
                />
                
                <Route 
                  path="/dashboard" 
                  element={
                    <PrivateRoute>
                      <Dashboard />
                    </PrivateRoute>
                  } 
                />
                
                <Route 
                  path="/transactions" 
                  element={
                    <PrivateRoute>
                      <Transactions />
                    </PrivateRoute>
                  } 
                />
                
                <Route 
                  path="/budgets" 
                  element={
                    <PrivateRoute>
                      <Budgets />
                    </PrivateRoute>
                  } 
                />
                
                {/* Rota padrão - redireciona para o dashboard */}
                <Route 
                  path="/" 
                  element={
                    <PrivateRoute>
                      <Dashboard />
                    </PrivateRoute>
                  } 
                />
                
                {/* Rota para qualquer outra URL não correspondente */}
                <Route path="*" element={<Navigate to="/" />} />
              </Routes>
            </div>
          </Router>
        </BudgetProvider>
      </TransactionProvider>
    </AuthProvider>
  );
};

export default App; 