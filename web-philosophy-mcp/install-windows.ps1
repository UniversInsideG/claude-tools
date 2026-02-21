# Instalador de Web Philosophy MCP para Windows
# HTML / CSS / JS - Atomic Design
# Ejecutar como: powershell -ExecutionPolicy Bypass -File install-windows.ps1

Write-Host ""
Write-Host "=== Instalador Web Philosophy MCP ===" -ForegroundColor Cyan
Write-Host "    HTML / CSS / JS - Atomic Design" -ForegroundColor Cyan
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

# Configurar MCP - preservando servidores existentes
Write-Host ""
Write-Host "3. Configurando MCP Server..." -ForegroundColor Yellow
$mcpJsonPath = Join-Path $claudeDir ".mcp.json"
$serverPathEscaped = $serverPath -replace '\\', '\\\\'

if (Test-Path $mcpJsonPath) {
    # Backup
    $backup = "$mcpJsonPath.backup"
    Copy-Item $mcpJsonPath $backup
    Write-Host "   Backup creado: $backup" -ForegroundColor Gray

    # Leer config existente y añadir web-philosophy
    try {
        $mcpContent = Get-Content $mcpJsonPath -Raw | ConvertFrom-Json

        # Detectar formato: mcpServers o plano
        if ($mcpContent.mcpServers) {
            # Formato nuevo - añadir dentro de mcpServers
            $mcpContent.mcpServers | Add-Member -NotePropertyName "web-philosophy" -NotePropertyValue ([PSCustomObject]@{
                command = $pythonCmd
                args = @($serverPath)
            }) -Force
        } else {
            # Formato antiguo - migrar a mcpServers
            Write-Host "   Formato antiguo detectado, migrando a mcpServers..." -ForegroundColor Yellow
            $existingServers = @{}
            $mcpContent.PSObject.Properties | ForEach-Object {
                $existingServers[$_.Name] = $_.Value
            }
            $existingServers["web-philosophy"] = [PSCustomObject]@{
                command = $pythonCmd
                args = @($serverPath)
            }
            $mcpContent = [PSCustomObject]@{
                mcpServers = [PSCustomObject]$existingServers
            }
        }

        $mcpContent | ConvertTo-Json -Depth 10 | Out-File -FilePath $mcpJsonPath -Encoding UTF8
        Write-Host "   web-philosophy añadido a .mcp.json (servidores existentes preservados)" -ForegroundColor Green
    } catch {
        Write-Host "   ERROR al leer .mcp.json existente, creando nuevo..." -ForegroundColor Yellow
        $mcpConfig = @"
{
  "mcpServers": {
    "web-philosophy": {
      "command": "$pythonCmd",
      "args": ["$serverPathEscaped"]
    }
  }
}
"@
        $mcpConfig | Out-File -FilePath $mcpJsonPath -Encoding UTF8
        Write-Host "   Configuracion MCP creada" -ForegroundColor Green
    }
} else {
    # No existe - crear nuevo
    $mcpConfig = @"
{
  "mcpServers": {
    "web-philosophy": {
      "command": "$pythonCmd",
      "args": ["$serverPathEscaped"]
    }
  }
}
"@
    $mcpConfig | Out-File -FilePath $mcpJsonPath -Encoding UTF8
    Write-Host "   Configuracion MCP creada" -ForegroundColor Green
}

# Finalizado
Write-Host ""
Write-Host "=== INSTALACION COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "Que se instalo:" -ForegroundColor Cyan
Write-Host "  - MCP Server: web-philosophy (HTML/CSS/JS)"
Write-Host "  - Arquitectura: Atomic Design (Atom > Molecule > Organism > Template > Page)"
Write-Host ""
Write-Host "Validaciones incluidas:" -ForegroundColor Cyan
Write-Host "  - CSS: colores hardcodeados, !important, selectores profundos, bloques duplicados"
Write-Host "  - HTML: estilos inline, div soup, alt faltante, DRY visual"
Write-Host "  - JS: var en lugar de const/let, queries DOM sin cachear"
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Reinicia Claude Code"
Write-Host "  2. Ejecuta /mcp para verificar 'web-philosophy'"
Write-Host ""
Write-Host "Si tambien usas Godot/Python:" -ForegroundColor Gray
Write-Host "  cd ..\philosophy-mcp && INSTALAR.bat" -ForegroundColor Gray
Write-Host ""
Read-Host "Presiona Enter para salir"
