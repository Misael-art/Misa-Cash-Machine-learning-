import { useState, useEffect, useCallback } from 'react';
import { User, login as loginApi, register as registerApi, getCurrentUser, logout as logoutApi, isAuthenticated as checkAuth, LoginCredentials, RegisterData } from '../services/auth';

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

export const useAuth = () => {
  const [state, setState] = useState<AuthState>({
    user: null,
    loading: true,
    error: null,
    isAuthenticated: checkAuth()
  });

  // Função para carregar o usuário atual
  const loadUser = useCallback(async () => {
    if (!checkAuth()) {
      setState({
        user: null,
        loading: false,
        error: null,
        isAuthenticated: false
      });
      return;
    }

    setState(prev => ({ ...prev, loading: true }));

    try {
      const response = await getCurrentUser();
      
      if (response.success && response.user) {
        setState({
          user: response.user,
          loading: false,
          error: null,
          isAuthenticated: true
        });
      } else {
        // Se houver erro ao carregar o usuário, considera como não autenticado
        logoutApi();
        setState({
          user: null,
          loading: false,
          error: response.error || 'Erro ao carregar usuário',
          isAuthenticated: false
        });
      }
    } catch (error) {
      logoutApi();
      setState({
        user: null,
        loading: false,
        error: 'Erro ao carregar usuário',
        isAuthenticated: false
      });
    }
  }, []);

  // Carrega o usuário na montagem do componente
  useEffect(() => {
    loadUser();
  }, [loadUser]);

  // Função de login
  const login = async (credentials: LoginCredentials) => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const response = await loginApi(credentials);
      
      if (response.token) {
        setState({
          user: response.user,
          loading: false,
          error: null,
          isAuthenticated: true
        });
        return { success: true };
      } else {
        setState(prev => ({
          ...prev,
          loading: false,
          error: response.error || response.message || 'Erro ao fazer login',
          isAuthenticated: false
        }));
        return { success: false, error: response.error || response.message };
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: 'Erro ao fazer login',
        isAuthenticated: false
      }));
      return { success: false, error: 'Erro ao fazer login' };
    }
  };

  // Função de registro
  const register = async (userData: RegisterData) => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const response = await registerApi(userData);
      
      if (response.token) {
        setState({
          user: response.user,
          loading: false,
          error: null,
          isAuthenticated: true
        });
        return { success: true };
      } else {
        setState(prev => ({
          ...prev,
          loading: false,
          error: response.error || response.message || 'Erro ao registrar',
          isAuthenticated: false
        }));
        return { success: false, error: response.error || response.message };
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: 'Erro ao registrar',
        isAuthenticated: false
      }));
      return { success: false, error: 'Erro ao registrar' };
    }
  };

  // Função de logout
  const logout = () => {
    logoutApi();
    setState({
      user: null,
      loading: false,
      error: null,
      isAuthenticated: false
    });
  };

  return {
    user: state.user,
    loading: state.loading,
    error: state.error,
    isAuthenticated: state.isAuthenticated,
    login,
    register,
    logout,
    refreshUser: loadUser
  };
}; 