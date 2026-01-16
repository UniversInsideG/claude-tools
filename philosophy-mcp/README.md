# Philosophy MCP Server v1.5.0

Servidor MCP que fuerza la filosofía de programación modular en Claude Code.

> **"Máximo impacto, menor esfuerzo — a largo plazo"**
> **"Verificar ANTES de escribir, no DESPUÉS de fallar"**
> **"Documentar DESPUÉS de validar"**

---

## Herramientas (9 pasos obligatorios)

| Paso | Herramienta | Pregunta |
|------|-------------|----------|
| 1 | `philosophy_q1_responsabilidad` | ¿Hace UNA sola cosa? |
| 2 | `philosophy_q2_reutilizacion` | ¿Puedo reutilizar? |
| 3 | `philosophy_q3_buscar` | ¿Existe algo similar? (código + docs) |
| 4 | `philosophy_q4_herencia` | ¿Se actualizan las instancias? |
| 5 | `philosophy_q5_nivel` | ¿Nivel correcto? (comportamiento > nombre) |
| 6 | `philosophy_q6_verificar_dependencias` | ¿Las dependencias existen? |
| 7 | *Escribir código* | Siguiendo el diseño |
| 8 | `philosophy_validate` | Validar código |
| 9 | *Documentar* | Actualizar CHANGELOG |

**Auxiliares:**
- `philosophy_checklist` - Referencia rápida de las 5 preguntas y arquitectura

**Análisis arquitectónico:**
- `philosophy_architecture_analysis` - Iniciar análisis global de proyecto
- `philosophy_architecture_status` - Ver estado y encontrar análisis existentes
- `philosophy_architecture_resume` - Retomar análisis después de compactación
- `philosophy_architecture_checkpoint` - Guardar progreso

---

## Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `/filosofia [tarea]` | Activa el flujo de 9 pasos para la tarea |
| `/arquitectura [proyecto]` | Análisis arquitectónico global |

---

## Novedades v1.5.0

### Paso 3: Jerarquización de documentación
- Busca en código **Y** en `.claude/` y `docs/`
- Ordena por: tipo + fecha + relevancia
- Detecta versiones superseded del mismo tema
- Indicadores: 🔥 ALTA, 📌 MEDIA, 📎 BAJA

### Paso 5: Valida comportamiento
- Prioriza **comportamiento** sobre nomenclatura
- Legacy: documenta como deuda técnica (no bloquea)
- Código nuevo: exige nomenclatura correcta

### Paso 9: Documentar (NUEVO)
- Después de validar, documentar en CHANGELOG
- Incluir sección "Reemplaza/Obsoleta" si aplica

### /arquitectura: Búsqueda en disco
- Encuentra análisis existentes al iniciar nueva sesión
- Busca recursivamente en `.claude/`

---

## Aplica a TODO (sin excepciones)

| Tipo de cambio | ¿Usar flujo? | Por qué |
|----------------|--------------|---------|
| Código nuevo | ✅ SÍ | Diseño correcto desde inicio |
| Bug fix | ✅ SÍ | Un bug es señal de problema estructural |
| Modificación | ✅ SÍ | Verificar que no rompe arquitectura |
| Refactor | ✅ SÍ | Oportunidad de mejorar |

**NUNCA racionalizar para saltarse el flujo.** "Es solo un fix pequeño" es una excusa que acumula deuda técnica.

---

## Instalación

### Windows (recomendado)

1. Clona el repositorio:
   ```
   git clone https://github.com/usuario/claude-tools.git
   ```
2. Navega a la carpeta `philosophy-mcp`
3. Doble clic en **`INSTALAR.bat`**
4. Reinicia Claude Code

**El instalador configura:**
- MCP Server (philosophy)
- Comando `/filosofia` (9 pasos)
- Comando `/arquitectura` (análisis global)
- Instrucciones globales (CLAUDE.md)

### macOS / Linux

