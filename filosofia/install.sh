#!/bin/bash

# ============================================
# Instalador de Configuración Claude Code
# Filosofía de Programación - UniversInside
# ============================================

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Instalador de Filosofía de Programación"
echo "  UniversInside - Claude Code Config"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Detectar directorio de trabajo (donde están los proyectos)
DEFAULT_DIR="$HOME/Documents/GitHub"

read -p "Directorio de proyectos [$DEFAULT_DIR]: " WORK_DIR
WORK_DIR=${WORK_DIR:-$DEFAULT_DIR}

# Crear directorios si no existen
mkdir -p "$WORK_DIR"
mkdir -p "$WORK_DIR/.claude/commands"
mkdir -p "$WORK_DIR/.claude/hooks"

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copiar archivos
echo ""
echo -e "${YELLOW}Instalando archivos...${NC}"

# CLAUDE.md
cp "$SCRIPT_DIR/CLAUDE.md" "$WORK_DIR/CLAUDE.md"
echo -e "${GREEN}✓${NC} CLAUDE.md → $WORK_DIR/"

# Documentación
cp "$SCRIPT_DIR/CODING_PHILOSOPHY.md" "$WORK_DIR/.claude/CODING_PHILOSOPHY.md"
echo -e "${GREEN}✓${NC} CODING_PHILOSOPHY.md → $WORK_DIR/.claude/"

# Comando /filosofia
cp "$SCRIPT_DIR/commands/filosofia.md" "$WORK_DIR/.claude/commands/filosofia.md"
echo -e "${GREEN}✓${NC} filosofia.md → $WORK_DIR/.claude/commands/"

# Hooks
cp "$SCRIPT_DIR/hooks/validate_philosophy.py" "$WORK_DIR/.claude/hooks/validate_philosophy.py"
chmod +x "$WORK_DIR/.claude/hooks/validate_philosophy.py"
echo -e "${GREEN}✓${NC} validate_philosophy.py → $WORK_DIR/.claude/hooks/"

cp "$SCRIPT_DIR/hooks/planning_reminder.py" "$WORK_DIR/.claude/hooks/planning_reminder.py"
chmod +x "$WORK_DIR/.claude/hooks/planning_reminder.py"
echo -e "${GREEN}✓${NC} planning_reminder.py → $WORK_DIR/.claude/hooks/"

# Configurar settings.json (o settings.local.json)
SETTINGS_FILE="$WORK_DIR/.claude/settings.local.json"

# Verificar si ya existe configuración
if [ -f "$SETTINGS_FILE" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Ya existe $SETTINGS_FILE${NC}"
    read -p "¿Sobrescribir configuración de hooks? (s/n) [n]: " OVERWRITE
    OVERWRITE=${OVERWRITE:-n}
else
    OVERWRITE="s"
fi

if [ "$OVERWRITE" = "s" ] || [ "$OVERWRITE" = "S" ]; then
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)",
      "Bash(find:*)",
      "Bash(grep:*)"
    ]
  },
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/planning_reminder.py\"",
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
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate_philosophy.py\"",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "mcp__gdai.*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate_philosophy.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
EOF
    echo -e "${GREEN}✓${NC} settings.local.json → $WORK_DIR/.claude/"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Instalación completada${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Archivos instalados en: $WORK_DIR"
echo ""
echo -e "${YELLOW}Sistema de validación:${NC}"
echo "  • CAPA 1: Recordatorio de filosofía antes de planificar"
echo "  • CAPA 2: Validación de código antes de escribir"
echo ""
echo -e "${YELLOW}Comandos disponibles:${NC}"
echo "  /filosofia           Ver resumen de principios"
echo "  /filosofia check     Checklist antes de programar"
echo "  /filosofia doc       Documentación completa"
echo ""
echo -e "${YELLOW}IMPORTANTE:${NC}"
echo "  Abre un NUEVO terminal de Claude Code para activar los hooks."
echo ""
