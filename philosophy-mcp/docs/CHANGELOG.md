# Changelog - Philosophy MCP

## [2026-01-26] - Parámetro decision_usuario para desbloquear pasos

### Añadido
- **`decision_usuario`**: Nuevo parámetro en todas las herramientas q2-q9
- Cuando el usuario toma una decisión consciente (aunque difiera del MCP), Claude puede llamar con `decision_usuario=true`
- El paso anterior se marca como completado y el flujo continúa
- El usuario asume la responsabilidad de su decisión

### Cambiado
- `generar_error_paso_saltado()` ahora indica cómo usar `decision_usuario=true`
- Validación de nomenclatura en q5 puede omitirse con `decision_usuario=true`

### Motivo
Cuando el MCP bloqueaba un paso, no había forma de desbloquear aunque el usuario tomara una decisión consciente. El usuario respondía pero el MCP seguía bloqueando porque no reconocía la respuesta.

### Flujo cuando el usuario decide continuar
1. MCP detecta paso saltado o validación fallida
2. Claude EXPLICA y PREGUNTA con AskUserQuestion
3. Usuario decide continuar (asumiendo responsabilidad)
4. Claude llama de nuevo con `decision_usuario=true`
5. MCP marca el paso como completado y continúa

---

## [2026-01-17] - Arquitectura completa activa /filosofia automáticamente

### Corregido
- Cuando `architecture_checkpoint` guarda checkpoint 4, muestra instrucción obligatoria de usar `/filosofia`
- Cuando `architecture_resume` retoma análisis con checkpoint >= 4, también muestra la instrucción
- Mensaje claro: "ANÁLISIS COMPLETO - AHORA IMPLEMENTAR CON /filosofia"

### Motivo
Claude terminaba el análisis arquitectónico y pasaba a implementar sin usar el flujo de filosofía.
Ahora el MCP le recuerda que CADA tarea del plan debe pasar por los 9 pasos.

---

## [2026-01-17] - CLAUDE.md reforzado con regla principal

### Añadido
- **REGLA PRINCIPAL** en CLAUDE.md: "SEGUIR INSTRUCCIONES DEL MCP"
- Instrucciones explícitas de cuándo usar AskUserQuestion
- Lista de PROHIBIDO para Claude
- Flujo actualizado a 9 pasos con philosophy_q9_documentar

### Motivo
Los MCPs solo devuelven texto, no pueden forzar comportamiento.
El CLAUDE.md refuerza que Claude DEBE seguir las instrucciones del MCP.

---

## [2026-01-17] - Análisis arquitectónico también obliga a preguntar

### Añadido
- **Instrucciones obligatorias** en `architecture_analysis`, `architecture_resume`, `architecture_checkpoint`
- Claude debe completar las 4 FASES o explicar por qué quiere abandonar
- Cada checkpoint muestra progreso de fases con checkboxes

### Motivo
Claude perdía el hilo del análisis arquitectónico y abandonaba sin completar las 4 fases.

---

## [2026-01-17] - Claude debe explicar POR QUÉ quiere saltar pasos

### Cambiado
- **TODOS los pasos** ahora obligan a Claude a:
  1. EXPLICAR su argumento de por qué quiere saltar el paso
  2. PREGUNTAR al usuario con AskUserQuestion
- **Warnings** también requieren que Claude explique su opinión sobre cada advertencia
- Nueva función `generar_error_paso_saltado()` con instrucciones de 2 pasos
- Nuevo parámetro `usuario_confirmo_warnings` para confirmar después de preguntar

### Motivo
Claude decidía por su cuenta saltarse pasos sin explicar por qué.
Ahora el usuario puede evaluar el argumento de Claude antes de decidir.

### Flujo cuando se salta un paso
1. MCP detecta paso saltado
2. Claude EXPLICA: "Intenté saltar porque [razón específica]"
3. Claude PREGUNTA con AskUserQuestion
4. Usuario decide con información completa

---

## [2026-01-16] - Herramienta philosophy_q9_documentar obligatoria

### Añadido
- **`philosophy_q9_documentar`**: Nueva herramienta obligatoria para el paso 9
- **Búsqueda automática** de docs afectados:
  - CHANGELOG.md para registrar el cambio
  - README.md si cambia funcionalidad pública
  - Otros docs en docs/ que mencionen los archivos modificados
- **Template de CHANGELOG** generado automáticamente con fecha, tipo y archivos
- **`step_8`** en SESSION_STATE para tracking de validación
- **Flujo ahora es 9 pasos obligatorios** con herramientas MCP (no manual)

### Cambiado
- `philosophy_validate` ya NO resetea estado - ahora marca `step_8 = True`
- `philosophy_validate` indica usar `philosophy_q9_documentar` (no documentación manual)
- `show_checklist` muestra `philosophy_q9_documentar` como paso 9 obligatorio
- Renombrada `step7_validate` → `step8_validate` internamente

### Motivo
El paso 9 de documentación existía pero era manual (solo un recordatorio).
Ahora es una herramienta MCP que:
1. Obliga a documentar (no puedes cerrar el flujo sin usarla)
2. Busca automáticamente qué docs actualizar
3. Genera templates listos para copiar

