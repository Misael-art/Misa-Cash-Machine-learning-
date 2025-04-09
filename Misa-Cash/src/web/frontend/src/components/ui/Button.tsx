import React from 'react';
import {
  Button as ChakraButton,
  ButtonProps as ChakraButtonProps,
  useColorMode,
} from '@chakra-ui/react';

interface ButtonProps extends ChakraButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactElement;
  rightIcon?: React.ReactElement;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  ...props
}) => {
  const { colorMode } = useColorMode();

  const getVariantStyles = () => {
    switch (variant) {
      case 'primary':
        return {
          bg: 'primary.500',
          color: 'white',
          _hover: { bg: 'primary.600' },
          _active: { bg: 'primary.700' },
        };
      case 'secondary':
        return {
          bg: colorMode === 'light' ? 'gray.100' : 'gray.700',
          color: colorMode === 'light' ? 'gray.700' : 'gray.100',
          _hover: {
            bg: colorMode === 'light' ? 'gray.200' : 'gray.600',
          },
          _active: {
            bg: colorMode === 'light' ? 'gray.300' : 'gray.500',
          },
        };
      case 'outline':
        return {
          border: '2px',
          borderColor: 'primary.500',
          color: 'primary.500',
          _hover: {
            bg: colorMode === 'light' ? 'primary.50' : 'gray.700',
          },
        };
      case 'ghost':
        return {
          color: 'primary.500',
          _hover: {
            bg: colorMode === 'light' ? 'primary.50' : 'gray.700',
          },
        };
      default:
        return {};
    }
  };

  return (
    <ChakraButton
      size={size}
      isLoading={isLoading}
      leftIcon={leftIcon}
      rightIcon={rightIcon}
      borderRadius="lg"
      fontWeight="medium"
      className="transition-all duration-200"
      {...getVariantStyles()}
      {...props}
    >
      {children}
    </ChakraButton>
  );
};

export default Button; 