# Criterios: Crear instaladores para web-philosophy-mcp (Mac terminal/VS Code, Mac Desktop, Windows) y actualizar instaladores Windows existentes de philosophy-mcp

## Reformulación
Crear scripts de instalación para que el MCP web-philosophy se pueda instalar en tres contextos: Claude Code (terminal + VS Code, misma config), Claude Desktop (config diferente), y Windows. Los instaladores deben preservar servidores MCP ya instalados (no borrar philosophy al añadir web-philosophy). También actualizar los instaladores Windows de philosophy-mcp para informar de la existencia de web-philosophy.

## Criterios de éxito
1. El instalador Mac/Linux permite elegir destino: Claude Code (terminal+VS Code), Claude Desktop, o ambos
2. Instalar web-philosophy NO borra ni modifica otros servidores MCP existentes (ej: philosophy)
3. El instalador Windows configura web-philosophy en .mcp.json preservando servidores existentes
4. Los instaladores de philosophy-mcp mencionan la existencia de web-philosophy al final
5. Cada instalador verifica Python 3 e instala la dependencia mcp antes de configurar
6. El instalador de Claude Desktop escribe en ~/Library/Application Support/Claude/claude_desktop_config.json preservando preferences existentes
