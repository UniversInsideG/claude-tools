# Implementación MCP - Filosofía UniversInside

> Este documento define CÓMO el MCP implementa la filosofía.
> El documento base (`CODING_PHILOSOPHY.md`) es la guía y NO se modifica.

---

## 0. Instalación y Configuración

### Requisitos
- Python 3.10+
- Claude Code CLI
- Paquete MCP: `pip install mcp`

---

### Instalación en macOS/Linux

#### Paso 1: Copiar el servidor
```bash
cp -r philosophy-mcp /ruta/destino/
```

#### Paso 2: Instalar dependencias
```bash
pip install mcp
```

#### Paso 3: Configurar Claude Code

**Opción A: Global (recomendado)**
```bash
# Crear/editar ~/.claude/.mcp.json
```

```json
{
  "philosophy": {
    "command": "python3",
    "args": ["/ruta/completa/a/philosophy-mcp/server.py"]
  }
}
```

**Opción B: Por proyecto**
```bash
# Crear .mcp.json en la raíz del proyecto
```

---

### Instalación en Windows

#### Paso 1: Copiar el servidor
```powershell
# Copiar la carpeta philosophy-mcp a tu ubicación deseada
# Ejemplo: C:\Users\TuUsuario\claude-tools\philosophy-mcp
```

#### Paso 2: Instalar dependencias

```powershell
pip install mcp
```

**Si `pip` no funciona, probar estas alternativas:**

```powershell
# Opción 1: Usar py launcher
py -m pip install mcp

# Opción 2: Usar python -m
python -m pip install mcp

# Opción 3: Ruta completa (ajustar versión)
C:\Users\TuUsuario\AppData\Local\Programs\Python\Python311\Scripts\pip.exe install mcp
```

**Si ninguna funciona:**
1. Reinstalar Python desde https://www.python.org/downloads/
2. Marcar "Add Python to PATH" durante la instalación
3. Reiniciar la terminal

#### Paso 3: Configurar Claude Code

**Opción A: Global (recomendado)**

Crear archivo en: `C:\Users\TuUsuario\.claude\.mcp.json`

```json
{
  "philosophy": {
    "command": "python",
    "args": ["C:\\Users\\TuUsuario\\claude-tools\\philosophy-mcp\\server.py"]
  }
}
```

> **Nota Windows:** Usar `python` en lugar de `python3`, y rutas con `\\` o `/`

**Opción B: Por proyecto**

Crear `.mcp.json` en la raíz del proyecto con la misma estructura.

#### Paso 4: Verificar Python en PATH
```powershell
python --version
# Debe mostrar Python 3.10+
```

Si no funciona, añadir Python al PATH o usar ruta completa:
```json
{
  "philosophy": {
    "command": "C:\\Users\\TuUsuario\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
    "args": ["C:\\Users\\TuUsuario\\claude-tools\\philosophy-mcp\\server.py"]
  }
}
```

### Paso 4: Reiniciar Claude Code
Sal y vuelve a entrar a Claude Code para que cargue el MCP.

### Paso 5: Verificar instalación
```bash
# En Claude Code, ejecuta:
/mcp
```
Debería aparecer `philosophy` en la lista.

### Paso 6: Copiar el comando /filosofia (opcional)
```bash
# Para tenerlo disponible globalmente:
cp filosofia/commands/filosofia.md ~/.claude/commands/
```

### Paso 7: Configurar CLAUDE.md global (opcional)
Para que Claude aplique la filosofía automáticamente en todos los proyectos:

```bash
# Crear/editar ~/.claude/CLAUDE.md
```

```markdown
# Instrucciones Globales para Claude Code

## Filosofía de Programación

**OBLIGATORIO:** Antes de escribir cualquier código, usar el MCP `philosophy` si está disponible.

- Seguir los 7 pasos del flujo obligatorio
- Aplicar arquitectura de 5 niveles (Pieza → Componente → Contenedor → Pantalla → Estructura)
- Validar nomenclatura según el lenguaje
- Principio: "Máximo impacto, menor esfuerzo — a largo plazo"

Si el MCP no está disponible, aplicar mentalmente las 5 preguntas:
1. ¿Hace UNA sola cosa?
2. ¿Puedo reutilizar?
3. ¿Existe algo similar?
4. ¿Se actualizan las instancias si cambio la base?
5. ¿Nivel correcto?
```

