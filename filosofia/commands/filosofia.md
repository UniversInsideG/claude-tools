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

### PASO 9: `philosophy_q9_documentar` (OBLIGATORIO)
Pregunta: ¿Está documentado el cambio?
- Usa la herramienta `philosophy_q9_documentar`
- Parámetros:
  - `project_path`: Ruta del proyecto
  - `archivos_modificados`: Lista de archivos creados/modificados
  - `descripcion_cambio`: Descripción breve del cambio
  - `tipo_cambio`: añadido/corregido/cambiado/eliminado
  - `reemplaza`: (opcional) Qué código/docs deja obsoleto

La herramienta busca automáticamente:
- **CHANGELOG.md**: Genera template con fecha y descripción
- **README.md**: Indica si necesita actualización (funcionalidad pública)
- **Otros docs**: Lista docs que mencionan los archivos modificados

> El flujo NO se cierra hasta usar esta herramienta.
> La documentación es OBLIGATORIA (excepto cambios triviales como typos).

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

**Flujo completo:** q1 → q2 → q3 → q4 → q5 → q6 → código → validate → **q9_documentar**
