# Actualizador de Philosophy MCP para Windows (v1.5.0)
# Ejecutar como: powershell -ExecutionPolicy Bypass -File update-windows.ps1

Write-Host ""
Write-Host "=== Actualizador Philosophy MCP v1.5.0 ===" -ForegroundColor Cyan
Write-Host ""

# Obtener rutas
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = Join-Path $scriptPath "server.py"
$parentPath = Split-Path -Parent $scriptPath

# Verificar que server.py existe
if (-not (Test-Path $serverPath)) {
    Write-Host "ERROR: server.py no encontrado en $scriptPath" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "1. Verificando archivos..." -ForegroundColor Yellow
Write-Host "   server.py: OK" -ForegroundColor Green

# Rutas de destino
$claudeDir = Join-Path $env:USERPROFILE ".claude"
$commandsDir = Join-Path $claudeDir "commands"

if (-not (Test-Path $commandsDir)) {
    New-Item -ItemType Directory -Path $commandsDir -Force | Out-Null
}

# Actualizar /filosofia
Write-Host ""
Write-Host "2. Actualizando comandos..." -ForegroundColor Yellow

$filosofiaSource = Join-Path $parentPath "filosofia\commands\filosofia.md"
if (Test-Path $filosofiaSource) {
    Copy-Item $filosofiaSource (Join-Path $commandsDir "filosofia.md") -Force
    Write-Host "   /filosofia actualizado (9 pasos)" -ForegroundColor Green
} else {
    Write-Host "   /filosofia no encontrado" -ForegroundColor Yellow
}

# Actualizar /arquitectura
$arquitecturaSource = Join-Path $parentPath "filosofia\commands\arquitectura.md"
if (Test-Path $arquitecturaSource) {
    Copy-Item $arquitecturaSource (Join-Path $commandsDir "arquitectura.md") -Force
    Write-Host "   /arquitectura actualizado" -ForegroundColor Green
} else {
    Write-Host "   /arquitectura no encontrado" -ForegroundColor Yellow
}

# Actualizar CLAUDE.md
Write-Host ""
Write-Host "3. Actualizando instrucciones..." -ForegroundColor Yellow
$claudeMdSource = Join-Path $parentPath "filosofia\CLAUDE.md"
if (Test-Path $claudeMdSource) {
    Copy-Item $claudeMdSource (Join-Path $claudeDir "CLAUDE.md") -Force
    Write-Host "   CLAUDE.md actualizado" -ForegroundColor Green
} else {
    Write-Host "   CLAUDE.md no encontrado" -ForegroundColor Gray
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

# Cerrar procesos de Claude Code
Write-Host ""
Write-Host "5. Buscando procesos de Claude Code..." -ForegroundColor Yellow

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

# Finalizado
Write-Host ""
Write-Host "=== ACTUALIZACION COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "Novedades v1.5.0:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  PASO 3 - Jerarquizacion de documentacion:" -ForegroundColor White
Write-Host "    - Busca en .claude/ y docs/ del proyecto"
Write-Host "    - Ordena por: tipo + fecha + relevancia"
Write-Host "    - Detecta versiones superseded del mismo tema"
Write-Host "    - Indicadores: ALTA/MEDIA/BAJA prioridad"
Write-Host ""
Write-Host "  PASO 9 - Documentar (NUEVO):" -ForegroundColor White
Write-Host "    - Despues de validar, documentar en CHANGELOG"
Write-Host "    - Incluir seccion 'Reemplaza/Obsoleta'"
Write-Host "    - Maxima: 'Documentar DESPUES de validar'"
Write-Host ""
Write-Host "  Q5 - Valida comportamiento:" -ForegroundColor White
Write-Host "    - Prioriza comportamiento sobre nomenclatura"
Write-Host "    - Legacy: documenta como deuda tecnica"
Write-Host "    - Nuevo: exige nomenclatura correcta"
Write-Host ""
Write-Host "  /arquitectura - Busqueda en disco:" -ForegroundColor White
Write-Host "    - Encuentra analisis existentes al iniciar"
Write-Host "    - Busca recursivamente en .claude/"
Write-Host ""
Write-Host "Para verificar:" -ForegroundColor Yellow
Write-Host "  1. Abre Claude Code"
Write-Host "  2. Ejecuta: /filosofia crear componente X"
Write-Host "  3. El flujo debe tener 9 pasos"
Write-Host ""
Read-Host "Presiona Enter para salir"
