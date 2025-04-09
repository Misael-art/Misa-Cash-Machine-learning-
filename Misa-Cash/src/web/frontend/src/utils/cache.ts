// Prefixo para as chaves do cache
const CACHE_PREFIX = '@MisaCash:cache:';

// Interface para os dados do cache
interface CacheData<T> {
  data: T;
  timestamp: number;
  ttl: number;
}

// Obtém uma chave de cache formatada
const getCacheKey = (key: string): string => {
  return `${CACHE_PREFIX}${key}`;
};

// Armazena dados no cache
export const setCache = <T>(key: string, data: T, ttl: number): void => {
  const cacheData: CacheData<T> = {
    data,
    timestamp: Date.now(),
    ttl,
  };

  localStorage.setItem(getCacheKey(key), JSON.stringify(cacheData));
};

// Obtém dados do cache
export const getCache = <T>(key: string): T | null => {
  const cachedData = localStorage.getItem(getCacheKey(key));
  
  if (!cachedData) {
    return null;
  }

  const { data, timestamp, ttl }: CacheData<T> = JSON.parse(cachedData);
  const now = Date.now();

  // Verifica se o cache expirou
  if (now - timestamp > ttl) {
    removeCache(key);
    return null;
  }

  return data;
};

// Remove dados do cache
export const removeCache = (key: string): void => {
  localStorage.removeItem(getCacheKey(key));
};

// Limpa todo o cache
export const clearCache = (): void => {
  Object.keys(localStorage).forEach(key => {
    if (key.startsWith(CACHE_PREFIX)) {
      localStorage.removeItem(key);
    }
  });
};

// Verifica se existem dados em cache
export const hasCache = (key: string): boolean => {
  return getCache(key) !== null;
};

// Obtém o tempo restante do cache
export const getCacheTTL = (key: string): number => {
  const cachedData = localStorage.getItem(getCacheKey(key));
  
  if (!cachedData) {
    return 0;
  }

  const { timestamp, ttl }: CacheData<any> = JSON.parse(cachedData);
  const now = Date.now();
  const remainingTime = ttl - (now - timestamp);

  return Math.max(0, remainingTime);
};

// Atualiza o TTL do cache
export const updateCacheTTL = (key: string, newTTL: number): void => {
  const cachedData = localStorage.getItem(getCacheKey(key));
  
  if (!cachedData) {
    return;
  }

  const { data, ttl }: CacheData<any> = JSON.parse(cachedData);
  setCache(key, data, newTTL);
};

// Obtém todas as chaves do cache
export const getCacheKeys = (): string[] => {
  return Object.keys(localStorage)
    .filter(key => key.startsWith(CACHE_PREFIX))
    .map(key => key.replace(CACHE_PREFIX, ''));
};

// Obtém o tamanho do cache em bytes
export const getCacheSize = (): number => {
  let size = 0;
  
  Object.keys(localStorage).forEach(key => {
    if (key.startsWith(CACHE_PREFIX)) {
      size += localStorage.getItem(key)?.length || 0;
    }
  });

  return size;
};

// Limpa o cache expirado
export const clearExpiredCache = (): void => {
  Object.keys(localStorage).forEach(key => {
    if (key.startsWith(CACHE_PREFIX)) {
      getCache(key.replace(CACHE_PREFIX, ''));
    }
  });
}; 