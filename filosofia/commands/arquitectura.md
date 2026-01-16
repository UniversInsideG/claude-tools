---
description: Análisis arquitectónico global para refactorizaciones (exhaustivo, sistemático y exacto)
---

# ANÁLISIS ARQUITECTÓNICO GLOBAL

> **"El análisis ES exhaustivo, sistemático y exacto"**
>
> **"Verificar ANTES de escribir, no DESPUÉS de fallar"**
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
- **INCLUYE FIRMAS PÚBLICAS** de cada archivo (extraídas automáticamente)
- Las firmas son la base para verificar dependencias
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=1

### FASE 2: MAPA DE FUNCIONALIDADES
- Identificar QUÉ HACE cada parte
- **USAR LAS FIRMAS VERIFICADAS** del inventario
- No asumir firmas, usar las reales
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=2

### FASE 3: CLASIFICACIÓN POR NIVELES
- Mapear cada archivo al nivel correcto
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=3

### FASE 4: PLAN DE REFACTORIZACIÓN
- Generar plan ordenado
- **CADA TAREA DEBE INCLUIR:**
  - Test de verificación específico
  - **DEPENDENCIAS EXTERNAS VERIFICADAS** (funciones que va a llamar)
- Formato de tarea:
```
TAREA X.Y: [descripción]
ARCHIVO ORIGEN: [ruta]
ARCHIVO DESTINO: [ruta]
DEPENDENCIAS VERIFICADAS:
  - archivo.gd → funcion(params) -> tipo ✓
  - otro.gd → otra_funcion(params) -> tipo ✓
TEST: [cómo verificar que funciona]
```
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=4

---

## FASE 5: EJECUCIÓN CON PRUEBAS (CRÍTICA)

Esta es la fase donde se refactoriza. **OBLIGATORIO seguir este flujo para CADA tarea:**

### PASO 1: Leer la tarea del plan
Identifica:
- Qué hacer
- Archivo origen
- Archivo destino
- **DEPENDENCIAS VERIFICADAS** (del plan)
- **TEST DE VERIFICACIÓN** (del plan)

### PASO 2: Implementar usando /filosofia
Usa el flujo q1→q8 para implementar la tarea.
**IMPORTANTE:** En q6 (verificar dependencias), usa las firmas del plan.

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
DEPENDENCIAS: [X funciones verificadas]
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
│ 1. Leer dependencias del plan                               │
│ 2. Implementar (usar /filosofia con q6)                     │
│ 3. EJECUTAR TEST ←── OBLIGATORIO                            │
│ 4. ¿Pasó?                                                   │
│    ├─ SÍ → Marcar completada → TAREA 1.2                    │
│    └─ NO → Corregir → Volver a paso 3                       │
└─────────────────────────────────────────────────────────────┘
```

---

## EJEMPLO DE TAREA CON DEPENDENCIAS

```
TAREA 1.1: Extraer lógica de autenticación
ARCHIVO ORIGEN: src/main_controller.gd:45-120
ARCHIVO DESTINO: systems/auth_system.gd
DEPENDENCIAS VERIFICADAS:
  - components/user_data.gd → get_current_user() -> User ✓
  - pieces/crypto_piece.gd → hash_password(pass: String) -> String ✓
TEST: "Hacer login con usuario válido, verificar que funciona"

[Implemento la tarea usando /filosofia]
[En q6 verifico las dependencias listadas]

EJECUTANDO TEST:
- Acción: Ejecutar login con usuario "test@test.com"
- Esperado: Login exitoso, redirección a dashboard
- Resultado: ✅ Login exitoso, usuario redirigido correctamente

RESULTADO: ✅ PASÓ
→ Continúo con tarea 1.2
```

---

## HERRAMIENTAS

| Herramienta | Cuándo |
|-------------|--------|
| `philosophy_architecture_analysis` | Iniciar análisis nuevo (extrae firmas públicas) |
| `philosophy_architecture_status` | Ver estado actual |
| `philosophy_architecture_checkpoint` | Guardar progreso de fases 1-4 |
| `philosophy_architecture_resume` | Retomar si se compactó |
| `philosophy_q6_verificar_dependencias` | Verificar firmas antes de escribir código |

---

## RESUMEN DE OBLIGACIONES

1. ✅ Checkpoint después de cada fase (1-4)
2. ✅ FASE 1 extrae firmas públicas automáticamente
3. ✅ FASE 2 usa firmas verificadas, no asumidas
4. ✅ FASE 4: cada tarea lista dependencias verificadas
5. ✅ FASE 5: usar q6 para verificar dependencias antes de escribir
6. ✅ **EJECUTAR test después de cada tarea en fase 5**
7. ✅ **NO continuar si el test falla**
8. ✅ Usar resume si se compacta la conversación

---

## TAREA DEL USUARIO
$ARGUMENTS

---

## EMPIEZA AHORA

1. `philosophy_architecture_status` → verificar estado
2. Si no hay análisis → `philosophy_architecture_analysis`
3. Si hay análisis → continuar desde la fase indicada
4. En FASE 5 → **verificar dependencias (q6) + test obligatorio**
