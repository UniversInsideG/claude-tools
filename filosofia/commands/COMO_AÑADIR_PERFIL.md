# Como Añadir un Nuevo Perfil de Traduccion

Guia paso a paso para incorporar a una nueva persona al sistema de traduccion adaptativa. Documenta el proceso que se siguio con Miguel, Celeste y Cecilia, incluyendo los errores cometidos y las correcciones que los resolvieron.

---

## Que necesitas antes de empezar

**Un informe de procesamiento cognitivo** de la persona (HTML generado a partir de un test de analisis cognitivo). Este informe es la fuente de verdad. Sin el, no hay perfil — no se puede inventar como procesa alguien.

El informe debe contener:
- Como recuerda (memoria visual vs textual, con datos)
- Como organiza la informacion (lineal, circular, asociativa...)
- Que formato prefiere (visual, texto, mixto)
- Que la conecta y que la desconecta
- Preferencias de aprendizaje
- Citas textuales de la persona durante el test

**Ejemplo**: los informes existentes estan en `data/references/{nombre}_processing_report.html`

---

## Paso 1 — Guardar el informe de referencia

Copiar el HTML del informe cognitivo a:

```
data/references/{nombre}_processing_report.html
```

**Verificar** que el archivo esta completo. En el caso de Miguel, el primer archivo tenia solo 435 lineas (truncado) y genero un perfil incorrecto. El archivo completo tiene ~700 lineas y revelo un patron de procesamiento completamente diferente al asumido.

**Leccion**: un informe incompleto produce un perfil incorrecto. Verificar que el HTML se renderiza completo en el navegador antes de continuar.

---

## Paso 2 — Leer el informe completo y extraer dos dimensiones

Leer el HTML renderizado y el codigo fuente. Extraer DOS dimensiones:

### Dimension visual (como se VE la informacion)
- Layout general (ancho, grid, cards, paneles)
- Fondo (oscuro, claro, gradiente, color especifico)
- Paleta de colores usada en el informe
- Elementos graficos (SVGs, barras, badges, iconos)
- Nivel de interactividad (hover, click, drag, modales)

### Dimension organizativa (como se ESTRUCTURA la informacion)
- Que va primero, que va despues
- Como se agrupan los conceptos (por naturaleza, por secuencia, por relacion)
- Como se profundiza (modales, expandibles, click to reveal)
- Como se navega entre secciones (lineal, circular, libre)
- Que relacion tienen las secciones entre si

**Leccion**: en la primera version de los perfiles solo se extrajo la dimension visual (colores, layout, CSS). Faltaba la organizativa. El resultado era un HTML bonito pero mal estructurado para el receptor. Ambas dimensiones son igualmente importantes.

---

## Paso 3 — Redactar el perfil con 5 secciones obligatorias

Cada perfil tiene exactamente estas 5 secciones. No se reduce a bullet points superficiales — se describe el procesamiento real de la persona con evidencia del informe.

### 1. Como construye comprension
Describe el PATRON COMPLETO de como la persona integra informacion. No basta con "visual" o "textual" — hay que especificar la secuencia, las fases, y que pasa en cada una.

**Ejemplo bueno** (Cecilia): "Tres fases: PRIMERO observa imagen/visual, LUEGO regresa al texto para confirmar, FINALMENTE reinterpreta y profundiza."

**Ejemplo malo**: "Procesamiento visual-asociativo." (Esto no dice nada actionable.)

### 2. Que texto necesita
El texto NUNCA desaparece. Incluso para perfiles altamente visuales, el texto es imprescindible para que lo visual tenga sentido. Esta seccion define que tipo de texto, que longitud, como se relaciona con los elementos visuales.

**Leccion**: en un intento con Miguel se elimino casi todo el texto, dejando solo visuales. El resultado era incomprensible. El texto breve, claro y anclado a elementos visuales es lo que Miguel necesita — no la ausencia de texto.

### 3. Que lo/la desconecta
Los anti-patrones especificos que hacen que la persona pierda interes o no pueda procesar. Con citas textuales del informe cuando sea posible.

**Leccion importante sobre el color** (Cecilia): el exceso de color en el TEXTO impide priorizar la informacion visual. El color va en la ESTRUCTURA (cards, bordes, lineas). El texto corrido se mantiene neutro. Solo datos verdaderamente criticos se destacan con color en el texto. Esta regla surgio de una correccion directa de la usuario tras ver una version con demasiados spans coloreados.

