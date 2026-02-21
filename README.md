# Claude Tools - UniversInside

Colección de herramientas MCP para Claude Code que imponen filosofía de programación modular.

## MCP Servers disponibles

| MCP Server | Stack | Arquitectura | Comando |
|------------|-------|-------------|---------|
| **philosophy** | Godot (GDScript, .tscn) + Python | Pieza → Componente → Contenedor → Pantalla → Estructura | `/filosofia` |
| **web-philosophy** | HTML, CSS, JS vanilla | Atom → Molecule → Organism → Template → Page (Atomic Design) | `/filosofia` |

Ambos servidores comparten el mismo flujo de 10 pasos obligatorios (q0-q9) y las mismas protecciones (decision_usuario dos pasos, plan_approved gate, criterios persistentes).

## Instalación

### philosophy (Godot/Python)

```bash
cd philosophy-mcp
pip install -r requirements.txt
claude mcp add philosophy -- python3 $(pwd)/server.py
```

### web-philosophy (HTML/CSS/JS)

```bash
cd web-philosophy-mcp
pip install -r requirements.txt
claude mcp add web-philosophy -- python3 $(pwd)/server.py
```

### Verificar instalación

```bash
# En Claude Code
/mcp  # Debe mostrar "philosophy" y/o "web-philosophy"
```

## Estructura del repositorio

```
claude-tools/
├── README.md
├── CHANGELOG.md
├── CLAUDE.md
│
├── philosophy-mcp/               # MCP Server para Godot/Python
│   ├── server.py                 # Servidor MCP (~4600 líneas)
│   ├── requirements.txt
│   ├── INSTALAR.bat              # Instalador Windows
│   ├── ACTUALIZAR.bat            # Actualizador Windows
│   └── docs/                     # Documentos de diseño
│
├── web-philosophy-mcp/           # MCP Server para Web (HTML/CSS/JS)
│   ├── server.py                 # Servidor MCP (~4600 líneas)
│   └── requirements.txt
│
└── filosofia/                    # Configuración para usuarios
    ├── CLAUDE.md                 # Instrucciones para proyectos
    ├── CODING_PHILOSOPHY.md      # Documentación de la filosofía
    ├── commands/
    │   ├── filosofia.md          # Comando /filosofia (flujo de 10 pasos)
    │   └── arquitectura.md       # Comando /arquitectura (análisis global)
    └── hooks/                    # Hooks legacy (deprecado, MCP preferido)
```

## Flujo de 10 pasos (ambos servidores)

```
0. q0_criterios        → Definir criterios con el usuario (BLOQUEA q1)
1. q1_responsabilidad  → ¿Hace UNA sola cosa?
2. q2_reutilizacion    → ¿Puedo reutilizar?
3. q3_buscar           → ¿Existe algo similar?
4. q4_herencia         → ¿Se actualizan las instancias?
5. q5_nivel            → ¿Nivel correcto?
6. q6_verificar_deps   → ¿Las dependencias existen?
7. (Escribir código)
8. validate            → Validar el resultado
9. q9_documentar       → Documentar cambios
```

## Qué valida cada servidor

### philosophy (Godot/Python)

| Criterio | Qué detecta |
|----------|-------------|
| **Nomenclatura** | `*_piece.gd`, `*_component.gd`, `*_system.gd`, `*_screen.gd` |
| **Jerarquía** | Pieza → Componente → Contenedor → Pantalla → Estructura |
| **Godot** | Signals vs llamadas directas, .tscn DRY (SubResources, overrides) |
| **DRY** | Duplicación real (>60% similitud entre archivos) |

### web-philosophy (HTML/CSS/JS)

| Criterio | Qué detecta |
|----------|-------------|
| **Nomenclatura** | `atoms/`, `molecules/`, `organisms/`, `templates/`, `pages/` |
| **Jerarquía** | Atom → Molecule → Organism → Template → Page |
| **CSS** | Colores hardcodeados, `!important`, selectores profundos (>3 niveles), bloques duplicados |
| **HTML** | Estilos inline, div soup, imágenes sin alt, estructuras repetidas |
| **JS** | `var` en lugar de `const/let`, queries DOM sin cachear |
| **DRY visual** | Componentes visuales que deberían ser el mismo pero difieren |

## Principio Central

> **"Máximo impacto, menor esfuerzo — a largo plazo"**

---

*UniversInside - Arquitectura Modular Jerárquica*
