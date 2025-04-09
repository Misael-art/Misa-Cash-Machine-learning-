// Capitaliza a primeira letra de uma string
export const capitalize = (str: string): string => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

// Capitaliza a primeira letra de cada palavra em uma string
export const capitalizeWords = (str: string): string => {
  if (!str) return '';
  return str.split(' ').map(word => capitalize(word)).join(' ');
};

// Remove acentos de uma string
export const removeAccents = (str: string): string => {
  if (!str) return '';
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
};

// Remove caracteres especiais de uma string
export const removeSpecialChars = (str: string): string => {
  if (!str) return '';
  return str.replace(/[^a-zA-Z0-9]/g, '');
};

// Converte uma string para slug
export const toSlug = (str: string): string => {
  if (!str) return '';
  return removeAccents(str)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
};

// Trunca uma string para um tamanho máximo
export const truncate = (str: string, maxLength: number, suffix: string = '...'): string => {
  if (!str) return '';
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength) + suffix;
};

// Verifica se uma string está vazia
export const isEmpty = (str: string): boolean => {
  return !str || str.trim().length === 0;
};

// Verifica se uma string contém apenas números
export const isNumeric = (str: string): boolean => {
  if (!str) return false;
  return /^\d+$/.test(str);
};

// Verifica se uma string contém apenas letras
export const isAlpha = (str: string): boolean => {
  if (!str) return false;
  return /^[a-zA-Z]+$/.test(str);
};

// Verifica se uma string contém apenas letras e números
export const isAlphanumeric = (str: string): boolean => {
  if (!str) return false;
  return /^[a-zA-Z0-9]+$/.test(str);
};

// Verifica se uma string é um email válido
export const isValidEmail = (str: string): boolean => {
  if (!str) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str);
};

// Verifica se uma string é uma URL válida
export const isValidUrl = (str: string): boolean => {
  if (!str) return false;
  try {
    new URL(str);
    return true;
  } catch {
    return false;
  }
};

// Verifica se uma string é um CPF válido
export const isValidCPF = (str: string): boolean => {
  if (!str) return false;
  const clean = str.replace(/[^\d]/g, '');
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
};

// Verifica se uma string é um CNPJ válido
export const isValidCNPJ = (str: string): boolean => {
  if (!str) return false;
  const clean = str.replace(/[^\d]/g, '');
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
};

// Verifica se uma string é um telefone válido
export const isValidPhone = (str: string): boolean => {
  if (!str) return false;
  const clean = str.replace(/[^\d]/g, '');
  return clean.length === 10 || clean.length === 11;
};

// Verifica se uma string é um CEP válido
export const isValidCEP = (str: string): boolean => {
  if (!str) return false;
  const clean = str.replace(/[^\d]/g, '');
  return clean.length === 8;
};

// Formata um CPF
export const formatCPF = (str: string): string => {
  if (!str) return '';
  const clean = str.replace(/[^\d]/g, '');
  return clean.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
};

// Formata um CNPJ
export const formatCNPJ = (str: string): string => {
  if (!str) return '';
  const clean = str.replace(/[^\d]/g, '');
  return clean.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
};

// Formata um telefone
export const formatPhone = (str: string): string => {
  if (!str) return '';
  const clean = str.replace(/[^\d]/g, '');
  if (clean.length === 11) {
    return clean.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  }
  return clean.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
};

// Formata um CEP
export const formatCEP = (str: string): string => {
  if (!str) return '';
  const clean = str.replace(/[^\d]/g, '');
  return clean.replace(/(\d{5})(\d{3})/, '$1-$2');
};

// Formata um cartão de crédito
export const formatCreditCard = (str: string): string => {
  if (!str) return '';
  const clean = str.replace(/[^\d]/g, '');
  return clean.replace(/(\d{4})(\d{4})(\d{4})(\d{4})/, '$1 $2 $3 $4');
};

// Formata um cartão de crédito mascarado
export const formatCreditCardMasked = (str: string): string => {
  if (!str) return '';
  const clean = str.replace(/[^\d]/g, '');
  return clean.replace(/(\d{4})(\d{4})(\d{4})(\d{4})/, '$1 $2 $3 ****');
};

// Formata um nome
export const formatName = (str: string): string => {
  if (!str) return '';
  return str
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

// Formata um slug
export const formatSlug = (str: string): string => {
  if (!str) return '';
  return removeAccents(str)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}; 