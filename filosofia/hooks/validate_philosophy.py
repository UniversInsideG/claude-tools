#!/usr/bin/env python3
"""
Hook de validación - Filosofía de Programación UniversInside
============================================================
Valida que el código generado cumpla con:
- Arquitectura Modular Jerárquica
- DRY (Don't Repeat Yourself)
- Single Responsibility
- Nomenclatura estándar
"""
import json
import sys
import re
import os

# ============================================================
# CONFIGURACIÓN DE CRITERIOS
# ============================================================

# Máximo de líneas para una función/método (Single Responsibility)
MAX_FUNCTION_LINES = 50

# Máximo de responsabilidades detectadas por archivo
MAX_RESPONSIBILITIES = 3

# Patrones de nomenclatura esperados por tipo
NAMING_PATTERNS = {
    'godot': {
        'component': r'.*[_]?component\.gd$',
        'system': r'.*[_]?system\.gd$',
        'manager': r'.*[_]?manager\.gd$',
    },
    'python': {
        'component': r'.*/components?/.*\.py$',
        'core': r'.*/core/.*\.py$',
        'utils': r'.*/utils?/.*\.py$',
    }
}

# Palabras clave que indican múltiples responsabilidades
RESPONSIBILITY_KEYWORDS = [
    (r'\bsave\b.*\bload\b', 'Guardar Y cargar en el mismo lugar'),
    (r'\brender\b.*\bupdate\b.*\bprocess\b', 'Renderizar, actualizar Y procesar juntos'),
    (r'\bhttp\b.*\bdatabase\b', 'HTTP Y base de datos acoplados'),
    (r'\bui\b.*\blogic\b', 'UI Y lógica de negocio mezcladas'),
]

# ============================================================
# FUNCIONES DE VALIDACIÓN
# ============================================================

def check_single_responsibility(content, file_path):
    """Verifica que el archivo tenga una sola responsabilidad"""
    issues = []

    # Contar clases en el archivo
    classes = re.findall(r'^class\s+\w+', content, re.MULTILINE)
    if len(classes) > 2:
        issues.append(f"⚠️ SOLID: {len(classes)} clases en un archivo. Considera separar en archivos distintos.")

    # Buscar mezcla de responsabilidades
    content_lower = content.lower()
    for pattern, description in RESPONSIBILITY_KEYWORDS:
        if re.search(pattern, content_lower):
            issues.append(f"⚠️ SOLID: Posible mezcla de responsabilidades - {description}")

    # Verificar funciones muy largas
    functions = re.findall(r'(def\s+\w+|func\s+\w+|function\s+\w+)[^{]*[{:]', content)
    lines = content.split('\n')

    # Análisis simple de longitud de funciones (aproximado)
    in_function = False
    function_lines = 0
    current_function = ""

    for line in lines:
        if re.match(r'\s*(def|func|function)\s+', line):
            if in_function and function_lines > MAX_FUNCTION_LINES:
                issues.append(f"⚠️ SOLID: Función '{current_function}' tiene ~{function_lines} líneas. Considera dividirla.")
            in_function = True
            function_lines = 0
            match = re.search(r'(def|func|function)\s+(\w+)', line)
            current_function = match.group(2) if match else "desconocida"
        elif in_function:
            function_lines += 1

    return issues


def check_dry(content, file_path):
    """Detecta posible código duplicado o repetitivo"""
    issues = []
    lines = content.split('\n')

    # Buscar bloques de código muy similares
    code_blocks = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if len(stripped) > 20 and not stripped.startswith('#') and not stripped.startswith('//'):
            if stripped in code_blocks:
                code_blocks[stripped].append(i + 1)
            else:
                code_blocks[stripped] = [i + 1]

    # Reportar líneas duplicadas significativas
    for code, line_numbers in code_blocks.items():
        if len(line_numbers) >= 3:
            issues.append(f"⚠️ DRY: Código repetido {len(line_numbers)} veces (líneas {line_numbers[:3]}...). Considera extraer a función/componente.")
            break  # Solo reportar el primer caso

    # Detectar patrones copy-paste comunes
    if re.search(r'# ?TODO:? ?(copy|copiar|duplicar)', content, re.IGNORECASE):
        issues.append("⚠️ DRY: Comentario sugiere código copiado. Considera refactorizar.")

    return issues


