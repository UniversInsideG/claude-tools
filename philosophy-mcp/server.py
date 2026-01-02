#!/usr/bin/env python3
"""
MCP Server: Philosophy - UniversInside
=======================================
Servidor MCP que fuerza la filosofía de programación modular.
Implementa 7 pasos obligatorios con 6 herramientas.

"Máximo impacto, menor esfuerzo — a largo plazo"
"""

import re
from pathlib import Path

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
    SESSION_STATE["search_results"] = None


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
Este es el PRIMER paso del flujo obligatorio.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Descripción de lo que vas a crear"
                    },
                    "responsabilidad_unica": {
                        "type": "string",
                        "description": "Define la UNA responsabilidad que tendrá"
                    },
                    "language": {
                        "type": "string",
                        "enum": ["godot", "python", "web", "other"],
                        "description": "Lenguaje/tecnología"
                    }
                },
                "required": ["description", "responsabilidad_unica", "language"]
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
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Ejecuta una herramienta según el nombre proporcionado"""

    if name == "philosophy_q1_responsabilidad":
        result = await step1_responsabilidad(
            arguments["description"],
            arguments["responsabilidad_unica"],
            arguments["language"]
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

    else:
        result = f"Error: Herramienta '{name}' no encontrada"

    return [TextContent(type="text", text=result)]


# ============================================================
# IMPLEMENTACIÓN DE PASOS
# ============================================================

async def step1_responsabilidad(description: str, responsabilidad: str, language: str) -> str:
    """PASO 1: ¿Hace UNA sola cosa?"""

    # Guardar en estado
    SESSION_STATE["current_description"] = description
    SESSION_STATE["current_language"] = language
    SESSION_STATE["step_1"] = True

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 1/7: RESPONSABILIDAD ÚNICA                                 ║
║  Pregunta: ¿Esta pieza hace UNA sola cosa?                       ║
╚══════════════════════════════════════════════════════════════════╝

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

    current_step = "Ninguno"
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

    return f"""
╔══════════════════════════════════════════════════════════════════╗
║  FILOSOFÍA DE PROGRAMACIÓN - UniversInside                       ║
║  "Máximo impacto, menor esfuerzo — a largo plazo"               ║
╚══════════════════════════════════════════════════════════════════╝

📊 ESTADO ACTUAL: {current_step}

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
