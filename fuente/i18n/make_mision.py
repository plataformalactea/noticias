import re, glob, json
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
P = B + 'web/project/'
# nav + footer link on every page
for f in glob.glob(P + '*.dc.html'):
    s = open(f, encoding='utf-8').read()
    if 'href="Mision.dc.html" class="nav"' not in s:
        s = re.sub(r'(<a href="Sobre-nosotros\.dc\.html" class="nav"[^>]*>Sobre nosotros</a>)', r'\1\n<a href="Mision.dc.html" class="nav">Misión</a>', s, count=1)
        s = s.replace('<a href="Sobre-nosotros.dc.html">Sobre nosotros</a>', '<a href="Sobre-nosotros.dc.html">Sobre nosotros</a><a href="Mision.dc.html">Misión</a>', 1)
    open(f, 'w', encoding='utf-8').write(s)

tpl = open(P + 'Sobre-nosotros.dc.html', encoding='utf-8').read()
head = tpl[:tpl.index('<section')]; foot = tpl[tpl.index('<footer'):]
head = head.replace('<a href="Sobre-nosotros.dc.html" class="nav" style="color: #2B4F9C">Sobre nosotros</a>', '<a href="Sobre-nosotros.dc.html" class="nav">Sobre nosotros</a>')
head = head.replace('<a href="Mision.dc.html" class="nav">Misión</a>', '<a href="Mision.dc.html" class="nav" style="color: #2B4F9C">Misión</a>')
head = re.sub(r'<title>[^<]*</title>', '<title>Misión · Plataforma Láctea</title>', head, count=1)

K = 'font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2B4F9C'
H2 = 'margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 34px; line-height: 1.12'
TXT = 'margin: 0; font-size: 17px; line-height: 1.65; color: #33435F'
def step(n, t, d, bg, fg):
    return f'<div style="flex: 1 1 240px; min-width: 0; background: {bg}; color: {fg}; border-radius: 18px; padding: 26px 26px 28px; display: flex; flex-direction: column; gap: 10px"><span style="width: 36px; height: 36px; border-radius: 50%; background: #E8B84A; color: #0E2A4F; font-weight: 800; display: flex; align-items: center; justify-content: center">{n}</span><h3 style="margin: 0; font-family: Archivo, sans-serif; font-size: 20px">{t}</h3><p style="margin: 0; font-size: 15px; line-height: 1.55; opacity: .9">{d}</p></div>'
ARROW = '<div aria-hidden="true" style="flex: 0 0 auto; align-self: center; font-size: 28px; font-weight: 800; color: #2B4F9C">→</div>'
def stat(v, l):
    return f'<div style="flex: 1 1 220px; background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 18px; padding: 24px 26px; display: flex; flex-direction: column; gap: 6px"><span style="font-family: Archivo, sans-serif; font-weight: 800; font-size: 44px; color: #2B4F9C; line-height: 1">{v}</span><span style="font-size: 15px; line-height: 1.45; color: #33435F">{l}</span></div>'

