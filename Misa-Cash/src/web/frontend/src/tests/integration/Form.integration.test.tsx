import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Form from '../../components/Form';
import Input from '../../components/Input';
import Button from '../../components/Button';
import Alert from '../../components/Alert';

describe('Form Integration', () => {
  const mockSubmit = jest.fn();

  beforeEach(() => {
    mockSubmit.mockClear();
  });

  it('integra corretamente Form com Input e Button', async () => {
    render(
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
    );

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

  it('integra corretamente Form com Alert para exibir erros', async () => {
    const validate = (values: any) => {
      const errors: any = {};
      if (!values.email) {
        errors.email = 'Email é obrigatório';
      }
      if (!values.password) {
        errors.password = 'Senha é obrigatória';
      }
      return errors;
    };

    render(
      <Form onSubmit={mockSubmit} validate={validate}>
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
    );

    fireEvent.click(screen.getByText('Entrar'));

    await waitFor(() => {
      expect(screen.getByText('Email é obrigatório')).toBeInTheDocument();
      expect(screen.getByText('Senha é obrigatória')).toBeInTheDocument();
    });
  });

  it('integra corretamente Form com Alert para exibir sucesso', async () => {
    render(
      <Form
        onSubmit={async () => {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          return { success: true };
        }}
        successMessage="Login realizado com sucesso!"
      >
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
    );

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'usuario@exemplo.com' },
    });
    fireEvent.change(screen.getByLabelText('Senha'), {
      target: { value: 'senha123' },
    });
    fireEvent.click(screen.getByText('Entrar'));

    await waitFor(() => {
      expect(screen.getByText('Login realizado com sucesso!')).toBeInTheDocument();
    });
  });

  it('integra corretamente Form com múltiplos campos e validação assíncrona', async () => {
    const asyncValidate = async (values: any) => {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const errors: any = {};
      if (values.email === 'existente@exemplo.com') {
        errors.email = 'Email já cadastrado';
      }
      return errors;
    };

    render(
      <Form onSubmit={mockSubmit} asyncValidate={asyncValidate}>
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
        <Input
          name="password"
          label="Senha"
          type="password"
          placeholder="Digite sua senha"
        />
        <Input
          name="confirmPassword"
          label="Confirmar Senha"
          type="password"
          placeholder="Confirme sua senha"
        />
        <Button type="submit">Cadastrar</Button>
      </Form>
    );

    fireEvent.change(screen.getByLabelText('Nome'), {
      target: { value: 'João Silva' },
    });
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'existente@exemplo.com' },
    });
    fireEvent.change(screen.getByLabelText('Senha'), {
      target: { value: 'senha123' },
    });
    fireEvent.change(screen.getByLabelText('Confirmar Senha'), {
      target: { value: 'senha123' },
    });
    fireEvent.click(screen.getByText('Cadastrar'));

    await waitFor(() => {
      expect(screen.getByText('Email já cadastrado')).toBeInTheDocument();
    });
  });

  it('integra corretamente Form com Input mascarado e validação personalizada', async () => {
    const validate = (values: any) => {
      const errors: any = {};
      if (!values.phone) {
        errors.phone = 'Telefone é obrigatório';
      } else if (!/^\(\d{2}\) \d{5}-\d{4}$/.test(values.phone)) {
        errors.phone = 'Telefone inválido';
      }
      return errors;
    };

    render(
      <Form onSubmit={mockSubmit} validate={validate}>
        <Input
          name="phone"
          label="Telefone"
          mask="(99) 99999-9999"
          placeholder="Digite seu telefone"
        />
        <Button type="submit">Enviar</Button>
      </Form>
    );

    fireEvent.change(screen.getByLabelText('Telefone'), {
      target: { value: '1234567890' },
    });
    fireEvent.click(screen.getByText('Enviar'));

    await waitFor(() => {
      expect(screen.getByText('Telefone inválido')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText('Telefone'), {
      target: { value: '12345678901' },
    });

    expect(screen.getByLabelText('Telefone')).toHaveValue('(12) 34567-8901');
  });

  it('integra corretamente Form com loading state e feedback visual', async () => {
    render(
      <Form
        onSubmit={async () => {
          await new Promise((resolve) => setTimeout(resolve, 1000));
        }}
      >
        <Input
          name="email"
          label="Email"
          type="email"
          placeholder="Digite seu email"
        />
        <Button type="submit" loading={false}>
          Enviar
        </Button>
      </Form>
    );

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'usuario@exemplo.com' },
    });
    fireEvent.click(screen.getByText('Enviar'));

    await waitFor(() => {
      expect(screen.getByRole('button')).toBeDisabled();
      expect(screen.getByRole('status')).toBeInTheDocument();
    });
  });

  it('integra corretamente Form com validação de campo dependente', async () => {
    const validate = (values: any) => {
      const errors: any = {};
      if (values.password !== values.confirmPassword) {
        errors.confirmPassword = 'As senhas não conferem';
      }
      return errors;
    };

    render(
      <Form onSubmit={mockSubmit} validate={validate}>
        <Input
          name="password"
          label="Senha"
          type="password"
          placeholder="Digite sua senha"
        />
        <Input
          name="confirmPassword"
          label="Confirmar Senha"
          type="password"
          placeholder="Confirme sua senha"
        />
        <Button type="submit">Cadastrar</Button>
      </Form>
    );

    fireEvent.change(screen.getByLabelText('Senha'), {
      target: { value: 'senha123' },
    });
    fireEvent.change(screen.getByLabelText('Confirmar Senha'), {
      target: { value: 'senha456' },
    });
    fireEvent.click(screen.getByText('Cadastrar'));

    await waitFor(() => {
      expect(screen.getByText('As senhas não conferem')).toBeInTheDocument();
    });
  });
}); 