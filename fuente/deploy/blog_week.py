"""Genera la pestaña Blog (y las tarjetas de noticias del inicio) a partir de los datos en blog_src/.

Datos (todos los textos en es/en/fr/pt; los números se formatean solos en cada idioma):
  blog_src/semana.json        resumen semanal: semana, noticias (la 1.ª, 2.ª y 3.ª salen también en el inicio)
  blog_src/cotizaciones.json  cuadro «Cotizaciones de referencia»
  blog_src/temporada.json     apartados de leche de cabra y de oveja
  blog_src/aldia.json         sección «Al día» (noticias diarias; se muestran las de los últimos 7 días)

Escribe: web/project/Blog.dc.html, web/project/Main.dc.html (tarjetas del inicio),
         i18n/tr_blogdata.py (traducciones generadas), deploy/blog_filter.html, blog_src/noticias.json.
"""
import json, html as H, datetime as _dt
import os as _os; B = _os.environ['PIL_FUENTE'].rstrip('/') + '/'
SRC = B + 'web/project/Blog.dc.html'
MAIN = B + 'web/project/Main.dc.html'
LANGS = ('es', 'en', 'fr', 'pt')

# Fuentes que se revisan (elegidas por Miguel Ángel)
FUENTES = [
    ('Vaca Pinta', 'https://www.vacapinta.com/es/es-la-leche.html'),
    ('Agroinformación – vacuno de leche', 'https://www.agroinformacion.com/category/ganaderia/vacuno-de-leche/'),
    ('MAPA – vacuno lechero', 'https://www.mapa.gob.es/es/ganaderia/temas/produccion-y-mercados-ganaderos/sectores-ganaderos/vacuno-de-leche'),
    ('eDairy News (España y Europa; se descarta Latinoamérica)', 'https://es.edairynews.com/'),
    ('Agronews Castilla y León', 'https://www.agronewscastillayleon.com/'),
    ('Interempresas – ovino y caprino', 'https://www.interempresas.net/caprino/'),
    ('Newsletter CanalDis (Gmail)', 'https://canaldis.com/'),
    ('EEX (solo enlace)', 'https://www.eex.com/en/markets/agriculturals'),
]

def load(name):
    return json.load(open(B + 'blog_src/' + name, encoding='utf-8'))

TR = []           # traducciones generadas (es, en, fr, pt)
def tr(d):
    """d = {'es':..,'en':..,'fr':..,'pt':..} → registra la traducción y devuelve el texto en español."""
    if isinstance(d, str): return d
    t = tuple(d[l] for l in LANGS)
    if t not in TR: TR.append(t)
    return d['es']

# ---------- formato de números por idioma ----------
def _n(x, dec, lang):
    s = f"{abs(x):,.{dec}f}"  # 1,234.56
    if lang == 'en': out = s
    elif lang == 'fr': out = s.replace(',', ' ').replace('.', ',')
    else: out = s.replace(',', '#').replace('.', ',').replace('#', '.')
    return ('−' if x < 0 else '') + out

UNITS = {'€/t': ('/t',), '€/kg': ('/kg',), '€/l': ('/l',), '€/1000l': ('/1,000 l',), '€': ('',), '$/t': ('/t',)}
def money(x, dec, unit, lang, sign=False):
    n = _n(abs(x), dec, lang)
    sg = ('+' if x > 0 else '−' if x < 0 else '') if sign else ('−' if x < 0 else '')
    cur = '$' if unit.startswith('$') else '€'
    if lang == 'en':
        return f'{sg}{cur}{n}{UNITS[unit][0]}'
    tail = {'€/t': '€/t', '€/kg': '€/kg', '€/l': '€/l', '€/1000l': '€/1.000 l' if lang != 'fr' else '€/1 000 l', '€': '€', '$/t': '$/t'}[unit]
    return f'{sg}{n} {tail}'

def pct(x, dec, lang):
    return f'{_n(x, dec, lang)}%' if lang == 'en' else f'{_n(x, dec, lang)} %'

