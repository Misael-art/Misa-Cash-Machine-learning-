import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Alert from '../../components/Alert';
import Button from '../../components/Button';
import Form from '../../components/Form';
import Input from '../../components/Input';
import Modal from '../../components/Modal';

describe('Alert Integration', () => {
  it('integra corretamente Alert com Form para feedback de validação', async () => {
    const mockSubmit = jest.fn();
    const [error, setError] = React.useState('');

    render(
      <>
        {error && (
          <Alert
            type="error"
            message={error}
            onClose={() => setError('')}
          />
        )}
        <Form
          onSubmit={(values) => {
            if (!values.email) {
              setError('Email é obrigatório');
              return;
            }
            mockSubmit(values);
          }}
        >
          <Input
            name="email"
            label="Email"
            type="email"
            placeholder="Digite seu email"
          />
          <Button type="submit">Enviar</Button>
        </Form>
      </>
    );

    fireEvent.click(screen.getByText('Enviar'));
    expect(screen.getByText('Email é obrigatório')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Fechar' }));
    expect(screen.queryByText('Email é obrigatório')).not.toBeInTheDocument();
  });

  it('integra corretamente Alert com Modal para confirmação', async () => {
    const mockDelete = jest.fn();
    const [showModal, setShowModal] = React.useState(false);
    const [showAlert, setShowAlert] = React.useState(false);

    render(
      <>
        <Button onClick={() => setShowModal(true)}>Excluir Item</Button>

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
                  mockDelete();
                  setShowModal(false);
                  setShowAlert(true);
                },
              },
            ]}
          />
        </Modal>

        {showAlert && (
          <Alert
            type="success"
            message="Item excluído com sucesso!"
            autoClose={3000}
            onClose={() => setShowAlert(false)}
          />
        )}
      </>
    );

    fireEvent.click(screen.getByText('Excluir Item'));
    expect(screen.getByText('Tem certeza que deseja excluir este item?')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Confirmar'));
    expect(mockDelete).toHaveBeenCalled();
    expect(screen.getByText('Item excluído com sucesso!')).toBeInTheDocument();
  });

  it('integra corretamente Alert com Form para feedback de submissão', async () => {
    const mockSubmit = jest.fn();
    const [feedback, setFeedback] = React.useState(null);

    render(
      <>
        <Form
          onSubmit={async (values) => {
            try {
              await mockSubmit(values);
              setFeedback({
                type: 'success',
                message: 'Dados salvos com sucesso!',
              });
            } catch (error) {
              setFeedback({
                type: 'error',
                message: 'Erro ao salvar dados.',
              });
            }
          }}
        >
          <Input
            name="name"
            label="Nome"
            placeholder="Digite seu nome"
          />
          <Button type="submit">Salvar</Button>
        </Form>

        {feedback && (
          <Alert
            type={feedback.type}
            message={feedback.message}
            onClose={() => setFeedback(null)}
          />
        )}
      </>
    );

    mockSubmit.mockImplementationOnce(() => Promise.resolve());
    fireEvent.change(screen.getByLabelText('Nome'), {
      target: { value: 'João Silva' },
    });
    fireEvent.click(screen.getByText('Salvar'));

    await waitFor(() => {
      expect(screen.getByText('Dados salvos com sucesso!')).toBeInTheDocument();
    });

    mockSubmit.mockImplementationOnce(() => Promise.reject());
    fireEvent.click(screen.getByText('Salvar'));

    await waitFor(() => {
      expect(screen.getByText('Erro ao salvar dados.')).toBeInTheDocument();
    });
  });

  it('integra corretamente Alert com múltiplos alertas', async () => {
    const [alerts, setAlerts] = React.useState([]);

    const addAlert = (type, message) => {
      const id = Date.now();
      setAlerts([...alerts, { id, type, message }]);
      setTimeout(() => {
        setAlerts(current => current.filter(alert => alert.id !== id));
      }, 3000);
    };

    render(
      <>
        <div className="alerts-container">
          {alerts.map(alert => (
            <Alert
              key={alert.id}
              type={alert.type}
              message={alert.message}
              onClose={() => setAlerts(current => current.filter(a => a.id !== alert.id))}
            />
          ))}
        </div>

        <Button
          onClick={() => addAlert('success', 'Operação realizada com sucesso!')}
        >
          Sucesso
        </Button>
        <Button
          onClick={() => addAlert('error', 'Erro ao realizar operação!')}
        >
          Erro
        </Button>
        <Button
          onClick={() => addAlert('warning', 'Atenção!')}
        >
          Aviso
        </Button>
      </>
    );

    fireEvent.click(screen.getByText('Sucesso'));
    expect(screen.getByText('Operação realizada com sucesso!')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Erro'));
    expect(screen.getByText('Erro ao realizar operação!')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Aviso'));
    expect(screen.getByText('Atenção!')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.queryByText('Operação realizada com sucesso!')).not.toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('integra corretamente Alert com ações personalizadas', async () => {
    const mockAction1 = jest.fn();
    const mockAction2 = jest.fn();
    const [showAlert, setShowAlert] = React.useState(true);

    render(
      <Alert
        type="info"
        message="Você tem atualizações pendentes"
        show={showAlert}
        onClose={() => setShowAlert(false)}
        actions={[
          {
            label: 'Ver Detalhes',
            onClick: mockAction1,
            variant: 'primary',
          },
          {
            label: 'Ignorar',
            onClick: () => {
              mockAction2();
              setShowAlert(false);
            },
            variant: 'secondary',
          },
        ]}
      />
    );

    expect(screen.getByText('Você tem atualizações pendentes')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Ver Detalhes'));
    expect(mockAction1).toHaveBeenCalled();

    fireEvent.click(screen.getByText('Ignorar'));
    expect(mockAction2).toHaveBeenCalled();
    expect(screen.queryByText('Você tem atualizações pendentes')).not.toBeInTheDocument();
  });
}); 