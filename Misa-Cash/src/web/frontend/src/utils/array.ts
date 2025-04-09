// Verifica se um array está vazia
export const isEmpty = <T>(arr: T[]): boolean => {
  return !arr || arr.length === 0;
};

// Verifica se um array contém um valor
export const contains = <T>(arr: T[], value: T): boolean => {
  return arr.includes(value);
};

// Verifica se um array contém todos os valores
export const containsAll = <T>(arr: T[], values: T[]): boolean => {
  return values.every(value => arr.includes(value));
};

// Verifica se um array contém algum dos valores
export const containsAny = <T>(arr: T[], values: T[]): boolean => {
  return values.some(value => arr.includes(value));
};

// Verifica se um array contém valores duplicados
export const hasDuplicates = <T>(arr: T[]): boolean => {
  return new Set(arr).size !== arr.length;
};

// Remove valores duplicados de um array
export const removeDuplicates = <T>(arr: T[]): T[] => {
  return [...new Set(arr)];
};

// Remove valores nulos ou undefined de um array
export const removeNulls = <T>(arr: T[]): T[] => {
  return arr.filter(value => value != null);
};

// Remove valores vazios de um array
export const removeEmpty = <T>(arr: T[]): T[] => {
  return arr.filter(value => {
    if (typeof value === 'string') return value.trim().length > 0;
    if (Array.isArray(value)) return value.length > 0;
    if (typeof value === 'object') return Object.keys(value).length > 0;
    return value != null;
  });
};

// Obtém o primeiro elemento de um array
export const first = <T>(arr: T[]): T | undefined => {
  return arr[0];
};

// Obtém o último elemento de um array
export const last = <T>(arr: T[]): T | undefined => {
  return arr[arr.length - 1];
};

// Obtém o elemento do meio de um array
export const middle = <T>(arr: T[]): T | undefined => {
  if (arr.length === 0) return undefined;
  const middleIndex = Math.floor(arr.length / 2);
  return arr[middleIndex];
};

// Obtém um elemento aleatório de um array
export const random = <T>(arr: T[]): T | undefined => {
  if (arr.length === 0) return undefined;
  const randomIndex = Math.floor(Math.random() * arr.length);
  return arr[randomIndex];
};

// Obtém múltiplos elementos aleatórios de um array
export const randomMultiple = <T>(arr: T[], count: number): T[] => {
  if (arr.length === 0 || count <= 0) return [];
  const shuffled = [...arr].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, Math.min(count, arr.length));
};

// Embaralha um array
export const shuffle = <T>(arr: T[]): T[] => {
  return [...arr].sort(() => 0.5 - Math.random());
};

// Inverte um array
export const reverse = <T>(arr: T[]): T[] => {
  return [...arr].reverse();
};

// Obtém um subarray de um array
export const slice = <T>(arr: T[], start: number, end?: number): T[] => {
  return arr.slice(start, end);
};

// Obtém os primeiros n elementos de um array
export const take = <T>(arr: T[], n: number): T[] => {
  return arr.slice(0, n);
};

// Obtém os últimos n elementos de um array
export const takeLast = <T>(arr: T[], n: number): T[] => {
  return arr.slice(-n);
};

// Remove os primeiros n elementos de um array
export const drop = <T>(arr: T[], n: number): T[] => {
  return arr.slice(n);
};

// Remove os últimos n elementos de um array
export const dropLast = <T>(arr: T[], n: number): T[] => {
  return arr.slice(0, -n);
};

// Agrupa elementos de um array por uma chave
export const groupBy = <T>(arr: T[], key: keyof T): Record<string, T[]> => {
  return arr.reduce((groups, item) => {
    const value = String(item[key]);
    if (!groups[value]) {
      groups[value] = [];
    }
    groups[value].push(item);
    return groups;
  }, {} as Record<string, T[]>);
};

// Agrupa elementos de um array por uma função
export const groupByFn = <T>(arr: T[], fn: (item: T) => string): Record<string, T[]> => {
  return arr.reduce((groups, item) => {
    const key = fn(item);
    if (!groups[key]) {
      groups[key] = [];
    }
    groups[key].push(item);
    return groups;
  }, {} as Record<string, T[]>);
};

// Ordena um array por uma chave
export const sortBy = <T>(arr: T[], key: keyof T, direction: 'asc' | 'desc' = 'asc'): T[] => {
  return [...arr].sort((a, b) => {
    if (direction === 'asc') {
      return a[key] > b[key] ? 1 : -1;
    }
    return a[key] < b[key] ? 1 : -1;
  });
};

