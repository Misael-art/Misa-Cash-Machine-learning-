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
  FormControl,
  FormLabel,
  Input,
  FormErrorMessage,
  Select,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  VStack,
  useToast
} from '@chakra-ui/react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Budget } from '../../types/Budget';
import { useBudget } from '../../contexts/BudgetContext';
import { useCategory } from '../../contexts/CategoryContext';

interface BudgetFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  budgetId: string | null;
}

const BudgetFormModal: React.FC<BudgetFormModalProps> = ({
  isOpen,
  onClose,
  budgetId
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { budgets, createBudget, updateBudget, getBudgetById } = useBudget();
  const { categories } = useCategory();
  const toast = useToast();

  const BudgetSchema = Yup.object().shape({
    name: Yup.string().required('Nome é obrigatório'),
    amount: Yup.number()
      .required('Valor é obrigatório')
      .positive('Valor deve ser positivo'),
    categoryId: Yup.string().required('Categoria é obrigatória'),
    startDate: Yup.date().required('Data inicial é obrigatória'),
    endDate: Yup.date()
      .required('Data final é obrigatória')
      .min(Yup.ref('startDate'), 'Data final deve ser posterior à data inicial')
  });

  const formik = useFormik({
    initialValues: {
      name: '',
      amount: 0,
      categoryId: '',
      startDate: new Date().toISOString().split('T')[0],
      endDate: new Date(new Date().setMonth(new Date().getMonth() + 1))
        .toISOString()
        .split('T')[0]
    },
    validationSchema: BudgetSchema,
    onSubmit: async (values) => {
      setIsSubmitting(true);
      try {
        if (budgetId) {
          await updateBudget(budgetId, values);
          toast({
            title: 'Orçamento atualizado',
            description: 'O orçamento foi atualizado com sucesso.',
            status: 'success',
            duration: 3000,
            isClosable: true
          });
        } else {
          await createBudget(values);
          toast({
            title: 'Orçamento criado',
            description: 'O orçamento foi criado com sucesso.',
            status: 'success',
            duration: 3000,
            isClosable: true
          });
        }
        onClose();
      } catch (error) {
        console.error('Erro ao salvar orçamento:', error);
        toast({
          title: 'Erro',
          description: 'Ocorreu um erro ao salvar o orçamento.',
          status: 'error',
          duration: 3000,
          isClosable: true
        });
      } finally {
        setIsSubmitting(false);
      }
    }
  });

  useEffect(() => {
    if (isOpen) {
      if (budgetId) {
        const budget = getBudgetById(budgetId);
        if (budget) {
          formik.setValues({
            name: budget.name,
            amount: budget.amount,
            categoryId: budget.categoryId,
            startDate: new Date(budget.startDate).toISOString().split('T')[0],
            endDate: new Date(budget.endDate).toISOString().split('T')[0]
          });
        }
      } else {
        formik.resetForm();
      }
    }
  }, [isOpen, budgetId]);

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="md">
      <ModalOverlay />
      <ModalContent>
        <form onSubmit={formik.handleSubmit}>
          <ModalHeader>
            {budgetId ? 'Editar Orçamento' : 'Novo Orçamento'}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4}>
              <FormControl
                isInvalid={!!(formik.touched.name && formik.errors.name)}
                isRequired
              >
                <FormLabel>Nome</FormLabel>
                <Input
                  id="name"
                  name="name"
                  value={formik.values.name}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                />
                <FormErrorMessage>{formik.errors.name}</FormErrorMessage>
              </FormControl>

              <FormControl
                isInvalid={!!(formik.touched.amount && formik.errors.amount)}
                isRequired
              >
                <FormLabel>Valor</FormLabel>
                <NumberInput
                  min={0}
                  value={formik.values.amount}
                  onChange={(valueString) =>
                    formik.setFieldValue('amount', parseFloat(valueString))
                  }
                >
                  <NumberInputField id="amount" name="amount" />
                  <NumberInputStepper>
                    <NumberIncrementStepper />
                    <NumberDecrementStepper />
                  </NumberInputStepper>
                </NumberInput>
                <FormErrorMessage>{formik.errors.amount}</FormErrorMessage>
              </FormControl>

              <FormControl
                isInvalid={!!(formik.touched.categoryId && formik.errors.categoryId)}
                isRequired
              >
                <FormLabel>Categoria</FormLabel>
                <Select
                  id="categoryId"
                  name="categoryId"
                  placeholder="Selecione uma categoria"
                  value={formik.values.categoryId}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                >
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </Select>
                <FormErrorMessage>{formik.errors.categoryId}</FormErrorMessage>
              </FormControl>

              <FormControl
                isInvalid={!!(formik.touched.startDate && formik.errors.startDate)}
                isRequired
              >
                <FormLabel>Data Inicial</FormLabel>
                <Input
                  id="startDate"
                  name="startDate"
                  type="date"
                  value={formik.values.startDate}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                />
                <FormErrorMessage>{formik.errors.startDate}</FormErrorMessage>
              </FormControl>

              <FormControl
                isInvalid={!!(formik.touched.endDate && formik.errors.endDate)}
                isRequired
              >
                <FormLabel>Data Final</FormLabel>
                <Input
                  id="endDate"
                  name="endDate"
                  type="date"
                  value={formik.values.endDate}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                />
                <FormErrorMessage>{formik.errors.endDate}</FormErrorMessage>
              </FormControl>
            </VStack>
          </ModalBody>

          <ModalFooter>
            <Button variant="outline" mr={3} onClick={onClose}>
              Cancelar
            </Button>
            <Button
              colorScheme="teal"
              type="submit"
              isLoading={isSubmitting}
              loadingText="Salvando"
            >
              Salvar
            </Button>
          </ModalFooter>
        </form>
      </ModalContent>
    </Modal>
  );
};

export default BudgetFormModal; 