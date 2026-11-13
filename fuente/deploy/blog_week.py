"""Genera el contenido de la pestaña Blog a partir de los datos de la semana.
Escribe: web/project/Blog.dc.html (sección de noticias) y blog_src/noticias.json."""
import json, html as H, re
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
SRC = B + 'web/project/Blog.dc.html'

# Fuentes que se revisan cada semana (elegidas por Miguel Ángel)
FUENTES = [
    ('Vaca Pinta', 'https://www.vacapinta.com/es/es-la-leche.html'),
    ('Agroinformación – vacuno de leche', 'https://www.agroinformacion.com/category/ganaderia/vacuno-de-leche/'),
    ('MAPA – vacuno lechero', 'https://www.mapa.gob.es/es/ganaderia/temas/produccion-y-mercados-ganaderos/sectores-ganaderos/vacuno-de-leche'),
    ('eDairy News (España y Europa; se descarta Latinoamérica)', 'https://es.edairynews.com/'),
    ('EEX (solo enlace)', 'https://www.eex.com/en/markets/agriculturals'),
]

SEMANA = {'numero': 45, 'rango': '2 – 8 de noviembre de 2026', 'actualizado': '9 nov 2026', 'fecha': '2026-11-09'}

DESTACADO = {
    'cat': 'Precios', 'fecha': '3 nov 2026', 'dato': '0,474 €/l', 'dato_pie': 'precio medio leche de vaca · septiembre',
    'titulo': 'La leche cruda sube por segundo mes seguido y se paga a 0,474 €/litro en septiembre',
    'texto': ['Según las declaraciones de entregas al Ministerio de Agricultura, el precio medio en España pasó de 0,469 €/l en agosto a 0,474 €/l en septiembre, después de marcar en julio el mínimo del año (0,465 €/l).',
              'Las entregas sumaron 596.601 toneladas, un 1,4 % más, y de enero a septiembre alcanzan unos 5.695 millones de kilos (+1,7 %). Por regiones: Galicia 0,455 €/l, Castilla y León 0,487 €/l, Cantabria 0,496 €/l y País Vasco 0,502 €/l.'],
    'fuente': 'Vaca Pinta', 'url': 'https://vacapinta.com/es/mercados/el-precio-medio-de-la-leche-en-espana-repunta-y-al.html',
}

