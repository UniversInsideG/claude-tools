# Claude Tools - UniversInside

Colección de herramientas, configuraciones y comandos personalizados para Claude Code.

## Herramientas disponibles

| Herramienta | Descripción | Comando |
|-------------|-------------|---------|
| **Filosofía de Programación** | Arquitectura modular, principios DRY/SOLID, plantillas | `/filosofia` |

## Instalación rápida

```bash
git clone https://github.com/TU_USUARIO/claude-tools.git
cd claude-tools/filosofia
./install.sh
```

## Estructura del repositorio

```
claude-tools/
├── README.md
├── filosofia/                    # Filosofía de programación modular
│   ├── CLAUDE.md                 # Instrucciones automáticas
│   ├── CODING_PHILOSOPHY.md      # Documentación completa
│   ├── commands/
│   │   └── filosofia.md          # Comando /filosofia
│   └── install.sh                # Instalador
└── [futuras herramientas]/
```

## Uso

Después de instalar:

- **Automático**: Claude Code carga las instrucciones al iniciar
- **Manual**: Usa `/filosofia` para ver principios y checklist

```bash
/filosofia           # Ver resumen
/filosofia check     # Checklist antes de programar
/filosofia doc       # Documentación completa
```

## Agregar nuevas herramientas

Cada herramienta tiene su propia carpeta con:
- `install.sh` - Instalador independiente
- Archivos de configuración necesarios

---

*UniversInside - "Máximo impacto, menor esfuerzo — a largo plazo"*
