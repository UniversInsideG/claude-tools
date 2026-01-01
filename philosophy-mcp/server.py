#!/usr/bin/env python3
"""
MCP Server: Philosophy - UniversInside
=======================================
Servidor MCP que fuerza la filosofía de programación modular.
"Todo debe estar construido con piezas modulares reutilizables"
"""

import json
import os
import re
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server


# Crear instancia del servidor MCP
server = Server("philosophy")

# ============================================================
# CONFIGURACIÓN DE FILOSOFÍA
# ============================================================

PHILOSOPHY = {
    "principle": "Todo debe estar construido con piezas modulares reutilizables",
    "levels": {
        "pieza": "Unidad mínima, hace UNA sola cosa",
        "componente": "Reutilizable, va en components/",
        "pantalla": "Instancia única, construida con componentes",
        "contenedor": "Sistema que agrupa componentes (*_system, *_manager)",
        "estructura": "El proyecto completo"
    },
    "flow": {
        "1": "Buscar si existe algo similar (philosophy_search_similar)",
        "2": "Si existe → usarlo o extenderlo",
        "3": "Si no existe → crearlo siguiendo la filosofía",
        "4": "Validar que cumple las reglas (philosophy_validate_code)"
    },
    # Patrones que indican código NO modular en Godot
    "godot_smells": [
        (r"AppTheme\.style_button_primary\s*\(", "Usa PrimaryButton en lugar de Button + AppTheme.style_button_primary()"),
        (r"AppTheme\.style_button_secondary\s*\(", "Usa SecondaryButton en lugar de Button + AppTheme.style_button_secondary()"),
        (r"AppTheme\.style_button_icon\s*\(", "Usa IconButton en lugar de Button + AppTheme.style_button_icon()"),
        (r"AppTheme\.style_", "Considera crear un componente en lugar de aplicar estilos manualmente"),
    ],
    # Patrones que indican código NO modular en Python
    "python_smells": [
        (r"def\s+\w+\(.*\):\s*\n(\s+.+\n){50,}", "Función muy larga. Divide en funciones más pequeñas."),
    ],
    # Patrones que indican código NO modular en Web
    "web_smells": [
        (r"style\s*=\s*[\"']", "Evita estilos inline. Usa clases CSS reutilizables."),
    ]
}


