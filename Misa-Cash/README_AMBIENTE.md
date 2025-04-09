# Configuração do Ambiente Misa-Cash

O ambiente virtual Python foi criado com sucesso em `Misa-Cash/venv`.

## Instruções para instalação de dependências

Devido a limitações de conexão, as dependências não foram instaladas completamente. Siga os passos abaixo para instalar as dependências quando tiver uma conexão estável:

1. Ative o ambiente virtual:
   ```
   cd Misa-Cash
   .\venv\Scripts\activate
   ```

2. Instale as dependências básicas:
   ```
   pip install setuptools wheel
   pip install -r requirements.txt
   ```

3. Se continuar enfrentando problemas, instale as dependências principais uma a uma:
   ```
   pip install numpy pandas matplotlib scikit-learn flask requests pytest
   ```

4. Para instalar dependências adicionais necessárias para o frontend:
   ```
   cd src/web/frontend
   npm install
   ```

## Verificação da configuração

Após a instalação das dependências, você pode verificar se o ambiente está funcionando corretamente executando:

```
python -c "import numpy; import pandas; import matplotlib; print('Ambiente configurado com sucesso!')"
```

## Estrutura do Projeto

O projeto Misa-Cash foi organizado com sucesso e agora contém todos os arquivos e diretórios necessários:

- `Misa-Cash/src/` - Todo o código-fonte do projeto
- `Misa-Cash/docs/` - Documentação completa
- `Misa-Cash/.github/workflows/` - Configurações de CI/CD
- `Misa-Cash/deployment/` - Configurações de deployment
- `Misa-Cash/tests/` - Testes automatizados

O ambiente virtual antigo em `D:\Bussines\Finance\Machine learning\venv` pode ser removido com segurança, pois foi substituído pelo novo ambiente em `Misa-Cash/venv`. 