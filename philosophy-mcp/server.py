#!/usr/bin/env python3
"""
MCP Server: Philosophy - UniversInside
=======================================
Servidor MCP que fuerza la filosofía de programación modular.
Provee herramientas que Claude DEBE usar antes de escribir código.
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
    "levels": {
        "pieza": "Unidad mínima, hace UNA sola cosa",
        "componente": "Combina piezas, nomenclatura: *_component",
        "contenedor": "Agrupa componentes, nomenclatura: *_system, *_manager",
        "estructura": "El proyecto completo"
    },
    "naming": {
        "godot": {
            "component": r".*_component\.gd$",
            "system": r".*_system\.gd$",
            "manager": r".*_manager\.gd$"
        },
        "python": {
            "component": r".*/components?/.*\.py$",
            "base": r".*/core/.*\.py$"
        }
    },
    "rules": [
        "Buscar si existe algo similar antes de crear",
        "Cada pieza hace UNA sola cosa",
        "Heredar de clases/escenas base cuando sea posible",
        "Usar signals en lugar de llamadas directas (Godot)",
        "No duplicar código - reutilizar"
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
            description="""OBLIGATORIO: Usa esta herramienta ANTES de escribir cualquier código.
Analiza qué vas a crear y verifica que cumple la filosofía modular.
Debes proporcionar: qué vas a crear, el nivel (pieza/componente/contenedor/estructura),
si hereda de algo, y la nomenclatura propuesta.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Descripción de lo que vas a crear"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["pieza", "componente", "contenedor", "estructura"],
                        "description": "Nivel en la arquitectura modular"
                    },
                    "inherits_from": {
                        "type": "string",
                        "description": "Clase o escena base de la que hereda (o 'ninguno' si no aplica)"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Nombre propuesto para el archivo"
                    },
                    "language": {
                        "type": "string",
                        "enum": ["godot", "python", "web", "other"],
                        "description": "Lenguaje/tecnología"
                    },
                    "reuses_existing": {
                        "type": "string",
                        "description": "Componentes existentes que reutiliza (o 'ninguno')"
                    }
                },
                "required": ["description", "level", "inherits_from", "filename", "language"]
            }
        ),
        Tool(
            name="philosophy_search_similar",
            description="""Busca componentes similares en el proyecto antes de crear uno nuevo.
DEBES usar esta herramienta antes de crear cualquier componente para verificar
que no existe algo similar que puedas reutilizar o extender.""",
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
            description="""Valida que un bloque de código cumple con la filosofía modular.
Analiza responsabilidad única, duplicación, nomenclatura y nivel correcto.""",
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
                    },
                    "expected_level": {
                        "type": "string",
                        "enum": ["pieza", "componente", "contenedor", "estructura"],
                        "description": "Nivel esperado según el análisis previo"
                    }
                },
                "required": ["code", "filename", "expected_level"]
            }
        ),
        Tool(
            name="philosophy_checklist",
            description="""Muestra el checklist completo de la filosofía de programación.
Usa esto cuando necesites recordar los principios o mostrarlos al usuario.""",
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
            arguments["expected_level"]
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
    approved = True

    # Validar nomenclatura según nivel y lenguaje
    if language == "godot":
        if level == "componente" and not re.search(r"_component\.gd$", filename):
            issues.append(f"❌ Nomenclatura: Un componente debe terminar en '_component.gd', no '{filename}'")
            approved = False
        elif level == "contenedor" and not re.search(r"(_system|_manager)\.gd$", filename):
            issues.append(f"❌ Nomenclatura: Un contenedor debe terminar en '_system.gd' o '_manager.gd', no '{filename}'")
            approved = False

    # Validar herencia
    if inherits_from.lower() == "ninguno" or inherits_from.strip() == "":
        if level in ["componente", "contenedor"]:
            warnings.append(f"⚠️ Herencia: Un {level} normalmente debería heredar de una base. Justifica por qué no.")

    # Validar reutilización
    if reuses_existing.lower() == "ninguno" or reuses_existing.strip() == "":
        warnings.append("⚠️ Reutilización: ¿Buscaste componentes existentes? Usa philosophy_search_similar primero.")

    # Construir respuesta
    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  ANÁLISIS DE FILOSOFÍA - UniversInside                          ║
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
        response += "❌ PROBLEMAS ENCONTRADOS:\n"
        for issue in issues:
            response += f"   {issue}\n"
        response += "\n"
        approved = False

    if warnings:
        response += "⚠️ ADVERTENCIAS:\n"
        for warning in warnings:
            response += f"   {warning}\n"
        response += "\n"

    if approved and not issues:
        response += """✅ ANÁLISIS APROBADO

Puedes proceder a escribir el código siguiendo estos principios:
• Responsabilidad única - cada función hace UNA cosa
• Usar signals para comunicación (Godot)
• No duplicar código existente
"""
    else:
        response += """🚫 ANÁLISIS NO APROBADO

Corrige los problemas antes de escribir código.
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

    # Definir extensiones a buscar
    extensions = {
        "gd": [".gd"],
        "tscn": [".tscn"],
        "py": [".py"],
        "php": [".php"],
        "js": [".js", ".ts"],
        "all": [".gd", ".tscn", ".py", ".php", ".js", ".ts"]
    }

    exts = extensions.get(file_type, extensions["all"])

    # Buscar archivos
    found_files = []
    search_lower = search_term.lower()

    for ext in exts:
        for file in path.rglob(f"*{ext}"):
            if search_lower in file.name.lower() or search_lower in str(file).lower():
                # Ignorar directorios comunes
                if ".git" not in str(file) and "__pycache__" not in str(file):
                    found_files.append(file)

    # Construir respuesta
    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  BÚSQUEDA DE COMPONENTES SIMILARES                              ║
╚══════════════════════════════════════════════════════════════════╝

🔍 Término: "{search_term}"
📁 Directorio: {project_path}
📄 Tipos: {file_type}

"""

    if found_files:
        response += f"✅ ENCONTRADOS ({len(found_files)} archivos):\n\n"
        for f in found_files[:20]:  # Limitar a 20 resultados
            relative = f.relative_to(path)
            response += f"   • {relative}\n"

        if len(found_files) > 20:
            response += f"\n   ... y {len(found_files) - 20} más\n"

        response += """
⚠️ IMPORTANTE: Revisa estos archivos antes de crear uno nuevo.
   Considera extender o reutilizar lo existente.
"""
    else:
        response += """❌ NO SE ENCONTRARON COINCIDENCIAS

   No hay componentes similares. Puedes crear uno nuevo,
   pero asegúrate de que sea reutilizable para el futuro.
"""

    return response


async def validate_code(code: str, filename: str, expected_level: str) -> str:
    """Valida que el código cumple con la filosofía"""

    issues = []
    warnings = []

    # Contar clases
    classes = re.findall(r'^class\s+\w+', code, re.MULTILINE)
    if len(classes) > 2:
        issues.append(f"❌ Responsabilidad: {len(classes)} clases en un archivo. Dividir en archivos separados.")

    # Detectar código duplicado potencial
    lines = code.split('\n')
    line_counts = {}
    for line in lines:
        stripped = line.strip()
        if len(stripped) > 30 and not stripped.startswith('#') and not stripped.startswith('//'):
            line_counts[stripped] = line_counts.get(stripped, 0) + 1

    duplicates = {k: v for k, v in line_counts.items() if v >= 3}
    if duplicates:
        issues.append(f"❌ DRY: Hay {len(duplicates)} líneas repetidas 3+ veces. Extraer a función.")

    # Validar nomenclatura Godot
    if filename.endswith('.gd'):
        # Verificar signals vs llamadas directas
        direct_calls = len(re.findall(r'get_node\(["\']/', code))
        signals = len(re.findall(r'\.emit\(|\.connect\(', code))

        if direct_calls > 3 and signals == 0:
            warnings.append("⚠️ Godot: Muchas llamadas directas a nodos. Usa signals para desacoplar.")

        # Verificar estilos hardcodeados
        if "Color(" in code and "AppTheme" not in code:
            warnings.append("⚠️ Godot: Colores hardcodeados. Usa AppTheme para consistencia.")

    # Construir respuesta
    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  VALIDACIÓN DE CÓDIGO - UniversInside                           ║
╚══════════════════════════════════════════════════════════════════╝

📄 Archivo: {filename}
📊 Nivel esperado: {expected_level.upper()}
📏 Líneas: {len(lines)}

"""

    if issues:
        response += "❌ PROBLEMAS:\n"
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
        response += "✅ CÓDIGO APROBADO CON ADVERTENCIAS - Revisar sugerencias.\n"
    else:
        response += "🚫 CÓDIGO NO APROBADO - Corregir problemas antes de guardar.\n"

    return response


async def show_checklist() -> str:
    """Muestra el checklist completo de filosofía"""

    return """
╔══════════════════════════════════════════════════════════════════╗
║  FILOSOFÍA DE PROGRAMACIÓN - UniversInside                       ║
║  "Máximo impacto, menor esfuerzo — a largo plazo"               ║
╚══════════════════════════════════════════════════════════════════╝

📐 ARQUITECTURA MODULAR JERÁRQUICA:

   Nivel 4: ESTRUCTURA   → El proyecto completo
   Nivel 3: CONTENEDOR   → Sistemas (*_system.gd, *_manager.gd)
   Nivel 2: COMPONENTE   → Combinan piezas (*_component.gd)
   Nivel 1: PIEZA        → Unidad mínima, hace UNA cosa

📋 CHECKLIST OBLIGATORIO:

   □ ¿Busqué si ya existe algo similar? (philosophy_search_similar)
   □ ¿Es el nivel correcto? (pieza/componente/contenedor/estructura)
   □ ¿Hereda de una clase/escena base?
   □ ¿La nomenclatura es correcta? (*_component, *_system, etc.)
   □ ¿Cada función hace UNA sola cosa?
   □ ¿Usa signals en lugar de llamadas directas? (Godot)
   □ ¿Puedo reutilizar esto en el futuro?

🔧 FLUJO OBLIGATORIO:

   1. philosophy_search_similar  → Buscar existente
   2. philosophy_analyze         → Analizar antes de escribir
   3. [Escribir código]
   4. philosophy_validate_code   → Validar resultado

⛔ NUNCA:
   • Mezclar responsabilidades de diferentes niveles
   • Duplicar código existente
   • Hardcodear estilos (usar AppTheme)
   • Usar llamadas directas cuando puedes usar signals
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
