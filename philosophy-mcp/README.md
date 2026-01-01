# Philosophy MCP Server - UniversInside

Servidor MCP que fuerza la filosofía de programación modular en Claude Code.

## Herramientas que provee

| Herramienta | Descripción | Uso |
|-------------|-------------|-----|
| `philosophy_analyze` | Analiza ANTES de escribir código | OBLIGATORIO |
| `philosophy_search_similar` | Busca componentes existentes | OBLIGATORIO |
| `philosophy_validate_code` | Valida código escrito | Recomendado |
| `philosophy_checklist` | Muestra el checklist completo | Referencia |

## Instalación

### 1. Instalar dependencias

```bash
cd philosophy-mcp
pip install -r requirements.txt
```

### 2. Registrar en Claude Code

```bash
claude mcp add philosophy -- python3 /ruta/completa/philosophy-mcp/server.py
```

**IMPORTANTE**: Usa la ruta absoluta completa.

Ejemplo:
```bash
claude mcp add philosophy -- python3 /Users/cecilia/Documents/GitHub/claude-tools/philosophy-mcp/server.py
```

### 3. Verificar

```bash
claude mcp list
```

Debe mostrar:
```
philosophy (local - stdio)
```

## Uso

Dentro de Claude Code, las herramientas estarán disponibles automáticamente.

### Flujo obligatorio:

1. **Buscar similar**: `philosophy_search_similar`
2. **Analizar**: `philosophy_analyze`
3. **Escribir código**
4. **Validar**: `philosophy_validate_code`

### Ejemplo de uso:

```
Usuario: "Crea un componente de salud para Godot"

Claude DEBE:
1. Usar philosophy_search_similar para buscar "health" en el proyecto
2. Usar philosophy_analyze para clasificar lo que va a crear
3. Solo entonces escribir el código
4. Opcionalmente usar philosophy_validate_code para validar
```

## Desinstalar

```bash
claude mcp remove philosophy
```

## Arquitectura

```
Nivel 4: ESTRUCTURA   → El proyecto completo
Nivel 3: CONTENEDOR   → Sistemas (*_system.gd, *_manager.gd)
Nivel 2: COMPONENTE   → Combinan piezas (*_component.gd)
Nivel 1: PIEZA        → Unidad mínima, hace UNA cosa
```

---

> "Máximo impacto, menor esfuerzo — a largo plazo"

*UniversInside*