def multi(fn):
    """Aplica fn(lang) a los 4 idiomas, registra la traducción y devuelve el español."""
    return tr({l: fn(l) for l in LANGS})

CAT = {'Precios': {'es': 'Precios', 'en': 'Prices', 'fr': 'Prix', 'pt': 'Preços'},
       'Mercados': {'es': 'Mercados', 'en': 'Markets', 'fr': 'Marchés', 'pt': 'Mercados'},
       'Normativa': {'es': 'Normativa', 'en': 'Regulation', 'fr': 'Réglementation', 'pt': 'Regulamentação'},
       'Novedades': {'es': 'Novedades', 'en': 'News', 'fr': 'Nouveautés', 'pt': 'Novidades'}}
FUENTE = {'es': 'Fuente: {} ↗', 'en': 'Source: {} ↗', 'fr': 'Source : {} ↗', 'pt': 'Fonte: {} ↗'}
def fuente(src): return multi(lambda l: FUENTE[l].format(src))

COL = {'Precios': ('#FFF3D6', '#7A5200'), 'Mercados': ('#E6EDF8', '#2B4F9C'), 'Normativa': ('#E4F2EA', '#2E6B45'), 'Novedades': ('#EFE8F8', '#5B3E8C')}
e = lambda s: H.escape(s, quote=False)

# ---------- resumen semanal ----------
def chip(c, on=False):
    st = ('background: #0E2A4F; color: #FFFFFF; border: 1.5px solid #0E2A4F' if on else 'background: #FFFFFF; color: #0E2A4F; border: 1.5px solid #D3DCEA')
    return f'<button type="button" class="blog-chip" data-cat="{c}" aria-pressed="{"true" if on else "false"}" style="padding: 10px 16px; border-radius: 999px; {st}; font: inherit; font-weight: 600; font-size: 14px; cursor: pointer">{c}</button>'

def etiqueta(n):
    return multi(lambda l: f'{CAT[n["cat"]][l]} · {n["fecha"][l]}')

def card(n):
    bg, fg = COL[n['cat']]
    return (f'<a href="{n["url"]}" target="_blank" rel="noopener" class="card-link blog-item" data-cat="{n["cat"]}" style="background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 16px; overflow: hidden; display: flex; flex-direction: column">'
            f'<div style="background: {bg}; color: {fg}; padding: 22px 22px 18px; display: flex; flex-direction: column; gap: 2px">'
            f'<span style="font-family: Archivo, sans-serif; font-weight: 800; font-size: 34px; line-height: 1.05">{e(tr(n["dato"]))}</span>'
            f'<span style="font-size: 13px; font-weight: 600">{e(tr(n["dato_pie"]))}</span></div>'
            f'<div style="padding: 20px 22px 22px; display: flex; flex-direction: column; gap: 10px; flex: 1">'
            f'<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: {fg}">{e(etiqueta(n))}</span>'
            f'<h3 style="margin: 0; font-size: 19px; line-height: 1.35">{e(tr(n["titulo"]))}</h3>'
            f'<p style="margin: 0; color: #4D5D78; line-height: 1.6; font-size: 15px">{e(tr(n["texto"]))}</p>'
            f'<span style="margin-top: auto; padding-top: 6px; font-size: 13px; font-weight: 700; color: #2B4F9C">{e(fuente(n["fuente"]))}</span></div></a>')

# ---------- cotizaciones ----------
SEM_LBL = {'es': 'Semana {} · actualizado {}', 'en': 'Week {} · updated {}', 'fr': 'Semaine {} · mise à jour le {}', 'pt': 'Semana {} · atualizado a {}'}
NATA_LBL = {'es': '{o} · nata {g} % a {p}', 'en': '{o} · {g}% cream at {p}', 'fr': '{o} · crème {g} % à {p}', 'pt': '{o} · nata {g} % a {p}'}

