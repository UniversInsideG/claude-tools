# Instalador de Philosophy MCP para Windows
# Ejecutar como: powershell -ExecutionPolicy Bypass -File install-windows.ps1

Write-Host "=== Instalador Philosophy MCP para Windows ===" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
$pythonCmd = $null

# Probar diferentes comandos de Python
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

# Obtener ruta del script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = Join-Path $scriptPath "server.py"

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
Write-Host "3. Configurando Claude Code..." -ForegroundColor Yellow
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

# Si ya existe, hacer backup
if (Test-Path $mcpJsonPath) {
    $backup = "$mcpJsonPath.backup"
    Copy-Item $mcpJsonPath $backup
    Write-Host "   Backup creado: $backup" -ForegroundColor Gray
}

$mcpConfig | Out-File -FilePath $mcpJsonPath -Encoding UTF8
Write-Host "   Configuracion guardada en: $mcpJsonPath" -ForegroundColor Green

# Copiar comando /filosofia
Write-Host ""
Write-Host "4. Instalando comando /filosofia..." -ForegroundColor Yellow
$commandsDir = Join-Path $claudeDir "commands"
if (-not (Test-Path $commandsDir)) {
    New-Item -ItemType Directory -Path $commandsDir | Out-Null
}

$filosofiaSource = Join-Path (Split-Path -Parent $scriptPath) "filosofia\commands\filosofia.md"
if (Test-Path $filosofiaSource) {
    Copy-Item $filosofiaSource (Join-Path $commandsDir "filosofia.md")
    Write-Host "   Comando /filosofia instalado" -ForegroundColor Green
} else {
    Write-Host "   Comando /filosofia no encontrado (opcional)" -ForegroundColor Gray
}

# Finalizado
Write-Host ""
Write-Host "=== INSTALACION COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Cyan
Write-Host "1. Reinicia Claude Code (cierra y abre de nuevo)"
Write-Host "2. Ejecuta /mcp para verificar que 'philosophy' aparece"
Write-Host "3. Usa /filosofia [tarea] para empezar"
Write-Host ""
Read-Host "Presiona Enter para salir"
