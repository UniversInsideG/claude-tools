# Actualizador de Philosophy MCP para Windows (v2.5.0)
# Ejecutar como: powershell -ExecutionPolicy Bypass -File update-windows.ps1

Write-Host ""
Write-Host "=== Actualizador Philosophy MCP v2.5.0 ===" -ForegroundColor Cyan
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

# Detectar Python
$pythonCmd = $null
$pythonOptions = @("python", "py", "python3")
foreach ($cmd in $pythonOptions) {
    try {
        $version = & $cmd --version 2>&1
        if ($version -match "Python 3") {
            $pythonCmd = $cmd
            break
        }
    } catch {}
}

if (-not $pythonCmd) {
    $pythonCmd = "python3"
    Write-Host "   ADVERTENCIA: Python no detectado, usando 'python3'" -ForegroundColor Yellow
}

# Rutas de destino
$claudeDir = Join-Path $env:USERPROFILE ".claude"
$commandsDir = Join-Path $claudeDir "commands"
$hooksDir = Join-Path $claudeDir "hooks"

if (-not (Test-Path $commandsDir)) {
    New-Item -ItemType Directory -Path $commandsDir -Force | Out-Null
}

# Actualizar /filosofia
Write-Host ""
Write-Host "2. Actualizando comandos..." -ForegroundColor Yellow

$filosofiaSource = Join-Path $parentPath "filosofia\commands\filosofia.md"
if (Test-Path $filosofiaSource) {
    Copy-Item $filosofiaSource (Join-Path $commandsDir "filosofia.md") -Force
    Write-Host "   /filosofia actualizado (10 pasos)" -ForegroundColor Green
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

# Actualizar hooks
Write-Host ""
Write-Host "4. Actualizando hooks de metacognicion..." -ForegroundColor Yellow

if (-not (Test-Path $hooksDir)) {
    New-Item -ItemType Directory -Path $hooksDir -Force | Out-Null
}

$hooksSource = Join-Path $parentPath "filosofia\hooks"

# Copiar metacognicion.py
$metacogSource = Join-Path $hooksSource "metacognicion.py"
if (Test-Path $metacogSource) {
    Copy-Item $metacogSource (Join-Path $hooksDir "metacognicion.py") -Force
    Write-Host "   metacognicion.py actualizado" -ForegroundColor Green
} else {
    Write-Host "   metacognicion.py no encontrado" -ForegroundColor Yellow
}

# Copiar planning_reminder.py
$planningSource = Join-Path $hooksSource "planning_reminder.py"
if (Test-Path $planningSource) {
    Copy-Item $planningSource (Join-Path $hooksDir "planning_reminder.py") -Force
    Write-Host "   planning_reminder.py actualizado" -ForegroundColor Green
} else {
    Write-Host "   planning_reminder.py no encontrado" -ForegroundColor Yellow
}

# Configurar hooks en settings.json
Write-Host ""
Write-Host "5. Actualizando hooks en settings.json..." -ForegroundColor Yellow
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

# Verificar y actualizar configuracion MCP
Write-Host ""
Write-Host "6. Verificando configuracion MCP..." -ForegroundColor Yellow
$mcpJsonPath = Join-Path $claudeDir ".mcp.json"
$serverPathEscaped = $serverPath -replace '\\', '\\\\'

if (Test-Path $mcpJsonPath) {
    $mcpContent = Get-Content $mcpJsonPath -Raw | ConvertFrom-Json
    if ($mcpContent.mcpServers.philosophy) {
        Write-Host "   Configuracion MCP: OK (formato mcpServers)" -ForegroundColor Green
    } elseif ($mcpContent.philosophy) {
        Write-Host "   Formato antiguo detectado, actualizando a mcpServers..." -ForegroundColor Yellow
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
        $backup = "$mcpJsonPath.backup"
        Copy-Item $mcpJsonPath $backup
        $mcpConfig | Out-File -FilePath $mcpJsonPath -Encoding UTF8
        Write-Host "   Configuracion MCP actualizada (backup: $backup)" -ForegroundColor Green
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
Write-Host "7. Buscando procesos de Claude Code..." -ForegroundColor Yellow

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
Write-Host "Novedades v2.5.0 (gate plan_approved + devolucion funcional):" -ForegroundColor Cyan
Write-Host ""
Write-Host "  NUEVO:" -ForegroundColor White
Write-Host "    - plan_approved bloquea q1 hasta que el usuario apruebe el plan del analisis"
Write-Host "    - Checkpoint 4 exige devolucion funcional + tecnica con checklist de reconexion"
Write-Host "    - Instrucciones con formato QUE/PARA QUE/POR QUE en checkpoint 4 y resume"
Write-Host "    - architecture_resume infiere plan_approved del estado guardado"
Write-Host "    - CLAUDE.md con regla 'Analizar = /arquitectura' y comunicacion funcional"
Write-Host ""
Write-Host "  Incluye v2.4.0:" -ForegroundColor Gray
Write-Host "    - decision_usuario 2 pasos, validate .tscn, q3 ripgrep, q0 gate criterios"
Write-Host ""
Write-Host "  Incluye v2.1-2.3:" -ForegroundColor Gray
Write-Host "    - Paso 0, criterios persistentes, q6 references, deteccion criterios sesgados"
Write-Host ""
Write-Host "Para verificar:" -ForegroundColor Yellow
Write-Host "  1. Abre Claude Code"
Write-Host "  2. Ejecuta /mcp para verificar 'philosophy'"
Write-Host "  3. Usa /filosofia [tarea] para probar el flujo completo"
Write-Host ""
Write-Host "Si tambien trabajas con HTML/CSS/JS:" -ForegroundColor Gray
Write-Host "  cd ..\web-philosophy-mcp && INSTALAR.bat" -ForegroundColor Gray
Write-Host ""
Read-Host "Presiona Enter para salir"
