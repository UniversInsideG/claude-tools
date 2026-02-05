---
description: Análisis arquitectónico global para refactorizaciones (exhaustivo, sistemático y exacto)
---

# ANÁLISIS ARQUITECTÓNICO GLOBAL

> **"El análisis ES exhaustivo, sistemático y exacto"**
>
> **"Verificar ANTES de escribir, no DESPUÉS de fallar"**

## ⛔ REGLA CRÍTICA: NO ANALICES ANTES DE USAR ESTA HERRAMIENTA

**PROHIBIDO** analizar código, leer archivos, o sacar conclusiones ANTES de usar `philosophy_q0_criterios`.

❌ **INCORRECTO:**
```
Usuario: "Investiga este bug"
Claude: [lee código, saca conclusiones] ← PROHIBIDO
Claude: [usa arquitectura con criterios sesgados]
```

✅ **CORRECTO:**
```
Usuario: "Investiga este bug"
Claude: [usa q0 PRIMERO para definir criterios con el usuario]
Claude: [DESPUÉS analiza código usando las fases de arquitectura]
```

**¿Por qué?** Cuando analizas antes:
- Haces análisis superficial (suposiciones, cambios erráticos)
- Llegas al análisis arquitectónico con conclusiones sesgadas
- Las fases de análisis exhaustivo se vuelven redundantes
- El análisis profundo que evita errores se pierde

**Las herramientas GUÍAN el análisis desde cero, no validan conclusiones previas.**

---

## ANTES DE TODO: COMPRENDER LA TAREA

Usa `philosophy_q0_criterios` con `confirmado_por_usuario=false` para iniciar la fase de comprensión. El MCP te guiará para:

1. **Reformular lo que entendiste** — para exponer tu interpretación antes de que se convierta en análisis, porque los supuestos ocultos son la causa principal de análisis en la dirección equivocada. Si tu reformulación es incorrecta, el usuario puede corregirla antes de que produzca un plan de refactorización inválido.

2. **Identificar lo que no sabes o asumes** — para hacer las preguntas correctas, porque preguntar lo incorrecto no resuelve la ambigüedad. El coste de una pregunta es mínimo; el coste de analizar en la dirección equivocada es un análisis completo que hay que rehacer.

3. **Presentar criterios de éxito al usuario** — para tener una referencia de éxito compartida, porque sin criterios acordados no hay forma de saber si el resultado del análisis es correcto ni si las tareas de refactorización cumplen el objetivo real.

4. **ESPERAR confirmación del usuario** — para actuar sobre información real, no sobre suposiciones. La pregunta es el final del turno. NO ejecutes herramientas de análisis en el mismo turno donde presentas los criterios.

5. **Tras confirmación, llamar con `confirmado_por_usuario=true`** — para desbloquear el flujo con criterios validados. Documéntalos en `.claude/criterios_[nombre-tarea].md` con los criterios exactos: qué se hace, para qué, y qué debe cumplir. Sin resumir ni parafrasear — los criterios exactos tal cual se acordaron. Este archivo persiste entre sesiones y después de compactación.

Solo después de documentar los criterios, continúa con los pasos siguientes.

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

Después de comprender la tarea (Paso 0), verifica si hay un análisis previo:

1. Usa `philosophy_architecture_status`
2. Si hay análisis activo → continúa desde donde se quedó
3. Si no hay análisis pero el usuario menciona continuar → usa `philosophy_architecture_resume`

No empieces de cero si ya existe un análisis.

---

## FASES DE ANÁLISIS (1-4)

### INICIAR ANÁLISIS
```
philosophy_architecture_analysis(
    project_path="ruta",
    language="godot|python|web|other",
    project_name="nombre"
)
```

### FASE 1: INVENTARIO EXHAUSTIVO
Documentar TODOS los archivos e incluir firmas públicas de cada uno — para tener una base de datos real de lo que existe, porque sin inventario completo las fases posteriores trabajan con información parcial y las decisiones de refactorización ignoran dependencias reales.
- **INCLUYE FIRMAS PÚBLICAS** de cada archivo (extraídas automáticamente)
- Las firmas son la base para verificar dependencias en fases posteriores
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=1

### FASE 2: MAPA DE FUNCIONALIDADES
Identificar QUÉ HACE cada parte usando las firmas verificadas del inventario — para entender la responsabilidad real de cada archivo antes de moverlo, porque asumir lo que hace un archivo sin leerlo produce planes de refactorización que rompen funcionalidad.
- **USAR LAS FIRMAS VERIFICADAS** del inventario, no asumir
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=2

### FASE 3: CLASIFICACIÓN POR NIVELES
Mapear cada archivo al nivel correcto de la arquitectura (pieza/componente/contenedor/pantalla/estructura) — para detectar qué archivos están en el nivel equivocado, porque un archivo en el nivel incorrecto tiene dependencias incorrectas y nomenclatura que no refleja su rol real.
- Al terminar → `philosophy_architecture_checkpoint` con checkpoint=3

### FASE 4: PLAN DE REFACTORIZACIÓN
Generar plan ordenado con tareas concretas — para tener una secuencia verificable de cambios, porque ejecutar refactorizaciones sin plan produce cambios que se anulan entre sí o rompen dependencias no detectadas.
- **CADA TAREA DEBE INCLUIR:**
  - Test de verificación específico — para saber si la tarea funcionó antes de pasar a la siguiente
  - **DEPENDENCIAS EXTERNAS VERIFICADAS** — para no llamar funciones que no existen o con firmas incorrectas
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
Para tener claro el alcance exacto antes de tocar código, porque implementar sin leer la tarea produce cambios que no coinciden con el plan.
- Qué hacer, archivo origen, archivo destino
- **DEPENDENCIAS VERIFICADAS** (del plan)
- **TEST DE VERIFICACIÓN** (del plan)

### PASO 2: Implementar usando /filosofia
Para que cada tarea pase el mismo flujo de diseño que código nuevo, porque una refactorización sin verificación de responsabilidad, herencia y dependencias introduce los mismos problemas que intenta resolver.
- Usa el flujo q0→q9 para implementar la tarea
- En q6 (verificar dependencias), usa las firmas del plan

### PASO 3: EJECUTAR EL TEST (OBLIGATORIO)
Para verificar que la tarea funciona antes de pasar a la siguiente, porque sin test los errores se acumulan y al final no se sabe cuál tarea rompió qué. **NO PUEDES SALTARTE ESTE PASO.**

Ejemplos:
- "Ejecutar el proyecto y verificar que X funciona"
- "Llamar a la función Y y verificar que retorna Z"
- "Abrir la pantalla y verificar que muestra los datos"

### PASO 4: Reportar resultado
Para que el usuario vea evidencia concreta de que la tarea pasó, porque "funciona" sin evidencia no es verificable.
```
TAREA: [nombre]
DEPENDENCIAS: [X funciones verificadas]
TEST: [descripción del test]
RESULTADO: ✅ PASÓ | ❌ FALLÓ
EVIDENCIA: [qué verificaste]
```

### PASO 5: Decidir siguiente acción
Para evitar que errores se propaguen entre tareas, porque continuar con una tarea fallida acumula errores que se vuelven imposibles de diagnosticar.

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

## EMPIEZA

1. Comprende la tarea (sección "ANTES DE TODO" arriba) y verifica con el usuario
2. `philosophy_architecture_status` → verificar estado
3. Si no hay análisis → `philosophy_architecture_analysis`
4. Si hay análisis → continuar desde la fase indicada
5. En FASE 5 → **verificar dependencias (q6) + test obligatorio**
