# Implementación MCP - Filosofía UniversInside

> Este documento define CÓMO el MCP implementa la filosofía.
> El documento base (`CODING_PHILOSOPHY.md`) es la guía y NO se modifica.

---

## 1. Nomenclatura Clara

| Nivel | Carpeta | Archivo | Función |
|-------|---------|---------|---------|
| Pieza | `pieces/` | `*_piece.gd` | Atómica, hace UNA cosa |
| Componente | `components/` | `*_component.gd` | Combina piezas |
| Contenedor | `systems/` | `*_system.gd` | Orquesta componentes |
| Estructura | raíz | `main.tscn` | Proyecto completo |

### Por lenguaje

| Nivel | Godot | Python | Web |
|-------|-------|--------|-----|
| Pieza | `pieces/*_piece.gd` | `pieces/*.py` | `atoms/` |
| Componente | `components/*_component.gd` | `components/*.py` | `molecules/` |
| Contenedor | `systems/*_system.gd` | `systems/*.py` | `organisms/` |
| Estructura | `main.tscn` | `main.py` | `pages/` |

---

## 2. Arquitectura: 4 Niveles

```
ESTRUCTURA (proyecto completo)
    └── CONTENEDOR (orquesta)
          └── COMPONENTE (combina)
                └── PIEZA (atómica)
```

- "Pantalla" NO es un nivel separado
- Una pantalla es un **componente** compuesto de otros componentes/piezas

---

## 3. Las 5 Preguntas (del documento base)

Antes de escribir código, responder:

1. ¿Esta pieza hace UNA sola cosa?
2. ¿Puedo reutilizar esto en otro lugar?
3. ¿Existe algo similar que pueda extender/heredar?
4. ¿Si cambio la base, se actualizarán todas las instancias?
5. ¿Está en el nivel correcto de la jerarquía?

---

## 4. IA + Código Trabajan Juntos (por paso)

| Paso | Pregunta | IA hace | Código hace | Cuándo código |
|------|----------|---------|-------------|---------------|
| 1 | ¿Hace UNA cosa? | Reflexiona, define responsabilidad | Detecta clases múltiples, funciones largas | Paso 7 |
| 2 | ¿Puedo reutilizar? | Reflexiona sobre diseño | Nada | - |
| 3 | ¿Existe similar? | Evalúa resultados | Busca nombre + contenido + patrón | Paso 3 |
| 4 | ¿Se actualizan instancias? | Define herencia correcta | Verifica extends, signals | Paso 7 |
| 5 | ¿Nivel correcto? | Justifica nivel | Valida nomenclatura | Paso 5 |
| 7 | Validar código | Evalúa resultado final | Code smells, duplicados | Paso 7 |

---

## 5. Validación: ANTES y DESPUÉS

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

## 6. Code Smells por Lenguaje

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

## 7. Búsqueda Mejorada

`philosophy_q3_buscar` debe buscar:

1. **Por nombre de archivo** - Coincidencia en nombre
2. **Por contenido** - Buscar dentro del código
3. **Por patrón** - Expresiones regulares

---

## 8. Comportamiento ante Fallo

- **BLOQUEAR** si el diseño no es óptimo
- No permitir continuar si no aplica el principio central
- Principio: "Máximo impacto, menor esfuerzo a largo plazo"

### Qué bloquea:
- Nomenclatura incorrecta
- No responder las 5 preguntas
- Crear sin buscar similares primero
- Diseño que no es reutilizable

---

## 9. Migración de Código Existente

- El código existente debe migrarse a la nueva nomenclatura
- Aunque sea incómodo, es necesario para consistencia
- Considerar herramienta de migración automática

---

## 10. Flujo Forzado con Código: 7 Pasos

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

## 11. Herramientas del MCP (6 herramientas)

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
- **IA hace:** Justifica elección de nivel (pieza/componente/contenedor/estructura)
- **Código hace:** Valida nomenclatura vs nivel declarado
- **Requiere:** step_4 completado
- **Marca:** step_5 = true
- **Bloquea si:** Nomenclatura no coincide con nivel

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
- Muestra arquitectura de 4 niveles
- Referencia rápida
- No requiere estado, se puede usar en cualquier momento

---

## Principio Central

> "Máximo impacto, menor esfuerzo — a largo plazo"

Todo lo que hace el MCP debe servir a este principio.

---

*Documento de implementación para el MCP - UniversInside*
