---
description: Muestra la filosofía de programación modular de UniversInside
allowed-tools: Read
argument-hint: [check|revisar archivo|aplicar descripcion|doc]
---

Ejecuta la acción de filosofía de programación según el argumento: $ARGUMENTS

## Si no hay argumentos o es "resumen":
Muestra este resumen:

```
═══════════════════════════════════════════════════════════════
   FILOSOFÍA DE PROGRAMACIÓN - UniversInside
   "Máximo impacto, menor esfuerzo — a largo plazo"
═══════════════════════════════════════════════════════════════

ARQUITECTURA MODULAR JERÁRQUICA:
┌─────────────────────────────────────┐
│  4. ESTRUCTURA GENERAL (Proyecto)   │
│  ┌───────────────────────────────┐  │
│  │ 3. CONTENEDORES (Sistemas)    │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │ 2. COMPONENTES          │  │  │
│  │  │  ┌───────┐ ┌───────┐   │  │  │
│  │  │  │PIEZA 1│ │PIEZA 2│   │  │  │
│  │  │  └───────┘ └───────┘   │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘

PRINCIPIOS CLAVE:
• DRY → Cambiar en 1 lugar = actualiza todo
• Herencia → Definir base, extender, reutilizar
• Single Responsibility → Cada pieza hace UNA cosa
• Composición → Piezas pequeñas → estructuras grandes

TECNOLOGÍAS:
• GODOT:  Componentes como nodos + Escenas heredadas + Signals
• PYTHON: Clases base abstractas + Composición
• WEB:    Atomic Design (atoms → molecules → organisms → pages)
═══════════════════════════════════════════════════════════════
```

## Si el argumento es "check":
Muestra el checklist:

```
CHECKLIST - Antes de escribir código:

□ ¿Esta pieza hace UNA sola cosa?
□ ¿Puedo reutilizar esto en otro lugar?
□ ¿Existe algo similar que pueda extender/heredar?
□ ¿Si cambio la base, se actualizarán todas las instancias?
□ ¿Está en el nivel correcto? (Pieza/Componente/Contenedor/Estructura)
□ ¿Sigue la nomenclatura estándar?
```

Luego pregunta: "¿Qué vas a crear? Descríbelo y te ayudo a ubicarlo en la arquitectura correcta."

## Si el argumento empieza con "revisar" o "analizar":
Lee el archivo especificado y genera un reporte:
- ✅ Lo que cumple con la filosofía
- ⚠️ Lo que podría mejorar
- 🔧 Sugerencias de refactorización
- 📍 Nivel en la jerarquía (Pieza/Componente/Contenedor/Estructura)

## Si el argumento empieza con "aplicar":
Toma la descripción y:
1. Identifica en qué nivel de la jerarquía pertenece
2. Sugiere estructura de archivos
3. Propone nombres según nomenclatura
4. Ofrece crear el esqueleto del código

## Si el argumento es "doc":
Lee y muestra el contenido de `.claude/CODING_PHILOSOPHY.md`
