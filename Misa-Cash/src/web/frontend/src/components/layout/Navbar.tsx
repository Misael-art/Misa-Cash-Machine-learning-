import React from 'react';
import {
  Box,
  Flex,
  IconButton,
  useColorMode,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Avatar,
  Text,
  Badge,
  Input,
  InputGroup,
  InputLeftElement,
} from '@chakra-ui/react';
import {
  FiSun,
  FiMoon,
  FiBell,
  FiSearch,
  FiSettings,
  FiHelpCircle,
  FiLogOut,
} from 'react-icons/fi';

const Navbar: React.FC = () => {
  const { colorMode, toggleColorMode } = useColorMode();

  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      w="full"
      px="4"
      h="16"
      className="transition-all duration-200"
    >
      {/* Barra de Pesquisa */}
      <Box flex="1" maxW="2xl">
        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <FiSearch className="text-gray-400" />
          </InputLeftElement>
          <Input
            placeholder="Pesquisar..."
            variant="filled"
            bg={colorMode === 'light' ? 'gray.100' : 'gray.700'}
            _hover={{ bg: colorMode === 'light' ? 'gray.200' : 'gray.600' }}
            _focus={{
              bg: colorMode === 'light' ? 'white' : 'gray.800',
              borderColor: 'primary.500',
            }}
          />
        </InputGroup>
      </Box>

      {/* Ações do Usuário */}
      <Flex align="center" gap="4">
        {/* Botão de Tema */}
        <IconButton
          aria-label="Alternar tema"
          icon={colorMode === 'light' ? <FiMoon /> : <FiSun />}
          onClick={toggleColorMode}
          variant="ghost"
          className="hover:bg-gray-100 dark:hover:bg-gray-700"
        />

        {/* Notificações */}
        <Box position="relative">
          <IconButton
            aria-label="Notificações"
            icon={<FiBell />}
            variant="ghost"
            className="hover:bg-gray-100 dark:hover:bg-gray-700"
          />
          <Badge
            position="absolute"
            top="-1"
            right="-1"
            colorScheme="red"
            variant="solid"
            borderRadius="full"
            w="5"
            h="5"
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            3
          </Badge>
        </Box>

        {/* Menu do Usuário */}
        <Menu>
          <MenuButton
            as={Box}
            cursor="pointer"
            className="hover:opacity-80 transition-opacity"
          >
            <Flex align="center" gap="3">
              <Avatar
                size="sm"
                name="Usuário"
                src="/images/avatar-placeholder.png"
              />
              <Box display={{ base: 'none', md: 'block' }}>
                <Text fontWeight="medium">Usuário</Text>
                <Text fontSize="sm" color="gray.500">
                  usuario@exemplo.com
                </Text>
              </Box>
            </Flex>
          </MenuButton>
          <MenuList>
            <MenuItem icon={<FiSettings />}>Configurações</MenuItem>
            <MenuItem icon={<FiHelpCircle />}>Ajuda</MenuItem>
            <MenuItem icon={<FiLogOut />} color="red.500">
              Sair
            </MenuItem>
          </MenuList>
        </Menu>
      </Flex>
    </Flex>
  );
};

export default Navbar; 