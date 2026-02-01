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

## Flujo Obligatorio: 10 Pasos

> **"Entender bien es la forma más rápida de resolver"**
> **"Verificar ANTES de escribir, no DESPUÉS de fallar"**
> **"Documentar DESPUÉS de validar"**

Usar las herramientas del MCP `philosophy` en orden:

0. **`philosophy_q0_criterios`** — para acordar con el usuario qué se hace y qué debe cumplir, porque sin criterios compartidos no hay forma de saber si el resultado es correcto. Llamar con `confirmado_por_usuario=false`, ESPERAR respuesta, y tras confirmación llamar con `confirmado_por_usuario=true`. **BLOQUEA q1.**
1. **`philosophy_q1_responsabilidad`** — para garantizar que cada pieza hace UNA sola cosa, porque mezclar responsabilidades genera código que hay que reescribir cuando cambia cualquiera de ellas.
2. **`philosophy_q2_reutilizacion`** — para decidir si el diseño permite reutilización, porque código que solo sirve en un lugar se duplica cuando se necesita en otro.
3. **`philosophy_q3_buscar`** — para encontrar código similar que ya existe, porque crear algo nuevo cuando ya hay algo que funciona es duplicación y deuda técnica.
4. **`philosophy_q4_herencia`** — para definir de qué hereda y qué reutiliza, porque si cambio la base deben actualizarse todas las instancias automáticamente.
5. **`philosophy_q5_nivel`** — para ubicar en el nivel correcto de la arquitectura, porque el nivel determina la nomenclatura, las dependencias permitidas y la granularidad.
6. **`philosophy_q6_verificar_dependencias`** — para confirmar que las funciones externas que voy a llamar existen y sus firmas coinciden, porque llamar a funciones inexistentes o con parámetros incorrectos produce errores que se detectan tarde.
7. **Escribir código** — usando las firmas verificadas y el diseño de los pasos anteriores.
8. **`philosophy_validate`** — para detectar code smells, duplicación y problemas estructurales, porque los errores de diseño son más baratos de corregir antes de que se integren.
9. **`philosophy_q9_documentar`** — para registrar qué se cambió y por qué, porque sin documentación el próximo cambio empieza sin contexto y repite errores. **(OBLIGATORIO)**

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
