import re, json, subprocess, html as H
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
OUT = B + 'Web_Plataforma_Lactea/'
PAGES = ['index','industriales','retail-horeca','catalogos','blog','sobre-nosotros','mision','solicitud','aviso-legal','privacidad','cookies']
LANGS = ['en', 'fr', 'pt']
LI = {'en': 1, 'fr': 2, 'pt': 3}

def load(mod):
    ns = {}; exec(open(B + 'i18n/' + mod + '.py', encoding='utf-8').read(), ns); return ns
WEB = {}
for m in ['tr_common', 'tr_pages', 'tr_legal', 'tr_blog', 'tr_aldia']:
    for t in load(m)['T']: WEB[t[0]] = t
P = load('tr_prod'); PROD = {t[0]: t for t in P['T']}; UI = P['UI']
CAT_TITLES = {t[0]: t for t in WEB.values()}
PAGE_WORD = {'en': ('Page', 'of'), 'fr': ('Page', 'sur'), 'pt': ('Página', 'de')}
CAT_WORD = {'en': 'Catalogue, page', 'fr': 'Catalogue, page', 'pt': 'Catálogo, página'}

def en_num(s):
    s = re.sub(r'(\d)\.(\d{3})(?!\d)', r'\1,\2', s)
    s = re.sub(r'(\d),(\d)', r'\1.\2', s)
    return s

def tr(s, lang, table=WEB):
    k = s.strip()
    if k in table: return table[k][LI[lang]]
    m = re.fullmatch(r'Página (\d+) de (\d+)', k)
    if m: w = PAGE_WORD[lang]; return f'{w[0]} {m.group(1)} {w[1]} {m.group(2)}'
    m = re.fullmatch(r'Catálogo, página (\d+): (.+)', k)
    if m: return f'{CAT_WORD[lang]} {m.group(1)}: {tr(m.group(2), lang)}'
    return None

MISSING = set()
SAME = {'© 2026 Plataforma Interprofesional Láctea S.L.','Plataforma Interprofesional Láctea S.L.','50008 Zaragoza (Spain)','Plataforma Interprofesional Láctea S.L.U.','Web','Plataforma Interprofesional Láctea','Plataforma Interprofesional Láctea, S.L.U.','Plataforma Láctea','Rosales, 18','© 2026 Plataforma Interprofesional Láctea, S.L.U.','Linsoles'}

def tr_text_nodes(doc, lang):
    # split into script/style blocks and the rest
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', doc, flags=re.S)
    for i in range(0, len(parts), 2):
        seg = parts[i]
        def rep_text(m):
            txt = m.group(1)
            if not txt.strip(): return m.group(0)
            raw = H.unescape(txt)
            norm = re.sub(r'\s+', ' ', raw.strip())
            t = tr(norm, lang)
            if t is None:
                if re.search(r'[A-Za-zÁÉÍÓÚáéíóúñÑ]{3}', norm) and norm not in SAME: MISSING.add(norm)
                return m.group(0)
            lead = txt[:len(txt) - len(txt.lstrip())]; trail = txt[len(txt.rstrip()):]
            return '>' + lead + H.escape(t, quote=False) + trail + '<'
        seg = re.sub(r'>([^<>]+)<', rep_text, seg)
        def rep_attr(m):
            a, v = m.group(1), m.group(2)
            t = tr(H.unescape(v), lang)
            if t is None: return m.group(0)
            return f'{a}="{H.escape(t)}"'
        seg = re.sub(r'\b(alt|placeholder|aria-label|title)="([^"]*)"', rep_attr, seg)
        parts[i] = seg
    return ''.join(parts)

def switcher(page, lang):
    cur = lang or 'es'
    out = []
    for L in ['es', 'fr', 'pt', 'en']:
        if L == 'es': href = (page + '.html') if not lang else ('../' + page + '.html')
        else: href = (f'{L}/{page}.html') if not lang else (f'../{L}/{page}.html')
        st = 'color: #0E2A4F; text-decoration: underline; text-underline-offset: 3px' if L == cur else 'color: #4D5D78; text-decoration: none'
        out.append(f'<a href="{href}" hreflang="{L}" lang="{L}" style="{st}">{L.upper()}</a>')
    return '<span style="font-size: 13px; font-weight: 700; color: #4D5D78; letter-spacing: 0.04em; display: inline-flex; gap: 6px">' + ' · '.join(out) + '</span>'

