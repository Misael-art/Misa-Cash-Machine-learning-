import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Grid,
  InputAdornment,
  FormHelperText,
  Typography
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { Budget } from '../../types/Budget';
import dayjs from 'dayjs';

interface BudgetFormProps {
  budget?: Budget;
  onSubmit: (budget: Omit<Budget, 'id' | 'spent'>) => void;
  onCancel: () => void;
  categories: string[];
  isSubmitting?: boolean;
}

const emptyBudget = {
  name: '',
  category: '',
  amount: 0,
  period: 'monthly',
  startDate: new Date().toISOString(),
  endDate: new Date(new Date().setMonth(new Date().getMonth() + 1)).toISOString(),
};

const BudgetForm: React.FC<BudgetFormProps> = ({
  budget,
  onSubmit,
  onCancel,
  categories,
  isSubmitting = false
}) => {
  const [formData, setFormData] = useState(budget || emptyBudget);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [customPeriod, setCustomPeriod] = useState(formData.period === 'custom');

  useEffect(() => {
    if (budget) {
      setFormData(budget);
      setCustomPeriod(budget.period === 'custom');
    }
  }, [budget]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>) => {
    const { name, value } = e.target;
    if (!name) return;

    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Limpa o erro quando o usuário começa a digitar
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleDateChange = (field: 'startDate' | 'endDate') => (date: dayjs.Dayjs | null) => {
    if (date) {
      setFormData(prev => ({
        ...prev,
        [field]: date.toISOString()
      }));
      
      if (errors[field]) {
        setErrors(prev => ({ ...prev, [field]: '' }));
      }
    }
  };

  const handlePeriodChange = (e: React.ChangeEvent<{ name?: string; value: unknown }>) => {
    const value = e.target.value as string;
    setCustomPeriod(value === 'custom');
    
    let updatedFormData = {
      ...formData,
      period: value
    };
    
    // Ajusta as datas de acordo com o período selecionado
    if (value !== 'custom') {
      const startDate = new Date();
      let endDate = new Date();
      
      switch (value) {
        case 'monthly':
          endDate = new Date(startDate);
          endDate.setMonth(startDate.getMonth() + 1);
          break;
        case 'quarterly':
          endDate = new Date(startDate);
          endDate.setMonth(startDate.getMonth() + 3);
          break;
        case 'annual':
          endDate = new Date(startDate);
          endDate.setFullYear(startDate.getFullYear() + 1);
          break;
      }
      
      updatedFormData = {
        ...updatedFormData,
        startDate: startDate.toISOString(),
        endDate: endDate.toISOString()
      };
    }
    
    setFormData(updatedFormData);
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    }
    
    if (!formData.category) {
      newErrors.category = 'Categoria é obrigatória';
    }
    
    if (!formData.amount || formData.amount <= 0) {
      newErrors.amount = 'Valor deve ser maior que zero';
    }
    
    if (customPeriod) {
      const start = new Date(formData.startDate);
      const end = new Date(formData.endDate);
      
      if (start >= end) {
        newErrors.endDate = 'Data final deve ser posterior à data inicial';
      }
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validate()) {
      const budgetData = { ...formData };
      delete (budgetData as any).id;
      delete (budgetData as any).spent;
      
      onSubmit(budgetData);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6">
            {budget ? 'Editar Orçamento' : 'Novo Orçamento'}
          </Typography>
        </Grid>
        
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Nome"
            name="name"
            value={formData.name}
            onChange={handleChange}
            error={!!errors.name}
            helperText={errors.name}
            disabled={isSubmitting}
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <FormControl fullWidth error={!!errors.category}>
            <InputLabel>Categoria</InputLabel>
            <Select
              name="category"
              value={formData.category}
              onChange={handleChange}
              label="Categoria"
              disabled={isSubmitting}
            >
              {categories.map(category => (
                <MenuItem key={category} value={category}>
                  {category}
                </MenuItem>
              ))}
            </Select>
            {errors.category && <FormHelperText>{errors.category}</FormHelperText>}
          </FormControl>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Valor"
            name="amount"
            type="number"
            value={formData.amount || ''}
            onChange={handleChange}
            InputProps={{
              startAdornment: <InputAdornment position="start">R$</InputAdornment>,
            }}
            error={!!errors.amount}
            helperText={errors.amount}
            disabled={isSubmitting}
          />
        </Grid>
        
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Período</InputLabel>
            <Select
              name="period"
              value={formData.period}
              onChange={handlePeriodChange}
              label="Período"
              disabled={isSubmitting}
            >
              <MenuItem value="monthly">Mensal</MenuItem>
              <MenuItem value="quarterly">Trimestral</MenuItem>
              <MenuItem value="annual">Anual</MenuItem>
              <MenuItem value="custom">Personalizado</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        {customPeriod && (
          <>
            <Grid item xs={12} md={6}>
              <DatePicker
                label="Data inicial"
                value={dayjs(formData.startDate)}
                onChange={handleDateChange('startDate')}
                disabled={isSubmitting}
                slotProps={{
                  textField: {
                    fullWidth: true,
                    error: !!errors.startDate,
                    helperText: errors.startDate
                  }
                }}
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <DatePicker
                label="Data final"
                value={dayjs(formData.endDate)}
                onChange={handleDateChange('endDate')}
                disabled={isSubmitting}
                slotProps={{
                  textField: {
                    fullWidth: true,
                    error: !!errors.endDate,
                    helperText: errors.endDate
                  }
                }}
              />
            </Grid>
          </>
        )}
        
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 2 }}>
            <Button
              variant="outlined"
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Salvando...' : 'Salvar'}
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BudgetForm; 