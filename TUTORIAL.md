# Tutorial do Misa-Cash

Este documento fornece instruções detalhadas para instalação, configuração e uso do sistema Misa-Cash.

## Sobre o Misa-Cash

O Misa-Cash é um sistema de gerenciamento financeiro com recursos de Machine Learning que permite o controle detalhado de receitas e despesas. O objetivo principal é fornecer uma visão clara da situação financeira do usuário e ajudar na tomada de decisões com base em análises e previsões inteligentes.

### Principais Recursos (Planejados)

- Registro e categorização de receitas e despesas
- Dashboard interativo com resumo financeiro
- Relatórios detalhados e personalizáveis
- Previsões de gastos futuros usando IA
- Detecção de padrões de gastos e anomalias
- Recomendações personalizadas para economia
- Definição e acompanhamento de metas financeiras

## Requisitos do Sistema

- **Sistema Operacional**: Windows 10/11, macOS ou Linux
- **Python**: 3.7 ou superior
- **Node.js**: 14.x ou superior (para o frontend)
- **Navegador web**: Chrome, Firefox, Edge (versões recentes)
- **Espaço em disco**: Mínimo 500MB
- **Memória RAM**: Mínimo 4GB (recomendado 8GB)

## Instalação Passo a Passo

### 1. Clone o Repositório

```bash
git clone https://github.com/Misael-art/Misa-Cash-Machine-learning-.git
cd Misa-Cash-Machine-learning-
```

### 2. Configuração do Backend

#### Criação do Ambiente Virtual

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate.ps1

# Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

#### Instalação das Dependências

```bash
# Instalar o pacote em modo desenvolvimento
pip install -e .

# Para desenvolvedores, instale também as ferramentas de desenvolvimento
pip install -e .[dev]
```

#### Inicialização do Banco de Dados

```bash
cd src/web/backend
flask --app run init-db
```

Você deverá ver a mensagem "Banco de dados inicializado." confirmando a criação do banco de dados SQLite.

#### Execução do Backend

```bash
python run.py
```

O servidor backend será iniciado em `http://localhost:5000`. Você verá uma mensagem semelhante a:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Mantenha esta janela de terminal aberta enquanto estiver usando o sistema.

### 3. Configuração do Frontend (Quando Disponível)

#### Instalação das Dependências

```bash
cd src/web/frontend
npm install
```

#### Execução do Frontend

```bash
npm start
```

O aplicativo frontend será iniciado em `http://localhost:3000` e abrirá automaticamente em seu navegador padrão.

## Guia de Uso

### Navegação na Interface (Quando Disponível)

A interface do Misa-Cash é organizada nas seguintes seções principais:

- **Dashboard**: Visão geral das finanças
- **Transações**: Gerenciamento de receitas e despesas
- **Relatórios**: Análises detalhadas
- **Previsões**: Insights baseados em IA
- **Configurações**: Preferências e configurações de conta

### Página Inicial (Dashboard)

Ao acessar o sistema, você será direcionado para o Dashboard, que exibirá:

- **Resumo Financeiro**: Receitas, despesas e saldo do período atual
- **Gráfico de Evolução**: Saldo ao longo do tempo
- **Distribuição por Categoria**: Gráfico de pizza com gastos por categoria
- **Transações Recentes**: Lista das últimas movimentações
- **Alertas e Recomendações**: Avisos sobre gastos anormais e dicas personalizadas

### Gerenciamento de Transações

#### Adicionar Nova Transação

1. Clique no botão "Nova Transação" no menu lateral ou no Dashboard
2. Preencha os dados no formulário:
   - **Descrição**: Breve descrição da transação (ex: "Mercado Semanal")
   - **Valor**: Montante da transação (ex: 150.75)
   - **Tipo**: Selecione "Receita" ou "Despesa"
   - **Data**: Data em que a transação ocorreu
   - **Categoria**: Selecione a categoria apropriada da lista
   - **Notas**: Informações adicionais (opcional)
3. Clique em "Salvar"
4. Uma confirmação será exibida e a transação aparecerá na lista de transações

#### Visualizar Transações

1. Acesse "Transações" no menu lateral
2. A tabela mostrará todas as suas transações com as seguintes informações:
   - Data
   - Descrição
   - Categoria
   - Valor (em vermelho para despesas, verde para receitas)
3. Use os filtros disponíveis para encontrar transações específicas:
   - **Período**: Defina o intervalo de datas
   - **Categoria**: Filtre por categorias específicas
   - **Tipo**: Filtre por receitas ou despesas
   - **Pesquisa**: Busque por texto na descrição ou notas
4. Clique no cabeçalho das colunas para ordenar as transações

#### Editar ou Excluir Transação

1. Na lista de transações, clique na transação desejada
2. Um painel de detalhes será exibido com todas as informações
3. Clique no botão "Editar" para modificar os dados
4. Faça as alterações necessárias e clique em "Salvar"
5. Para excluir, clique em "Excluir" e confirme a ação quando solicitado

### Relatórios

1. Acesse "Relatórios" no menu lateral
2. Escolha o tipo de relatório:
   - **Relatório Mensal**: Visão geral do mês selecionado
   - **Relatório por Categoria**: Análise detalhada por categoria
   - **Fluxo de Caixa**: Entradas e saídas ao longo do tempo
   - **Comparativo**: Compare períodos diferentes
