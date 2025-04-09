import { VALIDATION } from '@/constants';

// Validação de email
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validação de senha
export const isValidPassword = (password: string): boolean => {
  return password.length >= VALIDATION.PASSWORD_MIN_LENGTH;
};

// Validação de nome de usuário
export const isValidUsername = (username: string): boolean => {
  return (
    username.length >= VALIDATION.USERNAME_MIN_LENGTH &&
    username.length <= VALIDATION.USERNAME_MAX_LENGTH
  );
};

// Validação de CPF
export const isValidCPF = (cpf: string): boolean => {
  const cleanCPF = cpf.replace(/[^\d]/g, '');

  if (cleanCPF.length !== 11) return false;

  if (/^(\d)\1{10}$/.test(cleanCPF)) return false;

  let sum = 0;
  for (let i = 0; i < 9; i++) {
    sum += parseInt(cleanCPF.charAt(i)) * (10 - i);
  }
  let digit = 11 - (sum % 11);
  if (digit > 9) digit = 0;
  if (digit !== parseInt(cleanCPF.charAt(9))) return false;

  sum = 0;
  for (let i = 0; i < 10; i++) {
    sum += parseInt(cleanCPF.charAt(i)) * (11 - i);
  }
  digit = 11 - (sum % 11);
  if (digit > 9) digit = 0;
  if (digit !== parseInt(cleanCPF.charAt(10))) return false;

  return true;
};

// Validação de CNPJ
export const isValidCNPJ = (cnpj: string): boolean => {
  const cleanCNPJ = cnpj.replace(/[^\d]/g, '');

  if (cleanCNPJ.length !== 14) return false;

  if (/^(\d)\1{13}$/.test(cleanCNPJ)) return false;

  let size = cleanCNPJ.length - 2;
  let numbers = cleanCNPJ.substring(0, size);
  let digits = cleanCNPJ.substring(size);
  let sum = 0;
  let pos = size - 7;

  for (let i = size; i >= 1; i--) {
    sum += parseInt(numbers.charAt(size - i)) * pos--;
    if (pos < 2) pos = 9;
  }

  let result = sum % 11 < 2 ? 0 : 11 - (sum % 11);
  if (result !== parseInt(digits.charAt(0))) return false;

  size += 1;
  numbers = cleanCNPJ.substring(0, size);
  sum = 0;
  pos = size - 7;

  for (let i = size; i >= 1; i--) {
    sum += parseInt(numbers.charAt(size - i)) * pos--;
    if (pos < 2) pos = 9;
  }

  result = sum % 11 < 2 ? 0 : 11 - (sum % 11);
  if (result !== parseInt(digits.charAt(1))) return false;

  return true;
};

// Validação de telefone
export const isValidPhone = (phone: string): boolean => {
  const cleanPhone = phone.replace(/[^\d]/g, '');
  return cleanPhone.length >= 10 && cleanPhone.length <= 11;
};

// Validação de CEP
export const isValidCEP = (cep: string): boolean => {
  const cleanCEP = cep.replace(/[^\d]/g, '');
  return cleanCEP.length === 8;
};

// Tipos de validação
export type ValidationRule = {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  pattern?: RegExp;
  custom?: (value: any) => boolean;
  message: string;
};

export type ValidationRules = {
  [key: string]: ValidationRule[];
};

// Valida um valor com base em uma regra
const validateValue = (value: any, rule: ValidationRule): string | null => {
  if (rule.required && (value === undefined || value === null || value === '')) {
    return rule.message;
  }

  if (value === undefined || value === null || value === '') {
    return null;
  }

  if (rule.minLength !== undefined && String(value).length < rule.minLength) {
    return rule.message;
  }

  if (rule.maxLength !== undefined && String(value).length > rule.maxLength) {
    return rule.message;
  }

  if (rule.min !== undefined && Number(value) < rule.min) {
    return rule.message;
  }

  if (rule.max !== undefined && Number(value) > rule.max) {
    return rule.message;
  }

  if (rule.pattern !== undefined && !rule.pattern.test(String(value))) {
    return rule.message;
  }

  if (rule.custom !== undefined && !rule.custom(value)) {
    return rule.message;
  }

  return null;
};

// Valida um objeto com base em regras
export const validate = (data: Record<string, any>, rules: ValidationRules): Record<string, string[]> => {
  const errors: Record<string, string[]> = {};

  Object.keys(rules).forEach(field => {
    const fieldRules = rules[field];
    const fieldErrors: string[] = [];

    fieldRules.forEach(rule => {
      const error = validateValue(data[field], rule);
      if (error) {
        fieldErrors.push(error);
      }
    });

    if (fieldErrors.length > 0) {
      errors[field] = fieldErrors;
    }
  });

  return errors;
};

