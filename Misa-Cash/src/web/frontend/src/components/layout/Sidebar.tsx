import React from 'react';
import {
  Box,
  VStack,
  Icon,
  Text,
  Flex,
  useColorMode,
  Tooltip,
} from '@chakra-ui/react';
import {
  FiHome,
  FiTrendingUp,
  FiDatabase,
  FiSettings,
  FiBarChart2,
  FiActivity,
  FiLayers,
  FiBook,
} from 'react-icons/fi';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface NavItemProps {
  icon: any;
  children: string;
  href: string;
  isActive?: boolean;
}

const NavItem: React.FC<NavItemProps> = ({
  icon,
  children,
  href,
  isActive = false,
}) => {
  const { colorMode } = useColorMode();

  return (
    <Tooltip label={children} placement="right" hasArrow>
      <Link href={href} passHref>
        <Flex
          align="center"
          p="4"
          mx="4"
          borderRadius="lg"
          role="group"
          cursor="pointer"
          className={`
            transition-all duration-200
            ${
              isActive
                ? 'bg-primary-500 text-white'
                : 'hover:bg-primary-50 dark:hover:bg-gray-700'
            }
          `}
          bg={isActive ? 'primary.500' : 'transparent'}
          color={isActive ? 'white' : colorMode === 'light' ? 'gray.600' : 'gray.300'}
        >
          <Icon
            mr="4"
            fontSize="16"
            as={icon}
            className={isActive ? '' : 'group-hover:text-primary-500'}
          />
          <Text fontSize="sm" fontWeight="medium">
            {children}
          </Text>
        </Flex>
      </Link>
    </Tooltip>
  );
};

const Sidebar: React.FC = () => {
  const router = useRouter();
  const { colorMode } = useColorMode();

  const navItems = [
    { icon: FiHome, label: 'Dashboard', href: '/' },
    { icon: FiTrendingUp, label: 'Estratégias', href: '/strategies' },
    { icon: FiBarChart2, label: 'Backtesting', href: '/backtesting' },
    { icon: FiActivity, label: 'Otimização', href: '/optimization' },
    { icon: FiDatabase, label: 'Dados', href: '/data' },
    { icon: FiLayers, label: 'Portfólio', href: '/portfolio' },
    { icon: FiBook, label: 'Documentação', href: '/docs' },
    { icon: FiSettings, label: 'Configurações', href: '/settings' },
  ];

  return (
    <Box h="full" py="5">
      {/* Logo */}
      <Flex
        h="16"
        align="center"
        justifyContent="center"
        borderBottom="1px"
        borderColor={colorMode === 'light' ? 'gray.200' : 'gray.700'}
        mb="5"
      >
        <Text
          fontSize="2xl"
          fontWeight="bold"
          bgGradient="linear(to-r, primary.500, primary.300)"
          bgClip="text"
        >
          ML Finance
        </Text>
      </Flex>

      {/* Menu de Navegação */}
      <VStack spacing="2">
        {navItems.map((item) => (
          <NavItem
            key={item.href}
            icon={item.icon}
            href={item.href}
            isActive={router.pathname === item.href}
          >
            {item.label}
          </NavItem>
        ))}
      </VStack>

      {/* Versão */}
      <Text
        position="absolute"
        bottom="4"
        width="full"
        textAlign="center"
        fontSize="sm"
        color="gray.500"
      >
        v0.1.0
      </Text>
    </Box>
  );
};

export default Sidebar; 