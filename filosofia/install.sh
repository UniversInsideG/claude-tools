#!/bin/bash

# ============================================
# Instalador de Configuración Claude Code
# Filosofía de Programación - UniversInside
# ============================================

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "═══════════════════════════════════════════════════"
echo "  Instalador de Filosofía de Programación"
echo "  UniversInside - Claude Code Config"
echo "═══════════════════════════════════════════════════"
echo ""

# Detectar directorio de trabajo (donde están los proyectos)
DEFAULT_DIR="$HOME/Documents/GitHub"

read -p "Directorio de proyectos [$DEFAULT_DIR]: " WORK_DIR
WORK_DIR=${WORK_DIR:-$DEFAULT_DIR}

# Crear directorio si no existe
mkdir -p "$WORK_DIR"
mkdir -p "$WORK_DIR/.claude/commands"

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copiar archivos
echo ""
echo -e "${YELLOW}Instalando archivos...${NC}"

cp "$SCRIPT_DIR/CLAUDE.md" "$WORK_DIR/CLAUDE.md"
echo -e "${GREEN}✓${NC} CLAUDE.md → $WORK_DIR/"

cp "$SCRIPT_DIR/CODING_PHILOSOPHY.md" "$WORK_DIR/.claude/CODING_PHILOSOPHY.md"
echo -e "${GREEN}✓${NC} CODING_PHILOSOPHY.md → $WORK_DIR/.claude/"

cp "$SCRIPT_DIR/commands/filosofia.md" "$WORK_DIR/.claude/commands/filosofia.md"
echo -e "${GREEN}✓${NC} filosofia.md → $WORK_DIR/.claude/commands/"

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Instalación completada${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo "Archivos instalados en: $WORK_DIR"
echo ""
echo "Uso:"
echo "  - CLAUDE.md se carga automáticamente"
echo "  - Escribe /filosofia para ver los principios"
echo "  - Escribe /filosofia check antes de programar"
echo ""