def cambio_txt(row, lang):
    c = row.get('cambio', 0)
    if c == 'est': return None
    return money(c, row.get('dec_cambio', row.get('dec', 0)), row['unidad'], lang, sign=True) if c else None

def cotiz_filas(cz):
    filas, por_id = [], {r['id']: r for r in cz['filas'] if 'id' in r}
    for r in cz['filas']:
        t = r['tipo']
        if t == 'num':
            prod, det = tr(r['producto']), tr(r['detalle'])
            val = multi(lambda l: money(r['valor'], r.get('dec', 0), r['unidad'], l))
            c = r.get('cambio', 0)
            if c == 'est': cam = 'est'
            elif not c: cam = '='
            else: cam = multi(lambda l: cambio_txt(r, l))
        elif t == 'proteina':
            s = por_id[r['de']]; f = r.get('proteina', 34) / 100
            prod, det = tr(r['producto']), tr(r['detalle'])
            val = multi(lambda l: money(s['valor'] / f / 1000, 2, '€/kg', l))
            c = round((s.get('cambio', 0) or 0) / f / 1000, 2)
            cam = '=' if c == 0 else multi(lambda l: money(c, 2, '€/kg', l, sign=True))
        elif t == 'nata':
            f = r['grasa'] / 100
            prod = tr(r['producto'])
            det = multi(lambda l: NATA_LBL[l].format(o=r['origen'][l], g=_n(r['grasa'], 0, l), p=money(r['precio'], 0, '€/t', l)))
            val = multi(lambda l: money(r['precio'] / f, 0, '€/t', l))
            c = round((r.get('cambio', 0) or 0) / f)
            cam = '=' if c == 0 else multi(lambda l: money(c, 0, '€/t', l, sign=True))
        filas.append((prod, val, cam, det))
    return filas

def cambio_html(c):
    if c == 'est': return '#CBD8EE', 'estimación'
    if c == '=': return '#CBD8EE', 'sin cambios'
    up = c.startswith('+')
    lab = multi(lambda l: None) if False else None
    return ('#7FD3A0' if up else '#F2A7A7'), ('▲ ' if up else '▼ ') + c

def registra_flechas(filas):
    # «▲ +20 €/t» como texto completo: registra la traducción a partir de las traducciones del cambio
    for _, _, c, _ in filas:
        if c in ('est', '='): continue
        t = next(x for x in TR if x[0] == c)
        pref = '▲ ' if c.startswith('+') else '▼ '
        tt = tuple(pref + x for x in t)
        if tt not in TR: TR.append(tt)


# ---------- precios spot EXW ----------
SPOT_TXT = {
 'eyebrow': {'es': 'Precios spot EXW', 'en': 'EXW spot prices', 'fr': 'Prix spot EXW', 'pt': 'Preços spot EXW'},
 'titulo': {'es': 'Ingredientes lácteos · precios spot', 'en': 'Dairy ingredients · spot prices', 'fr': 'Ingrédients laitiers · prix spot', 'pt': 'Ingredientes lácteos · preços spot'},
 'act': {'es': 'Actualizado {} · €/t, EXW', 'en': 'Updated {} · €/t, EXW', 'fr': 'Mis à jour le {} · €/t, EXW', 'pt': 'Atualizado a {} · €/t, EXW'},
 'aviso': {'es': 'Precios spot en condiciones EXW, en euros por tonelada, sujetos a cambios y a disponibilidad. No constituyen una oferta en firme.',
           'en': 'Spot prices on EXW terms, in euros per tonne, subject to change and availability. They do not constitute a firm offer.',
           'fr': 'Prix spot aux conditions EXW, en euros par tonne, susceptibles de modification et sous réserve de disponibilité. Ils ne constituent pas une offre ferme.',
           'pt': 'Preços spot em condições EXW, em euros por tonelada, sujeitos a alterações e a disponibilidade. Não constituem uma proposta firme.'},
 'cta': {'es': 'Solicitar cotización', 'en': 'Request a quote', 'fr': 'Demander un devis', 'pt': 'Pedir cotação'},
}

