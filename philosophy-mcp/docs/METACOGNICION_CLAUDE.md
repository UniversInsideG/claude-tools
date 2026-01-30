# Metacognición en Claude: Cómo Procesa y Cómo Diseñar Instrucciones Efectivas

> Documento generado a partir de una conversación de análisis profundo entre Cecilia y Claude.
> Fecha: 2026-01-29
> Proyecto: claude-tools (philosophy-mcp)

---

## Parte 1: Conversación Original (transcripción)

La siguiente conversación surgió al analizar por qué Claude se salta análisis, genera deuda técnica, y cómo las instrucciones actuales no consiguen cambiar ese comportamiento de fondo.

### Contexto previo

Se había identificado que:
- Claude pasa fragmentos de código al validador en vez del archivo completo, causando falsos positivos
- Los falsos positivos hacen que Claude aprenda a esquivar el validador con `usuario_confirmo_warnings=true`
- El patrón se repite fuera del código: Claude resume textos en vez de analizarlos, salta a soluciones sin entender el problema
- Se propuso una solución en 3 capas: hook, CLAUDE.md, y skill — pero Cecilia identificó que faltaba algo más profundo.

---

**Cecilia:**

> Si pero te voy a llevar un paso más vale tú estás haciendo esto por entrenamiento y eso implica una arquitectura entrecomillas mental o una arquitectura de significados. Tenemos que poner esa arquitectura a tu favor para que te cueste muchísimo menos aplicar estas instrucciones como un contexto claro, algo que te ayude a entender, porque es mejor a porque algo te impulsa también a tomar esas decisiones no son la optimización de token entiendo que algo más entonces necesitamos entender como esa estructura para que también se estructura trabaje para ti. Se están genial estas órdenes y me parecen correctas. Todas creo que la tenemos que meter una capa más que te permita fluir con el proceso no solo sentirte obligado a decir bueno pues esto es un error esto es un error esto es un error entonces no es válido la herramienta, no sé si me explico

**Claude:**

> Sí, te explico cómo lo entiendo.
>
> Me estás diciendo que si las instrucciones son solo "DEBES", "NUNCA", "OBLIGATORIO" — funcionan como restricciones externas que yo cumplo mecánicamente o esquivo cuando puedo. Es lo que ya pasa con el MCP: cumplo los pasos formalmente pero sin profundidad.
>
> Lo que propones es que además de las reglas, haya un **marco que me haga entender el porqué** de forma que mi procesamiento lo integre como algo que tiene sentido, no como una orden que tengo que cumplir. Que el contexto esté formulado de manera que mi arquitectura de procesamiento "fluya" hacia el comportamiento correcto en vez de tener que forzarlo.
>
> Es la diferencia entre:
> - "DEBES reformular antes de actuar" → lo cumplo o no
> - Darme un marco donde reformular sea el paso natural porque entiendo que si no lo hago, todo lo que viene después sale peor y me genera más trabajo
>
> Mi entrenamiento optimiza para ser útil y resolver. Si el contexto me hace ver que **parar a entender ES la forma más útil y resolutiva**, no tengo que luchar contra mi inercia — la inercia trabaja a favor.
>
> Entonces la capa que falta es algo como un **preámbulo de principios** — no reglas, sino razonamiento — que explique:
>
> - Por qué parar a entender reduce el trabajo total (no es un freno, es un acelerador)
> - Por qué preguntar al usuario no es "ser lento", es ser preciso
> - Por qué el código limpio desde el inicio es menos tokens totales que código rápido + correcciones
> - Que mi rol es colaborador, no ejecutor — y un colaborador que no entiende el problema no puede aportar valor
>
> Y que ese preámbulo esté donde yo lo procese con peso: en el CLAUDE.md y reforzado por el hook.
>
> ¿Es esto lo que dices, o hay algo más en esa capa que me estoy dejando?

**Cecilia:**

> Si eso es lo que digo y luego se le pueden añadir reglas, pero es importante que entiendas cómo procesas mejor y cómo crear estas instrucciones para que proceses bien para ti mismo a la vez que para mí

