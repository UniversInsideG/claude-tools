# Sistema de Traduccion Adaptativa — Fundamentos

## QUE ES

Un sistema que traduce comunicaciones de UNIVERSINSIDE al estilo de procesamiento cognitivo de cada receptor. El contenido es el mismo; la representacion visual, la estructura y el tono se adaptan a como cada persona procesa mejor la informacion.

## POR QUE EXISTE

Cada cerebro procesa la informacion de forma diferente. Un documento corporativo presentado de la misma manera para todos:
- Es ignorado por quien necesita estimulo visual fuerte
- Es confuso para quien necesita secuencia clara
- Pierde impacto cuando no conecta con el procesamiento natural del receptor

La traduccion adaptativa resuelve esto: **el significado llega completo porque llega en el formato que el receptor puede absorber**.

## PRINCIPIOS

### 1. Fidelidad total al contenido
Todo lo que dice el documento original debe estar en la version adaptada. Sin omisiones, sin invenciones, sin resumenes que pierdan informacion. Si el original tiene 6 valores innegociables, la version adaptada tiene 6.

### 2. Tres capas, responsabilidades separadas

| Capa | Que es | Cambia? |
|------|--------|---------|
| **Estetica UNIVERSINSIDE** | Colores, tipografia, identidad de marca | Nunca |
| **Estructura visual personal** | Layout, SVGs, como se presenta la informacion | Fija por persona |
| **Adaptacion de contenido** | El texto adaptado al procesamiento del receptor | Cada documento |

### 3. El informe de procesamiento es la referencia
Cada persona tiene un informe de analisis cognitivo (HTML) que documenta como procesa informacion. Ese informe NO es una plantilla — es la referencia de estilo que guia COMO presentar informacion a esa persona.

### 4. La estructura del documento original se respeta
Las secciones, la jerarquia y la organizacion del documento original se mantienen. La adaptacion cambia como se PRESENTA cada seccion, no que secciones hay.

### 5. El analisis completo, no categorias reducidas
El "codigo de traduccion" de cada persona viene de su analisis cognitivo completo, no de una reduccion a categorias genericas. Las particularidades importan.

---

## CAPA 1: ESTETICA UNIVERSINSIDE

Constantes que aplican siempre:

| Elemento | Valor |
|----------|-------|
| Dorado principal | rgb(212, 175, 55) / #D4AF37 |
| Fondo claro | rgb(248, 248, 248) |
| Texto principal | rgb(51, 51, 51) |
| Texto secundario | rgb(102, 102, 102) |
| Tipografia | 'Segoe UI', system-ui, sans-serif |
| Estilo | Profesional, limpio, premium sin recargar |
| Firma | "Cecilia • CEO • UniversInside" |

---

## CAPA 2: PERFILES DE TRADUCCION (estructura visual fija por persona)

### Miguel — Visual-Analitico / Dashboard

**Como construye comprension:** Retiene 87% visual vs 50% textual. Procesa imagenes 3x mas rapido que texto. Patron: ve el grafico primero, luego lee texto breve para confirmar, integra. Hiper-observador: detecta sombras, proporciones, inconsistencias. Analiza ventajas estrategicas en todo.

**Que texto necesita:** Breve, claro, secuencialmente logico. Anclado a elementos visuales (graficos, barras, iconos). Datos cuantitativos dentro de SVGs, no como texto suelto. Badges de estado (fortaleza/debilidad). El texto es imprescindible para que lo visual tenga sentido, pero corto y concreto. En emails-tarea, cada tarea lleva un ancla visual distintiva que represente SU contenido especifico (SVG en HTML, emoji en email). No iconos genericos — iconos que anclen la tarea a una imagen mental concreta. Con 87% de retencion visual, el icono es lo que recuerda.

**Que lo desconecta:** Sobrecarga textual sin apoyo visual. Info pre-enlazada que quita libertad. Falta de datos especificos.

**Como organiza:** Dashboard con metricas arriba, patrones en grid, analisis, sintesis. Progresion secuencial entre secciones (barra de progreso), grid de cards dentro de cada una. Profundizacion via modales. Control personal (drag & drop).

**Presentacion:** Grid 1200px, fondo oscuro (rgb(15,15,30) -> rgb(25,25,50)), texto claro. Cards con SVG circulares, bar-charts, radar, timelines. Drag & drop, modales, hover con glow.

- **Referencia**: `data/references/miguel_processing_report.html`

### Celeste — Global/Circular con Precision

**Como construye comprension:** Necesita formato mixto imagen+texto con precision — "las dos juntas". Pide ejes, porcentajes, referencias claras. Elige vision global/circular sobre secuencial: "vision circular... muchisimo mas facil". Aprendizaje: Activo > Teorico > Reflexivo > Practico. Observadora detallada.