```bash
cd philosophy-mcp
pip install -r requirements.txt
claude mcp add philosophy -- python3 $(pwd)/server.py

# Copiar comandos
cp ../filosofia/commands/filosofia.md ~/.claude/commands/
cp ../filosofia/commands/arquitectura.md ~/.claude/commands/
cp ../filosofia/CLAUDE.md ~/.claude/
```

### Verificar instalación

En Claude Code:
```
/mcp
```

Debe mostrar `philosophy` en la lista.

---

## Actualización

### Windows

1. Cierra Claude Code
2. En la carpeta del repo: `git pull`
3. Doble clic en **`ACTUALIZAR.bat`**
4. Reinicia Claude Code

### macOS / Linux

```bash
cd philosophy-mcp
git pull

# Actualizar comandos
cp ../filosofia/commands/filosofia.md ~/.claude/commands/
cp ../filosofia/commands/arquitectura.md ~/.claude/commands/
```

### Verificar actualización

```
/filosofia crear componente X
```

El flujo debe mostrar **9 pasos** y el paso 3 debe buscar documentación.

---

## Uso

### Flujo básico con /filosofia

```
Usuario: /filosofia crear sistema de inventario

Claude ejecuta automáticamente:
1. philosophy_q1_responsabilidad → Define responsabilidad única
2. philosophy_q2_reutilizacion → ¿Es reutilizable?
3. philosophy_q3_buscar → Busca código Y documentación similar
4. philosophy_q4_herencia → Define herencia
5. philosophy_q5_nivel → Valida nivel (comportamiento)
6. philosophy_q6_verificar_dependencias → Verifica que existen
7. [Escribe el código]
8. philosophy_validate → Valida el código
9. [Documenta en CHANGELOG]
```

### Análisis arquitectónico con /arquitectura

```
Usuario: /arquitectura /ruta/al/proyecto

Claude ejecuta:
1. Busca análisis existentes en disco
2. Si encuentra → ofrece retomar
3. Si no → inicia nuevo análisis con 4 fases:
   - FASE 1: Inventario de archivos
   - FASE 2: Mapa de funcionalidades
   - FASE 3: Clasificación por niveles
   - FASE 4: Plan de refactorización
```

---

## Arquitectura de 5 niveles

```
Nivel 5: ESTRUCTURA   → El proyecto completo (main.tscn)
    └── Nivel 4: PANTALLA     → Vista única (*_screen)
          └── Nivel 3: CONTENEDOR   → Lógica reutilizable (*_system, *_manager)
                └── Nivel 2: COMPONENTE   → Combina piezas (*_component)
                      └── Nivel 1: PIEZA        → Unidad mínima, UNA cosa
```

**Nomenclatura Godot:**
- Pieza: `pieces/*_piece.(gd|tscn)`
- Componente: `components/*_component.(gd|tscn)`
- Contenedor: `systems/*_system.(gd|tscn)`
- Pantalla: `screens/*_screen.(gd|tscn)`
- Estructura: `main.tscn`

---

## Documentación adicional

| Documento | Descripción |
|-----------|-------------|
| `docs/CHANGELOG.md` | Historial de cambios |
| `docs/Q5_NIVEL_DESIGN.md` | Diseño del paso 5 (comportamiento vs nombre) |
| `docs/ARCHITECTURE_ANALYSIS_DESIGN.md` | Diseño del análisis arquitectónico |

---

## Troubleshooting

### El MCP no aparece

```bash
# Verificar
claude mcp list

# Reinstalar
claude mcp remove philosophy
claude mcp add philosophy -- python3 /ruta/completa/server.py
```

### Los comandos no funcionan

1. Verifica que existen en `~/.claude/commands/`
2. Reinicia Claude Code completamente

### Windows: Matar procesos

```powershell
Get-Process -Name "claude*" | Stop-Process -Force
```

---

## Desinstalar

```bash
claude mcp remove philosophy
rm ~/.claude/commands/filosofia.md
rm ~/.claude/commands/arquitectura.md
```

---

> **"Máximo impacto, menor esfuerzo — a largo plazo"**

*Philosophy MCP - UniversInside*
