import React, { useState, useEffect } from 'react';
import { TransactionFilters as FiltersType } from '../../services/transactions';

interface TransactionFiltersProps {
  onFilterChange: (filters: Partial<FiltersType>) => void;
  onResetFilters: () => void;
  currentFilters: FiltersType;
}

const TransactionFilters: React.FC<TransactionFiltersProps> = ({
  onFilterChange,
  onResetFilters,
  currentFilters
}) => {
  const [filters, setFilters] = useState<Partial<FiltersType>>({
    startDate: currentFilters.startDate || '',
    endDate: currentFilters.endDate || '',
    type: currentFilters.type || 'all',
    category: currentFilters.category || '',
    minAmount: currentFilters.minAmount || undefined,
    maxAmount: currentFilters.maxAmount || undefined,
    search: currentFilters.search || ''
  });

  const [showFilters, setShowFilters] = useState(false);

  // Categorias de transações (normalmente viriam de uma API)
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

  // Atualiza os filtros locais quando os filtros atuais mudam
  useEffect(() => {
    setFilters({
      startDate: currentFilters.startDate || '',
      endDate: currentFilters.endDate || '',
      type: currentFilters.type || 'all',
      category: currentFilters.category || '',
      minAmount: currentFilters.minAmount,
      maxAmount: currentFilters.maxAmount,
      search: currentFilters.search || ''
    });
  }, [currentFilters]);

  // Manipulador de alterações nos campos de formulário
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    // Para campos numéricos, armazenamos como números ou undefined
    if (type === 'number') {
      const numValue = value !== '' ? parseFloat(value) : undefined;
      setFilters(prev => ({ ...prev, [name]: numValue }));
    } else {
      setFilters(prev => ({ ...prev, [name]: value }));
    }
  };

  // Manipulador de busca por termo (debounce pode ser adicionado para otimização)
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setFilters(prev => ({ ...prev, search: value }));
  };

  // Aplicar filtros
  const handleApplyFilters = () => {
    onFilterChange(filters);
  };

  // Limpar filtros
  const handleResetFilters = () => {
    onResetFilters();
  };

  // Alternar visualização do painel de filtros avançados
  const toggleFilters = () => {
    setShowFilters(prev => !prev);
  };

  return (
    <div className="transaction-filters">
      {/* Barra de busca sempre visível */}
      <div className="search-bar">
        <input
          type="text"
          name="search"
          placeholder="Buscar transações..."
          value={filters.search || ''}
          onChange={handleSearch}
          className="search-input"
        />
        <button 
          className="btn-search" 
          onClick={handleApplyFilters}
          title="Buscar"
        >
          <i className="fas fa-search"></i>
        </button>
        <button 
          className={`btn-filter ${showFilters ? 'active' : ''}`}
          onClick={toggleFilters}
          title="Filtros avançados"
        >
          <i className="fas fa-filter"></i>
        </button>
      </div>

      {/* Filtros avançados colapsáveis */}
      {showFilters && (
        <div className="advanced-filters">
          <div className="filter-row">
            <div className="filter-group">
              <label htmlFor="startDate">Data inicial</label>
              <input
                type="date"
                id="startDate"
                name="startDate"
                value={filters.startDate || ''}
                onChange={handleChange}
              />
            </div>

            <div className="filter-group">
              <label htmlFor="endDate">Data final</label>
              <input
                type="date"
                id="endDate"
                name="endDate"
                value={filters.endDate || ''}
                onChange={handleChange}
              />
            </div>

            <div className="filter-group">
              <label htmlFor="type">Tipo</label>
              <select
                id="type"
                name="type"
                value={filters.type || 'all'}
                onChange={handleChange}
              >
                <option value="all">Todos</option>
                <option value="income">Receitas</option>
                <option value="expense">Despesas</option>
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="category">Categoria</label>
              <select
                id="category"
                name="category"
                value={filters.category || ''}
                onChange={handleChange}
              >
                <option value="">Todas</option>
                {categories.map(category => (
                  <option key={category} value={category.toLowerCase()}>
                    {category}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="filter-row">
            <div className="filter-group">
              <label htmlFor="minAmount">Valor mínimo</label>
              <input
                type="number"
                id="minAmount"
                name="minAmount"
                min="0"
                step="0.01"
                value={filters.minAmount || ''}
                onChange={handleChange}
                placeholder="R$ 0,00"
              />
            </div>

            <div className="filter-group">
              <label htmlFor="maxAmount">Valor máximo</label>
              <input
                type="number"
                id="maxAmount"
                name="maxAmount"
                min="0"
                step="0.01"
                value={filters.maxAmount || ''}
                onChange={handleChange}
                placeholder="R$ 0,00"
              />
            </div>

            <div className="filter-actions">
              <button 
                className="btn btn-primary"
                onClick={handleApplyFilters}
              >
                Aplicar Filtros
              </button>
              <button 
                className="btn btn-secondary"
                onClick={handleResetFilters}
              >
                Limpar Filtros
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TransactionFilters; 