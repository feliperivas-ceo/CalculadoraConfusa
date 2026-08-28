# firewall-config.ps1 - Script de Configuración de Firewall para Windows (Fase 2: DevOps)
# Descripción: Abre puertos necesarios en el Windows Firewall
# Uso: powershell -ExecutionPolicy Bypass -RunAs Administrator -File .\firewall-config.ps1
# Nota: Requiere permisos de administrador

Write-Host "==========================================" -ForegroundColor Green
Write-Host "Configuración de Firewall - Windows" -ForegroundColor Green
Write-Host "Calculadora Confusa" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Verificar permisos de administrador
$isAdmin = [Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains [Security.Principal.SecurityIdentifier]"S-1-5-32-544"
if (-not $isAdmin) {
    Write-Host "❌ Este script requiere permisos de administrador" -ForegroundColor Red
    Write-Host "Por favor, ejecuta PowerShell como administrador y vuelve a intentar" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "✓ Permisos de administrador confirmados" -ForegroundColor Green
Write-Host ""

# Paso 1: Habilitar firewall
Write-Host "[1/3] Verificando Windows Firewall..." -ForegroundColor Cyan
try {
    $fwProfile = Get-NetFirewallProfile
    if ($fwProfile) {
        Write-Host "✓ Windows Firewall detectado" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ No se pudo acceder a la configuración del firewall" -ForegroundColor Yellow
}

# Paso 2: Abrir puerto 5000
Write-Host "[2/3] Abriendo puerto 5000 (Backend)..." -ForegroundColor Cyan
try {
    # Verificar si la regla ya existe
    $existingRule = Get-NetFirewallRule -DisplayName "Calculadora Confusa - Backend (5000)" -ErrorAction SilentlyContinue
    
    if ($existingRule) {
        Write-Host "✓ Regla de firewall ya existe" -ForegroundColor Green
    } else {
        # Crear nueva regla
        New-NetFirewallRule `
            -DisplayName "Calculadora Confusa - Backend (5000)" `
            -Direction Inbound `
            -LocalPort 5000 `
            -Protocol TCP `
            -Action Allow | Out-Null
        Write-Host "✓ Puerto 5000 abierto para TCP" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error al configurar la regla de firewall: $_" -ForegroundColor Red
    exit 1
}

# Paso 3: Mostrar status
Write-Host "[3/3] Verificando reglas activas..." -ForegroundColor Cyan
$rules = Get-NetFirewallRule -DisplayName "*Calculadora Confusa*" -ErrorAction SilentlyContinue
if ($rules) {
    Write-Host "Reglas de firewall activas:" -ForegroundColor White
    $rules | Format-Table -Property DisplayName, Direction, Enabled -AutoSize
} else {
    Write-Host "⚠️ No se encontraron reglas específicas (pero el puerto puede estar abierto)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✓ Configuración de firewall completada" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "La aplicación Backend estará disponible en:" -ForegroundColor Yellow
Write-Host "  http://127.0.0.1:5000" -ForegroundColor White
Write-Host ""
Write-Host "Desde otra máquina en la red (reemplaza IP):" -ForegroundColor Yellow
Write-Host "  http://<IP_DEL_SERVIDOR>:5000" -ForegroundColor White
Write-Host ""
Write-Host "Para deshacer la regla, ejecuta:" -ForegroundColor Gray
Write-Host "  Remove-NetFirewallRule -DisplayName 'Calculadora Confusa - Backend (5000)'" -ForegroundColor Gray
Write-Host ""
