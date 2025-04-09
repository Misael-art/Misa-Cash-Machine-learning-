import requests
import time
import statistics
import json
from datetime import datetime
import argparse
import sys

class APIBenchmark:
    """Classe para realizar benchmarks de API específicas do Misa Cash"""
    
    def __init__(self, base_url, email="test@example.com", password="test123"):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.token = None
        self.headers = {}
        self.results = {}

    def login(self):
        """Realiza login para obter o token de autenticação"""
        url = f"{self.base_url}/api/auth/login"
        data = {"email": self.email, "password": self.password}
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
            print("Login realizado com sucesso")
            return True
        else:
            print(f"Falha no login: {response.status_code} - {response.text}")
            return False

    def benchmark_endpoint(self, endpoint, method="GET", data=None, name=None, iterations=50):
        """Realiza benchmark de um endpoint específico"""
        url = f"{self.base_url}{endpoint}"
        request_name = name or endpoint
        times = []
        status_codes = []
        
        print(f"Iniciando benchmark para {request_name}...")
        
        for i in range(iterations):
            sys.stdout.write(f"\rIteração {i+1}/{iterations}")
            sys.stdout.flush()
            
            start_time = time.time()
            
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                print(f"\nMétodo não suportado: {method}")
                return
            
            end_time = time.time()
            request_time = (end_time - start_time) * 1000  # converter para milissegundos
            times.append(request_time)
            status_codes.append(response.status_code)
        
        # Calcular estatísticas
        avg_time = statistics.mean(times)
        median_time = statistics.median(times)
        min_time = min(times)
        max_time = max(times)
        p95_time = sorted(times)[int(iterations * 0.95)]
        success_rate = status_codes.count(200) / iterations * 100
        
        # Armazenar resultados
        self.results[request_name] = {
            "avg_time": avg_time,
            "median_time": median_time,
            "min_time": min_time,
            "max_time": max_time,
            "p95_time": p95_time,
            "success_rate": success_rate,
            "sample_size": iterations
        }
        
        # Exibir resultados
        print(f"\nResultados para {request_name}:")
        print(f"  Tempo médio: {avg_time:.2f} ms")
        print(f"  Tempo mediano: {median_time:.2f} ms")
        print(f"  Tempo mínimo: {min_time:.2f} ms")
        print(f"  Tempo máximo: {max_time:.2f} ms")
        print(f"  Tempo P95: {p95_time:.2f} ms")
        print(f"  Taxa de sucesso: {success_rate:.2f}%")
        print(f"  Tamanho da amostra: {iterations}")
        print()
        
        return self.results[request_name]

    def run_dashboard_benchmark(self, iterations=50):
        """Executa benchmark do endpoint de dashboard"""
        return self.benchmark_endpoint(
            endpoint="/api/dashboard/summary",
            method="GET",
            name="Dashboard Summary",
            iterations=iterations
        )

    def run_transactions_list_benchmark(self, iterations=50):
        """Executa benchmark do endpoint de listagem de transações"""
        return self.benchmark_endpoint(
            endpoint="/api/transactions",
            method="GET",
            name="List Transactions",
            iterations=iterations
        )

    def run_reports_benchmark(self, iterations=30):
        """Executa benchmark do endpoint de relatórios"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        return self.benchmark_endpoint(
            endpoint=f"/api/reports/monthly?month={current_month}&year={current_year}",
            method="GET",
            name="Monthly Report",
            iterations=iterations
        )

    def run_transaction_create_benchmark(self, iterations=20):
        """Executa benchmark de criação de transação"""
        data = {
            "type": "expense",
            "amount": 100.00,
            "category": "food",
            "description": "Benchmark transaction",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        return self.benchmark_endpoint(
            endpoint="/api/transactions",
            method="POST",
            data=data,
            name="Create Transaction",
            iterations=iterations
        )

    def run_user_profile_benchmark(self, iterations=20):
        """Executa benchmark de obtenção de perfil do usuário"""
        return self.benchmark_endpoint(
            endpoint="/api/users/profile",
            method="GET",
            name="User Profile",
            iterations=iterations
        )

    def run_all_benchmarks(self):
        """Executa todos os benchmarks disponíveis"""
        if not self.token and not self.login():
            return False
        
        # Executar todos os benchmarks
        self.run_dashboard_benchmark()
        self.run_transactions_list_benchmark()
        self.run_reports_benchmark()
        self.run_transaction_create_benchmark()
        self.run_user_profile_benchmark()
        
        # Salvar resultados em um arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_results_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Resultados salvos em {filename}")
        return True

    def compare_results(self, previous_results_file):
        """Compara os resultados atuais com resultados anteriores"""
        try:
            with open(previous_results_file, "r") as f:
                previous_results = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar resultados anteriores: {e}")
            return
        
        print("\nComparação com execução anterior:")
        print("-" * 80)
        print(f"{'Endpoint':<25} {'Atual (ms)':<12} {'Anterior (ms)':<12} {'Diferença':<12} {'Mudança %'}")
        print("-" * 80)
        
        for endpoint, current_data in self.results.items():
            if endpoint in previous_results:
                prev_data = previous_results[endpoint]
                current_avg = current_data["avg_time"]
                prev_avg = prev_data["avg_time"]
                diff = current_avg - prev_avg
                percent = (diff / prev_avg) * 100 if prev_avg > 0 else 0
                
                # Formatar a diferença com sinal
                diff_str = f"{diff:+.2f}"
                percent_str = f"{percent:+.2f}%"
                
                print(f"{endpoint:<25} {current_avg:<12.2f} {prev_avg:<12.2f} {diff_str:<12} {percent_str}")
            else:
                print(f"{endpoint:<25} {current_data['avg_time']:<12.2f} {'N/A':<12} {'N/A':<12} {'N/A'}")
        
        print("-" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="API Benchmark para o Misa Cash")
    parser.add_argument("--url", default="http://localhost:5000", help="URL base da API")
    parser.add_argument("--email", default="test@example.com", help="Email para login")
    parser.add_argument("--password", default="test123", help="Senha para login")
    parser.add_argument("--iterations", type=int, default=50, help="Número de iterações por endpoint")
    parser.add_argument("--compare", help="Arquivo de resultados anteriores para comparação")
    parser.add_argument("--endpoint", help="Executar apenas um endpoint específico")
    
    args = parser.parse_args()
    
    benchmark = APIBenchmark(args.url, args.email, args.password)
    
    if not benchmark.login():
        sys.exit(1)
    
    if args.endpoint:
        # Executar apenas um endpoint específico
        if args.endpoint == "dashboard":
            benchmark.run_dashboard_benchmark(args.iterations)
        elif args.endpoint == "transactions":
            benchmark.run_transactions_list_benchmark(args.iterations)
        elif args.endpoint == "reports":
            benchmark.run_reports_benchmark(args.iterations)
        elif args.endpoint == "create":
            benchmark.run_transaction_create_benchmark(args.iterations)
        elif args.endpoint == "profile":
            benchmark.run_user_profile_benchmark(args.iterations)
        else:
            print(f"Endpoint desconhecido: {args.endpoint}")
            sys.exit(1)
    else:
        # Executar todos os benchmarks
        benchmark.run_all_benchmarks()
    
    if args.compare:
        benchmark.compare_results(args.compare) 