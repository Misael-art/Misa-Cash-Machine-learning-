// Configurações da API
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
  },
  STRATEGIES: {
    LIST: '/strategies',
    DETAIL: (id: string) => `/strategies/${id}`,
    CREATE: '/strategies',
    UPDATE: (id: string) => `/strategies/${id}`,
    DELETE: (id: string) => `/strategies/${id}`,
    TOGGLE_STATUS: (id: string) => `/strategies/${id}/toggle-status`,
  },
  BACKTEST: {
    RUN: '/backtest/run',
    RESULTS: '/backtest/results',
    DETAIL: (id: string) => `/backtest/results/${id}`,
  },
  TRADES: {
    LIST: '/trades',
    DETAIL: (id: string) => `/trades/${id}`,
  },
};

// Configurações de paginação
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
};

// Configurações de data
export const DATE_FORMATS = {
  DISPLAY: 'dd/MM/yyyy',
  API: 'yyyy-MM-dd',
  DATETIME: 'dd/MM/yyyy HH:mm:ss',
};

// Configurações de moeda
export const CURRENCY = {
  SYMBOL: 'R$',
  DECIMAL_PLACES: 2,
};

// Configurações de gráficos
export const CHART_COLORS = {
  PRIMARY: '#0ea5e9',
  SECONDARY: '#64748b',
  SUCCESS: '#22c55e',
  DANGER: '#ef4444',
  WARNING: '#f59e0b',
  INFO: '#3b82f6',
};

// Configurações de validação
export const VALIDATION = {
  PASSWORD_MIN_LENGTH: 8,
  USERNAME_MIN_LENGTH: 3,
  USERNAME_MAX_LENGTH: 20,
};

// Configurações de cache
export const CACHE = {
  STRATEGIES_TTL: 5 * 60 * 1000, // 5 minutos
  TRADES_TTL: 1 * 60 * 1000, // 1 minuto
  BACKTEST_RESULTS_TTL: 30 * 60 * 1000, // 30 minutos
};

// Configurações de notificações
export const NOTIFICATIONS = {
  SUCCESS_DURATION: 3000,
  ERROR_DURATION: 5000,
  WARNING_DURATION: 4000,
  INFO_DURATION: 3000,
}; 