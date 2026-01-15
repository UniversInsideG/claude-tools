# Fix: Verificación de Interfaces antes de escribir código

**Fecha:** 2026-01-14
**Estado:** PROBLEMA IDENTIFICADO - Pendiente implementación

---

## PROBLEMA IDENTIFICADO

**Ambos flujos** tienen el mismo hueco crítico: **no verifican las dependencias externas**.

Este problema causa que:
1. Se escriba código llamando a funciones que no existen
2. Se asuman firmas incorrectas
3. Los errores se detecten en runtime, no en diseño

### Tabla del problema

| Paso | Qué hace | Qué falta |
|------|----------|-----------|
| q1-q2 | Define responsabilidad y reutilización | ✅ OK |
| q3 | Busca código similar | ❌ NO busca las interfaces de las DEPENDENCIAS |
| q4-q5 | Define herencia y nivel | ✅ OK |
| q6 | Escribir código | ❌ Escribe sin verificar firmas de funciones externas |
| q7 | Valida código escrito | ❌ Solo valida sintaxis, NO llamadas externas |

### Huecos en /arquitectura

| Fase | Qué hace | Qué falta |
|------|----------|-----------|
| FASE 1 | Inventario de archivos | ❌ NO lista las firmas de funciones públicas |
| FASE 2 | Mapa de funcionalidades | ❌ Dice "qué hace" pero NO "con qué firma" |
| FASE 3 | Clasificación por niveles | ✅ OK |
| FASE 4 | Plan de refactorización | ❌ Las tareas NO incluyen verificación de interfaces |
| FASE 5 | Ejecución | ❌ Tests son "funciona/no funciona", NO "las llamadas son correctas" |

### Ejemplo del problema

En FASE 2 se documentó:
```
player_turn_panel: load_player_turn(), end_game_controller(has_won, reason)
```

**Problema:** Se asumieron los nombres sin verificar que:
1. Las funciones existen
2. Las firmas son correctas
3. Los parámetros coinciden

### Consecuencia

El código se escribe llamando a funciones que:
- No existen
- Tienen firma diferente (parámetros, tipos)
- Han cambiado desde la última vez que se vieron

**Resultado:** Errores en runtime que podrían haberse evitado.

---

## SOLUCIÓN PROPUESTA

### 1. Para /filosofia: Nuevo paso `philosophy_q6_verificar_dependencias`

**Ubicación:** Entre q5 (nivel) y escribir código

**Flujo actualizado:**
```
q1 → q2 → q3 → q4 → q5 → q6 → [escribir] → q7
                         ↑
                    NUEVO: Verificar
                    dependencias externas
```

### 2. Para /arquitectura: Mejoras en FASE 1, 2 y 4

**FASE 1 mejorada:** Inventario incluye firmas públicas
```
| Archivo | Funciones públicas (con firma) |
|---------|--------------------------------|
| auth_system.gd | validate_user(email: String, pass: String) -> bool |
| auth_system.gd | logout() -> void |
```

**FASE 2 mejorada:** Mapa incluye firmas exactas verificadas
```
Funcionalidad: Autenticación
- auth_system.gd:validate_user(email: String, pass: String) -> bool ✓ verificado
- auth_system.gd:logout() -> void ✓ verificado
```

**FASE 4 mejorada:** Cada tarea lista dependencias verificadas
```
TAREA 1.1: Crear GameViewSystem
DEPENDENCIAS EXTERNAS (verificadas):
  - player_turn_panel.gd → load_player(data: Dictionary) -> void ✓
  - character_sheet.gd → load_user(user: User, config: Dictionary) -> void ✓
```

### Qué hace q6_verificar_dependencias

1. **Lista** todas las funciones/métodos externos que el código va a llamar
2. **Busca** cada función en los archivos del proyecto
3. **Extrae** la firma real (nombre, parámetros, tipos de retorno)
4. **Compara** con lo que se espera usar
5. **Bloquea** si hay discrepancias

### Input del paso

```python
{
    "calls": [
        {
            "file": "systems/auth_system.gd",
            "function": "validate_user",
            "expected_params": ["username: String", "password: String"],
            "expected_return": "bool"
        },
        {
            "file": "components/dialog_component.gd",
            "function": "show_error",
            "expected_params": ["message: String"],
            "expected_return": "void"
        }
    ],
    "project_path": "/ruta/al/proyecto"
}
```

