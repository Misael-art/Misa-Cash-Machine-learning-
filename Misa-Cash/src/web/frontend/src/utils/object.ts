// Verifica se um objeto está vazio
export const isEmpty = (obj: object): boolean => {
  return Object.keys(obj).length === 0;
};

// Verifica se um objeto tem uma propriedade específica
export const hasProperty = (obj: object, prop: string): boolean => {
  return Object.prototype.hasOwnProperty.call(obj, prop);
};

// Obtém todas as chaves de um objeto
export const getKeys = <T extends object>(obj: T): (keyof T)[] => {
  return Object.keys(obj) as (keyof T)[];
};

// Obtém todos os valores de um objeto
export const getValues = <T extends object>(obj: T): T[keyof T][] => {
  return Object.values(obj);
};

// Obtém todas as entradas (chave-valor) de um objeto
export const getEntries = <T extends object>(obj: T): [keyof T, T[keyof T]][] => {
  return Object.entries(obj) as [keyof T, T[keyof T]][];
};

// Cria um novo objeto com as propriedades selecionadas
export const pick = <T extends object, K extends keyof T>(
  obj: T,
  keys: K[]
): Pick<T, K> => {
  return keys.reduce((result, key) => {
    if (hasProperty(obj, key as string)) {
      result[key] = obj[key];
    }
    return result;
  }, {} as Pick<T, K>);
};

// Cria um novo objeto sem as propriedades especificadas
export const omit = <T extends object, K extends keyof T>(
  obj: T,
  keys: K[]
): Omit<T, K> => {
  return Object.keys(obj).reduce((result, key) => {
    if (!keys.includes(key as K)) {
      result[key as keyof Omit<T, K>] = obj[key as keyof T];
    }
    return result;
  }, {} as Omit<T, K>);
};

// Cria um novo objeto com as propriedades transformadas
export const mapValues = <T extends object, R>(
  obj: T,
  fn: (value: T[keyof T], key: keyof T) => R
): Record<keyof T, R> => {
  return Object.keys(obj).reduce((result, key) => {
    result[key as keyof T] = fn(obj[key as keyof T], key as keyof T);
    return result;
  }, {} as Record<keyof T, R>);
};

// Cria um novo objeto com as chaves transformadas
export const mapKeys = <T extends object>(
  obj: T,
  fn: (key: keyof T) => string
): Record<string, T[keyof T]> => {
  return Object.keys(obj).reduce((result, key) => {
    result[fn(key as keyof T)] = obj[key as keyof T];
    return result;
  }, {} as Record<string, T[keyof T]>);
};

// Cria um novo objeto com as propriedades invertidas (chave -> valor, valor -> chave)
export const invert = <T extends object>(obj: T): Record<string, keyof T> => {
  return Object.keys(obj).reduce((result, key) => {
    result[String(obj[key as keyof T])] = key as keyof T;
    return result;
  }, {} as Record<string, keyof T>);
};

// Cria um novo objeto com as propriedades ordenadas
export const sortKeys = <T extends object>(obj: T): T => {
  return Object.keys(obj)
    .sort()
    .reduce((result, key) => {
      result[key as keyof T] = obj[key as keyof T];
      return result;
    }, {} as T);
};

// Cria um novo objeto com as propriedades aninhadas achatadas
export const flatten = <T extends object>(
  obj: T,
  prefix = ''
): Record<string, any> => {
  return Object.keys(obj).reduce((result, key) => {
    const value = obj[key as keyof T];
    const newKey = prefix ? `${prefix}.${key}` : key;

    if (value && typeof value === 'object' && !Array.isArray(value)) {
      Object.assign(result, flatten(value as object, newKey));
    } else {
      result[newKey] = value;
    }

    return result;
  }, {} as Record<string, any>);
};