---

## 1. Nomenclatura Clara (5 Niveles = Atomic Design)

La arquitectura sigue el mismo patrón que **Atomic Design** para web, adaptado a apps/juegos.

| Nivel | Nombre | Carpeta | Función | Web (Atomic Design) |
|-------|--------|---------|---------|---------------------|
| 1 | Pieza | `pieces/` | Atómica, hace UNA cosa | Atoms |
| 2 | Componente | `components/` | Combina piezas | Molecules |
| 3 | Contenedor | `systems/` | Lógica reutilizable, orquesta componentes | Organisms |
| 4 | Pantalla | `screens/` | Vista única del usuario, orquesta contenedores | Templates/Pages |
| 5 | Estructura | raíz | Proyecto completo | App |

### Por lenguaje

| Nivel | Godot | Python | Web |
|-------|-------|--------|-----|
| 1. Pieza | `pieces/*_piece.(gd\|tscn)` | `pieces/*.py` | `atoms/` |
| 2. Componente | `components/*_component.(gd\|tscn)` | `components/*.py` | `molecules/` |
| 3. Contenedor | `systems/*_system.(gd\|tscn)` | `systems/*.py` | `organisms/` |
| 4. Pantalla | `screens/*_screen.(gd\|tscn)` | `screens/*.py` | `templates/` |
| 5. Estructura | `main.tscn` | `main.py` | `app/` |

> **Nota Godot:** Cada nivel puede ser `.gd` (solo código), `.tscn` (solo visual), o ambos (visual + script adjunto). La extensión no determina el nivel, lo determina la **nomenclatura** (`*_piece`, `*_component`, etc.).

---

## 2. Determinar Nivel (sin nomenclatura previa)

Cuando el código no tiene nomenclatura o tiene una diferente:

### Por carpeta (si aplica)
Si está en `pieces/`, `components/`, `systems/`, `screens/` → ese es su nivel.

### Por análisis (flujo de decisión)

```
¿Hace UNA sola cosa atómica?
  └── Sí → PIEZA
  └── No → ¿Combina piezas para UNA función?
              └── Sí → COMPONENTE
              └── No → ¿Orquesta componentes?
                          └── Sí → CONTENEDOR
                          └── No → ¿Es una vista completa del usuario?
                                      └── Sí → PANTALLA
                                      └── No → ESTRUCTURA
```

### Criterios de identificación

| Criterio | Pieza | Componente | Contenedor | Pantalla |
|----------|-------|------------|------------|----------|
| Responsabilidad | UNA cosa | UNA función (varias piezas) | Lógica reutilizable | Vista única del usuario |
| Dependencias | Ninguna o mínimas | Usa piezas | Usa componentes | Usa contenedores |
| Reutilizable | Muy reutilizable | Reutilizable | Sí (en varias pantallas) | No (única para esa vista) |
| Enfoque | Qué hace | Qué combina | Qué lógica orquesta | Qué ve el usuario |
| Ejemplo | `health_bar.gd` | `player_stats.gd` | `combat_system.gd` | `battle_screen.tscn` |

### Contenedor vs Pantalla (distinción clave)

```
battle_screen.tscn (PANTALLA - vista única)
    ├── combat_system.gd (CONTENEDOR - reutilizable en otras pantallas)
    ├── inventory_system.gd (CONTENEDOR - reutilizable)
    └── ui_overlay_component (COMPONENTE)
```

| | Contenedor | Pantalla |
|-|------------|----------|
| **Es** | Función/lógica reutilizable | Vista única del usuario |
| **Orquesta** | Componentes para UNA lógica | Contenedores para UNA experiencia |
| **Puede usarse en** | Múltiples pantallas | Solo esa vista |
| **Ejemplo** | `combat_system` → battle, training, arena | `battle_screen` → solo batalla |

