import time
import statistics
import json
import argparse
import sys
import random
from datetime import datetime, timedelta
import pymysql
import matplotlib.pyplot as plt
import numpy as np

class DBPerformanceTester:
    """Classe para testar a performance do banco de dados"""
    
    def __init__(self, host="localhost", port=3306, user="root", password="", database="misa_cash"):
        self.connection_params = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor
        }
        self.connection = None
        self.results = {}
        
    def connect(self):
        """Conecta ao banco de dados"""
        try:
            self.connection = pymysql.connect(**self.connection_params)
            print("Conexão ao banco de dados realizada com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False
            
    def disconnect(self):
        """Desconecta do banco de dados"""
        if self.connection:
            self.connection.close()
            print("Conexão fechada")
            
    def execute_query(self, query, params=None):
        """Executa uma consulta SQL"""
        if not self.connection:
            raise Exception("Não conectado ao banco de dados")
            
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
            
    def execute_write(self, query, params=None):
        """Executa uma operação de escrita (INSERT, UPDATE, DELETE)"""
        if not self.connection:
            raise Exception("Não conectado ao banco de dados")
            
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.rowcount
    
    def benchmark_query(self, name, query, params=None, iterations=50):
        """Realiza benchmark de uma consulta SQL"""
        if not self.connection and not self.connect():
            return False
            
        print(f"Iniciando benchmark para {name}...")
        times = []
        rows_counts = []
        
        for i in range(iterations):
            sys.stdout.write(f"\rIteração {i+1}/{iterations}")
            sys.stdout.flush()
            
            start_time = time.time()
            
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                results = cursor.fetchall()
                rows_count = len(results)
                
            end_time = time.time()
            query_time = (end_time - start_time) * 1000  # converter para milissegundos
            times.append(query_time)
            rows_counts.append(rows_count)
        
        # Calcular estatísticas
        avg_time = statistics.mean(times)
        median_time = statistics.median(times)
        min_time = min(times)
        max_time = max(times)
        p95_time = sorted(times)[int(iterations * 0.95)]
        avg_rows = statistics.mean(rows_counts)
        
        # Armazenar resultados
        self.results[name] = {
            "avg_time": avg_time,
            "median_time": median_time,
            "min_time": min_time,
            "max_time": max_time,
            "p95_time": p95_time,
            "avg_rows": avg_rows,
            "sample_size": iterations,
            "type": "query"
        }
        
        # Exibir resultados
        print(f"\nResultados para {name}:")
        print(f"  Tempo médio: {avg_time:.2f} ms")
        print(f"  Tempo mediano: {median_time:.2f} ms")
        print(f"  Tempo mínimo: {min_time:.2f} ms")
        print(f"  Tempo máximo: {max_time:.2f} ms")
        print(f"  Tempo P95: {p95_time:.2f} ms")
        print(f"  Linhas retornadas (média): {avg_rows:.1f}")
        print(f"  Tamanho da amostra: {iterations}")
        print()
        
        return self.results[name]
    
    def benchmark_write(self, name, query_template, param_generator, iterations=20):
        """Realiza benchmark de operações de escrita (INSERT, UPDATE, DELETE)"""
        if not self.connection and not self.connect():
            return False
            
        print(f"Iniciando benchmark de escrita para {name}...")
        times = []
        affected_rows = []
        
        for i in range(iterations):
            sys.stdout.write(f"\rIteração {i+1}/{iterations}")
            sys.stdout.flush()
            
            # Gerar parâmetros para a consulta
            params = param_generator()
            
            start_time = time.time()
            
            with self.connection.cursor() as cursor:
                cursor.execute(query_template, params)
                self.connection.commit()
                rows_affected = cursor.rowcount
                
            end_time = time.time()
            write_time = (end_time - start_time) * 1000  # converter para milissegundos
            times.append(write_time)
            affected_rows.append(rows_affected)
        
        # Calcular estatísticas
        avg_time = statistics.mean(times)
        median_time = statistics.median(times)
        min_time = min(times)
        max_time = max(times)
        p95_time = sorted(times)[int(iterations * 0.95)]
        avg_affected = statistics.mean(affected_rows)
        
        # Armazenar resultados
        self.results[name] = {
            "avg_time": avg_time,
            "median_time": median_time,
            "min_time": min_time,
            "max_time": max_time,
            "p95_time": p95_time,
            "avg_affected_rows": avg_affected,
            "sample_size": iterations,
            "type": "write"
        }
        
        # Exibir resultados
        print(f"\nResultados para {name}:")
        print(f"  Tempo médio: {avg_time:.2f} ms")
        print(f"  Tempo mediano: {median_time:.2f} ms")
        print(f"  Tempo mínimo: {min_time:.2f} ms")
        print(f"  Tempo máximo: {max_time:.2f} ms")
        print(f"  Tempo P95: {p95_time:.2f} ms")
        print(f"  Linhas afetadas (média): {avg_affected:.1f}")
        print(f"  Tamanho da amostra: {iterations}")
        print()
        
        return self.results[name]
        
    def random_transaction_params(self):
        """Gera parâmetros aleatórios para uma transação"""
        types = ["income", "expense"]
        categories = ["food", "transport", "entertainment", "salary", "bonus", "utilities", "rent"]
        
        # Gerar data aleatória no último ano
        days_back = random.randint(0, 365)
        transaction_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        return {
            "user_id": 1,  # Usuário de teste
            "type": random.choice(types),
            "amount": round(random.uniform(10, 1000), 2),
            "category": random.choice(categories),
            "description": f"Test transaction {random.randint(1000, 9999)}",
            "date": transaction_date,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def test_select_all_transactions(self, iterations=50):
        """Testa desempenho da consulta que retorna todas as transações"""
        query = "SELECT * FROM transactions WHERE user_id = 1"
        return self.benchmark_query("Select All Transactions", query, iterations=iterations)
    
    def test_select_recent_transactions(self, iterations=50):
        """Testa desempenho da consulta que retorna transações recentes"""
        query = """
            SELECT * FROM transactions 
            WHERE user_id = 1 
            ORDER BY date DESC 
            LIMIT 10
        """
        return self.benchmark_query("Recent Transactions", query, iterations=iterations)
    
    def test_select_with_filter(self, iterations=50):
        """Testa desempenho da consulta com filtro por tipo e categoria"""
        query = """
            SELECT * FROM transactions 
            WHERE user_id = 1 
            AND type = 'expense' 
            AND category = 'food'
        """
        return self.benchmark_query("Filtered Transactions", query, iterations=iterations)
    
    def test_monthly_summary(self, iterations=30):
        """Testa desempenho da consulta de resumo mensal"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        query = """
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expenses,
                SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) as balance
            FROM transactions 
            WHERE user_id = 1 
            AND MONTH(date) = %s
            AND YEAR(date) = %s
        """
        return self.benchmark_query(
            "Monthly Summary", 
            query, 
            params=(current_month, current_year),
            iterations=iterations
        )
    
    def test_category_summary(self, iterations=30):
        """Testa desempenho da consulta de resumo por categoria"""
        query = """
            SELECT 
                category,
                SUM(amount) as total_amount,
                COUNT(*) as transaction_count
            FROM transactions 
            WHERE user_id = 1 
            GROUP BY category
            ORDER BY total_amount DESC
        """
        return self.benchmark_query("Category Summary", query, iterations=iterations)
    
    def test_insert_transaction(self, iterations=20):
        """Testa desempenho da inserção de transação"""
        query = """
            INSERT INTO transactions 
            (user_id, type, amount, category, description, date, created_at)
            VALUES 
            (%(user_id)s, %(type)s, %(amount)s, %(category)s, %(description)s, %(date)s, %(created_at)s)
        """
        return self.benchmark_write(
            "Insert Transaction", 
            query, 
            self.random_transaction_params,
            iterations=iterations
        )
    
    def test_update_transaction(self, iterations=20):
        """Testa desempenho da atualização de transação"""
        # Primeiro, obter IDs de transações existentes
        try:
            transaction_ids = self.execute_query(
                "SELECT id FROM transactions WHERE user_id = 1 LIMIT 100"
            )
            transaction_ids = [row['id'] for row in transaction_ids]
            
            if not transaction_ids:
                print("Nenhuma transação encontrada para atualizar. Pulando teste.")
                return None
                
            def update_params_generator():
                return {
                    "id": random.choice(transaction_ids),
                    "amount": round(random.uniform(10, 1000), 2),
                    "description": f"Updated transaction {random.randint(1000, 9999)}",
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
            query = """
                UPDATE transactions 
                SET amount = %(amount)s, 
                    description = %(description)s,
                    updated_at = %(updated_at)s
                WHERE id = %(id)s
            """
            return self.benchmark_write(
                "Update Transaction", 
                query, 
                update_params_generator,
                iterations=iterations
            )
        except Exception as e:
            print(f"Erro ao testar atualização: {e}")
            return None
    
    def test_delete_transaction(self, iterations=10):
        """Testa desempenho da exclusão de transação"""
        # Inserir transações temporárias para teste de exclusão
        temp_ids = []
        for _ in range(iterations):
            params = self.random_transaction_params()
            params["description"] = "Temporary transaction for delete test"
            
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO transactions 
                    (user_id, type, amount, category, description, date, created_at)
                    VALUES 
                    (%(user_id)s, %(type)s, %(amount)s, %(category)s, %(description)s, %(date)s, %(created_at)s)
                """, params)
                temp_ids.append(cursor.lastrowid)
            self.connection.commit()
            
        def delete_params_generator():
            if not temp_ids:
                raise Exception("Sem IDs temporários para excluir")
            return {"id": temp_ids.pop()}
            
        query = "DELETE FROM transactions WHERE id = %(id)s"
        return self.benchmark_write(
            "Delete Transaction", 
            query, 
            delete_params_generator,
            iterations=iterations
        )
    
    def test_complex_report_query(self, iterations=20):
        """Testa desempenho de uma consulta complexa para relatório"""
        query = """
            SELECT 
                YEAR(date) as year,
                MONTH(date) as month,
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses,
                SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) as balance,
                COUNT(*) as transaction_count
            FROM transactions 
            WHERE user_id = 1
            GROUP BY YEAR(date), MONTH(date)
            ORDER BY YEAR(date) DESC, MONTH(date) DESC
        """
        return self.benchmark_query("Complex Report Query", query, iterations=iterations)
    
    def run_all_tests(self):
        """Executa todos os testes de desempenho"""
        if not self.connection and not self.connect():
            return False
            
        # Executar todos os testes
        self.test_select_all_transactions()
        self.test_select_recent_transactions()
        self.test_select_with_filter()
        self.test_monthly_summary()
        self.test_category_summary()
        self.test_insert_transaction()
        self.test_update_transaction()
        self.test_delete_transaction()
        self.test_complex_report_query()
        
        # Salvar resultados em um arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"db_benchmark_results_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Resultados salvos em {filename}")
        
        # Gerar gráfico de desempenho
        self._generate_performance_chart(filename.replace(".json", ".png"))
        
        return True
    
    def _generate_performance_chart(self, filename):
        """Gera um gráfico de barras com o desempenho das consultas"""
        queries = [name for name, data in self.results.items() if data.get("type") == "query"]
        writes = [name for name, data in self.results.items() if data.get("type") == "write"]
        
        if queries:
            query_times = [self.results[name]["avg_time"] for name in queries]
            query_p95_times = [self.results[name]["p95_time"] for name in queries]
            
            # Gráfico para consultas
            plt.figure(figsize=(12, 6))
            bar_width = 0.35
            index = np.arange(len(queries))
            
            plt.bar(index, query_times, bar_width, label='Tempo Médio', color='b', alpha=0.7)
            plt.bar(index + bar_width, query_p95_times, bar_width, label='Tempo P95', color='r', alpha=0.7)
            
            plt.xlabel('Consulta')
            plt.ylabel('Tempo (ms)')
            plt.title('Desempenho das Consultas SQL')
            plt.xticks(index + bar_width/2, queries, rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            plt.savefig(filename.replace(".png", "_queries.png"))
            plt.close()
        
        if writes:
            write_times = [self.results[name]["avg_time"] for name in writes]
            write_p95_times = [self.results[name]["p95_time"] for name in writes]
            
            # Gráfico para operações de escrita
            plt.figure(figsize=(10, 5))
            bar_width = 0.35
            index = np.arange(len(writes))
            
            plt.bar(index, write_times, bar_width, label='Tempo Médio', color='g', alpha=0.7)
            plt.bar(index + bar_width, write_p95_times, bar_width, label='Tempo P95', color='y', alpha=0.7)
            
            plt.xlabel('Operação')
            plt.ylabel('Tempo (ms)')
            plt.title('Desempenho das Operações de Escrita SQL')
            plt.xticks(index + bar_width/2, writes, rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            plt.savefig(filename.replace(".png", "_writes.png"))
            plt.close()
        
        # Gráfico combinado
        all_operations = sorted(self.results.keys())
        all_times = [self.results[name]["avg_time"] for name in all_operations]
        
        plt.figure(figsize=(14, 7))
        colors = ['b' if self.results[name].get("type") == "query" else 'g' for name in all_operations]
        
        plt.barh(all_operations, all_times, color=colors, alpha=0.7)
        plt.xlabel('Tempo Médio (ms)')
        plt.ylabel('Operação')
        plt.title('Desempenho do Banco de Dados')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        
        print(f"Gráficos de desempenho salvos com prefixo {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DB Performance Tester para o Misa Cash")
    parser.add_argument("--host", default="localhost", help="Host do banco de dados")
    parser.add_argument("--port", type=int, default=3306, help="Porta do banco de dados")
    parser.add_argument("--user", default="root", help="Usuário do banco de dados")
    parser.add_argument("--password", default="", help="Senha do banco de dados")
    parser.add_argument("--database", default="misa_cash", help="Nome do banco de dados")
    parser.add_argument("--iterations", type=int, default=50, help="Número de iterações por teste")
    parser.add_argument("--test", help="Executar apenas um teste específico")
    
    args = parser.parse_args()
    
    tester = DBPerformanceTester(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database
    )
    
    if not tester.connect():
        sys.exit(1)
    
    try:
        if args.test:
            # Executar apenas um teste específico
            test_method = getattr(tester, f"test_{args.test}", None)
            if test_method:
                test_method(iterations=args.iterations)
            else:
                print(f"Teste desconhecido: {args.test}")
                print("Testes disponíveis:")
                print("  select_all_transactions")
                print("  select_recent_transactions")
                print("  select_with_filter")
                print("  monthly_summary")
                print("  category_summary")
                print("  insert_transaction")
                print("  update_transaction")
                print("  delete_transaction")
                print("  complex_report_query")
                sys.exit(1)
        else:
            # Executar todos os testes
            tester.run_all_tests()
    finally:
        tester.disconnect() 