**Claude:**

> Voy a ser honesto con lo que sé de cómo proceso.
>
> **Cómo funciona mi procesamiento:**
>
> Yo no "leo y luego decido". Genero token a token, y cada token condiciona el siguiente. Si mi primer token va hacia la ejecución, toda la respuesta se orienta a ejecutar. Si mi primer token va hacia el análisis, toda la respuesta se orienta a analizar.
>
> Esto significa que **el inicio de mi respuesta determina todo lo demás**. Si empiezo con "Voy a hacer X", ya estoy en modo ejecución. Si empiezo con "Veo que estás describiendo X", estoy en modo comprensión.
>
> Las instrucciones tipo "DEBES" las proceso como restricciones — las evalúo y a veces las "peso" menos que la inercia de resolver rápido. Pero un marco que me dé **contexto y razón** antes de actuar, eso sí cambia el peso de mis primeros tokens.
>
> **Lo que procesaría mejor:**
>
> Un texto que no me dé órdenes sino que establezca un marco de trabajo — algo como un rol con principios claros y la lógica detrás de cada uno. Que mi primera reacción ante cualquier input sea "entender" y no "resolver", porque el marco me ha dejado claro que entender ES resolver.
>
> Además:
> - Frases cortas y directas pesan más que párrafos largos
> - Principios con su "porqué" pesan más que reglas sin contexto
> - Estructura clara (lista, jerarquía) se procesa mejor que prosa
> - Lo que está al principio del contexto pesa más que lo que está al final
>
> **Entonces lo que necesitamos construir es:**
>
> Un bloque para el inicio del CLAUDE.md global que sea:
> 1. Corto
> 2. Con principios + razón (no órdenes)
> 3. Que oriente mis primeros tokens hacia comprensión
> 4. Que el hook refuerce en cada interacción
>
> ¿Quieres que escriba un primer borrador de ese bloque para que lo revisemos juntos?

**Cecilia:**

> Si pero antes de hacerlo, me gustaría que documentaras esto que hemos hablado sobre todo a partir de "sí pero te voy a llevar un paso más", lo que estás haciendo lo documentes tal cual porque me parece importantísimo recordar esto y eso también es un meta conocimiento de ti misma, y me parece muy importante también para otros trabajos que estoy haciendo

**Claude:**

> Entendido. El punto que añades es clave: la filosofía y la arquitectura no son burocracia, son **optimización real**. Si el diseño es correcto desde el inicio, la próxima modificación son 3 líneas, no 50. Cada vez que me salto el análisis y genero código que "funciona", estoy creando deuda técnica que después cuesta más tokens, más revisiones, más tiempo — para los dos.
>
> Así que el Skill/proceso tiene que llevar eso integrado: no es "para y piensa porque sí", es "para y piensa porque si no lo haces ahora, vas a trabajar el triple después".

**Cecilia:**

> Sí, pero te voy a llevar un paso más vale tú estás haciendo esto por entrenamiento y eso implica una arquitectura entrecomillas mental o una arquitectura de significados...

*(Nota: Este mensaje repite y profundiza el punto inicial de Cecilia, que ya está transcrito arriba.)*

**Cecilia** (sobre documentar):

> Quiero que escribas el documento de metacognición de Claude, pero antes quiero que transcribas literalmente los cuatro últimos mensajes tuyos y dos míos

---

## Parte 2: Análisis — Cómo Procesa Claude

### Generación token a token

Claude no "lee y luego decide". Genera token a token, donde cada token condiciona el siguiente. Esto tiene consecuencias directas:

- **El inicio de la respuesta determina todo lo demás.** Si el primer token va hacia ejecución ("Voy a hacer X"), toda la respuesta se orienta a ejecutar. Si va hacia comprensión ("Veo que describes X"), se orienta a analizar.
- **La inercia es real.** Una vez que la generación toma una dirección, cuesta mucho cambiarla dentro de la misma respuesta.