---

## 3. Arquitectura: 5 Niveles

```
ESTRUCTURA (proyecto completo: main.tscn)
    └── PANTALLA (vista única: screens/*_screen.tscn)
          └── CONTENEDOR (lógica reutilizable: systems/*_system.gd)
                └── COMPONENTE (combina piezas: components/*_component.gd)
                      └── PIEZA (atómica: pieces/*_piece.gd)
```

### Resumen por nivel

| Nivel | Qué es | Reutilizable | Ejemplo |
|-------|--------|--------------|---------|
| Pieza | UNA cosa atómica | Muy | `health_bar_piece.gd` |
| Componente | Combina piezas | Sí | `player_stats_component.gd` |
| Contenedor | Lógica que orquesta | Sí (en varias pantallas) | `combat_system.gd` |
| Pantalla | Vista única del usuario | No | `battle_screen.tscn` |
| Estructura | Proyecto completo | N/A | `main.tscn` |

---

## 4. Las 5 Preguntas (del documento base)

Antes de escribir código, responder:

1. ¿Esta pieza hace UNA sola cosa?
2. ¿Puedo reutilizar esto en otro lugar?
3. ¿Existe algo similar que pueda extender/heredar?
4. ¿Si cambio la base, se actualizarán todas las instancias?
5. ¿Está en el nivel correcto de la jerarquía?

---

## 5. IA + Código Trabajan Juntos (por paso)

| Paso | Pregunta | IA hace | Código hace | Cuándo código |
|------|----------|---------|-------------|---------------|
| 1 | ¿Hace UNA cosa? | Reflexiona, define responsabilidad | Detecta clases múltiples, funciones largas | Paso 7 |
| 2 | ¿Puedo reutilizar? | Reflexiona sobre diseño | Nada | - |
| 3 | ¿Existe similar? | Evalúa resultados | Busca nombre + contenido + patrón | Paso 3 |
| 4 | ¿Se actualizan instancias? | Define herencia correcta | Verifica extends, signals | Paso 7 |
| 5 | ¿Nivel correcto? | Justifica nivel | Valida nomenclatura | Paso 5 |
| 7 | Validar código | Evalúa resultado final | Code smells, duplicados | Paso 7 |

---

## 6. Validación: ANTES y DESPUÉS

### ANTES de escribir código (Pasos 1-5)

| Paso | IA | Código |
|------|-----|--------|
| 1 | Reflexiona responsabilidad | - |
| 2 | Reflexiona reutilización | - |
| 3 | Evalúa resultados | Busca similar |
| 4 | Define herencia | - |
| 5 | Justifica nivel | Valida nomenclatura |

### DESPUÉS de escribir código (Paso 7)

| Validación | Relacionado con |
|------------|-----------------|
| Múltiples clases, funciones largas | Pregunta 1 |
| Uso correcto de extends, signals | Pregunta 4 |
| Code smells por lenguaje | Principios generales |
| Código duplicado | Principio DRY |

---

## 7. Code Smells por Lenguaje

### Godot
- `AppTheme.style_*()` → Usar componentes existentes
- `Color()` hardcodeado → Usar AppTheme
- `get_node()` excesivo → Usar signals
- Múltiples clases en un archivo

### Python
- Funciones > 50 líneas
- Código duplicado
- Múltiples clases en un archivo

### Web
- Estilos inline (`style=""`)
- HTML duplicado
- Falta de componentización

---

## 8. Búsqueda Mejorada

`philosophy_q3_buscar` debe buscar:

1. **Por nombre de archivo** - Coincidencia en nombre
2. **Por contenido** - Buscar dentro del código
3. **Por patrón** - Expresiones regulares

---

## 9. Comportamiento ante Fallo

- **BLOQUEAR** si el diseño no es óptimo
- No permitir continuar si no aplica el principio central
- Principio: "Máximo impacto, menor esfuerzo a largo plazo"

### Qué bloquea:
- Nomenclatura incorrecta
- No responder las 5 preguntas
- Crear sin buscar similares primero
- Diseño que no es reutilizable

