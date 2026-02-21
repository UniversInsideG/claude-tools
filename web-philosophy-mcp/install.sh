#!/bin/bash

# ============================================
# Instalador de Web Philosophy MCP
# Para HTML, CSS y JS (Atomic Design)
# UniversInside
# ============================================

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  Instalador Web Philosophy MCP${NC}"
echo -e "${CYAN}  HTML / CSS / JS — Atomic Design${NC}"
echo -e "${CYAN}  UniversInside${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_PATH="$SCRIPT_DIR/server.py"

# Verificar que server.py existe
if [ ! -f "$SERVER_PATH" ]; then
    echo -e "${RED}ERROR: server.py no encontrado en $SCRIPT_DIR${NC}"
    exit 1
fi

# ── 1. Detectar Python ──────────────────────────────────────────

echo -e "${YELLOW}1. Verificando Python...${NC}"
PYTHON_CMD=""

for cmd in python3 python py; do
    if command -v "$cmd" &>/dev/null; then
        version=$("$cmd" --version 2>&1)
        if echo "$version" | grep -q "Python 3"; then
            PYTHON_CMD="$cmd"
            echo -e "   ${GREEN}Python encontrado: $version${NC}"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "   ${RED}ERROR: Python 3 no encontrado${NC}"
    echo -e "   ${YELLOW}Instala Python desde: https://www.python.org/downloads/${NC}"
    exit 1
fi

# ── 2. Instalar dependencias ────────────────────────────────────

echo ""
echo -e "${YELLOW}2. Instalando dependencias...${NC}"
if $PYTHON_CMD -m pip install mcp --quiet 2>/dev/null; then
    echo -e "   ${GREEN}Dependencia 'mcp' instalada${NC}"
else
    echo -e "   ${RED}ERROR al instalar 'mcp'${NC}"
    echo -e "   ${YELLOW}Intenta manualmente: $PYTHON_CMD -m pip install mcp${NC}"
    exit 1
fi

# ── 3. Elegir destino ───────────────────────────────────────────

echo ""
echo -e "${YELLOW}3. ¿Dónde quieres instalar web-philosophy?${NC}"
echo ""
echo "   1) Claude Code (terminal + VS Code)"
echo "   2) Claude Desktop"
echo "   3) Ambos"
echo ""
read -p "   Opción [1]: " INSTALL_OPTION
INSTALL_OPTION=${INSTALL_OPTION:-1}

# ── Funciones de instalación ────────────────────────────────────

install_claude_code() {
    echo ""
    echo -e "${YELLOW}Configurando Claude Code...${NC}"

    local MCP_JSON="$HOME/.claude/.mcp.json"
    local CLAUDE_DIR="$HOME/.claude"

    # Crear directorio si no existe
    mkdir -p "$CLAUDE_DIR"

    if [ -f "$MCP_JSON" ]; then
        # Backup
        cp "$MCP_JSON" "$MCP_JSON.backup"
        echo -e "   ${CYAN}Backup creado: $MCP_JSON.backup${NC}"

        # Verificar si ya tiene web-philosophy
        if $PYTHON_CMD -c "
import json, sys
with open('$MCP_JSON') as f:
    data = json.load(f)
servers = data.get('mcpServers', data)
if 'web-philosophy' in servers:
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
            echo -e "   ${YELLOW}web-philosophy ya está configurado en .mcp.json${NC}"
            return
        fi

        # Añadir web-philosophy preservando lo existente
        $PYTHON_CMD -c "
import json
with open('$MCP_JSON') as f:
    data = json.load(f)
if 'mcpServers' not in data:
    data = {'mcpServers': data}
data['mcpServers']['web-philosophy'] = {
    'command': '$PYTHON_CMD',
    'args': ['$SERVER_PATH']
}
with open('$MCP_JSON', 'w') as f:
    json.dump(data, f, indent=2)
"
    else
        # Crear nuevo
        $PYTHON_CMD -c "
import json
data = {
    'mcpServers': {
        'web-philosophy': {
            'command': '$PYTHON_CMD',
            'args': ['$SERVER_PATH']
        }
    }
}
with open('$MCP_JSON', 'w') as f:
    json.dump(data, f, indent=2)
"
    fi

    echo -e "   ${GREEN}web-philosophy añadido a .mcp.json${NC}"
}