NOTICIAS = [
    {'cat': 'Mercados', 'fecha': '3 nov 2026', 'dato': '+3 %', 'dato_pie': 'índice GDT',
     'titulo': 'Subasta de Fonterra: tercera subida seguida, con las leches en polvo al alza',
     'texto': 'Leche entera en polvo +5,9 % (3.971 $/t), desnatada +3,1 % (4.109 $/t), cheddar +8,6 % y mozzarella +5,8 %. La mantequilla baja un 4,7 % (4.503 $/t). Precio medio: 4.166 $/t.',
     'fuente': 'Vaca Pinta', 'url': 'https://vacapinta.com/es/mercados/el-indice-de-precios-de-fonterra-sube-un-3-en-novi.html'},
    {'cat': 'Precios', 'fecha': '4 nov 2026', 'dato': '371 €', 'dato_pie': 'desnatada en polvo · €/100 kg',
     'titulo': 'Holanda: las leches en polvo y la mantequilla siguen subiendo',
     'texto': 'Cotización ZuivelNL de la semana 45: mantequilla 375 €/100 kg (+3), leche entera en polvo 384 (+3), desnatada para consumo humano 371 (+2) y suero en polvo 164 (sin cambios).',
     'fuente': 'ZuivelNL', 'url': 'https://www.zuivelnl.org/marktinformatie/zuivelnoteringen'},
    {'cat': 'Mercados', 'fecha': '6 nov 2026', 'dato': '−2,5 %', 'dato_pie': 'mantequilla UE · referencia semanal',
     'titulo': 'Europa: la leche en polvo gana fuerza y la mantequilla pierde impulso',
     'texto': 'Referencia de la UE (26 oct–1 nov): leche desnatada en polvo 3.427 €/t (+0,4 %) y mantequilla 3.957 €/t (−2,5 %). En el mercado al contado, la desnatada para consumo humano sube 50 €, hasta 3.715 €/t.',
     'fuente': 'eDairy News', 'url': 'https://es.edairynews.com/la-leche-en-polvo-gana-fuerza-manteca-pierde/'},
    {'cat': 'Precios', 'fecha': '4 nov 2026', 'dato': '−5,5 cts', 'dato_pie': 'por litro frente a sept. 2025',
     'titulo': 'España produce más leche, pero la paga 5,5 céntimos menos que hace un año',
     'texto': 'Los 47,4 céntimos de septiembre son un 10,4 % menos que en 2025 y el precio de septiembre más bajo desde 2022. Las entregas suben un 1,7 % en el año y quedan 8.395 ganaderías, 373 menos que en diciembre.',
     'fuente': 'eDairy News', 'url': 'https://es.edairynews.com/espana-produce-mas-leche-pero-paga-55-centimos-menos-por-litro/'},
    {'cat': 'Precios', 'fecha': '3 nov 2026', 'dato': '+2–3 cts', 'dato_pie': 'propuesta en Galicia desde el 1 dic',
     'titulo': 'Galicia: las industrias proponen subir la leche 2 o 3 céntimos desde diciembre',
     'texto': 'Tras recortar 7–8 céntimos en abril, el precio quedó algo por debajo de 45 céntimos. Los ganaderos ven la subida insuficiente: los costes (gasóleo, abonos, electricidad) suben y se espera pienso más caro desde enero.',
     'fuente': 'eDairy News', 'url': 'https://es.edairynews.com/galicia-la-leche-subiria-hasta-3/'},
    {'cat': 'Precios', 'fecha': '26 oct 2026', 'dato': '47,00 €', 'dato_pie': 'FrieslandCampina · €/100 kg',
     'titulo': 'FrieslandCampina sube por cuarto mes el precio de la leche para noviembre',
     'texto': 'El precio garantizado de noviembre queda en 47,00 €/100 kg, 1,50 € más que en octubre. La cooperativa lo atribuye sobre todo a la firmeza del mercado de proteínas.',
     'fuente': 'Vaca Pinta', 'url': 'https://vacapinta.com/es/mercados/frieslandcampina-mejora-precio-leche-cuarto-mes-co.html'},
    {'cat': 'Novedades', 'fecha': '4 nov 2026', 'dato': '+30 %', 'dato_pie': 'demanda cubierta con importaciones',
     'titulo': 'FeNIL propone ocho medidas para reforzar la industria láctea española',
     'texto': 'Las importaciones cubren ya más del 30 % de la demanda y el déficit comercial lácteo (492.355 t y 1.500 M€) es el mayor de la UE. En quesos, España importó 434.844 t y exportó 131.696 t.',
     'fuente': 'FeNIL', 'url': 'https://fenil.org/reforzar-la-industria-lactea-es-reforzar-la-autonomia-alimentaria-de-espana-fenil-propone-ocho-medidas-para-impulsar-el-futuro-del-sector/'},
    {'cat': 'Normativa', 'fecha': '5 nov 2026', 'dato': '1 nov', 'dato_pie': 'en vigor',
     'titulo': 'Lengua azul y EHE: nuevo protocolo para mover ganado',
     'texto': 'El Ministerio sustituye las restricciones por zonas por una evaluación de riesgo basada en vacunación, pruebas diagnósticas y protección frente a vectores. Afecta a vacuno y ovino, también en movimientos a otros países de la UE.',
     'fuente': 'Agroinformación', 'url': 'https://agroinformacion.com/el-ministerio-actualiza-el-protocolo-de-movimientos-para-lengua-azul-y-ehe-con-nuevas-condiciones-para-el-traslado-de-ganado/'},
    {'cat': 'Normativa', 'fecha': '5 nov 2026', 'dato': '−10 %', 'dato_pie': 'rendimiento neto agrario',
     'titulo': 'Módulos del IRPF 2027: rebaja general del 10 % para la actividad agraria',
     'texto': 'Hacienda publica en el BOE la orden de módulos para 2027, con una reducción general del 10 % del rendimiento neto de las actividades agrarias.',
     'fuente': 'Agroinformación', 'url': 'https://agroinformacion.com/publicada-en-el-boe-la-orden-de-modulos-del-irpf-2027-con-una-reduccion-general-del-10-del-rendimiento-neto-a-la-actividad-agraria/'},
    {'cat': 'Novedades', 'fecha': '8 nov 2026', 'dato': '80 €/kg', 'dato_pie': 'Gamonéu del Puertu en tienda',
     'titulo': 'El Gamonéu del Puertu, un queso de 80 € el kilo que lucha por sobrevivir',
     'texto': 'Este queso asturiano con DOP, de leche cruda de vaca, oveja y cabra, solo tiene tres productores. Nuevos queseros llevan años sin lograr permisos para abrir queserías en los Picos de Europa.',
     'fuente': 'eDairy News', 'url': 'https://es.edairynews.com/el-queso-de-80-euros-el-kilo-q-lucha-sobrevivir-espana/'},
]

