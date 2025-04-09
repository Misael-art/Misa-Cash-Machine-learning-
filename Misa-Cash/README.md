# Misa Cash - Machine Learning para Análise Financeira

## Descrição
Sistema de análise financeira utilizando técnicas de Machine Learning para previsão de mercado e otimização de estratégias de investimento.

## Recursos Principais

- Gerenciamento de receitas e despesas
- Categorização de transações
- Relatórios e análises
- Dashboard com visualizações gráficas
- Suporte a múltiplos usuários
- Interfaces responsivas para web e mobile

## Estrutura do Projeto

```
Misa-Cash-Machine-learning/
├── docs/                    # Documentação
├── src/                     # Código fonte
│   ├── web/                 # Aplicação web
│   │   ├── backend/         # Backend (Python/Flask)
│   │   └── frontend/        # Frontend (React)
│   └── mobile/              # Aplicação móvel (React Native)
└── .github/                 # Configuração do GitHub
    └── workflows/           # GitHub Actions workflows
```

## Requisitos do Sistema

### Backend
- Python 3.10+
- MySQL 8.0+

### Frontend
- Node.js 18+
- npm 8+

### Mobile
- React Native 0.70+
- Android Studio / Xcode

## Configuração de Desenvolvimento

### Backend

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/Misa-Cash-Machine-learning.git
cd Misa-Cash-Machine-learning

# Configurar ambiente virtual
cd src/web/backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
python setup_db.py

# Iniciar servidor de desenvolvimento
python app.py
```

### Frontend

```bash
# Navegar para o diretório frontend
cd src/web/frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm start
```

## Testes

O projeto inclui testes unitários, de integração e de desempenho tanto para o backend quanto para o frontend.

### Executando Testes do Backend

```bash
cd src/web/backend

# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=. tests/

# Executar testes específicos
pytest tests/test_transactions.py
```

### Executando Testes do Frontend

```bash
cd src/web/frontend

# Executar todos os testes
npm test

# Executar testes com cobertura
npm test -- --coverage

# Executar testes em modo watch
npm test -- --watch
```

### Testes de Desempenho

Temos várias ferramentas para testes de desempenho disponíveis na pasta `src/web/backend/tests/performance/`:

#### Testes de Carga com Locust

```bash
cd src/web/backend/tests/performance
pip install locust
locust -f locustfile.py
```

Acesse http://localhost:8089 para iniciar os testes.

#### Benchmark de API

```bash
cd src/web/backend/tests/performance
python api_benchmark.py --url http://localhost:5000
```

#### Testes de Desempenho do Banco de Dados

```bash
cd src/web/backend/tests/performance
python db_performance.py --host localhost --user root --password YOUR_PASSWORD --database misa_cash
```

Para mais detalhes, consulte o [README dos testes de desempenho](src/web/backend/tests/performance/README.md).

## Integração Contínua e Entrega Contínua (CI/CD)

O projeto utiliza GitHub Actions para automatizar os fluxos de trabalho de CI/CD. Os workflows estão definidos em `.github/workflows/ci-cd.yml` e incluem:

- **Testes**: Executa testes unitários e de integração para o backend e frontend.
- **Linting**: Verifica a qualidade do código usando ESLint para JavaScript e Flake8/Black para Python.
- **Testes de Desempenho**: Executa testes de benchmark e de carga.
- **Build**: Compila o código para produção.
- **Deploy**: Implanta a aplicação no ambiente de produção (somente na branch main).
- **Análise de Segurança**: Verifica vulnerabilidades nas dependências e no código.

Para configurar o CI/CD, você precisará adicionar os seguintes segredos ao seu repositório GitHub:

- `SSH_PRIVATE_KEY`: Chave SSH para acessar o servidor de produção
- `DEPLOY_USER`: Usuário para login no servidor
- `DEPLOY_HOST`: Endereço do servidor
- `SNYK_TOKEN`: Token para o serviço Snyk (análise de segurança)

## Contribuindo

1. Fork o repositório
2. Crie um branch para sua feature (`git checkout -b feature/amazing-feature`)
3. Faça commit das suas mudanças (`git commit -m 'feat: add amazing feature'`)
4. Envie para o branch remoto (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

### Padrões de Código

- Utilizamos [Conventional Commits](https://www.conventionalcommits.org/) para mensagens de commit
- Código Python deve seguir PEP 8 e ser formatado com Black
- Código JavaScript deve seguir as regras do ESLint configuradas

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Email do Projeto: projeto@misacash.com 