import re, glob
P = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/web/project/'
def rd(f): return open(P + f, encoding='utf-8').read()
def wr(f, s): open(P + f, 'w', encoding='utf-8').write(s)
def rep(s, a, b, n=1):
    assert s.count(a) >= 1, a[:80]
    return s.replace(a, b) if n == 0 else s.replace(a, b, n)

# 1 mobile hero
s = rd('Main.dc.html')
s = rep(s, '<h1 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 56px;', '<h1 class="hero-h1" style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 56px;')
s = rep(s, '<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px; background: #FFFFFF; border-radius: 16px; padding: 16px 26px; align-self: flex-start; max-width: 620px"><p style="',
           '<div class="hero-box" style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px; background: #FFFFFF; border-radius: 16px; padding: 16px 26px; align-self: flex-start; max-width: 100%; box-sizing: border-box"><p style="')
if '.hero-h1{' not in s:
    s = rep(s, '</style>', '.hero-h1{font-size:clamp(28px,8vw,56px)!important;overflow-wrap:anywhere}\n.hero-box p{font-size:clamp(19px,5.4vw,26px)!important}\n@media (max-width:480px){.hero-box{padding:14px 18px!important}}\n</style>')
wr('Main.dc.html', s)

# 2 checkbox
s = rd('Solicitud.dc.html')
s = re.sub(r'(<input type="checkbox"[^>]*>)He leído la (<a href="Privacidad\.dc\.html">política de privacidad</a>) y acepto que Plataforma Interprofesional Láctea, S\.L\.U\. trate mis datos para responder a esta solicitud\.</label>',
           r'\1<span>He leído la \2 y acepto que Plataforma Interprofesional Láctea, S.L.U. trate mis datos para responder a esta solicitud.</span></label>', s)
assert '<span>He leído la' in s
wr('Solicitud.dc.html', s)

# 5 legal placeholders
for f in ['AvisoLegal.dc.html', 'Privacidad.dc.html', 'Cookies.dc.html']:
    s = rd(f); s = rep(s, 'Última actualización: [fecha de publicación] · Ver también:', 'Ver también:'); wr(f, s)
s = rd('AvisoLegal.dc.html')
s, n = re.subn(r'<div style="[^"]*"><span style="color: #4D5D78">Registro Mercantil</span><span style="[^"]*">[^<]*</span></div>', '', s)
assert n == 1; wr('AvisoLegal.dc.html', s)

# 6 cookies
s = rd('Cookies.dc.html')
a = s.index('<h2', s.index('1. Qué son las cookies') + 30); b = s.index('<h2', s.index('3. Cómo gestionar o retirar'))
H2 = re.search(r'<h2 style="[^"]*">', s).group(0); PP = re.search(r'<p style="margin: 0; font-size: 16px[^"]*">', s).group(0)
new = (H2 + '2. Uso de cookies en este sitio</h2>' + PP + 'Este sitio web no utiliza cookies ni tecnologías similares: no instala cookies propias ni de terceros, no usa herramientas de analítica ni de publicidad y no carga contenidos de otros servidores. Por eso no se muestra ningún aviso de cookies.</p>'
       + PP + 'Si en el futuro se incorporan cookies no necesarias, se le pedirá previamente su consentimiento y esta política se actualizará.</p>'
       + H2 + '3. Cómo gestionar las cookies en su navegador</h2>' + PP + 'Puede eliminar o bloquear las cookies desde la configuración de su navegador (Chrome, Firefox, Safari, Edge u otros).</p>')
s = s[:a] + new + s[b:]
assert 'Cookie técnica' not in s and '4. Más información' in s
wr('Cookies.dc.html', s)

# 7 privacy: IP
s = rd('Privacidad.dc.html')
s = rep(s, '<li>Información sobre su consulta: producto de interés, volúmenes, especificaciones y el contenido de su mensaje.</li>',
        '<li>Información sobre su consulta: producto de interés, volúmenes, especificaciones y el contenido de su mensaje.</li><li>Datos técnicos del envío del formulario: dirección IP, fecha y hora. Se usan solo para evitar abusos y envíos automáticos (spam). Base: interés legítimo en la seguridad del sitio (art. 6.1.f RGPD).</li>')
wr('Privacidad.dc.html', s)

# 8 + 9 every page
for f in glob.glob(P + '*.dc.html'):
    s = open(f, encoding='utf-8').read()
    s = s.replace('line-height: 1.15">Plataforma Interprofesional Láctea S.L.U.</span>', 'line-height: 1.15">Plataforma Interprofesional Láctea S.L.</span>')
    s = s.replace('50008 Zaragoza (Spain)', '50008 Zaragoza (España)')
    open(f, 'w', encoding='utf-8').write(s)
print('ok')