# Nata: se introduce el precio de la nata (€/t), su % de grasa y su variación semanal (€/t);
# la fila se convierte automáticamente a base 100 % grasa (precio / % grasa).
def _eur(n): return f"{round(n):,}".replace(',', '.')
def _var(n, unidad='€/t'): return '=' if n == 0 else (f'+{n} {unidad}' if n > 0 else f'−{-n} {unidad}')
def nata_fila(nombre, precio, grasa, cambio, origen):
    f = grasa / 100
    return (nombre, f'{_eur(precio / f)} €/t', _var(round(cambio / f)), f'{origen} · nata {grasa} % a {_eur(precio)} €/t')

# Leche desnatada en polvo (€/t) y variación: de aquí sale automáticamente el valor de la proteína (34 %).
SMP, SMP_CAMBIO = 3710, 20
def _kg(x): return f"{x:.2f}".replace('.', ',')
def proteina_fila():
    v, c = SMP / 0.34 / 1000, SMP_CAMBIO / 0.34 / 1000
    var = '=' if round(c, 2) == 0 else (f'+{_kg(c)} €/kg' if c > 0 else f'−{_kg(-c)} €/kg')
    return ('Proteína · valor por kg', f'{_kg(v)} €/kg', var, 'base leche desnatada en polvo (34 % proteína)')

COTIZ = [  # producto, precio, cambio (con unidad), detalle
    ('Leche desnatada en polvo', f'{_eur(SMP)} €/t', _var(SMP_CAMBIO), 'Holanda'),
    proteina_fila(),
    ('Leche entera en polvo', '3.840 €/t', '+30 €/t', 'Holanda'),
    ('Suero en polvo', '1.640 €/t', '=', 'Holanda'),
    ('Mantequilla 82 %', '3.750 €/t', '+30 €/t', 'Holanda'),
    nata_fila('Nata Italia · 100 % grasa', 1940, 40, 0, 'Milán'),
    nata_fila('Nata España · 100 % grasa', 1467.6, 30, 27.1, 'Ministerio, sem. 39'),
    ('Leche spot Francia', '490 €/1.000 l', 'est', 'valor mantequilla + polvo'),
    ('Leche de vaca España', '0,474 €/l', '+0,005 €/l', 'precio medio FEGA · septiembre'),
    ('Leche de vaca · Lonja de León', '0,475 €/l', '=', 'pactado oct–dic · 3,7 % grasa · 3,10 % proteína'),
]
COTIZ_NOTA = 'Fuentes: ZuivelNL (4 nov), Bolsa de Milán (semana 44), Ministerio de Agricultura (semana 39, último publicado), FEGA y Lonja de León (29 oct). Las natas se expresan en base 100 % grasa. Proteína: precio de la leche desnatada en polvo dividido entre su 34 % de proteína. Leche spot Francia: valor estimado de la mantequilla y la leche en polvo que se obtienen de 1.000 litros, antes de costes de transformación. Precios orientativos, no constituyen oferta. Solicite cotización para su volumen y destino.'

COL = {'Precios': ('#FFF3D6', '#7A5200'), 'Mercados': ('#E6EDF8', '#2B4F9C'), 'Normativa': ('#E4F2EA', '#2E6B45'), 'Novedades': ('#EFE8F8', '#5B3E8C')}
e = lambda s: H.escape(s, quote=False)

def chip(c, on=False):
    st = ('background: #0E2A4F; color: #FFFFFF; border: 1.5px solid #0E2A4F' if on else 'background: #FFFFFF; color: #0E2A4F; border: 1.5px solid #D3DCEA')
    return f'<button type="button" class="blog-chip" data-cat="{c}" aria-pressed="{"true" if on else "false"}" style="padding: 10px 16px; border-radius: 999px; {st}; font: inherit; font-weight: 600; font-size: 14px; cursor: pointer">{c}</button>'

def card(n):
    bg, fg = COL[n['cat']]
    return (f'<a href="{n["url"]}" target="_blank" rel="noopener" class="card-link blog-item" data-cat="{n["cat"]}" style="background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 16px; overflow: hidden; display: flex; flex-direction: column">'
            f'<div style="background: {bg}; color: {fg}; padding: 22px 22px 18px; display: flex; flex-direction: column; gap: 2px">'
            f'<span style="font-family: Archivo, sans-serif; font-weight: 800; font-size: 34px; line-height: 1.05">{e(n["dato"])}</span>'
            f'<span style="font-size: 13px; font-weight: 600">{e(n["dato_pie"])}</span></div>'
            f'<div style="padding: 20px 22px 22px; display: flex; flex-direction: column; gap: 10px; flex: 1">'
            f'<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: {fg}">{n["cat"]} · {e(n["fecha"])}</span>'
            f'<h3 style="margin: 0; font-size: 19px; line-height: 1.35">{e(n["titulo"])}</h3>'
            f'<p style="margin: 0; color: #4D5D78; line-height: 1.6; font-size: 15px">{e(n["texto"])}</p>'
            f'<span style="margin-top: auto; padding-top: 6px; font-size: 13px; font-weight: 700; color: #2B4F9C">Fuente: {e(n["fuente"])} ↗</span></div></a>')


