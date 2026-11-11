import re, json, html
from html.parser import HTMLParser
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
PAGES = ['index','industriales','retail-horeca','catalogos','blog','sobre-nosotros','mision','solicitud','aviso-legal','privacidad','cookies']
ATTRS = ('alt','placeholder','aria-label','title')
SKIP = re.compile(r'^[\s\d.,:;·•|/+%–\-—×°()<>≥≤=*~#&@_€$"\'’]*$')

def keep(t):
    t = t.strip()
    if not t or SKIP.match(t): return False
    if re.fullmatch(r'[A-Z0-9 .+/·%-]{1,12}', t): return False  # acronyms like SMP, WPC 80, 48+
    if '@' in t and ' ' not in t: return False
    if t.startswith('http') or t.startswith('www.'): return False
    return True

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.stack=[]; s.out=[]; s.scripts=[]
    def handle_starttag(s, tag, attrs):
        s.stack.append(tag)
        for k, v in attrs:
            if k in ATTRS and v and keep(v): s.out.append(v.strip())
    def handle_endtag(s, tag):
        while s.stack and s.stack.pop() != tag: pass
    def handle_data(s, d):
        cur = s.stack[-1] if s.stack else ''
        if cur == 'script': s.scripts.append(d); return
        if cur == 'style': return
        if keep(d): s.out.append(re.sub(r'\s+', ' ', d.strip()))

def js_strings(code):
    res = []
    for m in re.finditer(r"'((?:[^'\\\n]|\\.)*)'", code):
        v = m.group(1)
        if '<' in v or '>' in v:
            for seg in re.split(r'<[^>]*>', v):
                seg = seg.strip()
                if keep(seg) and re.search(r'[a-záéíóúñ]{3}', seg, re.I): res.append(seg)
        elif keep(v) and re.search(r'[a-záéíóúñ]{3}', v, re.I) and not re.fullmatch(r'[\w-]+', v) or (keep(v) and ' ' in v):
            if not v.startswith('#') and 'px' not in v and ':' not in v[:20] or ' ' in v:
                res.append(v)
    return res

allstr = {}
for pg in PAGES:
    h = open(B + 'Web_Plataforma_Lactea/' + pg + '.html', encoding='utf-8').read()
    p = P(); p.feed(h)
    for t in p.out: allstr.setdefault(t, set()).add(pg)
items = sorted(allstr.items(), key=lambda kv: (sorted(kv[1])[0], kv[0]))
json.dump([[k, sorted(v)] for k, v in items], open(B + 'i18n/strings.json', 'w'), ensure_ascii=False, indent=0)
print(len(items), sum(len(k) for k, _ in items))
