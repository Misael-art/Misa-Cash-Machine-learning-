import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  LinearProgress,
  IconButton,
  Chip,
  Tooltip
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { Budget } from '../../types/Budget';
import { formatCurrency, formatDate } from '../../utils/formatters';

interface BudgetCardProps {
  budget: Budget;
  onEdit: () => void;
  onDelete: () => void;
  progressColor: 'success' | 'warning' | 'error';
}

const BudgetCard: React.FC<BudgetCardProps> = ({
  budget,
  onEdit,
  onDelete,
  progressColor
}) => {
  const { name, category, amount, spent, period, startDate, endDate } = budget;
  const progress = Math.min(Math.round((spent / amount) * 100), 100);
  const remaining = amount - spent;

  const getPeriodLabel = () => {
    switch (period) {
      case 'monthly':
        return 'Mensal';
      case 'quarterly':
        return 'Trimestral';
      case 'annual':
        return 'Anual';
      case 'custom':
        return 'Personalizado';
      default:
        return period;
    }
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {name}
          </Typography>
          <Chip 
            label={category} 
            size="small" 
            color="primary" 
            variant="outlined"
          />
        </Box>

        <Box sx={{ mb: 2 }}>
          <Chip 
            label={getPeriodLabel()} 
            size="small" 
            color="secondary" 
            variant="outlined" 
            sx={{ mr: 1 }}
          />
          {period === 'custom' && (
            <Typography variant="caption" color="text.secondary" display="block">
              {formatDate(startDate)} - {formatDate(endDate)}
            </Typography>
          )}
        </Box>

        <Box sx={{ mb: 1 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <Typography variant="body2" color="text.secondary">
              Gasto
            </Typography>
            <Typography variant="body2">
              {formatCurrency(spent)} de {formatCurrency(amount)}
            </Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={progress} 
            color={progressColor}
            sx={{ mt: 1, height: 8, borderRadius: 4 }}
          />
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Restante:
          </Typography>
          <Typography 
            variant="body1" 
            fontWeight="bold"
            color={remaining < 0 ? 'error.main' : 'success.main'}
          >
            {formatCurrency(remaining)}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
          <Typography variant="body2" color="text.secondary">
            Progresso:
          </Typography>
          <Typography 
            variant="body2"
            color={progress >= 100 ? 'error.main' : progress >= 90 ? 'warning.main' : 'text.primary'}
          >
            {progress}%
          </Typography>
        </Box>
      </CardContent>

      <CardActions sx={{ justifyContent: 'flex-end', p: 1 }}>
        <Tooltip title="Editar">
          <IconButton size="small" color="primary" onClick={onEdit}>
            <EditIcon fontSize="small" />
          </IconButton>
        </Tooltip>
        <Tooltip title="Excluir">
          <IconButton size="small" color="error" onClick={onDelete}>
            <DeleteIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </CardActions>
    </Card>
  );
};

export default BudgetCard; 