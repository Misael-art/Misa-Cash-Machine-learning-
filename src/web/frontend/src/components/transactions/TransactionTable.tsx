import React from 'react';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Transaction } from '../../services/transactions';

interface TransactionTableProps {
  transactions: Transaction[];
  loading: boolean;
  error: string | null;
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
  currentSort: {
    field: string;
    order: 'asc' | 'desc';
  };
  onPageChange: (page: number) => void;
  onLimitChange: (limit: number) => void;
  onSort: (field: string, order: 'asc' | 'desc') => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  onView: (id: number) => void;
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
};

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  return format(date, 'dd/MM/yyyy', { locale: ptBR });
};

const TransactionTable: React.FC<TransactionTableProps> = ({
  transactions,
  loading,
  error,
  pagination,
  currentSort,
  onPageChange,
  onLimitChange,
  onSort,
  onEdit,
  onDelete,
  onView
}) => {
  // Cálculo para paginação
  const totalPages = Math.ceil(pagination.total / pagination.limit);
  const startItem = (pagination.page - 1) * pagination.limit + 1;
  const endItem = Math.min(startItem + pagination.limit - 1, pagination.total);

  // Manipulador para alternar ordenação
  const handleSort = (field: string) => {
    const newOrder = currentSort.field === field && currentSort.order === 'asc' ? 'desc' : 'asc';
    onSort(field, newOrder);
  };

  // Renderiza ícone de ordenação
  const renderSortIcon = (field: string) => {
    if (currentSort.field !== field) {
      return <i className="fas fa-sort"></i>;
    }
    
    return currentSort.order === 'asc' 
      ? <i className="fas fa-sort-up"></i> 
      : <i className="fas fa-sort-down"></i>;
  };

  // Renderiza botões de paginação
  const renderPagination = () => {
    // Se não há páginas, não renderiza paginação
    if (totalPages <= 1) return null;

    const pages = [];
    const currentPage = pagination.page;

    // Botão para primeira página
    pages.push(
      <button
        key="first"
        onClick={() => onPageChange(1)}
        disabled={currentPage === 1}
        className="page-btn"
        title="Primeira página"
      >
        <i className="fas fa-angle-double-left"></i>
      </button>
    );

    // Botão para página anterior
    pages.push(
      <button
        key="prev"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="page-btn"
        title="Página anterior"
      >
        <i className="fas fa-angle-left"></i>
      </button>
    );

    // Determina quais páginas mostrar (limitando a 5)
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, startPage + 4);
    
    // Ajusta para mostrar 5 páginas quando possível
    if (endPage - startPage < 4) {
      startPage = Math.max(1, endPage - 4);
    }

    // Botões de páginas
    for (let i = startPage; i <= endPage; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => onPageChange(i)}
          className={`page-btn ${i === currentPage ? 'active' : ''}`}
        >
          {i}
        </button>
      );
    }

    // Botão para próxima página
    pages.push(
      <button
        key="next"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="page-btn"
        title="Próxima página"
      >
        <i className="fas fa-angle-right"></i>
      </button>
    );

    // Botão para última página
    pages.push(
      <button
        key="last"
        onClick={() => onPageChange(totalPages)}
        disabled={currentPage === totalPages}
        className="page-btn"
        title="Última página"
      >
        <i className="fas fa-angle-double-right"></i>
      </button>
    );

    return (
      <div className="pagination-container">
        <div className="pagination-buttons">
          {pages}
        </div>
        
        <div className="pagination-info">
          Mostrando {startItem}-{endItem} de {pagination.total} transações
        </div>
        
        <div className="pagination-limit">
          <select 
            value={pagination.limit}
            onChange={(e) => onLimitChange(Number(e.target.value))}
            className="limit-select"
            title="Itens por página"
          >
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
          <span>por página</span>
        </div>
      </div>
    );
  };

  // Se estiver carregando, mostra indicador
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Carregando transações...</p>
      </div>
    );
  }

  // Se houver erro, mostra mensagem
  if (error) {
    return (
      <div className="error-container">
        <i className="fas fa-exclamation-circle error-icon"></i>
        <p>{error}</p>
      </div>
    );
  }

  // Se não houver transações, mostra mensagem
  if (transactions.length === 0) {
    return (
      <div className="empty-state">
        <i className="fas fa-receipt empty-icon"></i>
        <h3>Nenhuma transação encontrada</h3>
        <p>Tente ajustar os filtros ou adicione uma nova transação.</p>
      </div>
    );
  }

  return (
    <div className="transaction-table-container">
      <table className="transaction-table">
        <thead>
          <tr>
            <th 
              onClick={() => handleSort('date')}
              className="sortable"
            >
              <span>Data</span>
              {renderSortIcon('date')}
            </th>
            <th 
              onClick={() => handleSort('description')}
              className="sortable"
            >
              <span>Descrição</span>
              {renderSortIcon('description')}
            </th>
            <th 
              onClick={() => handleSort('category')}
              className="sortable"
            >
              <span>Categoria</span>
              {renderSortIcon('category')}
            </th>
            <th 
              onClick={() => handleSort('amount')}
              className="sortable"
            >
              <span>Valor</span>
              {renderSortIcon('amount')}
            </th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr 
              key={transaction.id}
              className={transaction.type}
            >
              <td>{formatDate(transaction.date)}</td>
              <td className="description-cell">
                <div className="transaction-description">{transaction.description}</div>
                {transaction.is_recurring && (
                  <span className="recurring-badge" title="Transação recorrente">
                    <i className="fas fa-sync-alt"></i>
                  </span>
                )}
              </td>
              <td>
                <span className="category-badge">{transaction.category}</span>
              </td>
              <td className={`amount-cell ${transaction.type}`}>
                {formatCurrency(transaction.amount)}
              </td>
              <td className="actions-cell">
                <button 
                  onClick={() => onView(transaction.id!)}
                  className="action-btn view-btn"
                  title="Visualizar"
                >
                  <i className="fas fa-eye"></i>
                </button>
                <button 
                  onClick={() => onEdit(transaction.id!)}
                  className="action-btn edit-btn"
                  title="Editar"
                >
                  <i className="fas fa-edit"></i>
                </button>
                <button 
                  onClick={() => onDelete(transaction.id!)}
                  className="action-btn delete-btn"
                  title="Excluir"
                >
                  <i className="fas fa-trash-alt"></i>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      {renderPagination()}
    </div>
  );
};

export default TransactionTable; 