body = f'''<section style="background: #0E2A4F; color: #FFFFFF">
<div style="max-width: 1240px; margin: 0 auto; padding: 64px 24px 56px; display: flex; flex-direction: column; gap: 18px">
<span style="{K}; color: #E8B84A">Misión</span>
<h1 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 48px; line-height: 1.08; max-width: 900px">Que el excedente de una industria cubra la necesidad de otra.</h1>
<p style="margin: 0; font-size: 19px; line-height: 1.6; color: #CBD8EE; max-width: 820px">Plataforma Interprofesional Láctea facilita a las industrias lácteas canalizar sus excedentes hacia otras industrias que necesitan cubrir necesidades puntuales, al mejor precio posible y con beneficio para ambas partes.</p>
</div>
</section>

<section>
<div style="max-width: 1240px; margin: 0 auto; padding: 64px 24px 24px; display: flex; flex-direction: column; gap: 28px">
<div style="display: flex; flex-direction: column; gap: 10px"><span style="{K}">Cómo trabajamos</span><h2 style="{H2}">Un mismo producto, dos industrias que ganan.</h2></div>
<div style="display: flex; flex-wrap: wrap; gap: 14px; align-items: stretch">
{step(1, 'Industria con excedente', 'Dispone de leche, nata, mantequilla, polvo o queso que no va a utilizar y quiere darle salida sin perder valor.', '#E6EDF8', '#0E2A4F')}
{ARROW}
{step(2, 'Plataforma Interprofesional Láctea', 'Localiza al comprador adecuado, ajusta producto, precio y calidad, y organiza el transporte y la documentación.', '#0E2A4F', '#FFFFFF')}
{ARROW}
{step(3, 'Industria con necesidad', 'Cubre una necesidad puntual de producción al mejor precio posible y en el plazo que necesita.', '#E6EDF8', '#0E2A4F')}
</div>
</div>
</section>

<section>
<div style="max-width: 1240px; margin: 0 auto; padding: 48px 24px 24px; display: flex; flex-wrap: wrap; gap: 40px; align-items: flex-start">
<div style="flex: 1 1 460px; min-width: 0; display: flex; flex-direction: column; gap: 16px">
<span style="{K}">Medio ambiente</span>
<h2 style="{H2}">Menos kilómetros, menos emisiones.</h2>
<p style="{TXT}">Nuestra propia fórmula de trabajo minimiza la huella de carbono. Buscamos los productos que necesita cada industria aplicando criterios de ahorro en transporte y, por tanto, de menor contaminación ambiental: ponemos a disposición de nuestros clientes los orígenes más cercanos posibles.</p>
<p style="{TXT}">Para ello trabajamos con más de 90 proveedores en diferentes países y elegimos las mejores opciones de transporte, aprovechando los retornos de camiones que vuelven vacíos entre proveedor y cliente. Hoy ya alcanzamos el 99 % de este objetivo.</p>
</div>
<div style="flex: 1 1 420px; min-width: 0; display: flex; flex-wrap: wrap; gap: 14px">
{stat('+90', 'proveedores en diferentes países')}
{stat('99 %', 'de nuestro objetivo de aprovechar los retornos de camiones vacíos, ya alcanzado')}
<div style="flex: 1 1 100%; background: #E6EDF8; border-radius: 18px; padding: 22px 26px; font-size: 15px; line-height: 1.5; color: #0E2A4F"><strong>El origen más cercano posible.</strong> Cuanto más cerca está el proveedor, menos kilómetros recorre el producto y menos emisiones genera.</div>
</div>
</div>
</section>

<section>
<div style="max-width: 1240px; margin: 0 auto; padding: 48px 24px 88px">
<div style="background: #2B4F9C; color: #FFFFFF; border-radius: 22px; padding: 40px; display: flex; flex-wrap: wrap; gap: 28px 48px; align-items: center">
<div style="flex: 0 0 auto; font-family: Archivo, sans-serif; font-weight: 800; font-size: 72px; line-height: 1; color: #E8B84A">3 %</div>
<div style="flex: 1 1 420px; min-width: 0; display: flex; flex-direction: column; gap: 10px">
<span style="{K}; color: #CBD8EE">Compromiso social</span>
<h2 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 28px; line-height: 1.2">En 2026 destinamos el 3 % de los beneficios de la empresa a las personas sin hogar.</h2>
<p style="margin: 0; font-size: 16px; line-height: 1.6; color: #E6EDF8">Colaboramos donando alimentos y dinero en efectivo.</p>
</div>
</div>
</div>
</section>

'''
page = head + body + foot
page = re.sub(r'"\$preview":\{"width":1440,"height":\d+\}', '"$preview":{"width":1440,"height":2200}', page)
open(P + 'Mision.dc.html', 'w', encoding='utf-8').write(page)
c = json.load(open(P + 'canvas.json'))
c['boards']['Mision.dc.html'] = {'x': 15200, 'y': 0, 'w': 1440, 'h': 2200, 'title': 'Misión', 'expand': 'fill'}
if 'Mision.dc.html' not in c['order']: c['order'].insert(c['order'].index('Sobre-nosotros.dc.html') + 1, 'Mision.dc.html')
json.dump(c, open(P + 'canvas.json', 'w'), ensure_ascii=False, indent=2)
print('ok')