// Regras de validação comuns
export const commonRules = {
  required: (message: string = 'Este campo é obrigatório'): ValidationRule => ({
    required: true,
    message,
  }),

  minLength: (length: number, message: string = `Mínimo de ${length} caracteres`): ValidationRule => ({
    minLength: length,
    message,
  }),

  maxLength: (length: number, message: string = `Máximo de ${length} caracteres`): ValidationRule => ({
    maxLength: length,
    message,
  }),

  min: (value: number, message: string = `Valor mínimo: ${value}`): ValidationRule => ({
    min: value,
    message,
  }),

  max: (value: number, message: string = `Valor máximo: ${value}`): ValidationRule => ({
    max: value,
    message,
  }),

  email: (message: string = 'Email inválido'): ValidationRule => ({
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message,
  }),

  cpf: (message: string = 'CPF inválido'): ValidationRule => ({
    pattern: /^\d{3}\.\d{3}\.\d{3}-\d{2}$/,
    message,
  }),

  cnpj: (message: string = 'CNPJ inválido'): ValidationRule => ({
    pattern: /^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/,
    message,
  }),

  phone: (message: string = 'Telefone inválido'): ValidationRule => ({
    pattern: /^\(\d{2}\) \d{4,5}-\d{4}$/,
    message,
  }),

  cep: (message: string = 'CEP inválido'): ValidationRule => ({
    pattern: /^\d{5}-\d{3}$/,
    message,
  }),

  url: (message: string = 'URL inválida'): ValidationRule => ({
    pattern: /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/,
    message,
  }),

  numeric: (message: string = 'Apenas números são permitidos'): ValidationRule => ({
    pattern: /^\d+$/,
    message,
  }),

  alpha: (message: string = 'Apenas letras são permitidas'): ValidationRule => ({
    pattern: /^[a-zA-Z]+$/,
    message,
  }),

  alphanumeric: (message: string = 'Apenas letras e números são permitidos'): ValidationRule => ({
    pattern: /^[a-zA-Z0-9]+$/,
    message,
  }),

  custom: (validator: (value: any) => boolean, message: string): ValidationRule => ({
    custom: validator,
    message,
  }),
};

// Regras de validação
export const rules = {
  required: (value: any): boolean => {
    if (value === null || value === undefined) return false;
    if (typeof value === 'string') return value.trim().length > 0;
    if (Array.isArray(value)) return value.length > 0;
    return true;
  },

  email: (value: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value);
  },

  minLength: (value: string | any[], min: number): boolean => {
    return value.length >= min;
  },

  maxLength: (value: string | any[], max: number): boolean => {
    return value.length <= max;
  },

  min: (value: number, min: number): boolean => {
    return value >= min;
  },

  max: (value: number, max: number): boolean => {
    return value <= max;
  },

  pattern: (value: string, pattern: RegExp): boolean => {
    return pattern.test(value);
  },

  url: (value: string): boolean => {
    try {
      new URL(value);
      return true;
    } catch {
      return false;
    }
  },

  numeric: (value: string): boolean => {
    return /^\d+$/.test(value);
  },

  alpha: (value: string): boolean => {
    return /^[a-zA-Z]+$/.test(value);
  },

  alphanumeric: (value: string): boolean => {
    return /^[a-zA-Z0-9]+$/.test(value);
  },

  cpf: (value: string): boolean => {
    const clean = value.replace(/[^\d]/g, '');
    if (clean.length !== 11) return false;

    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1{10}$/.test(clean)) return false;

    // Validação do primeiro dígito verificador
    let sum = 0;
    for (let i = 0; i < 9; i++) {
      sum += parseInt(clean.charAt(i)) * (10 - i);
    }
    let digit = 11 - (sum % 11);
    if (digit > 9) digit = 0;
    if (digit !== parseInt(clean.charAt(9))) return false;

    // Validação do segundo dígito verificador
    sum = 0;
    for (let i = 0; i < 10; i++) {
      sum += parseInt(clean.charAt(i)) * (11 - i);
    }
    digit = 11 - (sum % 11);
    if (digit > 9) digit = 0;
    if (digit !== parseInt(clean.charAt(10))) return false;

    return true;
  },

  cnpj: (value: string): boolean => {
    const clean = value.replace(/[^\d]/g, '');
    if (clean.length !== 14) return false;

    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1{13}$/.test(clean)) return false;

    // Validação do primeiro dígito verificador
    let size = clean.length - 2;
    let numbers = clean.substring(0, size);
    let digits = clean.substring(size);
    let sum = 0;
    let pos = size - 7;

    for (let i = size; i >= 1; i--) {
      sum += parseInt(numbers.charAt(size - i)) * pos--;
      if (pos < 2) pos = 9;
    }

    let result = sum % 11 < 2 ? 0 : 11 - (sum % 11);
    if (result !== parseInt(digits.charAt(0))) return false;

    // Validação do segundo dígito verificador
    size += 1;
    numbers = clean.substring(0, size);
    sum = 0;
    pos = size - 7;

    for (let i = size; i >= 1; i--) {
      sum += parseInt(numbers.charAt(size - i)) * pos--;
      if (pos < 2) pos = 9;
    }

    result = sum % 11 < 2 ? 0 : 11 - (sum % 11);
    if (result !== parseInt(digits.charAt(1))) return false;

    return true;
  },

  phone: (value: string): boolean => {
    const clean = value.replace(/[^\d]/g, '');
    return clean.length === 10 || clean.length === 11;
  },

  cep: (value: string): boolean => {
    const clean = value.replace(/[^\d]/g, '');
    return clean.length === 8;
  },

  date: (value: string): boolean => {
    const date = new Date(value);
    return date instanceof Date && !isNaN(date.getTime());
  },

  minDate: (value: string, min: string): boolean => {
    const date = new Date(value);
    const minDate = new Date(min);
    return date >= minDate;
  },

  maxDate: (value: string, max: string): boolean => {
    const date = new Date(value);
    const maxDate = new Date(max);
    return date <= maxDate;
  },

  fileSize: (file: File, maxSize: number): boolean => {
    return file.size <= maxSize;
  },

  fileType: (file: File, types: string[]): boolean => {
    return types.includes(file.type);
  },

  password: (value: string): boolean => {
    // Mínimo 8 caracteres, pelo menos uma letra maiúscula, uma minúscula e um número
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
    return passwordRegex.test(value);
  },

  match: (value: any, matchValue: any): boolean => {
    return value === matchValue;
  },

  custom: (value: any, validator: (value: any) => boolean): boolean => {
    return validator(value);
  }
};

