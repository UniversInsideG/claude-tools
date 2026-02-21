# Actualizador de Web Philosophy MCP para Windows
# Ejecutar como: powershell -ExecutionPolicy Bypass -File update-windows.ps1

Write-Host ""
Write-Host "=== Actualizador Web Philosophy MCP ===" -ForegroundColor Cyan
Write-Host ""

# Obtener rutas
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = Join-Path $scriptPath "server.py"

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

# Verificar y actualizar configuracion MCP
Write-Host ""
Write-Host "2. Verificando configuracion MCP..." -ForegroundColor Yellow
$mcpJsonPath = Join-Path $claudeDir ".mcp.json"
$serverPathEscaped = $serverPath -replace '\\', '\\\\'

if (Test-Path $mcpJsonPath) {
    try {
        $mcpContent = Get-Content $mcpJsonPath -Raw | ConvertFrom-Json

        if ($mcpContent.mcpServers -and $mcpContent.mcpServers."web-philosophy") {
            Write-Host "   Configuracion MCP: OK (web-philosophy encontrado)" -ForegroundColor Green
        } elseif ($mcpContent.mcpServers) {
            Write-Host "   web-philosophy no encontrado, añadiendo..." -ForegroundColor Yellow
            $backup = "$mcpJsonPath.backup"
            Copy-Item $mcpJsonPath $backup

            $mcpContent.mcpServers | Add-Member -NotePropertyName "web-philosophy" -NotePropertyValue ([PSCustomObject]@{
                command = $pythonCmd
                args = @($serverPath)
            }) -Force

            $mcpContent | ConvertTo-Json -Depth 10 | Out-File -FilePath $mcpJsonPath -Encoding UTF8
            Write-Host "   web-philosophy añadido (backup: $backup)" -ForegroundColor Green
        } elseif ($mcpContent."web-philosophy") {
            Write-Host "   Formato antiguo detectado, migrando a mcpServers..." -ForegroundColor Yellow
            $backup = "$mcpJsonPath.backup"
            Copy-Item $mcpJsonPath $backup

            $existingServers = @{}
            $mcpContent.PSObject.Properties | ForEach-Object {
                $existingServers[$_.Name] = $_.Value
            }

            $newConfig = [PSCustomObject]@{
                mcpServers = [PSCustomObject]$existingServers
            }
            $newConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $mcpJsonPath -Encoding UTF8
            Write-Host "   Configuracion MCP migrada (backup: $backup)" -ForegroundColor Green
        } else {
            Write-Host "   ADVERTENCIA: 'web-philosophy' no encontrado en .mcp.json" -ForegroundColor Yellow
            Write-Host "   Ejecuta INSTALAR.bat para configurar" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "   ERROR al leer .mcp.json" -ForegroundColor Red
        Write-Host "   Ejecuta INSTALAR.bat para reinstalar" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ADVERTENCIA: .mcp.json no existe" -ForegroundColor Yellow
    Write-Host "   Ejecuta INSTALAR.bat para instalar" -ForegroundColor Yellow
}

# Cerrar procesos de Claude Code
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

# Finalizado
Write-Host ""
Write-Host "=== ACTUALIZACION COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "Web Philosophy MCP actualizado." -ForegroundColor Cyan
Write-Host ""
Write-Host "Para verificar:" -ForegroundColor Yellow
Write-Host "  1. Abre Claude Code"
Write-Host "  2. Ejecuta /mcp para verificar 'web-philosophy'"
Write-Host ""
Read-Host "Presiona Enter para salir"
