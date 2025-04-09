import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Select from '../../components/Select';
import Form from '../../components/Form';
import Button from '../../components/Button';
import Input from '../../components/Input';
import Alert from '../../components/Alert';

const mockOptions = [
  { value: 'admin', label: 'Administrador' },
  { value: 'user', label: 'Usuário' },
  { value: 'guest', label: 'Convidado' },
];

describe('Select Integration', () => {
  it('integra corretamente Select com Form para validação', async () => {
    const mockSubmit = jest.fn();
    const validate = (values) => {
      const errors = {};
      if (!values.role) {
        errors.role = 'Função é obrigatória';
      }
      return errors;
    };

    render(
      <Form onSubmit={mockSubmit} validate={validate}>
        <Select
          name="role"
          label="Função"
          options={mockOptions}
          placeholder="Selecione uma função"
        />
        <Button type="submit">Salvar</Button>
      </Form>
    );

    fireEvent.click(screen.getByText('Salvar'));
    expect(screen.getByText('Função é obrigatória')).toBeInTheDocument();

    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'admin' },
    });
    fireEvent.click(screen.getByText('Salvar'));
    expect(mockSubmit).toHaveBeenCalledWith({ role: 'admin' });
  });

  it('integra corretamente Select com Input dependente', async () => {
    const [selectedRole, setSelectedRole] = React.useState('');
    const [showCustomField, setShowCustomField] = React.useState(false);

    render(
      <Form>
        <Select
          name="role"
          label="Função"
          options={mockOptions}
          value={selectedRole}
          onChange={(e) => {
            setSelectedRole(e.target.value);
            setShowCustomField(e.target.value === 'admin');
          }}
        />
        {showCustomField && (
          <Input
            name="permissions"
            label="Permissões"
            placeholder="Digite as permissões"
          />
        )}
      </Form>
    );

    expect(screen.queryByLabelText('Permissões')).not.toBeInTheDocument();

    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'admin' },
    });
    expect(screen.getByLabelText('Permissões')).toBeInTheDocument();

    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'user' },
    });
    expect(screen.queryByLabelText('Permissões')).not.toBeInTheDocument();
  });

  it('integra corretamente Select com múltiplos selects dependentes', async () => {
    const departments = [
      { value: 'ti', label: 'TI' },
      { value: 'rh', label: 'RH' },
    ];

    const positions = {
      ti: [
        { value: 'dev', label: 'Desenvolvedor' },
        { value: 'qa', label: 'QA' },
      ],
      rh: [
        { value: 'recruiter', label: 'Recrutador' },
        { value: 'manager', label: 'Gerente' },
      ],
    };

    const [selectedDepartment, setSelectedDepartment] = React.useState('');
    const [selectedPosition, setSelectedPosition] = React.useState('');

    render(
      <Form>
        <Select
          name="department"
          label="Departamento"
          options={departments}
          value={selectedDepartment}
          onChange={(e) => {
            setSelectedDepartment(e.target.value);
            setSelectedPosition('');
          }}
        />
        {selectedDepartment && (
          <Select
            name="position"
            label="Cargo"
            options={positions[selectedDepartment]}
            value={selectedPosition}
            onChange={(e) => setSelectedPosition(e.target.value)}
          />
        )}
      </Form>
    );

    expect(screen.queryByLabelText('Cargo')).not.toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('Departamento'), {
      target: { value: 'ti' },
    });
    expect(screen.getByLabelText('Cargo')).toBeInTheDocument();
    expect(screen.getByText('Desenvolvedor')).toBeInTheDocument();
    expect(screen.getByText('QA')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('Departamento'), {
      target: { value: 'rh' },
    });
    expect(screen.getByText('Recrutador')).toBeInTheDocument();
    expect(screen.getByText('Gerente')).toBeInTheDocument();
  });

  it('integra corretamente Select com busca e filtro', async () => {
    const longOptions = [
      { value: '1', label: 'Opção 1' },
      { value: '2', label: 'Opção 2' },
      { value: '3', label: 'Alternativa 1' },
      { value: '4', label: 'Alternativa 2' },
    ];

    const [filteredOptions, setFilteredOptions] = React.useState(longOptions);
    const [searchTerm, setSearchTerm] = React.useState('');

    render(
      <div>
        <Input
          type="search"
          placeholder="Buscar..."
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setFilteredOptions(
              longOptions.filter(option =>
                option.label.toLowerCase().includes(e.target.value.toLowerCase())
              )
            );
          }}
        />
        <Select
          name="option"
          label="Opção"
          options={filteredOptions}
        />
      </div>
    );

    expect(screen.getAllByRole('option').length).toBe(longOptions.length + 1); // +1 for placeholder

    fireEvent.change(screen.getByPlaceholderText('Buscar...'), {
      target: { value: 'Alternativa' },
    });
    expect(screen.getAllByRole('option').length).toBe(3); // 2 options + placeholder
    expect(screen.getByText('Alternativa 1')).toBeInTheDocument();
    expect(screen.getByText('Alternativa 2')).toBeInTheDocument();
  });

  it('integra corretamente Select com validação assíncrona', async () => {
    const mockValidate = jest.fn().mockImplementation((value) =>
      new Promise((resolve) => {
        setTimeout(() => {
          resolve(value === 'admin' ? 'Esta função requer aprovação' : null);
        }, 500);
      })
    );

    const [error, setError] = React.useState('');
    const [loading, setLoading] = React.useState(false);

    render(
      <>
        <Select
          name="role"
          label="Função"
          options={mockOptions}
          onChange={async (e) => {
            setLoading(true);
            const validationError = await mockValidate(e.target.value);
            setError(validationError);
            setLoading(false);
          }}
        />
        {loading && <div role="status">Validando...</div>}
        {error && <Alert type="warning" message={error} />}
      </>
    );

    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'admin' },
    });

    expect(screen.getByText('Validando...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Esta função requer aprovação')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByRole('combobox'), {
      target: { value: 'user' },
    });

    await waitFor(() => {
      expect(screen.queryByText('Esta função requer aprovação')).not.toBeInTheDocument();
    });
  });
}); 