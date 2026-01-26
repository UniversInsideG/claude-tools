# Instalador de Philosophy MCP para Windows (v1.8.0)
# Ejecutar como: powershell -ExecutionPolicy Bypass -File install-windows.ps1

Write-Host ""
Write-Host "=== Instalador Philosophy MCP v1.8.0 ===" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
$pythonCmd = $null

$pythonOptions = @("python", "py", "python3")
foreach ($cmd in $pythonOptions) {
    try {
        $version = & $cmd --version 2>&1
        if ($version -match "Python 3") {
            $pythonCmd = $cmd
            Write-Host "   Python encontrado: $version" -ForegroundColor Green
            break
        }
    } catch {}
}

if (-not $pythonCmd) {
    Write-Host "   ERROR: Python no encontrado" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "   IMPORTANTE: Marca 'Add Python to PATH' durante la instalacion" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Instalar dependencias
Write-Host ""
Write-Host "2. Instalando dependencias..." -ForegroundColor Yellow
try {
    & $pythonCmd -m pip install mcp --quiet
    Write-Host "   Dependencias instaladas" -ForegroundColor Green
} catch {
    Write-Host "   ERROR al instalar dependencias" -ForegroundColor Red
    Write-Host "   Intenta manualmente: $pythonCmd -m pip install mcp" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Obtener rutas
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = Join-Path $scriptPath "server.py"
$parentPath = Split-Path -Parent $scriptPath

# Verificar que server.py existe
if (-not (Test-Path $serverPath)) {
    Write-Host "   ERROR: server.py no encontrado en $scriptPath" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Crear directorio .claude si no existe
$claudeDir = Join-Path $env:USERPROFILE ".claude"
if (-not (Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir | Out-Null
    Write-Host "   Creado directorio: $claudeDir" -ForegroundColor Green
}

# Crear/actualizar .mcp.json
Write-Host ""
Write-Host "3. Configurando MCP Server..." -ForegroundColor Yellow
$mcpJsonPath = Join-Path $claudeDir ".mcp.json"
$serverPathEscaped = $serverPath -replace '\\', '\\\\'

$mcpConfig = @"
{
  "philosophy": {
    "command": "$pythonCmd",
    "args": ["$serverPathEscaped"]
  }
}
"@

if (Test-Path $mcpJsonPath) {
    $backup = "$mcpJsonPath.backup"
    Copy-Item $mcpJsonPath $backup
    Write-Host "   Backup creado: $backup" -ForegroundColor Gray
}

$mcpConfig | Out-File -FilePath $mcpJsonPath -Encoding UTF8
Write-Host "   Configuracion MCP guardada" -ForegroundColor Green

# Crear directorio commands
Write-Host ""
Write-Host "4. Instalando comandos /filosofia y /arquitectura..." -ForegroundColor Yellow
$commandsDir = Join-Path $claudeDir "commands"
if (-not (Test-Path $commandsDir)) {
    New-Item -ItemType Directory -Path $commandsDir | Out-Null
}

# Instalar /filosofia
$filosofiaSource = Join-Path $parentPath "filosofia\commands\filosofia.md"
if (Test-Path $filosofiaSource) {
    Copy-Item $filosofiaSource (Join-Path $commandsDir "filosofia.md") -Force
    Write-Host "   /filosofia instalado (9 pasos)" -ForegroundColor Green
} else {
    Write-Host "   /filosofia no encontrado" -ForegroundColor Yellow
}

# Instalar /arquitectura
$arquitecturaSource = Join-Path $parentPath "filosofia\commands\arquitectura.md"
if (Test-Path $arquitecturaSource) {
    Copy-Item $arquitecturaSource (Join-Path $commandsDir "arquitectura.md") -Force
    Write-Host "   /arquitectura instalado" -ForegroundColor Green
} else {
    Write-Host "   /arquitectura no encontrado" -ForegroundColor Yellow
}

# Copiar CLAUDE.md con instrucciones
Write-Host ""
Write-Host "5. Instalando instrucciones globales..." -ForegroundColor Yellow
$claudeMdSource = Join-Path $parentPath "filosofia\CLAUDE.md"
if (Test-Path $claudeMdSource) {
    Copy-Item $claudeMdSource (Join-Path $claudeDir "CLAUDE.md") -Force
    Write-Host "   CLAUDE.md instalado" -ForegroundColor Green
} else {
    Write-Host "   CLAUDE.md no encontrado (opcional)" -ForegroundColor Gray
}

# Finalizado
Write-Host ""
Write-Host "=== INSTALACION COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "Que se instalo:" -ForegroundColor Cyan
Write-Host "  - MCP Server: philosophy (server.py)"
Write-Host "  - Comando: /filosofia (flujo de 9 pasos)"
Write-Host "  - Comando: /arquitectura (analisis global)"
Write-Host "  - Instrucciones: CLAUDE.md"
Write-Host ""
Write-Host "Novedades v1.8.0:" -ForegroundColor Cyan
Write-Host "  - NUEVO: Parametro decision_usuario para desbloquear pasos"
Write-Host "  - NUEVO: Usuario puede continuar asumiendo responsabilidad"
Write-Host "  - NUEVO: Nomenclatura puede omitirse si usuario decide"
Write-Host ""
Write-Host "Incluye v1.7.0:" -ForegroundColor Gray
Write-Host "  - Deteccion de duplicacion REAL (similitud >60%)"
Write-Host "  - Claude ANALIZA, EXPLICA y PREGUNTA al usuario"
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Reinicia Claude Code"
Write-Host "  2. Ejecuta /mcp para verificar 'philosophy'"
Write-Host "  3. Usa /filosofia [tarea] o /arquitectura [proyecto]"
Write-Host ""
Read-Host "Presiona Enter para salir"
