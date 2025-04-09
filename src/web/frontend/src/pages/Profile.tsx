import React, { useEffect } from 'react';
import { useAuthContext } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Profile: React.FC = () => {
  const { user, loading, isAuthenticated, logout } = useAuthContext();
  const navigate = useNavigate();

  // Redirecionar para o login se não estiver autenticado
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      navigate('/login');
    }
  }, [loading, isAuthenticated, navigate]);

  // Enquanto estiver carregando, mostra um indicador
  if (loading) {
    return (
      <div className="loading">
        Carregando...
      </div>
    );
  }

  // Não renderiza nada se não estiver autenticado (será redirecionado)
  if (!isAuthenticated || !user) {
    return null;
  }

  return (
    <div className="profile-container">
      <h2>Perfil do Usuário</h2>
      
      <div className="profile-info">
        <div className="profile-item">
          <strong>Nome de usuário:</strong> {user.username}
        </div>
        
        <div className="profile-item">
          <strong>Email:</strong> {user.email}
        </div>
        
        <div className="profile-item">
          <strong>Função:</strong> {user.role}
        </div>
        
        <div className="profile-item">
          <strong>Conta criada em:</strong> {new Date(user.created_at).toLocaleDateString()}
        </div>
        
        <div className="profile-item">
          <strong>Última atualização:</strong> {new Date(user.updated_at).toLocaleDateString()}
        </div>
      </div>
      
      <div className="profile-actions">
        <button onClick={() => navigate('/change-password')}>
          Alterar Senha
        </button>
        
        <button onClick={() => navigate('/edit-profile')}>
          Editar Perfil
        </button>
        
        <button onClick={() => {
          logout();
          navigate('/login');
        }} className="logout-button">
          Sair
        </button>
      </div>
    </div>
  );
};

export default Profile; 