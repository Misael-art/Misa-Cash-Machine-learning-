// Debounce: Executa uma função após um delay, cancelando chamadas anteriores
export const debounce = <T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
};

// Throttle: Executa uma função no máximo uma vez por intervalo
export const throttle = <T extends (...args: any[]) => any>(
  fn: T,
  interval: number
): ((...args: Parameters<T>) => void) => {
  let lastExecution = 0;

  return (...args: Parameters<T>) => {
    const now = Date.now();
    if (now - lastExecution >= interval) {
      fn(...args);
      lastExecution = now;
    }
  };
};

// Memoize: Armazena o resultado de uma função para evitar recálculos
export const memoize = <T extends (...args: any[]) => any>(
  fn: T
): ((...args: Parameters<T>) => ReturnType<T>) => {
  const cache = new Map();

  return (...args: Parameters<T>) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};

// Once: Executa uma função apenas uma vez
export const once = <T extends (...args: any[]) => any>(
  fn: T
): ((...args: Parameters<T>) => ReturnType<T> | undefined) => {
  let called = false;
  let result: ReturnType<T>;

  return (...args: Parameters<T>) => {
    if (!called) {
      result = fn(...args);
      called = true;
      return result;
    }
  };
};

// Retry: Tenta executar uma função várias vezes em caso de falha
export const retry = async <T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  delay: number = 1000
): Promise<T> => {
  let lastError: Error;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (attempt < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError!;
};

// Timeout: Executa uma função com um timeout
export const timeout = async <T>(
  fn: () => Promise<T>,
  ms: number
): Promise<T> => {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error('Timeout')), ms);
  });

  return Promise.race([fn(), timeoutPromise]);
};

// Compose: Compõe múltiplas funções em uma única função
export const compose = <T>(...fns: ((arg: T) => T)[]): ((arg: T) => T) => {
  return (arg: T) => fns.reduceRight((result, fn) => fn(result), arg);
};

// Pipe: Executa funções em sequência, passando o resultado de uma para a próxima
export const pipe = <T>(...fns: ((arg: T) => T)[]): ((arg: T) => T) => {
  return (arg: T) => fns.reduce((result, fn) => fn(result), arg);
};

// Curry: Transforma uma função que recebe múltiplos argumentos em uma sequência de funções
export const curry = <T extends (...args: any[]) => any>(
  fn: T,
  arity: number = fn.length
): ((...args: Parameters<T>) => ReturnType<T> | ((...args: Parameters<T>) => ReturnType<T>)) => {
  return (...args: Parameters<T>) => {
    if (args.length >= arity) {
      return fn(...args);
    }
    return (...moreArgs: Parameters<T>) => curry(fn, arity)(...args, ...moreArgs);
  };
};

// Partial: Aplica alguns argumentos a uma função, retornando uma nova função
export const partial = <T extends (...args: any[]) => any>(
  fn: T,
  ...partialArgs: Parameters<T>
): ((...args: Parameters<T>) => ReturnType<T>) => {
  return (...args: Parameters<T>) => fn(...partialArgs, ...args);
};

// Bind: Vincula o contexto this a uma função
export const bind = <T extends (...args: any[]) => any>(
  fn: T,
  thisArg: any,
  ...partialArgs: Parameters<T>
): ((...args: Parameters<T>) => ReturnType<T>) => {
  return fn.bind(thisArg, ...partialArgs);
};

// Delay: Executa uma função após um delay
export const delay = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

// Async: Converte uma função síncrona em assíncrona
export const async = <T extends (...args: any[]) => any>(
  fn: T
): ((...args: Parameters<T>) => Promise<ReturnType<T>>) => {
  return async (...args: Parameters<T>) => {
    return Promise.resolve(fn(...args));
  };
};

// Sync: Converte uma função assíncrona em síncrona
export const sync = <T extends (...args: any[]) => Promise<any>>(
  fn: T
): ((...args: Parameters<T>) => ReturnType<T>) => {
  return (...args: Parameters<T>) => {
    return fn(...args).then(result => result);
  };
};

// Try: Executa uma função e retorna o resultado ou um valor padrão em caso de erro
export const try_ = async <T>(
  fn: () => Promise<T>,
  defaultValue: T
): Promise<T> => {
  try {
    return await fn();
  } catch {
    return defaultValue;
  }
};

// Cria uma função que retorna uma Promise que resolve com o primeiro valor não nulo
export const firstNonNull = <T>(
  promises: Promise<T>[]
): Promise<T> => {
  return new Promise((resolve, reject) => {
    let resolved = false;
    let errors: Error[] = [];

    promises.forEach(promise => {
      promise
        .then(value => {
          if (!resolved && value !== null) {
            resolved = true;
            resolve(value);
          }
        })
        .catch(error => {
          errors.push(error);
          if (errors.length === promises.length) {
            reject(new Error('All promises rejected'));
          }
        });
    });
  });
};

// Cria uma função que retorna uma Promise que resolve com o primeiro valor que satisfaz uma condição
export const firstMatch = <T>(
  promises: Promise<T>[],
  predicate: (value: T) => boolean
): Promise<T> => {
  return new Promise((resolve, reject) => {
    let resolved = false;
    let errors: Error[] = [];

    promises.forEach(promise => {
      promise
        .then(value => {
          if (!resolved && predicate(value)) {
            resolved = true;
            resolve(value);
          }
        })
        .catch(error => {
          errors.push(error);
          if (errors.length === promises.length) {
            reject(new Error('All promises rejected'));
          }
        });
    });
  });
};

// Cria uma função que retorna uma Promise que resolve com um array de resultados em ordem
export const sequence = <T>(
  promises: Promise<T>[]
): Promise<T[]> => {
  return promises.reduce(
    (acc, promise) =>
      acc.then(results =>
        promise.then(result => [...results, result])
      ),
    Promise.resolve([] as T[])
  );
};

// Cria uma função que retorna uma Promise que resolve com um objeto de resultados
export const parallel = <T extends Record<string, Promise<any>>>(
  promises: T
): Promise<{ [K in keyof T]: Awaited<T[K]> }> => {
  const keys = Object.keys(promises);
  const values = Object.values(promises);

  return Promise.all(values).then(results => {
    return keys.reduce(
      (obj, key, index) => {
        obj[key as keyof T] = results[index];
        return obj;
      },
      {} as { [K in keyof T]: Awaited<T[K]> }
    );
  });
}; 