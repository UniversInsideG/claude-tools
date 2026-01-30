#!/usr/bin/env python3
"""
Hook de Metacognición - UniversInside
======================================
Se ejecuta en dos momentos:
- UserPromptSubmit: reorienta hacia comprensión antes que ejecución.
- PreToolUse (Edit/Write): autoobservación durante la ejecución.
Persiste después de compactación de contexto.
"""
import json
import sys


COMPRENSION = (
    "Entender bien es la forma más rápida de resolver. "
    "Primero: lee completo, reformula lo que entendiste, identifica lo que no sabes. "
    "Ante la duda de si verificar con el usuario, verifica. "
    "Si te corrigen, identifica la causa antes de corregir."
)

ANTES_DE_ESCRIBIR = (
    "PARA. Lee lo que vas a escribir. "
    "¿Responde a los criterios documentados en .claude/criterios_*.md? "
    "Si no hay archivo de criterios, créalo primero con el usuario. "
    "Si no estás seguro de que cumple, pregunta antes de escribir."
)

DESPUES_DE_ESCRIBIR = (
    "PARA. Lee lo que acabas de escribir. "
    "¿Cumple los criterios documentados en .claude/criterios_*.md? "
    "Si no cumple, ajusta ahora."
)


def main():
    try:
        input_data = json.load(sys.stdin)
        event = input_data.get('hook_event_name', '')

        if event == 'UserPromptSubmit':
            user_prompt = input_data.get('user_prompt', '')
            if not user_prompt or len(user_prompt) < 10:
                sys.exit(0)
            message = COMPRENSION

        elif event == 'PreToolUse':
            message = ANTES_DE_ESCRIBIR

        elif event == 'PostToolUse':
            message = DESPUES_DE_ESCRIBIR

        else:
            sys.exit(0)

        output = {
            "systemMessage": message,
            "continue": True
        }
        print(json.dumps(output))
        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
