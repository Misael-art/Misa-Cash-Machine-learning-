# Script para copiar os workflows do GitHub
# Este script é chamado pelo script principal setup_project_structure.ps1

Write-Host "Copiando arquivos de workflows do GitHub..." -ForegroundColor Green

$sourcePath = "./Misa-Cash-Machine-learning-/.github/workflows"
$targetPath = "./Misa-Cash/.github/workflows"

# Verificar se o diretório de origem existe
if (Test-Path -Path $sourcePath) {
    # Criar o diretório de destino se não existir
    if (-not (Test-Path -Path $targetPath)) {
        New-Item -Path $targetPath -ItemType Directory -Force | Out-Null
        Write-Host "Criado diretório de workflows: $targetPath" -ForegroundColor Yellow
    }
    
    # Copiar arquivos
    $files = Get-ChildItem -Path $sourcePath -File
    foreach ($file in $files) {
        Copy-Item -Path $file.FullName -Destination $targetPath -Force
        Write-Host "Copiado workflow: $($file.Name)" -ForegroundColor Yellow
    }
}
else {
    Write-Host "Diretório de workflows GitHub não encontrado: $sourcePath" -ForegroundColor Gray
}

Write-Host "Operação de cópia de workflows concluída." -ForegroundColor Green 