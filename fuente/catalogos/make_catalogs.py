import json, os, html
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
IMG = 'file://' + B + 'catalogos/imgj/'
D = json.load(open(B + 'catalogos/products.json'))
P = {p['id']: p for p in D['P']}
CATS = {c['id']: c['label'] for c in D['CATS']}
E = html.escape
LIN = IMG + 'logo-linsoles.png'
PIL_HD = 'file://' + B + 'catalogos/pil-700.jpg'
PIL_SM = 'file://' + B + 'catalogos/pil-160.jpg'

CSS = '''
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;color:#0E2A4F;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;position:relative;overflow:hidden;background:#FFFFFF;page-break-after:always;display:flex;flex-direction:column}
.page:last-child{page-break-after:auto}
h1,h2,h3{font-family:"Inter Display",Inter,sans-serif;margin:0}
/* cover */
.cover{background:#FFFFFF}
.cover .top{height:9mm;background:linear-gradient(90deg,#0E2A4F,#2B4F9C)}
.cover .mid{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7mm;padding:0 20mm;position:relative}
.cover .mid img{width:132mm}
.cover .kick{font-size:11pt;font-weight:700;letter-spacing:.32em;text-transform:uppercase;color:#2B4F9C}
.cover h1{font-size:34pt;font-weight:800;letter-spacing:-.01em;text-align:center}
.cover .sub{font-size:13pt;color:#4D5D78;text-align:center;max-width:200mm;line-height:1.45}
.cover .bot{background:#0E2A4F;color:#E6EDF8;padding:9mm 16mm;display:flex;align-items:center;gap:10mm}
.cover .bot .pil{width:34mm;height:34mm;border-radius:5mm;background:#FFFFFF;padding:2mm;flex:none;display:flex;align-items:center;justify-content:center}
.cover .bot .pil img{width:100%;height:100%;object-fit:contain}
.cover .bot .co{display:flex;flex-direction:column;gap:1.6mm;font-size:10.5pt;line-height:1.35}
.cover .bot .co b{font-size:14pt;color:#FFFFFF}
.cover .bot .co .row{display:flex;flex-wrap:wrap;gap:1mm 6mm}
.cover .bot .ed{margin-left:auto;white-space:nowrap;text-align:right;font-size:9.5pt;color:#CBD8EE;line-height:1.5}
/* family pages */
.hd{display:flex;align-items:flex-end;justify-content:space-between;gap:10mm;padding:11mm 14mm 6mm;border-bottom:1.2mm solid #2B4F9C}
.hd .k{font-size:9pt;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:#2B4F9C;margin-bottom:2mm}
.hd h2{font-size:27pt;font-weight:800;line-height:1.05}
.hd .intro{font-size:10.5pt;color:#4D5D78;max-width:120mm;line-height:1.45;text-align:right}
.body{flex:1;padding:7mm 14mm 5mm;display:flex;min-height:0}
.grid{display:grid;gap:5mm;width:100%;align-content:stretch}
.card{background:#F4F7FB;border:0.3mm solid #D3DCEA;border-radius:4mm;padding:4mm;display:flex;flex-direction:column;gap:2mm;min-height:0}
.card .ph{flex:1;min-height:0;background:#FFFFFF;border-radius:3mm;display:flex;align-items:center;justify-content:center;padding:2.5mm}
.card .ph img{max-width:100%;max-height:100%;object-fit:contain;display:block}
.card .nm{display:flex;justify-content:space-between;align-items:flex-start;gap:3mm}
.card h3{font-size:12pt;font-weight:800;line-height:1.15}
.chip{flex:none;background:#0E2A4F;color:#FFFFFF;font-size:8pt;font-weight:800;letter-spacing:.06em;padding:1mm 2.4mm;border-radius:10mm;white-space:nowrap}
.spec{font-size:8.3pt;color:#33435F;line-height:1.35;display:flex;flex-direction:column;gap:.5mm}
.spec div{display:flex;justify-content:space-between;gap:3mm;border-top:0.2mm solid #D3DCEA;padding-top:.6mm}
.spec span:last-child{font-weight:700;text-align:right}
.ft{display:flex;align-items:center;gap:4mm;padding:3.5mm 14mm;background:#E6EDF8;font-size:8.3pt;color:#33435F}
.ft img{height:9mm}
.ft .lin{height:7mm}
.ft .pg{margin-left:auto;font-weight:800;color:#0E2A4F}
.note{font-size:8.3pt;color:#4D5D78;font-style:italic;padding:0 14mm 2mm}
/* liquids */
.liq{display:grid;grid-template-columns:1.15fr 1fr;gap:7mm;width:100%}
.liq .big{border-radius:4mm;overflow:hidden;background:#F4F7FB}
.liq .big img{width:100%;height:100%;object-fit:cover;display:block}
.liq ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:3mm}
.liq li{background:#F4F7FB;border:0.3mm solid #D3DCEA;border-radius:3mm;padding:3mm 4mm;display:flex;flex-direction:column;gap:1mm}
.liq li b{font-size:11pt}
.liq li span{font-size:8.6pt;color:#4D5D78;line-height:1.35}
/* retail cheese duo */
.duo{display:grid;grid-template-columns:1fr 1fr;gap:7mm;width:100%}
.blk{border:0.3mm solid #D3DCEA;border-radius:4mm;padding:5mm;display:flex;flex-direction:column;gap:3mm;background:#F4F7FB;min-height:0}
.blk .phs{flex:1;min-height:0;display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.blk .phs figure{margin:0;position:relative;background:#FFFFFF;border-radius:3mm;overflow:hidden;display:flex;align-items:center;justify-content:center}
.blk .phs img{width:100%;height:100%;object-fit:contain}
.blk .phs figcaption{position:absolute;left:2mm;top:2mm;font-size:7.5pt;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:.8mm 2.4mm;border-radius:10mm}
.blk h3{font-size:15pt;font-weight:800}
.blk p{margin:0;font-size:9pt;color:#33435F;line-height:1.4}
'''

