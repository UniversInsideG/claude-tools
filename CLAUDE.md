# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository (`claude-tools`) contains the **Philosophy MCP Server** - a Model Context Protocol server that enforces modular programming philosophy in Claude Code. The main component is the Python MCP server in `philosophy-mcp/`.

## Commands

### Development
```bash
# Run MCP server directly (for testing)
python3 philosophy-mcp/server.py

# Install MCP dependencies
pip install mcp
```

### Installation (for end users)
```bash
# macOS/Linux
cd philosophy-mcp
pip install -r requirements.txt
claude mcp add philosophy -- python3 $(pwd)/server.py

# Windows - use INSTALAR.bat in philosophy-mcp/
```

### Verify installation
```bash
# In Claude Code
/mcp  # Should show "philosophy" in the list
```

## Architecture

```
claude-tools/
├── philosophy-mcp/           # Main MCP server
│   ├── server.py             # MCP server implementation (all tools)
│   ├── INSTALAR.bat          # Windows installer
│   ├── ACTUALIZAR.bat        # Windows updater
│   └── docs/                 # Design documents
│
└── filosofia/                # User-facing configuration
    ├── commands/
    │   ├── filosofia.md      # /filosofia command (9-step flow)
    │   └── arquitectura.md   # /arquitectura command (refactoring analysis)
    ├── hooks/                # Legacy hooks (deprecated, MCP preferred)
    └── CLAUDE.md             # Instructions for end-user projects
```

### MCP Server (`philosophy-mcp/server.py`)

Single-file Python server implementing all MCP tools:

**Core Flow Tools (9 steps):**
1. `philosophy_q1_responsabilidad` - Single responsibility check
2. `philosophy_q2_reutilizacion` - Reusability analysis
3. `philosophy_q3_buscar` - Search for similar code/docs
4. `philosophy_q4_herencia` - Inheritance decision
5. `philosophy_q5_nivel` - Architecture level validation
6. `philosophy_q6_verificar_dependencias` - Verify external dependencies exist
7. (Write code)
8. `philosophy_validate` - Code validation (smells, duplication)
9. `philosophy_q9_documentar` - Document changes (mandatory)

**Auxiliary Tools:**
- `philosophy_checklist` - Quick reference

**Architecture Analysis Tools:**
- `philosophy_architecture_analysis` - Start global analysis
- `philosophy_architecture_status` - View current state
- `philosophy_architecture_resume` - Resume after compaction
- `philosophy_architecture_checkpoint` - Save progress

### Session State

The server maintains two state dictionaries:
- `SESSION_STATE` - Tracks the 9-step flow progress (resets per creation)
- `ARCHITECTURE_STATE` - Tracks architecture analysis progress (persists)

### 5-Level Architecture (equivalent to Atomic Design)

```
ESTRUCTURA (main.tscn)
    └── PANTALLA (*_screen) - Unique user view
          └── CONTENEDOR (*_system) - Reusable logic
                └── COMPONENTE (*_component) - Combines pieces
                      └── PIEZA (*_piece) - Atomic, ONE thing
```

## Key Concepts

- **Flow is mandatory**: All 9 steps must be completed in order
- **Step skipping blocked**: Server returns error if steps are skipped
- **User decision required**: When skipping is attempted, Claude must explain and ask user
- **Warnings require confirmation**: Validation warnings need explicit user approval
- **Documentation is mandatory**: Step 9 cannot be skipped

## Language Support

Naming conventions and code smell detection for:
- **Godot**: `*_piece.gd`, `*_component.gd`, `*_system.gd`, `*_screen.gd`
- **Python**: `pieces/`, `components/`, `systems/`, `screens/` folders
- **Web**: `atoms/`, `molecules/`, `organisms/`, `templates/` (Atomic Design)
