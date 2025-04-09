# Estratégia de Testes do Misa Cash

Este documento descreve a estratégia de testes adotada no projeto Misa Cash, abrangendo testes de backend, frontend e performance.

## Visão Geral

Nossa estratégia de testes segue uma abordagem em camadas:

1. **Testes Unitários**: Verificam componentes individuais do código.
2. **Testes de Integração**: Verificam a interação entre componentes.
3. **Testes de UI/UX**: Verificam a interface do usuário e a experiência do usuário.
4. **Testes de Performance**: Verificam o desempenho, escalabilidade e uso de recursos.

## Testes de Backend

### Testes Unitários e de Integração

Os testes de backend estão localizados em `src/web/backend/tests/` e são organizados por módulos:

- `test_auth.py`: Testes para autenticação e autorização.
- `test_users.py`: Testes para gerenciamento de usuários.
- `test_transactions.py`: Testes para criação, leitura, atualização e exclusão de transações.
- `test_reports.py`: Testes para relatórios e análises.

Utilizamos o framework **pytest** para executar os testes e **pytest-cov** para gerar relatórios de cobertura.

### Exemplos de Testes

```python
# Teste de criação de transação
def test_create_transaction(client, authenticated_headers):
    transaction_data = {
        "type": "expense",
        "amount": 100.00,
        "category": "food",
        "description": "Grocery shopping",
        "date": "2024-01-01"
    }
    
    response = client.post(
        "/api/transactions",
        data=json.dumps(transaction_data),
        headers=authenticated_headers,
        content_type="application/json"
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["type"] == "expense"
    assert data["amount"] == 100.00
```

### Como executar

```bash
cd src/web/backend

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=. tests/

# Executar testes específicos
pytest tests/test_transactions.py
```

## Testes de Frontend

### Testes de Componentes

Os testes de componentes do frontend estão localizados em `src/web/frontend/src/components/__tests__/` e verificam o comportamento de componentes React individuais:

- `Button.test.tsx`: Testes para o componente Button.
- `Input.test.tsx`: Testes para o componente Input.
- `Card.test.tsx`: Testes para o componente Card.
- `Table.test.tsx`: Testes para o componente Table.
- `Modal.test.tsx`: Testes para o componente Modal.
- `Form.test.tsx`: Testes para o componente Form.
- `Chart.test.tsx`: Testes para o componente Chart.
- `Alert.test.tsx`: Testes para o componente Alert.

Utilizamos **React Testing Library** e **Jest** para os testes de componentes.

### Testes de Integração

Os testes de integração do frontend estão localizados em `src/web/frontend/src/tests/integration/` e verificam a interação entre múltiplos componentes:

- `Form.integration.test.tsx`: Integração entre Form, Input, Button e Alert.
- `Modal.integration.test.tsx`: Integração entre Modal, Form, Button e Alert.
- `Table.integration.test.tsx`: Integração entre Table, Button, Input e Modal.
- `Chart.integration.test.tsx`: Integração entre Chart, Card e controles (Select, DatePicker).
- `Alert.integration.test.tsx`: Integração entre Alert e outros componentes.

### Exemplos de Testes

```typescript
// Teste de componente
test('renders Button with text', () => {
  render(<Button>Click me</Button>);
  const buttonElement = screen.getByText(/Click me/i);
  expect(buttonElement).toBeInTheDocument();
});

// Teste de integração
test('form submits with correct values and shows success', async () => {
  const mockSubmit = jest.fn();
  render(
    <Form onSubmit={mockSubmit}>
      <Input name="email" label="Email" />
      <Input name="password" type="password" label="Password" />
      <Button type="submit">Submit</Button>
    </Form>
  );
  
  fireEvent.change(screen.getByLabelText(/Email/i), {
    target: { value: 'test@example.com' }
  });
  
  fireEvent.change(screen.getByLabelText(/Password/i), {
    target: { value: 'password123' }
  });
  
  fireEvent.click(screen.getByText(/Submit/i));
  
  await waitFor(() => {
    expect(mockSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
});
```

