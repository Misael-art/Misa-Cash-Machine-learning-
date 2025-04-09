import { ApiError } from '@/types';

// Mensagens de erro padrão
export const ERROR_MESSAGES = {
  NETWORK: 'Erro de conexão. Verifique sua internet e tente novamente.',
  UNAUTHORIZED: 'Sessão expirada. Por favor, faça login novamente.',
  FORBIDDEN: 'Você não tem permissão para realizar esta ação.',
  NOT_FOUND: 'O recurso solicitado não foi encontrado.',
  VALIDATION: 'Por favor, verifique os dados informados.',
  SERVER: 'Erro interno do servidor. Tente novamente mais tarde.',
  UNKNOWN: 'Ocorreu um erro inesperado. Tente novamente mais tarde.',
};

// Tratamento de erros da API
export const handleApiError = (error: any): ApiError => {
  if (error.response) {
    // Erro com resposta do servidor
    const status = error.response.status;
    const data = error.response.data;

    switch (status) {
      case 400:
        return {
          message: data.message || ERROR_MESSAGES.VALIDATION,
          code: 'VALIDATION_ERROR',
          status,
        };
      case 401:
        return {
          message: ERROR_MESSAGES.UNAUTHORIZED,
          code: 'UNAUTHORIZED',
          status,
        };
      case 403:
        return {
          message: ERROR_MESSAGES.FORBIDDEN,
          code: 'FORBIDDEN',
          status,
        };
      case 404:
        return {
          message: ERROR_MESSAGES.NOT_FOUND,
          code: 'NOT_FOUND',
          status,
        };
      case 500:
        return {
          message: ERROR_MESSAGES.SERVER,
          code: 'SERVER_ERROR',
          status,
        };
      default:
        return {
          message: data.message || ERROR_MESSAGES.UNKNOWN,
          code: 'UNKNOWN_ERROR',
          status,
        };
    }
  }

  if (error.request) {
    // Erro sem resposta do servidor
    return {
      message: ERROR_MESSAGES.NETWORK,
      code: 'NETWORK_ERROR',
      status: 0,
    };
  }

  // Erro na configuração da requisição
  return {
    message: ERROR_MESSAGES.UNKNOWN,
    code: 'REQUEST_ERROR',
    status: 0,
  };
};

// Validação de campos obrigatórios
export const validateRequiredFields = (data: Record<string, any>, fields: string[]): string[] => {
  const errors: string[] = [];

  fields.forEach((field) => {
    if (!data[field] || (typeof data[field] === 'string' && !data[field].trim())) {
      errors.push(`O campo ${field} é obrigatório`);
    }
  });

  return errors;
};

// Validação de formato de email
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validação de força da senha
export const validatePasswordStrength = (password: string): string[] => {
  const errors: string[] = [];

  if (password.length < 8) {
    errors.push('A senha deve ter pelo menos 8 caracteres');
  }

  if (!/[A-Z]/.test(password)) {
    errors.push('A senha deve conter pelo menos uma letra maiúscula');
  }

  if (!/[a-z]/.test(password)) {
    errors.push('A senha deve conter pelo menos uma letra minúscula');
  }

  if (!/[0-9]/.test(password)) {
    errors.push('A senha deve conter pelo menos um número');
  }

  if (!/[!@#$%^&*]/.test(password)) {
    errors.push('A senha deve conter pelo menos um caractere especial (!@#$%^&*)');
  }

  return errors;
};

// Tratamento de erros de formulário
export const handleFormError = (error: any): string => {
  if (error.response?.data?.errors) {
    const errors = error.response.data.errors;
    if (typeof errors === 'object') {
      return Object.values(errors).flat().join('\n');
    }
    return errors.join('\n');
  }
  return error.message || ERROR_MESSAGES.UNKNOWN;
}; 