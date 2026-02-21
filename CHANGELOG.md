# Changelog - Philosophy MCP

Historial de cambios del MCP de Filosofía de Programación UniversInside.

---

## [Web 1.0.1] - 2026-02-13

### Añadido
- **Instaladores para web-philosophy-mcp**: Scripts de instalación para tres contextos.
  - Funcionalidad: Cualquier persona puede instalar web-philosophy con un solo script. En Mac/Linux elige destino (Claude Code terminal+VS Code, Claude Desktop, o ambos). En Windows ejecuta INSTALAR.bat. Si ya tiene philosophy instalado, no se borra.
  - Técnico: `install.sh` (Mac/Linux con menú y manipulación JSON vía Python), `install-windows.ps1` (Windows con preservación de servidores existentes vía ConvertFrom-Json), `update-windows.ps1` (actualizador), wrappers `.bat`.
- **Referencia cruzada en instaladores philosophy-mcp**: Los instaladores de philosophy-mcp ahora mencionan la existencia de web-philosophy al final.

### Archivos creados
- `web-philosophy-mcp/install.sh`
- `web-philosophy-mcp/install-windows.ps1`
- `web-philosophy-mcp/update-windows.ps1`
- `web-philosophy-mcp/INSTALAR.bat`
- `web-philosophy-mcp/ACTUALIZAR.bat`

### Archivos modificados
- `philosophy-mcp/install-windows.ps1` — mensaje informativo sobre web-philosophy
- `philosophy-mcp/update-windows.ps1` — mensaje informativo sobre web-philosophy

---

## [Web 1.0.0] - 2026-02-13

### Añadido
- **Nuevo MCP Server `web-philosophy`**: Servidor independiente que aplica la misma filosofía de programación modular pero adaptado a desarrollo web (HTML, CSS, JS vanilla).
  - Funcionalidad: Los proyectos web tienen ahora el mismo nivel de validación arquitectónica que los proyectos Godot. Claude sigue los 10 pasos obligatorios (q0-q9) verificando que el código web cumpla Atomic Design, DRY visual, semántica HTML y buenas prácticas CSS/JS.
  - Técnico: Servidor Python independiente en `web-philosophy-mcp/server.py` (~4600 líneas). Misma infraestructura que `philosophy-mcp` (SESSION_STATE, ARCHITECTURE_STATE, decision_usuario dos pasos, plan_approved gate) con todas las validaciones adaptadas a web.

- **Arquitectura Atomic Design (5 niveles)**:
  - Atom → `atoms/` — Elemento básico indivisible (botón, input, label)
  - Molecule → `molecules/` — Combina átomos en grupo funcional (campo de formulario)
  - Organism → `organisms/` — Sección compleja, combina moléculas (header, formulario completo)
  - Template → `templates/` — Layout de página, distribución de organismos
  - Page → `pages/` — Instancia concreta de un template con datos reales

- **Validación CSS**: Colores hardcodeados sin variables CSS, `!important`, selectores con más de 3 niveles de anidación, bloques CSS duplicados
- **Validación HTML**: Estilos inline, div soup (5+ divs sin semántica), imágenes sin alt, DRY visual (estructuras HTML repetidas)
- **Validación JS**: Uso de `var` en lugar de `const/let`, queries DOM repetidas sin cachear
- **Detección de duplicación web**: Estilos inline repetidos, colores hardcodeados, `!important`, queries DOM duplicadas, estructuras HTML similares
- **Búsqueda adaptada**: Extensiones `.html`, `.css`, `.js` con exclusión de `node_modules/`, `dist/`, `build/`
- **Detección de funciones JS**: Declaraciones `function`, arrow functions, y `export` functions
- **Instalación independiente**: `claude mcp add web-philosophy -- python3 $(pwd)/server.py`

### Archivos creados
- `web-philosophy-mcp/server.py` — Servidor MCP completo adaptado a web
- `web-philosophy-mcp/requirements.txt` — Dependencia: `mcp`

---

## [2.5.0] - 2026-02-09

### Añadido
- **Gate `plan_approved` en ARCHITECTURE_STATE**: Flag que bloquea q1 cuando hay análisis arquitectónico con checkpoint >= 4 pero el usuario no aprobó el plan. Enforcement en código, no solo instrucciones textuales.
  - Funcionalidad: Claude ya no puede saltarse la presentación de resultados al usuario para ir directamente a implementar. Está obligado a presentar devolución completa y obtener aprobación.
  - Técnico: `plan_approved` se gestiona en `architecture_checkpoint` (FASE_4→false, EJECUTANDO→true) y en `architecture_resume` (infiere del estado guardado). `step1_responsabilidad` bloquea si flag es false.
- **Instrucciones checkpoint 4 con QUÉ/PARA QUÉ/POR QUÉ**: Reescritas las instrucciones de checkpoint 4 (en `architecture_checkpoint` y `architecture_resume`) exigiendo devolución funcional + técnica por cada tarea del plan.
  - Funcionalidad: El usuario recibe explicación de qué cambia para él (funcional) además de qué se modifica en el código (técnico), para poder tomar decisiones informadas.
  - Técnico: Las instrucciones explican QUÉ hacer (presentar devolución), PARA QUÉ (que el usuario pueda decidir), POR QUÉ (Claude 4.6 tiende a saltar a implementar sin presentar).
- **Instrucciones para guardar análisis ampliado**: Si el usuario pide más análisis después del checkpoint 4, las instrucciones indican guardarlo con `architecture_checkpoint` antes de presentar, para que persista si se compacta la conversación.

### Motivo
Claude 4.6 terminaba el análisis arquitectónico, no presentaba devolución funcional al usuario, y se ponía a implementar directamente. El usuario se quedaba sin información para tomar decisiones. El análisis ampliado que se hacía después del plan no se guardaba y se perdía al compactarse la conversación.

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

### Corregido
- **`decision_usuario` + `usuario_verifico` juntos**: Ya no devuelve "LLAMADA INVÁLIDA". Si ambos se envían con `justificacion_salto`, resuelve en un solo paso.
- **q0 gate `step_0_presented`**: Bloquea `confirmado_por_usuario=true` si no se presentaron criterios primero con `confirmado_por_usuario=false`. Impide que Claude salte la presentación de criterios al usuario.
- **`architecture_analysis` criterios en disco**: Nuevo parámetro `criterios_file` para especificar qué archivo de criterios usar de sesión anterior. Ya no bloquea sin crear el archivo de análisis.

### Añadido (post-release)
- **q9 `descripcion_funcional`**: Nuevo parámetro para documentar qué cambia para el usuario, no solo el cambio técnico. El template del CHANGELOG incluye ambas líneas (Funcionalidad + Técnico).
- **CLAUDE.md regla MCP al inicio**: La regla de usar `philosophy_q0_criterios` antes de Edit/Write se mueve al principio del archivo global y de `filosofia/CLAUDE.md`.

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
