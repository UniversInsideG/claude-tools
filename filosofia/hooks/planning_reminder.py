#!/usr/bin/env python3
"""
Hook de Filosofía de Código - UniversInside
=============================================
Se ejecuta cuando el usuario envía un prompt con intención de código.
Recuerda la filosofía de arquitectura y el MCP philosophy.
Complementa metacognicion.py (que se activa en todos los prompts).
"""
import json
import sys
import re

# Palabras clave que indican que se va a escribir código
CODE_KEYWORDS = [
    r'\b(crea|crear|escribe|escribir|genera|generar|haz|hacer|implementa|implementar)\b',
    r'\b(script|escena|scene|nodo|node|clase|class|función|function|método|method)\b',
    r'\b(código|code|programa|program)\b',
    r'\b(component|componente|system|sistema|manager)\b',
    r'\b(gdscript|python|php|javascript|html|css)\b',
    r'\b(refactor|arregla|fix|modifica|cambia|añade|agrega|add)\b',
]

PHILOSOPHY_REMINDER = (
    "Código bien diseñado desde el inicio = 3 líneas en la próxima modificación. "
    "Código rápido sin análisis = 50 líneas cada vez + deuda técnica. "
    "Antes de escribir código, usa el MCP philosophy (9 pasos) porque cada paso existe para evitar trabajo futuro. "
    "Identifica qué nivel es (Pieza → Componente → Contenedor → Pantalla → Estructura) "
    "— porque el nivel determina si ya existe algo similar que reutilizar o extender. "
    "Si es nuevo, verifica que haga UNA sola cosa y que herede de la base correcta "
    "— si cambio la base, ¿se actualizan las instancias? "
    "El nombre debe reflejar el nivel (*_piece, *_component, *_system, *_screen) "
    "y la comunicación debe usar signals, no llamadas directas. "
    "Pasa siempre el archivo completo a philosophy_validate, nunca fragmentos "
    "— sin el archivo completo el validador genera falsos positivos que desacreditan "
    "la herramienta y anulan el control de calidad."
)

def detect_code_intent(prompt):
    """Detecta si el prompt implica escribir código"""
    prompt_lower = prompt.lower()

    for pattern in CODE_KEYWORDS:
        if re.search(pattern, prompt_lower):
            return True

    return False


def main():
    try:
        input_data = json.load(sys.stdin)
        hook_event = input_data.get('hook_event_name', '')

        # Solo procesar UserPromptSubmit
        if hook_event != 'UserPromptSubmit':
            sys.exit(0)

        # Obtener el prompt del usuario
        user_prompt = input_data.get('user_prompt', '')

        # Si no hay prompt o es muy corto, ignorar
        if not user_prompt or len(user_prompt) < 10:
            sys.exit(0)

        # Detectar si se va a escribir código
        if detect_code_intent(user_prompt):
            # Retornar mensaje de sistema para recordar la filosofía
            output = {
                "systemMessage": PHILOSOPHY_REMINDER,
                "continue": True
            }
            print(json.dumps(output))
            sys.exit(0)

        # No es código, continuar normal
        sys.exit(0)

    except Exception as e:
        # En caso de error, no bloquear
        sys.exit(0)


if __name__ == '__main__':
    main()
