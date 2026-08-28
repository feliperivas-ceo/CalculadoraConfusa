# deploy.ps1 - Script de Despliegue Automatizado para Windows (Fase 2: DevOps)
# Descripción: Instala dependencias y despliega la aplicación Calculadora Confusa
# Uso: powershell -ExecutionPolicy Bypass -File .\deploy.ps1

Write-Host "==========================================" -ForegroundColor Green
Write-Host "Calculadora Confusa - Script de Despliegue" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Paso 1: Verificar Python
Write-Host "[1/5] Verificando Python..." -ForegroundColor Cyan
$pythonCmd = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }

if (-not (Get-Command $pythonCmd -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python 3 no está instalado" -ForegroundColor Red
    Write-Host "Por favor, instala Python desde https://www.python.org" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = & $pythonCmd --version 2>&1
Write-Host "✓ $pythonVersion encontrado" -ForegroundColor Green

# Paso 2: Crear/Activar entorno virtual
Write-Host ""
Write-Host "[2/5] Configurando entorno virtual..." -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual..."
    & $pythonCmd -m venv .venv
    Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "✓ Entorno virtual ya existe" -ForegroundColor Green
}

# Activar entorno virtual
$activateScript = ".\\.venv\\Scripts\\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "✓ Entorno virtual activado" -ForegroundColor Green
}

# Paso 3: Instalar dependencias
Write-Host ""
Write-Host "[3/5] Instalando dependencias..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe -m pip install --upgrade pip | Out-Null
& .\.venv\Scripts\pip.exe install -r requirements.txt
Write-Host "✓ Dependencias instaladas" -ForegroundColor Green

# Paso 4: Verificar estructura
Write-Host ""
Write-Host "[4/5] Verificando estructura de archivos..." -ForegroundColor Cyan

$requiredFiles = @("calculadora.py", "requirements.txt", "templates\index.html")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ No se encontró $file" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✓ Estructura de archivos correcta" -ForegroundColor Green

# Paso 5: Crear historial
Write-Host ""
Write-Host "[5/5] Inicializando sistema de persistencia..." -ForegroundColor Cyan

if (-not (Test-Path "historial.json")) {
    "[]" | Set-Content "historial.json"
    Write-Host "✓ Archivo de historial inicializado" -ForegroundColor Green
} else {
    Write-Host "✓ Historial existente" -ForegroundColor Green
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✓ Despliegue completado exitosamente" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para ejecutar la aplicación:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python calculadora.py" -ForegroundColor White
Write-Host ""
Write-Host "Luego abre en tu navegador:" -ForegroundColor Yellow
Write-Host "  http://127.0.0.1:5000" -ForegroundColor White
Write-Host ""
