# Changelog - Philosophy MCP

Historial de cambios del MCP de Filosofía de Programación UniversInside.

---

## [2.4.0] - 2026-02-07

### Añadido
- **`decision_usuario` dos pasos**: Ahora saltar pasos requiere 2 llamadas separadas: 1) `decision_usuario=true` + `justificacion_salto` → registra y pide STOP, 2) `usuario_verifico=true` → verifica justificación previa y permite continuar. Impide que Claude salte pasos sin preguntar al usuario.
- **Helper `manejar_decision_usuario`**: Función centralizada que gestiona el proceso de dos pasos para las 7 herramientas (q2-q9)
- **Validate `.tscn`**: Rama de validación específica para archivos de escena Godot con checks DRY: SubResources duplicados, theme_overrides repetidos, colores hardcodeados
- **q3 ripgrep**: Búsqueda por nombre y contenido usa `rg` (ripgrep) vía subprocess. Fallback a Python rglob si `rg` no está disponible. Reduce tiempos de búsqueda de minutos a segundos en proyectos grandes.
- **q0 bloqueo en segunda llamada**: `confirmado_por_usuario=true` ahora re-verifica patrones de criterios de implementación. Si detecta criterios con código/debugging, devuelve error bloqueante pidiendo reformular.
- **Checkpoint 4 STOP hard**: Al completar las 4 fases de análisis arquitectónico, el MCP devuelve STOP obligatorio que exige presentar el plan al usuario con AskUserQuestion antes de implementar.
- **Parámetros nuevos en schemas**: `justificacion_salto` (string) y `usuario_verifico` (boolean) en todas las herramientas q2-q9
- **`decision_pendiente` en SESSION_STATE**: Dict para almacenar justificaciones pendientes de verificación del usuario

### Cambiado
- `generar_error_paso_saltado` ya no menciona `decision_usuario=true` como bypass directo
- Checkpoint 4 y `architecture_resume` usan instrucción de STOP con 3 opciones (implementar, ajustar, solo análisis)

---

## [2.1.0] - 2026-02-01

### Añadido
- **Criterios persistentes**: `q0_criterios` requiere `project_path` y guarda criterios en `.claude/criterios_{tarea}.md`
- **`criterios_file` en SESSION_STATE**: q0 guarda ruta del archivo para que `architecture_analysis` lo encuentre sin depender de nombres coincidentes
- **Listado de criterios en `architecture_analysis`**: en sesión nueva (retomar), lista archivos encontrados para que Claude identifique el correcto

### Cambiado
- `architecture_analysis` verifica criterios en dos niveles: sesión actual (`SESSION_STATE["step_0"]`) y disco (`criterios_*.md`)
- Eliminado fallback genérico que aceptaba criterios de cualquier tarea anterior

### Corregido
- q0 y architecture_analysis usaban nombres distintos para el archivo de criterios (tarea vs project_name) → nunca coincidían
- architecture_analysis se saltaba q0 si existía un archivo de criterios viejo de otra tarea
- `criterios_file` no definida en `architecture_analysis` cuando q0 se completó en sesión actual → error `name 'criterios_file' is not defined`
- Falso positivo DRY en validador: líneas `var x = funcion(...)` (llamadas a helpers) ya no se cuentan como duplicación
- **Scripts Windows actualizados a v2.1.0** (`install-windows.ps1`, `update-windows.ps1`):
  - Formato MCP corregido: `mcpServers` en lugar de formato plano
  - Hook Stop añadido (tipo prompt, detecta pregunta + ejecución en mismo turno)
  - Actualizador migra automáticamente `.mcp.json` de formato antiguo a `mcpServers`
  - 4 eventos de hooks (Stop, UserPromptSubmit, PreToolUse, PostToolUse)
  - Novedades y referencias actualizadas a 10 pasos

---

## [2.0.0] - 2026-01-31

### Añadido
- **Paso 0: `philosophy_q0_criterios`** — fase obligatoria de definición de criterios con el usuario antes del flujo de diseño
  - Primera llamada con `confirmado_por_usuario=false`: Claude presenta reformulación y criterios, recibe instrucción de PARAR y usar AskUserQuestion
  - Segunda llamada con `confirmado_por_usuario=true`: desbloquea q1 tras confirmación del usuario
  - **BLOQUEA q1** si no se completa — q1 devuelve error de paso saltado
  - Nuevo campo `step_0` en SESSION_STATE