# ---------------- Leche de cabra (apartado de temporada) ----------------
# Filas: referencia, detalle/periodo, €/litro, € por punto de extracto quesero (grasa + proteína), extracto quesero %
CABRA = [
    ('España · precio medio', 'Ministerio / FEGA · agosto 2026', 1.047, 0.1317, 7.95, 'ok'),
    ('Lonja de León', 'leche entregada en septiembre · EQ medio provincia', None, 0.12621, 8.27, 'ok'),
    ('Francia · precio pagado', 'Idele · 2º trimestre 2026', 0.837, None, 7.13, 'ok'),
]
CABRA_NOTA = 'Extracto quesero (EQ) = grasa + proteína (%). Precio por punto = precio por litro ÷ EQ; equivale al precio por hectogrado ÷ 100. Las cifras sin dato directo se calculan a partir de las otras dos. No existe una media europea oficial de leche de cabra: Francia, primer productor de la UE, sirve de referencia.'
CABRA_NOTICIAS = [
    ('nov 2026', 'España: en agosto la leche de cabra se pagó a 0,1317 € por punto de extracto quesero (+12,9 % en un año), con un extracto medio del 7,95 % (1,047 €/l). Frente a julio, el precio por punto baja un 0,7 %: la subida por litro (+1,7 %) se debe a una leche más rica. Las entregas crecen un 1,2 % (33,2 millones de litros), tras la caída del primer trimestre.', 'Ministerio de Agricultura', 'https://www.mapa.gob.es/dam/mapa/contenido/ganaderia/temas/produccion-y-mercados-ganaderos/sectores-ganaderos-2/ovino-caprino/ovino-y-caprino-de-leche/informes-leche/informe-entregas_ovino-y-caprino_ago26.pdf'),
    ('may 2026', 'La producción española cayó un 10,8 % en el primer trimestre (88,1 millones de litros) y los ganaderos de caprino de leche bajaron un 6,2 % en un año.', 'Interempresas', 'https://www.interempresas.net/caprino/631256-caida-de-produccion-acelera-cambio-de-tendencia-y-precios-historicos-en-caprino.html'),
    ('jul–sep 2026', 'Francia: la recogida de leche de cabra crece un 6 % en mayo y las ventas de quesos un 2 %; el precio pagado en el 2º trimestre, 837 €/1.000 l con un extracto quesero del 7,13 % (≈ 0,117 € por punto), sube solo 5 € en un año. España, en cambio, paga un 18 % más que hace un año.', 'Transformation Laitière', 'https://www.transformation-laitiere.fr/prix-lait-de-chevre-deuxieme-trimestre-2026-837-euros-ipampa-espagne/'),
    ('nov 2026', 'Canarias sigue perdiendo cabaña caprina: de 210.593 cabezas en 2015 a 199.285 en 2024.', 'eDairy News', 'https://es.edairynews.com/canarias-pierde-cabras-y-advierten-que-el-queso-sera-un-lujo/'),
]
CABRA_LECTURA = 'Señales a vigilar: precios españoles en máximos con una oferta que empieza a recuperarse en agosto y una Francia con más leche y precios estables. Si la recogida sigue creciendo en otoño, la presión sobre el precio podría notarse en los contratos de 2027.'