def footer(page, total, brand_line):
    return f'''<div class="ft"><img src="{PIL_SM}" alt="P.I.L."><span><b>Plataforma Interprofesional Láctea, S.L.U.</b> · Rosales, 18 · 50008 Zaragoza (Spain) · +34 625 77 97 90 · comercial@plataformalactea.com · www.plataformalactea.com</span><span class="pg">{page} / {total}</span></div>'''

def cover(kicker, title, sub, edition):
    return f'''<section class="page cover"><div class="top"></div>
<div class="mid"><span class="kick">{E(kicker)}</span><img src="{LIN}" alt="Linsoles"><h1>{E(title)}</h1><p class="sub">{E(sub)}</p></div>
<div class="bot"><div class="pil"><img src="{PIL_HD}" alt="P.I.L."></div>
<div class="co"><b>Plataforma Interprofesional Láctea, S.L.U.</b>
<div class="row"><span>Rosales, 18 · 50008 Zaragoza (Spain)</span><span>NIF B10766202 · VAT ESB10766202</span><span>RGSEAA 40.087876/Z</span></div>
<div class="row"><span>Tel. +34 625 77 97 90</span><span>comercial@plataformalactea.com</span><span>www.plataformalactea.com</span></div></div>
<div class="ed">{E(edition)}<br>Desde 1959 en el sector lácteo</div></div></section>'''

def header(kicker, title, intro):
    return f'<div class="hd"><div><div class="k">{E(kicker)}</div><h2>{E(title)}</h2></div><div class="intro">{E(intro)}</div></div>'

def card(img, name, chip, specs):
    sp = ''.join(f'<div><span>{E(a)}</span><span>{E(b)}</span></div>' for a, b in specs)
    ch = f'<span class="chip">{E(chip)}</span>' if chip else ''
    return f'<div class="card"><div class="ph"><img src="{img}" alt="{E(name)}"></div><div class="nm"><h3>{E(name)}</h3>{ch}</div><div class="spec">{sp}</div></div>'

def page(inner_head, body, n, total, note=''):
    nt = f'<div class="note">{E(note)}</div>' if note else ''
    return f'<section class="page">{inner_head}<div class="body">{body}</div>{nt}{footer(n,total,"")}</section>'

def doc(pages, title):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{E(title)}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'

