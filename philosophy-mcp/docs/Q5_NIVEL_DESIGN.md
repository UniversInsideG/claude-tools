# Diseño: Paso Q5 - Nivel Correcto

**Fecha:** 2026-01-16
**Estado:** IMPLEMENTADO

---

## QUÉ MIDE Q5

**Pregunta:** ¿Está en el nivel correcto de la jerarquía?

**Lo que mide:** Si el código **FUNCIONA** como el nivel indicado.

**Lo que NO mide:** Si el archivo tiene el nombre correcto.

---

## PRINCIPIO CLAVE

> El nivel se determina por el **COMPORTAMIENTO** del código, no por el **NOMBRE** del archivo.

El nombre es una **CONSECUENCIA** del nivel, no al revés.

---

## NIVELES Y SU COMPORTAMIENTO

| Nivel | ¿Qué HACE el código? | Palabras clave en justificación |
|-------|---------------------|--------------------------------|
| Pieza | UNA sola cosa atómica | "una sola cosa", "atómico", "mínimo", "único" |
| Componente | Combina piezas | "combina piezas", "agrupa", "UI elements", "junta" |
| Contenedor | Orquesta componentes, lógica reutilizable | "orquesta", "coordina", "sistema", "reutilizable en pantallas" |
| Pantalla | Vista única del usuario | "vista", "screen", "pantalla única", "usuario ve" |
| Estructura | Proyecto completo | "proyecto", "main", "aplicación completa" |

---

## FLUJO DE VALIDACIÓN

### 1. Usuario proporciona:
- `nivel`: pieza/componente/contenedor/pantalla/estructura
- `filename`: nombre del archivo
- `justificacion_nivel`: por qué es ese nivel (basado en comportamiento)

### 2. MCP valida COMPORTAMIENTO:
- ¿La justificación corresponde al nivel indicado?
- ¿El código hace lo que dice el nivel?

### 3. MCP verifica NOMENCLATURA (secundario):
- ¿El nombre del archivo sigue la convención?
- Si NO coincide → **deuda técnica de naming**

### 4. Resultado:

**Si comportamiento correcto + nombre correcto:**
```
✅ NIVEL VALIDADO
✅ NOMENCLATURA CORRECTA
```

**Si comportamiento correcto + nombre incorrecto:**
```
✅ NIVEL VALIDADO

⚠️ DEUDA TÉCNICA: Naming
   Actual:    island_chat_panel.gd
   Sugerido:  island_chat_component.gd
   Motivo:    Archivo existente con dependencias
   Mejora:    Renombrar en refactor futuro
```

**Si comportamiento incorrecto:**
```
❌ NIVEL INCORRECTO

El código hace X pero indicaste nivel Y.
Según la justificación, debería ser nivel Z.
```

---

## DIFERENCIA POR TIPO DE CAMBIO

| Tipo | Nomenclatura | Comportamiento |
|------|--------------|----------------|
| Código nuevo | ✅ Exigir correcta | ✅ Validar |
| Modificación | ⚠️ Advertir si incorrecta | ✅ Validar |
| Bugfix | ⚠️ Advertir si incorrecta | ✅ Validar |
| Refactor | ⚠️ Advertir si incorrecta | ✅ Validar |

---

## NOMENCLATURA: DEUDA TÉCNICA, NO BLOQUEO

Cuando la nomenclatura no coincide con el nivel:

1. **NO BLOQUEAR** - el trabajo debe continuar
2. **ADVERTIR** - mostrar claramente la discrepancia
3. **SUGERIR** - proponer el nombre correcto
4. **DOCUMENTAR** - registrar como deuda técnica
5. **EXPLICAR** - por qué no se renombra ahora (dependencias)

---

## EJEMPLOS

### Ejemplo 1: Código nuevo, todo correcto
```
nivel: componente
filename: chat_component.gd
justificacion: "Combina Label, ScrollContainer, LineEdit y Button para chat"

→ ✅ Nivel correcto (combina piezas = componente)
→ ✅ Nomenclatura correcta (*_component.gd)
```

### Ejemplo 2: Modificación, nivel correcto, nombre legacy
```
nivel: componente
filename: island_chat_panel.gd
justificacion: "Combina piezas de UI para mostrar chat de isla"

→ ✅ Nivel correcto (combina piezas = componente)
→ ⚠️ Deuda técnica: Nombre debería ser island_chat_component.gd
→ ✅ Continuar (no bloquear)
```

### Ejemplo 3: Nivel incorrecto
```
nivel: pieza
filename: game_manager.gd
justificacion: "Coordina todos los sistemas del juego"

→ ❌ Nivel incorrecto
→ "Coordina sistemas" = CONTENEDOR, no pieza
→ Corregir nivel antes de continuar
```

---

## IMPLEMENTACIÓN

### Validación de comportamiento (por palabras clave)

```python
NIVEL_KEYWORDS = {
    "pieza": ["una sola cosa", "atómico", "mínimo", "único", "single"],
    "componente": ["combina", "agrupa", "piezas", "ui elements", "junta"],
    "contenedor": ["orquesta", "coordina", "sistema", "reutilizable", "lógica"],
    "pantalla": ["vista", "screen", "usuario ve", "pantalla única"],
    "estructura": ["proyecto", "main", "aplicación", "completo"]
}
```

### Niveles incompatibles (detectar errores obvios)

```python
NIVEL_INCOMPATIBLE = {
    "pieza": ["coordina", "orquesta", "sistemas", "pantallas"],
    "componente": ["coordina sistemas", "orquesta componentes"],
    "contenedor": ["vista única", "usuario ve"],
    "pantalla": ["atómico", "una sola cosa"],
}
```

---

## RESUMEN

| Aspecto | Validación | Bloquea |
|---------|------------|---------|
| Comportamiento del código | ✅ Obligatoria | ❌ Si incorrecto |
| Nomenclatura del archivo | ⚠️ Advertencia | ❌ Nunca (solo deuda técnica) |

> **"El nivel es el COMPORTAMIENTO, el nombre es la ETIQUETA"**

---

## TESTS REALIZADOS (2026-01-16)

| # | Escenario | Resultado | Comportamiento |
|---|-----------|-----------|----------------|
| 1 | Legacy file con comportamiento correcto | ✅ PASS | Acepta nivel, documenta deuda técnica de naming |
| 2 | Nivel incorrecto (comportamiento no coincide) | ✅ PASS | Bloquea y sugiere nivel correcto |
| 3 | Código nuevo sin nomenclatura correcta | ✅ PASS | Bloquea y exige nombre correcto |
| 4 | Código nuevo todo correcto | ✅ PASS | Acepta sin advertencias |

### Funciones implementadas

- `validar_comportamiento_nivel(nivel, justificacion)` → Valida por palabras clave
- `get_suggested_filename(nivel, filename, language)` → Genera nombre sugerido
- `step5_nivel()` → Actualizado para validar comportamiento primero
