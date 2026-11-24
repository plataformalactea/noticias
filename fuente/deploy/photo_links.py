# Marca las fotos de producto con data-ficha (PDF) y añade el marco al pasar el ratón
# y la apertura de la ficha en el idioma de la página. Se ejecuta tras build_static.py.
import os, re, glob
B = os.environ['PIL_FUENTE'].rstrip('/') + '/'
W = B + 'Web_Plataforma_Lactea/'
F = 'fichas/Ficha_Linsoles_'
MAP = {  # nombre de imagen (sin extensión) -> PDF
 'saco-smp': 'SMP',
 'brick-entera': 'Leche_Entera_UHT_1L', 'brick-semidesnatada': 'Leche_Semidesnatada_UHT_1L', 'brick-desnatada': 'Leche_Desnatada_UHT_1L',
 'queso-oveja-entero': 'Queso_Oveja_Anejo_3kg', 'queso-oveja-linsoles': 'Queso_Oveja_Anejo_3kg', 'queso-oveja-marca-blanca': 'Queso_Oveja_Anejo_3kg',
 'queso-semicurado-entero': 'Queso_Semicurado_Mezcla', 'queso-semicurado-linsoles': 'Queso_Semicurado_Mezcla', 'queso-semicurado-marca-blanca': 'Queso_Semicurado_Mezcla',
 'barra-emmental': 'Queso_Emmental_Barra_3kg', 'barra-cheddar': 'Queso_Cheddar_Barra_3kg', 'barra-mozza': 'Queso_Mozzarella_Barra_3kg',
 'barra-edam': 'Queso_Edam_Barra_3kg', 'barra-gouda': 'Queso_Gouda_Barra_3kg',
}
CSS = ('<style id="ficha-css">[data-ficha]{cursor:pointer;outline:3px solid transparent;outline-offset:-3px;border-radius:12px;'
       'transition:outline-color .15s}[data-ficha]:hover,[data-ficha]:focus-visible{outline-color:#2B4F9C}'
       'a.cta[data-ficha]{outline:none}</style>')
JS = ('<script id="ficha-js">(function(){var L=(document.documentElement.lang||"es").slice(0,2).toLowerCase();'
      'function u(f){return L==="es"?f:"../"+f.replace(/\\.pdf$/,"_"+L.toUpperCase()+".pdf");}'
      'document.addEventListener("click",function(e){var t=e.target.closest("[data-ficha]");if(!t)return;'
      'if(t.tagName==="IMG"&&parseFloat(getComputedStyle(t).opacity)<0.99&&t.parentNode){var o=-1;'
      '[].forEach.call(t.parentNode.querySelectorAll("img"),function(x){var v=parseFloat(getComputedStyle(x).opacity);if(v>o){o=v;t=x;}});'
      'if(!t.hasAttribute("data-ficha"))return;}'
      'e.preventDefault();e.stopPropagation();window.open(u(t.getAttribute("data-ficha")),"_blank","noopener");},true);})();</script>')

def mark(m):
    tag = m.group(0)
    if 'data-ficha' in tag: return tag
    name = os.path.splitext(os.path.basename(m.group(1)))[0].replace('-recorte', '')
    if name not in MAP: return tag
    return tag[:-1].rstrip('/') + f' data-ficha="{F}{MAP[name]}.pdf" title="Ver ficha técnica">'

for f in glob.glob(W + '*.html'):
    s = open(f).read()
    s = re.sub(r'<img[^>]*\bsrc="img/([^"]+)"[^>]*>', mark, s)
    if 'id="ficha-js"' not in s and '</body>' in s:
        s = s.replace('</head>', CSS + '</head>', 1).replace('</body>', JS + '</body>', 1)
    open(f, 'w').write(s)
print('photo_links ok')
