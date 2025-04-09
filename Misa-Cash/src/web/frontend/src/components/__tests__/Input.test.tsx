import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Input from '../Input';

describe('Input Component', () => {
  it('renderiza corretamente com placeholder', () => {
    render(<Input placeholder="Digite algo" />);
    expect(screen.getByPlaceholderText('Digite algo')).toBeInTheDocument();
  });

  it('renderiza corretamente com valor inicial', () => {
    render(<Input value="Valor inicial" onChange={() => {}} />);
    expect(screen.getByDisplayValue('Valor inicial')).toBeInTheDocument();
  });

  it('renderiza corretamente com label', () => {
    render(<Input label="Nome" />);
    expect(screen.getByText('Nome')).toBeInTheDocument();
  });

  it('renderiza corretamente com erro', () => {
    render(<Input error="Campo obrigatório" />);
    expect(screen.getByText('Campo obrigatório')).toBeInTheDocument();
    expect(screen.getByRole('textbox')).toHaveClass('border-red-500');
  });

  it('renderiza corretamente quando desabilitado', () => {
    render(<Input disabled />);
    expect(screen.getByRole('textbox')).toBeDisabled();
    expect(screen.getByRole('textbox')).toHaveClass('opacity-50 cursor-not-allowed');
  });

  it('chama a função onChange quando o valor muda', () => {
    const handleChange = jest.fn();
    render(<Input onChange={handleChange} />);
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'Novo valor' } });
    expect(handleChange).toHaveBeenCalled();
  });

  it('renderiza corretamente com máscara', () => {
    render(<Input mask="(99) 99999-9999" />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: '12345678901' } });
    expect(input).toHaveValue('(12) 34567-8901');
  });

  it('renderiza corretamente com ícone', () => {
    render(
      <Input
        icon={<span data-testid="search-icon">🔍</span>}
      />
    );
    expect(screen.getByTestId('search-icon')).toBeInTheDocument();
  });

  it('renderiza corretamente com tipo password', () => {
    render(<Input type="password" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'password');
  });

  it('renderiza corretamente com tipo number', () => {
    render(<Input type="number" />);
    expect(screen.getByRole('spinbutton')).toBeInTheDocument();
  });

  it('renderiza corretamente com tipo email', () => {
    render(<Input type="email" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'email');
  });

  it('renderiza corretamente com tipo tel', () => {
    render(<Input type="tel" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'tel');
  });

  it('renderiza corretamente com tipo date', () => {
    render(<Input type="date" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'date');
  });

  it('renderiza corretamente com tipo time', () => {
    render(<Input type="time" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'time');
  });

  it('renderiza corretamente com tipo datetime-local', () => {
    render(<Input type="datetime-local" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'datetime-local');
  });

  it('renderiza corretamente com tipo search', () => {
    render(<Input type="search" />);
    expect(screen.getByRole('searchbox')).toBeInTheDocument();
  });

  it('renderiza corretamente com tipo url', () => {
    render(<Input type="url" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'url');
  });

  it('renderiza corretamente com tipo color', () => {
    render(<Input type="color" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'color');
  });

  it('renderiza corretamente com tipo file', () => {
    render(<Input type="file" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'file');
  });

  it('renderiza corretamente com tipo range', () => {
    render(<Input type="range" />);
    expect(screen.getByRole('slider')).toBeInTheDocument();
  });
}); 