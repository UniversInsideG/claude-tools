# Instrucciones para Claude Code - UniversInside

## Filosofía de Programación Obligatoria

> "Máximo impacto, menor esfuerzo — a largo plazo"

SIEMPRE usar el MCP `philosophy` antes de escribir código. El flujo es obligatorio.

---

## Arquitectura: 5 Niveles (= Atomic Design)

```
ESTRUCTURA (proyecto completo: main.tscn)
    └── PANTALLA (vista única del usuario: screens/*_screen)
          └── CONTENEDOR (lógica reutilizable: systems/*_system)
                └── COMPONENTE (combina piezas: components/*_component)
                      └── PIEZA (atómica: pieces/*_piece)
```

**Contenedor vs Pantalla:**
- Contenedor = lógica reutilizable en varias pantallas
- Pantalla = vista única del usuario (no reutilizable)

---

## Nomenclatura Obligatoria

| Nivel | Godot | Python | Web |
|-------|-------|--------|-----|
| 1. Pieza | `pieces/*_piece.(gd\|tscn)` | `pieces/*.py` | `atoms/` |
| 2. Componente | `components/*_component.(gd\|tscn)` | `components/*.py` | `molecules/` |
| 3. Contenedor | `systems/*_system.(gd\|tscn)` | `systems/*.py` | `organisms/` |
| 4. Pantalla | `screens/*_screen.(gd\|tscn)` | `screens/*.py` | `templates/` |
| 5. Estructura | `main.tscn` | `main.py` | `app/` |

> **Godot:** La extensión (`.gd` o `.tscn`) no determina el nivel. Lo determina la nomenclatura (`*_piece`, `*_component`, etc.).

---

## Flujo Obligatorio: 7 Pasos

Usar las herramientas del MCP `philosophy` en orden:

1. **`philosophy_q1_responsabilidad`** - ¿Hace UNA sola cosa?
2. **`philosophy_q2_reutilizacion`** - ¿Puedo reutilizar?
3. **`philosophy_q3_buscar`** - ¿Existe algo similar?
4. **`philosophy_q4_herencia`** - ¿Se actualizan las instancias?
5. **`philosophy_q5_nivel`** - ¿Nivel correcto? (valida nomenclatura)
6. **Escribir código**
7. **`philosophy_validate`** - Validar código escrito

El MCP bloquea si se salta un paso.

---

## Las 5 Preguntas

Antes de escribir código, responder:

1. ¿Esta pieza hace UNA sola cosa?
2. ¿Puedo reutilizar esto en otro lugar?
3. ¿Existe algo similar que pueda extender/heredar?
4. ¿Si cambio la base, se actualizarán todas las instancias?
5. ¿Está en el nivel correcto de la jerarquía?

---

## Comando Rápido

Usa `/filosofia [tarea]` para activar el flujo completo.

---

**Documentación completa:** `CODING_PHILOSOPHY.md`
**Implementación MCP:** `philosophy-mcp/IMPLEMENTACION_MCP.md`
