---
description: Activa la filosofía de programación modular usando MCP (7 pasos)
---

INSTRUCCIÓN OBLIGATORIA: Antes de escribir o modificar cualquier código, DEBES seguir los 7 pasos usando las herramientas del MCP philosophy. El MCP bloquea si saltas pasos.

## ⚠️ APLICA A TODO (SIN EXCEPCIONES):

| Tipo | ¿Usar flujo? | Por qué |
|------|--------------|---------|
| Código nuevo | ✅ SÍ | Diseño correcto desde inicio |
| Bug fix | ✅ SÍ | Un bug es señal de problema estructural |
| Modificación | ✅ SÍ | Verificar que no rompe arquitectura |
| Refactor | ✅ SÍ | Oportunidad de mejorar |

**NUNCA racionalizar para saltarse el flujo.** "Es solo un fix pequeño" es una excusa que acumula deuda técnica.

## FLUJO OBLIGATORIO (7 PASOS):

### PASO 1: `philosophy_q1_responsabilidad`
Pregunta: ¿Esta pieza hace UNA sola cosa?
- Describe lo que vas a crear/modificar
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
- Busca en el proyecto
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

### PASO 6: Escribir código
Siguiendo el diseño de los pasos anteriores

### PASO 7: `philosophy_validate`
Valida el código escrito

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
