# Filosofía de Programación - UniversInside

## Principio Central
> **"Máximo impacto, menor esfuerzo — a largo plazo"**

Esto significa invertir tiempo inicial en estructura para ganar velocidad y estabilidad en el futuro.

---

## 1. Arquitectura Modular Jerárquica

### Concepto
Construir desde la **pieza más pequeña** hacia la **estructura general**, como bloques de construcción.

```
┌─────────────────────────────────────┐
│           ESTRUCTURA GENERAL        │  ← Nivel 4: Aplicación/Proyecto
│  ┌───────────────────────────────┐  │
│  │         CONTENEDORES          │  │  ← Nivel 3: Módulos/Sistemas
│  │  ┌─────────────────────────┐  │  │
│  │  │      COMPONENTES        │  │  │  ← Nivel 2: Componentes compuestos
│  │  │  ┌───────┐ ┌───────┐   │  │  │
│  │  │  │ PIEZA │ │ PIEZA │   │  │  │  ← Nivel 1: Piezas atómicas
│  │  │  └───────┘ └───────┘   │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Regla de oro
- **Nivel 1 (Piezas)**: Hacen UNA sola cosa. Son la unidad mínima.
- **Nivel 2 (Componentes)**: Combinan piezas para funcionalidad específica.
- **Nivel 3 (Contenedores)**: Agrupan componentes relacionados.
- **Nivel 4 (Estructura)**: El proyecto completo.

---

## 2. Principios Fundamentales

### 2.1 DRY (Don't Repeat Yourself)
**"Cambias en un lugar → cambia en todos los relacionados"**

```
❌ MALO:
- Código copiado en 5 archivos
- Hay que cambiar 5 archivos si algo cambia

✅ BUENO:
- Código en 1 lugar (clase base, componente, función)
- Cambias 1 vez, se actualiza todo
```

### 2.2 Herencia e Instancias
**"Define una vez, usa muchas veces"**

- **Clase/Escena Base**: Define el comportamiento común
- **Herencia**: Extiende y especializa
- **Instancias**: Copias que heredan de la base

### 2.3 SOLID (Simplificado)

| Principio | Significado Práctico |
|-----------|---------------------|
| **S** - Single Responsibility | Cada archivo/clase/nodo hace UNA cosa |
| **O** - Open/Closed | Extender sin modificar el original |
| **L** - Liskov | Las clases hijas funcionan donde funciona la padre |
| **I** - Interface Segregation | Interfaces pequeñas y específicas |
| **D** - Dependency Inversion | Depender de abstracciones, no de implementaciones |

### 2.4 Composición sobre Herencia
Cuando sea posible, **combinar piezas** en lugar de crear largas cadenas de herencia.

---

## 3. Aplicación por Tecnología

### 3.1 Godot (GDScript)

#### Estructura de Carpetas
```
Game (Estructura General)
├── systems/ (Contenedores - orquestan)
│   ├── audio_system.gd
│   ├── save_system.gd
│   └── ui_system.gd
├── components/ (Componentes - combinan piezas)
│   ├── player_component.gd
│   ├── enemy_component.gd
│   └── npc_component.gd
└── pieces/ (Piezas - atómicas)
    ├── health_piece.gd
    ├── movement_piece.gd
    └── interaction_piece.gd
```

#### Patrones Clave en Godot
1. **Escenas Heredadas**: `enemy.tscn` hereda de `entity.tscn`
2. **Componentes como Nodos**: Agregar `HealthComponent` a cualquier entidad
3. **Signals**: Comunicación desacoplada entre nodos
4. **Autoloads**: Singletons para sistemas globales (GameManager, EventBus)

#### Ejemplo de Pieza Reutilizable
```gdscript
# pieces/health_piece.gd
class_name HealthPiece
extends Node

signal died
signal health_changed(new_health, max_health)

@export var max_health: int = 100
var current_health: int

func _ready():
    current_health = max_health

func take_damage(amount: int):
    current_health = max(0, current_health - amount)
    health_changed.emit(current_health, max_health)
    if current_health <= 0:
        died.emit()

func heal(amount: int):
    current_health = min(max_health, current_health + amount)
    health_changed.emit(current_health, max_health)
```

### 3.2 Python

#### Estructura de Proyecto
```
proyecto/
├── core/           # Piezas fundamentales
│   ├── base.py     # Clases base abstractas
│   └── utils.py    # Utilidades comunes
├── components/     # Componentes reutilizables
├── modules/        # Contenedores de funcionalidad
└── main.py         # Estructura general
```

#### Ejemplo
```python
# core/base.py
from abc import ABC, abstractmethod

class Entity(ABC):
    """Clase base para todas las entidades"""

    @abstractmethod
    def update(self):
        pass

# components/health.py
class HealthComponent:
    """Componente reutilizable de salud"""

    def __init__(self, max_health: int = 100):
        self.max_health = max_health
        self.current = max_health

    def damage(self, amount: int) -> bool:
        self.current = max(0, self.current - amount)
        return self.current <= 0  # True si murió
```

### 3.3 Web (HTML/CSS/JS/PHP)

#### Atomic Design
```
ui/
├── atoms/          # Botones, inputs, labels (Piezas)
├── molecules/      # Formularios simples, cards (Componentes)
├── organisms/      # Headers, sidebars (Contenedores)
├── templates/      # Layouts de página
└── pages/          # Páginas completas (Estructura)
```

#### PHP - Estructura MVC Modular
```
app/
├── Core/           # Framework base
│   ├── Model.php
│   ├── View.php
│   └── Controller.php
├── Components/     # Componentes reutilizables
├── Modules/        # Funcionalidades específicas
│   ├── Auth/
│   ├── Users/
│   └── Products/
└── public/
    └── index.php
```

---

## 4. Checklist de Implementación

Antes de escribir código, preguntarse:

- [ ] ¿Esta pieza hace UNA sola cosa?
- [ ] ¿Puedo reutilizar esto en otro lugar?
- [ ] ¿Existe algo similar que pueda extender/heredar?
- [ ] ¿Si cambio la base, se actualizarán todas las instancias?
- [ ] ¿Está en el nivel correcto de la jerarquía?

---

## 5. Nomenclatura Estándar

| Nivel | Godot | Python | Web |
|-------|-------|--------|-----|
| Pieza | `pieces/*_piece.gd` | `pieces/*.py` | `atoms/` |
| Componente | `components/*_component.gd` | `components/*.py` | `molecules/` |
| Contenedor | `systems/*_system.gd` | `systems/*.py` | `organisms/` |
| Estructura | `main.tscn` | `main.py` | `pages/` |

---

## 6. Anti-patrones a Evitar

1. **God Object**: Una clase que hace todo
2. **Copy-Paste**: Código duplicado
3. **Herencia Profunda**: Más de 3 niveles de herencia
4. **Acoplamiento Fuerte**: Dependencias directas entre módulos no relacionados
5. **Magic Numbers**: Valores hardcodeados sin constantes

---

## Resumen Ejecutivo

```
FILOSOFÍA = Modular + Reutilizable + Jerárquico

BENEFICIOS:
✓ Cambias 1 vez → actualiza todo
✓ Código probado se reutiliza
✓ Fácil de mantener y escalar
✓ Mejoras iterativas estables

COSTO INICIAL:
- Más tiempo en diseño
- Más archivos pequeños

GANANCIA A LARGO PLAZO:
- Menos bugs
- Desarrollo más rápido
- Código predecible
```

---

*Documento de referencia para Claude Code - UniversInside*
