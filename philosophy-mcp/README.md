# Philosophy MCP Server - UniversInside

Servidor MCP que fuerza la filosofía de programación modular en Claude Code.

> **"Máximo impacto, menor esfuerzo — a largo plazo"**

## Herramientas (7 pasos obligatorios)

| Paso | Herramienta | Pregunta |
|------|-------------|----------|
| 1 | `philosophy_q1_responsabilidad` | ¿Hace UNA sola cosa? |
| 2 | `philosophy_q2_reutilizacion` | ¿Puedo reutilizar? |
| 3 | `philosophy_q3_buscar` | ¿Existe algo similar? |
| 4 | `philosophy_q4_herencia` | ¿Se actualizan las instancias? |
| 5 | `philosophy_q5_nivel` | ¿Nivel correcto? |
| 6 | *Escribir código* | - |
| 7 | `philosophy_validate` | Validar código |

**Auxiliar:** `philosophy_checklist` - Muestra referencia rápida

## Aplica a TODO (sin excepciones)

| Tipo de cambio | ¿Usar flujo? | Por qué |
|----------------|--------------|---------|
| Código nuevo | ✅ SÍ | Diseño correcto desde inicio |
| Bug fix | ✅ SÍ | Un bug es señal de problema estructural |
| Modificación | ✅ SÍ | Verificar que no rompe arquitectura |
| Refactor | ✅ SÍ | Oportunidad de mejorar |

---

## Instalación

### Windows (recomendado)

1. Descarga o clona este repositorio
2. Navega a la carpeta `philosophy-mcp`
3. Doble clic en **`INSTALAR.bat`**
4. Reinicia Claude Code

### macOS / Linux

```bash
cd philosophy-mcp
pip install -r requirements.txt
claude mcp add philosophy -- python3 $(pwd)/server.py
```

### Verificar instalación

```bash
claude mcp list
```

Debe mostrar:
```
philosophy (local - stdio)
```

---

## Actualización

### Windows

> **Nota:** La actualización se hace desde el Explorador de Windows, NO desde Claude Code.

1. Cierra Claude Code si está abierto
2. Actualiza los archivos:
   - **Con git:** Abre terminal en la carpeta y ejecuta `git pull`
   - **Sin git:** Descarga el ZIP y reemplaza los archivos
3. Abre la carpeta `philosophy-mcp` en el Explorador
4. Doble clic en **`ACTUALIZAR.bat`**
5. Abre Claude Code de nuevo

### macOS / Linux

```bash
cd philosophy-mcp
git pull  # o descarga la nueva versión
# Reinicia Claude Code
```

### Verificar actualización

Después de reiniciar, ejecuta:
```
/filosofia arreglar bug en función X
```

El paso 1 debe pedir el parámetro `tipo_cambio` (nuevo/modificacion/bugfix/refactor).

---

## Reiniciar MCP manualmente

Si los cambios no se aplican:

### Opción 1: Reiniciar Claude Code
Cierra completamente y vuelve a abrir.

### Opción 2: Desde terminal
```bash
# Ver MCPs activos
claude mcp list

# Quitar y volver a añadir
claude mcp remove philosophy
claude mcp add philosophy -- python3 /ruta/completa/server.py
```

### Opción 3: Windows - Matar procesos
```powershell
Get-Process -Name "claude*" | Stop-Process -Force
```

---

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