NOTE = 'Datos orientativos. Nos adaptamos a la ficha técnica del cliente.'
IMGF = {'smp':'saco-smp.jpg','wmp':'saco-wmp.jpg','ssmp':'saco-ssmp.jpg','ffmp':'saco-ffmp.jpg','smpsl':'saco-smpsl.jpg','perm':'saco-perm.jpg',
 'cas-a':'saco-cas-a.jpg','cas-r':'saco-cas-r.jpg','casna':'saco-casna.jpg','mcc':'saco-mcc.jpg','swp':'saco-swp.jpg','wpc35':'saco-wpc35.jpg',
 'wpc80':'saco-wpc80.jpg','wpi':'saco-wpi.jpg','mant':'mantequilla.jpg','amf':'bidon-amf.jpg','cagliata':'queso-cagliata.jpg','mozza':'queso-mozza.jpg',
 'edam':'queso-edam.jpg','gouda':'queso-gouda.jpg','emmental':'queso-emmental.jpg','cheddar':'queso-cheddar.jpg'}

def short_pack(p):
    pk = p['pack']
    return pk if len(pk) < 46 else pk.split(';')[0].split(',')[0]

def icards(ids, nspecs=2):
    out = []
    for i in ids:
        p = P[i]
        specs = [(a, b) for a, b in p['params'][:nspecs]]
        specs.append(('Formato', short_pack(p)))
        out.append(card(IMG + IMGF[i], p['name'], p['short'], specs))
    return out

# ---------------- INDUSTRIAL ----------------
fam = [
 ('polvo', 'Leches en polvo para recombinación, lácteos, panadería, confitería y alimentación animal.', ['smp','wmp','ssmp','ffmp','smpsl','perm'], 3),
 ('prot', 'Caseínas y caseinatos para quesos fundidos, cárnicos, nutrición y aplicaciones técnicas.', ['cas-a','cas-r','casna','mcc'], 4),
 ('suero', 'Sueros y proteínas de suero para nutrición deportiva, infantil, bollería y lácteos.', ['swp','wpc35','wpc80','wpi'], 4),
 ('grasa', 'Grasas lácteas para panadería, bollería, chocolate y recombinación.', ['mant','amf'], 2),
 ('liq', None, ['leche-cruda','desnatada','nata','concentrada','suero-liq'], 0),
 ('queso', 'Quesos en bloque para industria, loncheado, rallado y hostelería.', ['cagliata','mozza','edam','gouda','emmental','cheddar'], 3),
]
total = 1 + len(fam)
pages = [cover('Catálogo de producto', 'Lácteos industriales',
               'Leches en polvo, proteínas, sueros, grasas, líquidos lácteos y quesos con la marca Linsoles, desde España para todo el mundo.',
               'Edición 2026')]
for n, (cid, intro, ids, cols) in enumerate(fam, start=2):
    if cid == 'liq':
        lis = ''.join(f'<li><b>{E(P[i]["name"])}</b><span>{E(P[i]["desc"])}</span></li>' for i in ids)
        body = f'<div class="liq"><div class="big"><img src="{IMG}camion-linsoles.jpg" alt="Cisterna Linsoles"></div><ul>{lis}</ul></div>'
        pages.append(page(header('Lácteos industriales · Linsoles', CATS[cid], 'Servidos a granel en cisterna isoterma, refrigerados y con origen controlado.'), body, n, total, NOTE))
        continue
    rows = (len(ids) + cols - 1) // cols
    body = f'<div class="grid" style="grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({rows},1fr)">{"".join(icards(ids, 2 if rows>1 else 3))}</div>'
    pages.append(page(header('Lácteos industriales · Linsoles', CATS[cid], intro), body, n, total, NOTE))
open(B + 'catalogos/industrial.html', 'w', encoding='utf-8').write(doc(pages, 'Catálogo Lácteos industriales · Linsoles'))

# ---------------- RETAIL ----------------
bricks = [('brick-entera.jpg','Leche Entera UHT','1 L',[('Grasa','≥ 3,5 %'),('Proteína','≥ 3,0 %'),('Energía','65 kcal / 100 g'),('EAN','8437026251000')]),
          ('brick-semidesnatada.jpg','Leche Semidesnatada UHT','1 L',[('Grasa','1,5 – 1,8 %'),('Proteína','≥ 3,0 %'),('Energía','47 kcal / 100 g'),('EAN','8437026251017')]),
          ('brick-desnatada.jpg','Leche Desnatada UHT','1 L',[('Grasa','≤ 0,5 %'),('Proteína','≥ 3,0 %'),('Energía','32 kcal / 100 g'),('EAN','8437026251024')])]
