import React, { useEffect, useState } from 'react';
import '../../styles/alert.css';

interface AlertProps {
  type: 'success' | 'error' | 'info';
  message: string;
  onClose?: () => void;
  autoClose?: boolean;
  duration?: number;
}

const Alert: React.FC<AlertProps> = ({
  type,
  message,
  onClose,
  autoClose = true,
  duration = 5000
}) => {
  const [isVisible, setIsVisible] = useState(true);

  // Configurar o temporizador para fechar automaticamente o alerta
  useEffect(() => {
    if (autoClose && isVisible) {
      const timer = setTimeout(() => {
        setIsVisible(false);
        if (onClose) onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [autoClose, duration, isVisible, onClose]);

  // Manipulador para fechar o alerta
  const handleClose = () => {
    setIsVisible(false);
    if (onClose) onClose();
  };

  // Determinar a classe e ícone com base no tipo
  const getAlertClass = () => {
    switch (type) {
      case 'success':
        return 'alert-success';
      case 'error':
        return 'alert-error';
      case 'info':
        return 'alert-info';
      default:
        return 'alert-info';
    }
  };

  const getAlertIcon = () => {
    switch (type) {
      case 'success':
        return <i className="fas fa-check-circle"></i>;
      case 'error':
        return <i className="fas fa-exclamation-circle"></i>;
      case 'info':
        return <i className="fas fa-info-circle"></i>;
      default:
        return <i className="fas fa-info-circle"></i>;
    }
  };

  // Se não estiver visível, não renderizar nada
  if (!isVisible) return null;

  return (
    <div className={`alert ${getAlertClass()}`}>
      <div className="alert-icon">
        {getAlertIcon()}
      </div>
      <div className="alert-content">
        {message}
      </div>
      <button 
        className="alert-close" 
        onClick={handleClose}
        aria-label="Fechar"
      >
        <i className="fas fa-times"></i>
      </button>
    </div>
  );
};

export default Alert; 