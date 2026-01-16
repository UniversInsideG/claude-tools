# Changelog - Philosophy MCP

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
