# Actualizador de Philosophy MCP para Windows
# Ejecutar como: powershell -ExecutionPolicy Bypass -File update-windows.ps1

Write-Host ""
Write-Host "=== Actualizador Philosophy MCP ===" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = Join-Path $scriptPath "server.py"

# Verificar que server.py existe
if (-not (Test-Path $serverPath)) {
    Write-Host "ERROR: server.py no encontrado en $scriptPath" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "1. Verificando archivos actualizados..." -ForegroundColor Yellow
Write-Host "   server.py: OK" -ForegroundColor Green

# Actualizar comando /filosofia
Write-Host ""
Write-Host "2. Actualizando comando /filosofia..." -ForegroundColor Yellow
$claudeDir = Join-Path $env:USERPROFILE ".claude"
$commandsDir = Join-Path $claudeDir "commands"

if (-not (Test-Path $commandsDir)) {
    New-Item -ItemType Directory -Path $commandsDir -Force | Out-Null
}

$filosofiaSource = Join-Path (Split-Path -Parent $scriptPath) "filosofia\commands\filosofia.md"
if (Test-Path $filosofiaSource) {
    Copy-Item $filosofiaSource (Join-Path $commandsDir "filosofia.md") -Force
    Write-Host "   Comando /filosofia actualizado" -ForegroundColor Green
} else {
    Write-Host "   filosofia.md no encontrado" -ForegroundColor Gray
}

# Cerrar procesos de Claude Code si estan corriendo
Write-Host ""
Write-Host "3. Buscando procesos de Claude Code..." -ForegroundColor Yellow

$claudeProcesses = Get-Process -Name "claude*" -ErrorAction SilentlyContinue
if ($claudeProcesses) {
    Write-Host "   Procesos encontrados: $($claudeProcesses.Count)" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "   Quieres cerrar Claude Code para aplicar cambios? (S/N)"
    if ($response -eq "S" -or $response -eq "s") {
        $claudeProcesses | Stop-Process -Force
        Write-Host "   Procesos cerrados" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "   OK, recuerda reiniciar Claude Code manualmente" -ForegroundColor Yellow
    }
} else {
    Write-Host "   Ningun proceso de Claude Code activo" -ForegroundColor Green
}

# Verificar configuracion MCP
Write-Host ""
Write-Host "4. Verificando configuracion MCP..." -ForegroundColor Yellow
$mcpJsonPath = Join-Path $claudeDir ".mcp.json"

if (Test-Path $mcpJsonPath) {
    $mcpContent = Get-Content $mcpJsonPath -Raw | ConvertFrom-Json
    if ($mcpContent.philosophy) {
        Write-Host "   Configuracion MCP: OK" -ForegroundColor Green
    } else {
        Write-Host "   ADVERTENCIA: 'philosophy' no encontrado en .mcp.json" -ForegroundColor Yellow
        Write-Host "   Ejecuta INSTALAR.bat para configurar" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ADVERTENCIA: .mcp.json no existe" -ForegroundColor Yellow
    Write-Host "   Ejecuta INSTALAR.bat para instalar" -ForegroundColor Yellow
}

# Finalizado
Write-Host ""
Write-Host "=== ACTUALIZACION COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "Cambios aplicados:" -ForegroundColor Cyan
Write-Host "  - Nuevo parametro 'tipo_cambio' en paso 1"
Write-Host "  - Tipos: nuevo, modificacion, bugfix, refactor"
Write-Host "  - Checklist muestra recordatorio 'aplica a todo'"
Write-Host ""
Write-Host "Para verificar:" -ForegroundColor Cyan
Write-Host "  1. Abre Claude Code"
Write-Host "  2. Ejecuta: /filosofia arreglar bug en funcion X"
Write-Host "  3. El paso 1 debe pedir 'tipo_cambio'"
Write-Host ""
Read-Host "Presiona Enter para salir"
