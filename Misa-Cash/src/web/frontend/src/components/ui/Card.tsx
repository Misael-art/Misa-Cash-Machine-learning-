import React from 'react';
import {
  Box,
  BoxProps,
  useColorMode,
} from '@chakra-ui/react';

interface CardProps extends BoxProps {
  children: React.ReactNode;
  hover?: boolean;
}

const Card: React.FC<CardProps> = ({
  children,
  hover = true,
  ...props
}) => {
  const { colorMode } = useColorMode();

  return (
    <Box
      bg={colorMode === 'light' ? 'white' : 'gray.800'}
      borderRadius="xl"
      boxShadow="base"
      p="6"
      className={`
        transition-all duration-200
        ${hover ? 'hover:shadow-lg' : ''}
      `}
      {...props}
    >
      {children}
    </Box>
  );
};

export default Card; 