import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Alert, AlertProps } from '@mui/material';
import { Button, TextField, Box, Modal, CircularProgress } from '@mui/material';

// Componente de formulário simples para teste
const TestForm = ({ onSubmit, onError, isLoading }: { onSubmit: () => void, onError: () => void, isLoading?: boolean }) => {
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [error, setError] = React.useState<string | null>(null);
  const [success, setSuccess] = React.useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validação simples
    if (!name || !email) {
      setError('Por favor, preencha todos os campos');
      setSuccess(null);
      onError();
      return;
    }
    
    if (!email.includes('@')) {
      setError('E-mail inválido');
      setSuccess(null);
      onError();
      return;
    }
    
    // Simulando sucesso
    setSuccess('Formulário enviado com sucesso!');
    setError(null);
    onSubmit();
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} data-testid="alert-error">
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} data-testid="alert-success">
          {success}
        </Alert>
      )}
      
      <TextField
        fullWidth
        label="Nome"
        value={name}
        onChange={(e) => setName(e.target.value)}
        margin="normal"
        data-testid="input-name"
      />
      
      <TextField
        fullWidth
        label="E-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        margin="normal"
        data-testid="input-email"
      />
      
      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={isLoading}
        sx={{ mt: 2 }}
        data-testid="submit-button"
      >
        {isLoading ? <CircularProgress size={24} /> : 'Enviar'}
      </Button>
    </Box>
  );
};

// Componente de modal simples para teste
const TestModal = ({ 
  open, 
  onClose, 
  onConfirm 
}: { 
  open: boolean, 
  onClose: () => void, 
  onConfirm: () => void 
}) => {
  const [error, setError] = React.useState<string | null>(null);
  const [success, setSuccess] = React.useState<string | null>(null);

  const handleConfirm = () => {
    setSuccess('Operação confirmada!');
    setError(null);
    onConfirm();
  };

  const handleError = () => {
    setError('Ocorreu um erro na operação');
    setSuccess(null);
  };

  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="modal-title"
      data-testid="test-modal"
    >
      <Box sx={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
      }}>
        <h2 id="modal-title">Confirmação</h2>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} data-testid="modal-alert-error">
            {error}
          </Alert>
        )}
        
        {success && (
          <Alert severity="success" sx={{ mb: 2 }} data-testid="modal-alert-success">
            {success}
          </Alert>
        )}
        
        <p>Deseja confirmar esta operação?</p>
        
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
          <Button onClick={onClose} variant="outlined" data-testid="modal-cancel">
            Cancelar
          </Button>
          <Button onClick={handleConfirm} variant="contained" color="primary" data-testid="modal-confirm">
            Confirmar
          </Button>
          <Button onClick={handleError} variant="contained" color="error" data-testid="modal-error">
            Simular Erro
          </Button>
        </Box>
      </Box>
    </Modal>
  );
};

