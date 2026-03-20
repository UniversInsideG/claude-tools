#!/usr/bin/env python3
"""
MCP Server: Philosophy - UniversInside
=======================================
Servidor MCP que fuerza la filosofía de programación modular.
Implementa 10 pasos obligatorios (q0-q9) con 8 herramientas.

"Máximo impacto, menor esfuerzo — a largo plazo"
"Verificar ANTES de escribir, no DESPUÉS de fallar"
"""

import re
import json
import difflib
from pathlib import Path
from datetime import datetime

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server


# Crear instancia del servidor MCP
server = Server("philosophy")

# ============================================================
# ESTADO DE SESIÓN - Tracking de los 10 pasos (q0-q9)
# ============================================================

SESSION_STATE = {
    "step_0": False,  # Q0: Criterios acordados con el usuario
    "step_0_presented": False,  # Q0: Primera llamada (presentación) completada
    "step_1": False,  # Q1: Responsabilidad
    "step_2": False,  # Q2: Reutilización
    "step_3": False,  # Q3: Buscar similar
    "step_4": False,  # Q4: Herencia
    "step_5": False,  # Q5: Nivel
    "step_6": False,  # Q6: Verificar dependencias
    # step_7 es escribir código (no es herramienta)
    "step_8": False,  # Validar (philosophy_validate)
    # step_9 es documentar (philosophy_q9_documentar)
    "current_description": None,
    "current_level": None,
    "current_filename": None,
    "current_language": None,
    "current_change_type": None,  # nuevo/modificacion/bugfix/refactor
    "search_results": None,
    "verified_dependencies": None,  # Dependencias verificadas en q6
    "duplication_detected": None,  # Resultado de detección de duplicación en q3
    "criterios_file": None,  # Ruta del archivo de criterios creado por q0
    "reference_properties": [],  # Propiedades de referencia extraídas en q6
    "decision_pendiente": {},  # Justificaciones pendientes de verificación del usuario
}

def reset_state():
    """Resetea el estado para una nueva creación"""
    SESSION_STATE["step_0"] = False
    SESSION_STATE["step_0_presented"] = False
    SESSION_STATE["step_1"] = False
    SESSION_STATE["step_2"] = False
    SESSION_STATE["step_3"] = False
    SESSION_STATE["step_4"] = False
    SESSION_STATE["step_5"] = False
    SESSION_STATE["step_6"] = False
    SESSION_STATE["step_8"] = False
    SESSION_STATE["current_description"] = None
    SESSION_STATE["current_level"] = None
    SESSION_STATE["current_filename"] = None
    SESSION_STATE["current_language"] = None
    SESSION_STATE["current_change_type"] = None
    SESSION_STATE["search_results"] = None
    SESSION_STATE["verified_dependencies"] = None
    SESSION_STATE["duplication_detected"] = None
    SESSION_STATE["criterios_file"] = None
    SESSION_STATE["reference_properties"] = []
    SESSION_STATE["decision_pendiente"] = {}


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
    "plan_approved": False,  # v2.5.0: Gate para bloquear q1 hasta que el usuario apruebe el plan
}

def reset_architecture_state():
    """Resetea el estado del análisis arquitectónico"""
    ARCHITECTURE_STATE["active"] = False
    ARCHITECTURE_STATE["analysis_file"] = None
    ARCHITECTURE_STATE["checkpoint"] = 0
    ARCHITECTURE_STATE["phase"] = None
    ARCHITECTURE_STATE["project_path"] = None
    ARCHITECTURE_STATE["language"] = None
    ARCHITECTURE_STATE["plan_approved"] = False


def generar_error_paso_saltado(paso_faltante: str, paso_actual: str) -> str:
    """Genera mensaje de error que OBLIGA a explicar y preguntar al usuario"""
    return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ PASO SALTADO - REQUIERE DECISIÓN DEL USUARIO                 ║
╚══════════════════════════════════════════════════════════════════╝

❌ Intentaste usar {paso_actual} sin completar {paso_faltante}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 INSTRUCCIÓN OBLIGATORIA PARA CLAUDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASO 1: EXPLICA tu argumento
   Antes de preguntar, DEBES explicar al usuario POR QUÉ intentaste
   saltar el paso. El usuario necesita tu argumento para decidir.

   Ejemplo: "Intenté saltar el flujo porque [tu razón específica]"

PASO 2: USA AskUserQuestion
   Después de explicar, pregunta qué quiere hacer.

   Pregunta sugerida: "¿Qué prefieres hacer?"
   Opciones:
   1. "Seguir el flujo" - Empezar desde {paso_faltante}
   2. "Saltarme el flujo" - Continuar sin filosofía

🚫 PROHIBIDO:
- Preguntar SIN explicar primero tu argumento
- Decidir por tu cuenta sin preguntar
- Omitir la explicación de por qué querías saltar
- Usar frases genéricas como "es estándar" sin justificar

EL USUARIO NECESITA TU ARGUMENTO PARA EVALUAR SI ES VÁLIDO.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 DESPUÉS de que el usuario responda:
   Si el usuario decide continuar → Vuelve a llamar {paso_actual}
   con el parámetro decision_usuario=true

   Esto marca el paso como completado porque el usuario tomó
   la decisión conscientemente (asume la responsabilidad).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def manejar_decision_usuario(paso_faltante: str, paso_actual: str,
                              decision_usuario: bool = False,
                              justificacion_salto: str = None,
                              usuario_verifico: bool = False):
    """Proceso de dos pasos para saltar pasos con verificación del usuario.

    Paso 1: Claude llama con decision_usuario=true + justificacion_salto
            → Se almacena la justificación, se devuelve STOP
    Paso 2: Claude llama con usuario_verifico=true (después de preguntar al usuario)
            → Se verifica que hay justificación almacenada, se permite continuar

    Returns None para continuar, o string con mensaje para devolver a Claude.
    """
    decision_key = f"decision_{paso_actual}"

    # Si ambos llegan juntos, resolver en un solo paso
    if decision_usuario and usuario_verifico:
        if justificacion_salto:
            # Tiene justificación: almacenar y proceder directamente
            del_key = SESSION_STATE["decision_pendiente"].get(decision_key)
            if del_key:
                del SESSION_STATE["decision_pendiente"][decision_key]
            return None  # Proceder
        # Sin justificación: verificar si hay una almacenada de antes
        stored = SESSION_STATE["decision_pendiente"].get(decision_key)
        if stored:
            del SESSION_STATE["decision_pendiente"][decision_key]
            return None  # Proceder
        # Nada: pedir justificación
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ FALTA JUSTIFICACIÓN                                           ║
╚══════════════════════════════════════════════════════════════════╝

Enviaste decision_usuario=true + usuario_verifico=true pero sin justificacion_salto.
Añade justificacion_salto="tu razón para saltar {paso_faltante}" en la misma llamada.
"""

    # Paso 2: Usuario ya verificó
    if usuario_verifico:
        stored = SESSION_STATE["decision_pendiente"].get(decision_key)
        if not stored:
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ NO HAY JUSTIFICACIÓN REGISTRADA                               ║
╚══════════════════════════════════════════════════════════════════╝

No puedes usar usuario_verifico=true sin haber llamado antes con
decision_usuario=true + justificacion_salto.

Flujo correcto:
1. Llama con decision_usuario=true, justificacion_salto="tu razón"
2. Presenta la justificación al usuario con AskUserQuestion
3. Si el usuario acepta → llama con usuario_verifico=true
"""
        # Limpiar estado y permitir continuar
        del SESSION_STATE["decision_pendiente"][decision_key]
        return None  # None = proceder

    # Paso 1: Claude proporciona justificación
    if decision_usuario:
        if not justificacion_salto:
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ FALTA JUSTIFICACIÓN                                           ║
╚══════════════════════════════════════════════════════════════════╝

decision_usuario=true requiere el parámetro justificacion_salto
con tu razón para saltar {paso_faltante}.

Ejemplo: justificacion_salto="El paso ya se completó implícitamente porque..."
"""

        SESSION_STATE["decision_pendiente"][decision_key] = justificacion_salto

        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️ JUSTIFICACIÓN REGISTRADA - REQUIERE VERIFICACIÓN DEL USUARIO ║
╚══════════════════════════════════════════════════════════════════╝

📝 Tu justificación para saltar {paso_faltante}:
   "{justificacion_salto}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 INSTRUCCIÓN OBLIGATORIA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASO 1: Presenta al usuario tu justificación (el texto de arriba)
PASO 2: USA AskUserQuestion para preguntar:
   "¿Aceptas saltar {paso_faltante}?"
   Opciones:
   - "Sí, continuar" → Llama de nuevo con usuario_verifico=true
   - "No, seguir el flujo" → Completa {paso_faltante}

⛔ NO ejecutes {paso_actual} ni ninguna otra herramienta en este turno.
⛔ La pregunta es el FINAL del turno.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # Sin decision_usuario ni usuario_verifico: error estándar
    return generar_error_paso_saltado(paso_faltante, paso_actual)


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
            # Color hardcodeado se detecta por línea en step8_validate (necesita contexto de línea)
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
        # Paso 0
        Tool(
            name="philosophy_q0_criterios",
            description="""PASO 0 (OBLIGATORIO): Definir criterios con el usuario ANTES de diseñar.

"Entender bien es la forma más rápida de resolver"

ANTES de iniciar el flujo de diseño (q1-q9), DEBES:
1. Reformular lo que entendiste de la tarea
2. Identificar lo que no sabes o asumes
3. Presentar los criterios de éxito propuestos
4. ESPERAR confirmación del usuario (confirmado_por_usuario=false la primera vez)
5. Solo cuando el usuario confirme, llamar de nuevo con confirmado_por_usuario=true