def spot_html(d):
    if not d or not d.get('grupos'): return ''
    T = {k: tr(v) for k, v in SPOT_TXT.items()}
    act = multi(lambda l: SPOT_TXT['act'][l].format(d['actualizado'][l]))
    cards = []
    for g in d['grupos']:
        rows = []
        ps = g['productos']
        for i, p in enumerate(ps):
            val = multi(lambda l: money(p['precio'], 0, '€/t', l))
            c = p.get('cambio')
            if c:
                cv = multi(lambda l: money(c, 0, '€/t', l, sign=True))
                cam = f'<span style="font-size: 12px; font-weight: 700; color: {"#1F8A4C" if c > 0 else "#C0392B"}">{"▲" if c > 0 else "▼"} <span>{e(cv)}</span></span>'
            else:
                cam = ''
            rows.append(
                f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 9px 0{"; border-bottom: 1px solid #E3E9F2" if i < len(ps) - 1 else ""}">'
                f'<span style="font-size: 15px; line-height: 1.35">{e(tr(p["nombre"]))}</span>'
                f'<span style="display: flex; flex-direction: column; align-items: flex-end; white-space: nowrap"><span style="font-weight: 700">{e(val)}</span>{cam}</span></div>')
        cards.append(
            '<div style="background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 16px; padding: 20px 22px; display: flex; flex-direction: column">'
            f'<h3 style="margin: 0 0 6px; font-family: Archivo, sans-serif; font-size: 17px; font-weight: 800; color: #0E2A4F">{e(tr(g["nombre"]))}</h3>'
            + ''.join(rows) + '</div>')
    return ('<section id="precios-spot" style="background: #F4F7FB">\n'
            '<div style="max-width: 1240px; margin: 0 auto; padding: 48px 24px; display: flex; flex-direction: column; gap: 20px">\n'
            '<div style="display: flex; flex-direction: column; gap: 6px">'
            f'<span style="font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2B4F9C">{e(T["eyebrow"])}</span>'
            f'<h2 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: clamp(26px, 5vw, 34px)">{e(T["titulo"])}</h2>'
            f'<span style="font-size: 14px; color: #4D5D78">{e(act)}</span></div>\n'
            '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; align-items: start">\n'
            + '\n'.join(cards) + '\n</div>\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; justify-content: space-between">'
            f'<p style="margin: 0; font-size: 13px; color: #4D5D78; line-height: 1.5; max-width: 760px">{e(T["aviso"])}</p>'
            f'<a href="Solicitud.dc.html" style="background: #0E2A4F; color: #FFFFFF; font-weight: 700; font-size: 15px; padding: 12px 22px; border-radius: 999px; text-decoration: none">{e(T["cta"])}</a>'
            '</div>\n</div>\n</section>\n')

