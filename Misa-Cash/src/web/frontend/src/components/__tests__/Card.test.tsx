import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Card from '../Card';

describe('Card Component', () => {
  it('renderiza corretamente com título', () => {
    render(<Card title="Título do Card" />);
    expect(screen.getByText('Título do Card')).toBeInTheDocument();
  });

  it('renderiza corretamente com conteúdo', () => {
    render(
      <Card>
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card')).toBeInTheDocument();
  });

  it('renderiza corretamente com título e conteúdo', () => {
    render(
      <Card title="Título do Card">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Título do Card')).toBeInTheDocument();
    expect(screen.getByText('Conteúdo do card')).toBeInTheDocument();
  });

  it('renderiza corretamente com footer', () => {
    render(
      <Card footer={<button>Botão no footer</button>}>
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Botão no footer')).toBeInTheDocument();
  });

  it('renderiza corretamente com loading', () => {
    render(
      <Card loading>
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renderiza corretamente com erro', () => {
    render(
      <Card error="Erro ao carregar">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Erro ao carregar')).toBeInTheDocument();
  });

  it('renderiza corretamente com hover', () => {
    render(
      <Card hover>
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('hover:shadow-lg');
  });

  it('renderiza corretamente com padding personalizado', () => {
    render(
      <Card padding="p-8">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('p-8');
  });

  it('renderiza corretamente com background personalizado', () => {
    render(
      <Card background="bg-gray-100">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('bg-gray-100');
  });

  it('renderiza corretamente com borda personalizada', () => {
    render(
      <Card border="border-2 border-blue-500">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('border-2', 'border-blue-500');
  });

  it('renderiza corretamente com sombra personalizada', () => {
    render(
      <Card shadow="shadow-xl">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('shadow-xl');
  });

  it('renderiza corretamente com largura personalizada', () => {
    render(
      <Card width="w-96">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('w-96');
  });

  it('renderiza corretamente com altura personalizada', () => {
    render(
      <Card height="h-64">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('h-64');
  });

  it('renderiza corretamente com overflow personalizado', () => {
    render(
      <Card overflow="overflow-auto">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('overflow-auto');
  });

  it('renderiza corretamente com cursor personalizado', () => {
    render(
      <Card cursor="cursor-pointer">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('cursor-pointer');
  });

  it('renderiza corretamente com transição personalizada', () => {
    render(
      <Card transition="transition-all duration-300">
        <p>Conteúdo do card</p>
      </Card>
    );
    expect(screen.getByText('Conteúdo do card').parentElement).toHaveClass('transition-all', 'duration-300');
  });
}); 