### 4. Como organiza la informacion
La estructura que la persona necesita para navegar y entender. No es como "queda bonito" sino como PIENSA.

### 5. Presentacion visual
Especificaciones concretas: ancho, fondo, colores, tipos de cards, elementos interactivos.

**Leccion sobre preferencias vs informe**: el informe de Cecilia usaba fondo purpura, pero Cecilia explicitamente dijo que no le gustaban los fondos purpura. Prefiere negro con colores neon. **Siempre preguntar a la persona** — el informe es referencia, pero las preferencias directas tienen prioridad.

---

## Paso 4 — Incorporar el perfil al sistema

El perfil se escribe en DOS archivos:

### 1. FUNDAMENTOS.md
Seccion "CAPA 2: PERFILES DE TRADUCCION". Añadir el nuevo perfil con las 5 secciones, siguiendo el mismo formato de los existentes. Incluir la referencia al archivo HTML.

### 2. traduccion.md (skill)
Seccion "Capa 2: Estructura visual Y organizativa". Añadir el perfil completo con mas detalle que en FUNDAMENTOS (el skill es la guia operativa, los fundamentos son la referencia).

Tambien añadir al receptor en:
- Paso 2 del protocolo (lista de receptores)
- Capa 3 (como se adapta el contenido para esta persona)

---

## Paso 5 — Validar con un documento real

Traducir un documento REAL (no inventado) para la nueva persona. Preferiblemente un email-tarea (corto, rapido de evaluar) y luego un documento completo (largo, con muchas secciones).

### Checklist de validacion

**Fidelidad:**
- [ ] Todo el contenido del original esta en la adaptacion
- [ ] No se ha inventado informacion
- [ ] Las secciones mantienen el orden logico del original

**Visual:**
- [ ] El layout sigue el patron del perfil
- [ ] Los colores coinciden con la paleta definida
- [ ] El contraste es legible (ratio 4.5:1 minimo)
- [ ] Los badges de datos no se solapan con titulos (fluyen con el contenido)
- [ ] El color esta en la estructura, no saturando el texto

**Organizativa:**
- [ ] La informacion se agrupa como indica el perfil
- [ ] La navegacion/profundizacion funciona segun el perfil
- [ ] El texto tiene la densidad correcta para el receptor

**Formato:**
- [ ] Si es HTML: autocontenido, sin dependencias externas
- [ ] Si es email: CSS inline, sin JS, max 600px, solo emojis unicode
- [ ] Si es Signal: texto plano con estructura basica

---

## Paso 6 — Iterar con feedback de la persona

Este paso es CRITICO. Los tres perfiles existentes requirieron multiples correcciones:

| Persona | Error inicial | Correccion |
|---------|--------------|------------|
| Miguel | Asumido como secuencial-claro | Es visual-analitico/dashboard/oscuro |
| Miguel | Texto eliminado casi por completo | Texto breve pero imprescindible |
| Celeste | Solo patrones visuales extraidos | Añadida dimension organizativa |
| Cecilia | Fondo purpura (del informe) | Negro con neon (preferencia directa) |
| Cecilia | Exceso de color en texto | Color en estructura, texto neutro |

**Cada correccion de la persona se incorpora al perfil y a las reglas generales del sistema** (FUNDAMENTOS.md y traduccion.md). Asi el sistema mejora con cada iteracion.

---

## Resumen: archivos a crear para un nuevo perfil

```
1. data/references/{nombre}_processing_report.html  ← informe cognitivo (fuente de verdad)
2. FUNDAMENTOS.md                                    ← añadir perfil en Capa 2
3. ~/.claude/commands/traduccion.md                  ← añadir perfil en Capa 2 + receptor en protocolo
4. data/adapted/{tipo}_{nombre}_{fecha}.html         ← traducciones de prueba para validar
```

---

## Ejemplo rapido: añadir a Jesus

```
1. Obtener el informe cognitivo de Jesus (HTML del test)
2. Guardarlo en data/references/jesus_processing_report.html
3. Leer el informe y extraer dimension visual + organizativa
4. Redactar las 5 secciones del perfil
5. Incorporar a FUNDAMENTOS.md y traduccion.md
6. Traducir un email corto y un documento largo para Jesus
7. Que Jesus (o alguien que lo conozca) revise y corrija
8. Incorporar correcciones al perfil y a las reglas generales
```
