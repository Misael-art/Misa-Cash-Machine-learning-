import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Table from '../../components/Table';
import Button from '../../components/Button';
import Input from '../../components/Input';
import Modal from '../../components/Modal';
import Alert from '../../components/Alert';

const mockData = [
  { id: 1, name: 'João', email: 'joao@exemplo.com', role: 'Admin' },
  { id: 2, name: 'Maria', email: 'maria@exemplo.com', role: 'User' },
  { id: 3, name: 'Pedro', email: 'pedro@exemplo.com', role: 'User' },
];

const mockColumns = [
  { key: 'name', label: 'Nome' },
  { key: 'email', label: 'Email' },
  { key: 'role', label: 'Função' },
];

describe('Table Integration', () => {
  const mockEdit = jest.fn();
  const mockDelete = jest.fn();
  const mockClose = jest.fn();

  beforeEach(() => {
    mockEdit.mockClear();
    mockDelete.mockClear();
    mockClose.mockClear();
  });

  it('integra corretamente Table com Button para ações', async () => {
    render(
      <Table
        data={mockData}
        columns={mockColumns}
        actions={[
          {
            label: 'Editar',
            render: (row) => (
              <Button onClick={() => mockEdit(row)} variant="primary">
                Editar
              </Button>
            ),
          },
          {
            label: 'Excluir',
            render: (row) => (
              <Button onClick={() => mockDelete(row)} variant="danger">
                Excluir
              </Button>
            ),
          },
        ]}
      />
    );

    fireEvent.click(screen.getAllByText('Editar')[0]);
    expect(mockEdit).toHaveBeenCalledWith(mockData[0]);

    fireEvent.click(screen.getAllByText('Excluir')[0]);
    expect(mockDelete).toHaveBeenCalledWith(mockData[0]);
  });

  it('integra corretamente Table com Input para busca', async () => {
    const onSearch = jest.fn();

    render(
      <Table
        data={mockData}
        columns={mockColumns}
        searchable
        onSearch={onSearch}
        searchInput={
          <Input
            placeholder="Buscar..."
            onChange={(e) => onSearch(e.target.value)}
          />
        }
      />
    );

    fireEvent.change(screen.getByPlaceholderText('Buscar...'), {
      target: { value: 'João' },
    });

    expect(onSearch).toHaveBeenCalledWith('João');
  });

  it('integra corretamente Table com Modal para confirmação de exclusão', async () => {
    const [showModal, setShowModal] = React.useState(false);
    const [selectedRow, setSelectedRow] = React.useState(null);

    render(
      <>
        <Table
          data={mockData}
          columns={mockColumns}
          actions={[
            {
              label: 'Excluir',
              render: (row) => (
                <Button
                  onClick={() => {
                    setSelectedRow(row);
                    setShowModal(true);
                  }}
                  variant="danger"
                >
                  Excluir
                </Button>
              ),
            },
          ]}
        />

        <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
          <Alert
            type="warning"
            message="Tem certeza que deseja excluir este item?"
            actions={[
              {
                label: 'Cancelar',
                onClick: () => setShowModal(false),
              },
              {
                label: 'Confirmar',
                onClick: () => {
                  mockDelete(selectedRow);
                  setShowModal(false);
                },
              },
            ]}
          />
        </Modal>
      </>
    );

    fireEvent.click(screen.getAllByText('Excluir')[0]);
    await waitFor(() => {
      expect(screen.getByText('Tem certeza que deseja excluir este item?')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Confirmar'));
    expect(mockDelete).toHaveBeenCalledWith(mockData[0]);
  });

  it('integra corretamente Table com Modal para edição', async () => {
    const [showModal, setShowModal] = React.useState(false);
    const [selectedRow, setSelectedRow] = React.useState(null);

    render(
      <>
        <Table
          data={mockData}
          columns={mockColumns}
          actions={[
            {
              label: 'Editar',
              render: (row) => (
                <Button
                  onClick={() => {
                    setSelectedRow(row);
                    setShowModal(true);
                  }}
                  variant="primary"
                >
                  Editar
                </Button>
              ),
            },
          ]}
        />

        <Modal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          title="Editar Usuário"
        >
          {selectedRow && (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                mockEdit(selectedRow);
                setShowModal(false);
              }}
            >
              <Input
                name="name"
                label="Nome"
                defaultValue={selectedRow.name}
              />
              <Input
                name="email"
                label="Email"
                defaultValue={selectedRow.email}
              />
              <Input
                name="role"
                label="Função"
                defaultValue={selectedRow.role}
              />
              <Button type="submit">Salvar</Button>
            </form>
          )}
        </Modal>
      </>
    );

    fireEvent.click(screen.getAllByText('Editar')[0]);
    await waitFor(() => {
      expect(screen.getByText('Editar Usuário')).toBeInTheDocument();
    });

    expect(screen.getByDisplayValue('João')).toBeInTheDocument();
    expect(screen.getByDisplayValue('joao@exemplo.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Admin')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Salvar'));
    expect(mockEdit).toHaveBeenCalledWith(mockData[0]);
  });

  it('integra corretamente Table com múltiplos componentes para filtragem', async () => {
    const onFilter = jest.fn();

    render(
      <div>
        <div className="filters">
          <Input
            name="name"
            placeholder="Filtrar por nome"
            onChange={(e) => onFilter({ name: e.target.value })}
          />
          <select
            onChange={(e) => onFilter({ role: e.target.value })}
          >
            <option value="">Todas as funções</option>
            <option value="Admin">Admin</option>
            <option value="User">User</option>
          </select>
        </div>

        <Table
          data={mockData}
          columns={mockColumns}
          filters={{
            name: '',
            role: '',
          }}
          onFilter={onFilter}
        />
      </div>
    );

    fireEvent.change(screen.getByPlaceholderText('Filtrar por nome'), {
      target: { value: 'João' },
    });
    expect(onFilter).toHaveBeenCalledWith({ name: 'João' });

    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'Admin' },
    });
    expect(onFilter).toHaveBeenCalledWith({ role: 'Admin' });
  });

  it('integra corretamente Table com Alert para feedback de ações', async () => {
    const [alert, setAlert] = React.useState(null);

    render(
      <>
        <Table
          data={mockData}
          columns={mockColumns}
          actions={[
            {
              label: 'Ativar',
              render: (row) => (
                <Button
                  onClick={() => {
                    setAlert({
                      type: 'success',
                      message: `Usuário ${row.name} ativado com sucesso!`,
                    });
                  }}
                  variant="success"
                >
                  Ativar
                </Button>
              ),
            },
          ]}
        />

        {alert && (
          <Alert
            type={alert.type}
            message={alert.message}
            onClose={() => setAlert(null)}
          />
        )}
      </>
    );

    fireEvent.click(screen.getAllByText('Ativar')[0]);
    expect(screen.getByText('Usuário João ativado com sucesso!')).toBeInTheDocument();
  });
}); 