---

## 10. Migración de Código Existente

- El código existente debe migrarse a la nueva nomenclatura
- Aunque sea incómodo, es necesario para consistencia
- Considerar herramienta de migración automática

---

## 11. Flujo Forzado con Código: 7 Pasos

El orden se fuerza mediante **estado/tracking** en el MCP.
Cada herramienta requiere que la anterior esté completada.

```
philosophy_q1_responsabilidad   → Paso 1: ¿Hace UNA cosa?
         ↓ (requiere q1)
philosophy_q2_reutilizacion     → Paso 2: ¿Puedo reutilizar?
         ↓ (requiere q2)
philosophy_q3_buscar            → Paso 3: ¿Existe similar?
         ↓ (requiere q3)
philosophy_q4_herencia          → Paso 4: ¿Se actualizan instancias?
         ↓ (requiere q4)
philosophy_q5_nivel             → Paso 5: ¿Nivel correcto?
         ↓ (requiere q5)
[Escribir código]               → Paso 6
         ↓
philosophy_validate             → Paso 7: Validar código
```

Si se intenta saltar un paso, el MCP **bloquea** y muestra error.

---

## 12. Herramientas del MCP (6 herramientas)

### philosophy_q1_responsabilidad
- **Pregunta:** ¿Esta pieza hace UNA sola cosa?
- **IA hace:** Reflexiona y define la responsabilidad única
- **Código hace:** Nada (valida después en paso 7)
- **Requiere:** Nada (es el primer paso)
- **Marca:** step_1 = true

### philosophy_q2_reutilizacion
- **Pregunta:** ¿Puedo reutilizar esto en otro lugar?
- **IA hace:** Reflexiona sobre el diseño reutilizable
- **Código hace:** Nada
- **Requiere:** step_1 completado
- **Marca:** step_2 = true

### philosophy_q3_buscar
- **Pregunta:** ¿Existe algo similar que pueda extender/heredar?
- **IA hace:** Evalúa resultados de búsqueda
- **Código hace:** Busca por nombre + contenido + patrón
- **Requiere:** step_2 completado
- **Marca:** step_3 = true

### philosophy_q4_herencia
- **Pregunta:** ¿Si cambio la base, se actualizarán todas las instancias?
- **IA hace:** Entiende y define la herencia correcta
- **Código hace:** Nada (valida extends/signals después en paso 7)
- **Requiere:** step_3 completado
- **Marca:** step_4 = true

### philosophy_q5_nivel
- **Pregunta:** ¿Está en el nivel correcto de la jerarquía?
- **IA hace:** Justifica elección de nivel (pieza/componente/contenedor/pantalla/estructura)
- **Código hace:** Valida nomenclatura vs nivel declarado
- **Requiere:** step_4 completado
- **Marca:** step_5 = true
- **Bloquea si:** Nomenclatura no coincide con nivel

**Niveles válidos (5):**
- `pieza` → `pieces/*_piece.(gd|tscn)`
- `componente` → `components/*_component.(gd|tscn)`
- `contenedor` → `systems/*_system.(gd|tscn)`
- `pantalla` → `screens/*_screen.(gd|tscn)`
- `estructura` → `main.tscn`

### philosophy_validate
- **Paso:** Validación final del código escrito
- **IA hace:** Evalúa resultado final
- **Código hace:**
  - Detecta code smells por lenguaje
  - Detecta código duplicado
  - Valida Q1: múltiples clases, funciones largas
  - Valida Q4: uso correcto de extends, signals
- **Requiere:** step_5 completado + código escrito
- **Bloquea si:** No cumple principios

### philosophy_checklist (auxiliar)
- Muestra las 5 preguntas
- Muestra arquitectura de 5 niveles
- Referencia rápida
- No requiere estado, se puede usar en cualquier momento

---

## Principio Central

> "Máximo impacto, menor esfuerzo — a largo plazo"

Todo lo que hace el MCP debe servir a este principio.

---

*Documento de implementación para el MCP - UniversInside*
