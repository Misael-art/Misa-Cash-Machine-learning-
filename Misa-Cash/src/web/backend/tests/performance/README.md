# Testes de Desempenho (Performance) - Misa Cash

Este diretório contém ferramentas para testar o desempenho e a escalabilidade do backend do Misa Cash.

## Ferramentas disponíveis

### 1. Locust - Testes de Carga

O arquivo `locustfile.py` contém configurações para testes de carga usando o [Locust](https://locust.io/), uma ferramenta de teste de carga que permite simular múltiplos usuários simultâneos.

#### Pré-requisitos
```
pip install locust
```

#### Como executar
```
cd src/web/backend/tests/performance
locust -f locustfile.py
```

Após iniciar o Locust, acesse a interface web em http://localhost:8089 para configurar e iniciar os testes.

### 2. API Benchmark - Testes de Desempenho de Endpoints

O arquivo `api_benchmark.py` fornece uma ferramenta para medir o desempenho de endpoints específicos da API, calculando métricas como tempo médio de resposta, P95, taxa de sucesso, etc.

#### Pré-requisitos
```
pip install requests statistics
```

#### Como executar
```
python api_benchmark.py --url http://localhost:5000
```

#### Opções disponíveis
- `--url`: URL base da API (padrão: http://localhost:5000)
- `--email`: Email para login (padrão: test@example.com)
- `--password`: Senha para login (padrão: test123)
- `--iterations`: Número de iterações por endpoint (padrão: 50)
- `--compare`: Arquivo de resultados anteriores para comparação
- `--endpoint`: Executar apenas um endpoint específico (opções: dashboard, transactions, reports, create, profile)

#### Exemplos
```
# Executar todos os testes
python api_benchmark.py

# Testar apenas o endpoint de dashboard
python api_benchmark.py --endpoint dashboard --iterations 100

# Comparar resultados com uma execução anterior
python api_benchmark.py --compare benchmark_results_20240407_123045.json
```

### 3. DB Performance Tester - Testes de Desempenho do Banco de Dados

O arquivo `db_performance.py` permite medir o desempenho de consultas SQL específicas e operações de escrita no banco de dados.

#### Pré-requisitos
```
pip install pymysql matplotlib numpy
```

#### Como executar
```
python db_performance.py --host localhost --user root --password YOUR_PASSWORD --database misa_cash
```

#### Opções disponíveis
- `--host`: Host do banco de dados (padrão: localhost)
- `--port`: Porta do banco de dados (padrão: 3306)
- `--user`: Usuário do banco de dados (padrão: root)
- `--password`: Senha do banco de dados
- `--database`: Nome do banco de dados (padrão: misa_cash)
- `--iterations`: Número de iterações por teste (padrão: 50)
- `--test`: Executar apenas um teste específico

#### Testes disponíveis
- `select_all_transactions`: Desempenho da consulta que retorna todas as transações
- `select_recent_transactions`: Desempenho da consulta que retorna transações recentes
- `select_with_filter`: Desempenho da consulta com filtros
- `monthly_summary`: Desempenho da consulta de resumo mensal
- `category_summary`: Desempenho da consulta de resumo por categoria
- `insert_transaction`: Desempenho da inserção de transação
- `update_transaction`: Desempenho da atualização de transação
- `delete_transaction`: Desempenho da exclusão de transação
- `complex_report_query`: Desempenho de uma consulta complexa para relatório

#### Exemplos
```
# Executar todos os testes
python db_performance.py --password YOUR_PASSWORD

# Testar apenas consulta específica
python db_performance.py --password YOUR_PASSWORD --test complex_report_query

# Aumentar o número de iterações
python db_performance.py --password YOUR_PASSWORD --iterations 100
```

## Interpretando os Resultados

### Métricas importantes

1. **Tempo médio (avg_time)**: Tempo médio de resposta em milissegundos.
2. **Tempo P95 (p95_time)**: 95% das requisições são concluídas abaixo deste tempo.
3. **Taxa de sucesso (success_rate)**: Porcentagem de requisições bem-sucedidas.

### Diretrizes gerais

- Para APIs REST, tempos de resposta abaixo de 300ms são considerados excelentes.
- Para operações de banco de dados, tempos de resposta abaixo de 50ms são considerados ótimos.
- A taxa de sucesso deve ser maior que 99.5% em condições normais.

## Boas Práticas para Testes de Desempenho

1. **Execute em ambiente semelhante ao de produção**: Para obter resultados mais precisos.
2. **Execute regularmente**: Idealmente após cada sprint ou mudança significativa.
3. **Estabeleça linhas de base**: Compare os resultados com execuções anteriores para identificar regressões.
4. **Teste com volumes de dados realistas**: Use conjuntos de dados que se aproximem do uso real.
5. **Incremente gradualmente a carga**: Comece com poucos usuários e aumente para identificar o ponto de ruptura.

## Solução de Problemas Comuns

### API lenta
- Verifique se há queries N+1 no código
- Avalie a necessidade de índices no banco de dados
- Considere implementar caching

### Banco de dados lento
- Analise o plano de execução das queries
- Adicione índices apropriados
- Otimize as consultas que levam mais tempo 