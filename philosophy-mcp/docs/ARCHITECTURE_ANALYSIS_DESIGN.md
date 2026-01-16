# Diseño: Análisis Arquitectónico Global
**Fecha:** 2026-01-14
**Estado:** DISEÑO APROBADO - Pendiente implementación

---

## MÁXIMA

> **"El análisis ES exhaustivo, sistemático y exacto"**
>
> No es opcional. No se abrevia. No se salta nada.
> Cada archivo, cada función, cada línea relevante queda documentada.

---

## 1. PROBLEMA IDENTIFICADO

### Situación actual
El MCP de filosofía funciona bien para **cambios puntuales** (crear/modificar una pieza o componente específico), pero tiene limitaciones cuando se necesita:

- **Análisis arquitectónico global** para refactorizaciones masivas
- **Análisis exhaustivo** que no se salte nada
- **Persistencia** cuando la conversación se compacta

### Comportamiento problemático observado
- Claude tiende a "abreviar" o "reducir" el análisis profundo
- Se salta detalles cuando debería ser exhaustivo
- Si solo se enfoca en errores → soluciones parciales → deuda técnica → parches → se rompe algo que funcionaba

### Lo que se necesita
1. Analizar código que **YA FUNCIONA**
2. Entender **qué hace** (mapear funcionalidades)
3. **Rediseñar** aplicando la filosofía a todos los niveles
4. **Refactorizar manteniendo funcionalidad**
5. **Persistir** el análisis para que no se pierda si se compacta la conversación

---

## 2. SOLUCIÓN PROPUESTA

### Nueva herramienta: `philosophy_architecture_analysis`

**Propósito:** Análisis arquitectónico exhaustivo para refactorizaciones globales.

**Diferencia con flujo actual:**
```
FLUJO ACTUAL (granular):              NUEVO FLUJO (global):
┌─────────────────────┐               ┌─────────────────────────────────┐
│ q1 → q2 → q3 → q4   │               │ philosophy_architecture_analysis │
│ → q5 → código →     │               │                                 │
│ validate            │               │ Analiza TODO el módulo/proyecto │
│                     │               │ Mapea a 5 niveles               │
│ Para UNA pieza      │               │ Genera plan de refactorización  │
└─────────────────────┘               └─────────────────────────────────┘
                                                    ↓
                                      Luego aplica flujo granular (q1→q7)
                                      a cada pieza del plan
```

---

## 3. REQUISITOS CLAVE

### 3.1 Documentación PRIMERO
- Antes de analizar o tocar nada, **documentar el estado actual**
- El análisis debe **persistir en un archivo**, no solo en el chat
- Ubicación: `.claude/architecture_analysis_[proyecto]_[fecha].md`

### 3.2 Momentos de guardado prefijados (Checkpoints)
- No es un análisis de una sola vez
- Hay **checkpoints** donde se guarda el progreso
- Si la conversación se compacta, el archivo tiene todo
- Claude puede **retomar leyendo el archivo**

### 3.3 Exactitud obligatoria
- El análisis ES **exacto**, no aproximado
- Cada archivo, cada función, cada responsabilidad documentada
- Nada de generalidades → debe ser específico con archivo:línea

### 3.4 Plan con pruebas intermedias
- No es "refactorizar todo y probar al final"
- Cada fase tiene una **prueba de verificación**
- Si algo falla, se detecta temprano
- Permite validar que vamos en la dirección correcta

### 3.5 Scope flexible
- Puede analizar **todo el proyecto** (ideal)
- O puede analizar **un módulo/carpeta específica**

---

## 4. FLUJO DE LA HERRAMIENTA

```
┌─────────────────────────────────────────────────────────────────┐
│  FASE 0: DOCUMENTACIÓN (persistencia)                           │
│  → Crear archivo: .claude/architecture_analysis_[fecha].md      │
│  → Guardar estado actual ANTES de tocar nada                    │
│  → CHECKPOINT 0                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 1: INVENTARIO EXHAUSTIVO                                  │
│  → Escanear TODOS los archivos (sin excepción)                  │
│  → Documentar: archivo, líneas, clases, funciones               │
│  → CHECKPOINT 1 (guardar en archivo)                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 2: MAPA DE FUNCIONALIDADES                                │
│  → Identificar QUÉ HACE cada parte del código                   │
│  → Agrupar por funcionalidad, no por archivo                    │
│  → CHECKPOINT 2 (guardar en archivo)                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 3: CLASIFICACIÓN POR NIVELES                              │
│  → Mapear CADA archivo al nivel correcto                        │
│  → Detectar: nivel actual vs nivel correcto                     │
│  → Identificar problemas arquitectónicos                        │
│  → CHECKPOINT 3 (guardar en archivo)                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 4: PLAN DE REFACTORIZACIÓN                                │
│  → Generar plan ordenado por fases (pieza→pantalla)             │
│  → CADA tarea tiene TEST de verificación                        │
│  → CHECKPOINT 4 (guardar en archivo)                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 5: EJECUCIÓN CON PRUEBAS                                  │
│  → Ejecutar tarea del plan                                      │
│  → PROBAR que funciona                                          │
│  → Actualizar progreso en archivo                               │
│  → Repetir hasta completar                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. ESTRUCTURA DEL ARCHIVO DE DOCUMENTACIÓN

```markdown
# Análisis Arquitectónico: [nombre_proyecto]
Generado: 2026-01-14 10:30
Última actualización: 2026-01-14 14:45

