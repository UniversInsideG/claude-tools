# Instrucciones para Claude Code - UniversInside

## Filosofía de Programación Obligatoria

> "Máximo impacto, menor esfuerzo — a largo plazo"

SIEMPRE usar el MCP `philosophy` antes de escribir código. El flujo es obligatorio.

---

## Arquitectura: 4 Niveles

```
ESTRUCTURA (proyecto completo: main.tscn)
    └── CONTENEDOR (systems/*_system.gd)
          └── COMPONENTE (components/*_component.gd)
                └── PIEZA (pieces/*_piece.gd)
```

---

## Nomenclatura Obligatoria

| Nivel | Godot | Python | Web |
|-------|-------|--------|-----|
| Pieza | `pieces/*_piece.gd` | `pieces/*.py` | `atoms/` |
| Componente | `components/*_component.gd` | `components/*.py` | `molecules/` |
| Contenedor | `systems/*_system.gd` | `systems/*.py` | `organisms/` |

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
