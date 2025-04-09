import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTransactions } from '../../contexts/TransactionContext';
import '../../styles/transactions.css';

// Componentes a serem criados posteriormente
import TransactionFilters from '../../components/transactions/TransactionFilters';
import TransactionTable from '../../components/transactions/TransactionTable';
import TransactionModal from '../../components/transactions/TransactionModal';
import Alert from '../../components/ui/Alert';

// Tipo para o estado do modal
interface ModalState {
  isOpen: boolean;
  mode: 'create' | 'edit' | 'delete' | 'view';
  transactionId?: number;
}

const Transactions: React.FC = () => {
  const navigate = useNavigate();
  const {
    transactions,
    loading,
    error,
    fetchTransactions,
    removeTransaction,
    filters,
    pagination,
    setTransactionFilters,
    resetFilters
  } = useTransactions();

  // Estado para controle do modal
  const [modalState, setModalState] = useState<ModalState>({
    isOpen: false,
    mode: 'create'
  });

  // Estado para mensagens de alerta
  const [alert, setAlert] = useState<{
    show: boolean;
    message: string;
    type: 'success' | 'error' | 'info';
  }>({
    show: false,
    message: '',
    type: 'info'
  });

  // Busca transações ao montar o componente
  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  // Manipuladores de evento
  const handleOpenCreateModal = () => {
    setModalState({
      isOpen: true,
      mode: 'create'
    });
  };

  const handleOpenEditModal = (id: number) => {
    setModalState({
      isOpen: true,
      mode: 'edit',
      transactionId: id
    });
  };

  const handleOpenViewModal = (id: number) => {
    setModalState({
      isOpen: true,
      mode: 'view',
      transactionId: id
    });
  };

  const handleOpenDeleteModal = (id: number) => {
    setModalState({
      isOpen: true,
      mode: 'delete',
      transactionId: id
    });
  };

  const handleCloseModal = () => {
    setModalState(prev => ({
      ...prev,
      isOpen: false
    }));
  };

  const handleDeleteTransaction = async (id: number) => {
    if (!id) return;
    
    const success = await removeTransaction(id);
    
    if (success) {
      setAlert({
        show: true,
        message: 'Transação excluída com sucesso',
        type: 'success'
      });
      
      // Fecha o modal após excluir
      handleCloseModal();
      
      // Recarrega a lista de transações
      fetchTransactions();
    } else {
      setAlert({
        show: true,
        message: 'Erro ao excluir transação',
        type: 'error'
      });
    }
  };

  const handlePageChange = (page: number) => {
    setTransactionFilters({ page });
  };

  const handleFilterChange = (newFilters: any) => {
    // Ao aplicar um novo filtro, voltamos para a primeira página
    setTransactionFilters({ ...newFilters, page: 1 });
  };

  const handleResetFilters = () => {
    resetFilters();
  };

  const handleChangeLimit = (limit: number) => {
    setTransactionFilters({ limit });
  };

  const handleSortChange = (sort: string, order: 'asc' | 'desc') => {
    setTransactionFilters({ sort, order });
  };

  const handleTransactionSuccess = (action: 'create' | 'update') => {
    // Exibe mensagem de sucesso
    setAlert({
      show: true,
      message: action === 'create' 
        ? 'Transação criada com sucesso' 
        : 'Transação atualizada com sucesso',
      type: 'success'
    });
    
    // Fecha o modal
    handleCloseModal();
    
    // Recarrega a lista de transações
    fetchTransactions();
  };

  // Manipulador para fechar o alerta
  const handleCloseAlert = () => {
    setAlert(prev => ({ ...prev, show: false }));
  };

  return (
    <div className="transactions-page">
      <div className="transactions-header">
        <h1>Gerenciar Transações</h1>
        <button 
          className="btn btn-primary" 
          onClick={handleOpenCreateModal}
        >
          Nova Transação
        </button>
      </div>

      {/* Exibe mensagens de alerta */}
      {alert.show && (
        <Alert 
          type={alert.type} 
          message={alert.message} 
          onClose={handleCloseAlert} 
        />
      )}

      {/* Filtros de transações */}
      <TransactionFilters 
        onFilterChange={handleFilterChange}
        onResetFilters={handleResetFilters}
        currentFilters={filters}
      />

      {/* Tabela de transações */}
      <TransactionTable 
        transactions={transactions}
        loading={loading}
        error={error}
        pagination={pagination}
        onPageChange={handlePageChange}
        onEdit={handleOpenEditModal}
        onDelete={handleOpenDeleteModal}
        onView={handleOpenViewModal}
        onLimitChange={handleChangeLimit}
        onSort={handleSortChange}
        currentSort={{ field: filters.sort || 'date', order: filters.order || 'desc' }}
      />

      {/* Modal de transação (criar/editar/visualizar/excluir) */}
      {modalState.isOpen && (
        <TransactionModal 
          isOpen={modalState.isOpen}
          mode={modalState.mode}
          transactionId={modalState.transactionId}
          onClose={handleCloseModal}
          onSuccess={handleTransactionSuccess}
          onDelete={handleDeleteTransaction}
        />
      )}
    </div>
  );
};

export default Transactions; 