### Reemplaza
- Comportamiento anterior: `philosophy_validate` reseteaba estado y solo mostraba recordatorio

---

## [2026-01-16] - Sistema de jerarquización de documentación

### Añadido
- **Sistema de scoring** para documentación con múltiples factores:
  - **Tipo de documento**: GUIA (100) > ARQUITECTURA (90) > ANALISIS (85) > PLAN (70) > CHANGELOG (40)
  - **Antigüedad**: Esta semana (+40%) > Este mes (+20%) > 3 meses (0%) > 6 meses (-30%) > +6 meses (-60%)
  - **Estado**: activo (+20%) > en_progreso (+10%) > completado (-50% para planes) > obsoleto (-90%)
  - **Topic duplicado**: Si hay versión más reciente del mismo tema (-70%)
  - **Frecuencia del término**: Bonus por apariciones
  - **Título**: Bonus si el término aparece en título
- **Detección de topics**: Agrupa documentos del mismo tema para detectar versiones superseded
- **Separación primary/secondary**: Docs relevantes vs obsoletos/baja prioridad
- **Etiquetas visuales**: 🔥 ALTA, 📌 MEDIA, 📎 BAJA + indicadores de antigüedad

### Motivo
Documentación puede tener múltiples versiones (ej: análisis del 15 y 16 enero).
El sistema debe mostrar la más relevante primero y advertir sobre versiones anteriores.

### Ejemplo de output
```
📚 DOCUMENTACIÓN RELEVANTE (21 principales, 3 secundarios)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🔥 ALTA Guía de Desarrollo: Master/Observer
   📁 docs/GUIA_DESARROLLO_MASTER_OBSERVER.md
   GUIA | 🟢 Esta semana | Score: 179.0

2. 📌 MEDIA Análisis Arquitectónico: master_observer_refactor
   📁 scenes/menu/players/.claude/architecture_analysis_...
   ANALISIS | 🟢 Esta semana | Score: 155.9
   ⚠️ Hay versión más reciente (1 día después)
```

### Funciones añadidas
- `extract_doc_topic()`: Detecta el tema de un documento
- `extract_doc_metadata()`: Extrae fecha, estado, tipo
- `calculate_doc_relevance()`: Calcula score combinado
- `search_project_documentation()`: Retorna {primary, secondary, topics}

---

## [2026-01-16] - Añadido paso 9: Documentar con tracking de obsoletos

### Añadido
- **Paso 9**: Documentar cambios en CHANGELOG después de validar
- Nueva máxima: "Documentar DESPUÉS de validar"
- `philosophy_validate` recuerda documentar incluyendo **qué queda obsoleto**
- `philosophy_checklist` actualizado a 9 pasos
- Skill `/filosofia` actualizado con formato de documentación

### Formato recomendado
```markdown
## [FECHA] - Título

### Añadido/Corregido
- Qué se hizo y por qué

### Reemplaza/Obsoleta (si aplica)
- `viejo.gd` → `nuevo.gd`
- Doc anterior: `docs/PLAN_VIEJO.md`
```

### Motivo
La documentación debe ser parte del flujo y rastrear qué deja obsoleto cada cambio.

---

## [2026-01-16] - Mejoras en búsqueda de análisis y Q5

### Corregido

#### `philosophy_architecture_status`
- **Problema:** No encontraba análisis existentes en disco al iniciar nueva sesión
- **Causa:** Búsqueda solo profundizaba 2 niveles, pero archivos estaban más profundos
- **Solución:**
  - Añadido parámetro `project_path` a la definición del tool
  - Actualizado `call_tool` para pasar el parámetro
  - `find_analysis_files()` ahora usa `rglob(".claude")` para búsqueda recursiva
  - Añadido campo `scope` a la información extraída

#### `philosophy_q5_nivel`
- **Problema:** Bloqueaba archivos legacy que no seguían nomenclatura
- **Causa:** Validaba nombre antes que comportamiento
- **Solución:**
  - Prioriza validación de COMPORTAMIENTO (por palabras clave en justificación)
  - Nomenclatura es secundaria: advertencia/deuda técnica, no bloqueo
  - Para código NUEVO sí exige nomenclatura correcta
  - Nuevas funciones: `validar_comportamiento_nivel()`, `get_suggested_filename()`

### Documentación actualizada
- `docs/ARCHITECTURE_ANALYSIS_DESIGN.md` - Sección 9 y 10 sobre búsqueda en disco
- `docs/Q5_NIVEL_DESIGN.md` - Añadidos tests realizados

---

## [2026-01-15] - Paso Q6 verificar dependencias

### Añadido
- `philosophy_q6_verificar_dependencias` - Verifica dependencias externas ANTES de escribir código
- Flujo actualizado de 7 a 8 pasos

### Máxima
> "Verificar ANTES de escribir, no DESPUÉS de fallar"

---

## [2026-01-14] - Análisis arquitectónico global

### Añadido
- `philosophy_architecture_analysis` - Iniciar análisis global
- `philosophy_architecture_resume` - Retomar después de compactación
- `philosophy_architecture_checkpoint` - Guardar progreso
- `philosophy_architecture_status` - Ver estado actual

### Máxima
> "El análisis ES exhaustivo, sistemático y exacto"