def _num(x, d): return f"{x:.{d}f}".replace('.', ',')
def especie_html(titulo, subtitulo, tabla, nota, noticias_l, lectura):
    filas = ''
    for (ref, det, l, pt, eq, _) in tabla:
        calc_l = l is None and eq is not None; calc_p = pt is None and eq is not None
        if calc_l: l = pt * eq
        if calc_p: pt = l / eq
        filas += ('<tr style="border-top: 1px solid #D3DCEA">'
                  f'<td style="padding: 14px 8px 14px 0"><div style="font-weight: 700">{e(ref)}</div><div style="font-size: 13px; color: #4D5D78">{e(det)}</div></td>'
                  f'<td style="padding: 14px 6px; text-align: right; font-weight: 700; white-space: nowrap">{("≈ " if calc_l else "") + _num(l, 3) + " €/l" if l is not None else "—"}</td>'
                  f'<td style="padding: 14px 6px; text-align: right; font-weight: 700; white-space: nowrap">{("≈ " if calc_p else "") + _num(pt, 4) + " €" if pt is not None else "—"}</td>'
                  f'<td style="padding: 14px 0 14px 6px; text-align: right; white-space: nowrap">{_num(eq, 2) + " %" if eq is not None else "—"}</td></tr>')
    noticias = ''.join(
        f'<li style="display: flex; flex-direction: column; gap: 4px; padding: 14px 0; border-top: 1px solid #D3DCEA">'
        f'<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #2E6B45">{e(f)}</span>'
        f'<span style="line-height: 1.55; font-size: 15px">{e(t)}</span>'
        f'<a href="{u}" target="_blank" rel="noopener" style="font-size: 13px; font-weight: 700; color: #2B4F9C; text-decoration: none">Fuente: {e(src)} ↗</a></li>'
        for f, t, src, u in noticias_l)
    return ('<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 24px 24px 24px">\n'
            '<div style="background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 20px; padding: clamp(18px, 4vw, 28px); display: flex; flex-direction: column; gap: 22px">\n'
            '<div style="display: flex; flex-direction: column; gap: 6px"><span style="font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2E6B45">Apartado de temporada</span>'
            f'<h2 style="margin: 0; font-family: Archivo, sans-serif; font-size: clamp(24px, 4.5vw, 30px)">{e(titulo)}</h2>'
            f'<p style="margin: 0; color: #4D5D78; line-height: 1.55; max-width: 760px">{e(subtitulo)}</p></div>\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 28px; align-items: flex-start">\n'
            '<div style="flex: 3 1 300px; min-width: 0; display: flex; flex-direction: column; gap: 12px"><div style="overflow-x: auto"><table style="width: 100%; border-collapse: collapse; font-size: clamp(13px, 3.6vw, 15px)">'
            '<thead><tr style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: #4D5D78"><th style="text-align: left; padding: 0 8px 10px 0; font-weight: 700">Referencia</th>'
            '<th style="text-align: right; padding: 0 6px 10px; font-weight: 700">Por litro</th><th style="text-align: right; padding: 0 6px 10px; font-weight: 700">Por punto EQ</th>'
            '<th style="text-align: right; padding: 0 0 10px 6px; font-weight: 700">EQ</th></tr></thead><tbody>' + filas + '</tbody></table></div>'
            f'<p style="margin: 0; font-size: 13px; color: #4D5D78; line-height: 1.5">{e(nota)}</p></div>\n'
            '<div style="flex: 2 1 340px; min-width: 0; display: flex; flex-direction: column; gap: 4px"><h3 style="margin: 0 0 6px; font-size: 17px">Tendencias y producción</h3>'
            f'<ul style="list-style: none; margin: 0; padding: 0">{noticias}</ul>'
            f'<p style="margin: 8px 0 0; padding: 14px 16px; background: #E4F2EA; color: #1F4A30; border-radius: 12px; font-size: 14px; line-height: 1.55">{e(lectura)}</p></div>\n'
            '</div>\n</div>\n</div>\n</section>\n')

def cabra_html():
    return especie_html('Leche de cabra', 'Precio por litro y por punto de extracto quesero. Datos públicos más recientes de España y Francia.', CABRA, CABRA_NOTA, CABRA_NOTICIAS, CABRA_LECTURA)