common = [('Formato','Brick 1 L con tapón · pack 6 × 1 L'),('Palé','140 packs · 840 uds'),('Consumo preferente','180 días')]
bc = ''.join(card(IMG + f, n, c, s + common) for f, n, c, s in bricks)
rpages = [cover('Catálogo de producto', 'Lácteos Retail / Horeca',
                'Leche UHT y quesos para cadenas de distribución, grandes distribuidores de Horeca y fabricantes. Con nuestra marca o marca blanca.',
                'Edición 2026')]
tot = 4
rpages.append(page(header('Retail / Horeca · Linsoles', 'Leche UHT en brik', 'Leche UHT Linsoles en brik de 1 litro con tapón, en pack de 6 unidades.'),
   f'<div class="grid" style="grid-template-columns:repeat(3,1fr)">{bc}</div>', 2, tot))
def blk(name, desc, a, b, specs):
    sp = ''.join(f'<div><span>{E(x)}</span><span>{E(y)}</span></div>' for x, y in specs)
    return f'''<div class="blk"><div class="phs"><figure><img src="{IMG}{a}" alt="{E(name)} marca Linsoles"><figcaption style="background:#0E2A4F;color:#FFF">Marca Linsoles</figcaption></figure><figure><img src="{IMG}{b}" alt="{E(name)} marca blanca"><figcaption style="background:#E6EDF8;color:#0E2A4F">Marca blanca</figcaption></figure></div>
<h3>{E(name)}</h3><p>{E(desc)}</p><div class="spec">{sp}</div></div>'''
log = [('Formato','Pieza aprox. 3 kg · Ø 19 × 10 cm'),('Caja / palé','2 piezas · 140 piezas por palé'),('Consumo preferente','365 días')]
duo = blk('Queso puro de oveja añejo', 'Leche cruda de oveja, pasta prensada, curación mínima de 270 días.', 'queso-oveja-linsoles.jpg', 'queso-oveja-marca-blanca.jpg',
          [('Grasa','41 g / 100 g'),('Proteína','26 g / 100 g')] + log) + \
      blk('Queso semicurado mezcla', 'Leche pasteurizada de vaca 90 %, oveja 5 % y cabra 5 %. Maduración mínima de 35 días.', 'queso-semicurado-linsoles.jpg', 'queso-semicurado-marca-blanca.jpg',
          [('Grasa','35,6 g / 100 g'),('Proteína','23,2 g / 100 g')] + log)
rpages.append(page(header('Retail / Horeca · Linsoles', 'Quesos nacionales', 'Quesos elaborados en España, con nuestra marca Linsoles o en marca blanca para su cadena.'),
   f'<div class="duo">{duo}</div>', 3, tot))
bars = [('emmental','Emmental','barra-emmental-recorte.jpg','45+'),('cheddar','Cheddar','barra-cheddar-recorte.jpg','48+'),('mozza','Mozzarella','barra-mozza-recorte.jpg','15+ a 48+'),
        ('edam','Edam','barra-edam-recorte.jpg','30+ / 40+'),('gouda','Gouda','barra-gouda-recorte.jpg','48+')]
bcards = ''.join(card(IMG + f, n, 'Barra 3 kg', [('Grasa s/ES', g), ('Conservación', P[i]['store'].replace('Refrigerado a ','').replace('Refrigerada a ','')), ('Vida útil', P[i]['life'])]) for i, n, f, g in bars)
rpages.append(page(header('Retail / Horeca · Linsoles', 'Quesos Horeca', 'Nuestros quesos en barras de 3 kg para hostelería, restauración y distribución.'),
   f'<div class="grid" style="grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)">{bcards}<div class="card" style="background:#0E2A4F;border:none;color:#FFFFFF;justify-content:center;padding:7mm;gap:3mm"><h3 style="font-size:15pt">Barras de 3 kg aprox.</h3><p style="margin:0;font-size:9.5pt;line-height:1.45;color:#CBD8EE">Los mismos quesos de nuestra gama industrial, listos para hostelería y distribución. Con marca Linsoles o en marca blanca.</p><p style="margin:0;font-size:9.5pt;font-weight:700">comercial@plataformalactea.com</p></div></div>', 4, tot, NOTE))
open(B + 'catalogos/retail.html', 'w', encoding='utf-8').write(doc(rpages, 'Catálogo Lácteos Retail / Horeca · Linsoles'))
print('ok', len(pages), len(rpages))