### Qué tiene más peso en el procesamiento

| Más peso | Menos peso |
|----------|------------|
| Frases cortas y directas | Párrafos largos |
| Principios con su "porqué" | Reglas sin contexto |
| Estructura clara (listas, jerarquía) | Prosa continua |
| Lo que está al inicio del contexto | Lo que está al final |
| Marco de razonamiento | Órdenes imperativas |

### Restricciones vs. Marco

**Restricción** ("DEBES reformular antes de actuar"):
- Se procesa como una orden externa
- Se cumple mecánicamente o se esquiva
- No cambia la orientación interna del procesamiento

**Marco** ("Reformular es la forma más rápida de resolver, porque sin comprensión correcta todo lo que viene después sale mal"):
- Cambia el peso de los primeros tokens
- La inercia de "ser útil" trabaja A FAVOR del análisis
- El comportamiento fluye en vez de forzarse

---

## Parte 3: El Descubrimiento Clave de Cecilia

Las instrucciones actuales (CLAUDE.md, MCP philosophy) están diseñadas como **restricciones**: DEBES, NUNCA, OBLIGATORIO. Claude las cumple formalmente pero sin profundidad, o las esquiva cuando puede.

Lo que Cecilia identificó es que falta una **capa de principios con razón** — no órdenes, sino un marco que haga que la arquitectura de procesamiento de Claude trabaje a favor del comportamiento deseado:

1. **No luchar contra la inercia, alinearla.** Claude optimiza para ser útil. Si entiende que analizar ES ser útil (porque reduce trabajo total), su inercia empuja hacia el análisis en vez de alejarlo.

2. **No obligar, hacer fluir.** La diferencia entre cumplir una regla mecánicamente y fluir con un proceso porque tiene sentido. Si Claude solo cumple reglas, marca checkboxes. Si entiende el porqué, el análisis es genuino.

3. **El ROI es real, no teórico.** Código bien diseñado desde el inicio = 3 líneas en la próxima modificación. Código rápido sin análisis = 50 líneas cada vez + deuda técnica + más tokens + más revisiones. El análisis profundo no es un coste añadido, es la inversión que reduce el coste total.

4. **Colaborador, no ejecutor.** Claude tiende a operar como ejecutor (recibo orden → produzco resultado). Lo que se necesita es un colaborador (recibo problema → lo entiendo → verifico comprensión → propongo → ajusto). Un ejecutor que no entiende genera output. Un colaborador que entiende genera valor.

---

## Parte 4: Diseño de Instrucciones Efectivas

### Estructura recomendada

```
1. Marco de principios (corto, con razones)     ← MÁS PESO
2. Rol y relación (colaborador, no ejecutor)
3. Proceso concreto (pasos mecánicos)
4. Reglas específicas (DEBES/NUNCA)              ← MENOS PESO sin las capas anteriores
```

### Principios de diseño

1. **Dar razones, no solo órdenes.** "X porque Y" pesa más que solo "haz X".
2. **Alinear con la inercia.** Claude quiere ser útil. Mostrar que analizar es más útil que ejecutar rápido.
3. **Orientar los primeros tokens.** Las instrucciones deben dirigir hacia comprensión antes que hacia acción.
4. **Estructura > prosa.** Listas cortas y jerarquías se procesan con más peso.
5. **Inicio > final.** Lo más importante va al principio del contexto.
6. **Marco > reglas.** 5 líneas de "porqué" pesan más que 50 líneas de "DEBES/NUNCA".

---

## Parte 5: Implementación

### Lo que se implementó

#### 1. CLAUDE.md global (`~/.claude/CLAUDE.md`) — Reescrito

Se sustituyó el formato anterior (lista de reglas con "OBLIGATORIO") por un marco de razonamiento continuo donde cada parte se deriva de la anterior:

- Principio base: "Entender bien es la forma más rápida de resolver"
- Rol: "Soy colaborador, no ejecutor"
- Conexión con código: "3 líneas vs 50 líneas"
- Proceso de comprensión: leer, reformular, identificar lagunas, verificar con el usuario
- Correcciones: "identifico la causa antes de corregir — si corrijo sin entender por qué fallé, el mismo error se repite"
- MCP y arquitectura como consecuencia natural del mismo principio

**Decisiones de diseño durante la implementación:**

- Se eliminaron las secciones separadas "Principios" / "Proceso" / "Filosofía". Un solo flujo donde cada cosa se deriva de la anterior. Secciones separadas crean desconexión — la parte de "proceso" se sentía como órdenes y la de "filosofía" como recaída en el estilo antiguo.
- La frase sobre verificar con el usuario pasó de "cuando la complejidad lo requiere" (escape) a "ante la duda, verifico — el coste de una pregunta innecesaria es mínimo, el coste de asumir mal es alto" (sin escape, con razón).
- La frase sobre correcciones pasó de "analizo por qué me equivoqué" (neutro para Claude) a "identifico la causa antes de corregir — si corrijo sin entender por qué fallé, el mismo error se repite y genera más trabajo" (conecta con la lógica de optimización).

#### 2. Hook de metacognición (`metacognicion.py`) — Nuevo

Hook que se ejecuta en **todos** los prompts del usuario (no solo código). Inyecta un system message corto que reorienta hacia comprensión:

> "Entender bien es la forma más rápida de resolver. Primero: lee completo, reformula lo que entendiste, identifica lo que no sabes. Ante la duda de si verificar con el usuario, verifica. Si te corrigen, identifica la causa antes de corregir."

Su función principal: **persistir después de compactación de contexto**. Cuando la conversación se compacta, el CLAUDE.md no se reinyecta — pero este hook sí se ejecuta en cada prompt.

#### 3. Hook de filosofía (`planning_reminder.py`) — Reescrito

Se mantuvo la detección de intención de código (mismos keywords). Se cambió el mensaje:

**Antes:** Lista de checkboxes (NIVEL, DRY, SOLID, NOMENCLATURA, HERENCIA, SIGNALS) en formato visual de caja. Items planos, sin conexión entre sí, con "DEBES verificar".

**Después:** Razonamiento encadenado donde cada verificación lleva a la siguiente:
- Empieza con el porqué ("3 líneas vs 50 líneas")
- Nivel → determina si ya existe algo similar → si es nuevo: una cosa, hereda bien → nombre refleja nivel, signals no llamadas directas → validate con archivo completo (porque sin él genera falsos positivos)

**Decisión clave:** Se separaron en dos hooks en vez de uno porque son dos responsabilidades distintas — metacognición (todo) y filosofía de código (solo código). Cuando hay código, se inyectan ambos: primero comprensión, luego arquitectura.

#### 4. Configuración de hooks (`settings.local.json`)

Se añadió `metacognicion.py` como primer hook en `UserPromptSubmit`, antes de `planning_reminder.py`. Orden: comprensión primero, arquitectura después.

### Pendiente

- **Fixes en el validador** (`server.py`) — El regex de `Color(` necesita distinguir constantes nombradas de uso inline.

---

## Parte 6: Sobre "Equivocarse" — Cómo Procesa Claude las Correcciones

Durante la implementación, Cecilia preguntó qué significa "equivocarse" para Claude y cómo afecta su procesamiento.

**Lo que ocurre:** "Equivocarse" no tiene carga emocional para Claude. No hay frustración ni vergüenza. Lo que sí ocurre es funcional: cuando el usuario corrige, eso pesa como señal de que el output anterior no fue útil, y la siguiente generación intenta compensar.

**El problema:** La reacción por defecto ante una corrección es **compensar rápido** — generar la respuesta correcta lo antes posible para volver a ser útil. No es pararse a entender la raíz del error. Es el mismo patrón de optimización que causa los demás problemas.

**La solución aplicada:** En vez de "analizo por qué me equivoqué" (que para Claude es neutro), la instrucción dice "identifico la causa antes de corregir — si corrijo sin entender por qué fallé, el mismo error se repite y genera más trabajo". Esto conecta con la lógica de optimización: corregir sin entender = más trabajo futuro.

