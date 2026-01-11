# Changelog - Philosophy MCP

Historial de cambios del MCP de Filosofía de Programación UniversInside.

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
