import React, { useEffect, useState } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  Text,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  useDisclosure
} from '@chakra-ui/react';
import { useBudget } from '../../contexts/BudgetContext';

interface BudgetDeleteModalProps {
  isOpen: boolean;
  onClose: () => void;
  budgetId: string | null;
}

const BudgetDeleteModal: React.FC<BudgetDeleteModalProps> = ({
  isOpen,
  onClose,
  budgetId
}) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const { deleteBudget, getBudgetById } = useBudget();
  const [budgetName, setBudgetName] = useState('');
  const cancelRef = React.useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen && budgetId) {
      const budget = getBudgetById(budgetId);
      if (budget) {
        setBudgetName(budget.name);
      }
    }
  }, [isOpen, budgetId, getBudgetById]);

  const handleDelete = async () => {
    if (!budgetId) return;
    
    setIsDeleting(true);
    try {
      await deleteBudget(budgetId);
      onClose();
    } catch (error) {
      console.error('Erro ao excluir orçamento:', error);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <AlertDialog
      isOpen={isOpen}
      leastDestructiveRef={cancelRef}
      onClose={onClose}
    >
      <AlertDialogOverlay>
        <AlertDialogContent>
          <AlertDialogHeader fontSize="lg" fontWeight="bold">
            Excluir Orçamento
          </AlertDialogHeader>

          <AlertDialogBody>
            <Text>
              Tem certeza que deseja excluir o orçamento <strong>{budgetName}</strong>?
            </Text>
            <Text mt={2} fontSize="sm" color="gray.500">
              Esta ação não pode ser desfeita.
            </Text>
          </AlertDialogBody>

          <AlertDialogFooter>
            <Button ref={cancelRef} onClick={onClose}>
              Cancelar
            </Button>
            <Button
              colorScheme="red"
              onClick={handleDelete}
              ml={3}
              isLoading={isDeleting}
              loadingText="Excluindo"
            >
              Excluir
            </Button>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialogOverlay>
    </AlertDialog>
  );
};

export default BudgetDeleteModal; 