// Mensagens de erro padrão
export const messages = {
  required: 'Este campo é obrigatório',
  email: 'Email inválido',
  minLength: (min: number) => `Mínimo de ${min} caracteres`,
  maxLength: (max: number) => `Máximo de ${max} caracteres`,
  min: (min: number) => `Valor mínimo é ${min}`,
  max: (max: number) => `Valor máximo é ${max}`,
  pattern: 'Formato inválido',
  url: 'URL inválida',
  numeric: 'Apenas números são permitidos',
  alpha: 'Apenas letras são permitidas',
  alphanumeric: 'Apenas letras e números são permitidos',
  cpf: 'CPF inválido',
  cnpj: 'CNPJ inválido',
  phone: 'Telefone inválido',
  cep: 'CEP inválido',
  date: 'Data inválida',
  minDate: (min: string) => `Data mínima é ${min}`,
  maxDate: (max: string) => `Data máxima é ${max}`,
  fileSize: (maxSize: number) => `Tamanho máximo do arquivo é ${maxSize} bytes`,
  fileType: (types: string[]) => `Tipos permitidos: ${types.join(', ')}`,
  password: 'Senha deve ter no mínimo 8 caracteres, uma letra maiúscula, uma minúscula e um número',
  match: 'Os valores não conferem',
  custom: 'Valor inválido'
};

// Valida um valor com base em uma regra
export const validate = (value: any, rule: keyof typeof rules, ...args: any[]): boolean => {
  return rules[rule](value, ...args);
};

// Valida um valor com base em múltiplas regras
export const validateAll = (value: any, rules: Array<{ rule: keyof typeof rules; args?: any[] }>): boolean => {
  return rules.every(({ rule, args = [] }) => validate(value, rule, ...args));
};

// Obtém a mensagem de erro para uma regra
export const getErrorMessage = (rule: keyof typeof rules, ...args: any[]): string => {
  return typeof messages[rule] === 'function' ? messages[rule](...args) : messages[rule];
};

// Valida um formulário inteiro
export const validateForm = (values: Record<string, any>, validations: Record<string, Array<{ rule: keyof typeof rules; args?: any[] }>>): Record<string, string[]> => {
  const errors: Record<string, string[]> = {};

  Object.entries(validations).forEach(([field, fieldRules]) => {
    const fieldErrors: string[] = [];
    fieldRules.forEach(({ rule, args = [] }) => {
      if (!validate(values[field], rule, ...args)) {
        fieldErrors.push(getErrorMessage(rule, ...args));
      }
    });
    if (fieldErrors.length > 0) {
      errors[field] = fieldErrors;
    }
  });

  return errors;
}; 