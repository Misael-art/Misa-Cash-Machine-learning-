# Script completo para configurar a estrutura do projeto Misa Cash
# Esta versão garante que todos os arquivos importantes sejam copiados

Write-Host "Iniciando configuração completa do projeto Misa Cash..." -ForegroundColor Green

# Criar a estrutura base do projeto
$dirs = @(
    "Misa-Cash",
    "Misa-Cash\src",
    "Misa-Cash\docs",
    "Misa-Cash\tests",
    "Misa-Cash\scripts",
    "Misa-Cash\configs",
    "Misa-Cash\data",
    "Misa-Cash\notebooks",
    "Misa-Cash\deployment",
    "Misa-Cash\deployment\docker",
    "Misa-Cash\.github",
    "Misa-Cash\.github\workflows"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "Criado diretório: $dir" -ForegroundColor Yellow
    }
}

# Copiar arquivos de configuração básicos
$configFiles = @(
    @{Source = ".env"; Destination = "Misa-Cash\.env"},
    @{Source = ".gitignore"; Destination = "Misa-Cash\.gitignore"},
    @{Source = "requirements.txt"; Destination = "Misa-Cash\requirements.txt"}
)

foreach ($file in $configFiles) {
    if (Test-Path $file.Source) {
        Copy-Item -Path $file.Source -Destination $file.Destination -Force
        Write-Host "Copiado: $($file.Source) -> $($file.Destination)" -ForegroundColor Yellow
    }
}

# Copiar arquivos importantes do projeto Misa-Cash-Machine-learning-
if (Test-Path "Misa-Cash-Machine-learning-") {
    Write-Host "Encontrado diretório Misa-Cash-Machine-learning-, copiando arquivos..." -ForegroundColor Green
    
    # Lista de arquivos importantes para copiar da raiz
    $mlFiles = @(
        @{Source = "Misa-Cash-Machine-learning-\README.md"; Destination = "Misa-Cash\README.md"},
        @{Source = "Misa-Cash-Machine-learning-\ROADMAP.md"; Destination = "Misa-Cash\docs\ROADMAP.md"},
        @{Source = "Misa-Cash-Machine-learning-\.env.example"; Destination = "Misa-Cash\.env.example"},
        @{Source = "Misa-Cash-Machine-learning-\docker-compose.prod.yml"; Destination = "Misa-Cash\docker-compose.prod.yml"},
        @{Source = "Misa-Cash-Machine-learning-\Dockerfile"; Destination = "Misa-Cash\Dockerfile"},
        @{Source = "Misa-Cash-Machine-learning-\pyproject.toml"; Destination = "Misa-Cash\pyproject.toml"},
        @{Source = "Misa-Cash-Machine-learning-\pytest.ini"; Destination = "Misa-Cash\pytest.ini"},
        @{Source = "Misa-Cash-Machine-learning-\.gitlab-ci.yml"; Destination = "Misa-Cash\.gitlab-ci.yml"},
        @{Source = "Misa-Cash-Machine-learning-\requirements.txt"; Destination = "Misa-Cash\requirements.txt"}
    )
    
    foreach ($file in $mlFiles) {
        if (Test-Path $file.Source) {
            Copy-Item -Path $file.Source -Destination $file.Destination -Force
            Write-Host "Copiado: $($file.Source) -> $($file.Destination)" -ForegroundColor Yellow
        }
        else {
            Write-Host "Arquivo não encontrado: $($file.Source)" -ForegroundColor Gray
        }
    }
    
    # Copiar diretórios especiais para deployment
    $specialDirs = @(
        @{Source = "Misa-Cash-Machine-learning-\nginx"; Destination = "Misa-Cash\deployment\docker\nginx"},
        @{Source = "Misa-Cash-Machine-learning-\prometheus"; Destination = "Misa-Cash\deployment\docker\prometheus"},
        @{Source = "Misa-Cash-Machine-learning-\alertmanager"; Destination = "Misa-Cash\deployment\docker\alertmanager"}
    )
    
    foreach ($dir in $specialDirs) {
        if (Test-Path $dir.Source) {
            if (-not (Test-Path $dir.Destination)) {
                New-Item -ItemType Directory -Force -Path $dir.Destination | Out-Null
            }
            # Usar xcopy para copiar o conteúdo do diretório
            cmd /c "xcopy /E /I /Y ""$($dir.Source)\*.*"" ""$($dir.Destination)"""
            Write-Host "Copiado diretório: $($dir.Source) -> $($dir.Destination)" -ForegroundColor Yellow
        }
    }
    
    # Copiar workflows do GitHub
    Write-Host "Copiando workflows do GitHub..." -ForegroundColor Green
    if (Test-Path "Misa-Cash-Machine-learning-\.github\workflows") {
        cmd /c "xcopy /E /I /Y ""Misa-Cash-Machine-learning-\.github\workflows\*.*"" ""Misa-Cash\.github\workflows"""
    }
    
    # Copiar o código-fonte completo
    Write-Host "Copiando código-fonte da versão Machine Learning..." -ForegroundColor Green
    if (Test-Path "Misa-Cash-Machine-learning-\src") {
        $srcDirs = Get-ChildItem -Path "Misa-Cash-Machine-learning-\src" -Directory
        foreach ($srcDir in $srcDirs) {
            $targetDir = "Misa-Cash\src\$($srcDir.Name)"
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
            }
            cmd /c "xcopy /E /I /Y ""$($srcDir.FullName)\*.*"" ""$targetDir"""
            Write-Host "Copiado diretório: $($srcDir.FullName) -> $targetDir" -ForegroundColor Yellow
        }
    }
    
    # Copiar documentação
    Write-Host "Copiando documentação..." -ForegroundColor Green
    if (Test-Path "Misa-Cash-Machine-learning-\docs") {
        cmd /c "xcopy /E /I /Y ""Misa-Cash-Machine-learning-\docs\*.*"" ""Misa-Cash\docs"""
    }
}