# ---------------- Leche de oveja (apartado de temporada) ----------------
OVEJA = [
    ('España · precio medio', 'Ministerio / FEGA · agosto 2026', 1.298, 0.1125, 11.53, 'ok'),
    ('Lonja de León', 'leche entregada en septiembre · EQ medio provincia', None, 0.11419, 12.41, 'ok'),
    ('Francia · precio pagado', 'Idele · campaña 2024-2025', 1.291, None, None, 'ok'),
]
OVEJA_NOTA = 'Extracto quesero (EQ) = grasa + proteína (%). Precio por punto = precio por litro ÷ EQ; equivale al precio por hectogrado ÷ 100. Las cifras sin dato directo se calculan a partir de las otras dos. Francia publica el precio por campaña (octubre a septiembre) y sin desglose de extracto quesero. No existe una media europea oficial de leche de oveja.'
OVEJA_NOTICIAS = [
    ('nov 2026', 'España: en agosto la leche de oveja se pagó a 0,1125 € por punto de extracto quesero (+6,4 % en un año), con un extracto medio del 11,53 % (1,298 €/l). Frente a julio, el precio por punto baja un 0,8 %: la subida por litro (+1,8 %) se debe a una leche más rica. Las entregas suben un 1,2 % (40,9 millones de litros).', 'Ministerio de Agricultura', 'https://www.mapa.gob.es/dam/mapa/contenido/ganaderia/temas/produccion-y-mercados-ganaderos/sectores-ganaderos-2/ovino-caprino/ovino-y-caprino-de-leche/informes-leche/informe-entregas_ovino-y-caprino_ago26.pdf'),
    ('jul 2026', 'De enero a mayo la producción cayó un 1,7 % (215,8 millones de litros), mientras el precio medio subió un 5,7 %, hasta 0,1109 € por punto de extracto quesero.', 'eDairy News', 'https://es.edairynews.com/espana-reduce-la-produccion-de-leche-de-oveja/'),
    ('sep 2026', 'Castilla-La Mancha: ASAJA calcula que la leche de oveja manchega de 2026 será un 25 % inferior a la de hace dos años y denuncia precios por debajo de costes, con riesgo para el suministro del Queso Manchego.', 'Agronews Castilla y León', 'https://www.agronewscastillayleon.com/leche-oveja-manchega-crisis-precios-produccion-2026/'),
    ('may 2026', 'Francia: el precio pagado en la campaña 2024-2025 fue de 1.291 €/1.000 l (+4,3 %), con más leche recogida y algo menos de grasa y proteína. La fuente no publica el extracto quesero, por lo que no puede pasarse a precio por punto.', 'Réussir', 'https://www.reussir.fr/patre/nouvelle-hausse-du-prix-paye-aux-eleveurs-sur-2024-2025'),
]
OVEJA_LECTURA = 'Señales a vigilar: el precio español se recupera tras la fuerte caída de 2025, pero la producción sigue bajando, sobre todo en la oveja manchega. Una oferta corta sostiene los precios de cara a los contratos de 2027, aunque los ganaderos manchegos siguen por debajo de costes.'

def oveja_html():
    return especie_html('Leche de oveja', 'Precio por litro y por punto de extracto quesero. Datos públicos más recientes de España y Francia.', OVEJA, OVEJA_NOTA, OVEJA_NOTICIAS, OVEJA_LECTURA)