# ============================================================
# HERRAMIENTAS DEL MCP
# ============================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Lista todas las herramientas disponibles"""
    return [
        Tool(
            name="philosophy_analyze",
            description="""OBLIGATORIO antes de escribir código.
Analiza qué vas a crear y verifica que cumple la filosofía modular.
Indica: descripción, nivel, de qué hereda, nombre de archivo, lenguaje, y qué reutiliza.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Descripción de lo que vas a crear"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["pieza", "componente", "pantalla", "contenedor", "estructura"],
                        "description": "Nivel en la arquitectura modular"
                    },
                    "inherits_from": {
                        "type": "string",
                        "description": "Clase o escena base de la que hereda (o 'ninguno')"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Ruta completa propuesta para el archivo"
                    },
                    "language": {
                        "type": "string",
                        "enum": ["godot", "python", "php", "web", "other"],
                        "description": "Lenguaje/tecnología"
                    },
                    "reuses_existing": {
                        "type": "string",
                        "description": "Componentes existentes que reutiliza (o 'ninguno' si no encontró)"
                    }
                },
                "required": ["description", "level", "inherits_from", "filename", "language"]
            }
        ),
        Tool(
            name="philosophy_search_similar",
            description="""OBLIGATORIO antes de crear algo nuevo.
Busca si ya existe algo similar en el proyecto que puedas reutilizar o extender.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "Término a buscar (ej: 'button', 'dialog', 'health')"
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Ruta del proyecto donde buscar"
                    },
                    "file_type": {
                        "type": "string",
                        "enum": ["gd", "tscn", "py", "php", "js", "all"],
                        "description": "Tipo de archivo a buscar"
                    }
                },
                "required": ["search_term", "project_path"]
            }
        ),
        Tool(
            name="philosophy_validate_code",
            description="""Valida que el código cumple con la filosofía modular.
Detecta: código duplicado, componentes no usados, estilos manuales, etc.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "El código a validar"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Ruta del archivo"
                    },
                    "language": {
                        "type": "string",
                        "enum": ["godot", "python", "php", "web", "other"],
                        "description": "Lenguaje del código"
                    }
                },
                "required": ["code", "filename", "language"]
            }
        ),
        Tool(
            name="philosophy_checklist",
            description="""Muestra el checklist y principios de la filosofía.""",
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

    if name == "philosophy_analyze":
        result = await analyze_before_code(
            arguments["description"],
            arguments["level"],
            arguments["inherits_from"],
            arguments["filename"],
            arguments["language"],
            arguments.get("reuses_existing", "ninguno")
        )

    elif name == "philosophy_search_similar":
        result = await search_similar_components(
            arguments["search_term"],
            arguments["project_path"],
            arguments.get("file_type", "all")
        )

    elif name == "philosophy_validate_code":
        result = await validate_code(
            arguments["code"],
            arguments["filename"],
            arguments["language"]
        )

    elif name == "philosophy_checklist":
        result = await show_checklist()

    else:
        result = f"Error: Herramienta '{name}' no encontrada"

    return [TextContent(type="text", text=result)]


# ============================================================
# IMPLEMENTACIÓN DE HERRAMIENTAS
# ============================================================

async def analyze_before_code(
    description: str,
    level: str,
    inherits_from: str,
    filename: str,
    language: str,
    reuses_existing: str
) -> str:
    """Analiza y valida antes de escribir código"""

    issues = []
    warnings = []
    suggestions = []

    # Validar nomenclatura según nivel y ubicación
    if language == "godot":
        # Solo validar nomenclatura *_component.gd si está en components/
        if level == "componente":
            if "components/" in filename or "component" in filename.lower():
                if not re.search(r"_component\.gd$|_button\.gd$|_card\.gd$|_dialog\.gd$|_input\.gd$", filename):
                    warnings.append(f"⚠️ Nomenclatura: Los componentes suelen terminar en _component.gd, _button.gd, etc.")

        # Contenedores deben tener nomenclatura específica
        elif level == "contenedor":
            if not re.search(r"(_system|_manager)\.gd$", filename):
                warnings.append(f"⚠️ Nomenclatura: Un contenedor debería terminar en '_system.gd' o '_manager.gd'")

        # Pantallas no requieren nomenclatura especial, pero deben heredar
        elif level == "pantalla":
            if inherits_from.lower() == "ninguno" or inherits_from.strip() == "":
                issues.append("❌ Las pantallas deben heredar de BaseScreen o similar")

    # Validar herencia para componentes
    if level == "componente" and (inherits_from.lower() == "ninguno" or inherits_from.strip() == ""):
        warnings.append("⚠️ Un componente normalmente hereda de una base. ¿Es intencional?")

    # Validar que buscó componentes existentes
    if reuses_existing.lower() == "ninguno" or reuses_existing.strip() == "":
        suggestions.append("💡 ¿Usaste philosophy_search_similar? Verifica que no exista algo similar.")

    # Construir respuesta
    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  ANÁLISIS DE FILOSOFÍA - UniversInside                          ║
║  "{PHILOSOPHY['principle']}"                                     ║
╚══════════════════════════════════════════════════════════════════╝

📋 DESCRIPCIÓN: {description}

📊 CLASIFICACIÓN:
   • Nivel: {level.upper()} - {PHILOSOPHY['levels'].get(level, '')}
   • Archivo: {filename}
   • Lenguaje: {language}
   • Hereda de: {inherits_from}
   • Reutiliza: {reuses_existing}

"""

    if issues:
        response += "❌ PROBLEMAS (corregir antes de continuar):\n"
        for issue in issues:
            response += f"   {issue}\n"
        response += "\n"

    if warnings:
        response += "⚠️ ADVERTENCIAS (revisar):\n"
        for warning in warnings:
            response += f"   {warning}\n"
        response += "\n"

    if suggestions:
        response += "💡 SUGERENCIAS:\n"
        for suggestion in suggestions:
            response += f"   {suggestion}\n"
        response += "\n"

    if not issues:
        response += """✅ ANÁLISIS APROBADO

Procede a escribir el código siguiendo:
• Cada función hace UNA sola cosa
• Usa componentes existentes (no reinventes)
• Signals para comunicación (Godot)
• No dupliques código
"""
    else:
        response += """🚫 CORRIGE LOS PROBLEMAS ANTES DE CONTINUAR
"""

    return response


async def search_similar_components(
    search_term: str,
    project_path: str,
    file_type: str = "all"
) -> str:
    """Busca componentes similares en el proyecto"""

    path = Path(project_path).expanduser().resolve()

    if not path.exists():
        return f"Error: El directorio {project_path} no existe"

    extensions = {
        "gd": [".gd"],
        "tscn": [".tscn"],
        "py": [".py"],
        "php": [".php"],
        "js": [".js", ".ts"],
        "all": [".gd", ".tscn", ".py", ".php", ".js", ".ts"]
    }

    exts = extensions.get(file_type, extensions["all"])

    found_files = []
    search_lower = search_term.lower()

    for ext in exts:
        for file in path.rglob(f"*{ext}"):
            if search_lower in file.name.lower() or search_lower in str(file).lower():
                if ".git" not in str(file) and "__pycache__" not in str(file) and "addons" not in str(file):
                    found_files.append(file)

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  BÚSQUEDA DE COMPONENTES EXISTENTES                             ║
╚══════════════════════════════════════════════════════════════════╝

🔍 Término: "{search_term}"
📁 Proyecto: {project_path}

"""

    if found_files:
        response += f"✅ ENCONTRADOS ({len(found_files)} archivos):\n\n"

        # Agrupar por carpeta
        by_folder = {}
        for f in found_files[:30]:
            folder = str(f.parent.relative_to(path))
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(f.name)

        for folder, files in by_folder.items():
            response += f"   📁 {folder}/\n"
            for fname in files:
                response += f"      • {fname}\n"

        if len(found_files) > 30:
            response += f"\n   ... y {len(found_files) - 30} más\n"

        response += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ DECISIÓN REQUERIDA:

   • Si existe algo similar → REUTILÍZALO o EXTIÉNDELO
   • Si no sirve → Justifica por qué creas uno nuevo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    else:
        response += """❌ NO SE ENCONTRÓ NADA SIMILAR

   Puedes crear algo nuevo, pero asegúrate de que:
   • Sea modular y reutilizable
   • Siga la nomenclatura correcta
   • Herede de una base si aplica
"""

    return response


async def validate_code(code: str, filename: str, language: str) -> str:
    """Valida que el código cumple con la filosofía"""

    issues = []
    warnings = []

    lines = code.split('\n')

    # Validar según lenguaje
    if language == "godot":
        # Detectar "code smells" de Godot
        for pattern, message in PHILOSOPHY["godot_smells"]:
            matches = re.findall(pattern, code)
            if matches:
                issues.append(f"❌ {message}")

        # Verificar signals vs llamadas directas
        direct_calls = len(re.findall(r'get_node\(["\']/', code))
        signals = len(re.findall(r'\.emit\(|\.connect\(', code))
        if direct_calls > 3 and signals == 0:
            warnings.append("⚠️ Muchas llamadas directas a nodos. Considera usar signals.")

        # Verificar colores hardcodeados
        if re.search(r'Color\s*\(\s*[\d.]+', code) and "AppTheme" not in code:
            warnings.append("⚠️ Colores hardcodeados. Usa AppTheme para consistencia.")

    elif language == "python":
        for pattern, message in PHILOSOPHY["python_smells"]:
            if re.search(pattern, code):
                warnings.append(f"⚠️ {message}")

    elif language == "web":
        for pattern, message in PHILOSOPHY["web_smells"]:
            if re.search(pattern, code):
                warnings.append(f"⚠️ {message}")

    # Validaciones universales
    # Clases múltiples
    classes = re.findall(r'^class\s+\w+', code, re.MULTILINE)
    if len(classes) > 2:
        warnings.append(f"⚠️ {len(classes)} clases en un archivo. Considera dividir.")

    # Código duplicado
    line_counts = {}
    for line in lines:
        stripped = line.strip()
        if len(stripped) > 30 and not stripped.startswith('#') and not stripped.startswith('//'):
            line_counts[stripped] = line_counts.get(stripped, 0) + 1
    duplicates = sum(1 for v in line_counts.values() if v >= 3)
    if duplicates > 0:
        warnings.append(f"⚠️ {duplicates} líneas repetidas 3+ veces. Extrae a función/componente.")

    # Construir respuesta
    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  VALIDACIÓN DE CÓDIGO - UniversInside                           ║
╚══════════════════════════════════════════════════════════════════╝

📄 Archivo: {filename}
🔧 Lenguaje: {language}
📏 Líneas: {len(lines)}

"""

    if issues:
        response += "❌ PROBLEMAS (usar componentes existentes):\n"
        for issue in issues:
            response += f"   {issue}\n"
        response += "\n"

    if warnings:
        response += "⚠️ ADVERTENCIAS:\n"
        for warning in warnings:
            response += f"   {warning}\n"
        response += "\n"

    if not issues and not warnings:
        response += "✅ CÓDIGO APROBADO - Cumple con la filosofía modular.\n"
    elif not issues:
        response += "✅ APROBADO CON ADVERTENCIAS - Revisar sugerencias.\n"
    else:
        response += "🚫 NO APROBADO - Usa los componentes existentes.\n"

    return response


async def show_checklist() -> str:
    """Muestra el checklist completo de filosofía"""

    return """
╔══════════════════════════════════════════════════════════════════╗
║  FILOSOFÍA DE PROGRAMACIÓN - UniversInside                       ║
║  "Todo debe estar construido con piezas modulares reutilizables" ║
╚══════════════════════════════════════════════════════════════════╝

📐 ARQUITECTURA:

   ESTRUCTURA (proyecto)
        └── CONTENEDOR (sistema)
              └── PANTALLA (instancia única)
                    └── COMPONENTE (reutilizable)
                          └── PIEZA (atómica)

📋 FLUJO OBLIGATORIO:

   1. philosophy_search_similar  → ¿Existe algo similar?
   2. Si existe → REUTILIZAR o EXTENDER
   3. Si no existe → CREAR siguiendo la filosofía
   4. philosophy_validate_code   → Validar resultado

✅ REGLAS (aplican a TODO, sea pantalla o componente):

   □ Buscar si existe antes de crear
   □ Usar componentes existentes (no reinventar)
   □ Heredar de base cuando corresponda
   □ Cada función hace UNA sola cosa
   □ Signals para comunicación (Godot)
   □ No estilos manuales si existe componente

❌ SEÑALES DE CÓDIGO NO MODULAR:

   Godot:
   • AppTheme.style_button_*() → Usa PrimaryButton, SecondaryButton
   • get_node() excesivo → Usa signals
   • Color() hardcodeado → Usa AppTheme

   Python:
   • Funciones de 50+ líneas → Divide
   • Código repetido → Extrae a función

   Web:
   • style="" inline → Usa clases CSS
   • HTML duplicado → Crea componente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"Máximo impacto, menor esfuerzo — a largo plazo"
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
