import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Alert from '../Alert';

describe('Alert Component', () => {
  it('renderiza corretamente com mensagem', () => {
    render(<Alert message="Mensagem de alerta" />);
    expect(screen.getByText('Mensagem de alerta')).toBeInTheDocument();
  });

  it('renderiza corretamente com título', () => {
    render(<Alert title="Título do Alerta" message="Mensagem de alerta" />);
    expect(screen.getByText('Título do Alerta')).toBeInTheDocument();
  });

  it('renderiza corretamente com tipo success', () => {
    render(<Alert type="success" message="Operação realizada com sucesso" />);
    expect(screen.getByText('Operação realizada com sucesso')).toHaveClass('bg-green-100', 'text-green-800');
  });

  it('renderiza corretamente com tipo error', () => {
    render(<Alert type="error" message="Ocorreu um erro" />);
    expect(screen.getByText('Ocorreu um erro')).toHaveClass('bg-red-100', 'text-red-800');
  });

  it('renderiza corretamente com tipo warning', () => {
    render(<Alert type="warning" message="Atenção" />);
    expect(screen.getByText('Atenção')).toHaveClass('bg-yellow-100', 'text-yellow-800');
  });

  it('renderiza corretamente com tipo info', () => {
    render(<Alert type="info" message="Informação importante" />);
    expect(screen.getByText('Informação importante')).toHaveClass('bg-blue-100', 'text-blue-800');
  });

  it('renderiza corretamente com ícone', () => {
    render(
      <Alert
        type="success"
        message="Operação realizada com sucesso"
        icon={<span data-testid="success-icon">✓</span>}
      />
    );
    expect(screen.getByTestId('success-icon')).toBeInTheDocument();
  });

  it('renderiza corretamente com botão de fechar', () => {
    const onClose = jest.fn();
    render(<Alert message="Mensagem de alerta" onClose={onClose} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onClose).toHaveBeenCalled();
  });

  it('renderiza corretamente com ação personalizada', () => {
    const onAction = jest.fn();
    render(
      <Alert
        message="Mensagem de alerta"
        action={{
          label: 'Ação',
          onClick: onAction,
        }}
      />
    );
    fireEvent.click(screen.getByText('Ação'));
    expect(onAction).toHaveBeenCalled();
  });

  it('renderiza corretamente com múltiplas ações', () => {
    const onAction1 = jest.fn();
    const onAction2 = jest.fn();
    render(
      <Alert
        message="Mensagem de alerta"
        actions={[
          { label: 'Ação 1', onClick: onAction1 },
          { label: 'Ação 2', onClick: onAction2 },
        ]}
      />
    );
    fireEvent.click(screen.getByText('Ação 1'));
    expect(onAction1).toHaveBeenCalled();
    fireEvent.click(screen.getByText('Ação 2'));
    expect(onAction2).toHaveBeenCalled();
  });

  it('renderiza corretamente com autoClose', () => {
    jest.useFakeTimers();
    const onClose = jest.fn();
    render(<Alert message="Mensagem de alerta" autoClose={3000} onClose={onClose} />);
    jest.advanceTimersByTime(3000);
    expect(onClose).toHaveBeenCalled();
    jest.useRealTimers();
  });

  it('renderiza corretamente com posição personalizada', () => {
    render(<Alert message="Mensagem de alerta" position="top-right" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('top-4', 'right-4');
  });

  it('renderiza corretamente com animação personalizada', () => {
    render(<Alert message="Mensagem de alerta" animation="slide-in" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('animate-slide-in');
  });

  it('renderiza corretamente com z-index personalizado', () => {
    render(<Alert message="Mensagem de alerta" zIndex={100} />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveStyle({ zIndex: 100 });
  });

  it('renderiza corretamente com padding personalizado', () => {
    render(<Alert message="Mensagem de alerta" padding="p-8" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('p-8');
  });

  it('renderiza corretamente com margin personalizada', () => {
    render(<Alert message="Mensagem de alerta" margin="m-4" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('m-4');
  });

  it('renderiza corretamente com largura personalizada', () => {
    render(<Alert message="Mensagem de alerta" width="w-96" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('w-96');
  });

  it('renderiza corretamente com altura personalizada', () => {
    render(<Alert message="Mensagem de alerta" height="h-32" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('h-32');
  });

  it('renderiza corretamente com overflow personalizado', () => {
    render(<Alert message="Mensagem de alerta" overflow="overflow-auto" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('overflow-auto');
  });

  it('renderiza corretamente com cursor personalizado', () => {
    render(<Alert message="Mensagem de alerta" cursor="cursor-pointer" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('cursor-pointer');
  });

  it('renderiza corretamente com transição personalizada', () => {
    render(<Alert message="Mensagem de alerta" transition="transition-all duration-300" />);
    expect(screen.getByText('Mensagem de alerta').parentElement).toHaveClass('transition-all', 'duration-300');
  });
}); 