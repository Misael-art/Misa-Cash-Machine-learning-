import { format, parse, isValid, addDays, addMonths, addYears, differenceInDays, differenceInMonths, differenceInYears, addHours, addMinutes, addSeconds, subDays, subHours, subMinutes, subSeconds, startOfDay, endOfDay, startOfWeek, endOfWeek, startOfMonth, endOfMonth, startOfYear, endOfYear, isSameDay, isSameWeek, isSameMonth, isSameYear, isBefore, isAfter, isBetween, min, max } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Formatos de data comuns
export const dateFormats = {
  short: 'dd/MM/yyyy',
  long: 'dd/MM/yyyy HH:mm:ss',
  time: 'HH:mm:ss',
  monthYear: 'MMMM/yyyy',
  iso: 'yyyy-MM-dd',
  isoDateTime: "yyyy-MM-dd'T'HH:mm:ss.SSSxxx",
} as const;

// Converte uma string para Date
export const parseDate = (dateStr: string, format: string = dateFormats.short): Date | null => {
  const parsedDate = parse(dateStr, format, new Date(), { locale: ptBR });
  return isValid(parsedDate) ? parsedDate : null;
};

// Formata uma data para string
export const formatDate = (date: Date | string, formatStr: string = dateFormats.short): string => {
  const dateObj = typeof date === 'string' ? parseDate(date) : date;
  if (!dateObj) return '';
  return format(dateObj, formatStr, { locale: ptBR });
};

// Adiciona dias a uma data
export const addDaysToDate = (date: Date | string, days: number): Date => {
  const dateObj = typeof date === 'string' ? parseDate(date) : date;
  if (!dateObj) return new Date();
  return addDays(dateObj, days);
};

// Adiciona meses a uma data
export const addMonthsToDate = (date: Date | string, months: number): Date => {
  const dateObj = typeof date === 'string' ? parseDate(date) : date;
  if (!dateObj) return new Date();
  return addMonths(dateObj, months);
};

// Adiciona anos a uma data
export const addYearsToDate = (date: Date | string, years: number): Date => {
  const dateObj = typeof date === 'string' ? parseDate(date) : date;
  if (!dateObj) return new Date();
  return addYears(dateObj, years);
};

// Calcula a diferença em dias entre duas datas
export const getDaysDifference = (date1: Date | string, date2: Date | string): number => {
  const dateObj1 = typeof date1 === 'string' ? parseDate(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? parseDate(date2) : date2;
  if (!dateObj1 || !dateObj2) return 0;
  return differenceInDays(dateObj2, dateObj1);
};

// Calcula a diferença em meses entre duas datas
export const getMonthsDifference = (date1: Date | string, date2: Date | string): number => {
  const dateObj1 = typeof date1 === 'string' ? parseDate(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? parseDate(date2) : date2;
  if (!dateObj1 || !dateObj2) return 0;
  return differenceInMonths(dateObj2, dateObj1);
};

// Calcula a diferença em anos entre duas datas
export const getYearsDifference = (date1: Date | string, date2: Date | string): number => {
  const dateObj1 = typeof date1 === 'string' ? parseDate(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? parseDate(date2) : date2;
  if (!dateObj1 || !dateObj2) return 0;
  return differenceInYears(dateObj2, dateObj1);
};

// Verifica se uma data é válida
export const isValidDate = (date: Date | string): boolean => {
  if (typeof date === 'string') {
    return isValid(parseDate(date));
  }
  return isValid(date);
};

// Obtém o primeiro dia do mês
export const getFirstDayOfMonth = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? parseDate(date) : date;
  if (!dateObj) return new Date();
  return new Date(dateObj.getFullYear(), dateObj.getMonth(), 1);
};

// Obtém o último dia do mês
export const getLastDayOfMonth = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? parseDate(date) : date;
  if (!dateObj) return new Date();
  return new Date(dateObj.getFullYear(), dateObj.getMonth() + 1, 0);
};

// Verifica se uma data está dentro de um intervalo
export const isDateInRange = (date: Date | string, startDate: Date | string, endDate: Date | string): boolean => {
  const dateObj = typeof date === 'string' ? parseDate(date) : date;
  const startObj = typeof startDate === 'string' ? parseDate(startDate) : startDate;
  const endObj = typeof endDate === 'string' ? parseDate(endDate) : endDate;

  if (!dateObj || !startObj || !endObj) return false;

  return dateObj >= startObj && dateObj <= endObj;
};

// Formata uma data para exibição relativa (ex: "há 2 dias")
export const formatRelativeDate = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? parseDate(date) : date;
  if (!dateObj) return '';

  const now = new Date();
  const diffInDays = getDaysDifference(dateObj, now);
  const diffInMonths = getMonthsDifference(dateObj, now);
  const diffInYears = getYearsDifference(dateObj, now);

  if (diffInYears > 0) {
    return `há ${diffInYears} ${diffInYears === 1 ? 'ano' : 'anos'}`;
  }

  if (diffInMonths > 0) {
    return `há ${diffInMonths} ${diffInMonths === 1 ? 'mês' : 'meses'}`;
  }

  if (diffInDays > 0) {
    return `há ${diffInDays} ${diffInDays === 1 ? 'dia' : 'dias'}`;
  }

  return 'hoje';
};

