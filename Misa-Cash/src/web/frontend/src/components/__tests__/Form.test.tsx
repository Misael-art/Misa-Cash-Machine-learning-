import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Form from '../Form';

describe('Form Component', () => {
  const mockSubmit = jest.fn();

  beforeEach(() => {
    mockSubmit.mockClear();
  });

  it('renderiza corretamente com campos', () => {
    render(
      <Form onSubmit={mockSubmit}>
        <input type="text" name="name" />
        <input type="email" name="email" />
      </Form>
    );
    expect(screen.getByRole('textbox', { name: 'name' })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: 'email' })).toBeInTheDocument();
  });

  it('renderiza corretamente com título', () => {
    render(
      <Form title="Formulário de Cadastro" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByText('Formulário de Cadastro')).toBeInTheDocument();
  });

  it('renderiza corretamente com descrição', () => {
    render(
      <Form description="Preencha os campos abaixo" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByText('Preencha os campos abaixo')).toBeInTheDocument();
  });

  it('chama onSubmit quando o formulário é enviado', () => {
    render(
      <Form onSubmit={mockSubmit}>
        <input type="text" name="name" defaultValue="João" />
        <button type="submit">Enviar</button>
      </Form>
    );
    fireEvent.click(screen.getByText('Enviar'));
    expect(mockSubmit).toHaveBeenCalledWith({ name: 'João' });
  });

  it('renderiza corretamente com validação', () => {
    const validate = jest.fn().mockReturnValue({ name: 'Nome é obrigatório' });
    render(
      <Form onSubmit={mockSubmit} validate={validate}>
        <input type="text" name="name" />
        <button type="submit">Enviar</button>
      </Form>
    );
    fireEvent.click(screen.getByText('Enviar'));
    expect(screen.getByText('Nome é obrigatório')).toBeInTheDocument();
    expect(mockSubmit).not.toHaveBeenCalled();
  });

  it('renderiza corretamente com loading', () => {
    render(
      <Form loading onSubmit={mockSubmit}>
        <input type="text" name="name" />
        <button type="submit">Enviar</button>
      </Form>
    );
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renderiza corretamente com erro', () => {
    render(
      <Form error="Erro ao enviar formulário" onSubmit={mockSubmit}>
        <input type="text" name="name" />
        <button type="submit">Enviar</button>
      </Form>
    );
    expect(screen.getByText('Erro ao enviar formulário')).toBeInTheDocument();
  });

  it('renderiza corretamente com sucesso', () => {
    render(
      <Form success="Formulário enviado com sucesso" onSubmit={mockSubmit}>
        <input type="text" name="name" />
        <button type="submit">Enviar</button>
      </Form>
    );
    expect(screen.getByText('Formulário enviado com sucesso')).toBeInTheDocument();
  });

  it('renderiza corretamente com layout personalizado', () => {
    render(
      <Form layout="horizontal" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('flex');
  });

  it('renderiza corretamente com tamanho personalizado', () => {
    render(
      <Form size="lg" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox')).toHaveClass('text-lg');
  });

  it('renderiza corretamente com padding personalizado', () => {
    render(
      <Form padding="p-8" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('p-8');
  });

  it('renderiza corretamente com background personalizado', () => {
    render(
      <Form background="bg-gray-100" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('bg-gray-100');
  });

  it('renderiza corretamente com borda personalizada', () => {
    render(
      <Form border="border-2 border-blue-500" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('border-2', 'border-blue-500');
  });

  it('renderiza corretamente com sombra personalizada', () => {
    render(
      <Form shadow="shadow-xl" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('shadow-xl');
  });

  it('renderiza corretamente com largura personalizada', () => {
    render(
      <Form width="w-96" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('w-96');
  });

  it('renderiza corretamente com altura personalizada', () => {
    render(
      <Form height="h-64" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('h-64');
  });

  it('renderiza corretamente com overflow personalizado', () => {
    render(
      <Form overflow="overflow-auto" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('overflow-auto');
  });

  it('renderiza corretamente com cursor personalizado', () => {
    render(
      <Form cursor="cursor-pointer" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('cursor-pointer');
  });

  it('renderiza corretamente com transição personalizada', () => {
    render(
      <Form transition="transition-all duration-300" onSubmit={mockSubmit}>
        <input type="text" name="name" />
      </Form>
    );
    expect(screen.getByRole('textbox').parentElement).toHaveClass('transition-all', 'duration-300');
  });
}); 