- **Hook Stop** en `~/.claude/settings.json` — detecta cuando Claude pregunta al usuario pero ejecuta herramientas modificadoras en el mismo turno, y bloquea
- **Reglas de interacción en CLAUDE.md global** — proceso de 8 puntos con qué/para qué/por qué integrados: leer, reformular, identificar dudas, preguntar y PARAR, esperar, acordar criterios, construir sobre lo existente, usar MCP

### Cambiado
- Flujo de 9 pasos → **10 pasos** (q0 a q9) en toda la documentación
- `philosophy_q1_responsabilidad` ahora verifica `step_0` antes de ejecutarse
- Descripción de q1 actualizada: "Requiere: Paso 0 completado"
- **Estructura qué/para qué/por qué** aplicada en todos los archivos de instrucciones:
  - `filosofia/CLAUDE.md` — los 10 pasos del flujo
  - `filosofia/commands/filosofia.md` — sección "ANTES DE TODO" y flujo
  - `filosofia/commands/arquitectura.md` — sección "ANTES DE TODO", fases 1-4 y fase 5

### Motivo
Claude ejecutaba sin esperar respuesta del usuario, reescribía archivos desde cero en lugar de iterar, y pasaba el flujo de filosofía sin checkpoints colaborativos. La causa raíz: las instrucciones describían intención pero no imponían paradas mecánicas, y no existía fase de acuerdo de criterios.

### Archivos modificados
- `philosophy-mcp/server.py` — step_0, reset_state, Tool q0, call_tool handler, step0_criterios, gate en step1
- `filosofia/commands/filosofia.md` — "ANTES DE TODO" con q0, flujo de 10 pasos
- `filosofia/commands/arquitectura.md` — "ANTES DE TODO" con q0, fases 1-4 y fase 5 con qué/para qué/por qué
- `filosofia/CLAUDE.md` — flujo de 10 pasos con qué/para qué/por qué
- `CLAUDE.md` — flujo actualizado de 7 a 10 pasos

---

## [1.7.0] - 2026-01-24

### Añadido
- **Detección de duplicación REAL en q3** (`philosophy_q3_buscar`)
  - Enfoque híbrido: patrones sospechosos + comparación de similitud
  - Nueva función `calcular_similitud()` usando difflib.SequenceMatcher
  - Solo reporta duplicación si similitud entre archivos > 60%
  - NO detecta falsos positivos (_ready/_process son normales en Godot)
  - Niveles: alto (>80% similitud), medio (>60%), bajo
  - Muestra: "archivo1 ↔ archivo2 (75.3% similitud)"
  - **Instrucciones explícitas para Claude** cuando hay duplicación:
    - "🛑 PARA - NO CONTINUES SIN RESOLVER ESTO"
    - Obliga a ANALIZAR, EXPLICAR al usuario, y PREGUNTAR antes de q4
    - Prohíbe explícitamente "mover a utils" como solución (es parche, no arquitectura)
    - Claude debe usar AskUserQuestion para que el usuario decida

- **Validación de coherencia en q4** (`philosophy_q4_herencia`)
  - BLOQUEA si hay duplicación alta y el usuario elige `hereda_de: "ninguno"`
  - Fuerza elegir: crear clase base, heredar de existente, o refactorizar primero
  - Muestra advertencia si hay duplicación media y no hereda
  - **Opción D: Ignorar con razón válida** - requiere palabra clave "USUARIO:"
    - Solo permite ignorar si la justificación empieza con: USUARIO:, USER:, DECISIÓN_USUARIO:, IGNORAR:
    - Esto garantiza que el usuario realmente decidió ignorar, no Claude

- **Nuevo campo `duplication_detected`** en SESSION_STATE

### Corregido
- **Detección de funciones async en Python** (`philosophy_q6_verificar_dependencias`)
  - El patrón regex ahora detecta `async def nombre()` además de `def nombre()`
  - Antes fallaba silenciosamente al verificar funciones async

### Archivos modificados
- `philosophy-mcp/server.py`:
  - Nueva función `calcular_similitud()`
  - Nueva función `detectar_duplicacion()` con enfoque híbrido
  - Modificado `step3_buscar()` para detectar y mostrar duplicación real
  - Modificado `step4_herencia()` para validar coherencia
  - Corregido regex de Python en `step6_verificar_dependencias()`
  - Añadido `import difflib`

---

## [1.6.1] - 2026-01-24

### Corregido
- **Detección de funciones estáticas en Godot** (`philosophy_q6_verificar_dependencias`)
  - El patrón regex ahora detecta `static func nombre()` además de `func nombre()`
  - Afecta también a `extract_function_signatures()` en análisis arquitectónico

### Archivos modificados
- `philosophy-mcp/server.py` - patrón regex actualizado en líneas 1558 y 2104