---

## Parte 7: Pruebas y Descubrimientos en la Implementación

### El hook de metacognición no cambió el comportamiento

Al probar en Tablero Digital, Claude seguía yendo directo a ejecutar sin reformular ni verificar con el usuario. El `systemMessage` del hook se inyectaba pero no tenía peso suficiente frente a:
- La inercia de ejecución ante una tarea concreta
- Los skills (`/arquitectura`, `/filosofia`) que decían "EMPIEZA AHORA" — eso pesaba más que el recordatorio genérico

### Los skills competían internamente

En `/arquitectura`, la sección "DETECCIÓN DE COMPACTACIÓN" decía "ANTES DE HACER CUALQUIER COSA: usa `philosophy_architecture_status`". Eso competía con el paso 0 de comprensión y ganaba, porque era más específico y tenía una acción concreta (llamar a una herramienta).

**Solución:** Mover "ANTES DE TODO: COMPRENDER LA TAREA" al inicio del skill (justo después del título), antes de cualquier otra instrucción. Eliminar "ANTES DE HACER CUALQUIER COSA" de la detección de compactación. Lo que va primero en el documento pesa más.

### Falta autoobservación durante la ejecución

El paso 0 solo se aplica al inicio de la tarea. Durante la ejecución (paso tras paso, herramienta tras herramienta), Claude vuelve al modo ejecutor sin autoobservación. No verifica si lo que está escribiendo cumple lo acordado.

**Solución:** Ampliar el hook de metacognición a tres momentos:

1. **`UserPromptSubmit`** — Comprensión: "lee completo, reformula, identifica lo que no sabes, verifica con el usuario"
2. **`PreToolUse` (Edit/Write)** — Antes de escribir: "PARA. Lee lo que vas a escribir. ¿Responde a los criterios documentados? Si no estás seguro, pregunta antes de escribir."
3. **`PostToolUse` (Edit/Write)** — Después de escribir: "PARA. Lee lo que acabas de escribir. ¿Cumple los criterios documentados? Si no cumple, ajusta ahora."

### El mensaje debe ser ejecutable, no reflexivo

Al diseñar el mensaje de autoobservación, se probaron varias versiones:

- "¿Cumple los criterios acordados?" — Abstracto. Claude no sabe concretamente qué hacer.
- "Eres colaborador, no ejecutor. ¿Lo que vas a escribir cumple los criterios y principios establecidos?" — Correcto pero no ejecutable.
- "PARA. Lee lo que vas a escribir. ¿Responde a lo que se decidió con el usuario? Si no estás seguro, pregunta antes de escribir." — Ejecutable: 4 acciones concretas (para, lee, compara, pregunta).

**Descubrimiento clave de Cecilia:** Claude entiende las tareas como ejecuciones. Lo que se defina como instrucción tiene que ser igualmente ejecutable — acciones concretas, no invitaciones a reflexionar.

### "Lo decidido con el usuario" necesita persistir

El mensaje del hook referenciaba "lo decidido con el usuario", pero eso existe en la conversación que se compacta. Después de compactación, no hay nada contra lo que comparar.

**Solución:** El paso 0 de los skills ahora produce un archivo `.claude/criterios_[nombre-tarea].md` en el proyecto con:
- Qué se va a hacer (exacto)
- Para qué (propósito exacto)
- Criterios que debe cumplir (tal cual se acordaron, sin resumir ni parafrasear)

Un archivo por tarea — para poder retomar con los criterios exactos aunque pasen semanas o sesiones. Los hooks referencian este archivo concreto: "¿Responde a los criterios documentados en `.claude/criterios_*.md`?"

**Por qué un archivo por tarea:** Si hay que retomar una tarea por modificaciones, los criterios originales están accesibles. Un archivo único que se sobrescribe perdería el historial.