SW = re.compile(r'<span style="font-size: 13px; font-weight: 700; color: #4D5D78; letter-spacing: 0.04em[^"]*">(?:ES · FR · PT · EN|.*?</a></span>)', re.S)

def prod_tr(s, lang):
    if not isinstance(s, str): return s
    if s in PROD: return PROD[s][LI[lang]]
    return en_num(s) if lang == 'en' else s

def tr_industriales_js(doc, lang):
    a = doc.index('var CATS'); b = doc.index('var state=')
    js = doc[a:b]
    data = json.loads(subprocess.run(['node', '-e', js.replace('var ', 'globalThis.', ) + ';console.log(JSON.stringify({CATS,PRODUCTS,IMG,TANK,MICRO}))'], capture_output=True, text=True, check=True).stdout)
    for c in data['CATS']: c['label'] = prod_tr(c['label'], lang)
    data['MICRO'] = [[prod_tr(x, lang) for x in r] for r in data['MICRO']]
    for p in data['PRODUCTS']:
        for k in ('name', 'short', 'alt', 'desc', 'pack', 'store', 'life'):
            if k in p: p[k] = prod_tr(p[k], lang)
        p['params'] = [[prod_tr(x, lang) for x in r] for r in p['params']]
    new = ''.join(f'var {k} = {json.dumps(data[k], ensure_ascii=False)};\n' for k in ('CATS', 'PRODUCTS', 'IMG', 'TANK', 'MICRO'))
    doc = doc[:a] + new + doc[b:]
    for u in UI:
        assert u[0] in doc, u[0]
        v = u[LI[lang]]
        if not (v.startswith("'") and v.endswith("'")): v = v.replace("'", '’')
        doc = doc.replace(u[0], v)
    return doc

def localise_assets(doc, lang):
    sfx = '_' + lang.upper()
    doc = re.sub(r'(href|download)="(?:fichas/)?(Ficha_[^"]+?)\.pdf"', lambda m: f'{m.group(1)}="' + ('../fichas/' if m.group(1) == 'href' else '') + m.group(2) + sfx + '.pdf"', doc)
    doc = re.sub(r'(href|download)="(?:catalogos/)?(Catalogo_[^"]+?)\.pdf"', lambda m: f'{m.group(1)}="' + ('../catalogos/' if m.group(1) == 'href' else '') + m.group(2) + sfx + '.pdf"', doc)
    doc = re.sub(r'img/catalogo-(industrial|retail)-(\d+)\.jpg', lambda m: f'img/catalogo-{m.group(1)}-{m.group(2)}-{lang}.jpg', doc)
    doc = re.sub(r'(src|href)="(img/|fichas/|catalogos/)', r'\1="../\2', doc)
    doc = re.sub(r"'(img/[^']+)'", r"'../\1'", doc)  # JS image paths (industriales)
    doc = re.sub(r'(?<!=)"(img/[^"]+)"', r'"../\1"', doc)  # JSON image paths
    return doc

import os
for lang in LANGS: os.makedirs(OUT + lang, exist_ok=True)
for page in PAGES:
    es = open(OUT + page + '.html', encoding='utf-8').read()
    es = SW.sub(lambda m: switcher(page, None), es, count=1)
    open(OUT + page + '.html', 'w', encoding='utf-8').write(es)
    for lang in LANGS:
        d = es.replace('<html lang="es">', f'<html lang="{lang}">', 1)
        if page == 'industriales': d = tr_industriales_js(d, lang)
        d = tr_text_nodes(d, lang)
        d = SW.sub(lambda m: switcher(page, lang), d, count=1)
        d = localise_assets(d, lang)
        open(OUT + lang + '/' + page + '.html', 'w', encoding='utf-8').write(d)
print('missing:', sorted(MISSING))
