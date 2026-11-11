import re, html as H, sys, json
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
LI = {'en': 1, 'fr': 2, 'pt': 3}
def load(mod):
    ns = {}; exec(open(B + 'i18n/' + mod + '.py', encoding='utf-8').read(), ns); return ns
D = {}
for m in ['tr_common', 'tr_pages', 'tr_legal', 'tr_prod', 'tr_cat']:
    for t in load(m)['T']: D.setdefault(t[0], t)
def en_num(s):
    s = re.sub(r'(\d)\.(\d{3})(?!\d)', r'\1,\2', s); return re.sub(r'(\d),(\d)', r'\1.\2', s)
MISSING = set()
def tr(s, lang):
    k = re.sub(r'\s+', ' ', s.strip())
    if k in D: return D[k][LI[lang]]
    if lang == 'en' and re.search(r'\d,\d', k) and not re.search(r'[a-záéíóú]{4}', k, re.I): return en_num(k)
    if re.search(r'[A-Za-zÁÉÍÓÚáéíóúñ]{3}', k): MISSING.add(k)
    return None
def translate(doc, lang):
    parts = re.split(r'(<style\b.*?</style>)', doc, flags=re.S)
    for i in range(0, len(parts), 2):
        def rt(m):
            txt = m.group(1)
            if not txt.strip(): return m.group(0)
            t = tr(H.unescape(txt), lang)
            if t is None: return m.group(0)
            return '>' + H.escape(t, quote=False) + '<'
        parts[i] = re.sub(r'>([^<>]+)<', rt, parts[i])
        parts[i] = re.sub(r'\balt="([^"]*)"', lambda m: f'alt="{H.escape(tr(H.unescape(m.group(1)), lang) or H.unescape(m.group(1)))}"', parts[i])
    return ''.join(parts).replace('<html lang="es">', f'<html lang="{lang}">')
if __name__ == '__main__':
    for n in ['industrial', 'retail']:
        es = open(B + f'catalogos/{n}.html', encoding='utf-8').read()
        for lang in LI:
            open(B + f'catalogos/{n}_{lang}.html', 'w', encoding='utf-8').write(translate(es, lang))
    print('missing', sorted(MISSING))