# ---------- cabra y oveja ----------
def especie_html(d):
    filas = ''
    for r in d['tabla']:
        l, pt_, eq = r.get('litro'), r.get('punto'), r.get('eq')
        calc_l = l is None and eq is not None and pt_ is not None; calc_p = pt_ is None and eq is not None and l is not None
        if calc_l: l = pt_ * eq
        if calc_p: pt_ = l / eq
        c_l = '—' if l is None else multi(lambda g: ('≈ ' if calc_l else '') + money(l, 3, '€/l', g))
        c_p = '—' if pt_ is None else multi(lambda g: ('≈ ' if calc_p else '') + money(pt_, 4, '€', g))
        c_e = '—' if eq is None else multi(lambda g: pct(eq, 2, g))
        filas += ('<tr style="border-top: 1px solid #D3DCEA">'
                  f'<td style="padding: 14px 8px 14px 0"><div style="font-weight: 700">{e(tr(r["ref"]))}</div><div style="font-size: 13px; color: #4D5D78">{e(tr(r["det"]))}</div></td>'
                  f'<td style="padding: 14px 6px; text-align: right; font-weight: 700; white-space: nowrap">{e(c_l)}</td>'
                  f'<td style="padding: 14px 6px; text-align: right; font-weight: 700; white-space: nowrap">{e(c_p)}</td>'
                  f'<td style="padding: 14px 0 14px 6px; text-align: right; white-space: nowrap">{e(c_e)}</td></tr>')
    noticias = ''.join(
        f'<li style="display: flex; flex-direction: column; gap: 4px; padding: 14px 0; border-top: 1px solid #D3DCEA">'
        f'<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #2E6B45">{e(tr(n["fecha"]))}</span>'
        f'<span style="line-height: 1.55; font-size: 15px">{e(tr(n["texto"]))}</span>'
        f'<a href="{n["url"]}" target="_blank" rel="noopener" style="font-size: 13px; font-weight: 700; color: #2B4F9C; text-decoration: none">{e(fuente(n["fuente"]))}</a></li>'
        for n in d['noticias'])
    return ('<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 24px 24px 24px">\n'
            '<div style="background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 20px; padding: clamp(18px, 4vw, 28px); display: flex; flex-direction: column; gap: 22px">\n'
            '<div style="display: flex; flex-direction: column; gap: 6px"><span style="font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2E6B45">Apartado de temporada</span>'
            f'<h2 style="margin: 0; font-family: Archivo, sans-serif; font-size: clamp(24px, 4.5vw, 30px)">{e(tr(d["titulo"]))}</h2>'
            f'<p style="margin: 0; color: #4D5D78; line-height: 1.55; max-width: 760px">{e(tr(d["subtitulo"]))}</p></div>\n'
            '<div style="display: flex; flex-wrap: wrap; gap: 28px; align-items: flex-start">\n'
            '<div style="flex: 3 1 300px; min-width: 0; display: flex; flex-direction: column; gap: 12px"><div style="overflow-x: auto"><table style="width: 100%; border-collapse: collapse; font-size: clamp(13px, 3.6vw, 15px)">'
            '<thead><tr style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: #4D5D78"><th style="text-align: left; padding: 0 8px 10px 0; font-weight: 700">Referencia</th>'
            '<th style="text-align: right; padding: 0 6px 10px; font-weight: 700">Por litro</th><th style="text-align: right; padding: 0 6px 10px; font-weight: 700">Por punto EQ</th>'
            '<th style="text-align: right; padding: 0 0 10px 6px; font-weight: 700">EQ</th></tr></thead><tbody>' + filas + '</tbody></table></div>'
            f'<p style="margin: 0; font-size: 13px; color: #4D5D78; line-height: 1.5">{e(tr(d["nota"]))}</p></div>\n'
            '<div style="flex: 2 1 340px; min-width: 0; display: flex; flex-direction: column; gap: 4px"><h3 style="margin: 0 0 6px; font-size: 17px">Tendencias y producción</h3>'
            f'<ul style="list-style: none; margin: 0; padding: 0">{noticias}</ul>'
            f'<p style="margin: 8px 0 0; padding: 14px 16px; background: #E4F2EA; color: #1F4A30; border-radius: 12px; font-size: 14px; line-height: 1.55">{e(tr(d["lectura"]))}</p></div>\n'
            '</div>\n</div>\n</div>\n</section>\n')

# ---------- Al día ----------
ALDIA_UI = [
    {'es': 'Al día', 'en': 'Daily news', 'fr': 'Au jour le jour', 'pt': 'Dia a dia'},
    {'es': 'Noticias lácteas de cada día, seleccionadas de la prensa del sector, de alimentación y de distribución.',
     'en': 'Daily dairy news, selected from the dairy, food and retail press.',
     'fr': 'Actualités laitières du jour, sélectionnées dans la presse laitière, alimentaire et de la distribution.',
     'pt': 'Notícias lácteas de cada dia, selecionadas da imprensa do setor, alimentar e da distribuição.'},
]
def aldia_items():
    try: items = load('aldia.json')
    except FileNotFoundError: return []
    hoy = _dt.date.today()
    items = [i for i in items if (hoy - _dt.date.fromisoformat(i['recibido'])).days <= 7]
    return sorted(items, key=lambda i: i['recibido'], reverse=True)

