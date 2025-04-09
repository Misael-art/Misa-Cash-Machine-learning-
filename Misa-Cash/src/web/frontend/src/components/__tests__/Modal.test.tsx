import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Modal from '../Modal';

describe('Modal Component', () => {
  it('renderiza corretamente quando aberto', () => {
    render(
      <Modal isOpen onClose={() => {}}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal')).toBeInTheDocument();
  });

  it('não renderiza quando fechado', () => {
    render(
      <Modal isOpen={false} onClose={() => {}}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.queryByText('Conteúdo do modal')).not.toBeInTheDocument();
  });

  it('renderiza corretamente com título', () => {
    render(
      <Modal isOpen title="Título do Modal" onClose={() => {}}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Título do Modal')).toBeInTheDocument();
  });

  it('chama onClose quando clica no botão de fechar', () => {
    const handleClose = jest.fn();
    render(
      <Modal isOpen onClose={handleClose}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    fireEvent.click(screen.getByRole('button'));
    expect(handleClose).toHaveBeenCalled();
  });

  it('chama onClose quando clica no overlay', () => {
    const handleClose = jest.fn();
    render(
      <Modal isOpen onClose={handleClose}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    fireEvent.click(screen.getByTestId('modal-overlay'));
    expect(handleClose).toHaveBeenCalled();
  });

  it('não chama onClose quando clica no conteúdo do modal', () => {
    const handleClose = jest.fn();
    render(
      <Modal isOpen onClose={handleClose}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    fireEvent.click(screen.getByText('Conteúdo do modal'));
    expect(handleClose).not.toHaveBeenCalled();
  });

  it('renderiza corretamente com footer', () => {
    render(
      <Modal
        isOpen
        onClose={() => {}}
        footer={
          <div>
            <button>Cancelar</button>
            <button>Confirmar</button>
          </div>
        }
      >
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Cancelar')).toBeInTheDocument();
    expect(screen.getByText('Confirmar')).toBeInTheDocument();
  });

  it('renderiza corretamente com tamanho personalizado', () => {
    render(
      <Modal isOpen size="lg" onClose={() => {}}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveClass('max-w-4xl');
  });

  it('renderiza corretamente com posição personalizada', () => {
    render(
      <Modal isOpen position="top" onClose={() => {}}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveClass('mt-4');
  });

  it('renderiza corretamente com animação personalizada', () => {
    render(
      <Modal isOpen animation="slide-up" onClose={() => {}}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveClass('animate-slide-up');
  });

  it('renderiza corretamente com backdrop personalizado', () => {
    render(
      <Modal isOpen backdrop="blur" onClose={() => {}}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByTestId('modal-overlay')).toHaveClass('backdrop-blur');
  });

  it('renderiza corretamente com scroll personalizado', () => {
    render(
      <Modal isOpen scroll="inside" onClose={() => {}}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveClass('overflow-auto');
  });

  it('renderiza corretamente com closeOnEsc desabilitado', () => {
    const handleClose = jest.fn();
    render(
      <Modal isOpen onClose={handleClose} closeOnEsc={false}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(handleClose).not.toHaveBeenCalled();
  });

  it('renderiza corretamente com closeOnOverlayClick desabilitado', () => {
    const handleClose = jest.fn();
    render(
      <Modal isOpen onClose={handleClose} closeOnOverlayClick={false}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    fireEvent.click(screen.getByTestId('modal-overlay'));
    expect(handleClose).not.toHaveBeenCalled();
  });

  it('renderiza corretamente com z-index personalizado', () => {
    render(
      <Modal isOpen onClose={() => {}} zIndex={100}>
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveStyle({ zIndex: 100 });
  });

  it('renderiza corretamente com padding personalizado', () => {
    render(
      <Modal isOpen onClose={() => {}} padding="p-8">
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveClass('p-8');
  });

  it('renderiza corretamente com background personalizado', () => {
    render(
      <Modal isOpen onClose={() => {}} background="bg-gray-100">
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveClass('bg-gray-100');
  });

  it('renderiza corretamente com borda personalizada', () => {
    render(
      <Modal isOpen onClose={() => {}} border="border-2 border-blue-500">
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveClass('border-2', 'border-blue-500');
  });

  it('renderiza corretamente com sombra personalizada', () => {
    render(
      <Modal isOpen onClose={() => {}} shadow="shadow-xl">
        <p>Conteúdo do modal</p>
      </Modal>
    );
    expect(screen.getByText('Conteúdo do modal').parentElement).toHaveClass('shadow-xl');
  });
}); 