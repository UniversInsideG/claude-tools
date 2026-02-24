# /traduccion — Traduccion Adaptativa UNIVERSINSIDE

Skill de Claude Code que traduce comunicaciones al estilo de procesamiento cognitivo de cada receptor. El contenido es el mismo; la representacion visual, la estructura y el tono se adaptan a como cada persona procesa mejor la informacion.

## Instalacion

### Mac / Linux

```bash
git clone git@github.com:UniversInsideG/claude-tools.git
cd claude-tools/traduccion-adaptativa
./install_mac.sh
```

### Windows (PowerShell)

```powershell
git clone git@github.com:UniversInsideG/claude-tools.git
cd claude-tools\traduccion-adaptativa
.\install_windows.ps1
```

Si Claude Code estaba abierto, reinicialo para que cargue la skill.

## Uso

```
/traduccion [mensaje o instrucciones]
```

Si no especificas nada, te pregunta:
1. Que mensaje quieres traducir (pega el texto o indica un archivo)
2. Para quien (Miguel / Celeste / Cecilia)
3. En que formato (HTML documento / Email / Signal)

### Ejemplos

```
/traduccion traduce el archivo /tmp/comunicado.txt para Miguel como email
```

```
/traduccion Buenos dias, os adjunto el documento de cultura corporativa. Revisadlo por favor. — para Celeste, email
```

## Receptores disponibles

| Receptor | Procesamiento | Estructura |
|----------|--------------|------------|
| **Miguel** | Visual-analitico | Dashboard: cards con SVGs, barras, metricas. Fondo oscuro. Texto breve anclado a visuales |
| **Celeste** | Global/circular con precision | Grid de cards con navegacion circular. Fondo azul oscuro. Mixto visual+texto con datos cuantitativos |
| **Cecilia** | Global/mind-map | Mapa mental con ramas expandibles. Fondo negro con neon. Color en estructura, texto neutro |

## Formatos de salida

| Formato | Uso | Restricciones |
|---------|-----|---------------|
| **HTML documento** | Leer en navegador | Completo: CSS, SVG, JS, interactividad |
| **Email** | Pegar en cliente de email | CSS inline, sin JS, max 600px, solo emojis unicode |
| **Signal** | Mensaje de texto | Texto plano con estructura basica |

## Que instala

```
~/.claude/
  commands/
    traduccion.md                          <- la skill
  traduccion-adaptativa/
    FUNDAMENTOS.md                         <- principios del sistema
    COMO_AÑADIR_PERFIL.md                  <- guia para nuevos perfiles
    data/references/
      miguel_processing_report.html        <- informe cognitivo Miguel
      celeste_processing_report.html       <- informe cognitivo Celeste
      cecilia_processing_report.html       <- informe cognitivo Cecilia
```

No modifica ni borra ningun archivo existente en `~/.claude/`.

## Añadir nuevos perfiles

Para incorporar a una nueva persona (ej: Jesus), sigue la guia en `COMO_AÑADIR_PERFIL.md`. Requiere un informe de procesamiento cognitivo (HTML del test) de la persona.

## Documentacion

- `FUNDAMENTOS.md` — Principios completos del sistema de traduccion
- `COMO_AÑADIR_PERFIL.md` — Proceso paso a paso para nuevos perfiles, con errores documentados y correcciones