def aldia_html():
    items = aldia_items()
    if not items: return ''
    li = ''.join(
        f'<a href="{i["url"]}" target="_blank" rel="noopener" class="card-link" style="display: flex; flex-direction: column; gap: 6px; padding: 18px 20px; background: #FFFFFF; border: 1px solid #D3DCEA; border-left: 4px solid #E8B84A; border-radius: 12px">'
        f'<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #7A5200">{e(tr(i["fecha"]))}</span>'
        f'<span style="font-weight: 700; font-size: 17px; line-height: 1.35">{e(tr(i["titulo"]))}</span>'
        f'<span style="color: #4D5D78; line-height: 1.55; font-size: 15px">{e(tr(i["texto"]))}</span>'
        f'<span style="font-size: 13px; font-weight: 700; color: #2B4F9C">{e(fuente(i["fuente"]))}</span></a>' for i in items)
    return ('<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 8px 24px 8px; display: flex; flex-direction: column; gap: 12px">\n'
            f'<div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 14px"><h2 style="margin: 0; font-family: Archivo, sans-serif; font-size: 24px">{e(tr(ALDIA_UI[0]))}</h2>'
            f'<span style="color: #4D5D78; font-size: 15px">{e(tr(ALDIA_UI[1]))}</span></div>\n'
            '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px">' + li + '</div>\n</div>\n</section>\n')

# ---------- página completa ----------
RANGO_LBL = {'es': 'Semana {} · {}', 'en': 'Week {} · {}', 'fr': 'Semaine {} · {}', 'pt': 'Semana {} · {}'}

