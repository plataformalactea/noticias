import re, glob, json
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
P = B + 'web/project/'
src = open(B + 'catalogos/add_viewer.py', encoding='utf-8').read()
exec(src[:src.index('\napply(')])  # IND, RET, titles, BASE_CSS, viewer(), apply()

# 1) remove viewer section + its CSS from the product pages
for f in ['Industriales.dc.html', 'Retail-Horeca.dc.html']:
    s = open(P + f, encoding='utf-8').read()
    if 'id="catalogo"' in s:
        a = s.index('<section id="catalogo">'); b = s.index('</section>', a) + len('</section>')
        s = s[:a].rstrip('\n') + '\n' + s[b:].lstrip('\n')
        a = s.index('\n.cv{display:flex'); b = s.index('</style>', a)
        s = s[:a] + '\n' + s[b:]
    open(P + f, 'w', encoding='utf-8').write(s)

# 2) nav item "Catálogos" on every page (before Blog)
for f in glob.glob(P + '*.dc.html'):
    s = open(f, encoding='utf-8').read()
    if 'href="Catalogos.dc.html" class="nav"' in s: continue
    s = re.sub(r'(<a href="Blog\.dc\.html" class="nav"[^>]*>Blog</a>)', r'<a href="Catalogos.dc.html" class="nav">Catálogos</a>\n\1', s, count=1)
    s = s.replace('<a href="Retail-Horeca.dc.html">Lácteos Retail / Horeca</a></div>\n<div style="display: flex; flex-direction: column; gap: 10px; font-size: 14px"><span style="font-weight: 700; color: #FFFFFF">Empresa</span>',
                  '<a href="Retail-Horeca.dc.html">Lácteos Retail / Horeca</a><a href="Catalogos.dc.html">Catálogos</a></div>\n<div style="display: flex; flex-direction: column; gap: 10px; font-size: 14px"><span style="font-weight: 700; color: #FFFFFF">Empresa</span>')
    open(f, 'w', encoding='utf-8').write(s)

# 3) new page from Sobre-nosotros shell
tpl = open(P + 'Sobre-nosotros.dc.html', encoding='utf-8').read()
head = tpl[:tpl.index('<section')]
foot = tpl[tpl.index('<footer'):]
head = head.replace('<a href="Sobre-nosotros.dc.html" class="nav" style="color: #2B4F9C">Sobre nosotros</a>', '<a href="Sobre-nosotros.dc.html" class="nav">Sobre nosotros</a>')
head = head.replace('<a href="Catalogos.dc.html" class="nav">Catálogos</a>', '<a href="Catalogos.dc.html" class="nav" style="color: #2B4F9C">Catálogos</a>')
head = re.sub(r'<title>[^<]*</title>', '<title>Catálogos · Plataforma Láctea</title>', head, count=1)
vi, ci = viewer('ci', IND, IND_T, 'f27038ba815803a11a7def6e09fc9bcb', 'Catalogo_Linsoles_Lacteos_Industriales.pdf', 'Lácteos industriales',
                'Leches en polvo, proteínas, sueros, grasas, líquidos lácteos y quesos. 7 páginas.')
vr, cr = viewer('cr', RET, RET_T, '6f9b51182fe0b9a576ea6d92cce1f0bd', 'Catalogo_Linsoles_Retail_Horeca.pdf', 'Lácteos Retail / Horeca',
                'Leche UHT en brik, quesos nacionales y quesos Horeca. 4 páginas.')
vi = vi.replace('<section id="catalogo">', '<section id="cat-industrial">')
vr = vr.replace('<section id="catalogo">', '<section id="cat-retail">').replace('padding: 40px 24px 8px', 'padding: 56px 24px 88px')
hero = '''<section style="background: #E6EDF8">
<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px 40px; display: flex; flex-direction: column; gap: 18px">
<span style="font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2B4F9C">Catálogos</span>
<h1 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 48px; line-height: 1.05">Catálogos de producto</h1>
<p style="margin: 0; font-size: 18px; line-height: 1.55; color: #33435F; max-width: 760px">Hojee nuestros catálogos página a página o descárguelos en PDF para compartirlos con su equipo.</p>
<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px">
<a href="#cat-industrial" class="tab" style="background: #0E2A4F; color: #FFFFFF">Lácteos industriales</a>
<a href="#cat-retail" class="tab" style="background: #FFFFFF; color: #0E2A4F">Lácteos Retail / Horeca</a>
</div>
</div>
</section>

'''
page = head + hero + vi + '\n' + vr + '\n' + foot
j = page.index('</style>')
page = page[:j] + BASE_CSS + ci + '\n' + cr + '\n' + page[j:]
page = re.sub(r'"\$preview":\{"width":1440,"height":\d+\}', '"$preview":{"width":1440,"height":2700}', page)
open(P + 'Catalogos.dc.html', 'w', encoding='utf-8').write(page)

c = json.load(open(P + 'canvas.json'))
c['boards']['Catalogos.dc.html'] = {'x': 13680, 'y': 0, 'w': 1440, 'h': 2700, 'title': 'Catálogos', 'expand': 'fill'}
if 'Catalogos.dc.html' not in c['order']: c['order'].insert(c['order'].index('Blog.dc.html'), 'Catalogos.dc.html')
for f, h in [('Industriales.dc.html', 2300), ('Retail-Horeca.dc.html', 4200)]:
    c['boards'][f]['h'] = h
    s = open(P + f, encoding='utf-8').read()
    s = re.sub(r'"\$preview":\{"width":1440,"height":\d+\}', '"$preview":{"width":1440,"height":%d}' % h, s); open(P + f, 'w', encoding='utf-8').write(s)
json.dump(c, open(P + 'canvas.json', 'w'), ensure_ascii=False, indent=2)
print('ok')
