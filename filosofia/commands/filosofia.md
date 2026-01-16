---
description: Activa la filosofía de programación modular usando MCP (9 pasos)
---

INSTRUCCIÓN OBLIGATORIA: Antes de escribir cualquier código, DEBES seguir los 9 pasos usando las herramientas del MCP philosophy. El MCP bloquea si saltas pasos.

> **"Verificar ANTES de escribir, no DESPUÉS de fallar"**
> **"Documentar DESPUÉS de validar"**

## FLUJO OBLIGATORIO (9 PASOS):

### PASO 1: `philosophy_q1_responsabilidad`
Pregunta: ¿Esta pieza hace UNA sola cosa?
- Describe lo que vas a crear
- Define la responsabilidad única
- Indica el lenguaje (godot/python/web)
- Indica el tipo de cambio (nuevo/modificacion/bugfix/refactor)

### PASO 2: `philosophy_q2_reutilizacion`
Pregunta: ¿Puedo reutilizar esto en otro lugar?
- ¿Es reutilizable?
- ¿Dónde podría reutilizarse?
- Justifica

### PASO 3: `philosophy_q3_buscar`
Pregunta: ¿Existe algo similar que pueda extender/heredar?
- Busca en código fuente Y documentación (.claude/, docs/)
- **PRIORIDAD:** Si hay documentación relevante, léela ANTES de crear código
- Evalúa los resultados
- Decide: reutilizar, extender o crear nuevo

### PASO 4: `philosophy_q4_herencia`
Pregunta: ¿Si cambio la base, se actualizarán las instancias?
- Define de qué hereda
- Qué componentes existentes reutiliza
- Justifica la herencia

### PASO 5: `philosophy_q5_nivel`
Pregunta: ¿Está en el nivel correcto de la jerarquía?
- Nivel: pieza/componente/contenedor/pantalla/estructura
- Nombre de archivo (nomenclatura correcta)
- Justifica el nivel

### PASO 6: `philosophy_q6_verificar_dependencias`
Pregunta: ¿Las dependencias externas existen y coinciden?
- Lista TODAS las funciones externas que vas a llamar
- El MCP verifica: archivo existe, función existe, firma coincide
- Si hay discrepancias, NO puedes continuar

### PASO 7: Escribir código
Siguiendo el diseño de los pasos anteriores y usando las firmas verificadas

### PASO 8: `philosophy_validate`
Valida el código escrito

### PASO 9: Documentar cambios
Después de validar, actualiza la documentación:
- **CHANGELOG.md**: Registra qué se hizo y por qué
- **Ubicación**: `docs/CHANGELOG.md` del proyecto
- **Formato**: Fecha, categoría, descripción, **qué reemplaza**

```markdown
## [FECHA] - Título breve

### Añadido/Corregido/Cambiado
- **Componente**: Descripción del cambio
- **Motivo**: Por qué se hizo

### Reemplaza/Obsoleta (si aplica)
- `archivo_viejo.gd` → `archivo_nuevo.gd`
- Documentación anterior: `docs/PLAN_VIEJO.md`
```

> Si el cambio es trivial (typo, formato), la documentación es opcional.
> Si el cambio reemplaza algo, **SIEMPRE documentar qué queda obsoleto**.

## ARQUITECTURA (5 NIVELES = Atomic Design):
```
ESTRUCTURA (main.tscn)
    └── PANTALLA (vista única: screens/*_screen)
          └── CONTENEDOR (lógica reutilizable: systems/*_system)
                └── COMPONENTE (combina piezas: components/*_component)
                      └── PIEZA (atómica: pieces/*_piece)
```

**Contenedor vs Pantalla:**
- Contenedor = lógica reutilizable en varias pantallas
- Pantalla = vista única del usuario (no reutilizable)

## NOMENCLATURA (Godot):
- 1. Pieza: `pieces/*_piece.(gd|tscn)`
- 2. Componente: `components/*_component.(gd|tscn)`
- 3. Contenedor: `systems/*_system.(gd|tscn)`
- 4. Pantalla: `screens/*_screen.(gd|tscn)`
- 5. Estructura: `main.tscn`

> La extensión no determina el nivel, lo determina la nomenclatura.

## TAREA DEL USUARIO:
$ARGUMENTS

## EMPIEZA AHORA:
Usa `philosophy_q1_responsabilidad` para comenzar el paso 1.

**Flujo completo:** q1 → q2 → q3 → q4 → q5 → q6 → código → validate → **documentar**
