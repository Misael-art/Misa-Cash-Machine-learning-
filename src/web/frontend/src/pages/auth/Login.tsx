import React, { useState } from 'react';
import { useAuthContext } from '../../contexts/AuthContext';

const Login: React.FC = () => {
  const { login, loading, error } = useAuthContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    // Validação simples do formulário
    if (!email || !password) {
      setFormError('Por favor, preencha todos os campos.');
      return;
    }

    const result = await login({ email, password });
    
    if (!result.success) {
      setFormError(result.error || 'Erro ao fazer login.');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      
      {formError && <div className="error-message">{formError}</div>}
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Senha:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            required
          />
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
      
      <div className="auth-links">
        <p>
          Não tem uma conta? <a href="/register">Registre-se</a>
        </p>
      </div>
    </div>
  );
};

export default Login; 