describe('Alert - Testes de Integração', () => {
  test('Integração com Form: exibição de mensagens de erro e sucesso', async () => {
    const handleSubmit = jest.fn();
    const handleError = jest.fn();
    
    render(<TestForm onSubmit={handleSubmit} onError={handleError} />);
    
    // Verificar que o alerta não está inicialmente visível
    expect(screen.queryByTestId('alert-error')).not.toBeInTheDocument();
    expect(screen.queryByTestId('alert-success')).not.toBeInTheDocument();
    
    // Testar submissão de formulário vazio (deve mostrar erro)
    fireEvent.click(screen.getByTestId('submit-button'));
    
    // Verificar que o alerta de erro está visível
    expect(screen.getByTestId('alert-error')).toBeInTheDocument();
    expect(screen.getByTestId('alert-error')).toHaveTextContent('Por favor, preencha todos os campos');
    expect(handleError).toHaveBeenCalledTimes(1);
    
    // Preencher o formulário com um email inválido
    fireEvent.change(screen.getByTestId('input-name'), { target: { value: 'João Silva' } });
    fireEvent.change(screen.getByTestId('input-email'), { target: { value: 'email-invalido' } });
    
    // Submeter novamente (deve mostrar erro de email)
    fireEvent.click(screen.getByTestId('submit-button'));
    
    // Verificar que o alerta de erro ainda está visível, mas com mensagem diferente
    expect(screen.getByTestId('alert-error')).toBeInTheDocument();
    expect(screen.getByTestId('alert-error')).toHaveTextContent('E-mail inválido');
    expect(handleError).toHaveBeenCalledTimes(2);
    
    // Corrigir o email e submeter novamente
    fireEvent.change(screen.getByTestId('input-email'), { target: { value: 'joao@example.com' } });
    fireEvent.click(screen.getByTestId('submit-button'));
    
    // Verificar que o alerta de sucesso está visível
    expect(screen.getByTestId('alert-success')).toBeInTheDocument();
    expect(screen.getByTestId('alert-success')).toHaveTextContent('Formulário enviado com sucesso!');
    expect(handleSubmit).toHaveBeenCalledTimes(1);
  });

  test('Integração com Button: alerta que pode ser descartado', () => {
    const AlertWithDismiss = () => {
      const [open, setOpen] = React.useState(true);
      
      return open ? (
        <Alert 
          severity="info" 
          data-testid="dismissible-alert"
          action={
            <Button 
              color="inherit" 
              size="small" 
              onClick={() => setOpen(false)}
              data-testid="dismiss-button"
            >
              Fechar
            </Button>
          }
        >
          Esta é uma mensagem informativa que pode ser fechada.
        </Alert>
      ) : null;
    };
    
    render(<AlertWithDismiss />);
    
    // Verificar que o alerta está inicialmente visível
    expect(screen.getByTestId('dismissible-alert')).toBeInTheDocument();
    
    // Clicar no botão de fechar
    fireEvent.click(screen.getByTestId('dismiss-button'));
    
    // Verificar que o alerta não está mais visível
    expect(screen.queryByTestId('dismissible-alert')).not.toBeInTheDocument();
  });

  test('Integração com Modal: alerta exibido dentro do modal após confirmação', async () => {
    const handleClose = jest.fn();
    const handleConfirm = jest.fn();
    
    render(
      <TestModal open={true} onClose={handleClose} onConfirm={handleConfirm} />
    );
    
    // Verificar que o modal está aberto
    expect(screen.getByTestId('test-modal')).toBeInTheDocument();
    
    // Verificar que nenhum alerta está visível inicialmente
    expect(screen.queryByTestId('modal-alert-success')).not.toBeInTheDocument();
    expect(screen.queryByTestId('modal-alert-error')).not.toBeInTheDocument();
    
    // Clicar no botão de confirmar
    fireEvent.click(screen.getByTestId('modal-confirm'));
    
    // Verificar que o alerta de sucesso está visível
    expect(screen.getByTestId('modal-alert-success')).toBeInTheDocument();
    expect(screen.getByTestId('modal-alert-success')).toHaveTextContent('Operação confirmada!');
    expect(handleConfirm).toHaveBeenCalledTimes(1);
    
    // Clicar no botão de erro
    fireEvent.click(screen.getByTestId('modal-error'));
    
    // Verificar que o alerta de erro está visível
    expect(screen.getByTestId('modal-alert-error')).toBeInTheDocument();
    expect(screen.getByTestId('modal-alert-error')).toHaveTextContent('Ocorreu um erro na operação');
  });

  test('Integração com Input: alerta responsivo a mudanças em campos', () => {
    const InputWithAlert = () => {
      const [value, setValue] = React.useState('');
      const [alert, setAlert] = React.useState<{ type: AlertProps['severity'], message: string } | null>(null);
      
      const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = e.target.value;
        setValue(newValue);
        
        if (newValue.length < 3 && newValue.length > 0) {
          setAlert({ type: 'warning', message: 'O texto é muito curto (mínimo 3 caracteres)' });
        } else if (newValue.length >= 10) {
          setAlert({ type: 'error', message: 'O texto é muito longo (máximo 9 caracteres)' });
        } else if (newValue.length >= 3) {
          setAlert({ type: 'success', message: 'Tamanho do texto válido!' });
        } else {
          setAlert(null);
        }
      };
      
      return (
        <Box>
          <TextField
            fullWidth
            label="Texto"
            value={value}
            onChange={handleChange}
            margin="normal"
            data-testid="validation-input"
          />
          
          {alert && (
            <Alert severity={alert.type} data-testid={`alert-${alert.type}`}>
              {alert.message}
            </Alert>
          )}
        </Box>
      );
    };
    
    render(<InputWithAlert />);
    
    // Verificar que nenhum alerta está visível inicialmente
    expect(screen.queryByTestId('alert-warning')).not.toBeInTheDocument();
    expect(screen.queryByTestId('alert-success')).not.toBeInTheDocument();
    expect(screen.queryByTestId('alert-error')).not.toBeInTheDocument();
    
    // Digitar menos de 3 caracteres
    fireEvent.change(screen.getByTestId('validation-input'), { target: { value: 'ab' } });
    
    // Verificar que o alerta de aviso está visível
    expect(screen.getByTestId('alert-warning')).toBeInTheDocument();
    expect(screen.getByTestId('alert-warning')).toHaveTextContent('O texto é muito curto (mínimo 3 caracteres)');
    
    // Digitar entre 3 e 9 caracteres
    fireEvent.change(screen.getByTestId('validation-input'), { target: { value: 'abcdef' } });
    
    // Verificar que o alerta de sucesso está visível
    expect(screen.getByTestId('alert-success')).toBeInTheDocument();
    expect(screen.getByTestId('alert-success')).toHaveTextContent('Tamanho do texto válido!');
    
    // Digitar mais de 9 caracteres
    fireEvent.change(screen.getByTestId('validation-input'), { target: { value: 'abcdefghijk' } });
    
    // Verificar que o alerta de erro está visível
    expect(screen.getByTestId('alert-error')).toBeInTheDocument();
    expect(screen.getByTestId('alert-error')).toHaveTextContent('O texto é muito longo (máximo 9 caracteres)');
    
    // Limpar o campo
    fireEvent.change(screen.getByTestId('validation-input'), { target: { value: '' } });
    
    // Verificar que nenhum alerta está visível novamente
    expect(screen.queryByTestId('alert-warning')).not.toBeInTheDocument();
    expect(screen.queryByTestId('alert-success')).not.toBeInTheDocument();
    expect(screen.queryByTestId('alert-error')).not.toBeInTheDocument();
  });

  test('Integração com Estado de Loading: alerta mostra mensagem diferente durante carregamento', async () => {
    const AlertWithLoading = () => {
      const [isLoading, setIsLoading] = React.useState(false);
      const [success, setSuccess] = React.useState(false);
      
      const handleButtonClick = () => {
        setIsLoading(true);
        setSuccess(false);
        
        // Simular operação assíncrona
        setTimeout(() => {
          setIsLoading(false);
          setSuccess(true);
        }, 100);
      };
      
      return (
        <Box>
          {isLoading && (
            <Alert severity="info" data-testid="alert-loading">
              Processando sua solicitação... <CircularProgress size={16} />
            </Alert>
          )}
          
          {success && (
            <Alert severity="success" data-testid="alert-done">
              Operação concluída com sucesso!
            </Alert>
          )}
          
          <Button
            variant="contained"
            onClick={handleButtonClick}
            disabled={isLoading}
            data-testid="load-button"
          >
            {isLoading ? 'Processando...' : 'Executar'}
          </Button>
        </Box>
      );
    };
    
    render(<AlertWithLoading />);
    
    // Verificar que nenhum alerta está visível inicialmente
    expect(screen.queryByTestId('alert-loading')).not.toBeInTheDocument();
    expect(screen.queryByTestId('alert-done')).not.toBeInTheDocument();
    
    // Clicar no botão para iniciar o carregamento
    fireEvent.click(screen.getByTestId('load-button'));
    
    // Verificar que o alerta de carregamento está visível
    expect(screen.getByTestId('alert-loading')).toBeInTheDocument();
    expect(screen.getByTestId('alert-loading')).toHaveTextContent('Processando sua solicitação...');
    
    // Aguardar a conclusão do carregamento
    await waitFor(() => {
      expect(screen.queryByTestId('alert-loading')).not.toBeInTheDocument();
      expect(screen.getByTestId('alert-done')).toBeInTheDocument();
    });
    
    // Verificar que o alerta de sucesso está visível
    expect(screen.getByTestId('alert-done')).toHaveTextContent('Operação concluída com sucesso!');
  });
}); 