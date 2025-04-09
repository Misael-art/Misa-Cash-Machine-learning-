import { api } from './api';
import { Report, ReportFilter } from '../types/Report';

export const reportService = {
  async generateReport(filter: ReportFilter): Promise<Report> {
    const response = await api.post<Report>('/reports/generate', filter);
    return response.data;
  },

  async getDefaultReport(): Promise<Report> {
    const today = new Date();
    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    
    const filter: ReportFilter = {
      startDate: firstDayOfMonth.toISOString().split('T')[0],
      endDate: today.toISOString().split('T')[0],
      includeIncome: true,
      includeExpense: true,
      groupBy: 'day'
    };
    
    return this.generateReport(filter);
  },

  async getMonthlyReport(year: number, month: number): Promise<Report> {
    const startDate = new Date(year, month - 1, 1);
    const endDate = new Date(year, month, 0); // Último dia do mês
    
    const filter: ReportFilter = {
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0],
      includeIncome: true,
      includeExpense: true,
      groupBy: 'day'
    };
    
    return this.generateReport(filter);
  },

  async getYearlyReport(year: number): Promise<Report> {
    const startDate = new Date(year, 0, 1);
    const endDate = new Date(year, 11, 31);
    
    const filter: ReportFilter = {
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0],
      includeIncome: true,
      includeExpense: true,
      groupBy: 'month'
    };
    
    return this.generateReport(filter);
  },

  async getCategoryReport(filter: ReportFilter): Promise<Report> {
    const updatedFilter = {
      ...filter,
      groupBy: 'category'
    };
    
    return this.generateReport(updatedFilter);
  },

  async exportReportPDF(filter: ReportFilter): Promise<Blob> {
    const response = await api.post('/reports/export/pdf', filter, {
      responseType: 'blob'
    });
    return response.data;
  },

  async exportReportExcel(filter: ReportFilter): Promise<Blob> {
    const response = await api.post('/reports/export/excel', filter, {
      responseType: 'blob'
    });
    return response.data;
  }
}; 