### Output del paso

**Si todo coincide:**
```
╔══════════════════════════════════════════════════════════════════╗
║  PASO 5b/7: VERIFICACIÓN DE INTERFACES                           ║
╚══════════════════════════════════════════════════════════════════╝

✅ TODAS LAS INTERFACES VERIFICADAS

| Función | Archivo | Estado |
|---------|---------|--------|
| validate_user(username: String, password: String) -> bool | auth_system.gd | ✅ |
| show_error(message: String) -> void | dialog_component.gd | ✅ |

➡️ SIGUIENTE: Escribe el código (paso 6)
```

**Si hay discrepancias:**
```
╔══════════════════════════════════════════════════════════════════╗
║  ⛔ ERROR: INTERFACES NO COINCIDEN                               ║
╚══════════════════════════════════════════════════════════════════╝

❌ DISCREPANCIAS ENCONTRADAS:

1. validate_user en auth_system.gd
   ESPERADO: validate_user(username: String, password: String) -> bool
   REAL:     validate_user(email: String, pass: String, remember: bool) -> Dictionary

   ⚠️ La firma ha cambiado. Ajusta tu diseño.

🚫 NO PUEDES CONTINUAR hasta resolver las discrepancias.
```

---

## IMPLEMENTACIÓN

### Función en server.py

```python
async def step5b_verificar_interfaces(calls: list, project_path: str) -> str:
    """PASO 5b: Verifica que las interfaces externas existen y coinciden"""

    # Verificar paso anterior
    if not SESSION_STATE["step_5"]:
        return "Error: Completa q5_nivel primero"

    path = Path(project_path).expanduser().resolve()
    issues = []
    verified = []

    for call in calls:
        file_path = path / call["file"]

        if not file_path.exists():
            issues.append(f"❌ Archivo no existe: {call['file']}")
            continue

        content = file_path.read_text()

        # Buscar la función
        func_name = call["function"]

        # Regex para encontrar la firma (Godot)
        pattern = rf'^func\s+{func_name}\s*\([^)]*\)'
        match = re.search(pattern, content, re.MULTILINE)

        if not match:
            issues.append(f"❌ Función no encontrada: {func_name} en {call['file']}")
            continue

        # Extraer firma real
        real_signature = match.group(0)

        # Comparar con esperada
        # [lógica de comparación de firmas]

        verified.append({
            "function": func_name,
            "file": call["file"],
            "signature": real_signature
        })

    if issues:
        # Bloquear
        return f"❌ INTERFACES NO COINCIDEN:\n" + "\n".join(issues)

    SESSION_STATE["step_5b"] = True
    return f"✅ TODAS LAS INTERFACES VERIFICADAS\n" + ...
```

---

## FLUJO ACTUALIZADO

```
ANTES:
q1 → q2 → q3 → q4 → q5 → [escribir] → q7

DESPUÉS:
q1 → q2 → q3 → q4 → q5 → q5b → [escribir] → q7
                         ↑
                    Verifica que las funciones
                    externas existen y sus
                    firmas coinciden
```

---

## PRÓXIMOS PASOS

### Para /filosofia
1. ⬜ Implementar `philosophy_q6_verificar_dependencias` en server.py
2. ⬜ Renumerar: q6→q7 (escribir), q7→q8 (validate)
3. ⬜ Actualizar skill `/filosofia` con el nuevo paso
4. ⬜ Probar con caso real

### Para /arquitectura
5. ⬜ Actualizar FASE 1: añadir extracción de firmas públicas
6. ⬜ Actualizar FASE 2: verificar firmas al documentar funcionalidades
7. ⬜ Actualizar FASE 4: cada tarea incluye dependencias verificadas
8. ⬜ Actualizar skill `/arquitectura`
9. ⬜ Probar con caso real

### General
10. ⬜ Documentar en CLAUDE.md

---

## RESUMEN DE CAMBIOS

| Flujo | Cambio |
|-------|--------|
| /filosofia | Nuevo paso q6 antes de escribir código |
| /arquitectura FASE 1 | Inventario incluye firmas públicas |
| /arquitectura FASE 2 | Mapa verifica firmas exactas |
| /arquitectura FASE 4 | Tareas listan dependencias verificadas |

---

> **"El análisis ES exhaustivo, sistemático y exacto"**
>
> **"Verificar ANTES de escribir, no DESPUÉS de fallar"**
