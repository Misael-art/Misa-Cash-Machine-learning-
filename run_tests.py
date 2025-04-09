import os
import sys
import pytest

# Adiciona o diretório src ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src'))

if __name__ == '__main__':
    try:
        # Executa os testes
        print("Executando testes da aplicação Misa-Cash...")
        result = pytest.main(['src/backend/tests'])
        sys.exit(result)
    except Exception as e:
        print(f"Erro ao executar os testes: {e}")
        sys.exit(1) 