### Como executar

```bash
cd src/web/frontend

# Executar todos os testes
npm test

# Executar com cobertura
npm test -- --coverage

# Executar em modo watch
npm test -- --watch
```

## Testes de Performance

### Ferramentas de Testes de Desempenho

Os testes de desempenho estão localizados em `src/web/backend/tests/performance/`:

1. **Locust** (`locustfile.py`): Para testes de carga e stress com múltiplos usuários.
2. **API Benchmark** (`api_benchmark.py`): Para benchmarking de endpoints específicos.
3. **DB Performance** (`db_performance.py`): Para testar o desempenho de consultas SQL.

### Testes de Carga com Locust

Permite simular múltiplos usuários executando diferentes cenários:

- Acesso ao dashboard
- Listagem de transações
- Criação de transações
- Geração de relatórios
- Atualização de perfil

### Benchmark de API

Mede o desempenho de endpoints específicos:

- Tempo médio de resposta
- Tempo mínimo e máximo
- Percentil 95 (P95)
- Taxa de sucesso

### Testes de Desempenho do Banco de Dados

Analisa o desempenho de consultas SQL:

- Seleção de todas as transações
- Seleção de transações recentes
- Consultas com filtros
- Resumo mensal
- Resumo por categoria
- Operações de inserção/atualização/exclusão

### Como executar

```bash
cd src/web/backend/tests/performance

# Testes de carga
locust -f locustfile.py

# Benchmark de API
python api_benchmark.py --url http://localhost:5000

# Testes de banco de dados
python db_performance.py --host localhost --user root --password YOUR_PASSWORD --database misa_cash
```

## Integração Contínua (CI)

Utilizamos GitHub Actions para automatizar a execução dos testes. Nosso pipeline de CI/CD inclui:

1. **Teste**: Executa testes unitários e de integração para o backend e frontend.
2. **Lint**: Verifica a qualidade do código usando ESLint, Flake8 e Black.
3. **Performance**: Executa testes de desempenho básicos.
4. **Build**: Compila o código para produção.
5. **Deploy**: Implanta a aplicação no ambiente de produção (somente na branch main).
6. **Security**: Analisa vulnerabilidades de segurança.

## Cobertura de Testes

Nosso objetivo é manter uma cobertura de testes de pelo menos:

- **Backend**: 85% de cobertura
- **Frontend**: 75% de cobertura

### Relatórios de Cobertura

Os relatórios de cobertura são gerados durante a execução do CI e podem ser visualizados no Codecov.

## Boas Práticas e Padrões

1. **Testes Isolados**: Cada teste deve ser independente e não afetar outros testes.
2. **Mocking**: Usar mocks para dependências externas como APIs ou bancos de dados.
3. **Nomeação clara**: Os nomes dos testes devem descrever claramente o que está sendo testado.
4. **Preparação e Limpeza**: Configurar os dados de teste necessários e limpar após o teste.
5. **Padrão AAA**: Arrange (preparar), Act (agir), Assert (verificar).

## Fluxo de Trabalho para Novos Recursos

1. Escrever testes unitários para a nova funcionalidade (TDD quando possível).
2. Implementar a funcionalidade até que os testes passem.
3. Adicionar testes de integração se necessário.
4. Verificar a cobertura de código e adicionar testes adicionais conforme necessário.
5. Realizar testes de desempenho para funcionalidades críticas.

## Problemas Comuns e Soluções

### Testes Intermitentes (Flaky Tests)

- **Problema**: Testes que passam às vezes e falham outras vezes.
- **Solução**: Identificar condições de corrida, usar esperas explícitas para operações assíncronas, isolar melhor os testes.

### Testes Lentos

- **Problema**: Suíte de testes leva muito tempo para executar.
- **Solução**: Usar mocks em vez de integrações reais, paralelizar a execução de testes, reduzir a quantidade de dados de teste.

### Testes Frágeis

- **Problema**: Testes que quebram com pequenas mudanças no código.
- **Solução**: Testar comportamento em vez de implementação, usar seletores robustos em testes de UI. 