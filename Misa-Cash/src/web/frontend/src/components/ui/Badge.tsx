import React from 'react';
import { Badge as ChakraBadge, BadgeProps as ChakraBadgeProps } from '@chakra-ui/react';

interface BadgeProps extends ChakraBadgeProps {
  variant?: 'success' | 'warning' | 'danger' | 'info';
}

const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'info',
  ...props
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'success':
        return {
          bg: 'green.100',
          color: 'green.800',
          _dark: {
            bg: 'green.900',
            color: 'green.100',
          },
        };
      case 'warning':
        return {
          bg: 'yellow.100',
          color: 'yellow.800',
          _dark: {
            bg: 'yellow.900',
            color: 'yellow.100',
          },
        };
      case 'danger':
        return {
          bg: 'red.100',
          color: 'red.800',
          _dark: {
            bg: 'red.900',
            color: 'red.100',
          },
        };
      case 'info':
      default:
        return {
          bg: 'blue.100',
          color: 'blue.800',
          _dark: {
            bg: 'blue.900',
            color: 'blue.100',
          },
        };
    }
  };

  return (
    <ChakraBadge
      px="2.5"
      py="0.5"
      borderRadius="full"
      fontSize="xs"
      fontWeight="medium"
      className="badge"
      {...getVariantStyles()}
      {...props}
    >
      {children}
    </ChakraBadge>
  );
};

export default Badge; 