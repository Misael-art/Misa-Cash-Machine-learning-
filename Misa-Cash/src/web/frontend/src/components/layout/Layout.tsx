import React from 'react';
import { Box, Flex, useColorMode } from '@chakra-ui/react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { colorMode } = useColorMode();

  return (
    <Flex
      minH="100vh"
      bg={colorMode === 'light' ? 'gray.50' : 'gray.900'}
      className="transition-colors duration-200"
    >
      {/* Sidebar */}
      <Box
        as="nav"
        pos="fixed"
        left="0"
        h="100vh"
        w="64"
        bg={colorMode === 'light' ? 'white' : 'gray.800'}
        borderRight="1px"
        borderColor={colorMode === 'light' ? 'gray.200' : 'gray.700'}
        className="transition-all duration-200 ease-in-out transform"
      >
        <Sidebar />
      </Box>

      {/* Main Content */}
      <Box ml="64" flex="1">
        {/* Navbar */}
        <Box
          as="header"
          pos="fixed"
          top="0"
          right="0"
          left="64"
          h="16"
          bg={colorMode === 'light' ? 'white' : 'gray.800'}
          borderBottom="1px"
          borderColor={colorMode === 'light' ? 'gray.200' : 'gray.700'}
          zIndex="sticky"
        >
          <Navbar />
        </Box>

        {/* Page Content */}
        <Box as="main" mt="16" p="6">
          <Box
            maxW="7xl"
            mx="auto"
            className="animate-fade-in"
          >
            {children}
          </Box>
        </Box>
      </Box>
    </Flex>
  );
};

export default Layout; 