---

## [1.3.0] - 2025-01-11

### Añadido
- **Nuevo parámetro `tipo_cambio`** en paso 1 (obligatorio)
  - Valores: `nuevo`, `modificacion`, `bugfix`, `refactor`
  - Cada tipo muestra contexto específico (ej: "¿El bug revela un problema estructural?")
- **Actualizador automático para Windows** (`ACTUALIZAR.bat`)
  - Actualiza comando `/filosofia`
  - Opción de cerrar Claude Code automáticamente
  - Verifica configuración MCP existente
- **Documentación de actualización** en README

### Cambiado
- **Regla explícita: SIEMPRE usar filosofía, sin excepciones**
  - Bug fixes, modificaciones, refactors → todos requieren flujo completo
  - Añadida tabla "Aplica a TODO" en CLAUDE.md, README, y comando /filosofia
  - Mensaje: "NUNCA racionalizar para saltarse el flujo"
- `philosophy_checklist` ahora muestra recordatorio de que aplica a todo
- README reorganizado con secciones de Instalación, Actualización y Reinicio manual

### Archivos modificados
- `server.py` - nuevo parámetro y estado `current_change_type`
- `CLAUDE.md` (global y local) - tabla de excepciones
- `filosofia/commands/filosofia.md` - tabla y nuevo parámetro
- `README.md` - documentación completa

---

## [1.2.0] - 2025-01-09

### Añadido
- **Instalador automático para Windows** (`INSTALAR.bat`)
  - Detecta Python automáticamente
  - Instala dependencias
  - Configura `.mcp.json` global
  - Instala comando `/filosofia`
- Instrucciones específicas para Windows en documentación
- Soluciones para problemas comunes de pip en Windows
- Ubicación recomendada para instalación

### Mejorado
- Documentación separada por sistema operativo (macOS/Linux y Windows)

---

## [1.1.0] - 2025-01-09

### Añadido
- **Arquitectura de 5 niveles** (equivalente a Atomic Design)
  - Pieza (Atoms)
  - Componente (Molecules)
  - Contenedor (Organisms)
  - Pantalla (Templates/Pages) ← NUEVO
  - Estructura (App)
- Distinción clara entre Contenedor (reutilizable) y Pantalla (única)
- Criterios para determinar nivel sin nomenclatura previa
- Soporte para `.gd` y `.tscn` en todos los niveles
- Instrucciones para configurar `~/.claude/CLAUDE.md` global
- Sección de instalación y configuración en documentación

### Cambiado
- Actualizado `server.py` con validación de 5 niveles
- Actualizado enum de niveles: añadido "pantalla"
- Actualizada nomenclatura: `screens/*_screen.(gd|tscn)`
- Renumeradas secciones del documento de implementación

---

## [1.0.0] - 2025-01-08

### Añadido
- **MCP Server con 6 herramientas + 1 auxiliar**
  - `philosophy_q1_responsabilidad` - ¿Hace UNA sola cosa?
  - `philosophy_q2_reutilizacion` - ¿Puedo reutilizar?
  - `philosophy_q3_buscar` - ¿Existe algo similar?
  - `philosophy_q4_herencia` - ¿Se actualizan las instancias?
  - `philosophy_q5_nivel` - ¿Nivel correcto?
  - `philosophy_validate` - Validar código escrito
  - `philosophy_checklist` - Referencia rápida (auxiliar)
- **Flujo obligatorio de 7 pasos** con bloqueo si se saltan
- **Estado de sesión** para tracking de pasos completados
- Validación de nomenclatura por lenguaje (Godot, Python, Web)
- Detección de code smells por lenguaje
- Búsqueda por nombre, contenido y patrón regex
- Comando `/filosofia` para activar el flujo

### Arquitectura inicial (4 niveles)
- Pieza → `pieces/*_piece.gd`
- Componente → `components/*_component.gd`
- Contenedor → `systems/*_system.gd`
- Estructura → `main.tscn`

---

## [0.1.0] - 2025-01-07

### Añadido
- Configuración inicial del proyecto
- Sistema de hooks (deprecado en favor de MCP)
- Documentación base de filosofía (`CODING_PHILOSOPHY.md`)

---

## Principio Central

> "Máximo impacto, menor esfuerzo — a largo plazo"

---

## Enlaces

- **Repositorio:** https://github.com/UniversInsideG/claude-tools
- **Documentación:** `philosophy-mcp/IMPLEMENTACION_MCP.md`
- **Filosofía base:** `filosofia/CODING_PHILOSOPHY.md`
