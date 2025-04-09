// Formata um número como moeda brasileira (R$)
export const formatCurrencyBR = (value: number, decimals: number = 2): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};

// Formata um número como percentual
export const formatPercentage = (value: number, decimals: number = 2): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value / 100);
};

// Formata um número com separadores de milhar
export const formatNumber = (value: number, decimals: number = 2): string => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};

// Arredonda um número para um número específico de casas decimais
export const round = (value: number, decimals: number = 2): number => {
  return Number(Math.round(Number(value + 'e' + decimals)) + 'e-' + decimals);
};

// Arredonda um número para cima
export const ceil = (value: number, decimals: number = 2): number => {
  return Number(Math.ceil(Number(value + 'e' + decimals)) + 'e-' + decimals);
};

// Arredonda um número para baixo
export const floor = (value: number, decimals: number = 2): number => {
  return Number(Math.floor(Number(value + 'e' + decimals)) + 'e-' + decimals);
};

// Verifica se um valor é um número
export const isNumber = (value: any): boolean => {
  return !isNaN(parseFloat(value)) && isFinite(value);
};

// Verifica se um número está dentro de um intervalo
export const isInRange = (value: number, min: number, max: number): boolean => {
  return value >= min && value <= max;
};

// Obtém o valor mínimo entre dois números
export const getMin = (a: number, b: number): number => {
  return Math.min(a, b);
};

// Obtém o valor máximo entre dois números
export const getMax = (a: number, b: number): number => {
  return Math.max(a, b);
};

// Calcula a média de um array de números
export const getAverage = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  return numbers.reduce((a, b) => a + b, 0) / numbers.length;
};

// Calcula a mediana de um array de números
export const getMedian = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  const sorted = [...numbers].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  if (sorted.length % 2 === 0) {
    return (sorted[middle - 1] + sorted[middle]) / 2;
  }
  return sorted[middle];
};

// Calcula o desvio padrão de um array de números
export const getStandardDeviation = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  const mean = getAverage(numbers);
  const squareDiffs = numbers.map(value => {
    const diff = value - mean;
    return diff * diff;
  });
  return Math.sqrt(getAverage(squareDiffs));
};

// Calcula a variância de um array de números
export const getVariance = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  const mean = getAverage(numbers);
  const squareDiffs = numbers.map(value => {
    const diff = value - mean;
    return diff * diff;
  });
  return getAverage(squareDiffs);
};

// Calcula o percentil de um array de números
export const getPercentile = (numbers: number[], percentile: number): number => {
  if (numbers.length === 0) return 0;
  const sorted = [...numbers].sort((a, b) => a - b);
  const index = (percentile / 100) * (sorted.length - 1);
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  const weight = index % 1;
  if (upper === lower) return sorted[index];
  return sorted[lower] * (1 - weight) + sorted[upper] * weight;
};

// Calcula o primeiro quartil de um array de números
export const getFirstQuartile = (numbers: number[]): number => {
  return getPercentile(numbers, 25);
};

// Calcula o terceiro quartil de um array de números
export const getThirdQuartile = (numbers: number[]): number => {
  return getPercentile(numbers, 75);
};

// Calcula o intervalo interquartil de um array de números
export const getInterquartileRange = (numbers: number[]): number => {
  return getThirdQuartile(numbers) - getFirstQuartile(numbers);
};

// Calcula o coeficiente de variação de um array de números
export const getCoefficientOfVariation = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  const mean = getAverage(numbers);
  if (mean === 0) return 0;
  return (getStandardDeviation(numbers) / mean) * 100;
};

// Calcula o erro padrão da média de um array de números
export const getStandardError = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  return getStandardDeviation(numbers) / Math.sqrt(numbers.length);
};

// Calcula o intervalo de confiança de um array de números
export const getConfidenceInterval = (numbers: number[], confidence: number = 0.95): [number, number] => {
  if (numbers.length === 0) return [0, 0];
  const mean = getAverage(numbers);
  const standardError = getStandardError(numbers);
  const zScore = confidence === 0.95 ? 1.96 : confidence === 0.99 ? 2.576 : 1.645;
  const marginOfError = zScore * standardError;
  return [mean - marginOfError, mean + marginOfError];
};

// Calcula a correlação entre dois arrays de números
export const getCorrelation = (x: number[], y: number[]): number => {
  if (x.length !== y.length || x.length === 0) return 0;
  const meanX = getAverage(x);
  const meanY = getAverage(y);
  const numerator = x.reduce((sum, xi, i) => {
    return sum + (xi - meanX) * (y[i] - meanY);
  }, 0);
  const denominator = Math.sqrt(
    x.reduce((sum, xi) => sum + Math.pow(xi - meanX, 2), 0) *
    y.reduce((sum, yi) => sum + Math.pow(yi - meanY, 2), 0)
  );
  return denominator === 0 ? 0 : numerator / denominator;
};

// Calcula a covariância entre dois arrays de números
export const getCovariance = (x: number[], y: number[]): number => {
  if (x.length !== y.length || x.length === 0) return 0;
  const meanX = getAverage(x);
  const meanY = getAverage(y);
  return x.reduce((sum, xi, i) => {
    return sum + (xi - meanX) * (y[i] - meanY);
  }, 0) / x.length;
};

// Calcula a variação percentual entre dois números
export const calculatePercentageChange = (oldValue: number, newValue: number): number => {
  if (oldValue === 0) return 0;
  return ((newValue - oldValue) / oldValue) * 100;
};

// Limita um número a um intervalo
export const clamp = (value: number, min: number, max: number): number => {
  return Math.min(Math.max(value, min), max);
};

// Calcula a média de um array de números
export const calculateAverage = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  return numbers.reduce((a, b) => a + b, 0) / numbers.length;
};

// Calcula o desvio padrão de um array de números
export const calculateStandardDeviation = (numbers: number[]): number => {
  if (numbers.length === 0) return 0;
  const mean = calculateAverage(numbers);
  const squareDiffs = numbers.map(value => {
    const diff = value - mean;
    return diff * diff;
  });
  const avgSquareDiff = calculateAverage(squareDiffs);
  return Math.sqrt(avgSquareDiff);
};

// Formata um número grande com sufixo (K, M, B, T)
export const formatLargeNumber = (value: number): string => {
  const absValue = Math.abs(value);
  if (absValue >= 1e12) return (value / 1e12).toFixed(1) + 'T';
  if (absValue >= 1e9) return (value / 1e9).toFixed(1) + 'B';
  if (absValue >= 1e6) return (value / 1e6).toFixed(1) + 'M';
  if (absValue >= 1e3) return (value / 1e3).toFixed(1) + 'K';
  return value.toString();
}; 