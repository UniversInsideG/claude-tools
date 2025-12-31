# Instrucciones para Claude Code - UniversInside

## Filosofía de Programación Obligatoria

SIEMPRE aplicar estos principios en todo el código que generes o modifiques:

### Arquitectura Modular Jerárquica
Construir desde lo pequeño hacia lo grande:
1. **Piezas** (atómicas) → 2. **Componentes** → 3. **Contenedores** → 4. **Estructura General**

### Principios Clave
- **DRY**: No repetir código. Cambiar en 1 lugar = actualiza todo
- **Herencia/Instancias**: Definir base, extender y reutilizar
- **Single Responsibility**: Cada pieza hace UNA cosa
- **Composición**: Combinar piezas pequeñas en estructuras mayores

### Reglas de Implementación
1. Antes de crear código nuevo, buscar si existe algo reutilizable
2. Si un código se usará más de 1 vez → convertirlo en componente/clase base
3. Preferir escenas heredadas (Godot) y clases base (Python/PHP)
4. Usar signals/eventos para comunicación desacoplada
5. Nombrar según nivel: `*_component`, `*_system`, etc.

### Por Tecnología

**Godot:**
- Componentes como nodos independientes (`HealthComponent`, `MovementComponent`)
- Escenas heredadas para entidades similares
- Autoloads para sistemas globales
- Signals para comunicación

**Python:**
- Clases base abstractas en `core/`
- Componentes reutilizables en `components/`
- Herencia y composición

**Web (HTML/CSS/JS/PHP):**
- Atomic Design: atoms → molecules → organisms → pages
- Componentes CSS reutilizables
- Módulos PHP independientes

---

**Documentación completa:** `.claude/CODING_PHILOSOPHY.md`

> "Máximo impacto, menor esfuerzo — a largo plazo"