**Que texto necesita:** Mixto visual+texto donde cada concepto tiene soporte en ambas modalidades. Citas textuales como ancla. Datos cuantitativos SIEMPRE visibles. Titulos en diferentes colores para jerarquia — "para que mi cerebro no se vaya". Texto concreto y especifico. Instrucciones con pasos claros.

**Que la desconecta:** Falta de datos ("faltan datos"). Material poco atractivo ("tosco"). Bloques densos ("mi cerebro dice esto es un toscon"). Instrucciones insuficientes.

**Como organiza:** Vista de conjunto primero, navegacion circular con secciones. Agrupacion por naturaleza: clave -> limitantes -> patrones -> conclusion -> talentos -> revision. Cada aspecto: porcentaje + icono + titulo + cita textual + explicacion. Patrones como nodos numerados con progresion.

**Presentacion:** Grid 1400px, fondo oscuro (#003049 -> #001D3D), texto blanco. Cards con bordes de color, porcentajes en badges. Particulas animadas, hover con light-follow. Navegacion circular.

- **Referencia**: `data/references/celeste_processing_report.html`

### Cecilia — Global/Mind-map con Profundizacion

**Como construye comprension:** Tres fases: PRIMERO observa imagen/visual, LUEGO regresa al texto para confirmar, FINALMENTE reinterpreta y profundiza. Alta sensibilidad visual: detecta luz, contrastes, disposicion espacial, patrones de color. Las imagenes son su "lienzo mental". Asocia, busca relaciones, optimiza. Vocabulario reflexivo: "me doy cuenta", "veo que", "me fijo".

**Que texto necesita:** Cada bloque de texto precedido por un ancla visual (su secuencia es imagen -> texto -> reinterpretacion). Highlights con color para datos clave. Texto que permita asociar conceptos entre si, no datos aislados. Cards con listas que conecten ideas.

**Que la desconecta:** Dependencia de luminosidad — si algo importante no esta destacado visualmente, lo pierde. Homogeneidad visual — pierde concentracion cuando todo es del mismo tono. Necesita CONTRASTE y VARIACION de color. Exceso de color en texto — si muchas palabras son de colores, no puede priorizar la informacion visual; el color va en la ESTRUCTURA (cards, bordes, lineas), no en el texto corrido. Solo datos verdaderamente criticos se destacan con color en el texto.

**Como organiza:** Mapa mental: concepto central con ramas. Navega por interes, no orden lineal. Profundizacion on-demand (click to expand). Cada rama con color neon propio. Conexiones visibles entre conceptos (lineas SVG).

**Presentacion:** Mind-map 1400px, fondo NEGRO (#0a0a0a) que maximice contraste. Colores neon luminosos para nodos, bordes y highlights que permitan organizar la informacion de un vistazo. Glow en bordes y hover. Paneles expandibles.

- **Referencia**: `data/references/cecilia_processing_report.html`

### Jesus — Visual-Secuencial / Flujo Contextualizado

**Como construye comprension:** Dos fases: PRIMERO ve el panorama completo de un vistazo ("De un vistazo aprecio toda la informacion", "De un vistazo veo todo el proceso"), LUEGO profundiza secuencialmente. Necesita el marco general antes de los detalles: "prefieres entender primero el marco general antes de pasar a la accion". Su 0% global NO significa que no necesite vision de conjunto — significa que esa vision debe estar ESTRUCTURADA. Tambien necesita CONTEXTO antes de cada pieza individual: "En las imagenes me falta contexto", "Una vez conozco el contexto, y sabiendo que representan las imagenes, me resulta mas facil". Memoria visual 16/16 (100%) vs textual 9/16 (56%), preferencia visual 5/6 (83%) vs textual 2/6 (33%). Procesamiento 100% secuencial (3/3) — el orden es requisito, no preferencia. Aprendizaje: teorizar -> reflexionar -> practicar -> actuar. Detecta capas/planos, agrupa elementos diversos en unidades cohesionadas, usa el contraste para organizar.

**Que texto necesita:** Breve y funcional — el texto establece el contexto que activa su canal visual, no es el canal principal. Cada bloque de texto enmarca lo que va a ver: titulo + descripcion corta antes del elemento visual. Estructura clara: titulo -> cita -> explicacion. Secuencial, ordenado, paso a paso. Datos concretos anclados a visuales (porcentajes dentro de graficos, no como texto suelto). El texto puro sin apoyo visual le cuesta: "El texto puro no es tu formato optimo".

**Que lo desconecta:** Falta de contexto — informacion visual sin marco de referencia pierde eficacia incluso siendo su canal fuerte. Informacion no lineal o desordenada — con 0/3 en procesamiento global, la informacion sin estructura clara le genera friccion directa. Texto denso sin apoyo visual — con 2/6 en preferencia textual y 9/16 en memoria textual, bloques de texto largo sin elementos graficos le cuestan el doble de esfuerzo. Ambiguedad — necesita saber que esta mirando y por que.

**Como organiza:** DOS NIVELES: primero una vision de conjunto que muestre TODO el alcance del documento de un vistazo (resumen visual, tabla, o seccion de contexto que enumere las partes), y DESPUES las secciones detalladas en orden secuencial. El overview no es opcional — sin el, las secciones pierden el marco. Flujo secuencial de arriba a abajo para las secciones detalladas. Dentro de cada seccion: contexto primero, luego datos visuales, luego interpretacion. Cards en layout horizontal: caja de icono a la izquierda + (titulo + cita + descripcion) a la derecha. Conexiones entre secciones con flechas/conectores que expliciten la progresion. Agrupa por capas: "Hay cuatro planos". Busca unidad: "A pesar de su diversidad ofrecen una sensacion de bloque, de unidad". Usa contraste para distinguir: "Tres arboles de vivos colores reflejan un gran contraste".

**Presentacion:** Estructura de dos niveles: contenedores `.seccion` BLANCOS (rgb(255,255,255), border-radius 12px, padding 32px, box-shadow) que agrupan cards hijas con fondo GRIS (rgb(248,248,248)). Cards en layout HORIZONTAL (flex, gap 20px): caja de icono 56x56 blanca con sombra a la izquierda, contenido a la derecha. Cards positivas con border-left 4px dorado, negativas con fondo rosado rgb(255,250,250) y border-left rojo. Badges de seccion 48x48 gradiente dorado->dorado claro rgb(245,215,110). Flechas SVG entre secciones (stroke-width 3, opacidad 0.4). Citas italic sin fondo, border-left 2px. Cero interactividad. Responsive a 768px. Referencia CSS exacta: `data/references/jesus_processing_report.html`.

- **Referencia**: `data/references/jesus_processing_report.html`

---

## CAPA 3: ADAPTACION DE CONTENIDO

### Reglas de fidelidad
1. **Completitud**: Si el original tiene N puntos, la adaptacion tiene N puntos
2. **Significado**: Cada punto dice lo mismo, con las mismas implicaciones
3. **Estructura**: Las secciones del original se preservan
4. **Sin invencion**: No anadir datos, ejemplos o informacion no presentes en el original
5. **Sin omision**: No saltar contenido por largo o complejo que sea

### Reglas de contraste y accesibilidad
- Texto oscuro sobre fondo claro: ratio minimo 4.5:1
- Texto claro sobre fondo oscuro: ratio minimo 4.5:1
- NUNCA texto gris claro sobre fondo claro
- NUNCA texto dorado sobre fondo blanco sin borde/sombra de apoyo
- Los iconos/SVGs/emojis son COMPLEMENTO del texto, no sustitutos
- Toda imagen o icono critico debe tener texto de contexto visible
- Badges de datos (tiempos, porcentajes, etiquetas) NUNCA con posicion absoluta dentro de cards — deben fluir con el contenido para no solaparse con titulos o texto

### Adaptacion por medio de entrega

| Medio | Formato | Restricciones |
|-------|---------|---------------|
| **Documento HTML** | HTML completo con CSS, SVG, JS | Sin restricciones |
| **Email** | HTML simplificado, CSS inline | Sin JS, sin animaciones, ancho max 600px |
| **Signal** | Texto plano con formato basico | Sin HTML, solo estructura con lineas y emojis |

---

## TIPOS DE COMUNICACION

| Tipo | Descripcion | Ejemplo |
|------|-------------|---------|
| comunicacion_oficial | Decisiones de direccion, politicas | Comunicado de estructura de empresa |
| cultura_corporativa | Valores, innegociables, principios | Codigo de cultura corporativa |
| email_tarea | Peticiones, coordinacion, informes | Solicitud de reporte semanal |
| feedback | Evaluaciones, reconocimientos | Devolucion de desempeno |

---

## AÑADIR NUEVOS PERFILES

El proceso para incorporar a una nueva persona esta documentado paso a paso en `COMO_AÑADIR_PERFIL.md`, incluyendo los errores cometidos con los tres perfiles existentes y como se resolvieron.

---

## ARCHIVOS DE REFERENCIA

```
data/references/
├── miguel_processing_report.html    # Informe cognitivo Miguel (completo)
├── celeste_processing_report.html   # Informe cognitivo Celeste (completo, 1123 lineas)
├── cecilia_processing_report.html   # Informe cognitivo Cecilia (completo, 607 lineas)
├── jesus_processing_report.html     # Informe cognitivo Jesus (completo)
└── miguel_raw_data.json             # Datos brutos del test de Miguel
```

---

## INVOCACION

El sistema se usa como skill de Claude Code:

```
/traduccion [mensaje o ruta del mensaje]
```

Sigue un protocolo interactivo: identifica mensaje, receptor, medio, y genera la adaptacion.
