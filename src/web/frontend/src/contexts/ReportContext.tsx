import React, { createContext, useContext, useState, ReactNode, useCallback, useEffect } from 'react';
import { Report, ReportFilter } from '../types/Report';
import { reportService } from '../services/reportService';
import { useAuth } from './AuthContext';
import { useToast } from './ToastContext';

interface ReportContextData {
  report: Report | null;
  filter: ReportFilter;
  loading: boolean;
  error: string | null;
  generateReport: (filter: ReportFilter) => Promise<void>;
  updateFilter: (newFilter: Partial<ReportFilter>) => void;
  resetFilter: () => void;
  exportToPDF: () => Promise<void>;
  exportToExcel: () => Promise<void>;
}

const ReportContext = createContext<ReportContextData>({} as ReportContextData);

export const useReport = () => useContext(ReportContext);

interface ReportProviderProps {
  children: ReactNode;
}

export const ReportProvider: React.FC<ReportProviderProps> = ({ children }) => {
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();
  const { addToast } = useToast();

  // Inicializa o filtro com o mês atual
  const today = new Date();
  const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
  
  const [filter, setFilter] = useState<ReportFilter>({
    startDate: firstDayOfMonth.toISOString().split('T')[0],
    endDate: today.toISOString().split('T')[0],
    includeIncome: true,
    includeExpense: true,
    groupBy: 'day'
  });

  const generateReport = useCallback(async (reportFilter: ReportFilter) => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const generatedReport = await reportService.generateReport(reportFilter);
      setReport(generatedReport);
    } catch (err) {
      setError('Erro ao gerar relatório. Tente novamente mais tarde.');
      addToast({
        type: 'error',
        title: 'Erro',
        message: 'Não foi possível gerar o relatório.'
      });
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, addToast]);

  const updateFilter = useCallback((newFilter: Partial<ReportFilter>) => {
    setFilter(prevFilter => ({
      ...prevFilter,
      ...newFilter
    }));
  }, []);

  const resetFilter = useCallback(() => {
    const today = new Date();
    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    
    setFilter({
      startDate: firstDayOfMonth.toISOString().split('T')[0],
      endDate: today.toISOString().split('T')[0],
      includeIncome: true,
      includeExpense: true,
      groupBy: 'day'
    });
  }, []);

  const exportToPDF = useCallback(async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    
    try {
      const blob = await reportService.exportReportPDF(filter);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `relatorio_financeiro_${new Date().toISOString().slice(0, 10)}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      
      addToast({
        type: 'success',
        title: 'Sucesso',
        message: 'Relatório PDF gerado com sucesso!'
      });
    } catch (err) {
      addToast({
        type: 'error',
        title: 'Erro',
        message: 'Erro ao exportar relatório em PDF.'
      });
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, filter, addToast]);

  const exportToExcel = useCallback(async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    
    try {
      const blob = await reportService.exportReportExcel(filter);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `relatorio_financeiro_${new Date().toISOString().slice(0, 10)}.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      
      addToast({
        type: 'success',
        title: 'Sucesso',
        message: 'Relatório Excel gerado com sucesso!'
      });
    } catch (err) {
      addToast({
        type: 'error',
        title: 'Erro',
        message: 'Erro ao exportar relatório em Excel.'
      });
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, filter, addToast]);

  useEffect(() => {
    if (isAuthenticated) {
      generateReport(filter);
    }
  }, [isAuthenticated, filter, generateReport]);

  return (
    <ReportContext.Provider
      value={{
        report,
        filter,
        loading,
        error,
        generateReport,
        updateFilter,
        resetFilter,
        exportToPDF,
        exportToExcel
      }}
    >
      {children}
    </ReportContext.Provider>
  );
}; 