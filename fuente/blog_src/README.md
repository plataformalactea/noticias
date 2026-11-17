# Datos del blog (www.plataformalactea.com/blog.html)

Todo el contenido del blog sale de estos archivos JSON. Para publicar un cambio:

```
cd /home/claude/noticias            # raíz del repositorio
# 1. editar los JSON de fuente/blog_src/
bash fuente/actualizar_web.sh        # reconstruye la web completa en sitio/ (1–3 min)
git add -A && git commit -m "..." && git push origin main
# 2. GitHub sube lo cambiado al hosting por FTPS y escribe el resultado en registro/ftp.txt
```

Reglas comunes a todos los archivos:

- Todo texto visible lleva las 4 lenguas: `{"es": "...", "en": "...", "fr": "...", "pt": "..."}` (portugués de Portugal).
- Formato numérico de cada idioma dentro de los textos: ES/PT `3.710 €/t`, `2,9 %`; EN `€3,710/t`, `2.9%`; FR `3 710 €/t`, `2,9 %`.
- Fechas cortas: es `11 nov 2026` · en `11 Nov 2026` · fr `11 nov. 2026` · pt `11 nov. 2026`.
  Meses: ene/Jan/janv./jan. · feb/Feb/févr./fev. · mar/Mar/mars/mar. · abr/Apr/avr./abr. · may/May/mai/maio · jun/Jun/juin/jun. · jul/Jul/juil./jul. · ago/Aug/août/ago. · sep/Sep/sept./set. · oct/Oct/oct./out. · nov/Nov/nov./nov. · dic/Dec/déc./dez.
- Los números de las cotizaciones y de las tablas de cabra/oveja se escriben como números (no texto): el programa los formatea en cada idioma y calcula conversiones.
- Solo información de interés para el sector lácteo publicada por medios u organismos; nunca publicidad ni notas de prensa de marcas (lanzamientos de producto, campañas…).
- Redactar con palabras propias, sin copiar frases de la fuente; no inventar ni redondear cifras.
- `url` siempre la de la noticia o informe original.

## aldia.json — sección «Al día» (diaria)

Lista. Se muestran las noticias con `recibido` de los últimos 7 días (las antiguas no se borran).

```json
{"id": "2026-11-17-palabras-clave", "recibido": "2026-11-17",
 "fecha": {"es": "16 nov 2026", "en": "16 Nov 2026", "fr": "16 nov. 2026", "pt": "16 nov. 2026"},
 "fuente": "Vaca Pinta", "url": "https://...",
 "titulo": {"es": "...", "en": "...", "fr": "...", "pt": "..."},
 "texto":  {"es": "1–2 frases, máx. ~280 caracteres", "en": "...", "fr": "...", "pt": "..."}}
```

`recibido` = día en que se añade; `fecha` = fecha de publicación de la noticia. No duplicar (misma url o id).

## semana.json — resumen semanal (cada lunes, sobre la semana anterior de lunes a domingo)

```json
{"semana": {"numero": 46, "fecha": "2026-11-16",
            "rango": {"es": "9 – 15 de noviembre de 2026", "en": "9–15 November 2026", "fr": "9–15 novembre 2026", "pt": "9–15 de novembro de 2026"}},
 "noticias": [ { "cat": "Precios", "fecha": {...}, "dato": {...}, "dato_pie": {...}, "titulo": {...}, "texto": {...}, "fuente": "Vaca Pinta", "url": "https://..." } ]}
```

- `cat`: una de `Precios`, `Mercados`, `Normativa`, `Novedades`.
- `dato`: la cifra clave en grande (p. ej. `0,474 €/l`, `+3 %`, `−5,5 cts`); `dato_pie`: qué es esa cifra (pocas palabras).
- Entre 6 y 10 noticias, ordenadas por relevancia: las 3 primeras salen también en la página de inicio.
- `numero` = número de semana ISO de la semana resumida.

## cotizaciones.json — cuadro «Cotizaciones de referencia»

```json
{"semana": 46, "actualizado": {"es": "17 nov 2026", ...}, "filas": [...], "nota": {...}}
```

Tipos de fila (el orden de la lista es el orden en pantalla):

- `num`: `{"tipo": "num", "id": "smp" (opcional), "producto": {...}, "valor": 3710, "dec": 0, "unidad": "€/t", "cambio": 20, "detalle": {...}}`
  - `unidad`: `€/t`, `€/kg`, `€/l`, `€/1000l`. `dec`: decimales de valor y cambio (0 por defecto; 3 para €/l).
  - `cambio`: variación frente al dato anterior de la misma fuente, en la misma unidad (0 = sin cambios; `"est"` = estimación).
- `proteina`: `{"tipo": "proteina", "de": "smp", "proteina": 34, ...}` → valor por kg de proteína calculado de la fila con ese id (precio ÷ 0,34). No tocar salvo textos.
- `nata`: `{"tipo": "nata", "precio": 1940, "grasa": 40, "cambio": 0, "origen": {...}}` → se muestra en base 100 % grasa (precio ÷ grasa). `precio` y `cambio` son de la nata tal cual (€/t).

Fuentes habituales: ZuivelNL (mantequilla, leches en polvo, suero; se publica los miércoles: https://www.zuivelnl.org/marktinformatie/zuivelnoteringen, €/100 kg → ×10 para €/t), Bolsa de Milán/Verona (nata, leche spot; semanal), Ministerio de Agricultura (informe semanal de coyuntura: nata 30 % a granel; con 4–6 semanas de retraso), FEGA (precio medio mensual de la leche de vaca), Lonja de León (leche de vaca pactada por trimestre). Al cambiar una fuente o su fecha, actualizar también `nota` y el `detalle` de la fila.

## temporada.json — apartados «Leche de cabra» y «Leche de oveja»

`{"cabra": {...}, "oveja": {...}}`, cada uno con `titulo`, `subtitulo`, `nota`, `lectura` (textos), `tabla` y `noticias`:

- `tabla`: `{"ref": {...}, "det": {...}, "litro": 1.047, "punto": 0.1317, "eq": 7.95}` — precio por litro (€/l), por punto de extracto quesero (€) y extracto quesero (%). Si falta uno se pone `null` y se calcula de los otros dos (se muestra con «≈»).
- `noticias`: `{"fecha": {...}, "texto": {...}, "fuente": "...", "url": "..."}` — tendencias, previsiones, producción. Expresar los precios por punto de extracto quesero junto al €/l.
- Fuentes: Ministerio de Agricultura, informe mensual de entregas de ovino y caprino (https://www.mapa.gob.es/es/ganaderia/temas/produccion-y-mercados-ganaderos/sectores-ganaderos/ovino-caprino/leche-de-oveja-y-cabra/informes-declaraciones-obligatorias-de-leche-por-primeros-compradores), Lonja de León (leche de oveja y cabra), Idele/Réussir (Francia).
