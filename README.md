# Claude Tools - UniversInside

Colección de herramientas, configuraciones y comandos personalizados para Claude Code.

## Herramientas disponibles

| Herramienta | Descripción | Comando |
|-------------|-------------|---------|
| **Filosofía de Programación** | Arquitectura modular, validación automática, hooks | `/filosofia` |

## Instalación rápida

```bash
git clone https://github.com/universinsidegames/claude-tools.git
cd claude-tools/filosofia
./install.sh
```

## Estructura del repositorio

```
claude-tools/
├── README.md
└── filosofia/                       # Filosofía de programación modular
    ├── CLAUDE.md                    # Instrucciones automáticas
    ├── CODING_PHILOSOPHY.md         # Documentación completa
    ├── commands/
    │   └── filosofia.md             # Comando /filosofia
    ├── hooks/
    │   ├── planning_reminder.py     # Hook: recordatorio antes de planificar
    │   └── validate_philosophy.py   # Hook: validación antes de escribir
    └── install.sh                   # Instalador
```

## Sistema de Validación

El sistema funciona en **dos capas**:

```
USUARIO PIDE CÓDIGO
        ↓
┌─────────────────────────────────────────────┐
│  CAPA 1: PLANIFICACIÓN                      │
│  Hook: planning_reminder.py                 │
│                                             │
│  → Detecta si vas a pedir código            │
│  → Recuerda la filosofía a Claude           │
│  → Claude DEBE explicar su razonamiento     │
└─────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────┐
│  CAPA 2: VALIDACIÓN                         │
│  Hook: validate_philosophy.py               │
│                                             │
│  → Intercepta: Edit, Write, MCP Godot       │
│  → Valida: DRY, SOLID, nomenclatura         │
│  → Muestra advertencias si no cumple        │
└─────────────────────────────────────────────┘
```

## Qué valida

| Criterio | Qué detecta |
|----------|-------------|
| **Single Responsibility** | Muchas clases por archivo, funciones largas |
| **DRY** | Código repetido, patrones copy-paste |
| **Nomenclatura** | `*_component.gd`, `*_system.gd` |
| **Jerarquía** | Pieza → Componente → Contenedor → Estructura |
| **Godot** | Signals vs llamadas directas |
| **Python** | Herencia de clases base |

## Comandos disponibles

```bash
/filosofia           # Ver resumen de principios
/filosofia check     # Checklist antes de programar
/filosofia revisar archivo.gd  # Analizar un archivo
/filosofia doc       # Documentación completa
```

## Compatibilidad

- **MCP Godot**: Compatible con `gdai-mcp-plugin-godot`
- **Lenguajes**: GDScript, Python, PHP, JavaScript, HTML/CSS
- **Plataformas**: macOS, Linux, Windows (con bash)

## Principio Central

> **"Máximo impacto, menor esfuerzo — a largo plazo"**

---

*UniversInside - Arquitectura Modular Jerárquica*
