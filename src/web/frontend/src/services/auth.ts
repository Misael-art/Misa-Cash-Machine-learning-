/**
 * Serviço de autenticação para interagir com as rotas de autenticação da API
 */

// Tipo para as respostas da API
interface ApiResponse<T> {
  success?: boolean;
  message?: string;
  error?: string;
  [key: string]: any;
}

// Tipo para o usuário
export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  role: string;
}

// Credenciais de login
export interface LoginCredentials {
  email: string;
  password: string;
}

// Dados de registro
export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

// URL base da API
const API_URL = '/api/auth';

/**
 * Registra um novo usuário
 * @param userData Dados do usuário para registro
 * @returns Promise com a resposta da API
 */
export const register = async (userData: RegisterData): Promise<ApiResponse<{ user: User; token: string }>> => {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao registrar usuário:', error);
    return { success: false, error: 'Ocorreu um erro ao registrar o usuário.' };
  }
};

/**
 * Realiza o login do usuário
 * @param credentials Credenciais de login
 * @returns Promise com a resposta da API
 */
export const login = async (credentials: LoginCredentials): Promise<ApiResponse<{ user: User; token: string }>> => {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    const data = await response.json();
    
    // Se o login for bem-sucedido, armazena o token no localStorage
    if (response.ok && data.token) {
      localStorage.setItem('authToken', data.token);
    }
    
    return data;
  } catch (error) {
    console.error('Erro ao fazer login:', error);
    return { success: false, error: 'Ocorreu um erro ao fazer login.' };
  }
};

/**
 * Obtém os dados do usuário logado
 * @returns Promise com os dados do usuário
 */
export const getCurrentUser = async (): Promise<ApiResponse<{ user: User }>> => {
  try {
    // Obtém o token do localStorage
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      return { success: false, error: 'Usuário não autenticado.' };
    }
    
    const response = await fetch(`${API_URL}/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao obter dados do usuário:', error);
    return { success: false, error: 'Ocorreu um erro ao obter os dados do usuário.' };
  }
};

/**
 * Realiza o logout do usuário
 */
export const logout = (): void => {
  localStorage.removeItem('authToken');
};

/**
 * Verifica se o usuário está autenticado
 * @returns Boolean indicando se o usuário está autenticado
 */
export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('authToken');
}; 