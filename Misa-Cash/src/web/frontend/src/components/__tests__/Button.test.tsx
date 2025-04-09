import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Button from '../Button';

describe('Button Component', () => {
  it('renderiza corretamente com texto', () => {
    render(<Button>Clique aqui</Button>);
    expect(screen.getByText('Clique aqui')).toBeInTheDocument();
  });

  it('renderiza corretamente com variante primária', () => {
    render(<Button variant="primary">Botão Primário</Button>);
    const button = screen.getByText('Botão Primário');
    expect(button).toHaveClass('bg-primary');
  });

  it('renderiza corretamente com variante secundária', () => {
    render(<Button variant="secondary">Botão Secundário</Button>);
    const button = screen.getByText('Botão Secundário');
    expect(button).toHaveClass('bg-secondary');
  });

  it('renderiza corretamente com variante outline', () => {
    render(<Button variant="outline">Botão Outline</Button>);
    const button = screen.getByText('Botão Outline');
    expect(button).toHaveClass('border');
  });

  it('renderiza corretamente com tamanho pequeno', () => {
    render(<Button size="sm">Botão Pequeno</Button>);
    const button = screen.getByText('Botão Pequeno');
    expect(button).toHaveClass('px-2 py-1 text-sm');
  });

  it('renderiza corretamente com tamanho grande', () => {
    render(<Button size="lg">Botão Grande</Button>);
    const button = screen.getByText('Botão Grande');
    expect(button).toHaveClass('px-6 py-3 text-lg');
  });

  it('renderiza corretamente quando desabilitado', () => {
    render(<Button disabled>Botão Desabilitado</Button>);
    const button = screen.getByText('Botão Desabilitado');
    expect(button).toBeDisabled();
    expect(button).toHaveClass('opacity-50 cursor-not-allowed');
  });

  it('chama a função onClick quando clicado', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Botão Clicável</Button>);
    fireEvent.click(screen.getByText('Botão Clicável'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('não chama a função onClick quando desabilitado', () => {
    const handleClick = jest.fn();
    render(<Button disabled onClick={handleClick}>Botão Desabilitado</Button>);
    fireEvent.click(screen.getByText('Botão Desabilitado'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('renderiza corretamente com ícone', () => {
    render(
      <Button>
        <span className="mr-2">+</span>
        Adicionar
      </Button>
    );
    expect(screen.getByText('+')).toBeInTheDocument();
    expect(screen.getByText('Adicionar')).toBeInTheDocument();
  });

  it('renderiza corretamente com loading', () => {
    render(<Button loading>Botão Carregando</Button>);
    expect(screen.getByText('Botão Carregando')).toBeInTheDocument();
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
}); 