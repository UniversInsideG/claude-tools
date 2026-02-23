# Criterios: Evitar que Claude analice superficialmente antes de usar las herramientas de filosofía/arquitectura

## Reformulación
Implementar defensa en 3 capas: 1) Skills dicen "NO analices antes", 2) q0 detecta/advierte si hubo análisis previo y valida que criterios sean funcionales (no código), 3) CLAUDE.md establece regla general de usar herramientas ANTES de analizar código

## Criterios de éxito
1. Skills (/filosofia, /arquitectura): añadir instrucción explícita de NO analizar código antes de usar la herramienta
2. q0: detectar si Claude menciona análisis previo o conclusiones y advertir/bloquear
3. q0: validar que los criterios sean funcionales/de calidad, NO código o detalles de implementación
4. CLAUDE.md: regla clara de que las herramientas guían el análisis, no lo validan después
5. Las 3 capas se complementan como defensa en profundidad
6. No romper funcionalidad existente del MCP