def build():
    d = DESTACADO; bg, fg = COL[d['cat']]
    intro = (
        '<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 24px; display: flex; flex-direction: column; gap: 18px">\n'
        '<span style="font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2B4F9C">Blog</span>\n'
        '<h1 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: clamp(32px, 7vw, 48px); line-height: 1.05">Actualidad del sector lácteo</h1>\n'
        '<p style="margin: 0; font-size: 18px; line-height: 1.55; color: #4D5D78; max-width: 720px">Noticias, precios de referencia, normativa y novedades del mercado lácteo europeo.</p>\n'
        '<p style="margin: 0; font-size: 15px; line-height: 1.5; color: #4D5D78">Resumen semanal, publicado cada lunes.</p>\n'
        f'<span style="font-size: 15px; font-weight: 700">Semana {SEMANA["numero"]} · {SEMANA["rango"]}</span>\n'
        '<div id="blog-filtros" role="group" aria-label="Filtrar noticias" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px">'
        + chip('Todas', True) + ''.join(chip(c) for c in ['Mercados', 'Precios', 'Normativa', 'Novedades']) + '</div>\n</div>\n</section>\n')
    dcard = dict(DESTACADO, texto=DESTACADO['texto'][0])
    feat = (
        '<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 24px 24px; display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start">\n'
        '<div id="blog-lista" style="flex: 3 1 560px; min-width: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px">\n'
        + '\n'.join(card(n) for n in [dcard] + NOTICIAS) + '\n</div>\n'
        '<aside style="flex: 1 1 320px; min-width: 0; position: sticky; top: 24px; background: #0E2A4F; color: #FFFFFF; border-radius: 20px; padding: 28px; display: flex; flex-direction: column; gap: 16px">\n'
        '<div style="display: flex; flex-direction: column; gap: 4px">\n<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #E8B84A">Cotizaciones de referencia</span>\n'
        f'<span style="color: #CBD8EE; font-size: 14px">Semana {SEMANA["numero"]} · actualizado {SEMANA["actualizado"]}</span>\n</div>\n<div style="display: flex; flex-direction: column">\n'
        + ''.join(
            f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 12px 0{"; border-bottom: 1px solid rgba(207,227,220,.2)" if i < len(COTIZ) - 1 else ""}">'
            f'<span style="display: flex; flex-direction: column"><span>{e(p)}</span><span style="font-size: 12px; color: #CBD8EE">{e(m)}</span></span>'
            f'<span style="display: flex; flex-direction: column; align-items: flex-end"><span style="font-weight: 700; white-space: nowrap">{e(v)}</span>'
            f'<span style="font-size: 12px; font-weight: 700; color: {"#7FD3A0" if c.startswith("+") else ("#F2A7A7" if c.startswith("−") else "#CBD8EE")}">{"▲ " + c if c.startswith("+") else ("▼ " + c if c.startswith("−") else ("estimación" if c == "est" else "sin cambios"))}</span></span></div>'
            for i, (p, v, c, m) in enumerate(COTIZ)) +
        f'</div>\n<p style="margin: 0; font-size: 13px; color: #CBD8EE; line-height: 1.5">{e(COTIZ_NOTA)}</p>\n'
        '<a href="https://www.eex.com/en/markets/agriculturals" target="_blank" rel="noopener" style="color: #E8B84A; font-weight: 700; font-size: 14px; text-decoration: none">Futuros lácteos en EEX ↗</a>\n</aside>\n</div>\n</section>\n')
    grid = ('<section>\n'
            '<p id="blog-vacio" hidden style="max-width: 1240px; margin: 0 auto; padding: 0 24px; color: #4D5D78">No hay noticias de esta categoría esta semana.</p>\n'
            '<div style="max-width: 1240px; margin: 0 auto; padding: 8px 24px 40px"><p style="margin: 0; font-size: 13px; color: #4D5D78; line-height: 1.5; max-width: 860px">Resumen elaborado por Plataforma Interprofesional Láctea a partir de las fuentes citadas. Cada noticia enlaza a su fuente original.</p></div>\n</section>\n')
    js = ('<script>\n(function(){var f=document.getElementById(\'blog-filtros\');if(!f)return;var pg=f.closest(\'.pg\')||document;\n'
          'f.addEventListener(\'click\',function(ev){var b=ev.target.closest(\'.blog-chip\');if(!b)return;var c=b.getAttribute(\'data-cat\'),n=0;\n'
          'f.querySelectorAll(\'.blog-chip\').forEach(function(x){var on=x===b;x.setAttribute(\'aria-pressed\',on?\'true\':\'false\');x.style.background=on?\'#0E2A4F\':\'#FFFFFF\';x.style.color=on?\'#FFFFFF\':\'#0E2A4F\';x.style.borderColor=on?\'#0E2A4F\':\'#D3DCEA\';});\n'
          'pg.querySelectorAll(\'.blog-item\').forEach(function(it){var ok=(c===\'Todas\'||it.getAttribute(\'data-cat\')===c);it.style.display=ok?\'\':\'none\';if(ok)n++;});\n'
          'var v=pg.querySelector(\'#blog-vacio\');if(v)v.hidden=n>0;});})();\n</script>\n')
    s = open(SRC, encoding='utf-8').read()
    a = s.index('<section>'); b = s.index('<footer')
    ad = aldia_html()
    if ad:
        mark = '<span style="font-size: 15px; font-weight: 700">Semana'
        intro = intro.replace(mark, '</div>\n</section>\n' + ad + '<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 24px 24px 0; display: flex; flex-direction: column; gap: 14px">\n' + mark, 1)
    s = s[:a] + intro + '\n' + feat + '\n' + grid + '\n' + cabra_html() + '\n' + oveja_html() + '\n' + s[b:]
    open(B + 'deploy/blog_filter.html', 'w', encoding='utf-8').write(js)
    open(SRC, 'w', encoding='utf-8').write(s)
    json.dump({'actualizado': SEMANA['fecha'], 'semana': SEMANA, 'destacado': DESTACADO, 'noticias': NOTICIAS,
               'cotizaciones': {'filas': [dict(producto=p, precio=v, cambio=c, mercado=m) for p, v, c, m in COTIZ], 'nota': COTIZ_NOTA}},
              open(B + 'blog_src/noticias.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# ---------------- Al día (noticias lácteas diarias, p. ej. de la newsletter de CanalDis) ----------------
# Datos en blog_src/aldia.json (cada noticia con textos en es/en/fr/pt). Se muestran las de los últimos 7 días.
import datetime as _dt
ALDIA_UI = [
    ('Al día', 'Daily news', 'Au jour le jour', 'Dia a dia'),
    ('Noticias lácteas de cada día, seleccionadas de la prensa de alimentación y distribución.',
     'Daily dairy news, selected from the food and retail press.',
     'Actualités laitières du jour, sélectionnées dans la presse alimentaire et de la distribution.',
     'Notícias lácteas de cada dia, selecionadas da imprensa alimentar e da distribuição.'),
]
def aldia_items():
    try: items = json.load(open(B + 'blog_src/aldia.json', encoding='utf-8'))
    except FileNotFoundError: return []
    hoy = _dt.date.today()
    items = [i for i in items if (hoy - _dt.date.fromisoformat(i['recibido'])).days <= 7]
    return sorted(items, key=lambda i: i['recibido'], reverse=True)

def aldia_html():
    items = aldia_items()
    if not items: return ''
    li = ''.join(
        f'<a href="{i["url"]}" target="_blank" rel="noopener" class="card-link" style="display: flex; flex-direction: column; gap: 6px; padding: 18px 20px; background: #FFFFFF; border: 1px solid #D3DCEA; border-left: 4px solid #E8B84A; border-radius: 12px">'
        f'<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #7A5200">{e(i["fecha"]["es"])}</span>'
        f'<span style="font-weight: 700; font-size: 17px; line-height: 1.35">{e(i["titulo"]["es"])}</span>'
        f'<span style="color: #4D5D78; line-height: 1.55; font-size: 15px">{e(i["texto"]["es"])}</span>'
        f'<span style="font-size: 13px; font-weight: 700; color: #2B4F9C">Fuente: {e(i["fuente"])} ↗</span></a>' for i in items)
    return ('<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 8px 24px 8px; display: flex; flex-direction: column; gap: 12px">\n'
            '<div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 14px"><h2 style="margin: 0; font-family: Archivo, sans-serif; font-size: 24px">Al día</h2>'
            '<span style="color: #4D5D78; font-size: 15px">Noticias lácteas de cada día, seleccionadas de la prensa de alimentación y distribución.</span></div>\n'
            '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px">' + li + '</div>\n</div>\n</section>\n')

def aldia_traducciones():
    T = list(ALDIA_UI)
    for i in aldia_items():
        T.append(tuple(i['fecha'][l] for l in ('es', 'en', 'fr', 'pt')))
        T.append(tuple(i['titulo'][l] for l in ('es', 'en', 'fr', 'pt')))
        T.append(tuple(i['texto'][l] for l in ('es', 'en', 'fr', 'pt')))
        src = i['fuente']; T.append((f'Fuente: {src} ↗', f'Source: {src} ↗', f'Source : {src} ↗', f'Fonte: {src} ↗'))
    with open(B + 'i18n/tr_aldia.py', 'w', encoding='utf-8') as f:
        f.write('# Generado por deploy/blog_week.py a partir de blog_src/aldia.json — no editar a mano\nT = ' + repr(T) + '\n')

MAIN = B + 'web/project/Main.dc.html'
def home_cards():
    """Rellena las tres tarjetas «Actualidad del sector» del inicio con el destacado y las primeras noticias de Mercados y Normativa."""
    picks = [DESTACADO] + [next(n for n in NOTICIAS if n['cat'] == c) for c in ('Mercados', 'Normativa')]
    cards = []
    for n in picks:
        bg, fg = COL[n['cat']]
        cards.append(f'<a href="Blog.dc.html" class="card-link" style="background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 16px; overflow: hidden; display: flex; flex-direction: column">'
                     f'<div style="background: {bg}; color: {fg}; padding: 22px 22px 18px; display: flex; flex-direction: column; gap: 2px">'
                     f'<span style="font-family: Archivo, sans-serif; font-weight: 800; font-size: 34px; line-height: 1.05">{e(n["dato"])}</span>'
                     f'<span style="font-size: 13px; font-weight: 600">{e(n["dato_pie"])}</span></div>'
                     f'<div style="padding: 22px; display: flex; flex-direction: column; gap: 8px"><span style="font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: {fg}">{n["cat"]} · {e(n["fecha"])}</span>'
                     f'<h3 style="margin: 0; font-size: 19px; line-height: 1.35">{e(n["titulo"])}</h3></div></a>')
    m = open(MAIN, encoding='utf-8').read()
    a = m.index('Actualidad del sector</h2>')
    g = m.index('<div', m.index('</div>', a))  # grid tras la cabecera
    end = m.index('\n</div>', m.index('</a>\n</div>', g)) if False else m.index('</div>\n</div>', m.rindex('</a>', g, m.index('</section>', g)))
    grid_open = '<div id="home-noticias" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px">'
    m = m[:g] + grid_open + '\n' + '\n'.join(cards) + '\n' + m[end:]
    open(MAIN, 'w', encoding='utf-8').write(m)

if __name__ == '__main__':
    aldia_traducciones(); build(); home_cards(); print('ok')
