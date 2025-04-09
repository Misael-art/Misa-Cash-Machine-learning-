import React from 'react';
import { 
  Box, 
  Flex, 
  Text, 
  VStack, 
  Icon, 
  Divider, 
  useColorModeValue 
} from '@chakra-ui/react';
import { Link, useLocation } from 'react-router-dom';
import { 
  FiHome, 
  FiDollarSign, 
  FiPieChart, 
  FiUser, 
  FiBarChart2,
  FiTag,
  FiClipboard
} from 'react-icons/fi';
import { useAuth } from '../../contexts/AuthContext';

interface NavItemProps {
  icon: any;
  children: React.ReactNode;
  to: string;
  isActive: boolean;
}

const NavItem = ({ icon, children, to, isActive }: NavItemProps) => {
  const activeBg = useColorModeValue('teal.50', 'teal.900');
  const inactiveBg = useColorModeValue('transparent', 'transparent');
  const activeColor = useColorModeValue('teal.600', 'teal.200');
  const inactiveColor = useColorModeValue('gray.600', 'gray.400');

  return (
    <Link to={to} style={{ width: '100%' }}>
      <Flex
        align="center"
        p="3"
        mx="2"
        borderRadius="lg"
        role="group"
        cursor="pointer"
        bg={isActive ? activeBg : inactiveBg}
        color={isActive ? activeColor : inactiveColor}
        fontWeight={isActive ? "medium" : "normal"}
        _hover={{
          bg: activeBg,
          color: activeColor,
        }}
        transition="all 0.2s"
      >
        <Icon
          mr="3"
          fontSize="18"
          as={icon}
        />
        <Text fontSize="sm">{children}</Text>
      </Flex>
    </Link>
  );
};

const Sidebar = () => {
  const location = useLocation();
  const { user } = useAuth();
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <Box
      position="fixed"
      left="0"
      h="full"
      w="64"
      bg={bgColor}
      borderRight="1px"
      borderRightColor={borderColor}
      py="6"
    >
      <Flex
        h="20"
        alignItems="center"
        mx="8"
        justifyContent="space-between"
      >
        <Text fontSize="2xl" fontWeight="bold" color="teal.500">
          Misa Cash
        </Text>
      </Flex>

      <Flex direction="column" h="full" justifyContent="space-between">
        <Box>
          <VStack align="stretch" spacing="1" mt="4">
            <NavItem 
              icon={FiHome} 
              to="/dashboard" 
              isActive={isActive('/dashboard')}
            >
              Dashboard
            </NavItem>
            <NavItem 
              icon={FiDollarSign} 
              to="/transactions" 
              isActive={isActive('/transactions')}
            >
              Transações
            </NavItem>
            <NavItem 
              icon={FiTag} 
              to="/categories" 
              isActive={isActive('/categories')}
            >
              Categorias
            </NavItem>
            <NavItem 
              icon={FiClipboard} 
              to="/budgets" 
              isActive={isActive('/budgets')}
            >
              Orçamentos
            </NavItem>
            <NavItem 
              icon={FiBarChart2} 
              to="/reports" 
              isActive={isActive('/reports')}
            >
              Relatórios
            </NavItem>
          </VStack>
        </Box>

        <Box mt="auto">
          <Divider my="6" />
          <NavItem 
            icon={FiUser} 
            to="/profile" 
            isActive={isActive('/profile')}
          >
            {user?.name ? user.name : 'Perfil'}
          </NavItem>
        </Box>
      </Flex>
    </Box>
  );
};

export default Sidebar; 