def check_naming_convention(content, file_path):
    """Verifica nomenclatura según la filosofía"""
    issues = []

    # Detectar tipo de archivo
    if file_path.endswith('.gd'):
        lang = 'godot'
    elif file_path.endswith('.py'):
        lang = 'python'
    else:
        return issues

    # Verificar si es un componente sin nomenclatura correcta
    content_lower = content.lower()

    # En Godot: si extiende Node y tiene señales, probablemente es un componente
    if lang == 'godot':
        is_component = 'signal ' in content and ('extends Node' in content or 'extends Area' in content)
        if is_component and not re.search(NAMING_PATTERNS['godot']['component'], file_path):
            issues.append(f"💡 Nomenclatura: Este parece ser un componente. Considera nombrarlo '*_component.gd'")

        is_system = 'autoload' in content_lower or ('func _ready' in content and 'get_tree' in content)
        if is_system and not re.search(NAMING_PATTERNS['godot']['system'], file_path):
            issues.append(f"💡 Nomenclatura: Este parece ser un sistema. Considera nombrarlo '*_system.gd'")

    return issues


def check_hierarchy_level(content, file_path):
    """Sugiere el nivel correcto en la jerarquía"""
    issues = []

    # Contar dependencias/imports
    imports = len(re.findall(r'^(import|from|#include|require|use)\s+', content, re.MULTILINE))

    # Contar exports/señales públicas
    exports = len(re.findall(r'(@export|@onready|signal\s+|public\s+|export\s+)', content))

    # Heurística simple
    if imports > 10:
        issues.append("💡 Jerarquía: Muchas dependencias. ¿Es este un Contenedor/Sistema? Verifica que no sea una Pieza sobrecargada.")

    if exports > 8:
        issues.append("💡 Jerarquía: Muchos exports/señales públicas. Verifica el nivel de abstracción.")

    return issues


def check_godot_specific(content, file_path):
    """Validaciones específicas para Godot"""
    issues = []

    if not file_path.endswith('.gd'):
        return issues

    # Verificar uso de señales vs llamadas directas
    direct_calls = len(re.findall(r'get_node\(["\']/', content))
    signals = len(re.findall(r'\.emit\(|\.connect\(', content))

    if direct_calls > 3 and signals == 0:
        issues.append("💡 Godot: Muchas llamadas directas a nodos. Considera usar Signals para desacoplar.")

    # Verificar herencia vs composición
    if 'extends Node' in content and len(re.findall(r'var\s+\w+\s*=\s*\$', content)) > 5:
        issues.append("💡 Godot: Muchas referencias a hijos. ¿Podrían ser componentes separados?")

    return issues


def check_python_specific(content, file_path):
    """Validaciones específicas para Python"""
    issues = []

    if not file_path.endswith('.py'):
        return issues

    # Verificar uso de clases base
    classes = re.findall(r'class\s+(\w+)\s*(?:\([^)]*\))?:', content)
    for cls in classes:
        # Si no hereda de nada significativo
        match = re.search(rf'class\s+{cls}\s*:', content)
        if match and 'ABC' not in content and 'Base' not in cls:
            issues.append(f"💡 Python: Clase '{cls}' no hereda. ¿Debería heredar de una clase base?")
            break

    return issues


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def validate(file_path, content):
    """Ejecuta todas las validaciones"""
    all_issues = []

    all_issues.extend(check_single_responsibility(content, file_path))
    all_issues.extend(check_dry(content, file_path))
    all_issues.extend(check_naming_convention(content, file_path))
    all_issues.extend(check_hierarchy_level(content, file_path))
    all_issues.extend(check_godot_specific(content, file_path))
    all_issues.extend(check_python_specific(content, file_path))

    return all_issues


def main():
    try:
        # Leer input del hook
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Solo procesar Edit y Write
        if tool_name not in ['Edit', 'Write']:
            sys.exit(0)

        file_path = tool_input.get('file_path', '')

        # Obtener contenido
        if tool_name == 'Write':
            content = tool_input.get('content', '')
        else:  # Edit
            content = tool_input.get('new_string', '')

        # Ignorar archivos de configuración y documentación
        ignore_patterns = ['.json', '.md', '.txt', '.yml', '.yaml', '.toml', '.lock']
        if any(file_path.endswith(p) for p in ignore_patterns):
            sys.exit(0)

        # Validar
        issues = validate(file_path, content)

        if issues:
            # Construir mensaje
            header = "\n╔══════════════════════════════════════════════════════════╗"
            header += "\n║  VALIDACIÓN - Filosofía de Programación UniversInside   ║"
            header += "\n╚══════════════════════════════════════════════════════════╝\n"

            message = header + f"\nArchivo: {file_path}\n\n"
            message += "\n".join(issues)
            message += "\n\n📖 Documenta: .claude/CODING_PHILOSOPHY.md"
            message += "\n💡 Comando: /filosofia check\n"

            # Retornar como advertencia (no bloquea, pero informa)
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "permissionDecisionReason": message
                }
            }
            print(json.dumps(output))
            sys.exit(0)

        # Sin issues - permitir silenciosamente
        sys.exit(0)

    except Exception as e:
        # En caso de error, no bloquear
        print(f"Error en hook de validación: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
