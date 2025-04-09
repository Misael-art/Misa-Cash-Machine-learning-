import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { BrowserRouter } from 'react-router-dom';
import { TransactionProvider } from '../../contexts/TransactionContext';
import { AuthProvider } from '../../contexts/AuthContext';
import Transactions from '../../pages/transactions/Transactions';

// Mock do react-router-dom
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
}));

// Mock para o contexto de transações
jest.mock('../../contexts/TransactionContext', () => {
  const originalModule = jest.requireActual('../../contexts/TransactionContext');
  
  return {
    ...originalModule,
    useTransactions: () => ({
      transactions: [
        {
          id: 1,
          user_id: 1,
          description: 'Salário',
          amount: 3000,
          type: 'income',
          category: 'salário',
          date: '2023-04-01',
          is_recurring: true,
          recurrence_frequency: 'monthly',
          tags: ['trabalho', 'fixo'],
          created_at: '2023-04-01T10:00:00Z',
          updated_at: '2023-04-01T10:00:00Z'
        },
        {
          id: 2,
          user_id: 1,
          description: 'Supermercado',
          amount: 250,
          type: 'expense',
          category: 'alimentação',
          date: '2023-04-03',
          is_recurring: false,
          tags: ['essencial'],
          created_at: '2023-04-03T15:30:00Z',
          updated_at: '2023-04-03T15:30:00Z'
        }
      ],
      loading: false,
      error: null,
      fetchTransactions: jest.fn(),
      removeTransaction: jest.fn().mockResolvedValue(true),
      filters: {
        page: 1,
        limit: 10,
        sort: 'date',
        order: 'desc'
      },
      pagination: {
        page: 1,
        limit: 10,
        total: 2
      },
      setTransactionFilters: jest.fn(),
      resetFilters: jest.fn()
    }),
  };
});

// Mock para o contexto de autenticação
jest.mock('../../contexts/AuthContext', () => {
  const originalModule = jest.requireActual('../../contexts/AuthContext');
  
  return {
    ...originalModule,
    useAuth: () => ({
      currentUser: { id: 1, name: 'Usuário Teste', email: 'teste@exemplo.com' },
      isAuthenticated: true,
    }),
  };
});

const renderTransactionsPage = () => {
  return render(
    <AuthProvider>
      <TransactionProvider>
        <BrowserRouter>
          <Transactions />
        </BrowserRouter>
      </TransactionProvider>
    </AuthProvider>
  );
};

describe('Transactions Page Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renderiza a página de transações com a tabela corretamente', async () => {
    renderTransactionsPage();
    
    // Verificar título da página
    expect(screen.getByText('Gerenciar Transações')).toBeInTheDocument();
    
    // Verificar se a tabela de transações é exibida com os dados corretos
    expect(screen.getByText('Salário')).toBeInTheDocument();
    expect(screen.getByText('Supermercado')).toBeInTheDocument();
    
    // Verificar filtros e botões
    expect(screen.getByPlaceholderText('Buscar transações...')).toBeInTheDocument();
    expect(screen.getByText('Nova Transação')).toBeInTheDocument();
  });

  test('abre modal para nova transação quando o botão é clicado', async () => {
    renderTransactionsPage();
    
    // Clicar no botão de nova transação
    fireEvent.click(screen.getByText('Nova Transação'));
    
    // Verificar se o modal é exibido
    await waitFor(() => {
      expect(screen.getByText('Nova Transação', { selector: 'h2' })).toBeInTheDocument();
    });
    
    // Verificar elementos do formulário
    expect(screen.getByLabelText(/Descrição \*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Valor \*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Tipo \*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Categoria \*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Data \*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Transação recorrente/i)).toBeInTheDocument();
  });

  test('abre modal para editar transação quando o botão de editar é clicado', async () => {
    renderTransactionsPage();
    
    // Encontrar botão de edição na primeira linha
    const editButtons = screen.getAllByTitle('Editar');
    fireEvent.click(editButtons[0]);
    
    // Verificar se o modal é exibido com o título correto
    await waitFor(() => {
      expect(screen.getByText('Editar Transação')).toBeInTheDocument();
    });
  });

  test('abre modal para excluir transação quando o botão de excluir é clicado', async () => {
    renderTransactionsPage();
    
    // Encontrar botão de exclusão na primeira linha
    const deleteButtons = screen.getAllByTitle('Excluir');
    fireEvent.click(deleteButtons[0]);
    
    // Verificar se o modal de confirmação é exibido
    await waitFor(() => {
      expect(screen.getByText('Excluir Transação')).toBeInTheDocument();
      expect(screen.getByText(/Tem certeza que deseja excluir a transação/i)).toBeInTheDocument();
    });
  });

  test('filtra transações quando o usuário utiliza a barra de busca', async () => {
    const { getByPlaceholderText } = renderTransactionsPage();
    
    // Mock do contexto com função de filtragem
    const mockSetFilters = jest.fn();
    jest.spyOn(React, 'useContext').mockImplementation(() => ({
      setTransactionFilters: mockSetFilters,
    }));
    
    // Digitar na barra de busca
    const searchInput = getByPlaceholderText('Buscar transações...');
    fireEvent.change(searchInput, { target: { value: 'Salário' } });
    
    // Clicar no botão de busca
    const searchButton = screen.getByTitle('Buscar');
    fireEvent.click(searchButton);
    
    // Verificar se a função de filtro foi chamada
    await waitFor(() => {
      expect(mockSetFilters).toHaveBeenCalledWith(expect.objectContaining({ 
        search: 'Salário',
        page: 1
      }));
    });
  });

  test('exibe mensagem quando não há transações', async () => {
    // Mock do contexto com lista vazia de transações
    jest.spyOn(React, 'useContext').mockImplementation(() => ({
      transactions: [],
      loading: false,
      error: null,
      fetchTransactions: jest.fn(),
      removeTransaction: jest.fn(),
      filters: { page: 1, limit: 10 },
      pagination: { page: 1, limit: 10, total: 0 },
      setTransactionFilters: jest.fn(),
      resetFilters: jest.fn()
    }));
    
    render(
      <AuthProvider>
        <TransactionProvider>
          <BrowserRouter>
            <Transactions />
          </BrowserRouter>
        </TransactionProvider>
      </AuthProvider>
    );
    
    // Verificar mensagem de lista vazia
    await waitFor(() => {
      expect(screen.getByText('Nenhuma transação encontrada')).toBeInTheDocument();
    });
  });

  // Mais testes podem ser adicionados para outros cenários
}); 