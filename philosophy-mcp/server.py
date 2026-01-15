#!/usr/bin/env python3
"""
MCP Server: Philosophy - UniversInside
=======================================
Servidor MCP que fuerza la filosofía de programación modular.
Implementa 7 pasos obligatorios con 6 herramientas.

"Máximo impacto, menor esfuerzo — a largo plazo"
"""

import re
import json
from pathlib import Path
from datetime import datetime

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server


# Crear instancia del servidor MCP
server = Server("philosophy")

# ============================================================
# ESTADO DE SESIÓN - Tracking de los 7 pasos
# ============================================================

SESSION_STATE = {
    "step_1": False,  # Q1: Responsabilidad
    "step_2": False,  # Q2: Reutilización
    "step_3": False,  # Q3: Buscar similar
    "step_4": False,  # Q4: Herencia
    "step_5": False,  # Q5: Nivel
    # step_6 es escribir código (no es herramienta)
    # step_7 es validar
    "current_description": None,
    "current_level": None,
    "current_filename": None,
    "current_language": None,
    "current_change_type": None,  # nuevo/modificacion/bugfix/refactor
    "search_results": None,
}

def reset_state():
    """Resetea el estado para una nueva creación"""
    SESSION_STATE["step_1"] = False
    SESSION_STATE["step_2"] = False
    SESSION_STATE["step_3"] = False
    SESSION_STATE["step_4"] = False
    SESSION_STATE["step_5"] = False
    SESSION_STATE["current_description"] = None
    SESSION_STATE["current_level"] = None
    SESSION_STATE["current_filename"] = None
    SESSION_STATE["current_language"] = None
    SESSION_STATE["current_change_type"] = None
    SESSION_STATE["search_results"] = None


# ============================================================
# ESTADO DE ANÁLISIS ARQUITECTÓNICO
# ============================================================

ARCHITECTURE_STATE = {
    "active": False,
    "analysis_file": None,
    "checkpoint": 0,
    "phase": None,  # FASE_0, FASE_1, FASE_2, FASE_3, FASE_4, EJECUTANDO
    "project_path": None,
    "language": None,
}

def reset_architecture_state():
    """Resetea el estado del análisis arquitectónico"""
    ARCHITECTURE_STATE["active"] = False
    ARCHITECTURE_STATE["analysis_file"] = None
    ARCHITECTURE_STATE["checkpoint"] = 0
    ARCHITECTURE_STATE["phase"] = None
    ARCHITECTURE_STATE["project_path"] = None
    ARCHITECTURE_STATE["language"] = None


# ============================================================
# CONFIGURACIÓN DE FILOSOFÍA
# ============================================================

PHILOSOPHY = {
    "principle": "Máximo impacto, menor esfuerzo — a largo plazo",
    "levels": {
        "pieza": "Atómica, hace UNA sola cosa → pieces/*_piece.(gd|tscn)",
        "componente": "Combina piezas → components/*_component.(gd|tscn)",
        "contenedor": "Lógica reutilizable, orquesta componentes → systems/*_system.(gd|tscn)",
        "pantalla": "Vista única del usuario, orquesta contenedores → screens/*_screen.(gd|tscn)",
        "estructura": "El proyecto completo → main.tscn"
    },
    "naming": {
        "godot": {
            "pieza": r".*_piece\.(gd|tscn)$",
            "componente": r".*_component\.(gd|tscn)$",
            "contenedor": r".*_system\.(gd|tscn)$",
            "pantalla": r".*_screen\.(gd|tscn)$"
        },
        "python": {
            "pieza": r".*/pieces?/.*\.py$",
            "componente": r".*/components?/.*\.py$",
            "contenedor": r".*/systems?/.*\.py$",
            "pantalla": r".*/screens?/.*\.py$"
        },
        "web": {
            "pieza": r".*/atoms?/.*",
            "componente": r".*/molecules?/.*",
            "contenedor": r".*/organisms?/.*",
            "pantalla": r".*/templates?/.*"
        }
    },
    "code_smells": {
        "godot": [
            (r"AppTheme\.style_button_primary\s*\(", "Usa PrimaryButton en lugar de Button + AppTheme.style_button_primary()"),
            (r"AppTheme\.style_button_secondary\s*\(", "Usa SecondaryButton en lugar de Button + AppTheme.style_button_secondary()"),
            (r"AppTheme\.style_button_icon\s*\(", "Usa IconButton en lugar de Button + AppTheme.style_button_icon()"),
            (r"AppTheme\.style_", "Considera crear un componente en lugar de aplicar estilos manualmente"),
            (r"Color\s*\(\s*[\d.]+", "Color hardcodeado. Usa AppTheme para consistencia."),
        ],
        "python": [
            (r"def\s+\w+\([^)]*\):\s*\n(?:\s+.+\n){50,}", "Función muy larga (>50 líneas). Divide en funciones más pequeñas."),
        ],
        "web": [
            (r'style\s*=\s*["\']', "Evita estilos inline. Usa clases CSS reutilizables."),
        ]
    }
}