// Cria um novo objeto com as propriedades aninhadas
export const unflatten = (obj: Record<string, any>): Record<string, any> => {
  const result: Record<string, any> = {};

  for (const key in obj) {
    const keys = key.split('.');
    let current = result;

    for (let i = 0; i < keys.length; i++) {
      const k = keys[i];
      if (i === keys.length - 1) {
        current[k] = obj[key];
      } else {
        current[k] = current[k] || {};
        current = current[k];
      }
    }
  }

  return result;
};

// Cria um novo objeto com as propriedades transformadas recursivamente
export const transform = <T extends object, R>(
  obj: T,
  fn: (value: any, key: string) => any
): R => {
  if (Array.isArray(obj)) {
    return obj.map(item => transform(item, fn)) as unknown as R;
  }

  if (obj && typeof obj === 'object') {
    return Object.keys(obj).reduce((result, key) => {
      result[key] = transform(obj[key as keyof T], fn);
      return result;
    }, {} as R);
  }

  return fn(obj, '') as R;
};

// Cria um novo objeto com as propriedades filtradas
export const filter = <T extends object>(
  obj: T,
  predicate: (value: T[keyof T], key: keyof T) => boolean
): Partial<T> => {
  return Object.keys(obj).reduce((result, key) => {
    if (predicate(obj[key as keyof T], key as keyof T)) {
      result[key as keyof T] = obj[key as keyof T];
    }
    return result;
  }, {} as Partial<T>);
};

// Cria um novo objeto com as propriedades transformadas em string
export const stringify = <T extends object>(obj: T): Record<keyof T, string> => {
  return Object.keys(obj).reduce((result, key) => {
    result[key as keyof T] = String(obj[key as keyof T]);
    return result;
  }, {} as Record<keyof T, string>);
};

// Cria um novo objeto com as propriedades transformadas em número
export const numberify = <T extends object>(obj: T): Record<keyof T, number> => {
  return Object.keys(obj).reduce((result, key) => {
    result[key as keyof T] = Number(obj[key as keyof T]);
    return result;
  }, {} as Record<keyof T, number>);
};

// Cria um novo objeto com as propriedades transformadas em boolean
export const booleanify = <T extends object>(obj: T): Record<keyof T, boolean> => {
  return Object.keys(obj).reduce((result, key) => {
    result[key as keyof T] = Boolean(obj[key as keyof T]);
    return result;
  }, {} as Record<keyof T, boolean>);
};

// Mescla dois objetos
export const merge = <T extends object>(obj1: T, obj2: Partial<T>): T => {
  return { ...obj1, ...obj2 };
};

// Cria um objeto a partir de um array de pares chave-valor
export const fromEntries = <T>(entries: [string, T][]): Record<string, T> => {
  return entries.reduce((result, [key, value]) => {
    result[key] = value;
    return result;
  }, {} as Record<string, T>);
};

// Transforma um objeto em um array de pares chave-valor
export const toEntries = <T>(obj: Record<string, T>): [string, T][] => {
  return getEntries(obj);
};

// Cria um objeto com valores padrão para chaves ausentes
export const withDefaults = <T extends object>(obj: Partial<T>, defaults: T): T => {
  return { ...defaults, ...obj };
};

// Verifica se dois objetos são iguais
export const areObjectsEqual = (obj1: object, obj2: object): boolean => {
  const keys1 = getKeys(obj1);
  const keys2 = getKeys(obj2);
  
  if (keys1.length !== keys2.length) return false;
  
  return keys1.every(key => {
    const val1 = obj1[key as keyof typeof obj1];
    const val2 = obj2[key as keyof typeof obj2];
    
    if (typeof val1 === 'object' && typeof val2 === 'object') {
      return areObjectsEqual(val1, val2);
    }
    
    return val1 === val2;
  });
};

// Cria uma cópia profunda de um objeto
export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  
  if (Array.isArray(obj)) {
    return obj.map(item => deepClone(item)) as unknown as T;
  }
  
  return Object.keys(obj).reduce((result, key) => {
    result[key as keyof T] = deepClone(obj[key as keyof T]);
    return result;
  }, {} as T);
}; 