import os, re, glob, shutil, html as H
from PIL import Image
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
D = B + 'Web_Plataforma_Lactea/'
SITE = 'https://www.plataformalactea.com/'
PAGES = ['index','industriales','retail-horeca','catalogos','blog','sobre-nosotros','mision','solicitud','aviso-legal','privacidad','cookies']
LANGS = ['es', 'en', 'fr', 'pt']

def pages():
    for L in LANGS:
        for p in PAGES:
            yield L, p, D + ('' if L == 'es' else L + '/') + p + '.html'

# ---------- 3. images -> WebP ----------
def images():
    ren = {}
    for f in sorted(glob.glob(D + 'img/*')):
        n = os.path.basename(f); stem, ext = os.path.splitext(n)
        if ext.lower() not in ('.png', '.jpg', '.jpeg'): continue
        im = Image.open(f); im.load()
        mx = 1400 if n.startswith('catalogo-') else (1280 if n.startswith('banner') else 1000)
        if max(im.size) > mx: im.thumbnail((mx, mx), Image.LANCZOS)
        if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA' if 'A' in im.mode or im.mode == 'P' else 'RGB')
        out = D + 'img/' + stem + '.webp'
        im.save(out, 'WEBP', quality=80, method=6)
        os.remove(f); ren[n] = stem + '.webp'
    # rewrite references in every html (incl. JS/JSON data)
    rx = re.compile(r'img/(' + '|'.join(re.escape(k) for k in sorted(ren, key=len, reverse=True)) + r')(?=["\')\s])')
    for p in glob.glob(D + '*.html') + glob.glob(D + '*/*.html'):
        h = open(p, encoding='utf-8').read()
        h2 = rx.sub(lambda m: 'img/' + ren[m.group(1)], h)
        if h2 != h: open(p, 'w', encoding='utf-8').write(h2)
    return len(ren)

