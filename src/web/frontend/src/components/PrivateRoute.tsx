import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';

interface PrivateRouteProps {
  children: React.ReactNode;
}

/**
 * Componente de rota privada que verifica se o usuário está autenticado
 * Redireciona para a página de login se não estiver, preservando a URL original como state
 */
const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  const { isAuthenticated, loading } = useAuthContext();
  const location = useLocation();

  // Exibe um indicador de carregamento enquanto verifica a autenticação
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Carregando...</p>
      </div>
    );
  }

  // Redireciona para a página de login se não estiver autenticado
  // Armazena a localização atual para redirecionar de volta após o login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Renderiza o conteúdo protegido se estiver autenticado
  return <>{children}</>;
};

export default PrivateRoute; 