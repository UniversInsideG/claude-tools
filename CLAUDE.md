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
    │   ├── filosofia.md      # /filosofia command (10-step flow)
    │   └── arquitectura.md   # /arquitectura command (refactoring analysis)
    ├── hooks/                # Legacy hooks (deprecated, MCP preferred)
    └── CLAUDE.md             # Instructions for end-user projects
```

### MCP Server (`philosophy-mcp/server.py`)

Single-file Python server implementing all MCP tools:

**Core Flow Tools (10 steps):**
0. `philosophy_q0_criterios` - Define criteria with user BEFORE designing (blocks q1)
1. `philosophy_q1_responsabilidad` - Single responsibility check
2. `philosophy_q2_reutilizacion` - Reusability analysis
3. `philosophy_q3_buscar` - Search for similar code/docs
4. `philosophy_q4_herencia` - Inheritance decision
5. `philosophy_q5_nivel` - Architecture level validation
6. `philosophy_q6_verificar_dependencias` - Verify external dependencies AND references (code to replicate)
7. (Write code)
8. `philosophy_validate` - Code validation (smells, duplication, reference properties)
9. `philosophy_q9_documentar` - Document changes (mandatory)

**Auxiliary Tools:**
- `philosophy_checklist` - Quick reference

**Duplication Detection (v1.7.0):**
- `calcular_similitud()` - Compares content using difflib.SequenceMatcher
- `detectar_duplicacion()` - Hybrid approach: suspicious patterns + similarity comparison
  - Only reports if similarity >60% between files
  - Does NOT flag false positives (_ready/_process in Godot are normal)

**Architecture Analysis Tools:**
- `philosophy_architecture_analysis` - Start global analysis
- `philosophy_architecture_status` - View current state
- `philosophy_architecture_resume` - Resume after compaction
- `philosophy_architecture_checkpoint` - Save progress

### Session State

The server maintains two state dictionaries:
- `SESSION_STATE` - Tracks the 10-step flow progress (resets per creation)
  - Includes `duplication_detected` with similarity analysis from q3
  - Includes `criterios_file` with path to criteria file written by q0
  - Includes `reference_properties` with extracted properties from q6 references (v2.2.0)
- `ARCHITECTURE_STATE` - Tracks architecture analysis progress (persists)

### 5-Level Architecture (equivalent to Atomic Design)

```
ESTRUCTURA (main.tscn)
    └── PANTALLA (*_screen) - Unique user view
          └── CONTENEDOR (*_system) - Reusable logic
                └── COMPONENTE (*_component) - Combines pieces
                      └── PIEZA (*_piece) - Atomic, ONE thing