install_claude_desktop() {
    echo ""
    echo -e "${YELLOW}Configurando Claude Desktop...${NC}"

    local DESKTOP_CONFIG
    if [ "$(uname)" = "Darwin" ]; then
        DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    else
        DESKTOP_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
    fi

    local CONFIG_DIR
    CONFIG_DIR="$(dirname "$DESKTOP_CONFIG")"

    # Crear directorio si no existe
    mkdir -p "$CONFIG_DIR"

    if [ -f "$DESKTOP_CONFIG" ]; then
        # Backup
        cp "$DESKTOP_CONFIG" "$DESKTOP_CONFIG.backup"
        echo -e "   ${CYAN}Backup creado: ${DESKTOP_CONFIG}.backup${NC}"

        # Verificar si ya tiene web-philosophy
        if $PYTHON_CMD -c "
import json, sys
with open('''$DESKTOP_CONFIG''') as f:
    data = json.load(f)
servers = data.get('mcpServers', {})
if 'web-philosophy' in servers:
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
            echo -e "   ${YELLOW}web-philosophy ya está configurado en Claude Desktop${NC}"
            return
        fi

        # Añadir web-philosophy preservando lo existente
        $PYTHON_CMD -c "
import json
with open('''$DESKTOP_CONFIG''') as f:
    data = json.load(f)
if 'mcpServers' not in data:
    data['mcpServers'] = {}
data['mcpServers']['web-philosophy'] = {
    'command': '$PYTHON_CMD',
    'args': ['$SERVER_PATH']
}
with open('''$DESKTOP_CONFIG''', 'w') as f:
    json.dump(data, f, indent=2)
"
    else
        # Crear nuevo preservando estructura Desktop
        $PYTHON_CMD -c "
import json
data = {
    'mcpServers': {
        'web-philosophy': {
            'command': '$PYTHON_CMD',
            'args': ['$SERVER_PATH']
        }
    }
}
with open('''$DESKTOP_CONFIG''', 'w') as f:
    json.dump(data, f, indent=2)
"
    fi

    echo -e "   ${GREEN}web-philosophy añadido a Claude Desktop${NC}"
}

# ── 4. Ejecutar instalación ─────────────────────────────────────

case $INSTALL_OPTION in
    1)
        install_claude_code
        ;;
    2)
        install_claude_desktop
        ;;
    3)
        install_claude_code
        install_claude_desktop
        ;;
    *)
        echo -e "${RED}Opción no válida${NC}"
        exit 1
        ;;
esac

# ── 5. Resumen ──────────────────────────────────────────────────

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Instalación completada${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Qué se instaló:${NC}"
echo "  - MCP Server: web-philosophy (HTML/CSS/JS)"
echo "  - Arquitectura: Atomic Design (Atom → Molecule → Organism → Template → Page)"
echo ""
echo -e "${CYAN}Validaciones incluidas:${NC}"
echo "  - CSS: colores hardcodeados, !important, selectores profundos, bloques duplicados"
echo "  - HTML: estilos inline, div soup, alt faltante, DRY visual"
echo "  - JS: var en lugar de const/let, queries DOM sin cachear"
echo ""
echo -e "${YELLOW}Próximos pasos:${NC}"

case $INSTALL_OPTION in
    1)
        echo "  1. Reinicia Claude Code (terminal o VS Code)"
        echo "  2. Ejecuta /mcp para verificar 'web-philosophy'"
        ;;
    2)
        echo "  1. Reinicia Claude Desktop"
        echo "  2. Verifica que web-philosophy aparece en la lista de MCP"
        ;;
    3)
        echo "  1. Reinicia Claude Code y/o Claude Desktop"
        echo "  2. En Claude Code: ejecuta /mcp para verificar 'web-philosophy'"
        echo "  3. En Desktop: verifica que aparece en la lista de MCP"
        ;;
esac

echo ""
echo -e "${YELLOW}Si también usas Godot/Python:${NC}"
echo "  cd ../philosophy-mcp && pip install -r requirements.txt"
echo "  claude mcp add philosophy -- $PYTHON_CMD \$(pwd)/server.py"
echo ""