def build():
    S = load('semana.json'); CZ = load('cotizaciones.json'); TEMP = load('temporada.json')
    SPOT = load('spot.json')
    sem = S['semana']; NOT = S['noticias']
    rango = multi(lambda l: RANGO_LBL[l].format(sem['numero'], sem['rango'][l]))
    intro = (
        '<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 24px; display: flex; flex-direction: column; gap: 18px">\n'
        '<span style="font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2B4F9C">Blog</span>\n'
        '<h1 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: clamp(32px, 7vw, 48px); line-height: 1.05">Actualidad del sector lácteo</h1>\n'
        '<p style="margin: 0; font-size: 18px; line-height: 1.55; color: #4D5D78; max-width: 720px">Noticias, precios de referencia, normativa y novedades del mercado lácteo europeo.</p>\n'
        '<p style="margin: 0; font-size: 15px; line-height: 1.5; color: #4D5D78">Resumen semanal, publicado cada lunes.</p>\n'
        f'<span style="font-size: 15px; font-weight: 700">{e(rango)}</span>\n'
        '<div id="blog-filtros" role="group" aria-label="Filtrar noticias" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px">'
        + chip('Todas', True) + ''.join(chip(c) for c in ['Mercados', 'Precios', 'Normativa', 'Novedades']) + '</div>\n</div>\n</section>\n')
    filas = cotiz_filas(CZ); registra_flechas(filas)
    act = multi(lambda l: SEM_LBL[l].format(CZ['semana'], CZ['actualizado'][l]))
    feat = (
        '<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 24px 24px; display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start">\n'
        '<div id="blog-lista" style="flex: 3 1 560px; min-width: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px">\n'
        + '\n'.join(card(n) for n in NOT) + '\n</div>\n'
        '<aside style="flex: 1 1 320px; min-width: 0; position: sticky; top: 24px; background: #0E2A4F; color: #FFFFFF; border-radius: 20px; padding: 28px; display: flex; flex-direction: column; gap: 16px">\n'
        '<div style="display: flex; flex-direction: column; gap: 4px">\n<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #E8B84A">Cotizaciones de referencia</span>\n'
        f'<span style="color: #CBD8EE; font-size: 14px">{e(act)}</span>\n</div>\n<div style="display: flex; flex-direction: column">\n'
        + ''.join(
            f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 12px 0{"; border-bottom: 1px solid rgba(207,227,220,.2)" if i < len(filas) - 1 else ""}">'
            f'<span style="display: flex; flex-direction: column"><span>{e(p)}</span><span style="font-size: 12px; color: #CBD8EE">{e(m)}</span></span>'
            f'<span style="display: flex; flex-direction: column; align-items: flex-end"><span style="font-weight: 700; white-space: nowrap">{e(v)}</span>'
            f'<span style="font-size: 12px; font-weight: 700; color: {cambio_html(c)[0]}">{e(cambio_html(c)[1])}</span></span></div>'
            for i, (p, v, c, m) in enumerate(filas)) +
        f'</div>\n<p style="margin: 0; font-size: 13px; color: #CBD8EE; line-height: 1.5">{e(tr(CZ["nota"]))}</p>\n'
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
        mark = f'<span style="font-size: 15px; font-weight: 700">{e(rango)}'
        intro = intro.replace(mark, '</div>\n</section>\n' + ad + '<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 24px 24px 0; display: flex; flex-direction: column; gap: 14px">\n' + mark, 1)
    s = s[:a] + intro + '\n' + feat + '\n' + grid + '\n' + spot_html(SPOT) + ''.join(especie_html(TEMP[k]) + '\n' for k in ('cabra', 'oveja')) + s[b:]
    open(B + 'deploy/blog_filter.html', 'w', encoding='utf-8').write(js)
    open(SRC, 'w', encoding='utf-8').write(s)
    json.dump({'semana': sem, 'noticias': NOT, 'cotizaciones': CZ, 'temporada': TEMP, 'spot': SPOT, 'aldia': aldia_items()},
              open(B + 'blog_src/noticias.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    home_cards(NOT[:3])

def home_cards(picks):
    """Tarjetas «Actualidad del sector» del inicio: las tres primeras noticias del resumen semanal."""
    cards = []
    for n in picks:
        bg, fg = COL[n['cat']]
        cards.append(f'<a href="Blog.dc.html" class="card-link" style="background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 16px; overflow: hidden; display: flex; flex-direction: column">'
                     f'<div style="background: {bg}; color: {fg}; padding: 22px 22px 18px; display: flex; flex-direction: column; gap: 2px">'
                     f'<span style="font-family: Archivo, sans-serif; font-weight: 800; font-size: 34px; line-height: 1.05">{e(tr(n["dato"]))}</span>'
                     f'<span style="font-size: 13px; font-weight: 600">{e(tr(n["dato_pie"]))}</span></div>'
                     f'<div style="padding: 22px; display: flex; flex-direction: column; gap: 8px"><span style="font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: {fg}">{e(etiqueta(n))}</span>'
                     f'<h3 style="margin: 0; font-size: 19px; line-height: 1.35">{e(tr(n["titulo"]))}</h3></div></a>')
    m = open(MAIN, encoding='utf-8').read()
    a = m.index('Actualidad del sector</h2>')
    g = m.index('<div', m.index('</div>', a))
    end = m.index('</div>\n</div>', m.rindex('</a>', g, m.index('</section>', g)))
    grid_open = '<div id="home-noticias" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px">'
    m = m[:g] + grid_open + '\n' + '\n'.join(cards) + '\n' + m[end:]
    open(MAIN, 'w', encoding='utf-8').write(m)

def write_tr():
    for d in ALDIA_UI: tr(d)
    with open(B + 'i18n/tr_blogdata.py', 'w', encoding='utf-8') as f:
        f.write('# Generado por deploy/blog_week.py a partir de blog_src/*.json — no editar a mano\nT = ' + repr(TR) + '\n')

if __name__ == '__main__':
    build(); write_tr(); print('ok')
