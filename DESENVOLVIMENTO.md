# Instruções para Desenvolvimento

Este documento contém instruções para configurar o ambiente de desenvolvimento para o projeto Misa-Cash.

## Configuração do Ambiente

### Opção 1: Instalação em modo desenvolvimento

Com esta opção, você instala o pacote em "modo de desenvolvimento", o que significa que alterações no código são refletidas imediatamente sem precisar reinstalar o pacote.

```bash
# Clonar o repositório
git clone https://github.com/Misael-art/Misa-Cash-Machine-learning-.git
cd Misa-Cash-Machine-learning-

# Criar e ativar ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate.ps1
# Linux/MacOS
source venv/bin/activate

# Instalar em modo desenvolvimento
pip install -e .[dev]
```

### Opção 2: Configuração manual do PYTHONPATH

Se preferir não instalar o pacote, você pode configurar a variável de ambiente PYTHONPATH para incluir o diretório `src`:

```bash
# Windows (PowerShell)
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)\src"

# Linux/MacOS
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

## Executando a Aplicação

```bash
cd src/web/backend
python run.py
```

## Executando os Testes

```bash
# Na raiz do projeto
pytest src/web/backend/tests

# Ou para testes específicos
pytest src/web/backend/tests/test_transactions.py
```

## Estrutura do Pacote

O pacote Python tem a seguinte estrutura:

```
misa_cash/
└── web/
    ├── backend/
    │   ├── app/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   └── routes.py
    │   ├── tests/
    │   │   ├── __init__.py
    │   │   └── test_transactions.py
    │   └── run.py
    └── frontend/ (apenas estrutura inicial)
```

## Convenções de Código

- Seguimos a PEP 8 para estilo de código Python
- Utilizamos Black e isort para formatação automática
- Documentamos funções e classes usando docstrings no estilo Google
- Escrevemos testes unitários para todas as funcionalidades

## Fluxo de Trabalho com Git

1. Crie uma branch para sua feature: `git checkout -b feature/nome-da-feature`
2. Faça suas alterações
3. Execute os testes: `pytest`
4. Formate o código: `black .` e `isort .`
5. Commit e push: `git commit -m "Descrição da alteração"` e `git push origin feature/nome-da-feature`
6. Abra um Pull Request no GitHub 