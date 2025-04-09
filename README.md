# Misa-Cash

Uma aplicação para gerenciamento de finanças pessoais, desenvolvida com Python Flask no backend e React no frontend, com recursos de Machine Learning para análise e previsão de gastos.

## Estrutura do Projeto

A estrutura do projeto Misa-Cash foi organizada da seguinte forma:

```
Misa-Cash-Machine-Learning/
├── src/                       # Código fonte principal do projeto
│   ├── ml/                    # Módulos de Machine Learning
│   │   ├── api/               # API para integração dos serviços de ML
│   │   ├── config/            # Configurações dos modelos de ML
│   │   ├── data/              # Processamento de dados para ML
│   │   ├── models/            # Implementação dos modelos preditivos
│   │   └── utils/             # Utilitários para visualização e análise
│   ├── web/                   # Aplicação web (backend e frontend)
│   │   ├── backend/           # API REST e lógica de negócio
│   │   └── frontend/          # Interface de usuário (React)
│   ├── backend/               # Componentes adicionais do backend
│   └── frontend/              # Componentes adicionais do frontend
├── scripts/                   # Scripts de automação e utilidades
├── venv/                      # Ambiente virtual Python (não versionado)
├── ROADMAP.md                 # Planejamento e acompanhamento do projeto
├── setup.py                   # Configuração do pacote Python
└── README.md                  # Documentação principal
```

### Diretrizes de Desenvolvimento

1. **Desenvolvimento Principal**: Todo novo código deve ser adicionado ao diretório raiz do projeto, seguindo a estrutura acima.

2. **Módulo de Machine Learning**: Desenvolva os modelos de ML e suas visualizações em `src/ml/`.

3. **Diretório `Misa-Cash-Machine-learning-`**: Este é um submódulo que reflete o repositório GitHub. Não desenvolva código diretamente nele.

4. **Diretório `Misa-Cash`**: Este diretório contém a estrutura original do projeto e serve como referência. O desenvolvimento ativo deve acontecer nos diretórios principais do projeto e não dentro deste diretório.

### Fluxo de Trabalho Recomendado

1. Desenvolva novas funcionalidades em `src/`
2. Execute os testes com `python run_tests.py`
3. Execute a aplicação com `python run_app.py`
4. Utilize `git add` e `git commit` para versionar as alterações
5. Utilize `git push` para enviar as alterações para o repositório GitHub

Esta estrutura evita duplicação de código e mantém o projeto organizado para facilitar o desenvolvimento futuro.

## Instalação Rápida

O projeto está configurado como um pacote Python, facilitando a instalação e o desenvolvimento:

```bash
# Clonar o repositório
git clone https://github.com/Misael-art/Misa-Cash-Machine-learning-.git
cd Misa-Cash-Machine-learning-

# Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate.ps1  # Para Windows com PowerShell
# OU
source venv/bin/activate   # Para Linux/macOS

# Instalar o pacote em modo desenvolvimento
pip install -e .
```

Para mais detalhes sobre desenvolvimento, consulte [DESENVOLVIMENTO.md](DESENVOLVIMENTO.md).

## Executando a Aplicação

```bash
cd src/web/backend
python run.py
```

A API estará disponível em `http://localhost:5000/api`.

## API Endpoints

### Transações

- `GET /api/transactions` - Lista todas as transações
- `GET /api/transactions/<id>` - Obtém uma transação específica
- `POST /api/transactions` - Cria uma nova transação
- `PUT /api/transactions/<id>` - Atualiza uma transação existente
- `DELETE /api/transactions/<id>` - Remove uma transação
- `GET /api/transactions/summary` - Obtém um resumo das transações (receitas, despesas e saldo)

## Funcionalidades

- Registro de receitas e despesas
- Categorização das transações
- Resumo financeiro
- (Mais funcionalidades serão adicionadas)

## Machine Learning (Planejado)

Futuramente, o projeto incluirá recursos de Machine Learning:

- Previsão de gastos
- Detecção de anomalias nas transações
- Recomendações de economia
- Análise de padrões de gastos

## Licença

Este projeto está licenciado sob a licença MIT. 