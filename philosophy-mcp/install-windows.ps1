# Instalador de Philosophy MCP para Windows (v2.3.0)
# Ejecutar como: powershell -ExecutionPolicy Bypass -File install-windows.ps1

Write-Host ""
Write-Host "=== Instalador Philosophy MCP v2.3.0 ===" -ForegroundColor Cyan
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
  "mcpServers": {
    "philosophy": {
      "command": "$pythonCmd",
      "args": ["$serverPathEscaped"]
    }
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
    Write-Host "   /filosofia instalado (10 pasos)" -ForegroundColor Green
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

# Instalar hooks de metacognicion
Write-Host ""
Write-Host "6. Instalando hooks de metacognicion..." -ForegroundColor Yellow
$hooksDir = Join-Path $claudeDir "hooks"
if (-not (Test-Path $hooksDir)) {
    New-Item -ItemType Directory -Path $hooksDir | Out-Null
}

$hooksSource = Join-Path $parentPath "filosofia\hooks"
$hooksInstalled = 0

# Copiar metacognicion.py
$metacogSource = Join-Path $hooksSource "metacognicion.py"
if (Test-Path $metacogSource) {
    Copy-Item $metacogSource (Join-Path $hooksDir "metacognicion.py") -Force
    Write-Host "   metacognicion.py instalado" -ForegroundColor Green
    $hooksInstalled++
} else {
    Write-Host "   metacognicion.py no encontrado" -ForegroundColor Yellow
}

# Copiar planning_reminder.py
$planningSource = Join-Path $hooksSource "planning_reminder.py"
if (Test-Path $planningSource) {
    Copy-Item $planningSource (Join-Path $hooksDir "planning_reminder.py") -Force
    Write-Host "   planning_reminder.py instalado" -ForegroundColor Green
    $hooksInstalled++
} else {
    Write-Host "   planning_reminder.py no encontrado" -ForegroundColor Yellow
}

# Configurar hooks en settings.json
Write-Host ""
Write-Host "7. Configurando hooks en settings.json..." -ForegroundColor Yellow
$settingsPath = Join-Path $claudeDir "settings.json"
$metacogPath = (Join-Path $hooksDir "metacognicion.py") -replace '\\', '\\\\'
$planningPath = (Join-Path $hooksDir "planning_reminder.py") -replace '\\', '\\\\'

$settingsConfig = @"
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Did the assistant ask a question AND also use Edit, Write, or MCP tools in the same turn? If yes: {\"ok\": false, \"reason\": \"You asked a question but used tools without waiting for the answer. Questions end the turn.\"}. If no: {\"ok\": true}.",
            "timeout": 30
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$pythonCmd $metacogPath",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "$pythonCmd $planningPath",
            "timeout": 5
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$pythonCmd $metacogPath",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$pythonCmd $metacogPath",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
"@

if (Test-Path $settingsPath) {
    $backup = "$settingsPath.backup"
    Copy-Item $settingsPath $backup
    Write-Host "   Backup creado: $backup" -ForegroundColor Gray
}

$settingsConfig | Out-File -FilePath $settingsPath -Encoding UTF8
Write-Host "   Hooks configurados (4 eventos: Stop, UserPromptSubmit, PreToolUse, PostToolUse)" -ForegroundColor Green

# Finalizado
Write-Host ""
Write-Host "=== INSTALACION COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "Que se instalo:" -ForegroundColor Cyan
Write-Host "  - MCP Server: philosophy (server.py)"
Write-Host "  - Comando: /filosofia (flujo de 10 pasos)"
Write-Host "  - Comando: /arquitectura (analisis global)"
Write-Host "  - Instrucciones: CLAUDE.md"
Write-Host "  - Hook: metacognicion.py (comprension + autoobservacion)"
Write-Host "  - Hook: planning_reminder.py (filosofia de codigo)"
Write-Host "  - Hook Stop: detecta pregunta + ejecucion en el mismo turno"
Write-Host "  - Hooks configurados en 4 eventos: Stop, UserPromptSubmit, PreToolUse, PostToolUse"
Write-Host ""
Write-Host "Novedades v2.3.0:" -ForegroundColor Cyan
Write-Host "  - NUEVO: q0 detecta criterios con implementacion en vez de funcionalidad"
Write-Host "  - NUEVO: Advertencia cuando buscas POR QUE falla y olvidas la FUNCIONALIDAD"
Write-Host "  - NUEVO: Skills /filosofia y /arquitectura advierten NO analizar antes de q0"
Write-Host ""
Write-Host "Incluye v2.2.0:" -ForegroundColor Gray
Write-Host "  - q6 acepta 'references' para analisis exhaustivo de codigo a replicar"
Write-Host "  - validate verifica que propiedades de referencia se incluyan"
Write-Host ""
Write-Host "Incluye v2.1.0:" -ForegroundColor Gray
Write-Host "  - Paso 0 obligatorio (q0_criterios)"
Write-Host "  - Hook Stop - bloquea pregunta + ejecucion en mismo turno"
Write-Host "  - Criterios persistentes en .claude/criterios_*.md"
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Reinicia Claude Code"
Write-Host "  2. Ejecuta /mcp para verificar 'philosophy'"
Write-Host "  3. Usa /filosofia [tarea] o /arquitectura [proyecto]"
Write-Host ""
Read-Host "Presiona Enter para salir"
