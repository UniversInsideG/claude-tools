# Criterios: Adaptar el MCP Philosophy a Claude 4.6: 5 cambios en server.py para mejorar el flujo con el nuevo modelo

## Reformulación
Claude 4.6 es más autónomo que 4.5 y trata los pasos del MCP como trámite. Necesitamos 5 cambios en server.py: (1) q0 bloquea criterios de implementación en la segunda llamada, (2) checkpoint 4 pausa dura con flujo filosofía obligatorio, (3) decision_usuario en dos pasos con verificación, (4) q3 usa ripgrep para escaneo, (5) validate soporta .tscn con checks de DRY.

## Criterios de éxito
1. q0 bloquea cuando detecta criterios de implementación en la segunda llamada (confirmado_por_usuario=true), no solo avisa en la primera
2. Checkpoint 4 de arquitectura devuelve instrucción de STOP que obliga a presentar plan y esperar aprobación, y luego ejecutar cada tarea con flujo filosofía
3. decision_usuario requiere dos llamadas: primera con justificación (STOP), segunda con usuario_verifico=true tras preguntar al usuario
4. q3 usa ripgrep (subprocess) para buscar archivos por nombre y contenido, manteniendo búsqueda de documentación y detección de duplicación en Python
5. validate soporta archivos .tscn con checks relevantes para escenas Godot (duplicación de SubResources, estilos repetidos, propiedades hardcodeadas) en vez de fallar
6. Los cambios no rompen el flujo existente que ya funciona
