---
description: Análisis arquitectónico global para refactorizaciones (exhaustivo, sistemático y exacto)
---

# ANÁLISIS ARQUITECTÓNICO GLOBAL

> **"El análisis ES exhaustivo, sistemático y exacto"**
>
> No es opcional. No se abrevia. No se salta nada.

---

## REGLA CRÍTICA: TESTS DE VERIFICACIÓN

**NUNCA continuar a la siguiente tarea sin probar que la actual funciona.**

```
INCORRECTO:                          CORRECTO:
Tarea 1 → Tarea 2 → Tarea 3          Tarea 1 → TEST → ✅ → Tarea 2 → TEST → ✅ → Tarea 3
(se acumulan errores)                (errores detectados temprano)
```

Si saltas un test y algo falla después, tendrás que deshacer múltiples cambios.

---

## DETECCIÓN DE COMPACTACIÓN

**ANTES DE HACER CUALQUIER COSA:**

1. Usa `philosophy_architecture_status`
2. Si hay análisis activo → continúa desde donde se quedó
3. Si no hay análisis pero el usuario menciona continuar → usa `philosophy_architecture_resume`

**NUNCA empieces de cero si ya existe un análisis.**

---

## FASES DE ANÁLISIS (1-4)

### FASE 0: INICIAR
```
philosophy_architecture_analysis(
    project_path="ruta",
    language="godot|python|web|other",
    project_name="nombre"
)
```

### FASE 1: INVENTARIO EXHAUSTIVO
- Documentar TODOS los archivos
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=1

### FASE 2: MAPA DE FUNCIONALIDADES
- Identificar QUÉ HACE cada parte
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=2

### FASE 3: CLASIFICACIÓN POR NIVELES
- Mapear cada archivo al nivel correcto
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=3

### FASE 4: PLAN DE REFACTORIZACIÓN
- Generar plan ordenado
- **CADA TAREA DEBE TENER UN TEST DE VERIFICACIÓN ESPECÍFICO**
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=4

---

## FASE 5: EJECUCIÓN CON PRUEBAS (CRÍTICA)

Esta es la fase donde se refactoriza. **OBLIGATORIO seguir este flujo para CADA tarea:**

### PASO 1: Leer la tarea del plan
Identifica:
- Qué hacer
- Archivo origen
- Archivo destino
- **TEST DE VERIFICACIÓN** (definido en el plan)

### PASO 2: Implementar usando /filosofia
Usa el flujo q1→q7 para implementar la tarea.

### PASO 3: EJECUTAR EL TEST (OBLIGATORIO)
**NO PUEDES SALTARTE ESTE PASO.**

Ejecuta el test de verificación definido en el plan. Ejemplos:
- "Ejecutar el proyecto y verificar que X funciona"
- "Llamar a la función Y y verificar que retorna Z"
- "Abrir la pantalla y verificar que muestra los datos"

### PASO 4: Reportar resultado
Muestra al usuario:
```
TAREA: [nombre]
TEST: [descripción del test]
RESULTADO: ✅ PASÓ | ❌ FALLÓ
EVIDENCIA: [qué verificaste]
```

### PASO 5: Decidir siguiente acción

**SI EL TEST PASÓ:**
- Marcar tarea como completada en el archivo
- Continuar con la siguiente tarea

**SI EL TEST FALLÓ:**
- **NO CONTINUAR** con la siguiente tarea
- Diagnosticar el problema
- Corregir
- Volver a ejecutar el test
- Solo cuando pase, continuar

---

## FLUJO VISUAL FASE 5

```
┌─────────────────────────────────────────────────────────────┐
│ TAREA 1.1                                                   │
├─────────────────────────────────────────────────────────────┤
│ 1. Implementar (usar /filosofia)                            │
│ 2. EJECUTAR TEST ←── OBLIGATORIO                            │
│ 3. ¿Pasó?                                                   │
│    ├─ SÍ → Marcar completada → TAREA 1.2                    │
│    └─ NO → Corregir → Volver a paso 2                       │
└─────────────────────────────────────────────────────────────┘
```

---

## EJEMPLO DE EJECUCIÓN CORRECTA

```
TAREA 1.1: Extraer lógica de autenticación
TEST DEFINIDO: "Hacer login con usuario válido, verificar que funciona"

[Implemento la tarea usando /filosofia]

EJECUTANDO TEST:
- Acción: Ejecutar login con usuario "test@test.com"
- Esperado: Login exitoso, redirección a dashboard
- Resultado: ✅ Login exitoso, usuario redirigido correctamente

RESULTADO: ✅ PASÓ
→ Continúo con tarea 1.2
```

```
TAREA 1.2: Extraer validación de formularios
TEST DEFINIDO: "Enviar formulario vacío, verificar mensaje de error"

[Implemento la tarea usando /filosofia]

EJECUTANDO TEST:
- Acción: Enviar formulario con campos vacíos
- Esperado: Mostrar "Campos requeridos"
- Resultado: ❌ No muestra mensaje, formulario se envía

RESULTADO: ❌ FALLÓ
→ NO continúo. Diagnostico y corrijo primero.
```

---

## HERRAMIENTAS

| Herramienta | Cuándo |
|-------------|--------|
| `philosophy_architecture_analysis` | Iniciar análisis nuevo |
| `philosophy_architecture_status` | Ver estado actual |
| `philosophy_architecture_checkpoint` | Guardar progreso de fases 1-4 |
| `philosophy_architecture_resume` | Retomar si se compactó |

---

## RESUMEN DE OBLIGACIONES

1. ✅ Checkpoint después de cada fase (1-4)
2. ✅ Cada tarea del plan tiene test definido
3. ✅ **EJECUTAR test después de cada tarea en fase 5**
4. ✅ **NO continuar si el test falla**
5. ✅ Usar resume si se compacta la conversación

---

## TAREA DEL USUARIO
$ARGUMENTS

---

## EMPIEZA AHORA

1. `philosophy_architecture_status` → verificar estado
2. Si no hay análisis → `philosophy_architecture_analysis`
3. Si hay análisis → continuar desde la fase indicada
4. En FASE 5 → **test obligatorio después de cada tarea**
