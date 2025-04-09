import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  config: {
    initialColorMode: 'light',
    useSystemColorMode: true,
  },
  fonts: {
    heading: 'Inter var, sans-serif',
    body: 'Inter var, sans-serif',
  },
  colors: {
    primary: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      200: '#bae6fd',
      300: '#7dd3fc',
      400: '#38bdf8',
      500: '#0ea5e9',
      600: '#0284c7',
      700: '#0369a1',
      800: '#075985',
      900: '#0c4a6e',
    },
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: 'medium',
        borderRadius: 'lg',
      },
      variants: {
        solid: (props: any) => ({
          bg: props.colorScheme === 'primary' ? 'primary.500' : undefined,
          color: props.colorScheme === 'primary' ? 'white' : undefined,
          _hover: {
            bg: props.colorScheme === 'primary' ? 'primary.600' : undefined,
          },
          _active: {
            bg: props.colorScheme === 'primary' ? 'primary.700' : undefined,
          },
        }),
        outline: (props: any) => ({
          borderColor: props.colorScheme === 'primary' ? 'primary.500' : undefined,
          color: props.colorScheme === 'primary' ? 'primary.500' : undefined,
          _hover: {
            bg: props.colorScheme === 'primary' ? 'primary.50' : undefined,
          },
        }),
        ghost: (props: any) => ({
          color: props.colorScheme === 'primary' ? 'primary.500' : undefined,
          _hover: {
            bg: props.colorScheme === 'primary' ? 'primary.50' : undefined,
          },
        }),
      },
    },
    Input: {
      variants: {
        filled: {
          field: {
            borderRadius: 'lg',
            _focus: {
              borderColor: 'primary.500',
            },
          },
        },
        outline: {
          field: {
            borderRadius: 'lg',
            _focus: {
              borderColor: 'primary.500',
              boxShadow: '0 0 0 1px var(--chakra-colors-primary-500)',
            },
          },
        },
      },
    },
    Card: {
      baseStyle: (props: any) => ({
        container: {
          bg: props.colorMode === 'light' ? 'white' : 'gray.800',
          borderRadius: 'xl',
          boxShadow: 'base',
          overflow: 'hidden',
        },
      }),
    },
    Modal: {
      baseStyle: {
        dialog: {
          borderRadius: 'xl',
        },
      },
    },
    Tooltip: {
      baseStyle: {
        borderRadius: 'md',
        px: '3',
        py: '2',
      },
    },
  },
  styles: {
    global: (props: any) => ({
      body: {
        bg: props.colorMode === 'light' ? 'gray.50' : 'gray.900',
        color: props.colorMode === 'light' ? 'gray.800' : 'white',
      },
    }),
  },
});

export default theme; 