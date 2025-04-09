import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Table from '../Table';

const mockData = [
  { id: 1, name: 'João', email: 'joao@example.com', role: 'Admin' },
  { id: 2, name: 'Maria', email: 'maria@example.com', role: 'User' },
  { id: 3, name: 'Pedro', email: 'pedro@example.com', role: 'User' },
];

const mockColumns = [
  { key: 'name', label: 'Nome' },
  { key: 'email', label: 'Email' },
  { key: 'role', label: 'Função' },
];

describe('Table Component', () => {
  it('renderiza corretamente com dados e colunas', () => {
    render(<Table data={mockData} columns={mockColumns} />);
    expect(screen.getByText('João')).toBeInTheDocument();
    expect(screen.getByText('maria@example.com')).toBeInTheDocument();
    expect(screen.getByText('User')).toBeInTheDocument();
  });

  it('renderiza corretamente com título', () => {
    render(<Table title="Lista de Usuários" data={mockData} columns={mockColumns} />);
    expect(screen.getByText('Lista de Usuários')).toBeInTheDocument();
  });

  it('renderiza corretamente com loading', () => {
    render(<Table loading data={mockData} columns={mockColumns} />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renderiza corretamente com erro', () => {
    render(<Table error="Erro ao carregar dados" data={mockData} columns={mockColumns} />);
    expect(screen.getByText('Erro ao carregar dados')).toBeInTheDocument();
  });

  it('renderiza corretamente com paginação', () => {
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        pagination
        totalItems={10}
        itemsPerPage={5}
        currentPage={1}
        onPageChange={() => {}}
      />
    );
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  it('renderiza corretamente com ordenação', () => {
    const onSort = jest.fn();
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        sortable
        onSort={onSort}
      />
    );
    fireEvent.click(screen.getByText('Nome'));
    expect(onSort).toHaveBeenCalledWith('name', 'asc');
  });

  it('renderiza corretamente com seleção', () => {
    const onSelect = jest.fn();
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        selectable
        onSelect={onSelect}
      />
    );
    fireEvent.click(screen.getByRole('checkbox'));
    expect(onSelect).toHaveBeenCalledWith([1]);
  });

  it('renderiza corretamente com ações', () => {
    const onEdit = jest.fn();
    const onDelete = jest.fn();
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        actions={[
          { label: 'Editar', onClick: onEdit },
          { label: 'Excluir', onClick: onDelete },
        ]}
      />
    );
    fireEvent.click(screen.getByText('Editar'));
    expect(onEdit).toHaveBeenCalledWith(mockData[0]);
  });

  it('renderiza corretamente com filtros', () => {
    const onFilter = jest.fn();
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        filters={[
          { key: 'role', label: 'Função', options: ['Admin', 'User'] },
        ]}
        onFilter={onFilter}
      />
    );
    fireEvent.change(screen.getByLabelText('Função'), { target: { value: 'Admin' } });
    expect(onFilter).toHaveBeenCalledWith({ role: 'Admin' });
  });

  it('renderiza corretamente com busca', () => {
    const onSearch = jest.fn();
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        searchable
        onSearch={onSearch}
      />
    );
    fireEvent.change(screen.getByPlaceholderText('Buscar...'), { target: { value: 'João' } });
    expect(onSearch).toHaveBeenCalledWith('João');
  });

  it('renderiza corretamente com exportação', () => {
    const onExport = jest.fn();
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        exportable
        onExport={onExport}
      />
    );
    fireEvent.click(screen.getByText('Exportar'));
    expect(onExport).toHaveBeenCalled();
  });

  it('renderiza corretamente com densidade', () => {
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        density="compact"
      />
    );
    expect(screen.getByRole('table')).toHaveClass('compact');
  });

  it('renderiza corretamente com alinhamento personalizado', () => {
    render(
      <Table
        data={mockData}
        columns={[
          { key: 'name', label: 'Nome', align: 'right' },
          { key: 'email', label: 'Email', align: 'center' },
          { key: 'role', label: 'Função', align: 'left' },
        ]}
      />
    );
    expect(screen.getByText('João').parentElement).toHaveClass('text-right');
    expect(screen.getByText('maria@example.com').parentElement).toHaveClass('text-center');
    expect(screen.getByText('User').parentElement).toHaveClass('text-left');
  });

  it('renderiza corretamente com formatação personalizada', () => {
    render(
      <Table
        data={mockData}
        columns={[
          {
            key: 'name',
            label: 'Nome',
            format: (value) => value.toUpperCase(),
          },
        ]}
      />
    );
    expect(screen.getByText('JOÃO')).toBeInTheDocument();
  });

  it('renderiza corretamente com renderização personalizada', () => {
    render(
      <Table
        data={mockData}
        columns={[
          {
            key: 'role',
            label: 'Função',
            render: (value) => (
              <span className="badge">{value}</span>
            ),
          },
        ]}
      />
    );
    expect(screen.getByText('Admin')).toHaveClass('badge');
  });
}); 