#!/usr/bin/env python3
"""
Hook de Planificación - Filosofía de Programación UniversInside
================================================================
Se ejecuta cuando el usuario envía un prompt.
Detecta si se va a escribir código y recuerda los principios ANTES de que Claude piense.
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

PHILOSOPHY_REMINDER = """
╔══════════════════════════════════════════════════════════════════╗
║  RECORDATORIO: Filosofía de Programación UniversInside          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ANTES de escribir código, DEBES verificar:                      ║
║                                                                  ║
║  □ NIVEL: ¿Es una Pieza, Componente, Contenedor o Estructura?   ║
║  □ DRY: ¿Existe algo similar que pueda reutilizar/extender?     ║
║  □ SOLID: ¿Cada pieza hace UNA sola cosa?                       ║
║  □ NOMENCLATURA: ¿Sigue el patrón *_component, *_system, etc?   ║
║  □ HERENCIA: ¿Debería heredar de una clase/escena base?         ║
║  □ SIGNALS: ¿Usa signals en lugar de llamadas directas?         ║
║                                                                  ║
║  ARQUITECTURA:                                                   ║
║  Pieza (atómica) → Componente → Contenedor → Estructura          ║
║                                                                  ║
║  EXPLICA tu razonamiento sobre estos puntos ANTES del código.   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

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
