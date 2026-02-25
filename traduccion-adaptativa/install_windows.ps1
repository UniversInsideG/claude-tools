# Instalador de /traduccion — Traduccion Adaptativa UNIVERSINSIDE
# Para Windows — Claude Code (terminal y VS Code)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallDir = Join-Path $env:USERPROFILE ".claude\traduccion-adaptativa"
$CommandsDir = Join-Path $env:USERPROFILE ".claude\commands"

Write-Host ""
Write-Host "  Traduccion Adaptativa UNIVERSINSIDE — Instalador"
Write-Host "  ================================================="
Write-Host ""

# Verificar que estamos en el directorio correcto
$SkillSource = Join-Path $ScriptDir "commands\traduccion.md"
if (-not (Test-Path $SkillSource)) {
    Write-Host "  ERROR: No se encuentra commands\traduccion.md"
    Write-Host "  Ejecuta este script desde el directorio traduccion-adaptativa\"
    exit 1
}

# Crear directorios
Write-Host "  Creando directorios..."
New-Item -ItemType Directory -Path $CommandsDir -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $InstallDir "data\references") -Force | Out-Null

# Copiar archivos de soporte
Write-Host "  Copiando archivos de soporte..."
Copy-Item (Join-Path $ScriptDir "data\FUNDAMENTOS.md") $InstallDir -Force
Copy-Item (Join-Path $ScriptDir "data\COMO_AÑADIR_PERFIL.md") $InstallDir -Force
Copy-Item (Join-Path $ScriptDir "data\references\miguel_processing_report.html") (Join-Path $InstallDir "data\references\") -Force
Copy-Item (Join-Path $ScriptDir "data\references\celeste_processing_report.html") (Join-Path $InstallDir "data\references\") -Force
Copy-Item (Join-Path $ScriptDir "data\references\cecilia_processing_report.html") (Join-Path $InstallDir "data\references\") -Force
Copy-Item (Join-Path $ScriptDir "data\references\jesus_processing_report.html") (Join-Path $InstallDir "data\references\") -Force

# Instalar skill con rutas resueltas
Write-Host "  Instalando skill /traduccion..."
$SkillContent = Get-Content $SkillSource -Raw -Encoding UTF8
$SkillContent = $SkillContent -replace "__INSTALL_DIR__", $InstallDir
Set-Content -Path (Join-Path $CommandsDir "traduccion.md") -Value $SkillContent -Encoding UTF8

Write-Host ""
Write-Host "  Instalacion completada."
Write-Host ""
Write-Host "  Archivos instalados:"
Write-Host "    Skill:       $CommandsDir\traduccion.md"
Write-Host "    Soporte:     $InstallDir\"
Write-Host "    Referencias: $InstallDir\data\references\"
Write-Host ""
Write-Host "  Uso: abre Claude Code y escribe /traduccion"
Write-Host ""
Write-Host "  Si Claude Code estaba abierto, reinicialo para que cargue la skill."
Write-Host ""