```

## Critical Rule: Tools Guide Analysis (v2.3.0)

**PROHIBITED:** Analyzing code, reading files, or drawing conclusions BEFORE using `philosophy_q0_criterios` or `philosophy_architecture_analysis`.

**Why this matters:**
- When Claude analyzes before using tools, the analysis is superficial (guessing, assumptions, erratic changes)
- This biases the criteria in q0, which should reflect what the USER wants, not what Claude found
- The deep analysis that prevents errors gets lost

**Correct flow:**
```
User: "Investigate this bug"
Claude: [uses q0 FIRST to define criteria with user]
Claude: [THEN analyzes code guided by agreed criteria]
```

**q0 now detects (v2.3.0):**
1. Prior analysis patterns in reformulation (e.g., "I found", "the bug is", "line 123")
2. Implementation details in criteria instead of functional requirements

**Good vs Bad criteria:**
- ❌ BAD: "use layout_mode = 0" (implementation detail)
- ✅ GOOD: "image should scale maintaining aspect ratio" (functional requirement)

## Key Concepts

- **Criteria phase (v2.0.0)**: Step 0 forces Claude to define criteria with user before q1
- **Persistent criteria (v2.1.0)**: q0 requires `project_path` and writes criteria to `.claude/criterios_{tarea}.md`
- **Architecture↔criteria connection (v2.1.0)**: `architecture_analysis` checks `SESSION_STATE["step_0"]` for current session, falls back to disk search for resumed sessions
- **Flow is mandatory**: All 10 steps must be completed in order
- **Step skipping blocked**: Server returns error if steps are skipped
- **User decision required**: When skipping is attempted, Claude must explain and ask user
- **User decision two-step (v2.4.0)**: Skipping steps requires two calls: 1) `decision_usuario=true` + `justificacion_salto`, 2) `usuario_verifico=true` after user confirms
- **Warnings require confirmation**: Validation warnings need explicit user approval
- **Documentation is mandatory**: Step 9 cannot be skipped
- **Duplication detection (v1.7.0)**: q3 detects REAL duplication (>60% similarity between files)
- **User must decide on duplication**: Claude must ANALYZE, EXPLAIN, and ASK user before continuing
- **Ignore requires keyword**: Option D "Ignore" requires justification starting with "USUARIO:"
- **Reference analysis (v2.2.0)**: q6 accepts optional `references` parameter to extract properties from code to replicate
- **Reference verification (v2.2.0)**: validate checks that reference properties were included in written code
- **q0 blocks implementation criteria (v2.4.0)**: Second call (`confirmado_por_usuario=true`) re-checks criteria patterns and blocks if implementation details found
- **Validate .tscn (v2.4.0)**: step8_validate has dedicated branch for .tscn/.tres files with DRY checks (duplicate SubResources, repeated theme_overrides, hardcoded colors)
- **q3 ripgrep (v2.4.0)**: Search uses `rg` subprocess when available, falls back to Python rglob
- **Checkpoint 4 hard STOP (v2.4.0)**: Architecture checkpoint 4 returns STOP requiring user confirmation via AskUserQuestion before implementation
- **plan_approved gate (v2.5.0)**: `ARCHITECTURE_STATE["plan_approved"]` blocks q1 when architecture analysis has checkpoint >= 4 but user hasn't approved. Set to False on FASE_4, True on EJECUTANDO. `architecture_resume` infers from saved state. Enforcement in code, not just text instructions.
- **Checkpoint 4 functional devolución (v2.5.0)**: Instructions rewritten with QUÉ/PARA QUÉ/POR QUÉ format, requiring both functional (what changes for the user) and technical (what code changes) explanation per task before asking for approval
- **Expanded analysis persistence (v2.5.0)**: Checkpoint 4 instructions tell Claude to save additional analysis with architecture_checkpoint before presenting, so it persists on context compaction
- **q0 presentation gate (v2.4.0)**: `step_0_presented` blocks `confirmado_por_usuario=true` if criteria weren't presented first with `confirmado_por_usuario=false`
- **architecture_analysis criterios_file (v2.4.0)**: Accepts optional `criterios_file` parameter to use criteria from a previous session without blocking
- **q9 descripcion_funcional (v2.4.0)**: New parameter to document what changes for the user (functional), not just the technical change. CHANGELOG template shows both lines.

## User Decision Parameter (v2.4.0, replaces v1.8.0)

All tools q2-q9 support a **two-step** process to skip steps:

**Step 1:** Call with `decision_usuario=true` + `justificacion_salto="reason"`
- MCP stores the justification and returns STOP
- Claude must present justification to user with AskUserQuestion

**Step 2:** Call with `usuario_verifico=true` (after user confirms)
- MCP verifies stored justification exists
- Allows skipping the step

**Guards:**
- Both params in same call → resolved in one step (if `justificacion_salto` provided or stored)
- `usuario_verifico` without prior justification → rejected
- `decision_usuario` without `justificacion_salto` → rejected

## Reference Analysis (v2.2.0)

q6 now supports a `references` parameter for exhaustive analysis of code to replicate:

```python
"references": [
    {
        "file": "scripts/master.gd",      # Required: file path
        "start_line": 2132,               # Optional: 1-indexed
        "end_line": 2150,                 # Optional: 1-indexed
        "search_pattern": "TextureRect",  # Optional: find block by pattern
        "must_document": ["layout_mode", "anchors_preset", "stretch_mode"]  # Required
    }
]
```

**How it works:**
1. q6 reads the reference file and extracts values for `must_document` properties
2. Shows extracted values in output (forces Claude to see them)
3. Saves properties in `SESSION_STATE["reference_properties"]`
4. validate (step 8) checks that written code includes these properties
5. If properties are missing, validate shows warning

**Use case:** When replicating UI configurations, node properties, or code patterns that must match exactly.

## Language Support

Naming conventions and code smell detection for:
- **Godot**: `*_piece.gd`, `*_component.gd`, `*_system.gd`, `*_screen.gd`
- **Python**: `pieces/`, `components/`, `systems/`, `screens/` folders
- **Web**: `atoms/`, `molecules/`, `organisms/`, `templates/` (Atomic Design)