# Copiar código-fonte da raiz (se existir)
if (Test-Path "src") {
    Write-Host "Copiando código-fonte da raiz do projeto..." -ForegroundColor Green
    $srcDirs = Get-ChildItem -Path "src" -Directory
    foreach ($srcDir in $srcDirs) {
        $targetDir = "Misa-Cash\src\$($srcDir.Name)"
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        }
        cmd /c "xcopy /E /I /Y ""$($srcDir.FullName)\*.*"" ""$targetDir"""
        Write-Host "Copiado diretório: $($srcDir.FullName) -> $targetDir" -ForegroundColor Yellow
    }
}

# Copiar outros recursos (se existirem)
$otherDirs = @(
    @{Source = "notebooks"; Destination = "Misa-Cash\notebooks"},
    @{Source = "data"; Destination = "Misa-Cash\data"},
    @{Source = "tests"; Destination = "Misa-Cash\tests"}
)

foreach ($dir in $otherDirs) {
    if (Test-Path $dir.Source) {
        Write-Host "Copiando $($dir.Source)..." -ForegroundColor Green
        cmd /c "xcopy /E /I /Y ""$($dir.Source)\*.*"" ""$($dir.Destination)"""
    }
}

# Verificar a migração
function Test-DirectoryExists {
    param (
        [string]$Path,
        [string]$Description
    )
    
    if (Test-Path $Path) {
        Write-Host "✓ $Description ($Path)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ $Description não encontrado ($Path)" -ForegroundColor Red
        return $false
    }
}

function Test-FileExists {
    param (
        [string]$Path,
        [string]$Description
    )
    
    if (Test-Path $Path) {
        Write-Host "✓ $Description ($Path)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ $Description não encontrado ($Path)" -ForegroundColor Red
        return $false
    }
}

Write-Host "`nVerificando estrutura do projeto Misa-Cash..." -ForegroundColor Cyan

# Verificar diretórios principais
$mainDirs = @(
    @{Path = "Misa-Cash\src"; Description = "Código-fonte"},
    @{Path = "Misa-Cash\docs"; Description = "Documentação"},
    @{Path = "Misa-Cash\.github\workflows"; Description = "Workflows do GitHub"},
    @{Path = "Misa-Cash\deployment"; Description = "Configurações de deploy"},
    @{Path = "Misa-Cash\deployment\docker"; Description = "Configurações Docker"}
)

$allDirsExist = $true
foreach ($dir in $mainDirs) {
    $allDirsExist = $allDirsExist -and (Test-DirectoryExists -Path $dir.Path -Description $dir.Description)
}

# Verificar arquivos principais
$mainFiles = @(
    @{Path = "Misa-Cash\README.md"; Description = "README principal"},
    @{Path = "Misa-Cash\.env.example"; Description = "Exemplo de variáveis de ambiente"},
    @{Path = "Misa-Cash\requirements.txt"; Description = "Dependências Python"},
    @{Path = "Misa-Cash\Dockerfile"; Description = "Dockerfile principal"},
    @{Path = "Misa-Cash\docker-compose.prod.yml"; Description = "Docker-compose produção"}
)

$allFilesExist = $true
foreach ($file in $mainFiles) {
    $allFilesExist = $allFilesExist -and (Test-FileExists -Path $file.Path -Description $file.Description)
}

# Verificar diretórios src específicos da versão ML
$srcDirs = @(
    @{Path = "Misa-Cash\src\data"; Description = "Módulo de dados"},
    @{Path = "Misa-Cash\src\models"; Description = "Módulo de modelos"},
    @{Path = "Misa-Cash\src\web"; Description = "Módulo web"},
    @{Path = "Misa-Cash\src\utils"; Description = "Utilitários"},
    @{Path = "Misa-Cash\src\analysis"; Description = "Módulo de análise"}
)

foreach ($dir in $srcDirs) {
    Test-DirectoryExists -Path $dir.Path -Description $dir.Description
}

# Verificar resultado final
if ($allDirsExist -and $allFilesExist) {
    Write-Host "`nEstrutura basica completa!" -ForegroundColor Green
} 
else {
    Write-Host "`nAlguns componentes podem estar faltando. Verifique os itens acima." -ForegroundColor Yellow
}

# Mensagem final
Write-Host "`nConfiguracao completa finalizada. Estrutura disponivel em: Misa-Cash\" -ForegroundColor Green
Write-Host "Recomendacao: Verifique os arquivos e ajuste conforme necessario." -ForegroundColor Yellow 