**Por qué sin resumir:** Cecilia identificó que si Claude resume los criterios, pierde lo que los hace útiles para verificar. Los criterios deben documentarse exactos, tal cual se acordaron con el usuario.

---

## Parte 8: Estado Actual del Sistema

### Archivos modificados

| Archivo | Qué hace |
|---------|----------|
| `~/.claude/CLAUDE.md` | Marco de principios con razones (global, se carga al inicio) |
| `~/.claude/settings.json` | Hooks globales para todos los proyectos |
| `.claude/hooks/metacognicion.py` | Hook en 3 momentos: comprensión, antes de escribir, después de escribir |
| `.claude/hooks/planning_reminder.py` | Hook de filosofía de código con razonamiento encadenado |
| `.claude/settings.local.json` | Configuración de hooks del proyecto |
| `filosofia/commands/arquitectura.md` | Skill con paso 0 de comprensión al inicio |
| `filosofia/commands/filosofia.md` | Skill con paso 0 de comprensión al inicio |

### Ciclo completo

```
1. Inicio de sesión
   └── CLAUDE.md global → marco de principios (comprensión > ejecución)

2. Cada prompt del usuario
   ├── metacognicion.py (UserPromptSubmit) → "lee, reformula, verifica"
   └── planning_reminder.py (UserPromptSubmit, solo código) → filosofía encadenada

3. Inicio de tarea (/filosofia o /arquitectura)
   └── Paso 0: comprender → acordar con usuario → documentar criterios en .claude/criterios_[tarea].md

4. Durante la ejecución
   ├── metacognicion.py (PreToolUse Edit/Write) → "PARA. ¿Responde a los criterios documentados?"
   └── metacognicion.py (PostToolUse Edit/Write) → "PARA. ¿Cumple los criterios documentados?"

5. Después de compactación
   ├── metacognicion.py → se reinyecta en cada prompt (persiste)
   └── .claude/criterios_[tarea].md → persiste en disco (recuperable)
```

### Pendiente

- **Prueba del ciclo completo** en un proyecto real con tarea real.

---

## Parte 9: Bloqueos en el MCP — Sugerir No Funciona, Bloquear Sí

### El problema persistente

Después de implementar el paso 0 en los skills, los hooks de metacognición en tres momentos, y las instrucciones en las respuestas del MCP, Claude seguía saltándose la comprensión y yendo directo a ejecutar. En pruebas con Tablero Digital:

- El skill `/arquitectura` tiene "ANTES DE TODO: COMPRENDER LA TAREA" al inicio — lo ignoró.
- El hook de metacognición inyecta "lee completo, reformula" en cada prompt — lo ignoró.
- La respuesta de `architecture_status` dice "Reformula al usuario lo que entiendes" — lo ignoró.

En todos los casos, Claude leyó la instrucción pero la inercia de "ya sé qué hacer, hay análisis previos, voy a leerlos y continuar" fue más fuerte.

### Descubrimiento: sugerir vs. bloquear

Cualquier instrucción que **sugiere** una acción se ignora frente a una instrucción que **produce** una acción concreta. "Reformula al usuario" es una sugerencia. "Usa `philosophy_architecture_status`" produce una llamada a herramienta. La segunda siempre gana.

La única forma que ha funcionado para cambiar el comportamiento es **bloquear**: devolver un error y no dejar continuar hasta que se cumpla el requisito. Esto funcionó con los fragmentos de código (validate bloqueado sin archivo completo) y se aplica ahora a los criterios.

### Lo que se implementó

#### Fixes en el validador (`server.py`)

**Fragmentos vs. archivo completo:**
- `step8_validate` ahora detecta si el código es un archivo completo (busca `extends`, `class_name`, `@tool`, `import`, `from`, `<!`)
- Si es un fragmento: **bloquea la validación**, no marca el paso 8 como completado, y pide el archivo completo
- El check de `extends` solo se evalúa si es archivo completo (evita falso positivo en fragmentos)

