# Misa-Cash

Uma aplicação para gerenciamento de finanças pessoais, desenvolvida com Python Flask no backend e React no frontend, com recursos de Machine Learning para análise e previsão de gastos.

## Estrutura do Projeto

```
Misa-Cash-Machine-learning-/
│
├── src/                      # Código fonte
│   └── web/
│       ├── backend/          # API Flask
│       │   ├── app/          # Código da aplicação
│       │   ├── tests/        # Testes da aplicação
│       │   └── run.py        # Script para executar a aplicação
│       │
│       └── frontend/         # Aplicação React (a ser desenvolvida)
│
├── setup.py                  # Configuração do pacote Python
├── DESENVOLVIMENTO.md        # Instruções detalhadas para desenvolvimento
└── README.md                 # Este arquivo
```

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