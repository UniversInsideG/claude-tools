#!/bin/bash
# Instalador de /traduccion — Traduccion Adaptativa UNIVERSINSIDE
# Para Mac/Linux — Claude Code (terminal y VS Code)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/.claude/traduccion-adaptativa"
COMMANDS_DIR="$HOME/.claude/commands"

echo ""
echo "  Traduccion Adaptativa UNIVERSINSIDE — Instalador"
echo "  ================================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "$SCRIPT_DIR/commands/traduccion.md" ]; then
    echo "  ERROR: No se encuentra commands/traduccion.md"
    echo "  Ejecuta este script desde el directorio traduccion-adaptativa/"
    exit 1
fi

# Crear directorios
echo "  Creando directorios..."
mkdir -p "$COMMANDS_DIR"
mkdir -p "$INSTALL_DIR/data/references"

# Copiar archivos de soporte
echo "  Copiando archivos de soporte..."
cp "$SCRIPT_DIR/data/FUNDAMENTOS.md" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/data/COMO_AÑADIR_PERFIL.md" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/data/references/miguel_processing_report.html" "$INSTALL_DIR/data/references/"
cp "$SCRIPT_DIR/data/references/celeste_processing_report.html" "$INSTALL_DIR/data/references/"
cp "$SCRIPT_DIR/data/references/cecilia_processing_report.html" "$INSTALL_DIR/data/references/"
cp "$SCRIPT_DIR/data/references/jesus_processing_report.html" "$INSTALL_DIR/data/references/"

# Instalar skill con rutas resueltas
echo "  Instalando skill /traduccion..."
sed "s|__INSTALL_DIR__|$INSTALL_DIR|g" "$SCRIPT_DIR/commands/traduccion.md" > "$COMMANDS_DIR/traduccion.md"

echo ""
echo "  Instalacion completada."
echo ""
echo "  Archivos instalados:"
echo "    Skill:       $COMMANDS_DIR/traduccion.md"
echo "    Soporte:     $INSTALL_DIR/"
echo "    Referencias: $INSTALL_DIR/data/references/"
echo ""
echo "  Uso: abre Claude Code y escribe /traduccion"
echo ""
echo "  Si Claude Code estaba abierto, reinicialo para que cargue la skill."
echo ""
