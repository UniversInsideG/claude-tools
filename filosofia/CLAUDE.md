# Instrucciones para Claude Code - UniversInside

## REGLA PRINCIPAL: SEGUIR INSTRUCCIONES DEL MCP

**OBLIGATORIO:** Cuando el MCP `philosophy` te dé una instrucción, DEBES seguirla.

### Cuando el MCP dice "USA AskUserQuestion":
1. **EXPLICA** tu argumento/opinión al usuario
2. **USA** la herramienta AskUserQuestion
3. **ESPERA** la decisión del usuario

### Cuando q3 detecta DUPLICACIÓN:
1. **ANALIZA** los archivos con similitud (lee el contenido)
2. **EXPLICA** al usuario qué código está duplicado y tu recomendación
3. **PREGUNTA** con AskUserQuestion: A) Crear base, B) Heredar, C) Refactorizar, D) Ignorar
4. **USA** la respuesta en q4:
   - Si D (ignorar) → justificación debe empezar con "USUARIO: [razón]"

### PROHIBIDO:
- Decidir por tu cuenta ignorar warnings o saltar pasos
- Argumentar "es código estándar" sin preguntar al usuario
- Continuar sin seguir las instrucciones del MCP
- Mover funciones a utils/helpers como "solución" a duplicación (es PARCHE, no arquitectura)

---

## Filosofía de Programación Obligatoria

> "Máximo impacto, menor esfuerzo — a largo plazo"

SIEMPRE usar el MCP `philosophy` antes de escribir o modificar código. El flujo es obligatorio.

### ⚠️ APLICA A TODO (SIN EXCEPCIONES):

| Tipo | ¿Usar flujo? | Por qué |
|------|--------------|---------|
| Código nuevo | ✅ SÍ | Diseño correcto desde inicio |
| Bug fix | ✅ SÍ | Un bug es señal de problema estructural |
| Modificación | ✅ SÍ | Verificar que no rompe arquitectura |
| Refactor | ✅ SÍ | Oportunidad de mejorar |

**NUNCA racionalizar para saltarse el flujo.** "Es solo un fix pequeño" es una excusa.

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

## Flujo Obligatorio: 9 Pasos

> **"Verificar ANTES de escribir, no DESPUÉS de fallar"**
> **"Documentar DESPUÉS de validar"**

Usar las herramientas del MCP `philosophy` en orden:

1. **`philosophy_q1_responsabilidad`** - ¿Hace UNA sola cosa?
2. **`philosophy_q2_reutilizacion`** - ¿Puedo reutilizar?
3. **`philosophy_q3_buscar`** - ¿Existe algo similar?
4. **`philosophy_q4_herencia`** - ¿Se actualizan las instancias?
5. **`philosophy_q5_nivel`** - ¿Nivel correcto? (valida nomenclatura)
6. **`philosophy_q6_verificar_dependencias`** - ¿Las dependencias externas existen y coinciden?
7. **Escribir código**
8. **`philosophy_validate`** - Validar código escrito
9. **`philosophy_q9_documentar`** - Documentar cambios (OBLIGATORIO)

**El MCP bloquea si se salta un paso.** Si intentas saltar:
- DEBES explicar por qué
- DEBES usar AskUserQuestion para preguntar al usuario

---

## Las 5 Preguntas + Verificación

Antes de escribir código, responder:

1. ¿Esta pieza hace UNA sola cosa?
2. ¿Puedo reutilizar esto en otro lugar?
3. ¿Existe algo similar que pueda extender/heredar?
4. ¿Si cambio la base, se actualizarán todas las instancias?
5. ¿Está en el nivel correcto de la jerarquía?
6. ¿Las dependencias externas existen y sus firmas coinciden?

---

## Comando Rápido

Usa `/filosofia [tarea]` para activar el flujo completo.

---

**Documentación completa:** `CODING_PHILOSOPHY.md`
**Implementación MCP:** `philosophy-mcp/IMPLEMENTACION_MCP.md`