# ============================================================
# HERRAMIENTAS DEL MCP
# ============================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Lista todas las herramientas disponibles"""
    return [
        # Paso 1
        Tool(
            name="philosophy_q1_responsabilidad",
            description="""PASO 1 (OBLIGATORIO): ¿Esta pieza hace UNA sola cosa?
Reflexiona y define la responsabilidad única de lo que vas a crear.
Este es el PRIMER paso del flujo obligatorio.
APLICA A TODO: código nuevo, bug fixes, refactors, modificaciones.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Descripción de lo que vas a crear/modificar"
                    },
                    "responsabilidad_unica": {
                        "type": "string",
                        "description": "Define la UNA responsabilidad que tendrá"
                    },
                    "language": {
                        "type": "string",
                        "enum": ["godot", "python", "web", "other"],
                        "description": "Lenguaje/tecnología"
                    },
                    "tipo_cambio": {
                        "type": "string",
                        "enum": ["nuevo", "modificacion", "bugfix", "refactor"],
                        "description": "Tipo de cambio: nuevo (crear desde cero), modificacion (alterar existente), bugfix (corregir error), refactor (mejorar estructura)"
                    }
                },
                "required": ["description", "responsabilidad_unica", "language", "tipo_cambio"]
            }
        ),
        # Paso 2
        Tool(
            name="philosophy_q2_reutilizacion",
            description="""PASO 2 (OBLIGATORIO): ¿Puedo reutilizar esto en otro lugar?
Reflexiona sobre el diseño reutilizable.
Requiere: Paso 1 completado.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "es_reutilizable": {
                        "type": "boolean",
                        "description": "¿Se podrá reutilizar en otros lugares?"
                    },
                    "donde_reutilizar": {
                        "type": "string",
                        "description": "¿Dónde podría reutilizarse? (o 'solo aquí' si no aplica)"
                    },
                    "justificacion": {
                        "type": "string",
                        "description": "Justifica por qué es o no reutilizable"
                    }
                },
                "required": ["es_reutilizable", "donde_reutilizar", "justificacion"]
            }
        ),
        # Paso 3
        Tool(
            name="philosophy_q3_buscar",
            description="""PASO 3 (OBLIGATORIO): ¿Existe algo similar que pueda extender/heredar?
Busca por nombre + contenido + patrón en el proyecto.
Requiere: Paso 2 completado.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "Término a buscar"
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Ruta del proyecto donde buscar"
                    },
                    "content_pattern": {
                        "type": "string",
                        "description": "Patrón de contenido a buscar (regex opcional)"
                    }
                },
                "required": ["search_term", "project_path"]
            }
        ),
        # Paso 4
        Tool(
            name="philosophy_q4_herencia",
            description="""PASO 4 (OBLIGATORIO): ¿Si cambio la base, se actualizarán todas las instancias?
Define la herencia correcta basándote en lo que encontraste.
Requiere: Paso 3 completado.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "hereda_de": {
                        "type": "string",
                        "description": "Clase/escena base de la que hereda (o 'ninguno')"
                    },
                    "reutiliza_existente": {
                        "type": "string",
                        "description": "Componentes existentes que reutiliza (o 'ninguno')"
                    },
                    "justificacion_herencia": {
                        "type": "string",
                        "description": "Justifica la decisión de herencia"
                    }
                },
                "required": ["hereda_de", "reutiliza_existente", "justificacion_herencia"]
            }
        ),
        # Paso 5
        Tool(
            name="philosophy_q5_nivel",
            description="""PASO 5 (OBLIGATORIO): ¿Está en el nivel correcto de la jerarquía?
Justifica el nivel y propón el nombre de archivo.
El código valida que la nomenclatura coincida.
Requiere: Paso 4 completado.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "nivel": {
                        "type": "string",
                        "enum": ["pieza", "componente", "contenedor", "pantalla", "estructura"],
                        "description": "Nivel en la arquitectura (5 niveles)"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Nombre de archivo propuesto (con ruta)"
                    },
                    "justificacion_nivel": {
                        "type": "string",
                        "description": "Justifica por qué es este nivel"
                    }
                },
                "required": ["nivel", "filename", "justificacion_nivel"]
            }
        ),
        # Paso 7 (después de escribir código)
        Tool(
            name="philosophy_validate",
            description="""PASO 7 (OBLIGATORIO): Valida el código escrito.
Detecta code smells, duplicación, múltiples clases.
Requiere: Paso 5 completado + código escrito.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "El código a validar"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Nombre del archivo"
                    }
                },
                "required": ["code", "filename"]
            }
        ),
        # Auxiliar
        Tool(
            name="philosophy_checklist",
            description="""Muestra las 5 preguntas y la arquitectura.
Referencia rápida. Se puede usar en cualquier momento.""",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        # ============================================================
        # ANÁLISIS ARQUITECTÓNICO GLOBAL
        # ============================================================
        Tool(
            name="philosophy_architecture_analysis",
            description="""ANÁLISIS ARQUITECTÓNICO GLOBAL para refactorizaciones.

"El análisis ES exhaustivo, sistemático y exacto"

Úsalo cuando necesites:
- Refactorizar un módulo/proyecto completo
- Entender la arquitectura actual de código existente
- Reorganizar código que funciona para hacerlo mantenible

NO es para: crear una pieza nueva (usa el flujo q1→q7)

El análisis:
1. Crea archivo de documentación persistente
2. Escanea TODOS los archivos del módulo
3. Identifica funcionalidades existentes
4. Mapea cada archivo al nivel correcto (pieza/componente/contenedor/pantalla/estructura)
5. Detecta problemas arquitectónicos
6. Genera plan de refactorización con tests de verificación
7. Guarda checkpoints para retomar si se compacta la conversación""",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "Ruta del proyecto/módulo a analizar"
                    },
                    "language": {
                        "type": "string",
                        "enum": ["godot", "python", "web", "other"],
                        "description": "Lenguaje/tecnología principal"
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Nombre del proyecto (para el archivo de documentación)"
                    }
                },
                "required": ["project_path", "language", "project_name"]
            }
        ),
        Tool(
            name="philosophy_architecture_resume",
            description="""RETOMAR análisis arquitectónico después de compactación.

Lee el archivo de análisis y retoma EXACTAMENTE donde se quedó.
Usa esto cuando:
- La conversación se ha compactado
- Quieres continuar un análisis previo
- Necesitas recordar el estado actual del análisis""",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_file": {
                        "type": "string",
                        "description": "Ruta al archivo .md de análisis arquitectónico"
                    }
                },
                "required": ["analysis_file"]
            }
        ),
        Tool(
            name="philosophy_architecture_checkpoint",
            description="""GUARDAR checkpoint del análisis arquitectónico.

Guarda el progreso actual en el archivo de documentación.
Usa esto para asegurar que no se pierde información.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_file": {
                        "type": "string",
                        "description": "Ruta al archivo .md de análisis"
                    },
                    "checkpoint": {
                        "type": "integer",
                        "description": "Número de checkpoint (1-4)"
                    },
                    "phase": {
                        "type": "string",
                        "enum": ["FASE_1", "FASE_2", "FASE_3", "FASE_4", "EJECUTANDO"],
                        "description": "Fase actual del análisis"
                    },
                    "current_task": {
                        "type": "string",
                        "description": "Descripción de la tarea actual"
                    },
                    "next_step": {
                        "type": "string",
                        "description": "Descripción del siguiente paso"
                    },
                    "data": {
                        "type": "string",
                        "description": "Datos del checkpoint en formato markdown (inventario, mapa, análisis o plan)"
                    }
                },
                "required": ["analysis_file", "checkpoint", "phase", "current_task", "next_step", "data"]
            }
        ),
        Tool(
            name="philosophy_architecture_status",
            description="""VER ESTADO del análisis arquitectónico actual.

Muestra:
- Archivo de análisis activo
- Checkpoint actual
- Fase actual
- Progreso general""",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Ejecuta una herramienta según el nombre proporcionado"""

    if name == "philosophy_q1_responsabilidad":
        result = await step1_responsabilidad(
            arguments["description"],
            arguments["responsabilidad_unica"],
            arguments["language"],
            arguments.get("tipo_cambio", "nuevo")
        )

    elif name == "philosophy_q2_reutilizacion":
        result = await step2_reutilizacion(
            arguments["es_reutilizable"],
            arguments["donde_reutilizar"],
            arguments["justificacion"]
        )

    elif name == "philosophy_q3_buscar":
        result = await step3_buscar(
            arguments["search_term"],
            arguments["project_path"],
            arguments.get("content_pattern", None)
        )

    elif name == "philosophy_q4_herencia":
        result = await step4_herencia(
            arguments["hereda_de"],
            arguments["reutiliza_existente"],
            arguments["justificacion_herencia"]
        )

    elif name == "philosophy_q5_nivel":
        result = await step5_nivel(
            arguments["nivel"],
            arguments["filename"],
            arguments["justificacion_nivel"]
        )

    elif name == "philosophy_validate":
        result = await step7_validate(
            arguments["code"],
            arguments["filename"]
        )

    elif name == "philosophy_checklist":
        result = await show_checklist()

    # Análisis arquitectónico
    elif name == "philosophy_architecture_analysis":
        result = await architecture_analysis(
            arguments["project_path"],
            arguments["language"],
            arguments["project_name"]
        )

    elif name == "philosophy_architecture_resume":
        result = await architecture_resume(
            arguments["analysis_file"]
        )

    elif name == "philosophy_architecture_checkpoint":
        result = await architecture_checkpoint(
            arguments["analysis_file"],
            arguments["checkpoint"],
            arguments["phase"],
            arguments["current_task"],
            arguments["next_step"],
            arguments["data"]
        )

    elif name == "philosophy_architecture_status":
        result = await architecture_status()

    else:
        result = f"Error: Herramienta '{name}' no encontrada"

    return [TextContent(type="text", text=result)]


# ============================================================
# IMPLEMENTACIÓN DE PASOS
# ============================================================

async def step1_responsabilidad(description: str, responsabilidad: str, language: str, tipo_cambio: str = "nuevo") -> str:
    """PASO 1: ¿Hace UNA sola cosa?"""

    # Guardar en estado
    SESSION_STATE["current_description"] = description
    SESSION_STATE["current_language"] = language
    SESSION_STATE["current_change_type"] = tipo_cambio
    SESSION_STATE["step_1"] = True

    # Emoji y contexto según tipo de cambio
    tipo_info = {
        "nuevo": ("🆕", "Código nuevo", "Diseñar correctamente desde el inicio"),
        "modificacion": ("✏️", "Modificación", "Verificar que no rompe la responsabilidad única"),
        "bugfix": ("🐛", "Bug fix", "¿El bug revela un problema estructural?"),
        "refactor": ("♻️", "Refactor", "Oportunidad de mejorar la arquitectura"),
    }
    emoji, tipo_label, tipo_contexto = tipo_info.get(tipo_cambio, ("📝", tipo_cambio, ""))

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 1/7: RESPONSABILIDAD ÚNICA                                 ║
║  Pregunta: ¿Esta pieza hace UNA sola cosa?                       ║
╚══════════════════════════════════════════════════════════════════╝

{emoji} TIPO DE CAMBIO: {tipo_label}
   → {tipo_contexto}

📋 DESCRIPCIÓN: {description}

🎯 RESPONSABILIDAD ÚNICA DEFINIDA:
   {responsabilidad}

🔧 LENGUAJE: {language}

✅ PASO 1 COMPLETADO

➡️ SIGUIENTE: Usa philosophy_q2_reutilizacion
   Pregunta: ¿Puedo reutilizar esto en otro lugar?
"""
    return response


async def step2_reutilizacion(es_reutilizable: bool, donde: str, justificacion: str) -> str:
    """PASO 2: ¿Puedo reutilizar?"""

    # Verificar paso anterior
    if not SESSION_STATE["step_1"]:
        return """
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: PASO OBLIGATORIO OMITIDO                              ║
╚══════════════════════════════════════════════════════════════════╝

❌ DEBES completar philosophy_q1_responsabilidad PRIMERO

FLUJO OBLIGATORIO:
   1. philosophy_q1_responsabilidad  ← FALTA
   2. philosophy_q2_reutilizacion
   3. philosophy_q3_buscar
   4. philosophy_q4_herencia
   5. philosophy_q5_nivel
   6. [Escribir código]
   7. philosophy_validate
"""

    SESSION_STATE["step_2"] = True

    emoji = "♻️" if es_reutilizable else "📍"

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 2/7: REUTILIZACIÓN                                         ║
║  Pregunta: ¿Puedo reutilizar esto en otro lugar?                 ║
╚══════════════════════════════════════════════════════════════════╝

{emoji} ¿ES REUTILIZABLE?: {"Sí" if es_reutilizable else "No"}

📍 DÓNDE REUTILIZAR: {donde}

💡 JUSTIFICACIÓN: {justificacion}

✅ PASO 2 COMPLETADO

➡️ SIGUIENTE: Usa philosophy_q3_buscar
   Pregunta: ¿Existe algo similar que pueda extender/heredar?
"""
    return response


async def step3_buscar(search_term: str, project_path: str, content_pattern: str = None) -> str:
    """PASO 3: ¿Existe algo similar?"""

    # Verificar paso anterior
    if not SESSION_STATE["step_2"]:
        return """
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: PASO OBLIGATORIO OMITIDO                              ║
╚══════════════════════════════════════════════════════════════════╝

❌ DEBES completar philosophy_q2_reutilizacion PRIMERO

FLUJO OBLIGATORIO:
   1. philosophy_q1_responsabilidad  ✅
   2. philosophy_q2_reutilizacion    ← FALTA
   3. philosophy_q3_buscar
   4. philosophy_q4_herencia
   5. philosophy_q5_nivel
   6. [Escribir código]
   7. philosophy_validate
"""

    path = Path(project_path).expanduser().resolve()

    if not path.exists():
        return f"Error: El directorio {project_path} no existe"

    # Buscar por nombre
    found_by_name = []
    search_lower = search_term.lower()

    extensions = [".gd", ".tscn", ".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".vue"]

    for ext in extensions:
        for file in path.rglob(f"*{ext}"):
            if search_lower in file.name.lower():
                if ".git" not in str(file) and "__pycache__" not in str(file) and "addons" not in str(file):
                    found_by_name.append(file)

    # Buscar por contenido si se proporciona patrón
    found_by_content = []
    if content_pattern:
        for ext in extensions:
            for file in path.rglob(f"*{ext}"):
                if ".git" not in str(file) and "__pycache__" not in str(file):
                    try:
                        content = file.read_text(encoding='utf-8', errors='ignore')
                        if re.search(content_pattern, content, re.IGNORECASE):
                            if file not in found_by_name:
                                found_by_content.append(file)
                    except:
                        pass

    # Guardar resultados
    SESSION_STATE["search_results"] = found_by_name + found_by_content
    SESSION_STATE["step_3"] = True

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 3/7: BUSCAR SIMILAR                                        ║
║  Pregunta: ¿Existe algo similar que pueda extender/heredar?      ║
╚══════════════════════════════════════════════════════════════════╝

🔍 TÉRMINO: "{search_term}"
📁 PROYECTO: {project_path}
{"🔎 PATRÓN CONTENIDO: " + content_pattern if content_pattern else ""}

"""

    if found_by_name:
        response += f"📄 POR NOMBRE ({len(found_by_name)} archivos):\n"
        for f in found_by_name[:15]:
            try:
                relative = f.relative_to(path)
                response += f"   • {relative}\n"
            except:
                response += f"   • {f.name}\n"
        if len(found_by_name) > 15:
            response += f"   ... y {len(found_by_name) - 15} más\n"
        response += "\n"

    if found_by_content:
        response += f"📝 POR CONTENIDO ({len(found_by_content)} archivos):\n"
        for f in found_by_content[:10]:
            try:
                relative = f.relative_to(path)
                response += f"   • {relative}\n"
            except:
                response += f"   • {f.name}\n"
        response += "\n"

    if not found_by_name and not found_by_content:
        response += """❌ NO SE ENCONTRÓ NADA SIMILAR

   Puedes crear algo nuevo.
"""
    else:
        response += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IA: EVALÚA estos resultados y decide:
   • ¿Puedo REUTILIZAR alguno directamente?
   • ¿Puedo EXTENDER/HEREDAR de alguno?
   • ¿Necesito crear uno NUEVO? ¿Por qué?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    response += """
✅ PASO 3 COMPLETADO

➡️ SIGUIENTE: Usa philosophy_q4_herencia
   Pregunta: ¿Si cambio la base, se actualizarán todas las instancias?
"""
    return response


async def step4_herencia(hereda_de: str, reutiliza: str, justificacion: str) -> str:
    """PASO 4: ¿Se actualizan las instancias?"""

    # Verificar paso anterior
    if not SESSION_STATE["step_3"]:
        return """
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: PASO OBLIGATORIO OMITIDO                              ║
╚══════════════════════════════════════════════════════════════════╝

❌ DEBES completar philosophy_q3_buscar PRIMERO

FLUJO OBLIGATORIO:
   1. philosophy_q1_responsabilidad  ✅
   2. philosophy_q2_reutilizacion    ✅
   3. philosophy_q3_buscar           ← FALTA
   4. philosophy_q4_herencia
   5. philosophy_q5_nivel
   6. [Escribir código]
   7. philosophy_validate
"""

    SESSION_STATE["step_4"] = True

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 4/7: HERENCIA                                              ║
║  Pregunta: ¿Si cambio la base, se actualizarán las instancias?   ║
╚══════════════════════════════════════════════════════════════════╝

🔗 HEREDA DE: {hereda_de}

♻️ REUTILIZA EXISTENTE: {reutiliza}

💡 JUSTIFICACIÓN: {justificacion}

✅ PASO 4 COMPLETADO

➡️ SIGUIENTE: Usa philosophy_q5_nivel
   Pregunta: ¿Está en el nivel correcto de la jerarquía?
"""
    return response


async def step5_nivel(nivel: str, filename: str, justificacion: str) -> str:
    """PASO 5: ¿Nivel correcto?"""

    # Verificar paso anterior
    if not SESSION_STATE["step_4"]:
        return """
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: PASO OBLIGATORIO OMITIDO                              ║
╚══════════════════════════════════════════════════════════════════╝

❌ DEBES completar philosophy_q4_herencia PRIMERO

FLUJO OBLIGATORIO:
   1. philosophy_q1_responsabilidad  ✅
   2. philosophy_q2_reutilizacion    ✅
   3. philosophy_q3_buscar           ✅
   4. philosophy_q4_herencia         ← FALTA
   5. philosophy_q5_nivel
   6. [Escribir código]
   7. philosophy_validate
"""

    # Validar nomenclatura
    language = SESSION_STATE.get("current_language", "godot")
    issues = []

    if language in PHILOSOPHY["naming"]:
        pattern = PHILOSOPHY["naming"][language].get(nivel)
        if pattern and not re.search(pattern, filename):
            expected = {
                "pieza": "*_piece.(gd|tscn)" if language == "godot" else "pieces/*.py",
                "componente": "*_component.(gd|tscn)" if language == "godot" else "components/*.py",
                "contenedor": "*_system.(gd|tscn)" if language == "godot" else "systems/*.py",
                "pantalla": "*_screen.(gd|tscn)" if language == "godot" else "screens/*.py",
            }
            issues.append(f"❌ Nomenclatura incorrecta para {nivel}: debería ser {expected.get(nivel, 'ver documentación')}")

    if issues:
        error_response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: NOMENCLATURA NO VÁLIDA                                ║
╚══════════════════════════════════════════════════════════════════╝

📊 NIVEL: {nivel.upper()}
📄 ARCHIVO: {filename}

{chr(10).join(issues)}

NOMENCLATURA CORRECTA (5 niveles):
   • Pieza      → pieces/*_piece.(gd|tscn)
   • Componente → components/*_component.(gd|tscn)
   • Contenedor → systems/*_system.(gd|tscn)
   • Pantalla   → screens/*_screen.(gd|tscn)
   • Estructura → main.tscn

🚫 CORRIGE LA NOMENCLATURA Y VUELVE A INTENTAR
"""
        return error_response

    # Todo OK
    SESSION_STATE["step_5"] = True
    SESSION_STATE["current_level"] = nivel
    SESSION_STATE["current_filename"] = filename

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 5/7: NIVEL CORRECTO                                        ║
║  Pregunta: ¿Está en el nivel correcto de la jerarquía?           ║
╚══════════════════════════════════════════════════════════════════╝

📊 NIVEL: {nivel.upper()} - {PHILOSOPHY['levels'].get(nivel, '')}

📄 ARCHIVO: {filename}

💡 JUSTIFICACIÓN: {justificacion}

✅ NOMENCLATURA VALIDADA
✅ PASO 5 COMPLETADO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 RESUMEN DE DISEÑO:
   • Descripción: {SESSION_STATE.get('current_description', 'N/A')}
   • Nivel: {nivel}
   • Archivo: {filename}
   • Lenguaje: {language}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

➡️ SIGUIENTE:
   PASO 6: Escribe el código siguiendo el diseño
   PASO 7: Usa philosophy_validate para validar
"""
    return response


async def step7_validate(code: str, filename: str) -> str:
    """PASO 7: Validar código escrito"""

    # Verificar paso anterior
    if not SESSION_STATE["step_5"]:
        return """
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: PASOS OBLIGATORIOS OMITIDOS                           ║
╚══════════════════════════════════════════════════════════════════╝

❌ DEBES completar los pasos 1-5 antes de validar

FLUJO OBLIGATORIO:
   1. philosophy_q1_responsabilidad
   2. philosophy_q2_reutilizacion
   3. philosophy_q3_buscar
   4. philosophy_q4_herencia
   5. philosophy_q5_nivel
   6. [Escribir código]
   7. philosophy_validate          ← ESTÁS AQUÍ

⚠️ Empieza desde el paso 1.
"""

    language = SESSION_STATE.get("current_language", "godot")
    issues = []
    warnings = []

    lines = code.split('\n')

    # Detectar code smells por lenguaje
    if language in PHILOSOPHY["code_smells"]:
        for pattern, message in PHILOSOPHY["code_smells"][language]:
            if re.search(pattern, code):
                issues.append(f"❌ {message}")

    # Validar Q1: múltiples clases, funciones largas
    classes = re.findall(r'^class\s+\w+', code, re.MULTILINE)
    if len(classes) > 2:
        issues.append(f"❌ Responsabilidad: {len(classes)} clases en un archivo. Viola Q1: debe hacer UNA sola cosa.")

    # Detectar funciones muy largas
    func_matches = list(re.finditer(r'^(func|def)\s+\w+', code, re.MULTILINE))
    for i, match in enumerate(func_matches):
        start = match.start()
        end = func_matches[i + 1].start() if i + 1 < len(func_matches) else len(code)
        func_code = code[start:end]
        func_lines = len(func_code.split('\n'))
        if func_lines > 50:
            warnings.append(f"⚠️ Función muy larga ({func_lines} líneas). Considera dividir.")

    # Validar Q4: signals vs llamadas directas (Godot)
    if language == "godot":
        direct_calls = len(re.findall(r'get_node\(["\']/', code))
        signals = len(re.findall(r'\.emit\(|\.connect\(', code))
        if direct_calls > 3 and signals == 0:
            warnings.append("⚠️ Herencia: Muchas llamadas directas. Usa signals para desacoplar.")

        # Verificar extends
        if not re.search(r'^extends\s+', code, re.MULTILINE):
            warnings.append("⚠️ Herencia: No hay 'extends'. ¿Debería heredar de algo?")

    # Detectar código duplicado
    line_counts = {}
    for line in lines:
        stripped = line.strip()
        if len(stripped) > 30 and not stripped.startswith('#') and not stripped.startswith('//'):
            line_counts[stripped] = line_counts.get(stripped, 0) + 1

    duplicates = sum(1 for v in line_counts.values() if v >= 3)
    if duplicates > 0:
        issues.append(f"❌ DRY: {duplicates} líneas repetidas 3+ veces. Extrae a función/componente.")

    # Construir respuesta
    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 7/7: VALIDACIÓN FINAL                                      ║
╚══════════════════════════════════════════════════════════════════╝

📄 ARCHIVO: {filename}
🔧 LENGUAJE: {language}
📏 LÍNEAS: {len(lines)}

"""

    if issues:
        response += "❌ PROBLEMAS (bloquean):\n"
        for issue in issues:
            response += f"   {issue}\n"
        response += "\n"

    if warnings:
        response += "⚠️ ADVERTENCIAS:\n"
        for warning in warnings:
            response += f"   {warning}\n"
        response += "\n"

    if not issues and not warnings:
        response += "✅ CÓDIGO APROBADO\n\n"
        response += "El código cumple con la filosofía modular.\n"
        # Resetear estado para la próxima creación
        reset_state()
    elif not issues:
        response += "✅ CÓDIGO APROBADO CON ADVERTENCIAS\n\n"
        response += "Considera las advertencias para mejorar.\n"
        # Resetear estado
        reset_state()
    else:
        response += """🚫 CÓDIGO NO APROBADO

Corrige los problemas y vuelve a validar.
El código NO cumple con: "Máximo impacto, menor esfuerzo — a largo plazo"
"""

    return response


async def show_checklist() -> str:
    """Muestra el checklist completo"""

    current_step = "Ningún flujo activo"
    if SESSION_STATE["step_5"]:
        current_step = "5 completados → Listo para escribir código"
    elif SESSION_STATE["step_4"]:
        current_step = "4/5 → Falta: Q5 Nivel"
    elif SESSION_STATE["step_3"]:
        current_step = "3/5 → Falta: Q4 Herencia"
    elif SESSION_STATE["step_2"]:
        current_step = "2/5 → Falta: Q3 Buscar"
    elif SESSION_STATE["step_1"]:
        current_step = "1/5 → Falta: Q2 Reutilización"

    change_type = SESSION_STATE.get("current_change_type")
    change_type_display = f"({change_type})" if change_type else ""

    return f"""
╔══════════════════════════════════════════════════════════════════╗
║  FILOSOFÍA DE PROGRAMACIÓN - UniversInside                       ║
║  "Máximo impacto, menor esfuerzo — a largo plazo"               ║
╚══════════════════════════════════════════════════════════════════╝

⚠️ APLICA A TODO (sin excepciones):
   • Código nuevo    → Diseño correcto desde inicio
   • Bug fix         → Un bug es señal de problema estructural
   • Modificación    → Verificar que no rompe arquitectura
   • Refactor        → Oportunidad de mejorar

📊 ESTADO ACTUAL: {current_step} {change_type_display}

📐 ARQUITECTURA (5 niveles = Atomic Design):

   ESTRUCTURA (proyecto completo: main.tscn)
        └── PANTALLA (vista única: screens/*_screen)
              └── CONTENEDOR (lógica reutilizable: systems/*_system)
                    └── COMPONENTE (combina piezas: components/*_component)
                          └── PIEZA (atómica: pieces/*_piece)

   Contenedor = lógica reutilizable en varias pantallas
   Pantalla = vista única del usuario (no reutilizable)

📋 LAS 5 PREGUNTAS (flujo obligatorio):

   {"✅" if SESSION_STATE["step_1"] else "□"} 1. ¿Esta pieza hace UNA sola cosa?
   {"✅" if SESSION_STATE["step_2"] else "□"} 2. ¿Puedo reutilizar esto en otro lugar?
   {"✅" if SESSION_STATE["step_3"] else "□"} 3. ¿Existe algo similar que pueda extender/heredar?
   {"✅" if SESSION_STATE["step_4"] else "□"} 4. ¿Si cambio la base, se actualizarán todas las instancias?
   {"✅" if SESSION_STATE["step_5"] else "□"} 5. ¿Está en el nivel correcto de la jerarquía?

🔧 FLUJO DE HERRAMIENTAS:

   philosophy_q1_responsabilidad  → Paso 1
   philosophy_q2_reutilizacion    → Paso 2
   philosophy_q3_buscar           → Paso 3
   philosophy_q4_herencia         → Paso 4
   philosophy_q5_nivel            → Paso 5
   [Escribir código]              → Paso 6
   philosophy_validate            → Paso 7

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Si saltas un paso, el MCP bloquea y muestra error.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# ============================================================
# ANÁLISIS ARQUITECTÓNICO - IMPLEMENTACIÓN
# ============================================================

def get_file_info(file_path: Path, language: str) -> dict:
    """Extrae información de un archivo de código"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')

        # Contar clases y funciones según lenguaje
        if language == "godot":
            classes = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
            classes += 1 if re.search(r'^class_name\s+', content, re.MULTILINE) else 0
            functions = len(re.findall(r'^func\s+\w+', content, re.MULTILINE))
            extends = re.search(r'^extends\s+(\w+)', content, re.MULTILINE)
            extends = extends.group(1) if extends else None
        elif language == "python":
            classes = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
            functions = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
            extends = None
        elif language == "web":
            classes = len(re.findall(r'class\s+\w+', content))
            functions = len(re.findall(r'function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\(', content))
            extends = None
        else:
            classes = 0
            functions = 0
            extends = None

        # Determinar nivel actual basado en nomenclatura
        filename = file_path.name.lower()
        nivel_actual = "sin_clasificar"

        if language == "godot":
            if "_piece." in filename:
                nivel_actual = "pieza"
            elif "_component." in filename:
                nivel_actual = "componente"
            elif "_system." in filename:
                nivel_actual = "contenedor"
            elif "_screen." in filename:
                nivel_actual = "pantalla"
            elif filename == "main.tscn":
                nivel_actual = "estructura"
        elif language == "python":
            path_str = str(file_path).lower()
            if "/pieces/" in path_str or "/piece/" in path_str:
                nivel_actual = "pieza"
            elif "/components/" in path_str or "/component/" in path_str:
                nivel_actual = "componente"
            elif "/systems/" in path_str or "/system/" in path_str:
                nivel_actual = "contenedor"
            elif "/screens/" in path_str or "/screen/" in path_str:
                nivel_actual = "pantalla"

        return {
            "path": str(file_path),
            "name": file_path.name,
            "lines": len(lines),
            "classes": classes,
            "functions": functions,
            "extends": extends,
            "nivel_actual": nivel_actual
        }
    except Exception as e:
        return {
            "path": str(file_path),
            "name": file_path.name,
            "lines": 0,
            "classes": 0,
            "functions": 0,
            "extends": None,
            "nivel_actual": "error",
            "error": str(e)
        }


def scan_project_files(project_path: Path, language: str) -> list:
    """Escanea TODOS los archivos del proyecto"""
    files_info = []

    # Extensiones por lenguaje
    extensions = {
        "godot": [".gd", ".tscn"],
        "python": [".py"],
        "web": [".js", ".ts", ".jsx", ".tsx", ".vue", ".svelte"],
        "other": [".gd", ".py", ".js", ".ts"]
    }

    exts = extensions.get(language, extensions["other"])

    # Carpetas a ignorar
    ignore_dirs = {".git", "__pycache__", "node_modules", ".godot", "addons", "venv", ".venv"}

    for ext in exts:
        for file_path in project_path.rglob(f"*{ext}"):
            # Verificar si está en carpeta ignorada
            if any(ignored in file_path.parts for ignored in ignore_dirs):
                continue

            file_info = get_file_info(file_path, language)
            try:
                file_info["relative_path"] = str(file_path.relative_to(project_path))
            except:
                file_info["relative_path"] = file_path.name

            files_info.append(file_info)

    return files_info


def generate_analysis_template(project_name: str, project_path: str, language: str) -> str:
    """Genera la plantilla inicial del archivo de análisis"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f'''# Análisis Arquitectónico: {project_name}
Generado: {now}
Última actualización: {now}

> **"El análisis ES exhaustivo, sistemático y exacto"**

## METADATA (para retomar si se compacta la conversación)
- **Estado:** FASE_0
- **Checkpoint actual:** 0
- **Scope:** {project_path}
- **Lenguaje:** {language}
- **Tarea actual:** Iniciando análisis
- **Siguiente paso:** Ejecutar inventario exhaustivo de archivos

---

## 1. INVENTARIO DE ARCHIVOS (CHECKPOINT 1)

*Pendiente de completar*

---

## 2. MAPA DE FUNCIONALIDADES (CHECKPOINT 2)

*Pendiente de completar*

---

## 3. ANÁLISIS POR NIVELES (CHECKPOINT 3)

*Pendiente de completar*

---

## 4. PROBLEMAS DETECTADOS

*Pendiente de completar*

---

## 5. PLAN DE REFACTORIZACIÓN (CHECKPOINT 4)

*Pendiente de completar*

---

## 6. REGISTRO DE PROGRESO

| Fecha | Hora | Checkpoint | Acción | Resultado |
|-------|------|------------|--------|-----------|
| {datetime.now().strftime("%Y-%m-%d")} | {datetime.now().strftime("%H:%M")} | 0 | Inicio análisis | OK |

---

## 7. NOTAS Y DECISIONES

### Decisiones tomadas
*Ninguna aún*

### Pendientes por clarificar
*Ninguno aún*

---

## INSTRUCCIONES PARA RETOMAR

Si la conversación se ha compactado, sigue estos pasos:

1. Lee este archivo completo
2. Identifica el **Estado** y **Checkpoint actual** en METADATA
3. Lee la **Tarea actual** y **Siguiente paso**
4. Continúa desde donde se quedó
5. Actualiza el archivo con el progreso

**IMPORTANTE:** No empieces de cero. Retoma exactamente donde se quedó.
'''


async def architecture_analysis(project_path: str, language: str, project_name: str) -> str:
    """Inicia el análisis arquitectónico global"""

    path = Path(project_path).expanduser().resolve()

    if not path.exists():
        return f"Error: El directorio {project_path} no existe"

    # Crear directorio .claude si no existe
    claude_dir = path / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Nombre del archivo de análisis
    date_str = datetime.now().strftime("%Y%m%d")
    analysis_filename = f"architecture_analysis_{project_name}_{date_str}.md"
    analysis_file = claude_dir / analysis_filename

    # Generar plantilla inicial
    template = generate_analysis_template(project_name, str(path), language)
    analysis_file.write_text(template, encoding='utf-8')

    # Escanear archivos
    files_info = scan_project_files(path, language)

    # Actualizar estado
    ARCHITECTURE_STATE["active"] = True
    ARCHITECTURE_STATE["analysis_file"] = str(analysis_file)
    ARCHITECTURE_STATE["checkpoint"] = 0
    ARCHITECTURE_STATE["phase"] = "FASE_0"
    ARCHITECTURE_STATE["project_path"] = str(path)
    ARCHITECTURE_STATE["language"] = language

    # Generar resumen del inventario
    total_lines = sum(f["lines"] for f in files_info)
    total_classes = sum(f["classes"] for f in files_info)
    total_functions = sum(f["functions"] for f in files_info)

    # Agrupar por nivel actual
    by_level = {}
    for f in files_info:
        nivel = f["nivel_actual"]
        if nivel not in by_level:
            by_level[nivel] = []
        by_level[nivel].append(f)

    # Construir tabla de inventario
    inventory_table = "| # | Archivo | Líneas | Clases | Funciones | Nivel actual | Extends |\n"
    inventory_table += "|---|---------|--------|--------|-----------|--------------|----------|\n"

    for i, f in enumerate(files_info, 1):
        inventory_table += f"| {i} | {f['relative_path']} | {f['lines']} | {f['classes']} | {f['functions']} | {f['nivel_actual']} | {f['extends'] or '-'} |\n"

    response = f'''
╔══════════════════════════════════════════════════════════════════╗
║  ANÁLISIS ARQUITECTÓNICO INICIADO                                ║
║  "El análisis ES exhaustivo, sistemático y exacto"               ║
╚══════════════════════════════════════════════════════════════════╝

📁 PROYECTO: {project_name}
📂 RUTA: {path}
🔧 LENGUAJE: {language}

📄 ARCHIVO DE ANÁLISIS CREADO:
   {analysis_file}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 INVENTARIO INICIAL (FASE 0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 RESUMEN:
   • Archivos encontrados: {len(files_info)}
   • Total líneas de código: {total_lines}
   • Total clases: {total_classes}
   • Total funciones: {total_functions}

📊 POR NIVEL ACTUAL:
'''

    for nivel, archivos in sorted(by_level.items()):
        response += f"   • {nivel}: {len(archivos)} archivos\n"

    response += f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 INVENTARIO DETALLADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{inventory_table}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ FASE 0 COMPLETADA

➡️ SIGUIENTES PASOS:
   1. Usa philosophy_architecture_checkpoint para guardar el inventario (CHECKPOINT 1)
   2. Analiza las funcionalidades de cada archivo (FASE 2)
   3. Clasifica cada archivo en su nivel correcto (FASE 3)
   4. Genera el plan de refactorización (FASE 4)

⚠️ IMPORTANTE:
   - Guarda checkpoints frecuentemente
   - Si la conversación se compacta, usa philosophy_architecture_resume
   - El archivo de análisis está en: {analysis_file}
'''

    return response


async def architecture_resume(analysis_file: str) -> str:
    """Retoma un análisis arquitectónico desde el archivo"""

    file_path = Path(analysis_file).expanduser().resolve()

    if not file_path.exists():
        return f"Error: El archivo {analysis_file} no existe"

    content = file_path.read_text(encoding='utf-8')

    # Parsear METADATA
    estado_match = re.search(r'\*\*Estado:\*\*\s*(\w+)', content)
    checkpoint_match = re.search(r'\*\*Checkpoint actual:\*\*\s*(\d+)', content)
    scope_match = re.search(r'\*\*Scope:\*\*\s*(.+)', content)
    language_match = re.search(r'\*\*Lenguaje:\*\*\s*(\w+)', content)
    tarea_match = re.search(r'\*\*Tarea actual:\*\*\s*(.+)', content)
    siguiente_match = re.search(r'\*\*Siguiente paso:\*\*\s*(.+)', content)

    estado = estado_match.group(1) if estado_match else "DESCONOCIDO"
    checkpoint = int(checkpoint_match.group(1)) if checkpoint_match else 0
    scope = scope_match.group(1).strip() if scope_match else "DESCONOCIDO"
    language = language_match.group(1) if language_match else "other"
    tarea = tarea_match.group(1).strip() if tarea_match else "No especificada"
    siguiente = siguiente_match.group(1).strip() if siguiente_match else "No especificado"

    # Actualizar estado global
    ARCHITECTURE_STATE["active"] = True
    ARCHITECTURE_STATE["analysis_file"] = str(file_path)
    ARCHITECTURE_STATE["checkpoint"] = checkpoint
    ARCHITECTURE_STATE["phase"] = estado
    ARCHITECTURE_STATE["project_path"] = scope
    ARCHITECTURE_STATE["language"] = language

    # Extraer título del proyecto
    title_match = re.search(r'^# Análisis Arquitectónico:\s*(.+)$', content, re.MULTILINE)
    project_name = title_match.group(1) if title_match else "Proyecto"

    response = f'''
╔══════════════════════════════════════════════════════════════════╗
║  ANÁLISIS ARQUITECTÓNICO RETOMADO                                ║
║  "El análisis ES exhaustivo, sistemático y exacto"               ║
╚══════════════════════════════════════════════════════════════════╝

📁 PROYECTO: {project_name}
📄 ARCHIVO: {file_path}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 ESTADO RECUPERADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   • Estado: {estado}
   • Checkpoint: {checkpoint}
   • Scope: {scope}
   • Lenguaje: {language}

📋 TAREA ACTUAL:
   {tarea}

➡️ SIGUIENTE PASO:
   {siguiente}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ESTADO CARGADO CORRECTAMENTE

⚠️ IMPORTANTE:
   - Continúa desde la TAREA ACTUAL indicada arriba
   - Lee el archivo completo si necesitas más contexto
   - No empieces de cero
'''

    return response


async def architecture_checkpoint(
    analysis_file: str,
    checkpoint: int,
    phase: str,
    current_task: str,
    next_step: str,
    data: str
) -> str:
    """Guarda un checkpoint en el archivo de análisis"""

    file_path = Path(analysis_file).expanduser().resolve()

    if not file_path.exists():
        return f"Error: El archivo {analysis_file} no existe"

    content = file_path.read_text(encoding='utf-8')
    now = datetime.now()

    # Actualizar METADATA
    content = re.sub(
        r'\*\*Estado:\*\*\s*\w+',
        f'**Estado:** {phase}',
        content
    )
    content = re.sub(
        r'\*\*Checkpoint actual:\*\*\s*\d+',
        f'**Checkpoint actual:** {checkpoint}',
        content
    )
    content = re.sub(
        r'\*\*Tarea actual:\*\*\s*.+',
        f'**Tarea actual:** {current_task}',
        content
    )
    content = re.sub(
        r'\*\*Siguiente paso:\*\*\s*.+',
        f'**Siguiente paso:** {next_step}',
        content
    )
    content = re.sub(
        r'Última actualización:.+',
        f'Última actualización: {now.strftime("%Y-%m-%d %H:%M")}',
        content
    )

    # Actualizar sección según checkpoint
    section_markers = {
        1: ("## 1. INVENTARIO DE ARCHIVOS (CHECKPOINT 1)", "## 2. MAPA DE FUNCIONALIDADES"),
        2: ("## 2. MAPA DE FUNCIONALIDADES (CHECKPOINT 2)", "## 3. ANÁLISIS POR NIVELES"),
        3: ("## 3. ANÁLISIS POR NIVELES (CHECKPOINT 3)", "## 4. PROBLEMAS DETECTADOS"),
        4: ("## 5. PLAN DE REFACTORIZACIÓN (CHECKPOINT 4)", "## 6. REGISTRO DE PROGRESO"),
    }

    if checkpoint in section_markers:
        start_marker, end_marker = section_markers[checkpoint]
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            new_section = f"{start_marker}\n\n{data}\n\n---\n\n"
            content = content[:start_idx] + new_section + content[end_idx:]

    # Añadir entrada al registro de progreso
    progress_marker = "| Fecha | Hora | Checkpoint | Acción | Resultado |"
    progress_idx = content.find(progress_marker)
    if progress_idx != -1:
        # Encontrar el final de la cabecera de la tabla
        header_end = content.find("\n", progress_idx + len(progress_marker) + 1)
        if header_end != -1:
            new_entry = f"\n| {now.strftime('%Y-%m-%d')} | {now.strftime('%H:%M')} | {checkpoint} | {current_task} | OK |"
            # Insertar después de la última entrada
            table_end = content.find("\n---", header_end)
            if table_end != -1:
                content = content[:table_end] + new_entry + content[table_end:]

    # Guardar archivo actualizado
    file_path.write_text(content, encoding='utf-8')

    # Actualizar estado global
    ARCHITECTURE_STATE["checkpoint"] = checkpoint
    ARCHITECTURE_STATE["phase"] = phase

    response = f'''
╔══════════════════════════════════════════════════════════════════╗
║  CHECKPOINT {checkpoint} GUARDADO                                         ║
╚══════════════════════════════════════════════════════════════════╝

📄 ARCHIVO: {file_path}
📊 FASE: {phase}
📋 TAREA COMPLETADA: {current_task}

➡️ SIGUIENTE PASO: {next_step}

✅ DATOS GUARDADOS CORRECTAMENTE

⚠️ Si la conversación se compacta, usa:
   philosophy_architecture_resume("{analysis_file}")
'''

    return response


async def architecture_status() -> str:
    """Muestra el estado actual del análisis arquitectónico"""

    if not ARCHITECTURE_STATE["active"]:
        return '''
╔══════════════════════════════════════════════════════════════════╗
║  ESTADO DEL ANÁLISIS ARQUITECTÓNICO                              ║
╚══════════════════════════════════════════════════════════════════╝

❌ NO HAY ANÁLISIS ACTIVO

Para iniciar un análisis usa:
   philosophy_architecture_analysis

Para retomar un análisis existente usa:
   philosophy_architecture_resume
'''

    return f'''
╔══════════════════════════════════════════════════════════════════╗
║  ESTADO DEL ANÁLISIS ARQUITECTÓNICO                              ║
╚══════════════════════════════════════════════════════════════════╝

✅ ANÁLISIS ACTIVO

📄 Archivo: {ARCHITECTURE_STATE["analysis_file"]}
📊 Checkpoint: {ARCHITECTURE_STATE["checkpoint"]}
🔄 Fase: {ARCHITECTURE_STATE["phase"]}
📁 Proyecto: {ARCHITECTURE_STATE["project_path"]}
🔧 Lenguaje: {ARCHITECTURE_STATE["language"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FASES DEL ANÁLISIS:
   {"✅" if ARCHITECTURE_STATE["checkpoint"] >= 1 else "⬜"} FASE 1: Inventario de archivos
   {"✅" if ARCHITECTURE_STATE["checkpoint"] >= 2 else "⬜"} FASE 2: Mapa de funcionalidades
   {"✅" if ARCHITECTURE_STATE["checkpoint"] >= 3 else "⬜"} FASE 3: Análisis por niveles
   {"✅" if ARCHITECTURE_STATE["checkpoint"] >= 4 else "⬜"} FASE 4: Plan de refactorización
   {"🔄" if ARCHITECTURE_STATE["phase"] == "EJECUTANDO" else "⬜"} EJECUTANDO: Implementación del plan
'''


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

async def main():
    """Ejecuta el servidor MCP"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