# ---------- 10. favicon ----------
def favicon():
    src = Image.open(B + 'prodimg/logo-pil-hd2.png').convert('RGBA')
    bb = src.getbbox(); src = src.crop(bb)
    w, h = src.size; s = max(w, h)
    sq = Image.new('RGBA', (s, s), (0, 0, 0, 0)); sq.paste(src, ((s - w) // 2, (s - h) // 2))
    sq.save(D + 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    sq.resize((192, 192), Image.LANCZOS).save(D + 'icon-192.png', optimize=True)
    bg = Image.new('RGBA', (180, 180), (255, 255, 255, 255)); ic = sq.resize((150, 150), Image.LANCZOS)
    bg.alpha_composite(ic, (15, 15)); bg.convert('RGB').save(D + 'apple-touch-icon.png', optimize=True)

# ---------- 11. meta descriptions ----------
DESC = {
 'index': ('Plataforma Interprofesional Láctea gestiona leche, nata, mantequilla, quesos e ingredientes lácteos para industria, distribución y Horeca. Zaragoza, desde 1959.',
           'Plataforma Interprofesional Láctea supplies milk, cream, butter, cheese and dairy ingredients for industry, retail and food service. Zaragoza, since 1959.',
           'Plataforma Interprofesional Láctea fournit lait, crème, beurre, fromages et ingrédients laitiers pour l’industrie, la distribution et la restauration. Saragosse, depuis 1959.',
           'A Plataforma Interprofesional Láctea fornece leite, nata, manteiga, queijos e ingredientes lácteos para indústria, distribuição e Horeca. Saragoça, desde 1959.'),
 'industriales': ('Lácteos industriales: leche y nata en cisterna, leches en polvo, sueros, caseínas, mantequilla, grasa láctea y quesos en bloque para fabricantes.',
           'Industrial dairy: bulk milk and cream, milk powders, whey, caseins, butter, milk fat and block cheese for manufacturers.',
           'Produits laitiers industriels : lait et crème en citerne, poudres de lait, lactosérums, caséines, beurre, matière grasse laitière et fromages en bloc.',
           'Lácteos industriais: leite e nata em cisterna, leites em pó, soros, caseínas, manteiga, gordura láctea e queijos em bloco para fabricantes.'),
 'retail-horeca': ('Leche UHT y quesos para cadenas de distribución, grandes distribuidores de Horeca y fabricantes. Con marca Linsoles o marca blanca. Fichas técnicas.',
           'UHT milk and cheese for retail chains, large food-service distributors and manufacturers. Linsoles brand or private label. Spec sheets.',
           'Lait UHT et fromages pour la grande distribution, les grossistes CHR et les fabricants. Marque Linsoles ou marque de distributeur. Fiches techniques.',
           'Leite UHT e queijos para cadeias de distribuição, grandes distribuidores Horeca e fabricantes. Marca Linsoles ou marca branca. Fichas técnicas.'),
 'catalogos': ('Catálogos de Plataforma Interprofesional Láctea: lácteos industriales y productos para retail y Horeca. Consulta en línea o descarga en PDF.',
           'Plataforma Interprofesional Láctea catalogues: industrial dairy and retail / food-service products. Browse online or download as PDF.',
           'Catalogues de Plataforma Interprofesional Láctea : produits laitiers industriels et produits pour la distribution et la restauration. En ligne ou en PDF.',
           'Catálogos da Plataforma Interprofesional Láctea: lácteos industriais e produtos para retalho e Horeca. Consulte online ou descarregue em PDF.'),
 'blog': ('Noticias y precios del sector lácteo: leche cruda, leche en polvo, nata, grasas y quesos. Resumen semanal de Plataforma Interprofesional Láctea.',
           'Dairy market news and prices: raw milk, milk powder, cream, fats and cheese. Weekly digest by Plataforma Interprofesional Láctea.',
           'Actualités et prix du secteur laitier : lait cru, poudre de lait, crème, matières grasses et fromages. Synthèse hebdomadaire.',
           'Notícias e preços do setor lácteo: leite cru, leite em pó, nata, gorduras e queijos. Resumo semanal da Plataforma Interprofesional Láctea.'),
 'sobre-nosotros': ('Desde 1959 en el sector lácteo. Conozca Plataforma Interprofesional Láctea: quiénes somos, cómo trabajamos y nuestra red de proveedores.',
           'In the dairy sector since 1959. Get to know Plataforma Interprofesional Láctea: who we are, how we work and our supplier network.',
           'Dans le secteur laitier depuis 1959. Découvrez Plataforma Interprofesional Láctea : qui nous sommes, notre façon de travailler et notre réseau de fournisseurs.',
           'No setor lácteo desde 1959. Conheça a Plataforma Interprofesional Láctea: quem somos, como trabalhamos e a nossa rede de fornecedores.'),
 'mision': ('Nuestra misión: dar salida a los excedentes lácteos, reducir la huella de carbono con más de 90 proveedores y destinar el 3 % del beneficio a personas sin hogar.',
           'Our mission: find outlets for dairy surpluses, cut the carbon footprint with over 90 suppliers and give 3% of profits to people experiencing homelessness.',
           'Notre mission : valoriser les excédents laitiers, réduire l’empreinte carbone avec plus de 90 fournisseurs et reverser 3 % des bénéfices aux personnes sans abri.',
           'A nossa missão: escoar excedentes lácteos, reduzir a pegada de carbono com mais de 90 fornecedores e destinar 3% do lucro a pessoas em situação de sem-abrigo.'),
 'solicitud': ('Solicite información, precios o muestras de leche, nata, mantequilla, quesos e ingredientes lácteos. Respondemos en un día laborable.',
           'Request information, prices or samples of milk, cream, butter, cheese and dairy ingredients. We reply within one working day.',
           'Demandez des informations, des prix ou des échantillons de lait, crème, beurre, fromages et ingrédients laitiers. Réponse sous un jour ouvré.',
           'Peça informações, preços ou amostras de leite, nata, manteiga, queijos e ingredientes lácteos. Respondemos num dia útil.'),
 'aviso-legal': ('Aviso legal de Plataforma Interprofesional Láctea, S.L.U.: datos del titular, condiciones de uso y propiedad intelectual del sitio web.',
           'Legal notice of Plataforma Interprofesional Láctea, S.L.U.: owner details, terms of use and intellectual property of the website.',
           'Mentions légales de Plataforma Interprofesional Láctea, S.L.U. : éditeur, conditions d’utilisation et propriété intellectuelle du site.',
           'Aviso legal da Plataforma Interprofesional Láctea, S.L.U.: dados do titular, condições de utilização e propriedade intelectual do site.'),
 'privacidad': ('Política de privacidad: cómo trata Plataforma Interprofesional Láctea, S.L.U. los datos del formulario de contacto y sus derechos según el RGPD.',
           'Privacy policy: how Plataforma Interprofesional Láctea, S.L.U. handles contact-form data and your rights under the GDPR.',
           'Politique de confidentialité : traitement des données du formulaire de contact par Plataforma Interprofesional Láctea, S.L.U. et vos droits (RGPD).',
           'Política de privacidade: como a Plataforma Interprofesional Láctea, S.L.U. trata os dados do formulário de contacto e os seus direitos (RGPD).'),
 'cookies': ('Política de cookies: este sitio web no utiliza cookies propias ni de terceros, ni herramientas de analítica o publicidad.',
           'Cookie policy: this website uses no first- or third-party cookies and no analytics or advertising tools.',
           'Politique de cookies : ce site n’utilise aucun cookie, propre ou tiers, ni outil d’analyse ou de publicité.',
           'Política de cookies: este site não utiliza cookies próprios nem de terceiros, nem ferramentas de análise ou publicidade.'),
}
LI = {'es': 0, 'en': 1, 'fr': 2, 'pt': 3}

def url(L, p):
    path = ('' if L == 'es' else L + '/') + ('' if p == 'index' else p + '.html')
    return SITE + path

def heads():
    for L, p, f in pages():
        h = open(f, encoding='utf-8').read()
        pre = '' if L == 'es' else '../'
        alt = ''.join(f'<link rel="alternate" hreflang="{x}" href="{url(x, p)}">\n' for x in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{url("es", p)}">\n'
        tags = (f'<meta name="description" content="{H.escape(DESC[p][LI[L]])}">\n'
                f'<link rel="canonical" href="{url(L, p)}">\n' + alt +
                f'<link rel="icon" href="{pre}favicon.ico" sizes="any">\n'
                f'<link rel="icon" type="image/png" sizes="192x192" href="{pre}icon-192.png">\n'
                f'<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">\n')
        assert 'name="description"' not in h, f
        h = h.replace('</title>\n', '</title>\n' + tags, 1)
        assert 'rel="canonical"' in h, f
        open(f, 'w', encoding='utf-8').write(h)

# ---------- 13. 404 ----------
P404 = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Página no encontrada · Plataforma Láctea</title>
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="icon" href="/favicon.ico" sizes="any">
<style>
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#F4F7FB;color:#0E2A4F;font-family:Manrope,system-ui,sans-serif;padding:24px;box-sizing:border-box}
.box{max-width:560px;text-align:center}
img{width:96px;height:auto}
h1{font-family:Archivo,sans-serif;font-weight:800;font-size:clamp(28px,7vw,44px);margin:18px 0 10px}
p{font-size:17px;line-height:1.6;color:#4D5D78;margin:6px 0}
.l{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:26px}
.l a{background:#2B4F9C;color:#fff;text-decoration:none;font-weight:700;padding:12px 18px;border-radius:999px;font-size:14px}
.l a:hover{background:#213E7D}
</style>
</head>
<body>
<div class="box">
<img src="/img/logo-pil.webp" alt="Plataforma Interprofesional Láctea">
<h1>Página no encontrada</h1>
<p>La página que busca no existe o ha cambiado de dirección.</p>
<p lang="en">Page not found · <span lang="fr">Page introuvable</span> · <span lang="pt">Página não encontrada</span></p>
<div class="l">
<a href="/" hreflang="es">Ir al inicio</a>
<a href="/fr/" hreflang="fr" lang="fr">Accueil</a>
<a href="/pt/" hreflang="pt" lang="pt">Início</a>
<a href="/en/" hreflang="en" lang="en">Home</a>
</div>
</div>
</body>
</html>
'''

HTACCESS = '''# Plataforma Interprofesional Láctea · configuración Apache (hosting compartido)
# Cada bloque solo se aplica si el módulo está disponible en el servidor.

AddDefaultCharset UTF-8
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html

# Forzar HTTPS y www (activar cuando el certificado SSL esté instalado)
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} off
  RewriteCond %{HTTP:X-Forwarded-Proto} !https
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  RewriteCond %{HTTP_HOST} ^plataformalactea\\.com$ [NC]
  RewriteRule ^ https://www.plataformalactea.com%{REQUEST_URI} [L,R=301]
  # No servir web.html (versión de vista previa) en producción
  RewriteRule ^web\\.html$ / [L,R=301]
</IfModule>

# Bloquear ficheros ocultos (.htaccess, .git, etc.)
<IfModule mod_authz_core.c>
  <FilesMatch "^\\.">
    Require all denied
  </FilesMatch>
</IfModule>

# Tipos
<IfModule mod_mime.c>
  AddType image/webp .webp
  AddType font/woff2 .woff2
  AddType image/svg+xml .svg
</IfModule>

# Compresión
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json application/xml image/svg+xml
</IfModule>

# Caché del navegador
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault "access plus 1 week"
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType image/webp "access plus 1 month"
  ExpiresByType image/png "access plus 1 month"
  ExpiresByType image/svg+xml "access plus 1 month"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresByType application/pdf "access plus 1 week"
</IfModule>

# Cabeceras de seguridad básicas
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Frame-Options "SAMEORIGIN"
</IfModule>
'''

def extras():
    open(D + '404.html', 'w', encoding='utf-8').write(P404)
    open(D + '.htaccess', 'w', encoding='utf-8').write(HTACCESS)
    open(D + 'robots.txt', 'w', encoding='utf-8').write(f'User-agent: *\nDisallow: /enviar.php\nDisallow: /web.html\n\nSitemap: {SITE}sitemap.xml\n')
    x = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for L, p, f in pages():
        x.append('  <url>')
        x.append(f'    <loc>{url(L, p)}</loc>')
        for a in LANGS: x.append(f'    <xhtml:link rel="alternate" hreflang="{a}" href="{url(a, p)}"/>')
        x.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url("es", p)}"/>')
        x.append('  </url>')
    x.append('</urlset>')
    open(D + 'sitemap.xml', 'w', encoding='utf-8').write('\n'.join(x) + '\n')

if __name__ == '__main__':
    print('webp:', images()); favicon(); heads(); extras(); print('ok')