3. Configure os parâmetros do relatório:
   - Período de análise
   - Categorias a incluir
   - Tipo de visualização (gráfico, tabela)
4. Visualize os resultados em diferentes formatos:
   - Gráficos interativos
   - Tabelas detalhadas
   - Indicadores principais
5. Exporte o relatório para:
   - PDF para impressão
   - Excel para análise adicional
   - CSV para importação em outros sistemas

### Recursos de Machine Learning (Quando Disponíveis)

#### Previsão de Gastos

1. Acesse "Previsões" no menu lateral
2. Visualize a previsão de gastos para o próximo mês:
   - Gráfico comparativo com meses anteriores
   - Previsão por categoria
   - Intervalo de confiança da previsão
3. Ajuste parâmetros da previsão:
   - Período base para a análise
   - Inclusão/exclusão de transações excepcionais
4. Consulte recomendações personalizadas:
   - Sugestões de economia baseadas no seu padrão de gastos
   - Alertas sobre categorias com crescimento consistente

#### Detecção de Anomalias

1. No Dashboard, observe alertas sobre gastos incomuns
2. Os alertas são identificados por:
   - Ícone de atenção
   - Cor destacada (geralmente amarelo ou vermelho)
3. Clique no alerta para mais detalhes:
   - Comparação com seu padrão histórico
   - Justificativa para o alerta
   - Opção para marcar como "esperado" ou "não esperado"
4. Use estas informações para:
   - Identificar gastos desnecessários
   - Detectar cobranças indevidas
   - Reconhecer mudanças nos seus hábitos financeiros

### Perfil e Configurações

1. Clique no ícone de perfil no canto superior direito
2. Acesse "Configurações" para personalizar:
   - **Perfil**: Informações pessoais e senha
   - **Notificações**: Configure alertas por email ou push
   - **Categorias**: Personalize as categorias de transações
   - **Metas**: Defina objetivos financeiros
   - **Tema**: Escolha entre tema claro ou escuro
   - **Moeda**: Defina sua moeda principal
   - **Exportação de Dados**: Faça backup dos seus dados

## Recursos via API REST

Para desenvolvedores, o Misa-Cash oferece uma API REST completa:

### Endpoints Principais

- `GET /api/transactions` - Lista todas as transações
- `GET /api/transactions/<id>` - Obtém detalhes de uma transação
- `POST /api/transactions` - Cria nova transação
- `PUT /api/transactions/<id>` - Atualiza uma transação
- `DELETE /api/transactions/<id>` - Remove uma transação
- `GET /api/transactions/summary` - Obtém resumo financeiro

### Exemplo de Uso da API

```python
import requests
import json

# Criar uma nova transação
transaction = {
    "description": "Supermercado",
    "amount": 120.50,
    "type": "expense",
    "date": "2023-04-15",
    "category": "Alimentação"
}

response = requests.post(
    "http://localhost:5000/api/transactions",
    data=json.dumps(transaction),
    headers={"Content-Type": "application/json"}
)

print(response.json())
```

## Solução de Problemas

### Backend não Inicia

- **Problema**: Erro ao iniciar o servidor Flask
- **Solução**: 
  - Verifique se todas as dependências foram instaladas
  - Confira se o Python está no PATH do sistema
  - Verifique se a porta 5000 está disponível (use `netstat -an | findstr 5000`)
  - Verifique se o banco de dados foi inicializado corretamente

### Erro: "ModuleNotFoundError"

- **Problema**: Python não encontra módulos necessários
- **Solução**:
  - Certifique-se de que o ambiente virtual está ativado
  - Reinstale as dependências: `pip install -e .`
  - Verifique se o diretório do projeto está no PYTHONPATH

### Frontend não Conecta ao Backend

- **Problema**: Frontend não consegue acessar a API
- **Solução**:
  - Verifique se o backend está em execução
  - Confira as configurações de CORS no backend
  - Verifique a URL da API nas configurações do frontend
  - Tente `curl http://localhost:5000/api/health` para testar a API

### Erro ao Adicionar Transações

- **Problema**: Falha ao salvar transações
- **Solução**:
  - Verifique se todos os campos obrigatórios foram preenchidos
  - Confirme que o formato da data está correto (YYYY-MM-DD)
  - Verifique a conexão com o banco de dados
  - Consulte os logs de erro do backend

## Limitações Atuais

- O sistema ainda está em desenvolvimento e muitas funcionalidades estão planejadas, mas não implementadas
- O frontend ainda não foi desenvolvido
- Os recursos de Machine Learning serão implementados em fases futuras
- Atualmente só suporta banco de dados SQLite local
- Não há suporte para múltiplos usuários
- Backup automático não está disponível

## Contribuindo com o Projeto

Se você deseja contribuir com o desenvolvimento do Misa-Cash, consulte o arquivo DESENVOLVIMENTO.md para obter instruções detalhadas sobre o ambiente de desenvolvimento e o fluxo de trabalho com Git.

## Contato e Suporte

Para problemas, sugestões ou dúvidas:

- **GitHub**: [github.com/Misael-art/Misa-Cash-Machine-learning-](https://github.com/Misael-art/Misa-Cash-Machine-learning-)
- **Email**: misael.junio.oliveira@gmail.com 