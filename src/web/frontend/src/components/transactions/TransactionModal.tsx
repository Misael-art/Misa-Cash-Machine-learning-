import React, { useState, useEffect } from 'react';
import { useTransactions } from '../../contexts/TransactionContext';
import { Transaction } from '../../services/transactions';

interface TransactionModalProps {
  isOpen: boolean;
  mode: 'create' | 'edit' | 'delete' | 'view';
  transactionId?: number;
  onClose: () => void;
  onSuccess: (action: 'create' | 'update') => void;
  onDelete: (id: number) => void;
}

const TransactionModal: React.FC<TransactionModalProps> = ({
  isOpen,
  mode,
  transactionId,
  onClose,
  onSuccess,
  onDelete
}) => {
  const [transaction, setTransaction] = useState<Partial<Transaction>>({
    description: '',
    amount: 0,
    type: 'expense',
    category: '',
    date: new Date().toISOString().split('T')[0],
    is_recurring: false,
    recurrence_frequency: null,
    tags: []
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [tagInput, setTagInput] = useState('');

  // Buscar dados da transação a partir do contexto
  const { 
    fetchTransaction, 
    addTransaction, 
    editTransaction, 
    loading: contextLoading 
  } = useTransactions();

  // Categorias predefinidas
  const categories = [
    'Alimentação',
    'Transporte',
    'Moradia',
    'Saúde',
    'Educação',
    'Entretenimento',
    'Vestuário',
    'Salário',
    'Investimentos',
    'Outros'
  ];

  // Frequências de recorrência
  const frequencies = [
    { value: 'daily', label: 'Diária' },
    { value: 'weekly', label: 'Semanal' },
    { value: 'monthly', label: 'Mensal' },
    { value: 'yearly', label: 'Anual' }
  ];

  // Buscar transação se estiver no modo de edição, visualização ou exclusão
  useEffect(() => {
    const loadTransaction = async () => {
      if (transactionId && (mode === 'edit' || mode === 'view' || mode === 'delete')) {
        setLoading(true);
        const result = await fetchTransaction(transactionId);
        
        if (result) {
          // Formatar a data para o formato 'yyyy-MM-dd'
          const formattedDate = result.date.split('T')[0];
          
          setTransaction({
            ...result,
            date: formattedDate,
            tags: result.tags || []
          });
        }
        
        setLoading(false);
      }
    };

    loadTransaction();
  }, [transactionId, mode, fetchTransaction]);

  // Manipular alterações nos campos do formulário
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    
    // Checkbox
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setTransaction(prev => ({ ...prev, [name]: checked }));
      
      // Se desmarcou o is_recurring, limpar o recurrence_frequency
      if (name === 'is_recurring' && !checked) {
        setTransaction(prev => ({ ...prev, recurrence_frequency: null }));
      }
      return;
    }
    
    // Campos numéricos
    if (type === 'number') {
      setTransaction(prev => ({ ...prev, [name]: parseFloat(value) }));
      return;
    }

    // Outros campos
    setTransaction(prev => ({ ...prev, [name]: value }));
    
    // Limpar erro do campo quando alterado
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  // Adicionar uma tag
  const handleAddTag = () => {
    if (tagInput.trim() && !transaction.tags?.includes(tagInput.trim())) {
      setTransaction(prev => ({
        ...prev,
        tags: [...(prev.tags || []), tagInput.trim()]
      }));
      setTagInput('');
    }
  };

  // Remover uma tag
  const handleRemoveTag = (tag: string) => {
    setTransaction(prev => ({
      ...prev,
      tags: prev.tags?.filter(t => t !== tag) || []
    }));
  };

  // Validar o formulário
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    if (!transaction.description?.trim()) {
      newErrors.description = 'A descrição é obrigatória';
    }
    
    if (transaction.amount === undefined || transaction.amount <= 0) {
      newErrors.amount = 'O valor deve ser maior que zero';
    }
    
    if (!transaction.category?.trim()) {
      newErrors.category = 'A categoria é obrigatória';
    }
    
    if (!transaction.date) {
      newErrors.date = 'A data é obrigatória';
    }
    
    if (transaction.is_recurring && !transaction.recurrence_frequency) {
      newErrors.recurrence_frequency = 'A frequência de recorrência é obrigatória';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Enviar o formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);

    try {
      if (mode === 'create') {
        const newTransaction = {
          ...transaction,
          user_id: 0, // Será substituído pelo backend com o ID do usuário autenticado
          amount: Number(transaction.amount)
        } as Omit<Transaction, 'id' | 'created_at' | 'updated_at'>;
        
        const result = await addTransaction(newTransaction);
        
        if (result) {
          onSuccess('create');
        }
      } else if (mode === 'edit' && transactionId) {
        const updatedTransaction = {
          ...transaction,
          amount: Number(transaction.amount)
        };
        
        const result = await editTransaction(transactionId, updatedTransaction);
        
        if (result) {
          onSuccess('update');
        }
      }
    } catch (error) {
      console.error('Erro ao processar transação:', error);
    } finally {
      setLoading(false);
    }
  };

  // Confirmar exclusão
  const handleConfirmDelete = () => {
    if (transactionId) {
      onDelete(transactionId);
    }
  };

  // Determinar título do modal com base no modo
  const getModalTitle = () => {
    switch (mode) {
      case 'create':
        return 'Nova Transação';
      case 'edit':
        return 'Editar Transação';
      case 'view':
        return 'Detalhes da Transação';
      case 'delete':
        return 'Excluir Transação';
      default:
        return '';
    }
  };

  // Renderizar formulário ou confirmação de exclusão com base no modo
  const renderContent = () => {
    // Se estiver carregando dados, mostrar indicador
    if ((loading || contextLoading) && (mode === 'edit' || mode === 'view' || mode === 'delete')) {
      return (
        <div className="modal-loading">
          <div className="loading-spinner"></div>
          <p>Carregando dados da transação...</p>
        </div>
      );
    }

    // Modal de exclusão
    if (mode === 'delete') {
      return (
        <div className="delete-confirmation">
          <div className="delete-icon">
            <i className="fas fa-exclamation-triangle"></i>
          </div>
          <p>
            Tem certeza que deseja excluir a transação <strong>{transaction.description}</strong>?
          </p>
          <p className="delete-warning">
            Esta ação não pode ser desfeita.
          </p>
          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={onClose}
              disabled={loading}
            >
              Cancelar
            </button>
            <button 
              type="button" 
              className="btn btn-danger" 
              onClick={handleConfirmDelete}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span className="sr-only">Excluindo...</span>
                </>
              ) : 'Excluir Transação'}
            </button>
          </div>
        </div>
      );
    }

    // Formulário para criação, edição ou visualização
    return (
      <form onSubmit={handleSubmit} className="transaction-form">
        <div className="form-group">
          <label htmlFor="description">Descrição *</label>
          <input
            type="text"
            id="description"
            name="description"
            value={transaction.description || ''}
            onChange={handleChange}
            disabled={mode === 'view'}
            className={`form-control ${errors.description ? 'is-invalid' : ''}`}
            placeholder="Descrição da transação"
          />
          {errors.description && (
            <div className="invalid-feedback">{errors.description}</div>
          )}
        </div>

        <div className="form-row">
          <div className="form-group col-md-6">
            <label htmlFor="amount">Valor *</label>
            <input
              type="number"
              id="amount"
              name="amount"
              value={transaction.amount || ''}
              onChange={handleChange}
              disabled={mode === 'view'}
              className={`form-control ${errors.amount ? 'is-invalid' : ''}`}
              min="0.01"
              step="0.01"
              placeholder="0,00"
            />
            {errors.amount && (
              <div className="invalid-feedback">{errors.amount}</div>
            )}
          </div>

          <div className="form-group col-md-6">
            <label htmlFor="type">Tipo *</label>
            <select
              id="type"
              name="type"
              value={transaction.type || 'expense'}
              onChange={handleChange}
              disabled={mode === 'view'}
              className="form-control"
            >
              <option value="income">Receita</option>
              <option value="expense">Despesa</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group col-md-6">
            <label htmlFor="category">Categoria *</label>
            <select
              id="category"
              name="category"
              value={transaction.category || ''}
              onChange={handleChange}
              disabled={mode === 'view'}
              className={`form-control ${errors.category ? 'is-invalid' : ''}`}
            >
              <option value="">Selecione uma categoria</option>
              {categories.map(category => (
                <option key={category} value={category.toLowerCase()}>
                  {category}
                </option>
              ))}
            </select>
            {errors.category && (
              <div className="invalid-feedback">{errors.category}</div>
            )}
          </div>

          <div className="form-group col-md-6">
            <label htmlFor="date">Data *</label>
            <input
              type="date"
              id="date"
              name="date"
              value={transaction.date || ''}
              onChange={handleChange}
              disabled={mode === 'view'}
              className={`form-control ${errors.date ? 'is-invalid' : ''}`}
            />
            {errors.date && (
              <div className="invalid-feedback">{errors.date}</div>
            )}
          </div>
        </div>

        <div className="form-group">
          <div className="form-check">
            <input
              type="checkbox"
              id="is_recurring"
              name="is_recurring"
              checked={transaction.is_recurring || false}
              onChange={handleChange}
              disabled={mode === 'view'}
              className="form-check-input"
            />
            <label htmlFor="is_recurring" className="form-check-label">
              Transação recorrente
            </label>
          </div>
        </div>

        {transaction.is_recurring && (
          <div className="form-group">
            <label htmlFor="recurrence_frequency">Frequência de recorrência *</label>
            <select
              id="recurrence_frequency"
              name="recurrence_frequency"
              value={transaction.recurrence_frequency || ''}
              onChange={handleChange}
              disabled={mode === 'view'}
              className={`form-control ${errors.recurrence_frequency ? 'is-invalid' : ''}`}
            >
              <option value="">Selecione uma frequência</option>
              {frequencies.map(freq => (
                <option key={freq.value} value={freq.value}>
                  {freq.label}
                </option>
              ))}
            </select>
            {errors.recurrence_frequency && (
              <div className="invalid-feedback">{errors.recurrence_frequency}</div>
            )}
          </div>
        )}

        <div className="form-group">
          <label htmlFor="tags">Tags</label>
          <div className="tags-input-container">
            <input
              type="text"
              id="tags"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              disabled={mode === 'view'}
              className="form-control"
              placeholder="Adicionar tag (pressione Enter)"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddTag();
                }
              }}
            />
            <button
              type="button"
              onClick={handleAddTag}
              disabled={mode === 'view'}
              className="btn btn-outline-secondary"
            >
              <i className="fas fa-plus"></i>
            </button>
          </div>
          <div className="tags-container">
            {transaction.tags?.map(tag => (
              <div key={tag} className="tag-badge">
                <span className="tag-text">{tag}</span>
                {mode !== 'view' && (
                  <button
                    type="button"
                    onClick={() => handleRemoveTag(tag)}
                    className="tag-remove"
                  >
                    <i className="fas fa-times"></i>
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="modal-footer">
          <button 
            type="button" 
            className="btn btn-secondary" 
            onClick={onClose}
            disabled={loading}
          >
            {mode === 'view' ? 'Fechar' : 'Cancelar'}
          </button>
          
          {mode !== 'view' && (
            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span className="sr-only">Salvando...</span>
                </>
              ) : mode === 'create' ? 'Criar Transação' : 'Salvar Alterações'}
            </button>
          )}
        </div>
      </form>
    );
  };

  // Se o modal não estiver aberto, não renderizar nada
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <div className="modal-header">
          <h2>{getModalTitle()}</h2>
          <button 
            type="button" 
            className="modal-close" 
            onClick={onClose}
            disabled={loading}
          >
            <i className="fas fa-times"></i>
          </button>
        </div>
        <div className="modal-body">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default TransactionModal; 