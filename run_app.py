import os
import sys

# Adiciona o diretório src ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src'))

if __name__ == '__main__':
    try:
        from src.backend.run import app
        print("Iniciando a aplicação Misa-Cash...")
        print("Acesse a API em: http://localhost:5000/api/health")
        app.run(debug=True)
    except ImportError as e:
        print(f"Erro ao importar módulos: {e}")
        print("Verifique se você está executando este script do diretório raiz do projeto.")
        sys.exit(1) 