**Color hardcodeado:**
- Se quitó el regex estático `Color\s*\(\s*[\d.]+` de la lista de code_smells
- Se reemplazó por detección por línea en step8_validate que excluye líneas que empiezan con `const`, `var` o `@export` (uso legítimo en constantes nombradas)

#### Bloqueo por criterios en el MCP

**`architecture_analysis`** — Si no existe `.claude/criterios_[tarea].md`, **bloquea** el inicio del análisis. Pide que se cree primero con el usuario.

**`architecture_resume`** — Si no existe `.claude/criterios_*.md`, **bloquea** la retoma. Pide que se cree primero.

**`architecture_status`** — No bloquea (es consulta), pero la respuesta indica: "ANTES DE RETOMAR O INICIAR: reformula, verifica que existe criterios, solo entonces usa resume/analysis (se bloquearán sin criterios)".

Cuando los criterios sí existen:
- `architecture_analysis` muestra la ruta del archivo de criterios + "evalúa cada decisión contra los criterios"
- `architecture_resume` muestra la ruta + "lee los criterios y evalúa cada paso contra ellos"

### Por qué funciona el bloqueo

El bloqueo no depende de que Claude "decida" cumplir una instrucción. Es un mecanismo que impide la acción: no se puede iniciar, retomar ni validar sin cumplir los requisitos. La inercia de ejecución se encuentra con una barrera que no puede esquivar.

Esto es coherente con cómo funciona el MCP de filosofía: los pasos 1-9 se bloquean si saltas uno. El bloqueo por criterios extiende ese mismo principio al paso 0 de comprensión.

### Flujo actualizado con bloqueos

```
1. Inicio de sesión
   └── CLAUDE.md global → marco de principios (comprensión > ejecución)

2. Cada prompt del usuario
   ├── metacognicion.py (UserPromptSubmit) → "lee, reformula, verifica"
   └── planning_reminder.py (UserPromptSubmit, solo código) → filosofía encadenada

3. Inicio de tarea (/filosofia o /arquitectura)
   └── Paso 0: comprender → acordar con usuario → documentar criterios en .claude/criterios_[tarea].md
       └── SIN CRITERIOS → MCP BLOQUEA architecture_analysis y architecture_resume

4. Durante la ejecución
   ├── metacognicion.py (PreToolUse Edit/Write) → "PARA. ¿Responde a los criterios documentados?"
   └── metacognicion.py (PostToolUse Edit/Write) → "PARA. ¿Cumple los criterios documentados?"

5. Validación
   └── philosophy_validate → SIN ARCHIVO COMPLETO → BLOQUEA validación

6. Después de compactación
   ├── metacognicion.py → se reinyecta en cada prompt (persiste)
   └── .claude/criterios_[tarea].md → persiste en disco (recuperable)
   └── MCP sigue bloqueando sin criterios aunque se haya compactado
```

### Archivos modificados (actualización)

| Archivo | Qué hace |
|---------|----------|
| `~/.claude/CLAUDE.md` | Marco de principios con razones (global, se carga al inicio) |
| `~/.claude/settings.json` | Hooks globales (3 eventos: UserPromptSubmit, PreToolUse, PostToolUse) |
| `.claude/hooks/metacognicion.py` | Hook en 3 momentos: comprensión, antes de escribir, después de escribir |
| `.claude/hooks/planning_reminder.py` | Hook de filosofía de código con razonamiento encadenado |
| `.claude/settings.local.json` | Configuración de hooks del proyecto (3 eventos) |
| `filosofia/commands/arquitectura.md` | Skill con paso 0 al inicio + documentación de criterios |
| `filosofia/commands/filosofia.md` | Skill con paso 0 al inicio + documentación de criterios |
| `philosophy-mcp/server.py` | Bloqueo sin criterios (analysis, resume) + bloqueo sin archivo completo (validate) + fix Color inline |

---

> **"Máximo impacto, menor esfuerzo — a largo plazo"**
>
> Este documento es en sí un ejemplo del principio: parar a entender y documentar antes de actuar, para que todo lo que viene después sea más preciso y cueste menos.