// Ordena um array por uma função
export const sortByFn = <T>(arr: T[], fn: (item: T) => any, direction: 'asc' | 'desc' = 'asc'): T[] => {
  return [...arr].sort((a, b) => {
    if (direction === 'asc') {
      return fn(a) > fn(b) ? 1 : -1;
    }
    return fn(a) < fn(b) ? 1 : -1;
  });
};

// Filtra um array por uma condição
export const filter = <T>(arr: T[], predicate: (item: T) => boolean): T[] => {
  return arr.filter(predicate);
};

// Mapeia um array para outro formato
export const map = <T, U>(arr: T[], fn: (item: T) => U): U[] => {
  return arr.map(fn);
};

// Reduz um array a um único valor
export const reduce = <T, U>(arr: T[], fn: (acc: U, item: T) => U, initialValue: U): U => {
  return arr.reduce(fn, initialValue);
};

// Aplica uma função a cada elemento de um array
export const forEach = <T>(arr: T[], fn: (item: T) => void): void => {
  arr.forEach(fn);
};

// Verifica se todos os elementos de um array satisfazem uma condição
export const every = <T>(arr: T[], predicate: (item: T) => boolean): boolean => {
  return arr.every(predicate);
};

// Verifica se algum elemento de um array satisfaz uma condição
export const some = <T>(arr: T[], predicate: (item: T) => boolean): boolean => {
  return arr.some(predicate);
};

// Encontra o primeiro elemento que satisfaz uma condição
export const find = <T>(arr: T[], predicate: (item: T) => boolean): T | undefined => {
  return arr.find(predicate);
};

// Encontra o último elemento que satisfaz uma condição
export const findLast = <T>(arr: T[], predicate: (item: T) => boolean): T | undefined => {
  return [...arr].reverse().find(predicate);
};

// Encontra o índice do primeiro elemento que satisfaz uma condição
export const findIndex = <T>(arr: T[], predicate: (item: T) => boolean): number => {
  return arr.findIndex(predicate);
};

// Encontra o índice do último elemento que satisfaz uma condição
export const findLastIndex = <T>(arr: T[], predicate: (item: T) => boolean): number => {
  return arr.length - 1 - [...arr].reverse().findIndex(predicate);
};

// Concatena múltiplos arrays
export const concat = <T>(...arrays: T[][]): T[] => {
  return arrays.reduce((result, arr) => [...result, ...arr], []);
};

// Aplica uma função a cada elemento de um array e concatena os resultados
export const flatMap = <T, U>(arr: T[], fn: (item: T) => U[]): U[] => {
  return arr.reduce((result, item) => [...result, ...fn(item)], [] as U[]);
};

// Achata um array aninhado
export const flatten = <T>(arr: (T | T[])[]): T[] => {
  return arr.reduce((result, item) => {
    if (Array.isArray(item)) {
      return [...result, ...item];
    }
    return [...result, item];
  }, [] as T[]);
};

// Achata um array aninhado até uma profundidade específica
export const flattenDepth = <T>(arr: any[], depth: number = 1): T[] => {
  if (depth === 0) return arr as T[];
  return arr.reduce((result, item) => {
    if (Array.isArray(item)) {
      return [...result, ...flattenDepth(item, depth - 1)];
    }
    return [...result, item];
  }, [] as T[]);
};

// Divide um array em chunks de tamanho específico
export const chunk = <T>(arr: T[], size: number): T[][] => {
  return arr.reduce((chunks, item, index) => {
    const chunkIndex = Math.floor(index / size);
    if (!chunks[chunkIndex]) {
      chunks[chunkIndex] = [];
    }
    chunks[chunkIndex].push(item);
    return chunks;
  }, [] as T[][]);
};

// Cria um array com valores únicos de duas arrays
export const union = <T>(arr1: T[], arr2: T[]): T[] => {
  return [...new Set([...arr1, ...arr2])];
};

// Cria um array com valores que existem em ambas as arrays
export const intersection = <T>(arr1: T[], arr2: T[]): T[] => {
  return arr1.filter(item => arr2.includes(item));
};

// Cria um array com valores que existem apenas na primeira array
export const difference = <T>(arr1: T[], arr2: T[]): T[] => {
  return arr1.filter(item => !arr2.includes(item));
};

// Cria um array com valores que existem em apenas uma das arrays
export const symmetricDifference = <T>(arr1: T[], arr2: T[]): T[] => {
  return [...difference(arr1, arr2), ...difference(arr2, arr1)];
}; 