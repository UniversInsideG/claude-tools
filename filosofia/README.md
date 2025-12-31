# Filosofía de Programación - UniversInside

Sistema de validación automática para Claude Code que asegura el cumplimiento de la arquitectura modular.

## Instalación

### Requisitos
- Claude Code instalado
- Python 3.x

### Pasos

1. **Clonar o copiar** esta carpeta a tu dispositivo

2. **Ejecutar el instalador**:
   ```bash
   cd filosofia
   ./install.sh
   ```

3. **Seguir las instrucciones**:
   - Te preguntará dónde está tu carpeta de proyectos
   - Por defecto: `~/Documents/GitHub`

4. **Abrir un nuevo terminal** de Claude Code

### Instalación manual (alternativa)

Si prefieres instalar manualmente:

```bash
# Definir tu carpeta de proyectos
WORK_DIR="$HOME/Documents/GitHub"

# Crear directorios
mkdir -p "$WORK_DIR/.claude/commands"
mkdir -p "$WORK_DIR/.claude/hooks"

# Copiar archivos
cp CLAUDE.md "$WORK_DIR/"
cp CODING_PHILOSOPHY.md "$WORK_DIR/.claude/"
cp commands/filosofia.md "$WORK_DIR/.claude/commands/"
cp hooks/*.py "$WORK_DIR/.claude/hooks/"
chmod +x "$WORK_DIR/.claude/hooks/"*.py

# Copiar configuración (o agregar manualmente a tu settings.local.json)
cp settings.local.json "$WORK_DIR/.claude/"
```

## Archivos instalados

```
Tu carpeta de proyectos/
├── CLAUDE.md                        # Instrucciones automáticas
└── .claude/
    ├── settings.local.json          # Configuración de hooks
    ├── CODING_PHILOSOPHY.md         # Documentación completa
    ├── commands/
    │   └── filosofia.md             # Comando /filosofia
    └── hooks/
        ├── planning_reminder.py     # Capa 1: Planificación
        └── validate_philosophy.py   # Capa 2: Validación
```

## Cómo funciona

### Capa 1: Planificación (planning_reminder.py)
- Se ejecuta cuando envías un mensaje
- Detecta si vas a pedir código
- Inyecta recordatorio de la filosofía
- Claude DEBE explicar su razonamiento antes de escribir

### Capa 2: Validación (validate_philosophy.py)
- Se ejecuta antes de Edit/Write y herramientas MCP Godot
- Valida el código contra los principios:
  - Single Responsibility
  - DRY (No repetir código)
  - Nomenclatura estándar
  - Nivel jerárquico correcto

## Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `/filosofia` | Ver resumen de principios |
| `/filosofia check` | Checklist antes de programar |
| `/filosofia revisar archivo.gd` | Analizar un archivo |
| `/filosofia aplicar [descripción]` | Diseñar estructura para algo nuevo |
| `/filosofia doc` | Ver documentación completa |

## Verificar instalación

1. Abre un **nuevo terminal** de Claude Code
2. Escribe `/hooks` - Deberías ver los hooks registrados
3. Escribe `/filosofia` - Deberías ver el resumen

## Desinstalar

Para desactivar los hooks, edita `.claude/settings.local.json` y elimina la sección `"hooks"`.

## Solución de problemas

### Los hooks no funcionan
- ¿Abriste un nuevo terminal después de instalar?
- Verifica con `/hooks` que estén registrados

### Error de Python
- Verifica que Python 3 esté instalado: `python3 --version`
- Los scripts deben ser ejecutables: `chmod +x .claude/hooks/*.py`

### El comando /filosofia no aparece
- Verifica que existe `.claude/commands/filosofia.md`
- Abre un nuevo terminal

---

> **"Máximo impacto, menor esfuerzo — a largo plazo"**

*UniversInside*