> **"El análisis ES exhaustivo, sistemático y exacto"**

## METADATA (para retomar si se compacta la conversación)
- **Estado:** [FASE_1 | FASE_2 | FASE_3 | FASE_4 | EJECUTANDO]
- **Checkpoint actual:** [0 | 1 | 2 | 3 | 4]
- **Scope:** [proyecto completo | módulo: /path/to/module]
- **Lenguaje:** [godot | python | web]
- **Tarea actual:** [descripción de lo que se estaba haciendo]
- **Siguiente paso:** [descripción del próximo paso]

---

## 1. INVENTARIO DE ARCHIVOS (CHECKPOINT 1)

| # | Archivo | Líneas | Clases | Funciones | Nivel actual | Nivel correcto | Estado |
|---|---------|--------|--------|-----------|--------------|----------------|--------|
| 1 | src/auth.gd | 245 | 2 | 12 | ninguno | contenedor | ⚠️ |
| 2 | src/ui/login.gd | 89 | 1 | 5 | ninguno | pantalla | ⚠️ |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Total:** X archivos, Y líneas de código

---

## 2. MAPA DE FUNCIONALIDADES (CHECKPOINT 2)

### Funcionalidad 1: [Nombre]
**Descripción:** [Qué hace]
**Archivos involucrados:**
- `archivo1.gd:45-120` - [responsabilidad específica]
- `archivo2.gd:1-200` - [responsabilidad específica]

### Funcionalidad 2: [Nombre]
...

---

## 3. ANÁLISIS POR NIVELES (CHECKPOINT 3)

### ESTRUCTURA (nivel 5)
| Archivo | Estado | Problema | Acción requerida |
|---------|--------|----------|------------------|
| main.tscn | ✅ | - | Ninguna |

### PANTALLAS (nivel 4)
| Archivo | Estado | Problema | Acción requerida |
|---------|--------|----------|------------------|
| screens/login_screen.gd | ✅ | - | Ninguna |
| screens/dashboard.gd | ⚠️ | Contiene lógica de negocio | Extraer a contenedor |

### CONTENEDORES (nivel 3)
...

### COMPONENTES (nivel 2)
...

### PIEZAS (nivel 1)
...

---

## 4. PROBLEMAS DETECTADOS

### Críticos (bloquean refactorización)
1. **[archivo:línea]** - [descripción del problema]

### Importantes (deben resolverse)
1. **[archivo:línea]** - [descripción del problema]

### Menores (mejoras opcionales)
1. **[archivo:línea]** - [descripción del problema]

---

## 5. PLAN DE REFACTORIZACIÓN (CHECKPOINT 4)

### FASE 1: PIEZAS (crear base sólida)
| # | Tarea | Archivo origen | Archivo destino | Test de verificación | Estado |
|---|-------|----------------|-----------------|----------------------|--------|
| 1.1 | Extraer X | src/big.gd:45-60 | pieces/x_piece.gd | [cómo verificar] | ⬜ |
| 1.2 | Extraer Y | src/big.gd:61-80 | pieces/y_piece.gd | [cómo verificar] | ⬜ |

### FASE 2: COMPONENTES
| # | Tarea | Archivo origen | Archivo destino | Test de verificación | Estado |
|---|-------|----------------|-----------------|----------------------|--------|
| 2.1 | Crear Z | pieces/x + y | components/z_component.gd | [cómo verificar] | ⬜ |

### FASE 3: CONTENEDORES
...

### FASE 4: PANTALLAS
...

---

## 6. REGISTRO DE PROGRESO

| Fecha | Hora | Checkpoint | Acción | Resultado |
|-------|------|------------|--------|-----------|
| 2026-01-14 | 10:30 | 0 | Inicio análisis | OK |
| 2026-01-14 | 10:45 | 1 | Inventario completo | 47 archivos |
| 2026-01-14 | 11:00 | 2 | Mapa funcionalidades | 12 funcionalidades |
| ... | ... | ... | ... | ... |

---

## 7. NOTAS Y DECISIONES

### Decisiones tomadas
- [fecha] - [decisión y justificación]

### Pendientes por clarificar
- [ ] [pregunta o duda]

---

## INSTRUCCIONES PARA RETOMAR

Si la conversación se ha compactado, sigue estos pasos:

1. Lee este archivo completo
2. Identifica el **Estado** y **Checkpoint actual** en METADATA
3. Lee la **Tarea actual** y **Siguiente paso**
4. Continúa desde donde se quedó
5. Actualiza el archivo con el progreso

