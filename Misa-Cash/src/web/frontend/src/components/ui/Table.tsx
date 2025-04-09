import React from 'react';
import {
  Table as ChakraTable,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableProps as ChakraTableProps,
  useColorMode,
} from '@chakra-ui/react';

interface Column {
  key: string;
  label: string;
  align?: 'left' | 'center' | 'right';
  width?: string;
}

interface TableProps extends Omit<ChakraTableProps, 'children'> {
  columns: Column[];
  data: Record<string, any>[];
  onRowClick?: (row: Record<string, any>) => void;
  isLoading?: boolean;
}

const Table: React.FC<TableProps> = ({
  columns,
  data,
  onRowClick,
  isLoading = false,
  ...props
}) => {
  const { colorMode } = useColorMode();

  return (
    <div className="table-container">
      <ChakraTable
        variant="simple"
        className="table"
        {...props}
      >
        <Thead>
          <Tr>
            {columns.map((column) => (
              <Th
                key={column.key}
                textAlign={column.align || 'left'}
                width={column.width}
                color={colorMode === 'light' ? 'gray.500' : 'gray.400'}
                fontSize="xs"
                fontWeight="medium"
                textTransform="uppercase"
                letterSpacing="wider"
                py="3"
                px="6"
              >
                {column.label}
              </Th>
            ))}
          </Tr>
        </Thead>
        <Tbody>
          {isLoading ? (
            <Tr>
              <Td colSpan={columns.length} textAlign="center" py="8">
                Carregando...
              </Td>
            </Tr>
          ) : data.length === 0 ? (
            <Tr>
              <Td colSpan={columns.length} textAlign="center" py="8">
                Nenhum dado encontrado
              </Td>
            </Tr>
          ) : (
            data.map((row, index) => (
              <Tr
                key={index}
                onClick={() => onRowClick?.(row)}
                cursor={onRowClick ? 'pointer' : 'default'}
                className="transition-colors"
                _hover={{
                  bg: colorMode === 'light' ? 'gray.50' : 'gray.700',
                }}
              >
                {columns.map((column) => (
                  <Td
                    key={column.key}
                    textAlign={column.align || 'left'}
                    py="4"
                    px="6"
                    color={colorMode === 'light' ? 'gray.900' : 'gray.100'}
                    fontSize="sm"
                  >
                    {row[column.key]}
                  </Td>
                ))}
              </Tr>
            ))
          )}
        </Tbody>
      </ChakraTable>
    </div>
  );
};

export default Table; 