Sin este paso, q1 está BLOQUEADO.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "tarea": {
                        "type": "string",
                        "description": "Qué pidió el usuario (la tarea original)"
                    },
                    "reformulacion": {
                        "type": "string",
                        "description": "Cómo entendiste la tarea (tu reformulación)"
                    },
                    "criterios": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Lista de criterios de éxito acordados"
                    },
                    "confirmado_por_usuario": {
                        "type": "boolean",
                        "description": "True SOLO después de que el usuario haya confirmado los criterios. La primera llamada DEBE ser false."
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Ruta del proyecto. Los criterios se guardan en .claude/criterios_{tarea}.md para persistir entre sesiones."
                    }
                },
                "required": ["tarea", "reformulacion", "criterios", "confirmado_por_usuario", "project_path"]
            }
        ),
        # Paso 1
        Tool(
            name="philosophy_q1_responsabilidad",
            description="""PASO 1 (OBLIGATORIO): ¿Esta pieza hace UNA sola cosa?
Reflexiona y define la responsabilidad única de lo que vas a crear.
Requiere: Paso 0 completado (criterios acordados con el usuario).
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
                    },
                    "decision_usuario": {
                        "type": "boolean",
                        "description": "PASO 1 para saltar: True + justificacion_salto. El MCP registra y pide que PREGUNTES al usuario."
                    },
                    "justificacion_salto": {
                        "type": "string",
                        "description": "OBLIGATORIO con decision_usuario=true. Tu razón para saltar el paso."
                    },
                    "usuario_verifico": {
                        "type": "boolean",
                        "description": "PASO 2 para saltar: True DESPUÉS de que el usuario confirmó con AskUserQuestion."
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
                    },
                    "decision_usuario": {
                        "type": "boolean",
                        "description": "PASO 1 para saltar: True + justificacion_salto. El MCP registra y pide que PREGUNTES al usuario."
                    },
                    "justificacion_salto": {
                        "type": "string",
                        "description": "OBLIGATORIO con decision_usuario=true. Tu razón para saltar el paso."
                    },
                    "usuario_verifico": {
                        "type": "boolean",
                        "description": "PASO 2 para saltar: True DESPUÉS de que el usuario confirmó con AskUserQuestion."
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
                    },
                    "decision_usuario": {
                        "type": "boolean",
                        "description": "PASO 1 para saltar: True + justificacion_salto. El MCP registra y pide que PREGUNTES al usuario."
                    },
                    "justificacion_salto": {
                        "type": "string",
                        "description": "OBLIGATORIO con decision_usuario=true. Tu razón para saltar el paso."
                    },
                    "usuario_verifico": {
                        "type": "boolean",
                        "description": "PASO 2 para saltar: True DESPUÉS de que el usuario confirmó con AskUserQuestion."
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
                    },
                    "decision_usuario": {
                        "type": "boolean",
                        "description": "PASO 1 para saltar: True + justificacion_salto. El MCP registra y pide que PREGUNTES al usuario."
                    },
                    "justificacion_salto": {
                        "type": "string",
                        "description": "OBLIGATORIO con decision_usuario=true. Tu razón para saltar el paso."
                    },
                    "usuario_verifico": {
                        "type": "boolean",
                        "description": "PASO 2 para saltar: True DESPUÉS de que el usuario confirmó con AskUserQuestion."
                    }
                },
                "required": ["nivel", "filename", "justificacion_nivel"]
            }
        ),
        # Paso 6 - NUEVO: Verificar dependencias
        Tool(
            name="philosophy_q6_verificar_dependencias",
            description="""PASO 6 (OBLIGATORIO): Verifica las dependencias externas ANTES de escribir código.

"Verificar ANTES de escribir, no DESPUÉS de fallar"

DEPENDENCIAS (funciones a llamar):
1. Que el archivo existe
2. Que la función existe
3. Que la firma (parámetros, tipos) coincide

FUNCIONES ELIMINADAS (dirección inversa):
1. Lista de funciones que se van a mover/eliminar del archivo original
2. Busca en TODO el proyecto quién las llama
3. Si encuentra llamadas externas → BLOQUEA con lista de archivos afectados
4. Así el diseño contempla wrappers/delegadores ANTES de escribir código

REFERENCIAS (código a replicar):
1. Extrae propiedades del código de referencia
2. Muestra los valores encontrados para análisis exhaustivo
3. Guarda las propiedades para que validate las verifique después

Si hay discrepancias, NO puedes continuar hasta resolverlas.
En refactors: si no se pasan removed_functions, se muestra warning.
Requiere: Paso 5 completado.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "Ruta del proyecto"
                    },
                    "dependencies": {
                        "type": "array",
                        "description": "Lista de dependencias a verificar",
                        "items": {
                            "type": "object",
                            "properties": {
                                "file": {
                                    "type": "string",
                                    "description": "Ruta del archivo (relativa al proyecto)"
                                },
                                "function": {
                                    "type": "string",
                                    "description": "Nombre de la función"
                                },
                                "expected_params": {
                                    "type": "string",
                                    "description": "Parámetros esperados, ej: 'data: Dictionary, flag: bool'"
                                },
                                "expected_return": {
                                    "type": "string",
                                    "description": "Tipo de retorno esperado, ej: 'void', 'bool', 'Dictionary'"
                                }
                            },
                            "required": ["file", "function"]
                        }
                    },
                    "references": {
                        "type": "array",
                        "description": "Lista de referencias (código a replicar) - OPCIONAL. Extrae propiedades para análisis exhaustivo.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "file": {
                                    "type": "string",
                                    "description": "Ruta del archivo (relativa al proyecto)"
                                },
                                "start_line": {
                                    "type": "integer",
                                    "description": "Línea inicial (opcional, 1-indexed)"
                                },
                                "end_line": {
                                    "type": "integer",
                                    "description": "Línea final (opcional, 1-indexed)"
                                },
                                "search_pattern": {
                                    "type": "string",
                                    "description": "Patrón para encontrar el bloque relevante (opcional)"
                                },
                                "must_document": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Propiedades que DEBEN documentarse, ej: ['layout_mode', 'anchors_preset']"
                                }
                            },
                            "required": ["file", "must_document"]
                        }
                    },
                    "removed_functions": {
                        "type": "array",
                        "description": "Lista de funciones que se van a ELIMINAR/MOVER del archivo original. El MCP busca en todo el proyecto quién las llama. Si encuentra llamadas externas, BLOQUEA.",
                        "items": {
                            "type": "string"
                        }
                    },
                    "source_file": {
                        "type": "string",
                        "description": "Archivo del que se eliminan las funciones (relativo al proyecto). Se excluye de la búsqueda para evitar falsos positivos."
                    },
                    "decision_usuario": {
                        "type": "boolean",
                        "description": "PASO 1 para saltar: True + justificacion_salto. El MCP registra y pide que PREGUNTES al usuario."
                    },
                    "justificacion_salto": {
                        "type": "string",
                        "description": "OBLIGATORIO con decision_usuario=true. Tu razón para saltar el paso."
                    },
                    "usuario_verifico": {
                        "type": "boolean",
                        "description": "PASO 2 para saltar: True DESPUÉS de que el usuario confirmó con AskUserQuestion."
                    }
                },
                "required": ["project_path"]
            }
        ),
        # Paso 8 (después de escribir código)
        Tool(
            name="philosophy_validate",
            description="""PASO 8 (OBLIGATORIO): Valida el código escrito.
Detecta code smells, duplicación, múltiples clases.
Requiere: Paso 6 completado + código escrito.

Si hay advertencias, DEBES preguntar al usuario con AskUserQuestion.
Usa usuario_confirmo_warnings=true solo DESPUÉS de que el usuario confirme.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "El código a validar. Opcional si se usa file_path."
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Ruta absoluta al archivo a validar. El servidor lee el contenido directamente. Usar cuando el código es muy grande para pasar como parámetro."
                    },
                    "filename": {
                        "type": "string",
                        "description": "Nombre del archivo. Opcional si se usa file_path (se extrae automáticamente)."
                    },
                    "usuario_confirmo_warnings": {
                        "type": "boolean",
                        "description": "SOLO usar después de preguntar al usuario. True = usuario confirmó ignorar advertencias."
                    },
                    "decision_usuario": {
                        "type": "boolean",
                        "description": "PASO 1 para saltar: True + justificacion_salto. El MCP registra y pide que PREGUNTES al usuario."
                    },
                    "justificacion_salto": {
                        "type": "string",
                        "description": "OBLIGATORIO con decision_usuario=true. Tu razón para saltar el paso."
                    },
                    "usuario_verifico": {
                        "type": "boolean",
                        "description": "PASO 2 para saltar: True DESPUÉS de que el usuario confirmó con AskUserQuestion."
                    }
                },
                "required": ["filename"]
            }
        ),
        # Paso 9 (documentar)
        Tool(
            name="philosophy_q9_documentar",
            description="""PASO 9 (OBLIGATORIO): Documenta los cambios realizados.

"Documentar DESPUÉS de validar"

Busca automáticamente:
1. CHANGELOG.md para registrar el cambio
2. README.md si cambia funcionalidad pública
3. Otros docs en docs/ que mencionen los archivos modificados

No puedes cerrar el flujo sin documentar.
Requiere: Paso 8 (validate) completado.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "Ruta del proyecto"
                    },
                    "archivos_modificados": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Lista de archivos creados/modificados"
                    },
                    "descripcion_cambio": {
                        "type": "string",
                        "description": "Descripción TÉCNICA del cambio (qué se modificó en el código)"
                    },
                    "descripcion_funcional": {
                        "type": "string",
                        "description": "Descripción FUNCIONAL del cambio (qué cambia para el usuario). Ejemplo: 'El popup de tiempo ahora aparece siempre al mover jugadores'"
                    },
                    "tipo_cambio": {
                        "type": "string",
                        "enum": ["añadido", "corregido", "cambiado", "eliminado"],
                        "description": "Tipo de cambio para el CHANGELOG"
                    },
                    "reemplaza": {
                        "type": "string",
                        "description": "Qué código/docs deja obsoleto este cambio (opcional)"
                    },
                    "decision_usuario": {
                        "type": "boolean",
                        "description": "PASO 1 para saltar: True + justificacion_salto. El MCP registra y pide que PREGUNTES al usuario."
                    },
                    "justificacion_salto": {
                        "type": "string",
                        "description": "OBLIGATORIO con decision_usuario=true. Tu razón para saltar el paso."
                    },
                    "usuario_verifico": {
                        "type": "boolean",
                        "description": "PASO 2 para saltar: True DESPUÉS de que el usuario confirmó con AskUserQuestion."
                    }
                },
                "required": ["project_path", "archivos_modificados", "descripcion_cambio", "tipo_cambio"]
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
                    },
                    "criterios_file": {
                        "type": "string",
                        "description": "Ruta al archivo de criterios a usar (de sesión anterior). Si se proporciona, no requiere q0 previo."
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

Busca tanto en memoria como en disco para encontrar análisis existentes.

Muestra:
- Archivo de análisis activo (si hay uno en memoria)
- Análisis previos encontrados en disco
- Checkpoint y fase actual
- Progreso general""",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "Ruta del proyecto donde buscar análisis existentes (opcional, mejora la búsqueda)"
                    }
                },
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Ejecuta una herramienta según el nombre proporcionado"""

    if name == "philosophy_q0_criterios":
        result = await step0_criterios(
            arguments["tarea"],
            arguments["reformulacion"],
            arguments["criterios"],
            arguments["confirmado_por_usuario"],
            arguments.get("project_path")
        )

    elif name == "philosophy_q1_responsabilidad":
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
            arguments["justificacion"],
            arguments.get("decision_usuario", False),
            arguments.get("justificacion_salto"),
            arguments.get("usuario_verifico", False)
        )

    elif name == "philosophy_q3_buscar":
        result = await step3_buscar(
            arguments["search_term"],
            arguments["project_path"],
            arguments.get("content_pattern", None),
            arguments.get("decision_usuario", False),
            arguments.get("justificacion_salto"),
            arguments.get("usuario_verifico", False)
        )

    elif name == "philosophy_q4_herencia":
        result = await step4_herencia(
            arguments["hereda_de"],
            arguments["reutiliza_existente"],
            arguments["justificacion_herencia"],
            arguments.get("decision_usuario", False),
            arguments.get("justificacion_salto"),
            arguments.get("usuario_verifico", False)
        )

    elif name == "philosophy_q5_nivel":
        result = await step5_nivel(
            arguments["nivel"],
            arguments["filename"],
            arguments["justificacion_nivel"],
            arguments.get("decision_usuario", False),
            arguments.get("justificacion_salto"),
            arguments.get("usuario_verifico", False)
        )

    elif name == "philosophy_q6_verificar_dependencias":
        result = await step6_verificar_dependencias(
            arguments["project_path"],
            arguments.get("dependencies", []),
            arguments.get("references", []),
            arguments.get("removed_functions", []),
            arguments.get("source_file"),
            arguments.get("decision_usuario", False),
            arguments.get("justificacion_salto"),
            arguments.get("usuario_verifico", False)
        )

    elif name == "philosophy_validate":
        result = await step8_validate(
            code=arguments.get("code"),
            filename=arguments.get("filename"),
            file_path=arguments.get("file_path"),
            usuario_confirmo_warnings=arguments.get("usuario_confirmo_warnings", False),
            decision_usuario=arguments.get("decision_usuario", False),
            justificacion_salto=arguments.get("justificacion_salto"),
            usuario_verifico=arguments.get("usuario_verifico", False)
        )

    elif name == "philosophy_q9_documentar":
        result = await step9_documentar(
            arguments["project_path"],
            arguments["archivos_modificados"],
            arguments["descripcion_cambio"],
            arguments["tipo_cambio"],
            arguments.get("reemplaza"),
            arguments.get("decision_usuario", False),
            arguments.get("justificacion_salto"),
            arguments.get("usuario_verifico", False),
            arguments.get("descripcion_funcional")
        )

    elif name == "philosophy_checklist":
        result = await show_checklist()

    # Análisis arquitectónico
    elif name == "philosophy_architecture_analysis":
        result = await architecture_analysis(
            arguments["project_path"],
            arguments["language"],
            arguments["project_name"],
            arguments.get("criterios_file")
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
        result = await architecture_status(
            arguments.get("project_path")
        )

    else:
        result = f"Error: Herramienta '{name}' no encontrada"

    return [TextContent(type="text", text=result)]


# ============================================================
# IMPLEMENTACIÓN DE PASOS
# ============================================================

async def step0_criterios(tarea: str, reformulacion: str, criterios: list, confirmado_por_usuario: bool, project_path: str = None) -> str:
    """PASO 0: Definir criterios con el usuario ANTES de diseñar"""
    import re

    # Detectar si Claude analizó código ANTES de usar esta herramienta
    patrones_analisis_previo = [
        r'\b(encontr[ée]|identifiqu[ée]|detect[ée]|descubr[íi])\b',
        r'\b(el bug est[áa]|la causa es|el problema est[áa])\b',
        r'\b(l[íi]nea \d+|en la funci[óo]n|en el archivo)\b',
        r'\b(deber[íi]a cambiar|hay que modificar|necesita corregir)\b',
        r'\b(ya analice|ya revis[ée]|ya le[íi])\b',
    ]

    advertencias_analisis = []
    texto_completo = f"{reformulacion} {' '.join(criterios)}"
    for patron in patrones_analisis_previo:
        if re.search(patron, texto_completo, re.IGNORECASE):
            advertencias_analisis.append(patron)

    # Detectar criterios que son código/implementación/debugging en vez de funcionales
    patrones_criterio_codigo = [
        # Código específico
        r'\b(usar|llamar|importar)\s+\w+\(',  # "usar funcion()"
        r'=\s*\d+',  # "= 0", "= 5"
        r'\b(layout_mode|anchors|stretch_mode|expand_mode)\b',  # propiedades específicas
        r'\.[a-z_]+\s*=',  # ".propiedad ="
        r'\b(get_node|add_child|emit|connect)\b',  # funciones específicas Godot
        r'_[a-z_]+\(',  # funciones con guión bajo "_trigger_master()"
        # Criterios de debugging/proceso (no funcionales)
        r'\b(identificar|verificar|comprobar)\s+(el punto|d[oó]nde|que los datos)\b',
        r'\b(proponer correcci[oó]n|basad[ao] en evidencia)\b',
        r'\b(los datos|par[aá]metros).*llegan correctamente\b',
        r'\b(el flujo|el punto exacto|d[oó]nde falla)\b',
    ]

    criterios_con_codigo = []
    for i, criterio in enumerate(criterios):
        for patron in patrones_criterio_codigo:
            if re.search(patron, criterio, re.IGNORECASE):
                criterios_con_codigo.append(i + 1)
                break

    if not confirmado_por_usuario:
        # Primera llamada: Claude presenta su entendimiento, debe PARAR y esperar
        criterios_fmt = "\n".join(f"   {i+1}. {c}" for i, c in enumerate(criterios))

        # Construir advertencias si las hay
        advertencias_texto = ""
        if advertencias_analisis:
            advertencias_texto += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ADVERTENCIA: POSIBLE ANÁLISIS PREVIO DETECTADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tu reformulación o criterios sugieren que YA ANALIZASTE código antes
de usar esta herramienta. Esto puede sesgar el análisis.

❌ INCORRECTO: Analizar → Usar herramienta (conclusiones sesgadas)
✅ CORRECTO: Usar herramienta → Analizar (guiado por criterios)

Si ya analizaste, considera:
- ¿Tus criterios reflejan lo que el USUARIO quiere, o lo que TÚ encontraste?
- ¿Estás definiendo QUÉ debe cumplirse, o CÓMO implementarlo?

"""

        if criterios_con_codigo:
            advertencias_texto += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ADVERTENCIA: CRITERIOS CON CÓDIGO/IMPLEMENTACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Los criterios #{', #'.join(map(str, criterios_con_codigo))} contienen cosas
concretas (código, debugging, flujo técnico) que sesgan el análisis.

Estás buscando POR QUÉ no funciona y te olvidas de la FUNCIONALIDAD que
debería cumplir.

Los criterios deben describir la FUNCIONALIDAD que el usuario espera, no el
proceso de investigación ni detalles de implementación.

Ejemplo - sesga el análisis:
   "Identificar el punto exacto donde falla el flujo"
   "Verificar que los datos (answer, type) llegan correctamente"

Ejemplo - describe la funcionalidad:
   "Todos los mensajes del Master deben quedar registrados en el chat privado"
   "Los observadores deben ver estos mensajes igual que el Master"

"""

        response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 0/9: CRITERIOS - REQUIERE CONFIRMACIÓN DEL USUARIO        ║
║  "Entender bien es la forma más rápida de resolver"              ║
╚══════════════════════════════════════════════════════════════════╝

📋 TAREA DEL USUARIO:
   {tarea}

🔄 TU REFORMULACIÓN:
   {reformulacion}

📐 CRITERIOS DE ÉXITO PROPUESTOS:
{criterios_fmt}
{advertencias_texto}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 INSTRUCCIÓN OBLIGATORIA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASO 1: Presenta al usuario tu reformulación y criterios (el texto de arriba)

   ⚠️ COMUNICACIÓN: Usa lenguaje FUNCIONAL, no nombres de funciones.
   El usuario necesita verificar que entendiste bien, y solo puede
   hacerlo si hablas de lo que PASA, no de cómo se LLAMA en el código.
   Ejemplo MAL: "show_view_grid() llama a _deferred_relayout()"
   Ejemplo BIEN: "al abrir capturas se oculta el mapa pero se le
   pide que se redibuje, lo que causa un bucle"

PASO 2: USA AskUserQuestion para preguntar:
   "¿Son correctos estos criterios?"
   Opciones:
   - "Sí, continuar" → Llama de nuevo con confirmado_por_usuario=true
   - "No, ajustar" → El usuario explicará qué cambiar

⛔ NO ejecutes q1 ni ninguna otra herramienta en este turno.
⛔ La pregunta es el FINAL del turno.
"""
        # Marcar que la presentación se completó
        SESSION_STATE["step_0_presented"] = True
        return response

    # Segunda llamada: usuario confirmó
    # Verificar que la primera llamada se hizo
    if not SESSION_STATE["step_0_presented"]:
        return """
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ CRITERIOS NO PRESENTADOS AL USUARIO                           ║
╚══════════════════════════════════════════════════════════════════╝

No puedes usar confirmado_por_usuario=true sin haber presentado
los criterios primero (confirmado_por_usuario=false).

El usuario debe VER los criterios antes de confirmarlos.

Llama primero con confirmado_por_usuario=false para presentar
tu reformulación y criterios. DESPUÉS de que el usuario confirme,
llama con confirmado_por_usuario=true.
"""
    # Re-verificar criterios de implementación (Claude puede haber ajustado sin limpiar)
    criterios_con_codigo_2 = []
    for i, criterio in enumerate(criterios):
        for patron in patrones_criterio_codigo:
            if re.search(patron, criterio, re.IGNORECASE):
                criterios_con_codigo_2.append(i + 1)
                break

    if criterios_con_codigo_2:
        criterios_fmt_err = "\n".join(f"   {i+1}. {c}" for i, c in enumerate(criterios))
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ CRITERIOS BLOQUEADOS - CONTIENEN IMPLEMENTACIÓN               ║
╚══════════════════════════════════════════════════════════════════╝

Los criterios #{', #'.join(map(str, criterios_con_codigo_2))} contienen detalles
de implementación, debugging o código específico:

{criterios_fmt_err}

Los criterios deben describir FUNCIONALIDAD, no implementación.

❌ INCORRECTO: "Usar layout_mode = 0" / "Verificar que los datos llegan"
✅ CORRECTO: "La imagen debe escalar manteniendo proporción" / "Los mensajes deben quedar registrados"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 ACCIÓN: Reformula los criterios marcados como funcionales
   y llama de nuevo con confirmado_por_usuario=false
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    SESSION_STATE["step_0"] = True

    criterios_fmt = "\n".join(f"   {i+1}. {c}" for i, c in enumerate(criterios))

    # Persistir criterios a disco
    from pathlib import Path
    import re
    path = Path(project_path).expanduser().resolve()
    claude_dir = path / ".claude"
    claude_dir.mkdir(exist_ok=True)
    nombre_tarea = re.sub(r'[^\w\s-]', '', tarea[:60]).strip().replace(' ', '_').lower()
    criterios_file = claude_dir / f"criterios_{nombre_tarea}.md"
    contenido = f"# Criterios: {tarea}\n\n## Reformulación\n{reformulacion}\n\n## Criterios de éxito\n"
    for i, c in enumerate(criterios):
        contenido += f"{i+1}. {c}\n"
    criterios_file.write_text(contenido, encoding='utf-8')
    SESSION_STATE["criterios_file"] = str(criterios_file)

    return f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 0/9: CRITERIOS ACORDADOS ✅                                ║
╚══════════════════════════════════════════════════════════════════╝

📋 TAREA: {tarea}

🔄 ENTENDIMIENTO: {reformulacion}

📐 CRITERIOS CONFIRMADOS:
{criterios_fmt}

✅ PASO 0 COMPLETADO - Criterios acordados con el usuario
💾 Criterios guardados en: {criterios_file}

➡️ SIGUIENTE: Usa philosophy_q1_responsabilidad
"""


async def step1_responsabilidad(description: str, responsabilidad: str, language: str, tipo_cambio: str = "nuevo") -> str:
    """PASO 1: ¿Hace UNA sola cosa?"""

    # Verificar paso 0
    if not SESSION_STATE["step_0"]:
        return generar_error_paso_saltado("philosophy_q0_criterios", "philosophy_q1_responsabilidad")

    # v2.5.0: Gate — bloquear implementación si hay análisis arquitectónico con plan no aprobado
    # QUÉ: Impide que q1 arranque si el plan del análisis arquitectónico no fue aprobado por el usuario.
    # PARA QUÉ: Para que el usuario reciba la devolución completa (técnica + funcional) y pueda decidir.
    # POR QUÉ: Sin este bloqueo, Claude 4.6 salta directamente a implementar después del checkpoint 4
    #           sin presentar conclusiones al usuario, que se queda sin información para tomar decisiones.
    if (ARCHITECTURE_STATE["active"]
            and ARCHITECTURE_STATE["checkpoint"] >= 4
            and not ARCHITECTURE_STATE["plan_approved"]):
        return """
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ IMPLEMENTACIÓN BLOQUEADA — PLAN NO APROBADO                  ║
╚══════════════════════════════════════════════════════════════════╝

El análisis arquitectónico tiene un plan completo (checkpoint 4)
pero el usuario NO ha aprobado la implementación.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUÉ debes hacer:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ANTES DE PRESENTAR — reconecta con los criterios:
   □ Lee los criterios acordados en q0 (.claude/criterios_*)
   □ ¿Cubres TODOS los criterios o solo los que coinciden
     con la solución técnica que encontraste?
   □ ¿El usuario puede verificar lo que dices sin leer código?
   □ ¿Cubres todas las situaciones que mencionó el usuario?

2. PRESENTA AL USUARIO la devolución del análisis:
   - Explicación FUNCIONAL: qué cambia para el usuario/jugador
   - Explicación TÉCNICA: qué archivos se modifican y por qué
   - Cada tarea con ambas explicaciones

3. USA AskUserQuestion para obtener aprobación explícita

4. Guarda la aprobación con architecture_checkpoint:
   phase="EJECUTANDO" para desbloquear la implementación

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARA QUÉ: El usuario necesita la información completa para decidir.
POR QUÉ: Sin devolución funcional, el usuario no puede evaluar si
         el plan resuelve su problema o si falta algo.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ NO puedes usar q1 hasta que el plan sea aprobado.
"""

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


async def step2_reutilizacion(es_reutilizable: bool, donde: str, justificacion: str,
                               decision_usuario: bool = False, justificacion_salto: str = None,
                               usuario_verifico: bool = False) -> str:
    """PASO 2: ¿Puedo reutilizar?"""

    # Verificar paso anterior
    if not SESSION_STATE["step_1"]:
        resultado = manejar_decision_usuario(
            "philosophy_q1_responsabilidad", "philosophy_q2_reutilizacion",
            decision_usuario, justificacion_salto, usuario_verifico
        )
        if resultado is not None:
            return resultado
        SESSION_STATE["step_1"] = True

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


# ============================================================
# SISTEMA DE JERARQUIZACIÓN DE DOCUMENTACIÓN
# ============================================================

# Tipos de documentos y su peso base
DOC_TYPE_WEIGHTS = {
    "guia": 100,        # Guías para desarrolladores - máxima prioridad
    "instrucciones": 95,
    "arquitectura": 90,
    "analisis": 85,
    "plan": 70,         # Planes bajan si están completados
    "solucion": 80,
    "fix": 75,
    "changelog": 40,    # Changelogs - prioridad baja (histórico)
    "deuda": 60,
    "indice": 20,       # Índices - muy baja prioridad
    "readme": 30,
    "otro": 50
}

# Tipos que permanecen vigentes aunque estén "completados/implementados"
DOC_TYPES_ALWAYS_VALID = {"guia", "instrucciones", "arquitectura"}

# Tipos que pierden relevancia cuando están "completados"
DOC_TYPES_EXPIRE_ON_COMPLETE = {"plan", "analisis", "fix", "solucion"}


def extract_doc_topic(filename: str, title: str) -> str:
    """Extrae el topic/tema principal de un documento para agrupar relacionados.

    Ejemplo: 'GUIA_DESARROLLO_MASTER_OBSERVER.md' -> 'master_observer'
             'architecture_analysis_master_observer_refactor_20260116.md' -> 'master_observer_refactor'
    """
    # Limpiar nombre
    name = filename.lower().replace('.md', '')

    # Quitar prefijos comunes
    prefixes_to_remove = [
        'guia_desarrollo_', 'guia_', 'guide_',
        'plan_refactorizacion_', 'plan_',
        'architecture_analysis_', 'analisis_',
        'solucion_', 'fix_', 'deuda_tecnica_'
    ]
    for prefix in prefixes_to_remove:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break

    # Quitar sufijos de fecha (ej: _20260116)
    name = re.sub(r'_\d{8}$', '', name)

    # Si el título es más específico, usarlo
    title_lower = title.lower()
    if 'master' in title_lower and 'observer' in title_lower:
        return 'master_observer'

    return name if name else 'general'


def extract_doc_metadata(content: str, filename: str) -> dict:
    """Extrae metadatos de un documento markdown."""
    metadata = {
        "date": None,
        "status": None,  # None = no especificado (diferente de "desconocido")
        "doc_type": "otro",
    }

    content_lower = content.lower()
    filename_lower = filename.lower()

    # 1. EXTRAER FECHA
    date_patterns = [
        r'última actualización[:\s]*(\d{4}-\d{2}-\d{2})',
        r'actualizado[:\s]*(\d{4}-\d{2}-\d{2})',
        r'fecha[:\s]*(\d{4}-\d{2}-\d{2})',
        r'generado[:\s]*(\d{4}-\d{2}-\d{2})',
        r'\*\*fecha:\*\*\s*(\d{4}-\d{2}-\d{2})',
        r'\*\*última actualización:\*\*\s*(\d{4}-\d{2}-\d{2})',
    ]

    for pattern in date_patterns:
        match = re.search(pattern, content_lower)
        if match:
            try:
                metadata["date"] = datetime.strptime(match.group(1), "%Y-%m-%d")
                break
            except:
                pass

    # Fecha en nombre de archivo (ej: _20260116)
    if not metadata["date"]:
        date_in_name = re.search(r'_(\d{8})\.md$', filename)
        if date_in_name:
            try:
                metadata["date"] = datetime.strptime(date_in_name.group(1), "%Y%m%d")
            except:
                pass

    # 2. EXTRAER ESTADO (solo si está explícito)
    status_patterns = [
        r'\*\*estado:\*\*\s*(\w+)',
        r'estado:\s*(\w+)',
    ]

    for pattern in status_patterns:
        match = re.search(pattern, content_lower)
        if match:
            status_raw = match.group(1).lower()
            # Normalizar
            if "activo" in status_raw or "vigente" in status_raw:
                metadata["status"] = "activo"
            elif "implementado" in status_raw:
                metadata["status"] = "implementado"
            elif "completado" in status_raw or "terminado" in status_raw:
                metadata["status"] = "completado"
            elif "progreso" in status_raw or "fase" in status_raw:
                metadata["status"] = "en_progreso"
            elif "pendiente" in status_raw:
                metadata["status"] = "pendiente"
            elif "obsoleto" in status_raw or "deprecated" in status_raw:
                metadata["status"] = "obsoleto"
            break

    # 3. EXTRAER TIPO DE DOCUMENTO
    if "guia" in filename_lower or "guide" in filename_lower:
        metadata["doc_type"] = "guia"
    elif "instrucciones" in filename_lower:
        metadata["doc_type"] = "instrucciones"
    elif "arquitectura" in filename_lower and "analisis" not in filename_lower:
        metadata["doc_type"] = "arquitectura"
    elif "architecture_analysis" in filename_lower or "analisis" in filename_lower:
        metadata["doc_type"] = "analisis"
    elif "plan" in filename_lower:
        metadata["doc_type"] = "plan"
    elif "solucion" in filename_lower:
        metadata["doc_type"] = "solucion"
    elif "fix" in filename_lower:
        metadata["doc_type"] = "fix"
    elif "changelog" in filename_lower:
        metadata["doc_type"] = "changelog"
    elif "deuda" in filename_lower:
        metadata["doc_type"] = "deuda"
    elif "indice" in filename_lower:
        metadata["doc_type"] = "indice"

    return metadata


def calculate_doc_relevance(doc: dict, search_term: str, content: str, topic_docs: dict) -> dict:
    """Calcula relevancia combinando: tipo + fecha + topic duplicado + frecuencia.

    Retorna dict con score y razones.
    """
    result = {
        "score": 0.0,
        "priority": "NORMAL",
        "age_label": "⚪ Sin fecha",
        "warnings": [],
        "is_superseded": False
    }

    search_lower = search_term.lower()
    doc_type = doc.get("doc_type", "otro")
    status = doc.get("status")  # None si no especificado
    doc_date = doc.get("date")
    topic = doc.get("topic", "general")

    # 1. PESO BASE POR TIPO
    base_score = DOC_TYPE_WEIGHTS.get(doc_type, 50)

    # 2. AJUSTE POR ESTADO (solo si está especificado)
    if status:
        if status == "obsoleto":
            base_score *= 0.1
            result["warnings"].append("⚠️ Marcado como obsoleto")
        elif status == "completado" and doc_type in DOC_TYPES_EXPIRE_ON_COMPLETE:
            base_score *= 0.5
            result["warnings"].append("Plan/análisis completado")
        elif status == "en_progreso":
            base_score *= 1.1  # Bonus por estar activo
        elif status == "activo":
            base_score *= 1.2

    # 3. AJUSTE POR ANTIGÜEDAD
    if doc_date:
        days_old = (datetime.now() - doc_date).days

        if days_old <= 7:
            base_score *= 1.4
            result["age_label"] = "🟢 Esta semana"
        elif days_old <= 30:
            base_score *= 1.2
            result["age_label"] = "🟢 Este mes"
        elif days_old <= 90:
            base_score *= 1.0
            result["age_label"] = "🟡 Últimos 3 meses"
        elif days_old <= 180:
            base_score *= 0.7
            result["age_label"] = "🟠 3-6 meses"
            if doc_type not in DOC_TYPES_ALWAYS_VALID:
                result["warnings"].append("Documento de hace 3-6 meses")
        else:
            base_score *= 0.4
            result["age_label"] = "🔴 +6 meses"
            if doc_type not in DOC_TYPES_ALWAYS_VALID:
                result["warnings"].append("Documento antiguo (+6 meses)")

    # 4. DETECCIÓN DE TOPIC DUPLICADO (superseded)
    if topic in topic_docs:
        same_topic_docs = topic_docs[topic]
        if len(same_topic_docs) > 1:
            # Ordenar por fecha (más reciente primero)
            sorted_by_date = sorted(
                same_topic_docs,
                key=lambda x: x.get("date") or datetime.min,
                reverse=True
            )

            # Si este doc NO es el más reciente del topic
            if doc_date and sorted_by_date[0].get("date"):
                newest_date = sorted_by_date[0].get("date")
                if doc_date < newest_date and doc["path"] != sorted_by_date[0]["path"]:
                    # Hay uno más nuevo
                    days_diff = (newest_date - doc_date).days
                    if days_diff > 7:  # Solo si hay diferencia significativa
                        result["is_superseded"] = True
                        base_score *= 0.3
                        result["warnings"].append(f"Hay versión más reciente ({days_diff} días después)")

    # 5. BONUS POR FRECUENCIA DEL TÉRMINO
    term_count = content.lower().count(search_lower)
    if term_count >= 10:
        base_score += 15
    elif term_count >= 5:
        base_score += 8

    # 6. BONUS SI APARECE EN TÍTULO
    if search_lower in doc.get("title", "").lower():
        base_score += 25

    # 7. BONUS POR SECCIONES CLAVE
    key_sections = ["instrucciones", "guía", "cómo", "pasos", "checklist", "para desarrolladores"]
    for section in doc.get("relevant_sections", []):
        if any(key in section.lower() for key in key_sections):
            base_score += 20
            break

    # Determinar prioridad
    result["score"] = round(base_score, 1)
    if result["score"] >= 100:
        result["priority"] = "🔥 ALTA"
    elif result["score"] >= 60:
        result["priority"] = "📌 MEDIA"
    else:
        result["priority"] = "📎 BAJA"

    return result


def search_project_documentation(project_path: Path, search_term: str) -> dict:
    """Busca documentación relevante con jerarquización inteligente.

    Retorna dict con:
    - primary: Lista de docs principales (más relevantes, no superseded)
    - secondary: Lista de docs secundarios (superseded o antiguos)
    - topics: Dict de topics encontrados
    """
    all_docs = []
    search_lower = search_term.lower()

    # Carpetas donde buscar
    doc_locations = [
        project_path / ".claude",
        project_path / "docs",
    ]

    for claude_dir in project_path.rglob(".claude"):
        if claude_dir.is_dir() and claude_dir not in doc_locations:
            doc_locations.append(claude_dir)

    # Primera pasada: recolectar todos los docs
    for doc_dir in doc_locations:
        if not doc_dir.exists():
            continue

        for md_file in doc_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')

                if search_lower not in content.lower():
                    continue

                # Extraer info básica
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem

                relevant_sections = []
                current_section = None
                for line in content.split('\n'):
                    if line.startswith('#'):
                        current_section = line.lstrip('#').strip()
                    if search_lower in line.lower() and current_section:
                        if current_section not in relevant_sections:
                            relevant_sections.append(current_section)

                metadata = extract_doc_metadata(content, md_file.name)
                topic = extract_doc_topic(md_file.name, title)

                doc_info = {
                    "path": str(md_file),
                    "relative_path": str(md_file.relative_to(project_path)) if md_file.is_relative_to(project_path) else md_file.name,
                    "title": title,
                    "relevant_sections": relevant_sections[:5],
                    "doc_type": metadata["doc_type"],
                    "status": metadata["status"],
                    "date": metadata["date"],
                    "topic": topic,
                    "content": content  # Guardar para calcular score
                }

                all_docs.append(doc_info)

            except Exception:
                pass

    # Agrupar por topic
    topic_docs = {}
    for doc in all_docs:
        topic = doc["topic"]
        if topic not in topic_docs:
            topic_docs[topic] = []
        topic_docs[topic].append(doc)

    # Segunda pasada: calcular relevancia con contexto de topics
    for doc in all_docs:
        relevance = calculate_doc_relevance(doc, search_term, doc["content"], topic_docs)
        doc["score"] = relevance["score"]
        doc["priority"] = relevance["priority"]
        doc["age_label"] = relevance["age_label"]
        doc["warnings"] = relevance["warnings"]
        doc["is_superseded"] = relevance["is_superseded"]
        del doc["content"]  # Limpiar

    # Separar primary y secondary
    primary = [d for d in all_docs if not d["is_superseded"] and d["score"] >= 30]
    secondary = [d for d in all_docs if d["is_superseded"] or d["score"] < 30]

    # Ordenar por score
    primary.sort(key=lambda x: x["score"], reverse=True)
    secondary.sort(key=lambda x: x["score"], reverse=True)

    return {
        "primary": primary,
        "secondary": secondary,
        "topics": list(topic_docs.keys()),
        "total": len(all_docs)
    }


# ============================================================
# DETECCIÓN DE DUPLICACIÓN (ENFOQUE HÍBRIDO)
# ============================================================

def calcular_similitud(contenido1: str, contenido2: str) -> float:
    """
    Calcula la similitud entre dos strings de código.
    Retorna un valor entre 0.0 (completamente diferentes) y 1.0 (idénticos).
    """
    if not contenido1 or not contenido2:
        return 0.0
    return difflib.SequenceMatcher(None, contenido1, contenido2).ratio()


def detectar_duplicacion(archivos: list, project_path: Path, language: str) -> dict:
    """
    Detecta duplicación REAL usando enfoque híbrido:
    1. Filtra archivos con patrones sospechosos (NO métodos estándar)
    2. Compara similitud de contenido entre archivos sospechosos
    3. Solo reporta duplicación si similitud > 60%

    Retorna:
        {
            "es_duplicacion": bool,
            "nivel": "alto" | "medio" | "bajo" | None,
            "archivos_duplicados": [(archivo1, archivo2, similitud)],
            "patrones_comunes": [patron1, patron2, ...],
            "recomendacion": str
        }
    """
    if not archivos:
        return {
            "es_duplicacion": False,
            "nivel": None,
            "archivos_duplicados": [],
            "patrones_comunes": [],
            "recomendacion": None
        }

    # PASO 1: Patrones que SÍ indican código sospechoso de duplicación
    # (NO incluye _ready/_process que son normales)
    if language == "godot":
        patrones_sospechosos = [
            (r'StyleBoxFlat\.new\(\)', "StyleBox creado manualmente"),
            (r'Color\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+', "Colores hardcodeados"),
            (r'add_theme_\w+_override\s*\([^)]+\)', "Overrides de tema"),
            (r'(HBoxContainer|VBoxContainer|TabContainer)\.new\(\)', "Containers en código"),
            (r'var\s+\w+\s*=\s*\d+\s*#', "Constantes mágicas"),
            (r'func\s+_crear_\w+|func\s+_setup_\w+|func\s+_init_\w+', "Funciones de setup custom"),
        ]
    elif language == "python":
        patrones_sospechosos = [
            (r'def\s+__init__\s*\(self[^)]*\):\s*\n\s+self\.\w+\s*=', "Init con atributos"),
            (r'def\s+(handle_|process_|create_)\w+', "Funciones handler/process/create"),
            (r'@(app|router)\.(get|post|put|delete)\s*\([^)]+\)', "Endpoints con ruta"),
            (r'class\s+\w+(Service|Manager|Handler|Controller)', "Clases Service/Manager"),
        ]
    else:
        patrones_sospechosos = [
            (r'function\s+(handle|create|process|init)\w+', "Funciones con prefijo común"),
            (r'class\s+\w+(Service|Manager|Handler|Controller)', "Clases Service/Manager"),
        ]

    # PASO 2: Filtrar archivos que tienen patrones sospechosos
    archivos_sospechosos = []
    patrones_encontrados = {}

    for archivo in archivos[:15]:  # Analizar hasta 15 archivos
        try:
            content = archivo.read_text(encoding='utf-8', errors='ignore')

            for patron, descripcion in patrones_sospechosos:
                if re.search(patron, content, re.MULTILINE):
                    archivos_sospechosos.append({
                        "archivo": archivo,
                        "contenido": content,
                        "patron": descripcion
                    })
                    patrones_encontrados[descripcion] = patrones_encontrados.get(descripcion, 0) + 1
                    break  # Un archivo solo cuenta una vez
        except:
            pass

    # Si menos de 2 archivos sospechosos, no hay duplicación posible
    if len(archivos_sospechosos) < 2:
        return {
            "es_duplicacion": False,
            "nivel": None,
            "archivos_duplicados": [],
            "patrones_comunes": [],
            "recomendacion": None
        }

    # PASO 3: Comparar similitud entre archivos sospechosos
    UMBRAL_SIMILITUD = 0.6  # 60% de similitud = duplicación
    duplicados = []

    for i, arch1 in enumerate(archivos_sospechosos):
        for arch2 in archivos_sospechosos[i+1:]:
            similitud = calcular_similitud(arch1["contenido"], arch2["contenido"])

            if similitud >= UMBRAL_SIMILITUD:
                duplicados.append({
                    "archivo1": arch1["archivo"].name,
                    "archivo2": arch2["archivo"].name,
                    "similitud": round(similitud * 100, 1),
                    "patron": arch1["patron"]
                })

    # PASO 4: Evaluar nivel de duplicación
    if not duplicados:
        # Hay archivos sospechosos pero no son similares entre sí
        return {
            "es_duplicacion": False,
            "nivel": None,
            "archivos_duplicados": [],
            "patrones_comunes": list(patrones_encontrados.keys()),
            "recomendacion": None
        }

    # Calcular nivel basado en similitud y cantidad
    max_similitud = max(d["similitud"] for d in duplicados)
    patrones_repetidos = [p for p, count in patrones_encontrados.items() if count > 1]

    if max_similitud >= 80 or len(duplicados) >= 3:
        nivel = "alto"
        recomendacion = "CREAR CLASE BASE que ambos hereden"
    elif max_similitud >= 60 or len(duplicados) >= 2:
        nivel = "medio"
        recomendacion = "Evaluar si HEREDAR del existente o EXTRAER base común"
    else:
        nivel = "bajo"
        recomendacion = "Revisar si hay oportunidad de REUTILIZAR"

    return {
        "es_duplicacion": True,
        "nivel": nivel,
        "archivos_duplicados": [(d["archivo1"], d["archivo2"], f"{d['similitud']}%") for d in duplicados],
        "patrones_comunes": patrones_repetidos if patrones_repetidos else [duplicados[0]["patron"]],
        "recomendacion": recomendacion
    }


async def step3_buscar(search_term: str, project_path: str, content_pattern: str = None,
                        decision_usuario: bool = False, justificacion_salto: str = None,
                        usuario_verifico: bool = False) -> str:
    """PASO 3: ¿Existe algo similar?

    Busca en:
    1. Código fuente (por nombre y contenido)
    2. Documentación del proyecto (.claude/, docs/)
    """

    # Verificar paso anterior
    if not SESSION_STATE["step_2"]:
        resultado = manejar_decision_usuario(
            "philosophy_q2_reutilizacion", "philosophy_q3_buscar",
            decision_usuario, justificacion_salto, usuario_verifico
        )
        if resultado is not None:
            return resultado
        SESSION_STATE["step_2"] = True

    path = Path(project_path).expanduser().resolve()

    if not path.exists():
        return f"Error: El directorio {project_path} no existe"

    # 1. BUSCAR EN CÓDIGO FUENTE (usando ripgrep si disponible, fallback a Python)
    import subprocess
    import shutil

    found_by_name = []
    found_by_content = []
    search_lower = search_term.lower()
    extensions = [".gd", ".tscn", ".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".vue"]
    rg_available = shutil.which("rg") is not None

    if rg_available:
        # Búsqueda por nombre con ripgrep --files + grep
        try:
            glob_args = []
            for ext in extensions:
                glob_args.extend(["--glob", f"*{ext}"])
            result = subprocess.run(
                ["rg", "--files", "--glob", "!.git", "--glob", "!__pycache__", "--glob", "!addons"] + glob_args,
                capture_output=True, text=True, cwd=str(path), timeout=30
            )
            for line in result.stdout.splitlines():
                if search_lower in Path(line).name.lower():
                    found_by_name.append(path / line)
        except (subprocess.TimeoutExpired, Exception):
            pass  # Fallback below if needed

        # Búsqueda por contenido con ripgrep
        if content_pattern:
            try:
                glob_args = []
                for ext in extensions:
                    glob_args.extend(["--glob", f"*{ext}"])
                result = subprocess.run(
                    ["rg", "-l", "-i", "--glob", "!.git", "--glob", "!__pycache__"] + glob_args + [content_pattern],
                    capture_output=True, text=True, cwd=str(path), timeout=30
                )
                for line in result.stdout.splitlines():
                    file_path_found = path / line
                    if file_path_found not in found_by_name:
                        found_by_content.append(file_path_found)
            except (subprocess.TimeoutExpired, Exception):
                pass
    else:
        # Fallback: Python rglob (lento en proyectos grandes)
        for ext in extensions:
            for file in path.rglob(f"*{ext}"):
                if ".git" not in str(file) and "__pycache__" not in str(file) and "addons" not in str(file):
                    if search_lower in file.name.lower():
                        found_by_name.append(file)

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

    # 2. BUSCAR EN DOCUMENTACIÓN DEL PROYECTO
    doc_results = search_project_documentation(path, search_term)
    primary_docs = doc_results["primary"]
    secondary_docs = doc_results["secondary"]

    # Guardar resultados
    SESSION_STATE["search_results"] = found_by_name + found_by_content
    SESSION_STATE["step_3"] = True

    # 3. DETECTAR DUPLICACIÓN
    language = SESSION_STATE.get("current_language", "godot")
    duplicacion = detectar_duplicacion(found_by_name + found_by_content, path, language)
    SESSION_STATE["duplication_detected"] = duplicacion

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 3/9: BUSCAR SIMILAR                                        ║
║  Pregunta: ¿Existe algo similar que pueda extender/heredar?      ║
╚══════════════════════════════════════════════════════════════════╝

🔍 TÉRMINO: "{search_term}"
📁 PROYECTO: {project_path}
{"🔎 PATRÓN CONTENIDO: " + content_pattern if content_pattern else ""}

"""

    # Mostrar documentación encontrada PRIMERO (prioridad alta)
    if primary_docs:
        response += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 DOCUMENTACIÓN RELEVANTE ({len(primary_docs)} principales, {len(secondary_docs)} secundarios)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANTE: Lee esta documentación ANTES de crear código nuevo.
   Ordenada por: tipo + fecha + relevancia (duplicados detectados)

"""
        for i, doc in enumerate(primary_docs[:5], 1):
            doc_type = doc.get('doc_type', 'otro').upper()
            priority = doc.get('priority', '📎 BAJA')
            age_label = doc.get('age_label', '⚪')

            response += f"{i}. {priority} {doc['title']}\n"
            response += f"   📁 {doc['relative_path']}\n"
            response += f"   {doc_type} | {age_label}\n"

            if doc.get('warnings'):
                for warning in doc['warnings'][:2]:
                    response += f"   ⚠️ {warning}\n"

            if doc['relevant_sections']:
                response += f"   Secciones:\n"
                for section in doc['relevant_sections'][:3]:
                    response += f"      → {section}\n"
            response += "\n"

        if secondary_docs:
            response += f"   📎 {len(secondary_docs)} docs secundarios (versiones anteriores o baja relevancia)\n\n"

    if found_by_name:
        response += f"📄 CÓDIGO POR NOMBRE ({len(found_by_name)} archivos):\n"
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
        response += f"📝 CÓDIGO POR CONTENIDO ({len(found_by_content)} archivos):\n"
        for f in found_by_content[:10]:
            try:
                relative = f.relative_to(path)
                response += f"   • {relative}\n"
            except:
                response += f"   • {f.name}\n"
        response += "\n"

    if not found_by_name and not found_by_content and not primary_docs:
        response += """❌ NO SE ENCONTRÓ NADA SIMILAR

   Puedes crear algo nuevo.
"""
    else:
        # Mostrar advertencia de duplicación si se detectó
        if duplicacion["es_duplicacion"]:
            nivel = duplicacion["nivel"]
            emoji = "⛔" if nivel == "alto" else "⚠️" if nivel == "medio" else "💡"

            response += f"""
{'═' * 68}
{emoji} DUPLICACIÓN DETECTADA - NIVEL {nivel.upper()}
{'═' * 68}

📋 ARCHIVOS CON CÓDIGO SIMILAR:
"""
            for arch1, arch2, similitud in duplicacion["archivos_duplicados"][:5]:
                response += f"   • {arch1} ↔ {arch2} ({similitud} similitud)\n"

            if duplicacion["patrones_comunes"]:
                response += f"\n🔍 PATRONES: {', '.join(duplicacion['patrones_comunes'])}\n"

            response += f"""
🎯 RECOMENDACIÓN: {duplicacion["recomendacion"]}

"""
            if nivel == "alto":
                response += """
╔══════════════════════════════════════════════════════════════════╗
║  🛑 PARA - NO CONTINUES SIN RESOLVER ESTO                        ║
╚══════════════════════════════════════════════════════════════════╝

⛔ INSTRUCCIÓN OBLIGATORIA PARA CLAUDE:

   Similitud >60% = DUPLICACIÓN REAL = DEUDA TÉCNICA

   ANTES de continuar con q4, DEBES:

   1. ANALIZAR qué código está duplicado entre los archivos
   2. IDENTIFICAR la abstracción común (BaseX, AbstractX)
   3. Estas son las opciones posibles:

      A) CREAR CLASE BASE nueva
         → hereda_de: "BaseNombreNuevo (crear)"
         → Los archivos existentes TAMBIÉN heredarán de ella

      B) HEREDAR del existente
         → hereda_de: "ArchivoExistente"
         → Extender funcionalidad, no duplicar

      C) REFACTORIZAR PRIMERO
         → hereda_de: "REFACTORIZAR_PRIMERO"
         → Explicar qué refactorizar antes de crear nuevo

   ❌ PROHIBIDO:
      - Elegir "ninguno" o "copiar y adaptar"
      - Mover funciones a utils/helpers (es un PARCHE, no arquitectura)
      - Continuar sin resolver la duplicación

   💡 PREGÚNTATE: "Si mañana cambio el estilo de tabs, ¿tendré que
      modificar 1 archivo (base) o N archivos (duplicados)?"

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📢 DESPUÉS DE ANALIZAR: EXPLICA Y PREGUNTA AL USUARIO
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   4. EXPLICA al usuario tus conclusiones:
      - Qué código está duplicado y por qué
      - Cuál es tu recomendación (A, B o C) y por qué

   5. USA AskUserQuestion para que el usuario DECIDA:
      - Presenta las opciones A, B, C
      - Añade opción D: "Ignorar (tengo una razón válida)"

   6. USA la respuesta del usuario en q4:
      - Si A → hereda_de: "BaseNueva"
      - Si B → hereda_de: "ClaseExistente"
      - Si C → hereda_de: "REFACTORIZAR_PRIMERO"
      - Si D → justificación: "USUARIO: [razón que dio el usuario]"

   NO continues sin la confirmación del usuario.

"""
            elif nivel == "medio":
                response += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ATENCIÓN CLAUDE - Similitud detectada
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ANTES de continuar, evalúa honestamente:

   • ¿El código que voy a escribir será >50% similar al existente?
   • Si copio y adapto, ¿estoy creando deuda técnica?
   • ¿Puedo HEREDAR del existente en lugar de duplicar?
   • ¿Debería EXTRAER base común primero?

   Si la respuesta a cualquiera es SÍ → trata como nivel ALTO

   📢 EXPLICA al usuario tu análisis y USA AskUserQuestion
      para confirmar cómo proceder antes de continuar.

"""
        else:
            response += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IA: EVALÚA estos resultados y decide:
   • ¿Hay DOCUMENTACIÓN con instrucciones a seguir?
   • ¿Puedo REUTILIZAR algún código directamente?
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


async def step4_herencia(hereda_de: str, reutiliza: str, justificacion: str,
                          decision_usuario: bool = False, justificacion_salto: str = None,
                          usuario_verifico: bool = False) -> str:
    """PASO 4: ¿Se actualizan las instancias?"""

    # Verificar paso anterior
    if not SESSION_STATE["step_3"]:
        resultado = manejar_decision_usuario(
            "philosophy_q3_buscar", "philosophy_q4_herencia",
            decision_usuario, justificacion_salto, usuario_verifico
        )
        if resultado is not None:
            return resultado
        SESSION_STATE["step_3"] = True

    # VALIDAR COHERENCIA CON DETECCIÓN DE DUPLICACIÓN
    duplicacion = SESSION_STATE.get("duplication_detected") or {}
    es_duplicacion = duplicacion.get("es_duplicacion", False)
    nivel_dup = duplicacion.get("nivel", None)

    # Normalizar respuestas
    hereda_lower = hereda_de.lower().strip()
    reutiliza_lower = reutiliza.lower().strip()
    justificacion_strip = justificacion.strip() if justificacion else ""

    # Detectar si está evitando la decisión
    evita_decision = hereda_lower in ["ninguno", "ninguna", "none", "no", "n/a", "-", ""]
    no_reutiliza = reutiliza_lower in ["ninguno", "ninguna", "none", "no", "n/a", "-", ""]

    # Detectar si el USUARIO decidió ignorar (debe tener palabra clave)
    palabras_clave_usuario = ["USUARIO:", "USER:", "DECISIÓN_USUARIO:", "IGNORAR:"]
    usuario_decidio_ignorar = any(justificacion_strip.upper().startswith(kw) for kw in palabras_clave_usuario)

    # BLOQUEAR si hay duplicación ALTA, evita decisión Y no es decisión del usuario
    if es_duplicacion and nivel_dup == "alto" and evita_decision and no_reutiliza:
        if not usuario_decidio_ignorar:
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ BLOQUEADO: DECISIÓN INCOHERENTE CON DUPLICACIÓN DETECTADA    ║
╚══════════════════════════════════════════════════════════════════╝

En el PASO 3 se detectó DUPLICACIÓN NIVEL ALTO:
   • Patrones: {', '.join(duplicacion.get('patrones_comunes', []))}
   • Recomendación: {duplicacion.get('recomendacion', 'N/A')}

Tu respuesta actual:
   • hereda_de: "{hereda_de}"
   • reutiliza_existente: "{reutiliza}"

⛔ ESTO NO ES ACEPTABLE

Cuando hay duplicación alta, DEBES elegir UNA de estas opciones:

   A) hereda_de: "NombreClaseBase" (crear o usar base existente)
   B) hereda_de: "ClaseExistente" + justificar extensión
   C) hereda_de: "REFACTORIZAR_PRIMERO" + explicar qué refactorizar
   D) hereda_de: "ninguno" + justificación que empiece con "USUARIO:"
      → Solo si el usuario DECIDIÓ ignorar la duplicación

❌ Tu justificación NO empieza con palabra clave de usuario.
   Palabras clave válidas: {', '.join(palabras_clave_usuario)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 VUELVE A LLAMAR philosophy_q4_herencia con:
   - Una decisión válida (A, B o C), O
   - justificación que empiece con "USUARIO: [razón del usuario]"
"""

    # ADVERTIR si el usuario decidió ignorar duplicación alta
    advertencia = ""
    if es_duplicacion and nivel_dup == "alto" and evita_decision and usuario_decidio_ignorar:
        advertencia = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ USUARIO DECIDIÓ IGNORAR DUPLICACIÓN ALTA

   Razón: {justificacion_strip}

   ⚠️ Si esto genera deuda técnica, el usuario es responsable.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # ADVERTIR si hay duplicación MEDIA y evita decisión
    if es_duplicacion and nivel_dup == "medio" and evita_decision and not advertencia:
        advertencia = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ADVERTENCIA: Se detectó duplicación MEDIA pero elegiste no heredar.

   Tu justificación: {justificacion}

   Asegúrate de que esto NO resulte en código duplicado.
   Si más tarde necesitas cambiar estilos/comportamiento, tendrás
   que modificar MÚLTIPLES archivos en lugar de UNA base.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    SESSION_STATE["step_4"] = True

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 4/9: HERENCIA                                              ║
║  Pregunta: ¿Si cambio la base, se actualizarán las instancias?   ║
╚══════════════════════════════════════════════════════════════════╝

🔗 HEREDA DE: {hereda_de}

♻️ REUTILIZA EXISTENTE: {reutiliza}

💡 JUSTIFICACIÓN: {justificacion}
{advertencia}
✅ PASO 4 COMPLETADO

➡️ SIGUIENTE: Usa philosophy_q5_nivel
   Pregunta: ¿Está en el nivel correcto de la jerarquía?
"""
    return response


# ============================================================
# VALIDACIÓN DE NIVEL POR COMPORTAMIENTO
# ============================================================

# Palabras clave que indican comportamiento de cada nivel
NIVEL_KEYWORDS = {
    "pieza": ["una sola cosa", "atómico", "mínimo", "único", "single", "una cosa", "único propósito"],
    "componente": ["combina piezas", "agrupa", "ui elements", "junta", "combina", "elementos ui", "piezas de ui"],
    "contenedor": ["orquesta", "coordina", "sistema", "reutilizable", "lógica", "gestiona", "maneja"],
    "pantalla": ["vista", "screen", "usuario ve", "pantalla única", "vista única", "interfaz usuario"],
    "estructura": ["proyecto", "main", "aplicación", "completo", "entrada principal"]
}

# Palabras que son INCOMPATIBLES con cada nivel (detectar errores obvios)
NIVEL_INCOMPATIBLE = {
    "pieza": ["coordina", "orquesta", "sistemas", "pantallas", "gestiona varios"],
    "componente": ["coordina sistemas", "orquesta componentes", "gestiona pantallas"],
    "contenedor": ["vista única", "usuario ve directamente", "pantalla principal"],
    "pantalla": ["atómico", "una sola cosa mínima", "pieza básica"],
    "estructura": []
}


def validar_comportamiento_nivel(nivel: str, justificacion: str) -> tuple:
    """
    Valida si la justificación corresponde al comportamiento del nivel.
    Retorna: (es_valido, mensaje, nivel_sugerido)
    """
    justificacion_lower = justificacion.lower()

    # Verificar palabras incompatibles (errores obvios)
    for palabra in NIVEL_INCOMPATIBLE.get(nivel, []):
        if palabra in justificacion_lower:
            # Buscar qué nivel sería el correcto
            for otro_nivel, keywords in NIVEL_KEYWORDS.items():
                if otro_nivel != nivel:
                    for kw in keywords:
                        if kw in justificacion_lower:
                            return (False, f"La justificación indica '{palabra}' que es incompatible con {nivel}.", otro_nivel)
            return (False, f"La justificación indica '{palabra}' que es incompatible con {nivel}.", None)

    # Verificar que hay al menos alguna palabra clave del nivel
    keywords_nivel = NIVEL_KEYWORDS.get(nivel, [])
    tiene_keyword = any(kw in justificacion_lower for kw in keywords_nivel)

    if not tiene_keyword:
        # No es un error, solo una advertencia suave
        return (True, "No se detectaron palabras clave típicas del nivel, pero se acepta la justificación.", None)

    return (True, "Comportamiento validado.", None)


def get_suggested_filename(nivel: str, current_filename: str, language: str) -> str:
    """Genera el nombre de archivo sugerido según nomenclatura"""
    import os
    basename = os.path.basename(current_filename)
    name_without_ext = os.path.splitext(basename)[0]
    ext = os.path.splitext(basename)[1] or (".gd" if language == "godot" else ".py")

    # Quitar sufijos comunes que no son de la nomenclatura
    for suffix in ["_panel", "_dialog", "_popup", "_view", "_controller", "_manager", "_handler", "_base"]:
        if name_without_ext.endswith(suffix):
            name_without_ext = name_without_ext[:-len(suffix)]
            break

    suffixes = {
        "godot": {"pieza": "_piece", "componente": "_component", "contenedor": "_system", "pantalla": "_screen"},
        "python": {"pieza": "_piece", "componente": "_component", "contenedor": "_system", "pantalla": "_screen"},
        "web": {"pieza": "_atom", "componente": "_molecule", "contenedor": "_organism", "pantalla": "_template"}
    }

    suffix = suffixes.get(language, suffixes["python"]).get(nivel, "")
    return f"{name_without_ext}{suffix}{ext}"


async def step5_nivel(nivel: str, filename: str, justificacion: str,
                       decision_usuario: bool = False, justificacion_salto: str = None,
                       usuario_verifico: bool = False) -> str:
    """PASO 5: ¿Está en el nivel correcto de la jerarquía?

    Valida el COMPORTAMIENTO del código (según justificación), no solo el nombre.
    El nivel se determina por lo que HACE el código, no por cómo se llama el archivo.
    """

    # Verificar paso anterior
    if not SESSION_STATE["step_4"]:
        resultado = manejar_decision_usuario(
            "philosophy_q4_herencia", "philosophy_q5_nivel",
            decision_usuario, justificacion_salto, usuario_verifico
        )
        if resultado is not None:
            return resultado
        SESSION_STATE["step_4"] = True

    language = SESSION_STATE.get("current_language", "godot")
    change_type = SESSION_STATE.get("current_change_type", "nuevo")

    # 1. VALIDAR COMPORTAMIENTO (principal)
    comportamiento_ok, comportamiento_msg, nivel_sugerido = validar_comportamiento_nivel(nivel, justificacion)

    if not comportamiento_ok:
        sugerencia = f"\n💡 Nivel sugerido: {nivel_sugerido.upper()}" if nivel_sugerido else ""
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: NIVEL INCORRECTO                                      ║
║  El nivel se determina por el COMPORTAMIENTO del código          ║
╚══════════════════════════════════════════════════════════════════╝

📊 NIVEL INDICADO: {nivel.upper()}
📄 ARCHIVO: {filename}

❌ {comportamiento_msg}
{sugerencia}

COMPORTAMIENTO POR NIVEL:
   • Pieza      → Hace UNA sola cosa atómica
   • Componente → Combina piezas
   • Contenedor → Orquesta componentes, lógica reutilizable
   • Pantalla   → Vista única del usuario
   • Estructura → Proyecto completo

🚫 CORRIGE EL NIVEL SEGÚN EL COMPORTAMIENTO DEL CÓDIGO
"""

    # 2. VERIFICAR NOMENCLATURA (secundario)
    nomenclatura_ok = True
    suggested_name = None

    if language in PHILOSOPHY["naming"]:
        pattern = PHILOSOPHY["naming"][language].get(nivel)
        if pattern and not re.search(pattern, filename):
            nomenclatura_ok = False
            suggested_name = get_suggested_filename(nivel, filename, language)

    # 3. Para código NUEVO: exigir nomenclatura (a menos que usuario verifique)
    if change_type == "nuevo" and not nomenclatura_ok and not usuario_verifico:
        nomenclatura_key = "decision_nomenclatura_q5"
        if decision_usuario and justificacion_salto:
            SESSION_STATE["decision_pendiente"][nomenclatura_key] = justificacion_salto
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️ NOMENCLATURA - REQUIERE VERIFICACIÓN DEL USUARIO             ║
╚══════════════════════════════════════════════════════════════════╝

📄 ARCHIVO: {filename}
💡 NOMBRE SUGERIDO: {suggested_name}

📝 Tu justificación: "{justificacion_salto}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 INSTRUCCIÓN OBLIGATORIA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASO 1: Presenta al usuario tu justificación y el nombre sugerido
PASO 2: USA AskUserQuestion:
   "¿Aceptas usar '{filename}' en vez de '{suggested_name}'?"
   - "Sí, mantener nombre" → Llama con usuario_verifico=true
   - "No, usar sugerido" → Usa el nombre sugerido

⛔ La pregunta es el FINAL del turno.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: NOMENCLATURA NO VÁLIDA (código nuevo)                 ║
╚══════════════════════════════════════════════════════════════════╝

📊 NIVEL: {nivel.upper()} - ✅ Comportamiento correcto
📄 ARCHIVO: {filename}

❌ Para código NUEVO debes usar la nomenclatura correcta.

💡 NOMBRE SUGERIDO: {suggested_name}

NOMENCLATURA CORRECTA:
   • Pieza      → *_piece.(gd|tscn) | pieces/*.py
   • Componente → *_component.(gd|tscn) | components/*.py
   • Contenedor → *_system.(gd|tscn) | systems/*.py
   • Pantalla   → *_screen.(gd|tscn) | screens/*.py

🚫 USA EL NOMBRE SUGERIDO
"""

    # 4. GUARDAR ESTADO - El nivel es válido
    SESSION_STATE["step_5"] = True
    SESSION_STATE["current_level"] = nivel
    SESSION_STATE["current_filename"] = filename

    # 5. CONSTRUIR RESPUESTA
    if nomenclatura_ok:
        response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 5/8: NIVEL CORRECTO                                        ║
║  "El nivel es el COMPORTAMIENTO, el nombre es la ETIQUETA"       ║
╚══════════════════════════════════════════════════════════════════╝

📊 NIVEL: {nivel.upper()} - {PHILOSOPHY['levels'].get(nivel, '')}

📄 ARCHIVO: {filename}

💡 JUSTIFICACIÓN: {justificacion}

✅ COMPORTAMIENTO VALIDADO
✅ NOMENCLATURA CORRECTA
✅ PASO 5 COMPLETADO
"""
    else:
        # Nomenclatura no coincide = deuda técnica de naming
        response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 5/8: NIVEL CORRECTO                                        ║
║  "El nivel es el COMPORTAMIENTO, el nombre es la ETIQUETA"       ║
╚══════════════════════════════════════════════════════════════════╝

📊 NIVEL: {nivel.upper()} - {PHILOSOPHY['levels'].get(nivel, '')}

📄 ARCHIVO: {filename}

💡 JUSTIFICACIÓN: {justificacion}

✅ COMPORTAMIENTO VALIDADO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ DEUDA TÉCNICA: Naming
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📛 ACTUAL:    {filename}
   💡 SUGERIDO:  {suggested_name}

   📋 MOTIVO: Archivo existente con dependencias.
   🔧 MEJORA FUTURA: Renombrar en refactor global.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PASO 5 COMPLETADO (nivel validado, naming documentado)
"""

    response += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 RESUMEN DE DISEÑO:
   • Descripción: {SESSION_STATE.get('current_description', 'N/A')}
   • Tipo: {change_type}
   • Nivel: {nivel}
   • Archivo: {filename}
   • Lenguaje: {language}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

➡️ SIGUIENTE:
   PASO 6: Usa philosophy_q6_verificar_dependencias
   (Lista las funciones externas que vas a llamar)
"""
    return response


def extraer_propiedades_referencia(content: str, lines: list, must_document: list, language: str) -> dict:
    """Extrae propiedades específicas de código de referencia.

    Args:
        content: Contenido completo del archivo
        lines: Lista de líneas del contenido (o subset si se especificó rango)
        must_document: Lista de propiedades a buscar
        language: Lenguaje del código

    Returns:
        dict con propiedades encontradas y faltantes
    """
    found = {}
    missing = []

    # Unir líneas para búsqueda
    text = '\n'.join(lines)

    for prop in must_document:
        # Patrones de búsqueda según lenguaje
        if language == "godot":
            # Buscar en código GDScript: propiedad = valor
            patterns = [
                rf'{re.escape(prop)}\s*=\s*([^\n]+)',  # variable = valor
                rf'\.{re.escape(prop)}\s*=\s*([^\n]+)',  # .propiedad = valor
            ]
            # Buscar en .tscn: propiedad = valor
            patterns.append(rf'{re.escape(prop)}\s*=\s*([^\n]+)')
        elif language == "python":
            patterns = [
                rf'{re.escape(prop)}\s*=\s*([^\n]+)',  # variable = valor
                rf'self\.{re.escape(prop)}\s*=\s*([^\n]+)',  # self.prop = valor
            ]
        else:
            patterns = [
                rf'{re.escape(prop)}\s*[=:]\s*([^\n,}}]+)',  # prop = valor o prop: valor
            ]

        value_found = None
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value_found = match.group(1).strip().rstrip(',').rstrip(';')
                break

        if value_found:
            found[prop] = value_found
        else:
            missing.append(prop)

    return {
        "found": found,
        "missing": missing,
        "total_requested": len(must_document),
        "total_found": len(found)
    }


async def step6_verificar_dependencias(project_path: str, dependencies: list = None, references: list = None,
                                        removed_functions: list = None, source_file: str = None,
                                        decision_usuario: bool = False, justificacion_salto: str = None,
                                        usuario_verifico: bool = False) -> str:
    """PASO 6: Verificar dependencias externas y referencias antes de escribir código"""

    # Verificar paso anterior
    if not SESSION_STATE["step_5"]:
        resultado = manejar_decision_usuario(
            "philosophy_q5_nivel", "philosophy_q6_verificar_dependencias",
            decision_usuario, justificacion_salto, usuario_verifico
        )
        if resultado is not None:
            return resultado
        SESSION_STATE["step_5"] = True

    path = Path(project_path).expanduser().resolve()

    if not path.exists():
        return f"Error: El directorio {project_path} no existe"

    language = SESSION_STATE.get("current_language", "godot")

    # Inicializar listas si son None
    if dependencies is None:
        dependencies = []
    if references is None:
        references = []
    if removed_functions is None:
        removed_functions = []

    verified = []
    issues = []

    # Procesar dependencias (funciones)
    for dep in dependencies:
        file_rel = dep.get("file", "")
        func_name = dep.get("function", "")
        expected_params = dep.get("expected_params", "")
        expected_return = dep.get("expected_return", "")

        file_path = path / file_rel

        # Verificar que el archivo existe
        if not file_path.exists():
            issues.append({
                "type": "FILE_NOT_FOUND",
                "file": file_rel,
                "function": func_name,
                "message": f"❌ Archivo no existe: {file_rel}"
            })
            continue

        # Leer contenido
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            issues.append({
                "type": "READ_ERROR",
                "file": file_rel,
                "function": func_name,
                "message": f"❌ Error leyendo archivo: {e}"
            })
            continue

        # Buscar la función según lenguaje
        if language == "godot":
            # Buscar: [static] func nombre_funcion(params) -> return:
            pattern = rf'^(?:static\s+)?func\s+{re.escape(func_name)}\s*\(([^)]*)\)(?:\s*->\s*(\w+))?'
        elif language == "python":
            # Buscar: [async] def nombre_funcion(params) -> return:
            pattern = rf'^(?:async\s+)?def\s+{re.escape(func_name)}\s*\(([^)]*)\)(?:\s*->\s*(\w+))?'
        else:
            pattern = rf'function\s+{re.escape(func_name)}\s*\(([^)]*)\)'

        match = re.search(pattern, content, re.MULTILINE)

        if not match:
            issues.append({
                "type": "FUNC_NOT_FOUND",
                "file": file_rel,
                "function": func_name,
                "message": f"❌ Función no encontrada: {func_name} en {file_rel}"
            })
            continue

        # Extraer firma real
        real_params = match.group(1).strip() if match.group(1) else ""
        real_return = match.group(2) if len(match.groups()) > 1 and match.group(2) else "void"

        # Comparar si se especificaron expectativas
        param_match = True
        return_match = True

        if expected_params:
            # Normalizar para comparar (quitar espacios extra)
            norm_expected = re.sub(r'\s+', ' ', expected_params.strip())
            norm_real = re.sub(r'\s+', ' ', real_params.strip())
            param_match = norm_expected.lower() == norm_real.lower()

        if expected_return:
            return_match = expected_return.lower() == real_return.lower()

        if not param_match or not return_match:
            issues.append({
                "type": "SIGNATURE_MISMATCH",
                "file": file_rel,
                "function": func_name,
                "expected_params": expected_params,
                "real_params": real_params,
                "expected_return": expected_return,
                "real_return": real_return,
                "message": f"❌ Firma no coincide: {func_name}"
            })
        else:
            verified.append({
                "file": file_rel,
                "function": func_name,
                "params": real_params,
                "return": real_return
            })

    # Verificar funciones eliminadas (dirección inversa: ¿quién me llama?)
    import subprocess
    import shutil

    removed_refs = []  # Archivos que llaman a funciones eliminadas
    extensions = [".gd", ".tscn", ".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".vue"]
    rg_available = shutil.which("rg") is not None

    # Normalizar source_file para exclusión
    source_file_resolved = None
    if source_file:
        source_file_resolved = (path / source_file).resolve()

    for func_name in removed_functions:
        callers = []  # Archivos que llaman a esta función

        if rg_available:
            try:
                glob_args = []
                for ext in extensions:
                    glob_args.extend(["--glob", f"*{ext}"])
                result = subprocess.run(
                    ["rg", "-n", "--glob", "!.git", "--glob", "!__pycache__", "--glob", "!addons"] + glob_args + [func_name],
                    capture_output=True, text=True, cwd=str(path), timeout=30
                )
                for line in result.stdout.splitlines():
                    # Formato rg -n: archivo:linea:contenido
                    parts = line.split(":", 2)
                    if len(parts) >= 3:
                        file_found = parts[0]
                        line_num = parts[1]
                        line_content = parts[2].strip()
                        file_resolved = (path / file_found).resolve()
                        # Excluir source_file
                        if source_file_resolved and file_resolved == source_file_resolved:
                            continue
                        callers.append({
                            "file": file_found,
                            "line": line_num,
                            "content": line_content
                        })
            except (subprocess.TimeoutExpired, Exception):
                pass
        else:
            # Fallback: Python
            for ext in extensions:
                for file in path.rglob(f"*{ext}"):
                    if ".git" in str(file) or "__pycache__" in str(file) or "addons" in str(file):
                        continue
                    if source_file_resolved and file.resolve() == source_file_resolved:
                        continue
                    try:
                        content = file.read_text(encoding='utf-8', errors='ignore')
                        for i, line in enumerate(content.split('\n'), 1):
                            if func_name in line:
                                callers.append({
                                    "file": str(file.relative_to(path)),
                                    "line": str(i),
                                    "content": line.strip()
                                })
                    except:
                        pass

        if callers:
            removed_refs.append({
                "function": func_name,
                "callers": callers
            })

    # Guardar en SESSION_STATE para validate
    SESSION_STATE["removed_functions_refs"] = removed_refs

    # Si hay llamadas externas a funciones eliminadas → BLOQUEAR
    if removed_refs:
        response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ BLOQUEO: FUNCIONES ELIMINADAS CON LLAMADAS EXTERNAS          ║
║  "Verificar ANTES de escribir, no DESPUÉS de fallar"             ║
╚══════════════════════════════════════════════════════════════════╝

Las siguientes funciones se van a eliminar/mover, pero otros archivos las llaman:

"""
        for ref in removed_refs:
            response += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            response += f"❌ {ref['function']}() — {len(ref['callers'])} referencia(s) externa(s):\n\n"
            for caller in ref['callers']:
                response += f"   📄 {caller['file']}:{caller['line']}\n"
                response += f"      {caller['content']}\n\n"

        response += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚫 NO PUEDES CONTINUAR hasta contemplar estos archivos en tu diseño.

Opciones:
1. Añadir wrappers/delegadores en el archivo original para mantener la interfaz pública
2. Actualizar los archivos que llaman a estas funciones
3. Ambas según el caso

DEBES explicar al usuario qué archivos se romperían y proponer solución ANTES de escribir código.
"""
        return response

    # Warning si es refactor y no se pasaron removed_functions
    refactor_warning = None
    tipo_cambio = SESSION_STATE.get("current_change_type", "")
    if tipo_cambio == "refactor" and not removed_functions:
        refactor_warning = "⚠️ Estás haciendo un refactor pero no indicaste removed_functions. ¿Estás eliminando/moviendo funciones del archivo original? Si es así, vuelve a llamar q6 con removed_functions para verificar quién las llama."

    # Procesar referencias (código a replicar)
    extracted_references = []
    reference_warnings = []

    for ref in references:
        file_rel = ref.get("file", "")
        start_line = ref.get("start_line")
        end_line = ref.get("end_line")
        search_pattern = ref.get("search_pattern")
        must_document = ref.get("must_document", [])

        file_path_ref = path / file_rel

        # Verificar que el archivo existe
        if not file_path_ref.exists():
            reference_warnings.append({
                "file": file_rel,
                "message": f"⚠️ Archivo de referencia no existe: {file_rel}"
            })
            continue

        # Leer contenido
        try:
            content = file_path_ref.read_text(encoding='utf-8', errors='ignore')
            all_lines = content.split('\n')
        except Exception as e:
            reference_warnings.append({
                "file": file_rel,
                "message": f"⚠️ Error leyendo archivo de referencia: {e}"
            })
            continue

        # Determinar líneas a analizar
        if start_line and end_line:
            # Rango específico (1-indexed)
            lines_to_analyze = all_lines[start_line - 1:end_line]
            line_range = f"{start_line}-{end_line}"
        elif search_pattern:
            # Buscar patrón y extraer contexto
            lines_to_analyze = []
            line_range = "patrón encontrado"
            for i, line in enumerate(all_lines):
                if re.search(search_pattern, line, re.IGNORECASE):
                    # Extraer contexto: 5 líneas antes y 15 después
                    start_idx = max(0, i - 5)
                    end_idx = min(len(all_lines), i + 15)
                    lines_to_analyze = all_lines[start_idx:end_idx]
                    line_range = f"{start_idx + 1}-{end_idx}"
                    break
            if not lines_to_analyze:
                reference_warnings.append({
                    "file": file_rel,
                    "message": f"⚠️ Patrón '{search_pattern}' no encontrado en {file_rel}"
                })
                continue
        else:
            # Todo el archivo
            lines_to_analyze = all_lines
            line_range = "completo"

        # Extraer propiedades
        extraction = extraer_propiedades_referencia(content, lines_to_analyze, must_document, language)

        extracted_references.append({
            "file": file_rel,
            "line_range": line_range,
            "found": extraction["found"],
            "missing": extraction["missing"],
            "must_document": must_document
        })

        if extraction["missing"]:
            reference_warnings.append({
                "file": file_rel,
                "message": f"⚠️ Propiedades no encontradas en {file_rel}: {', '.join(extraction['missing'])}"
            })

    # Guardar en SESSION_STATE para que validate las use
    SESSION_STATE["reference_properties"] = extracted_references

    # Construir respuesta
    if issues:
        response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: DEPENDENCIAS NO VÁLIDAS                               ║
║  "Verificar ANTES de escribir, no DESPUÉS de fallar"             ║
╚══════════════════════════════════════════════════════════════════╝

❌ DISCREPANCIAS ENCONTRADAS: {len(issues)}

"""
        for issue in issues:
            response += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            response += f"{issue['message']}\n"
            response += f"   Archivo: {issue.get('file', 'N/A')}\n"
            response += f"   Función: {issue.get('function', 'N/A')}\n"

            if issue['type'] == 'SIGNATURE_MISMATCH':
                response += f"\n   ESPERADO: {issue['function']}({issue.get('expected_params', '')}) -> {issue.get('expected_return', 'void')}\n"
                response += f"   REAL:     {issue['function']}({issue.get('real_params', '')}) -> {issue.get('real_return', 'void')}\n"

            response += "\n"

        if verified:
            response += f"\n✅ Dependencias verificadas correctamente: {len(verified)}\n"
            for v in verified:
                response += f"   • {v['file']}:{v['function']}({v['params']}) -> {v['return']}\n"

        response += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚫 NO PUEDES CONTINUAR hasta resolver las discrepancias.

Opciones:
1. Corregir las llamadas para usar las firmas reales
2. Modificar las funciones destino si es necesario
3. Volver a ejecutar este paso con las correcciones
"""
        return response

    # Todo OK
    SESSION_STATE["step_6"] = True
    SESSION_STATE["verified_dependencies"] = verified

    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 6/8: VERIFICACIÓN DE DEPENDENCIAS                          ║
║  "Verificar ANTES de escribir, no DESPUÉS de fallar"             ║
╚══════════════════════════════════════════════════════════════════╝

"""
    # Mostrar dependencias verificadas
    if verified:
        response += f"✅ DEPENDENCIAS VERIFICADAS: {len(verified)}\n\n"
        for v in verified:
            response += f"   ✓ {v['file']}:{v['function']}({v['params']}) -> {v['return']}\n"
        response += "\n"

    # Mostrar referencias extraídas (NUEVO)
    if extracted_references:
        response += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 REFERENCIAS ANALIZADAS (código a replicar): {len(extracted_references)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for ref in extracted_references:
            response += f"📄 {ref['file']} (líneas: {ref['line_range']})\n"
            if ref['found']:
                response += "   Propiedades encontradas:\n"
                for prop, value in ref['found'].items():
                    response += f"   • {prop} = {value}\n"
            if ref['missing']:
                response += f"   ⚠️ No encontradas: {', '.join(ref['missing'])}\n"
            response += "\n"

        response += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ DEBES replicar TODAS estas propiedades en tu código.
   validate (paso 8) verificará que las hayas incluido.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # Mostrar funciones eliminadas verificadas (sin llamadas externas)
    if removed_functions and not removed_refs:
        response += f"\n✅ FUNCIONES ELIMINADAS VERIFICADAS: {len(removed_functions)}\n"
        for func in removed_functions:
            response += f"   ✓ {func}() — sin llamadas externas\n"
        response += "\n"

    # Mostrar advertencias de referencias
    if reference_warnings:
        response += "\n⚠️ ADVERTENCIAS DE REFERENCIAS:\n"
        for warn in reference_warnings:
            response += f"   {warn['message']}\n"
        response += "\n"

    # Mostrar warning de refactor sin removed_functions
    if refactor_warning:
        response += f"\n{refactor_warning}\n"

    response += f"""
✅ PASO 6 COMPLETADO

➡️ SIGUIENTE:
   PASO 7: Escribe el código usando las firmas verificadas
   PASO 8: Usa philosophy_validate para validar
"""
    return response


async def step8_validate(code: str = None, filename: str = None, file_path: str = None,
                          usuario_confirmo_warnings: bool = False, decision_usuario: bool = False,
                          justificacion_salto: str = None, usuario_verifico: bool = False) -> str:
    """PASO 8: Validar código escrito"""

    # Resolver código desde file_path si no se pasó code
    if file_path:
        import os
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            return f"❌ No se pudo leer el archivo: {file_path}\nError: {e}"
        if not filename:
            filename = os.path.basename(file_path)

    if not code:
        return "❌ Debes proporcionar `code` o `file_path`."

    if not filename:
        return "❌ Debes proporcionar `filename` o `file_path`."

    # Verificar paso anterior (ahora requiere step_6)
    if not SESSION_STATE["step_6"]:
        resultado = manejar_decision_usuario(
            "pasos 1-6", "philosophy_validate",
            decision_usuario, justificacion_salto, usuario_verifico
        )
        if resultado is not None:
            return resultado
        SESSION_STATE["step_6"] = True

    language = SESSION_STATE.get("current_language", "godot")
    issues = []
    warnings = []

    lines = code.split('\n')

    # ===============================================================
    # RAMA ESPECIAL: Archivos .tscn/.tres (escenas Godot)
    # ===============================================================
    is_tscn = filename.endswith('.tscn') or filename.endswith('.tres')

    if is_tscn:
        # 1. DRY: Detectar SubResources duplicados (mismo tipo + propiedades similares)
        sub_resources = {}
        current_sub = None
        current_props = []

        for line in lines:
            sub_match = re.match(r'\[sub_resource\s+type="(\w+)"\s+id="([^"]+)"\]', line)
            if sub_match:
                if current_sub:
                    sub_resources[current_sub[1]] = {"type": current_sub[0], "props": current_props}
                current_sub = (sub_match.group(1), sub_match.group(2))
                current_props = []
            elif current_sub and '=' in line and not line.startswith('['):
                current_props.append(line.strip())

        if current_sub:
            sub_resources[current_sub[1]] = {"type": current_sub[0], "props": current_props}

        # Comparar SubResources del mismo tipo
        by_type = {}
        for sub_id, data in sub_resources.items():
            by_type.setdefault(data["type"], []).append((sub_id, data["props"]))

        for type_name, subs in by_type.items():
            if len(subs) < 2:
                continue
            for i in range(len(subs)):
                for j in range(i + 1, len(subs)):
                    props_i = set(subs[i][1])
                    props_j = set(subs[j][1])
                    if props_i and props_j and props_i == props_j:
                        issues.append(
                            f"❌ DRY: SubResources '{subs[i][0]}' y '{subs[j][0]}' "
                            f"(tipo {type_name}) son idénticos. Reutiliza uno solo."
                        )
                    elif props_i and props_j:
                        common = props_i & props_j
                        total = props_i | props_j
                        if total and len(common) / len(total) > 0.8:
                            warnings.append(
                                f"⚠️ DRY: SubResources '{subs[i][0]}' y '{subs[j][0]}' "
                                f"(tipo {type_name}) tienen >80% propiedades iguales."
                            )

        # 2. DRY: Detectar estilos/overrides repetidos en nodos
        node_overrides = {}
        current_node = None

        for line in lines:
            node_match = re.match(r'\[node\s+name="([^"]+)"', line)
            if node_match:
                current_node = node_match.group(1)
                node_overrides[current_node] = []
            elif current_node and line.startswith('theme_override_'):
                node_overrides[current_node].append(line.strip())

        # Buscar nodos con overrides idénticos
        override_groups = {}
        for node_name, overrides in node_overrides.items():
            if overrides:
                key = tuple(sorted(overrides))
                override_groups.setdefault(key, []).append(node_name)

        for key, nodes in override_groups.items():
            if len(nodes) >= 3:
                warnings.append(
                    f"⚠️ DRY: {len(nodes)} nodos ({', '.join(nodes[:3])}...) "
                    f"tienen los mismos theme_overrides. Considera usar un Theme."
                )

        # 3. Detectar colores hardcodeados en nodos
        color_count = 0
        for line in lines:
            if re.search(r'Color\s*\(\s*[\d.]+', line) and 'theme_override' not in line:
                color_count += 1
        if color_count > 3:
            warnings.append(f"⚠️ {color_count} colores hardcodeados. Usa AppTheme o un recurso de tema.")

        # 4. Verificar propiedades de referencia (del paso 6)
        reference_properties = SESSION_STATE.get("reference_properties", [])
        missing_reference_props = []

        for ref in reference_properties:
            ref_file = ref.get("file", "")
            found_props = ref.get("found", {})

            for prop, expected_value in found_props.items():
                patterns = [
                    rf'{re.escape(prop)}\s*=\s*',
                ]
                prop_found = any(re.search(p, code, re.IGNORECASE) for p in patterns)
                if not prop_found:
                    missing_reference_props.append({
                        "property": prop,
                        "expected_value": expected_value,
                        "source_file": ref_file
                    })

        if missing_reference_props:
            warnings.append(f"⚠️ Propiedades de referencia no replicadas ({len(missing_reference_props)}):")
            for mp in missing_reference_props[:5]:
                warnings.append(f"   • {mp['property']} = {mp['expected_value']} (de {mp['source_file']})")

        # Construir respuesta .tscn
        response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 8/9: VALIDACIÓN (.tscn)                                     ║
╚══════════════════════════════════════════════════════════════════╝

📄 ARCHIVO: {filename}
🔧 TIPO: Escena Godot
📏 LÍNEAS: {len(lines)}
📦 SubResources: {len(sub_resources)}

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
            SESSION_STATE["step_8"] = True
            response += "✅ ESCENA APROBADA\n\n"
            response += "La escena cumple con DRY y la filosofía modular.\n\n"
            response += """➡️ PASO 9 (OBLIGATORIO): Usa philosophy_q9_documentar

   "Documentar DESPUÉS de validar"

🚫 El flujo NO está completo hasta documentar.
"""
        elif not issues:
            if usuario_confirmo_warnings:
                SESSION_STATE["step_8"] = True
                response += "✅ ESCENA APROBADA (usuario confirmó ignorar advertencias)\n\n"
                response += """➡️ PASO 9 (OBLIGATORIO): Usa philosophy_q9_documentar

   "Documentar DESPUÉS de validar"

🚫 El flujo NO está completo hasta documentar.
"""
            else:
                response += """⚠️ ESCENA CON ADVERTENCIAS - REQUIERE DECISIÓN DEL USUARIO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 INSTRUCCIÓN OBLIGATORIA PARA CLAUDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASO 1: EXPLICA tu opinión sobre cada advertencia
PASO 2: USA AskUserQuestion
   - "Ignorar y continuar" → philosophy_validate con usuario_confirmo_warnings=true
   - "Corregir primero" → Modifica y vuelve a validar

⛔ La pregunta es el FINAL del turno.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        else:
            response += """🚫 ESCENA NO APROBADA

Corrige los problemas y vuelve a validar.
"""

        return response

    # ===============================================================
    # VALIDACIÓN ESTÁNDAR (código fuente)
    # ===============================================================

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

    # Detectar si es archivo completo o fragmento — bloquear si es fragmento
    is_complete_file = bool(re.search(r'^(extends|class_name|@tool|##|#\s*-|import |from |<!)', code, re.MULTILINE))

    if not is_complete_file:
        SESSION_STATE["step_8"] = False
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 8/9: VALIDACIÓN BLOQUEADA                                  ║
╚══════════════════════════════════════════════════════════════════╝

❌ El código no es un archivo completo.

Sin el archivo completo, la validación no es fiable: no se puede verificar
herencia, estructura, dependencias ni detectar problemas reales.

**Acción:** Lee el archivo con Read y pasa todo su contenido a philosophy_validate.

📄 Archivo: {filename}
"""

    # Validar Q4: signals vs llamadas directas (Godot)
    if language == "godot":
        direct_calls = len(re.findall(r'get_node\(["\']/', code))
        signals = len(re.findall(r'\.emit\(|\.connect\(', code))
        if direct_calls > 3 and signals == 0:
            warnings.append("⚠️ Herencia: Muchas llamadas directas. Usa signals para desacoplar.")

        # Verificar extends (solo si es archivo completo — en fragmentos da falso positivo)
        if is_complete_file and not re.search(r'^extends\s+', code, re.MULTILINE):
            warnings.append("⚠️ Herencia: No hay 'extends'. ¿Debería heredar de algo?")

        # Detectar Color hardcodeado inline (no en constantes ni variables)
        for line in lines:
            stripped = line.strip()
            if re.search(r'Color\s*\(\s*[\d.]+', stripped):
                if not re.match(r'^(const|var|@export)\s+', stripped):
                    issues.append(f"❌ Color hardcodeado inline: `{stripped}`. Usa AppTheme o una constante nombrada.")
                    break

    # Detectar código duplicado (excluir llamadas a helpers: "var x = func()")
    line_counts = {}
    for line in lines:
        stripped = line.strip()
        if len(stripped) > 30 and not stripped.startswith('#') and not stripped.startswith('//'):
            if re.match(r'^var\s+\w+\s*=\s*\w+\(', stripped):
                continue
            line_counts[stripped] = line_counts.get(stripped, 0) + 1

    duplicates = sum(1 for v in line_counts.values() if v >= 3)
    if duplicates > 0:
        issues.append(f"❌ DRY: {duplicates} líneas repetidas 3+ veces. Extrae a función/componente.")

    # Verificar propiedades de referencia (del paso 6)
    reference_properties = SESSION_STATE.get("reference_properties", [])
    missing_reference_props = []

    for ref in reference_properties:
        ref_file = ref.get("file", "")
        found_props = ref.get("found", {})

        for prop, expected_value in found_props.items():
            # Buscar la propiedad en el código escrito
            # Patrones flexibles: prop = valor, .prop = valor, self.prop = valor
            patterns = [
                rf'{re.escape(prop)}\s*=\s*',
                rf'\.{re.escape(prop)}\s*=\s*',
            ]

            prop_found = False
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    prop_found = True
                    break

            if not prop_found:
                missing_reference_props.append({
                    "property": prop,
                    "expected_value": expected_value,
                    "source_file": ref_file
                })

    if missing_reference_props:
        warnings.append(f"⚠️ Propiedades de referencia no replicadas ({len(missing_reference_props)}):")
        for mp in missing_reference_props[:5]:  # Mostrar máx 5
            warnings.append(f"   • {mp['property']} = {mp['expected_value']} (de {mp['source_file']})")
        if len(missing_reference_props) > 5:
            warnings.append(f"   ... y {len(missing_reference_props) - 5} más")

    # Construir respuesta
    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 8/9: VALIDACIÓN                                            ║
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
        SESSION_STATE["step_8"] = True
        response += "✅ CÓDIGO APROBADO\n\n"
        response += "El código cumple con la filosofía modular.\n\n"
        response += """➡️ PASO 9 (OBLIGATORIO): Usa philosophy_q9_documentar

   La herramienta buscará automáticamente:
   - CHANGELOG.md para registrar el cambio
   - README.md si cambia funcionalidad pública
   - Otros docs afectados

   "Documentar DESPUÉS de validar"

🚫 El flujo NO está completo hasta documentar.
"""
    elif not issues:
        # HAY WARNINGS - verificar si usuario ya confirmó
        if usuario_confirmo_warnings:
            # Usuario confirmó ignorar advertencias
            SESSION_STATE["step_8"] = True
            response += "✅ CÓDIGO APROBADO (usuario confirmó ignorar advertencias)\n\n"
            response += """➡️ PASO 9 (OBLIGATORIO): Usa philosophy_q9_documentar

   La herramienta buscará automáticamente:
   - CHANGELOG.md para registrar el cambio
   - README.md si cambia funcionalidad pública
   - Otros docs afectados

   "Documentar DESPUÉS de validar"

🚫 El flujo NO está completo hasta documentar.
"""
        else:
            # Usuario NO ha confirmado - OBLIGAR a explicar y preguntar
            response += """⚠️ CÓDIGO CON ADVERTENCIAS - REQUIERE DECISIÓN DEL USUARIO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 INSTRUCCIÓN OBLIGATORIA PARA CLAUDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASO 1: EXPLICA tu opinión sobre cada advertencia
   El usuario necesita saber QUÉ PIENSAS de las advertencias.
   Para CADA advertencia, explica:
   - ¿Es un problema real o es aceptable en este caso?
   - ¿Por qué crees eso?

   Ejemplo: "La advertencia sobre X creo que [tu opinión y razón]"

PASO 2: USA AskUserQuestion
   Después de explicar, pregunta qué quiere hacer.

   Opciones:
   1. "Ignorar y continuar" - Seguir al paso 9
   2. "Corregir primero" - Modificar el código

DESPUÉS de que el usuario responda:
- Si IGNORA → philosophy_validate con usuario_confirmo_warnings=true
- Si CORRIGE → Modifica y vuelve a validar

🚫 PROHIBIDO:
- Preguntar SIN explicar tu opinión sobre las advertencias
- Decidir por tu cuenta
- Usar frases genéricas sin justificar

EL USUARIO NECESITA TU ANÁLISIS PARA DECIDIR.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        response += """➡️ PASO 9 (OBLIGATORIO): Usa philosophy_q9_documentar

   La herramienta buscará automáticamente:
   - CHANGELOG.md para registrar el cambio
   - README.md si cambia funcionalidad pública
   - Otros docs afectados

   "Documentar DESPUÉS de validar"

🚫 El flujo NO está completo hasta documentar.
"""
    else:
        response += """🚫 CÓDIGO NO APROBADO

Corrige los problemas y vuelve a validar.
El código NO cumple con: "Máximo impacto, menor esfuerzo — a largo plazo"
"""

    return response


async def step9_documentar(
    project_path: str,
    archivos_modificados: list,
    descripcion_cambio: str,
    tipo_cambio: str,
    reemplaza: str = None,
    decision_usuario: bool = False,
    justificacion_salto: str = None,
    usuario_verifico: bool = False,
    descripcion_funcional: str = None
) -> str:
    """PASO 9: Documenta los cambios realizados"""

    # Verificar paso anterior
    if not SESSION_STATE["step_8"]:
        resultado = manejar_decision_usuario(
            "philosophy_validate (paso 8)", "philosophy_q9_documentar",
            decision_usuario, justificacion_salto, usuario_verifico
        )
        if resultado is not None:
            return resultado
        SESSION_STATE["step_8"] = True

    path = Path(project_path).expanduser().resolve()
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    # 1. BUSCAR DOCUMENTOS AFECTADOS
    docs_afectados = []
    changelog_path = None
    readme_path = None

    # Buscar CHANGELOG
    for changelog_loc in [path / "docs" / "CHANGELOG.md", path / "CHANGELOG.md"]:
        if changelog_loc.exists():
            changelog_path = changelog_loc
            break

    # Buscar README
    readme_loc = path / "README.md"
    if readme_loc.exists():
        readme_path = readme_loc

    # Buscar docs que mencionen los archivos modificados
    for archivo in archivos_modificados:
        archivo_name = Path(archivo).stem
        doc_results = search_project_documentation(path, archivo_name)
        for doc in doc_results.get("primary", [])[:3]:  # Top 3 por archivo
            if doc["path"] not in [d["path"] for d in docs_afectados]:
                docs_afectados.append(doc)

    # 2. GENERAR TEMPLATE PARA CHANGELOG
    tipo_label = {
        "añadido": "Añadido",
        "corregido": "Corregido",
        "cambiado": "Cambiado",
        "eliminado": "Eliminado"
    }.get(tipo_cambio, tipo_cambio.capitalize())

    archivos_str = "\n".join([f"   - `{a}`" for a in archivos_modificados])

    funcional = descripcion_funcional or ""
    changelog_template = f"""## [{fecha_hoy}] - {SESSION_STATE.get('current_description', descripcion_cambio)[:50]}

### {tipo_label}
- **Funcionalidad:** {funcional if funcional else '⚠️ FALTA - describe qué cambia para el usuario'}
- **Técnico:** {descripcion_cambio}
- Archivos:
{archivos_str}
"""

    if reemplaza:
        changelog_template += f"""
### Reemplaza/Obsoleta
- {reemplaza}
"""

    # 3. CONSTRUIR RESPUESTA
    response = f"""
╔══════════════════════════════════════════════════════════════════╗
║  PASO 9/9: DOCUMENTACIÓN                                         ║
║  "Documentar DESPUÉS de validar"                                 ║
╚══════════════════════════════════════════════════════════════════╝

📅 FECHA: {fecha_hoy}
📝 CAMBIO: {descripcion_cambio}
📁 ARCHIVOS: {len(archivos_modificados)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CHANGELOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    if changelog_path:
        response += f"""
✅ Encontrado: {changelog_path.relative_to(path) if changelog_path.is_relative_to(path) else changelog_path}

📝 AÑADE esta entrada al inicio del archivo:

```markdown
{changelog_template}```
"""
    else:
        response += f"""
⚠️ No encontrado. Crear en: docs/CHANGELOG.md

📝 Contenido inicial:

```markdown
# Changelog

{changelog_template}```
"""

    # README
    response += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 README
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    if readme_path:
        # Verificar si el cambio afecta funcionalidad pública
        description_lower = descripcion_cambio.lower()
        affects_public = any(word in description_lower for word in
            ["api", "comando", "función", "feature", "nueva", "nuevo", "añad", "interfaz", "herramienta"])

        if affects_public:
            response += f"""
⚠️ El cambio parece afectar funcionalidad pública.
📄 Revisa: {readme_path.relative_to(path) if readme_path.is_relative_to(path) else readme_path}

   Actualiza si es necesario:
   - Descripción de funcionalidades
   - Instrucciones de uso
   - Ejemplos
"""
        else:
            response += """
✅ El cambio parece interno. README probablemente no necesita actualización.
"""
    else:
        response += """
ℹ️ No hay README.md en el proyecto.
"""

    # Otros docs afectados
    if docs_afectados:
        response += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 OTROS DOCS QUE MENCIONAN LOS ARCHIVOS MODIFICADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Revisa si necesitan actualización:

"""
        for doc in docs_afectados[:5]:
            priority_emoji = {"ALTA": "🔥", "MEDIA": "📌", "BAJA": "📎"}.get(doc.get("priority", "BAJA"), "📄")
            response += f"   {priority_emoji} {doc['title']}\n"
            response += f"      📁 {doc['relative_path']}\n"
            if doc.get("relevant_sections"):
                response += f"      📑 Secciones: {', '.join(doc['relevant_sections'][:3])}\n"
            response += "\n"

    response += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PASO 9 COMPLETADO - FLUJO FINALIZADO

   Recuerda actualizar la documentación manualmente.
   El flujo está completo y listo para una nueva tarea.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # Resetear estado para la próxima creación
    reset_state()

    return response


async def show_checklist() -> str:
    """Muestra el checklist completo"""

    current_step = "Ningún flujo activo"
    if SESSION_STATE["step_8"]:
        current_step = "8 completados → Falta: Q9 Documentar"
    elif SESSION_STATE["step_6"]:
        current_step = "6 completados → Listo para escribir código y validar"
    elif SESSION_STATE["step_5"]:
        current_step = "5/6 → Falta: Q6 Verificar dependencias"
    elif SESSION_STATE["step_4"]:
        current_step = "4/6 → Falta: Q5 Nivel"
    elif SESSION_STATE["step_3"]:
        current_step = "3/6 → Falta: Q4 Herencia"
    elif SESSION_STATE["step_2"]:
        current_step = "2/6 → Falta: Q3 Buscar"
    elif SESSION_STATE["step_1"]:
        current_step = "1/6 → Falta: Q2 Reutilización"

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

📋 LAS 6 PREGUNTAS + VALIDACIÓN + DOCUMENTACIÓN (flujo obligatorio):

   {"✅" if SESSION_STATE["step_1"] else "□"} 1. ¿Esta pieza hace UNA sola cosa?
   {"✅" if SESSION_STATE["step_2"] else "□"} 2. ¿Puedo reutilizar esto en otro lugar?
   {"✅" if SESSION_STATE["step_3"] else "□"} 3. ¿Existe algo similar que pueda extender/heredar?
   {"✅" if SESSION_STATE["step_4"] else "□"} 4. ¿Si cambio la base, se actualizarán todas las instancias?
   {"✅" if SESSION_STATE["step_5"] else "□"} 5. ¿Está en el nivel correcto de la jerarquía?
   {"✅" if SESSION_STATE["step_6"] else "□"} 6. ¿Las dependencias externas existen y coinciden?
   {"✅" if SESSION_STATE["step_8"] else "□"} 8. ¿El código está validado?

   "Verificar ANTES de escribir, no DESPUÉS de fallar"
   "Documentar DESPUÉS de validar"

🔧 FLUJO DE HERRAMIENTAS (9 pasos):

   philosophy_q1_responsabilidad           → Paso 1
   philosophy_q2_reutilizacion             → Paso 2
   philosophy_q3_buscar                    → Paso 3
   philosophy_q4_herencia                  → Paso 4
   philosophy_q5_nivel                     → Paso 5
   philosophy_q6_verificar_dependencias    → Paso 6
   [Escribir código]                       → Paso 7
   philosophy_validate                     → Paso 8
   philosophy_q9_documentar                → Paso 9 (OBLIGATORIO)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Si saltas un paso, el MCP bloquea y muestra error.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# ============================================================
# ANÁLISIS ARQUITECTÓNICO - IMPLEMENTACIÓN
# ============================================================

def extract_function_signatures(content: str, language: str) -> list:
    """Extrae las firmas de funciones públicas de un archivo"""
    signatures = []

    if language == "godot":
        # Buscar: [static] func nombre(params) -> tipo:
        # Excluir funciones privadas (empiezan con _)
        pattern = r'^(?:static\s+)?func\s+([a-zA-Z][a-zA-Z0-9_]*)\s*\(([^)]*)\)(?:\s*->\s*(\w+))?'
        for match in re.finditer(pattern, content, re.MULTILINE):
            func_name = match.group(1)
            if not func_name.startswith('_'):  # Solo públicas
                params = match.group(2).strip() if match.group(2) else ""
                return_type = match.group(3) if match.group(3) else "void"
                signatures.append({
                    "name": func_name,
                    "params": params,
                    "return": return_type,
                    "signature": f"{func_name}({params}) -> {return_type}"
                })

    elif language == "python":
        # Buscar: def nombre(params) -> tipo:
        # Excluir funciones privadas (empiezan con _)
        pattern = r'^def\s+([a-zA-Z][a-zA-Z0-9_]*)\s*\(([^)]*)\)(?:\s*->\s*(\w+))?'
        for match in re.finditer(pattern, content, re.MULTILINE):
            func_name = match.group(1)
            if not func_name.startswith('_'):  # Solo públicas
                params = match.group(2).strip() if match.group(2) else ""
                return_type = match.group(3) if match.group(3) else "None"
                signatures.append({
                    "name": func_name,
                    "params": params,
                    "return": return_type,
                    "signature": f"{func_name}({params}) -> {return_type}"
                })

    elif language == "web":
        # Buscar: function nombre(params) o export function nombre(params)
        pattern = r'(?:export\s+)?function\s+([a-zA-Z][a-zA-Z0-9_]*)\s*\(([^)]*)\)'
        for match in re.finditer(pattern, content):
            func_name = match.group(1)
            params = match.group(2).strip() if match.group(2) else ""
            signatures.append({
                "name": func_name,
                "params": params,
                "return": "unknown",
                "signature": f"{func_name}({params})"
            })

    return signatures


def get_file_info(file_path: Path, language: str) -> dict:
    """Extrae información de un archivo de código incluyendo firmas públicas"""
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

        # Extraer firmas de funciones públicas
        public_signatures = extract_function_signatures(content, language)

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
            "nivel_actual": nivel_actual,
            "public_signatures": public_signatures  # NUEVO: firmas públicas
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
            "public_signatures": [],
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


async def architecture_analysis(project_path: str, language: str, project_name: str,
                                 criterios_file_param: str = None) -> str:
    """Inicia el análisis arquitectónico global"""

    path = Path(project_path).expanduser().resolve()

    if not path.exists():
        return f"Error: El directorio {project_path} no existe"

    # Crear directorio .claude si no existe
    claude_dir = path / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Verificar criterios: sesión actual → parámetro explícito → disco
    if SESSION_STATE["step_0"]:
        # q0 completado en esta sesión — criterios en memoria (y disco)
        criterios_file = SESSION_STATE.get("criterios_file", "sesión actual")
    elif criterios_file_param:
        # Claude especificó un archivo de criterios de sesión anterior
        cf_path = Path(criterios_file_param).expanduser().resolve()
        if not cf_path.exists():
            return f"Error: El archivo de criterios {criterios_file_param} no existe"
        criterios_file = str(cf_path)
        SESSION_STATE["step_0"] = True
        SESSION_STATE["criterios_file"] = criterios_file
    else:
        # q0 no se completó en esta sesión — buscar en disco
        criterios_files = sorted(claude_dir.glob("criterios_*.md"), key=lambda f: f.stat().st_mtime, reverse=True)

        if not criterios_files:
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ANÁLISIS BLOQUEADO: FALTAN CRITERIOS                            ║
╚══════════════════════════════════════════════════════════════════╝

❌ No se encontraron criterios acordados.

Usa philosophy_q0_criterios (con project_path="{project_path}") para:

1. Reformular al usuario lo que entiendes de la tarea
2. Acordar: qué se va a hacer, para qué, y qué debe cumplir
3. Confirmar con el usuario (confirmado_por_usuario=true)

El análisis sin criterios claros produce resultados que no se pueden evaluar.
"""

        # Listar archivos encontrados para que Claude identifique el correcto
        lista = "\n".join(f"  - {f.name} → {f}" for f in criterios_files)
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  CRITERIOS ENCONTRADOS EN DISCO                                  ║
╚══════════════════════════════════════════════════════════════════╝

Se encontraron archivos de criterios de sesiones anteriores:
{lista}

Para continuar, tienes dos opciones:

1. Si alguno corresponde a esta tarea:
   → Lee el archivo y confirma con el usuario que siguen vigentes
   → Llama de nuevo a philosophy_architecture_analysis con
     criterios_file="ruta_completa_del_archivo"

2. Si ninguno aplica:
   → Usa philosophy_q0_criterios para acordar nuevos criterios
"""

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
    total_public_signatures = sum(len(f.get("public_signatures", [])) for f in files_info)

    # Agrupar por nivel actual
    by_level = {}
    for f in files_info:
        nivel = f["nivel_actual"]
        if nivel not in by_level:
            by_level[nivel] = []
        by_level[nivel].append(f)

    # Construir tabla de inventario
    inventory_table = "| # | Archivo | Líneas | Clases | Funciones | Públicas | Nivel actual | Extends |\n"
    inventory_table += "|---|---------|--------|--------|-----------|----------|--------------|----------|\n"

    for i, f in enumerate(files_info, 1):
        num_public = len(f.get("public_signatures", []))
        inventory_table += f"| {i} | {f['relative_path']} | {f['lines']} | {f['classes']} | {f['functions']} | {num_public} | {f['nivel_actual']} | {f['extends'] or '-'} |\n"

    # Construir tabla de firmas públicas (FASE 1 mejorada)
    signatures_table = "| Archivo | Función | Firma completa |\n"
    signatures_table += "|---------|---------|----------------|\n"

    for f in files_info:
        for sig in f.get("public_signatures", []):
            signatures_table += f"| {f['relative_path']} | {sig['name']} | `{sig['signature']}` |\n"

    response = f'''
╔══════════════════════════════════════════════════════════════════╗
║  ANÁLISIS ARQUITECTÓNICO INICIADO                                ║
║  "El análisis ES exhaustivo, sistemático y exacto"               ║
║  "Verificar ANTES de escribir, no DESPUÉS de fallar"             ║
╚══════════════════════════════════════════════════════════════════╝

📁 PROYECTO: {project_name}
📂 RUTA: {path}
🔧 LENGUAJE: {language}

📄 ARCHIVO DE ANÁLISIS: {analysis_file}
📋 CRITERIOS DE LA TAREA: {criterios_file}

⚠️ Evalúa cada decisión contra los criterios documentados.
   Si algo no cumple los criterios, ajusta antes de continuar.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 INVENTARIO INICIAL (FASE 0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 RESUMEN:
   • Archivos encontrados: {len(files_info)}
   • Total líneas de código: {total_lines}
   • Total clases: {total_classes}
   • Total funciones: {total_functions}
   • Funciones públicas (verificables): {total_public_signatures}

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
📝 FIRMAS PÚBLICAS (para verificación de dependencias)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{signatures_table}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ FASE 0 COMPLETADA

➡️ SIGUIENTES PASOS:
   1. Usa philosophy_architecture_checkpoint para guardar el inventario (CHECKPOINT 1)
   2. Analiza las funcionalidades de cada archivo (FASE 2)
   3. Clasifica cada archivo en su nivel correcto (FASE 3)
   4. Genera el plan de refactorización con dependencias verificadas (FASE 4)

⚠️ IMPORTANTE:
   - Las FIRMAS PÚBLICAS son las interfaces verificables
   - Usa estas firmas en FASE 4 para definir dependencias de cada tarea
   - Si la conversación se compacta, usa philosophy_architecture_resume
   - El archivo de análisis está en: {analysis_file}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 INSTRUCCIÓN OBLIGATORIA PARA CLAUDE - ANÁLISIS ARQUITECTÓNICO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEBES completar las 4 FASES en orden. NO puedes abandonar sin preguntar.

Si quieres abandonar o saltar una fase:
1. EXPLICA por qué quieres abandonar/saltar
2. USA AskUserQuestion para preguntar al usuario

🚫 PROHIBIDO:
- Abandonar el análisis sin preguntar
- Saltar a otra tarea sin completar las 4 fases
- Decir "continuaremos después" sin confirmar con el usuario
- Olvidar guardar checkpoints

FASES PENDIENTES:
   ⬜ FASE 1: Guardar inventario (checkpoint 1)
   ⬜ FASE 2: Mapa de funcionalidades (checkpoint 2)
   ⬜ FASE 3: Clasificación por niveles (checkpoint 3)
   ⬜ FASE 4: Plan de refactorización (checkpoint 4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''

    return response


async def architecture_resume(analysis_file: str) -> str:
    """Retoma un análisis arquitectónico desde el archivo"""

    file_path = Path(analysis_file).expanduser().resolve()

    if not file_path.exists():
        return f"Error: El archivo {analysis_file} no existe"

    # Verificar que existen criterios documentados
    claude_dir = file_path.parent
    criterios_files = list(claude_dir.glob("criterios_*"))
    if not criterios_files:
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  RETOMA BLOQUEADA: FALTAN CRITERIOS                              ║
╚══════════════════════════════════════════════════════════════════╝

❌ No se encontró archivo de criterios en {claude_dir}/

Antes de retomar el análisis:

1. Reformula al usuario lo que entiendes de la tarea
2. Acuerda: qué se va a hacer, para qué, y qué debe cumplir
3. Crea el archivo .claude/criterios_[tarea].md con los criterios
   exactos tal cual se acordaron — sin resumir ni parafrasear

Retomar sin criterios claros lleva a ejecutar sin dirección.
"""

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

    # Buscar archivo de criterios
    scope_path = Path(scope).expanduser().resolve() if scope != "DESCONOCIDO" else file_path.parent.parent
    claude_dir = scope_path / ".claude"
    criterios_files = list(claude_dir.glob("criterios_*")) if claude_dir.exists() else []
    criterios_file = str(criterios_files[0]) if criterios_files else None

    # Actualizar estado global
    ARCHITECTURE_STATE["active"] = True
    ARCHITECTURE_STATE["analysis_file"] = str(file_path)
    ARCHITECTURE_STATE["checkpoint"] = checkpoint
    ARCHITECTURE_STATE["phase"] = estado
    ARCHITECTURE_STATE["project_path"] = scope
    ARCHITECTURE_STATE["language"] = language
    # v2.5.0: Si retomamos con EJECUTANDO, el plan ya fue aprobado.
    # Si retomamos con FASE_4 y checkpoint >= 4, aún no fue aprobado.
    ARCHITECTURE_STATE["plan_approved"] = (estado == "EJECUTANDO")

    # Extraer título del proyecto
    title_match = re.search(r'^# Análisis Arquitectónico:\s*(.+)$', content, re.MULTILINE)
    project_name = title_match.group(1) if title_match else "Proyecto"

    # Instrucción especial cuando análisis está completo pero NO aprobado
    instruccion_implementacion = ""
    if checkpoint >= 4 and not ARCHITECTURE_STATE["plan_approved"]:
        instruccion_implementacion = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ ANÁLISIS COMPLETO — DEVOLUCIÓN OBLIGATORIA ANTES DE IMPLEMENTAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUÉ debes hacer:
   Presentar al usuario una DEVOLUCIÓN COMPLETA del análisis.

ANTES DE PRESENTAR — reconecta con los criterios:
   □ Lee los criterios que se acordaron en q0 (archivo .claude/criterios_*)
   □ ¿Tu explicación responde a TODOS los criterios, o solo a los
     que coinciden con la solución técnica que encontraste?
   □ ¿El usuario puede verificar lo que dices sin leer el código?
     Si usas un nombre de función, explica QUÉ HACE en el juego.
   □ ¿Cubres todas las situaciones que el usuario mencionó, o te
     centraste en una y olvidaste el resto?

   La devolución tiene dos partes obligatorias por cada tarea:

   A) EXPLICACIÓN FUNCIONAL — qué cambia para el usuario/jugador:
      - Qué pasa hoy (el problema que vive el usuario)
      - Qué cambiará (cómo lo vivirá después del fix)
      - Qué notará el usuario (cambio visible o invisible)

   B) EXPLICACIÓN TÉCNICA — qué se modifica en el código:
      - Archivos afectados
      - Tipo de cambio (guard, refactor, nuevo componente)
      - Dependencias entre tareas

PARA QUÉ:
   Para que el usuario pueda tomar decisiones informadas.
   Sin la explicación funcional, el usuario no sabe si el plan
   resuelve su problema real o si falta cubrir alguna casuística.

POR QUÉ:
   Claude 4.6 tiende a presentar solo la parte técnica y saltar
   directamente a implementar. El usuario se queda sin información
   para decidir, y si falta algo lo descubre después del cambio.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESPUÉS de presentar la devolución:

1. USA AskUserQuestion para obtener aprobación:
   "¿Apruebas el plan? ¿Falta alguna casuística?"
   Opciones:
   - "Sí, implementar"
   - "Ajustar plan" → el usuario explica qué cambiar
   - "Solo análisis" → guardar sin implementar

2. Si el usuario pide más análisis:
   - Hazlo Y guárdalo con architecture_checkpoint (mismo checkpoint 4)
   - Para que persista si se compacta la conversación

3. Cuando el usuario apruebe, guarda con:
   architecture_checkpoint(phase="EJECUTANDO", data=<plan aprobado completo>)
   Esto desbloquea q1 para la implementación.

4. Para CADA tarea aprobada: usa philosophy_q0_criterios (q0→q9)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ q1 ESTÁ BLOQUEADO hasta que guardes con phase="EJECUTANDO".
⛔ La devolución al usuario es el FINAL del turno.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    response = f'''
╔══════════════════════════════════════════════════════════════════╗
║  ANÁLISIS ARQUITECTÓNICO RETOMADO                                ║
║  "El análisis ES exhaustivo, sistemático y exacto"               ║
╚══════════════════════════════════════════════════════════════════╝

📁 PROYECTO: {project_name}
📄 ARCHIVO: {file_path}
📋 CRITERIOS: {criterios_file or "⚠️ No encontrado — crea .claude/criterios_[tarea].md antes de continuar"}

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

⚠️ ANTES DE CONTINUAR:
   - Reformula al usuario lo que entiendes de la tarea y verifica tu comprensión
   - Lee los criterios documentados (ver CRITERIOS arriba) y evalúa cada paso contra ellos
   - Continúa desde la TAREA ACTUAL indicada arriba
   - Lee el archivo completo si necesitas más contexto
   - No empieces de cero
{instruccion_implementacion}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 INSTRUCCIÓN OBLIGATORIA PARA CLAUDE - ANÁLISIS ARQUITECTÓNICO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEBES completar las 4 FASES. NO puedes abandonar sin preguntar.

Si quieres abandonar o cambiar de tarea:
1. EXPLICA por qué quieres abandonar
2. USA AskUserQuestion para preguntar al usuario

🚫 PROHIBIDO abandonar sin confirmar con el usuario.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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

    # v2.5.0: Gestión del gate plan_approved
    # Checkpoint 4 con FASE_4 → plan pendiente de aprobación
    # Checkpoint con EJECUTANDO → plan aprobado por el usuario
    if checkpoint >= 4 and phase == "FASE_4":
        ARCHITECTURE_STATE["plan_approved"] = False
    elif phase == "EJECUTANDO":
        ARCHITECTURE_STATE["plan_approved"] = True

    # Instrucción especial cuando checkpoint 4 está completo
    instruccion_implementacion = ""
    if checkpoint >= 4 and not ARCHITECTURE_STATE["plan_approved"]:
        instruccion_implementacion = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ ANÁLISIS COMPLETO — DEVOLUCIÓN OBLIGATORIA ANTES DE IMPLEMENTAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUÉ debes hacer:
   Presentar al usuario una DEVOLUCIÓN COMPLETA del análisis.

ANTES DE PRESENTAR — reconecta con los criterios:
   □ Lee los criterios que se acordaron en q0 (archivo .claude/criterios_*)
   □ ¿Tu explicación responde a TODOS los criterios, o solo a los
     que coinciden con la solución técnica que encontraste?
   □ ¿El usuario puede verificar lo que dices sin leer el código?
     Si usas un nombre de función, explica QUÉ HACE en el juego.
   □ ¿Cubres todas las situaciones que el usuario mencionó, o te
     centraste en una y olvidaste el resto?

   La devolución tiene dos partes obligatorias por cada tarea:

   A) EXPLICACIÓN FUNCIONAL — qué cambia para el usuario/jugador:
      - Qué pasa hoy (el problema que vive el usuario)
      - Qué cambiará (cómo lo vivirá después del fix)
      - Qué notará el usuario (cambio visible o invisible)

   B) EXPLICACIÓN TÉCNICA — qué se modifica en el código:
      - Archivos afectados
      - Tipo de cambio (guard, refactor, nuevo componente)
      - Dependencias entre tareas

PARA QUÉ:
   Para que el usuario pueda tomar decisiones informadas.
   Sin la explicación funcional, el usuario no sabe si el plan
   resuelve su problema real o si falta cubrir alguna casuística.

POR QUÉ:
   Claude 4.6 tiende a presentar solo la parte técnica y saltar
   directamente a implementar. El usuario se queda sin información
   para decidir, y si falta algo lo descubre después del cambio.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESPUÉS de presentar la devolución:

1. USA AskUserQuestion para obtener aprobación:
   "¿Apruebas el plan? ¿Falta alguna casuística?"
   Opciones:
   - "Sí, implementar"
   - "Ajustar plan" → el usuario explica qué cambiar
   - "Solo análisis" → guardar sin implementar

2. Si el usuario pide más análisis:
   - Hazlo Y guárdalo con architecture_checkpoint (mismo checkpoint 4)
   - Para que persista si se compacta la conversación

3. Cuando el usuario apruebe, guarda con:
   architecture_checkpoint(phase="EJECUTANDO", data=<plan aprobado completo>)
   Esto desbloquea q1 para la implementación.

4. Para CADA tarea aprobada: usa philosophy_q0_criterios (q0→q9)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ q1 ESTÁ BLOQUEADO hasta que guardes con phase="EJECUTANDO".
⛔ La devolución al usuario es el FINAL del turno.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

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

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 RECUERDA: DEBES completar las 4 FASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   {"✅" if checkpoint >= 1 else "⬜"} FASE 1: Inventario
   {"✅" if checkpoint >= 2 else "⬜"} FASE 2: Mapa de funcionalidades
   {"✅" if checkpoint >= 3 else "⬜"} FASE 3: Clasificación por niveles
   {"✅" if checkpoint >= 4 else "⬜"} FASE 4: Plan de refactorización

Si quieres abandonar → EXPLICA por qué + AskUserQuestion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{instruccion_implementacion}'''

    return response


def find_analysis_files(project_path: str = None) -> list:
    """Busca archivos de análisis arquitectónico en disco.

    Busca recursivamente en todos los directorios .claude del proyecto.
    """
    found_files = []

    if not project_path:
        return found_files

    p = Path(project_path).expanduser().resolve()

    if not p.exists():
        return found_files

    # Carpetas a ignorar
    ignore_dirs = {".git", "__pycache__", "node_modules", ".godot", "addons", "venv", ".venv"}

    # Buscar todos los directorios .claude recursivamente
    for claude_dir in p.rglob(".claude"):
        if not claude_dir.is_dir():
            continue

        # Verificar que no esté en una carpeta ignorada
        if any(ignored in claude_dir.parts for ignored in ignore_dirs):
            continue

        # Buscar archivos de análisis en este .claude
        for f in claude_dir.glob("architecture_analysis_*.md"):
            try:
                content = f.read_text(encoding='utf-8')
                # Extraer metadata
                estado_match = re.search(r'\*\*Estado:\*\*\s*(\w+)', content)
                checkpoint_match = re.search(r'\*\*Checkpoint actual:\*\*\s*(\d+)', content)
                title_match = re.search(r'^# Análisis Arquitectónico:\s*(.+)$', content, re.MULTILINE)
                scope_match = re.search(r'\*\*Scope:\*\*\s*(.+)', content)

                found_files.append({
                    "path": str(f),
                    "name": title_match.group(1) if title_match else f.stem,
                    "estado": estado_match.group(1) if estado_match else "DESCONOCIDO",
                    "checkpoint": int(checkpoint_match.group(1)) if checkpoint_match else 0,
                    "scope": scope_match.group(1).strip() if scope_match else str(claude_dir.parent),
                    "modified": f.stat().st_mtime
                })
            except:
                pass

    # Ordenar por fecha de modificación (más reciente primero)
    found_files.sort(key=lambda x: x["modified"], reverse=True)
    return found_files


async def architecture_status(project_path: str = None) -> str:
    """Muestra el estado actual del análisis arquitectónico.

    Busca tanto en memoria como en disco para encontrar análisis existentes.
    """

    # 1. Si hay análisis activo en memoria, mostrarlo
    if ARCHITECTURE_STATE["active"]:
        return f'''
╔══════════════════════════════════════════════════════════════════╗
║  ESTADO DEL ANÁLISIS ARQUITECTÓNICO                              ║
╚══════════════════════════════════════════════════════════════════╝

✅ ANÁLISIS ACTIVO EN MEMORIA

⚠️ ANTES DE CONTINUAR: Reformula al usuario lo que entiendes de la tarea
   y verifica que tu comprensión es correcta. Si hay criterios documentados
   en .claude/criterios_*.md, léelos primero.

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

    # 2. Buscar archivos de análisis en disco
    found_files = find_analysis_files(project_path) if project_path else []

    if found_files:
        response = '''
╔══════════════════════════════════════════════════════════════════╗
║  ESTADO DEL ANÁLISIS ARQUITECTÓNICO                              ║
╚══════════════════════════════════════════════════════════════════╝

⚠️ NO HAY ANÁLISIS ACTIVO EN MEMORIA

⚠️ ANTES DE CONTINUAR: Reformula al usuario lo que entiendes de la tarea
   y verifica que tu comprensión es correcta. Si hay criterios documentados
   en .claude/criterios_*.md, léelos primero.

📂 SE ENCONTRARON ANÁLISIS PREVIOS EN DISCO:

'''
        for i, f in enumerate(found_files[:5], 1):
            checkpoint = f["checkpoint"]
            fases_completadas = f"{'✅' * checkpoint}{'⬜' * (4 - checkpoint)}"
            scope = f.get("scope", "N/A")
            response += f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{i}. {f["name"]}
   📄 Archivo: {f["path"]}
   📂 Scope: {scope}
   📊 Estado: {f["estado"]} (Checkpoint {checkpoint})
   🔄 Fases: {fases_completadas}
'''

        response += f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

➡️ ANTES DE RETOMAR O INICIAR:
   1. Reformula al usuario lo que entiendes de la tarea
   2. Verifica que existe .claude/criterios_[tarea].md — si no, créalo con el usuario
   3. Solo entonces usa resume o analysis (se bloquearán sin criterios)
'''
        return response

    # 3. No hay nada
    no_path_msg = ""
    if not project_path:
        no_path_msg = "\n💡 TIP: Usa project_path para buscar análisis en un proyecto específico."

    return f'''
╔══════════════════════════════════════════════════════════════════╗
║  ESTADO DEL ANÁLISIS ARQUITECTÓNICO                              ║
╚══════════════════════════════════════════════════════════════════╝

❌ NO HAY ANÁLISIS ACTIVO
{no_path_msg}

Para iniciar un análisis usa:
   philosophy_architecture_analysis

Para retomar un análisis existente usa:
   philosophy_architecture_resume
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
