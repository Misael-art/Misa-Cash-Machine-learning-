import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { CURRENCY, DATE_FORMATS } from '@/constants';

// Formatação de data
export const formatDate = (date: string | Date, formatStr = DATE_FORMATS.DISPLAY): string => {
  const parsedDate = typeof date === 'string' ? parseISO(date) : date;
  return format(parsedDate, formatStr, { locale: ptBR });
};

// Formatação de moeda
export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: CURRENCY.DECIMAL_PLACES,
    maximumFractionDigits: CURRENCY.DECIMAL_PLACES,
  }).format(value);
};

// Formatação de porcentagem
export const formatPercentage = (value: number, decimals = 2): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value / 100);
};

// Formatação de número
export const formatNumber = (value: number, decimals = 2): string => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};

// Formatação de quantidade
export const formatQuantity = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 8,
  }).format(value);
};

// Formatação de tempo decorrido
export const formatTimeAgo = (date: string | Date): string => {
  const now = new Date();
  const past = typeof date === 'string' ? parseISO(date) : date;
  const diffInSeconds = Math.floor((now.getTime() - past.getTime()) / 1000);

  if (diffInSeconds < 60) {
    return 'agora mesmo';
  }

  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    return `${diffInMinutes} minuto${diffInMinutes > 1 ? 's' : ''} atrás`;
  }

  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return `${diffInHours} hora${diffInHours > 1 ? 's' : ''} atrás`;
  }

  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 30) {
    return `${diffInDays} dia${diffInDays > 1 ? 's' : ''} atrás`;
  }

  return formatDate(date);
};

// Formata um número como moeda brasileira (R$)
export const formatCurrencyBR = (value: number, decimals: number = 2): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};

// Formata um CPF (xxx.xxx.xxx-xx)
export const formatCPF = (value: string): string => {
  const cleanValue = value.replace(/\D/g, '');
  if (cleanValue.length !== 11) return value;
  return cleanValue.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
};

// Formata um CNPJ (xx.xxx.xxx/xxxx-xx)
export const formatCNPJ = (value: string): string => {
  const cleanValue = value.replace(/\D/g, '');
  if (cleanValue.length !== 14) return value;
  return cleanValue.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
};

// Formata um telefone ((xx) xxxxx-xxxx)
export const formatPhone = (value: string): string => {
  const cleanValue = value.replace(/\D/g, '');
  if (cleanValue.length === 11) {
    return cleanValue.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  }
  if (cleanValue.length === 10) {
    return cleanValue.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
  }
  return value;
};

// Formata um CEP (xxxxx-xxx)
export const formatCEP = (value: string): string => {
  const cleanValue = value.replace(/\D/g, '');
  if (cleanValue.length !== 8) return value;
  return cleanValue.replace(/(\d{5})(\d{3})/, '$1-$2');
};

// Formata uma data (dd/mm/yyyy)
export const formatDate = (value: string | Date): string => {
  const date = typeof value === 'string' ? new Date(value) : value;
  return date.toLocaleDateString('pt-BR');
};

// Formata uma data e hora (dd/mm/yyyy HH:mm:ss)
export const formatDateTime = (value: string | Date): string => {
  const date = typeof value === 'string' ? new Date(value) : value;
  return date.toLocaleString('pt-BR');
};

// Formata um tamanho de arquivo
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Formata um tempo em segundos para formato legível
export const formatDuration = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;

  const parts = [];
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (remainingSeconds > 0 || parts.length === 0) parts.push(`${remainingSeconds}s`);

  return parts.join(' ');
};

// Formata um número de cartão de crédito (xxxx xxxx xxxx xxxx)
export const formatCreditCard = (value: string): string => {
  const cleanValue = value.replace(/\D/g, '');
  const groups = cleanValue.match(/.{1,4}/g);
  return groups ? groups.join(' ') : value;
};

// Formata um número de cartão de crédito para exibição parcial (xxxx xxxx xxxx ****)
export const formatCreditCardMasked = (value: string): string => {
  const cleanValue = value.replace(/\D/g, '');
  if (cleanValue.length !== 16) return value;
  return `${cleanValue.slice(0, 12).replace(/.{4}/g, '$& ')}****`;
};

// Formata um nome próprio (primeira letra maiúscula)
export const formatName = (value: string): string => {
  return value
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

// Formata um texto para slug (url-friendly)
export const formatSlug = (value: string): string => {
  return value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)+/g, '');
}; 