**IMPORTANTE:** No empieces de cero. Retoma exactamente donde se quedó.
```

---

## 6. HERRAMIENTAS A IMPLEMENTAR

### 6.1 `philosophy_architecture_analysis`
**Propósito:** Iniciar análisis arquitectónico global
**Parámetros:**
- `project_path` (string, requerido): Ruta del proyecto/módulo
- `language` (enum, requerido): godot | python | web | other
- `scope` (enum, opcional): full | structure_only | functionality_map
- `output_format` (enum, opcional): plan | report | both

**Comportamiento:**
1. Crea archivo de documentación
2. Ejecuta FASE 0-4
3. Guarda checkpoints automáticamente
4. Retorna resumen y ubicación del archivo

### 6.2 `philosophy_architecture_resume`
**Propósito:** Retomar análisis después de compactación
**Parámetros:**
- `analysis_file` (string, requerido): Ruta al archivo .md de análisis

**Comportamiento:**
1. Lee el archivo de análisis
2. Parsea METADATA para saber estado actual
3. Retorna resumen de dónde retomar
4. Continúa desde el checkpoint

### 6.3 `philosophy_architecture_checkpoint`
**Propósito:** Guardar checkpoint manualmente
**Parámetros:**
- `analysis_file` (string, requerido): Ruta al archivo
- `checkpoint` (int, requerido): Número de checkpoint
- `notes` (string, opcional): Notas adicionales

### 6.4 `philosophy_architecture_execute`
**Propósito:** Ejecutar una tarea del plan
**Parámetros:**
- `analysis_file` (string, requerido): Ruta al archivo
- `task_id` (string, requerido): ID de la tarea (ej: "1.1", "2.3")

**Comportamiento:**
1. Lee la tarea del plan
2. Ejecuta el flujo q1→q7 para esa tarea específica
3. Ejecuta el test de verificación
4. Actualiza el estado en el archivo

---

## 7. INTEGRACIÓN CON FLUJO EXISTENTE

El análisis arquitectónico **NO reemplaza** el flujo q1→q7, lo **complementa**:

```
                    ┌─────────────────────────┐
                    │ Análisis Arquitectónico │
                    │ (global, planificación) │
                    └───────────┬─────────────┘
                                │
                                │ genera plan con N tareas
                                │
                    ┌───────────▼─────────────┐
                    │   Para cada tarea:      │
                    │   q1 → q2 → q3 → q4 →   │
                    │   q5 → código → validate│
                    │   (flujo granular)      │
                    └─────────────────────────┘
```

---

## 8. PRÓXIMOS PASOS

1. ✅ Documentar diseño (este archivo)
2. ✅ Implementar `philosophy_architecture_analysis`
3. ✅ Implementar `philosophy_architecture_resume`
4. ✅ Implementar `philosophy_architecture_checkpoint`
5. ✅ Implementar `philosophy_architecture_status` (reemplaza execute)
6. ✅ Probar con proyecto real (2026-01-14)
7. ⬜ Documentar uso en CLAUDE.md

## 9. USO RÁPIDO

```
# Iniciar análisis de un proyecto
philosophy_architecture_analysis(
    project_path="/ruta/al/proyecto",
    language="godot",  # godot | python | web | other
    project_name="mi-proyecto"
)

# Ver estado actual (busca en memoria Y en disco)
philosophy_architecture_status(
    project_path="/ruta/al/proyecto"  # Opcional, mejora la búsqueda en disco
)

# Guardar checkpoint
philosophy_architecture_checkpoint(
    analysis_file="/ruta/.claude/architecture_analysis_xxx.md",
    checkpoint=1,
    phase="FASE_1",
    current_task="Descripción de lo completado",
    next_step="Descripción del siguiente paso",
    data="Contenido markdown del checkpoint"
)

# Retomar después de compactación
philosophy_architecture_resume(
    analysis_file="/ruta/.claude/architecture_analysis_xxx.md"
)
```

## 10. BÚSQUEDA DE ANÁLISIS EXISTENTES

`philosophy_architecture_status` busca análisis de dos formas:

1. **En memoria**: Si hay un análisis activo en la sesión actual
2. **En disco**: Busca recursivamente en todos los directorios `.claude/` del proyecto

### Comportamiento de búsqueda en disco

- Usa `rglob(".claude")` para encontrar todos los directorios `.claude` en cualquier nivel
- Busca archivos que coincidan con `architecture_analysis_*.md`
- Extrae metadata: estado, checkpoint, scope
- Ordena por fecha de modificación (más reciente primero)
- Muestra hasta 5 análisis encontrados

### Información mostrada

Para cada análisis encontrado:
- **Nombre**: Extraído del título del archivo
- **Archivo**: Ruta completa
- **Scope**: Directorio que se estaba analizando
- **Estado**: Fase actual y checkpoint
- **Fases**: Indicador visual de progreso (✅⬜⬜⬜)

---

> **"El análisis ES exhaustivo, sistemático y exacto"**
>
> **"Máximo impacto, menor esfuerzo — a largo plazo"**