// Formata uma data para o formato brasileiro
export const formatDateBR = (date: Date | string, formatStr: string = 'dd/MM/yyyy'): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return format(dateObj, formatStr, { locale: ptBR });
};

// Formata uma data e hora para o formato brasileiro
export const formatDateTimeBR = (date: Date | string, formatStr: string = 'dd/MM/yyyy HH:mm:ss'): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return format(dateObj, formatStr, { locale: ptBR });
};

// Converte uma string de data no formato brasileiro para um objeto Date
export const parseDateBR = (dateStr: string, formatStr: string = 'dd/MM/yyyy'): Date | null => {
  const parsedDate = parse(dateStr, formatStr, new Date(), { locale: ptBR });
  return isValid(parsedDate) ? parsedDate : null;
};

// Calcula a diferença em horas entre duas datas
export const getHoursDifference = (date1: Date | string, date2: Date | string): number => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return differenceInHours(dateObj2, dateObj1);
};

// Calcula a diferença em minutos entre duas datas
export const getMinutesDifference = (date1: Date | string, date2: Date | string): number => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return differenceInMinutes(dateObj2, dateObj1);
};

// Calcula a diferença em segundos entre duas datas
export const getSecondsDifference = (date1: Date | string, date2: Date | string): number => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return differenceInSeconds(dateObj2, dateObj1);
};

// Adiciona horas a uma data
export const addHoursToDate = (date: Date | string, hours: number): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return addHours(dateObj, hours);
};

// Adiciona minutos a uma data
export const addMinutesToDate = (date: Date | string, minutes: number): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return addMinutes(dateObj, minutes);
};

// Adiciona segundos a uma data
export const addSecondsToDate = (date: Date | string, seconds: number): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return addSeconds(dateObj, seconds);
};

// Subtrai dias de uma data
export const subDaysFromDate = (date: Date | string, days: number): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return subDays(dateObj, days);
};

// Subtrai horas de uma data
export const subHoursFromDate = (date: Date | string, hours: number): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return subHours(dateObj, hours);
};

// Subtrai minutos de uma data
export const subMinutesFromDate = (date: Date | string, minutes: number): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return subMinutes(dateObj, minutes);
};

// Subtrai segundos de uma data
export const subSecondsFromDate = (date: Date | string, seconds: number): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return subSeconds(dateObj, seconds);
};

// Obtém o início do dia
export const getStartOfDay = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return startOfDay(dateObj);
};

// Obtém o fim do dia
export const getEndOfDay = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return endOfDay(dateObj);
};

// Obtém o início da semana
export const getStartOfWeek = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return startOfWeek(dateObj, { locale: ptBR });
};

// Obtém o fim da semana
export const getEndOfWeek = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return endOfWeek(dateObj, { locale: ptBR });
};

// Obtém o início do mês
export const getStartOfMonth = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return startOfMonth(dateObj);
};

// Obtém o fim do mês
export const getEndOfMonth = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return endOfMonth(dateObj);
};

// Obtém o início do ano
export const getStartOfYear = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return startOfYear(dateObj);
};

// Obtém o fim do ano
export const getEndOfYear = (date: Date | string): Date => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return endOfYear(dateObj);
};

// Verifica se duas datas são do mesmo dia
export const isSameDayCheck = (date1: Date | string, date2: Date | string): boolean => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return isSameDay(dateObj1, dateObj2);
};

// Verifica se duas datas são da mesma semana
export const isSameWeekCheck = (date1: Date | string, date2: Date | string): boolean => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return isSameWeek(dateObj1, dateObj2, { locale: ptBR });
};

// Verifica se duas datas são do mesmo mês
export const isSameMonthCheck = (date1: Date | string, date2: Date | string): boolean => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return isSameMonth(dateObj1, dateObj2);
};

// Verifica se duas datas são do mesmo ano
export const isSameYearCheck = (date1: Date | string, date2: Date | string): boolean => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return isSameYear(dateObj1, dateObj2);
};

// Verifica se uma data é anterior a outra
export const isBeforeDate = (date1: Date | string, date2: Date | string): boolean => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return isBefore(dateObj1, dateObj2);
};

// Verifica se uma data é posterior a outra
export const isAfterDate = (date1: Date | string, date2: Date | string): boolean => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return isAfter(dateObj1, dateObj2);
};

// Verifica se uma data está entre duas outras datas
export const isBetweenDates = (date: Date | string, start: Date | string, end: Date | string): boolean => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const startObj = typeof start === 'string' ? new Date(start) : start;
  const endObj = typeof end === 'string' ? new Date(end) : end;
  return isBetween(dateObj, startObj, endObj);
};

// Obtém a data mais antiga entre duas datas
export const getMinDate = (date1: Date | string, date2: Date | string): Date => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return min([dateObj1, dateObj2]);
};

// Obtém a data mais recente entre duas datas
export const getMaxDate = (date1: Date | string, date2: Date | string): Date => {
  const dateObj1 = typeof date1 === 'string' ? new Date(date1) : date1;
  const dateObj2 = typeof date2 === 'string' ? new Date(date2) : date2;
  return max([dateObj1, dateObj2]);
}; 