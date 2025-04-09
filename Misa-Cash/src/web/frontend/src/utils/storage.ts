// Prefixo para as chaves do localStorage
const STORAGE_PREFIX = '@MisaCash:';

// Obtém uma chave formatada
const getKey = (key: string): string => {
  return `${STORAGE_PREFIX}${key}`;
};

// Armazena um valor no localStorage
export const setItem = <T>(key: string, value: T): void => {
  try {
    const serializedValue = JSON.stringify(value);
    localStorage.setItem(getKey(key), serializedValue);
  } catch (error) {
    console.error('Erro ao armazenar item:', error);
  }
};

// Obtém um valor do localStorage
export const getItem = <T>(key: string, defaultValue: T): T => {
  try {
    const item = localStorage.getItem(getKey(key));
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error('Erro ao obter item:', error);
    return defaultValue;
  }
};

// Remove um valor do localStorage
export const removeItem = (key: string): void => {
  try {
    localStorage.removeItem(getKey(key));
  } catch (error) {
    console.error('Erro ao remover item:', error);
  }
};

// Limpa todo o localStorage
export const clear = (): void => {
  try {
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith(STORAGE_PREFIX)) {
        localStorage.removeItem(key);
      }
    });
  } catch (error) {
    console.error('Erro ao limpar localStorage:', error);
  }
};

// Verifica se existe um valor no localStorage
export const hasItem = (key: string): boolean => {
  try {
    return localStorage.getItem(getKey(key)) !== null;
  } catch (error) {
    console.error('Erro ao verificar item:', error);
    return false;
  }
};

// Obtém todas as chaves do localStorage
export const getKeys = (): string[] => {
  try {
    return Object.keys(localStorage)
      .filter(key => key.startsWith(STORAGE_PREFIX))
      .map(key => key.replace(STORAGE_PREFIX, ''));
  } catch (error) {
    console.error('Erro ao obter chaves:', error);
    return [];
  }
};

// Obtém o tamanho do localStorage em bytes
export const getSize = (): number => {
  try {
    let size = 0;
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith(STORAGE_PREFIX)) {
        size += localStorage.getItem(key)?.length || 0;
      }
    });
    return size;
  } catch (error) {
    console.error('Erro ao obter tamanho:', error);
    return 0;
  }
};

// Obtém todos os itens do localStorage
export const getAllItems = (): Record<string, any> => {
  try {
    const items: Record<string, any> = {};
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith(STORAGE_PREFIX)) {
        const itemKey = key.replace(STORAGE_PREFIX, '');
        items[itemKey] = JSON.parse(localStorage.getItem(key) || '');
      }
    });
    return items;
  } catch (error) {
    console.error('Erro ao obter todos os itens:', error);
    return {};
  }
};

// Armazena múltiplos itens no localStorage
export const setItems = (items: Record<string, any>): void => {
  try {
    Object.entries(items).forEach(([key, value]) => {
      setItem(key, value);
    });
  } catch (error) {
    console.error('Erro ao armazenar múltiplos itens:', error);
  }
};

// Remove múltiplos itens do localStorage
export const removeItems = (keys: string[]): void => {
  try {
    keys.forEach(key => removeItem(key));
  } catch (error) {
    console.error('Erro ao remover múltiplos itens:', error);
  }
};

// Verifica se o localStorage está disponível
export const isAvailable = (): boolean => {
  try {
    const test = 'test';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (error) {
    return false;
  }
};

// Obtém o espaço disponível no localStorage
export const getAvailableSpace = (): number => {
  try {
    const testKey = 'test';
    const testValue = 'a'.repeat(1024); // 1KB
    let availableSpace = 0;

    while (true) {
      try {
        localStorage.setItem(testKey, testValue.repeat(availableSpace + 1));
        availableSpace++;
      } catch {
        break;
      }
    }

    localStorage.removeItem(testKey);
    return availableSpace * 1024; // Retorna em bytes
  } catch (error) {
    console.error('Erro ao obter espaço disponível:', error);
    return 0;
  }
};

// Limpa itens expirados do localStorage
export const clearExpiredItems = (): void => {
  try {
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith(STORAGE_PREFIX)) {
        const item = localStorage.getItem(key);
        if (item) {
          try {
            const { expiresAt } = JSON.parse(item);
            if (expiresAt && Date.now() > expiresAt) {
              localStorage.removeItem(key);
            }
          } catch {
            // Ignora itens que não têm data de expiração
          }
        }
      }
    });
  } catch (error) {
    console.error('Erro ao limpar itens expirados:', error);
  }
}; 