import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Modal from '../../components/Modal';
import Form from '../../components/Form';
import Input from '../../components/Input';
import Button from '../../components/Button';
import Alert from '../../components/Alert';

describe('Modal Integration', () => {
  const mockSubmit = jest.fn();
  const mockClose = jest.fn();

  beforeEach(() => {
    mockSubmit.mockClear();
    mockClose.mockClear();
  });

  it('integra corretamente Modal com Form e Input', async () => {
    render(
      <Modal isOpen onClose={mockClose} title="Login">
        <Form onSubmit={mockSubmit}>
          <Input
            name="email"
            label="Email"
            type="email"
            placeholder="Digite seu email"
          />
          <Input
            name="password"
            label="Senha"
            type="password"
            placeholder="Digite sua senha"
          />
          <Button type="submit">Entrar</Button>
        </Form>
      </Modal>
    );

    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Senha')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'usuario@exemplo.com' },
    });
    fireEvent.change(screen.getByLabelText('Senha'), {
      target: { value: 'senha123' },
    });
    fireEvent.click(screen.getByText('Entrar'));

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        email: 'usuario@exemplo.com',
        password: 'senha123',
      });
    });
  });

  it('integra corretamente Modal com Alert para feedback', async () => {
    render(
      <Modal isOpen onClose={mockClose} title="Confirmação">
        <Alert
          type="warning"
          message="Tem certeza que deseja excluir este item?"
          actions={[
            { label: 'Cancelar', onClick: mockClose },
            { label: 'Confirmar', onClick: mockSubmit },
          ]}
        />
      </Modal>
    );

    expect(screen.getByText('Tem certeza que deseja excluir este item?')).toBeInTheDocument();
    
    fireEvent.click(screen.getByText('Confirmar'));
    expect(mockSubmit).toHaveBeenCalled();

    fireEvent.click(screen.getByText('Cancelar'));
    expect(mockClose).toHaveBeenCalled();
  });

  it('integra corretamente Modal com Form e validação', async () => {
    const validate = (values: any) => {
      const errors: any = {};
      if (!values.name) {
        errors.name = 'Nome é obrigatório';
      }
      if (!values.email) {
        errors.email = 'Email é obrigatório';
      }
      return errors;
    };

    render(
      <Modal isOpen onClose={mockClose} title="Cadastro">
        <Form onSubmit={mockSubmit} validate={validate}>
          <Input
            name="name"
            label="Nome"
            type="text"
            placeholder="Digite seu nome"
          />
          <Input
            name="email"
            label="Email"
            type="email"
            placeholder="Digite seu email"
          />
          <Button type="submit">Cadastrar</Button>
        </Form>
      </Modal>
    );

    fireEvent.click(screen.getByText('Cadastrar'));

    await waitFor(() => {
      expect(screen.getByText('Nome é obrigatório')).toBeInTheDocument();
      expect(screen.getByText('Email é obrigatório')).toBeInTheDocument();
    });
  });

  it('integra corretamente Modal com Form e loading state', async () => {
    render(
      <Modal isOpen onClose={mockClose} title="Processando">
        <Form
          onSubmit={async () => {
            await new Promise((resolve) => setTimeout(resolve, 1000));
          }}
        >
          <Input
            name="data"
            label="Dados"
            type="text"
            placeholder="Digite os dados"
          />
          <Button type="submit" loading={false}>
            Processar
          </Button>
        </Form>
      </Modal>
    );

    fireEvent.change(screen.getByLabelText('Dados'), {
      target: { value: 'teste' },
    });
    fireEvent.click(screen.getByText('Processar'));

    await waitFor(() => {
      expect(screen.getByRole('button')).toBeDisabled();
      expect(screen.getByRole('status')).toBeInTheDocument();
    });
  });

  it('integra corretamente Modal com múltiplos componentes e interações', async () => {
    const steps = ['Dados Pessoais', 'Endereço', 'Confirmação'];
    const [currentStep, setCurrentStep] = React.useState(0);

    render(
      <Modal isOpen onClose={mockClose} title="Cadastro em Etapas">
        <div>
          {steps.map((step, index) => (
            <Button
              key={step}
              onClick={() => setCurrentStep(index)}
              variant={currentStep === index ? 'primary' : 'secondary'}
            >
              {step}
            </Button>
          ))}
        </div>

        {currentStep === 0 && (
          <Form onSubmit={() => setCurrentStep(1)}>
            <Input
              name="name"
              label="Nome"
              type="text"
              placeholder="Digite seu nome"
            />
            <Input
              name="email"
              label="Email"
              type="email"
              placeholder="Digite seu email"
            />
            <Button type="submit">Próximo</Button>
          </Form>
        )}

        {currentStep === 1 && (
          <Form onSubmit={() => setCurrentStep(2)}>
            <Input
              name="address"
              label="Endereço"
              type="text"
              placeholder="Digite seu endereço"
            />
            <Input
              name="city"
              label="Cidade"
              type="text"
              placeholder="Digite sua cidade"
            />
            <Button type="submit">Próximo</Button>
          </Form>
        )}

        {currentStep === 2 && (
          <Alert
            type="success"
            message="Confirme seus dados"
            actions={[
              { label: 'Voltar', onClick: () => setCurrentStep(1) },
              { label: 'Confirmar', onClick: mockSubmit },
            ]}
          />
        )}
      </Modal>
    );

    // Teste da navegação entre etapas
    expect(screen.getByText('Dados Pessoais')).toHaveClass('primary');
    
    fireEvent.change(screen.getByLabelText('Nome'), {
      target: { value: 'João Silva' },
    });
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'joao@exemplo.com' },
    });
    fireEvent.click(screen.getByText('Próximo'));

    await waitFor(() => {
      expect(screen.getByText('Endereço')).toHaveClass('primary');
    });

    fireEvent.change(screen.getByLabelText('Endereço'), {
      target: { value: 'Rua Exemplo, 123' },
    });
    fireEvent.change(screen.getByLabelText('Cidade'), {
      target: { value: 'São Paulo' },
    });
    fireEvent.click(screen.getByText('Próximo'));

    await waitFor(() => {
      expect(screen.getByText('Confirmação')).toHaveClass('primary');
      expect(screen.getByText('Confirme seus dados')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Confirmar'));
    expect(mockSubmit).toHaveBeenCalled();
  });
}); 