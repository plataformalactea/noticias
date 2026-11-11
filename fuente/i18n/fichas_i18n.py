import html as H, re, json
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
IMG = 'file://' + B + 'Web_Plataforma_Lactea/img/'
LOGO = IMG + 'logo-linsoles.png'
LANGS = ['en', 'fr', 'pt']; LI = {'en': 0, 'fr': 1, 'pt': 2}
E = lambda s: H.escape(s, quote=False)

def L(en, fr, pt): return (en, fr, pt)
def n(s, lang):  # number formatting
    if lang != 'en': return s.replace('.', ' ') if re.fullmatch(r'\d{1,3}(\.\d{3})+', s) and lang == 'fr' else s
    s = re.sub(r'(\d)\.(\d{3})(?!\d)', r'\1,\2', s); return re.sub(r'(\d),(\d)', r'\1.\2', s)
def t(x, lang):
    if isinstance(x, tuple): return x[LI[lang]]
    return n(x, lang)

CSS = '''@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Inter,Arial,sans-serif;color:#1d2433;font-size:7.7pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:210mm;height:297mm;padding:10mm 13mm 16mm;position:relative;overflow:hidden;page-break-after:always}.pg:last-child{page-break-after:auto}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:8mm;margin-bottom:4mm}
.top .co{font-size:13pt;font-weight:800;color:#0E2A4F}.top .sub{font-size:8.5pt;font-weight:700;color:#4D5D78;letter-spacing:.04em;text-transform:uppercase;margin-top:1mm}
.top img{height:12mm}.meta{font-size:8pt;text-align:right;line-height:1.5;color:#33435F}
h1{margin:1mm 0 .5mm;font-size:15pt;color:#0E2A4F}.line{color:#4D5D78;font-size:8.6pt;margin-bottom:3mm}
table{width:100%;border-collapse:collapse;margin:0 0 2.6mm}td,th{border:0.25mm solid #9aa7bd;padding:0.8mm 1.8mm;vertical-align:middle;text-align:left}
th{background:#D9E2F3;color:#0E2A4F;font-weight:800;font-size:7.8pt}td.k{background:#D9E2F3;font-weight:700;color:#0E2A4F;width:34%}
td.c,th.c{text-align:center}.sec th{text-transform:uppercase;letter-spacing:.03em}
.two{display:grid;grid-template-columns:1fr 1fr;gap:4mm;align-items:start}.two table{margin:0}
.hero{display:grid;grid-template-columns:30mm 1fr;gap:6mm;margin-bottom:3.5mm}.hero img{width:100%;object-fit:contain}
.note{font-size:7.4pt;color:#4D5D78;font-style:italic;margin:1mm 0}
.foot{position:absolute;left:14mm;right:14mm;bottom:8mm;border-top:0.4mm solid #0E2A4F;padding-top:2mm;text-align:center;font-size:7.4pt;color:#4D5D78}
.foot b{color:#0E2A4F}.tl{font-size:7.6pt;color:#B4232A;font-weight:700;margin-bottom:2mm}
'''
def kv(rows, lang, head=None):
    h = f'<tr class="sec"><th colspan="2">{E(t(head,lang))}</th></tr>' if head else ''
    return '<table>' + h + ''.join(f'<tr><td class="k">{E(t(a,lang))}</td><td>{E(t(b,lang))}</td></tr>' for a, b in rows) + '</table>'
def grid(headrow, rows, lang, title=None, center_from=1):
    h = f'<tr class="sec"><th colspan="{len(headrow)}">{E(t(title,lang))}</th></tr>' if title else ''
    h += '<tr>' + ''.join(f'<th class="{"c" if i>=center_from else ""}">{E(t(c,lang))}</th>' for i, c in enumerate(headrow)) + '</tr>'
    return '<table>' + h + ''.join('<tr>' + ''.join(f'<td class="{"c" if i>=center_from else ""}">{E(t(c,lang))}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows) + '</table>'

TRANS_NOTE = L('Translation provided for information purposes. In case of discrepancy, the Spanish version prevails.',
               'Traduction fournie à titre informatif. En cas de divergence, la version espagnole prévaut.',
               'Tradução fornecida a título informativo. Em caso de divergência, prevalece a versão espanhola.')
DOCTITLE = L('TECHNICAL DATA SHEET', 'FICHE TECHNIQUE', 'FICHA TÉCNICA')

def page(lang, body, title, line, company='Linsoles', meta='', footer=''):
    return f'''<section class="pg"><div class="top"><div><div class="co">{E(company)}</div><div class="sub">{E(t(DOCTITLE,lang))}</div></div><div style="display:flex;gap:6mm;align-items:flex-start">{f'<div class="meta">{meta}</div>' if meta else ''}<img src="{LOGO}" alt="Linsoles"></div></div>
<div class="tl">{E(t(TRANS_NOTE,lang))}</div><h1>{E(t(title,lang))}</h1><div class="line">{E(t(line,lang))}</div>{body}<div class="foot">{footer}</div></section>'''

def doc(lang, pages, title):
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{E(title)}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'

LFOOT = '<b>LINSOLES FOODS, S.L.U.</b> · C/ Ministro Cornel, 44 · 22440 Benasque (Huesca) · '
LFOOT_C = L('Spain', 'Espagne', 'Espanha')

# common labels
K = dict(
 cons=L('Storage','Conservation','Conservação'), shelf=L('Shelf life','Durée de vie','Validade'), allerg=L('ALLERGENS','ALLERGÈNES','ALERGÉNIOS'),
 milk_all=L('Contains milk and milk products (including lactose).','Contient du lait et des produits laitiers (y compris le lactose).','Contém leite e produtos lácteos (incluindo lactose).'),
 product=L('PRODUCT','PRODUIT','PRODUTO'), denom=L('DESCRIPTION','DÉNOMINATION','DENOMINAÇÃO'), pres=L('PRESENTATION','PRÉSENTATION','APRESENTAÇÃO'),
 fq=L('PHYSICO-CHEMICAL CHARACTERISTICS','CARACTÉRISTIQUES PHYSICO-CHIMIQUES','CARACTERÍSTICAS FÍSICO-QUÍMICAS'),
 indic=L('Indicative data. We adapt to the customer’s specification.','Données indicatives. Nous nous adaptons au cahier des charges du client.','Dados indicativos. Adaptamo-nos à ficha técnica do cliente.'),
)
PFOOT = '<b>Plataforma Interprofesional Láctea, S.L.U.</b> · Rosales, 18 · 50008 Zaragoza · +34 625 77 97 90 · comercial@plataformalactea.com'

# ---------------- BARS ----------------
BARS = {
 'Emmental': dict(name=L('EMMENTAL CHEESE «LINSOLES» · 3 KG BAR','FROMAGE EMMENTAL «LINSOLES» · BARRE 3 KG','QUEIJO EMMENTAL «LINSOLES» · BARRA 3 KG'),
   d=L('Cooked pressed cheese with eyes, for grating, slicing and gratins.','Fromage à pâte pressée cuite à ouverture, pour râper, trancher et gratiner.','Queijo de pasta prensada cozida com olhos, para ralar, fatiar e gratinar.'),
   p=[(L('Fat (in dry matter)','Matière grasse (sur extrait sec)','Gordura (s/ extrato seco)'),'≥ 45 %'),(L('Moisture','Humidité','Humidade'),'≤ 40 %'),(L('Salt','Sel','Sal'),'0,6 – 1,2 %')],
   c=L('Chilled at 2–8 °C','Réfrigéré entre 2 et 8 °C','Refrigerado a 2–8 °C'), v=L('3–6 months','3–6 mois','3–6 meses')),
 'Cheddar': dict(name=L('CHEDDAR CHEESE «LINSOLES» · 3 KG BAR','FROMAGE CHEDDAR «LINSOLES» · BARRE 3 KG','QUEIJO CHEDDAR «LINSOLES» · BARRA 3 KG'),
   d=L('Pressed cheese coloured orange with annatto. For slicing, grating, sauces, burgers and ready meals.','Fromage à pâte pressée coloré au rocou, de couleur orange. Pour trancher, râper, sauces, burgers et plats préparés.','Queijo de pasta prensada corado com urucum, de cor laranja. Para fatiar, ralar, molhos, hambúrgueres e pratos preparados.'),
   p=[(L('Fat (in dry matter)','Matière grasse (sur extrait sec)','Gordura (s/ extrato seco)'),'≥ 48 %'),(L('Moisture','Humidité','Humidade'),'≤ 39 %'),(L('Salt','Sel','Sal'),'1,4 – 2,0 %'),(L('Colouring','Colorant','Corante'),L('Annatto (E160b)','Rocou (E160b)','Urucum (E160b)'))],
   c=L('Chilled at 2–8 °C','Réfrigéré entre 2 et 8 °C','Refrigerado a 2–8 °C'), v=L('6–9 months','6–9 mois','6–9 meses')),
 'Mozzarella': dict(name=L('MOZZARELLA CHEESE «LINSOLES» · 3 KG BAR','FROMAGE MOZZARELLA «LINSOLES» · BARRE 3 KG','QUEIJO MOZZARELLA «LINSOLES» · BARRA 3 KG'),
   d=L('Pasta filata cheese with good melt, for pizza, ready meals and foodservice.','Fromage à pâte filée au bon fondant, pour pizzas, plats préparés et restauration.','Queijo de pasta filada com boa fusão, para pizza, pratos preparados e hotelaria.'),
   p=[(L('Fat (in dry matter)','Matière grasse (sur extrait sec)','Gordura (s/ extrato seco)'),L('15+ / 40+ / 45+ / 48+ (by type)','15+ / 40+ / 45+ / 48+ (selon le type)','15+ / 40+ / 45+ / 48+ (conforme o tipo)')),(L('Moisture','Humidité','Humidade'),'≤ 52 %'),(L('Salt','Sel','Sal'),'1,0 – 1,8 %')],
   c=L('Chilled at 0–4 °C','Réfrigérée entre 0 et 4 °C','Refrigerada a 0–4 °C'), v=L('60–90 days','60–90 jours','60–90 dias')),
 'Edam': dict(name=L('EDAM CHEESE «LINSOLES» · 3 KG BAR','FROMAGE ÉDAM «LINSOLES» · BARRE 3 KG','QUEIJO EDAM «LINSOLES» · BARRA 3 KG'),
   d=L('Semi-cured pressed cheese, for slicing, grating and as an ingredient.','Fromage mi-affiné à pâte pressée, pour trancher, râper et comme ingrédient.','Queijo meio-curado de pasta prensada, para fatiar, ralar e como ingrediente.'),
   p=[(L('Fat (in dry matter)','Matière grasse (sur extrait sec)','Gordura (s/ extrato seco)'),L('30+ / 40+ (by type)','30+ / 40+ (selon le type)','30+ / 40+ (conforme o tipo)')),(L('Moisture','Humidité','Humidade'),'≤ 46 %'),(L('Salt','Sel','Sal'),'1,5 – 2,2 %')],
   c=L('Chilled at 2–8 °C','Réfrigéré entre 2 et 8 °C','Refrigerado a 2–8 °C'), v=L('3–6 months','3–6 mois','3–6 meses')),
 'Gouda': dict(name=L('GOUDA CHEESE «LINSOLES» · 3 KG BAR','FROMAGE GOUDA «LINSOLES» · BARRE 3 KG','QUEIJO GOUDA «LINSOLES» · BARRA 3 KG'),
   d=L('Semi-cured pressed cheese, for slicing, grating and counter sales.','Fromage à pâte pressée mi-affiné, pour trancher, râper et vente à la coupe.','Queijo de pasta prensada meio-curado, para fatiar, ralar e venda ao corte.'),
   p=[(L('Fat (in dry matter)','Matière grasse (sur extrait sec)','Gordura (s/ extrato seco)'),'≥ 48 %'),(L('Moisture','Humidité','Humidade'),'≤ 42 %'),(L('Salt','Sel','Sal'),'1,5 – 2,2 %')],
   c=L('Chilled at 2–8 °C','Réfrigéré entre 2 et 8 °C','Refrigerado a 2–8 °C'), v=L('3–6 months','3–6 mois','3–6 meses')),
}
def bar(lang, k):
    q = BARS[k]
    body = kv([(K['product'], q['name'])], lang) + kv([(K['denom'], q['d']), (K['pres'], L('Bar of approx. 3 kg','Barre d’env. 3 kg','Barra de aprox. 3 kg'))], lang) + \
           kv(q['p'], lang, K['fq']) + kv([(K['cons'], q['c']), (K['shelf'], q['v'])], lang) + kv([(K['allerg'], K['milk_all'])], lang) + f'<p class="note">{E(t(K["indic"],lang))}</p>'
    return doc(lang, [page(lang, body, q['name'], L('Linsoles brand · 3 kg bar','Marque Linsoles · barre de 3 kg','Marca Linsoles · barra de 3 kg'), 'Linsoles', '', PFOOT)], k)

# ---------------- SEMICURED ----------------
def semi(lang):
    nut = [(L('Energy','Valeur énergétique','Valor energético'),'414 kcal'),(L('Fat','Matières grasses','Lípidos'),'35,6 g'),(L('of which saturates','dont acides gras saturés','dos quais saturados'),'24 g'),
           (L('Carbohydrate','Glucides','Hidratos de carbono'),'0,2 g'),(L('of which sugars','dont sucres','dos quais açúcares'),'0,2 g'),(L('Protein','Protéines','Proteínas'),'23,2 g'),(L('Salt','Sel','Sal'),'1,85 g')]
    body = kv([(K['product'], L('SEMI-CURED MIXED-MILK CHEESE «LINSOLES» 3 KG','FROMAGE MI-AFFINÉ AU LAIT DE MÉLANGE «LINSOLES» 3 KG','QUEIJO DE MISTURA MEIO-CURADO «LINSOLES» 3 KG'))], lang) + \
      kv([(K['denom'], L('Semi-cured cheese made from pasteurised cow’s, sheep’s and goat’s milk.','Fromage mi-affiné au lait pasteurisé de vache, de brebis et de chèvre.','Queijo meio-curado elaborado com leite pasteurizado de vaca, ovelha e cabra.')),
          (L('INGREDIENTS','INGRÉDIENTS','INGREDIENTES'), L('Pasteurised cow’s milk (90 %), pasteurised sheep’s milk (5 %), pasteurised goat’s milk (5 %), salt, rennet, calcium chloride and lactic cultures.','Lait de vache pasteurisé (90 %), lait de brebis pasteurisé (5 %), lait de chèvre pasteurisé (5 %), sel, présure, chlorure de calcium et ferments lactiques.','Leite de vaca pasteurizado (90 %), leite de ovelha pasteurizado (5 %), leite de cabra pasteurizado (5 %), sal, coalho, cloreto de cálcio e fermentos lácticos.')),
          (L('RIPENING','AFFINAGE','MATURAÇÃO'), L('Minimum 35 days.','Minimum 35 jours.','Mínimo 35 dias.'))], lang) + \
      '<div class="two">' + kv([(L('Colour','Couleur','Cor'),L('Ivory white','Blanc ivoire','Branco marfim')),(L('Texture','Texture','Textura'),L('Semi-hard and buttery','Demi-dure et fondante','Semidura e amanteigada')),(L('Aroma','Arôme','Aroma'),L('Lactic, with notes of butter and yogurt','Lactique, avec des notes de beurre et de yaourt','Láctico, com notas de manteiga e iogurte')),(L('Flavour','Saveur','Sabor'),L('Balanced, slightly sweet, with a hint of nuts','Équilibrée, légèrement douce, avec un rappel de fruits secs','Equilibrado, ligeiramente doce, com lembrança de frutos secos'))], lang, L('ORGANOLEPTIC CHARACTERISTICS','CARACTÉRISTIQUES ORGANOLEPTIQUES','CARACTERÍSTICAS ORGANOLÉTICAS')) + \
      kv([(L('Dry matter','Extrait sec','Extrato seco'),'> 50 %'),(L('Moisture','Humidité','Humidade'),'< 50 %'),(L('Fat in dry matter','Matière grasse sur extrait sec','Gordura s/ extrato seco'),'> 45 %'),(L('Protein in dry matter','Protéines sur extrait sec','Proteína s/ extrato seco'),'> 25 %'),('pH','< 5,5')], lang, K['fq']) + '</div><div style="height:2.6mm"></div>' + \
      kv(nut, lang, L('AVERAGE NUTRITIONAL INFORMATION (per 100 g)','INFORMATION NUTRITIONNELLE MOYENNE (pour 100 g)','INFORMAÇÃO NUTRICIONAL MÉDIA (por 100 g)')) + \
      kv([(K['allerg'], L('Contains milk and milk products (including lactose). Not suitable for people allergic to milk proteins.','Contient du lait et des produits laitiers (y compris le lactose). Ne convient pas aux personnes allergiques aux protéines de lait.','Contém leite e produtos lácteos (incluindo lactose). Não adequado para pessoas alérgicas às proteínas do leite.'))], lang) + \
      kv([(L('BEST BEFORE','À CONSOMMER DE PRÉFÉRENCE AVANT','CONSUMIR DE PREFERÊNCIA ANTES DE'),L('365 days','365 jours','365 dias')),(L('TRANSPORT TEMPERATURE','TEMPÉRATURE DE TRANSPORT','TEMPERATURA DE TRANSPORTE'),L('Refrigerated at 1–8 °C.','Réfrigéré entre 1 et 8 °C.','Refrigerado de 1 a 8 °C.')),(L('STORAGE','CONSERVATION','CONSERVAÇÃO'),L('Keep in a cool, dry place.','Conserver dans un endroit frais et sec.','Conservar em local fresco e seco.'))], lang) + packing(lang)
    return doc(lang, [page(lang, body, L('Semi-cured mixed-milk cheese «Linsoles»','Fromage mi-affiné au lait de mélange «Linsoles»','Queijo de mistura meio-curado «Linsoles»'), L('Linsoles brand or private label · wheel of approx. 3 kg','Marque Linsoles ou marque de distributeur · pièce d’env. 3 kg','Marca Linsoles ou marca branca · peça de aprox. 3 kg'), 'Linsoles', '', PFOOT)], 'Semicurado')

def packing(lang):
    U, C, P = L('SALES UNIT','UNITÉ DE VENTE','UNIDADE DE VENDA'), L('CASE','CARTON','CAIXA'), L('PALLET','PALETTE','PALETE')
    rows = [(U, L('Approx. weight (kg)','Poids approx. (kg)','Peso aprox. (kg)'), '3,000'), (U, L('Approx. height (cm)','Hauteur approx. (cm)','Altura aprox. (cm)'), '10'), (U, L('Approx. diameter (cm)','Diamètre approx. (cm)','Diâmetro aprox. (cm)'), '19'),
            (U, L('Packaging','Conditionnement','Embalagem'), L('Food-grade cardboard cases','Cartons de qualité alimentaire','Caixas de cartão de uso alimentar')),
            (C, L('Case weight (kg)','Poids du carton (kg)','Peso da caixa (kg)'), '0,272'), (C, L('Case dimensions (cm)','Dimensions du carton (cm)','Dimensões da caixa (cm)'), '40,5 × 21,0 × 12,2'), (C, L('Units per case','Unités par carton','Unidades por caixa'), '2'),
            (P, L('Pallet type','Type de palette','Tipo de palete'), L('Euro pallet','Europalette','Europeia')), (P, L('Cases per layer','Cartons par couche','Caixas por camada'), '10'), (P, L('Layers','Nombre de couches','N.º de camadas'), '7'),
            (P, L('Cases','Nombre de cartons','N.º de caixas'), '70'), (P, L('Wheels','Nombre de pièces','N.º de peças'), '140'), (P, L('Approx. net weight (kg)','Poids net approx. (kg)','Peso líquido aprox. (kg)'), '420'), (P, L('Dimensions (cm)','Dimensions (cm)','Dimensões (cm)'), '120 × 80 × 100,4')]
    out = f'<table><tr class="sec"><th colspan="3">{E(t(L("PACKAGING AND PALLETISATION","EMBALLAGE ET PALETTISATION","EMBALAGEM E PALETIZAÇÃO"),lang))}</th></tr>'
    prev = None
    for g, a, b in rows:
        span = sum(1 for r in rows if r[0] == g)
        first = g != prev; prev = g
        out += '<tr>' + (f'<td class="k" rowspan="{span}" style="width:22%">{E(t(g,lang))}</td>' if first else '') + f'<td>{E(t(a,lang))}</td><td>{E(t(b,lang))}</td></tr>'
    return out + '</table>'

# ---------------- SHEEP ----------------
def oveja(lang):
    yes, no = L('Yes','Oui','Sim'), L('No','Non','Não')
    p1 = kv([(K['product'], L('AGED RAW SHEEP’S MILK CHEESE 3 KG','FROMAGE AU LAIT CRU DE BREBIS AFFINÉ 3 KG','QUEIJO DE LEITE CRU DE OVELHA VELHO 3 KG'))], lang) + \
      kv([(L('INGREDIENTS','INGRÉDIENTS','INGREDIENTES'), L('Raw sheep’s milk, salt, rennet, stabiliser: calcium chloride, and lactic cultures. Inedible rind. On the rind: preservatives (E-202, E-235) and colour (E-160b(ii)). Origin of the milk: SPAIN.',
                                                          'Lait cru de brebis, sel, présure, stabilisant : chlorure de calcium et ferments lactiques. Croûte non comestible. Sur la croûte : conservateurs (E-202, E-235) et colorant (E-160b(ii)). Origine du lait : ESPAGNE.',
                                                          'Leite cru de ovelha, sal, coalho, estabilizador: cloreto de cálcio e fermentos lácticos. Casca não comestível. Na casca: conservantes (E-202, E-235) e corante (E-160b(ii)). Origem do leite: ESPANHA.'))], lang) + \
      kv([(L('Colour','Couleur','Cor'),L('Honey','Miel','Mel')),(L('Smell','Odeur','Cheiro'),L('Characteristic of the cheese','Caractéristique du fromage','Característico do queijo')),(L('Texture','Texture','Textura'),L('Characteristic of the cheese','Caractéristique du fromage','Característica do queijo'))], lang, L('ORGANOLEPTIC CHARACTERISTICS','CARACTÉRISTIQUES ORGANOLEPTIQUES','CARACTERÍSTICAS ORGANOLÉTICAS')) + \
      kv([(L('INTENDED USE','USAGE PRÉVU','USO PREVISTO'), L('Suitable for everyone except infants, people allergic to milk and people intolerant to lactose.','Convient à tous, à l’exception des nourrissons, des personnes allergiques au lait et des personnes intolérantes au lactose.','Adequado para todos, exceto lactentes, pessoas alérgicas ao leite e pessoas intolerantes à lactose.')),
          (L('DIRECTIONS FOR USE','MODE D’EMPLOI','MODO DE UTILIZAÇÃO'), L('To serve, cut with a two-handled knife and leave in a covered cheese dish at room temperature for about 30 minutes. Ideal serving temperature 16 °C. Once cut, wrap in food film and keep at around 5 °C.','Pour la consommation, couper avec un couteau à deux manches et placer dans une cloche à fromage à température ambiante environ 30 minutes avant. Température optimale de dégustation : 16 °C. Une fois entamé, envelopper le fromage dans un film alimentaire et le conserver à environ 5 °C.','Para consumir, cortar com uma faca de dois cabos e colocar numa queijeira à temperatura ambiente cerca de 30 minutos antes. Temperatura ideal de consumo: 16 °C. Depois de aberto, envolver em película alimentar e conservar a cerca de 5 °C.')),
          (L('RECOMMENDATIONS','RECOMMANDATIONS','RECOMENDAÇÕES'), L('On receipt, remove the plastic film from the pallet and take the cheeses out of the cases so they can breathe; this helps preserve them.','Dès réception, retirer le film plastique de la palette et sortir les fromages des cartons pour une bonne aération, ce qui favorise leur conservation.','Ao receber, retirar o filme plástico da palete e tirar os queijos das caixas para um correto arejamento, o que favorece a sua conservação.')),
          (L('BEST BEFORE','À CONSOMMER DE PRÉFÉRENCE AVANT','CONSUMIR DE PREFERÊNCIA ANTES DE'), L('365 days','365 jours','365 dias')),
          (L('CODING','CODAGE','CODIFICAÇÃO'), L('Packing batch: MNNNAA (M = line no.; NNN = Julian day of packing; AA = calendar year)','Lot de conditionnement : MNNNAA (M = n° de ligne ; NNN = jour julien ; AA = année)','Lote de embalamento: MNNNAA (M = n.º da linha; NNN = dia juliano; AA = ano)'))], lang) + \
      grid([L('Microorganism','Micro-organisme','Microrganismo'),L('Criticality','Criticité','Criticidade'),'n','c','m','M'],
           [['Salmonella /25 g',L('Pathogen','Pathogène','Patogénico'),'5','0',L('Not detected','Non détecté','Não detetado'),L('Not detected','Non détecté','Não detetado')],
            ['Listeria monocytogenes /25 g',L('Pathogen','Pathogène','Patogénico'),'5','0',L('Not detected','Non détecté','Não detetado'),L('Not detected','Non détecté','Não detetado')],
            [L('Coagulase-positive staphylococci','Staphylocoques à coagulase positive','Estafilococos coagulase positivos'),L('Indicator','Indicateur','Indicador'),'5','2','< 10⁴ ufc/g','< 10⁵ ufc/g']], lang, L('MICROBIOLOGICAL CHARACTERISTICS','CARACTÉRISTIQUES MICROBIOLOGIQUES','CARACTERÍSTICAS MICROBIOLÓGICAS')) + \
      kv([(L('TRANSPORT TEMPERATURE','TEMPÉRATURE DE TRANSPORT','TEMPERATURA DE TRANSPORTE'),L('Refrigerated at 1–8 °C.','Réfrigéré entre 1 et 8 °C.','Refrigerado de 1 a 8 °C.')),(L('STORAGE','CONSERVATION','CONSERVAÇÃO'),L('Keep in a cool, dry place.','Conserver dans un endroit frais et sec.','Conservar em local fresco e seco.')),
          (L('PROCESS','PROCÉDÉ','MÉTODO DE TRATAMENTO'),L('Solid product resulting from the enzymatic coagulation of raw sheep’s milk, pressed and aged for at least 270 days.','Produit solide issu de la coagulation enzymatique du lait cru de brebis, à pâte pressée et affiné au minimum 270 jours.','Produto sólido resultante da coagulação enzimática de leite cru de ovelha, de pasta prensada e com uma cura mínima de 270 dias.'))], lang)
    chem = [(L('Energy (kJ)','Valeur énergétique (kJ)','Valor energético (kJ)'),'1990'),(L('Energy (kcal)','Valeur énergétique (kcal)','Valor energético (kcal)'),'480'),(L('Fat (g)','Matières grasses (g)','Lípidos (g)'),'41'),(L('of which saturates (g)','dont acides gras saturés (g)','dos quais saturados (g)'),'29'),
            (L('Carbohydrate (g)','Glucides (g)','Hidratos de carbono (g)'),'1'),(L('of which sugars (g)','dont sucres (g)','dos quais açúcares (g)'),'< 0,1'),(L('Protein (g)','Protéines (g)','Proteínas (g)'),'26'),(L('Salt (g)','Sel (g)','Sal (g)'),'1,9'),
            (L('Calcium','Calcium','Cálcio'),'800'),(L('Minimum dry matter','Extrait sec minimum','Extrato seco mínimo'),'0,73'),('pH','5,96'),('aw','0,92')]
    cont = [(L('Sum of dioxins','Somme des dioxines','Soma de dioxinas'),L('2.0 pg/g fat','2,0 pg/g MG','2,0 pg/g gordura')),(L('Sum of dioxins and dioxin-like PCBs (milk)','Somme des dioxines et PCB de type dioxine (lait)','Soma de dioxinas e PCB sob a forma de dioxina (leite)'),L('4.0 pg/g fat','4,0 pg/g MG','4,0 pg/g gordura')),
            (L('Sum of PCB28, 52, 101, 138, 153 and 180','Somme des PCB28, 52, 101, 138, 153 et 180','Soma de PCB28, 52, 101, 138, 153 e 180'),L('40 ng/g fat','40 ng/g MG','40 ng/g gordura')),(L('Aflatoxin M1 (milk)','Aflatoxine M1 (lait)','Aflatoxina M1 (leite)'),'< 0,05 µg/kg'),
            (L('Lead (milk)','Plomb (lait)','Chumbo (leite)'),'< 0,02 mg/kg'),(L('Nitrates','Nitrates','Nitratos'),'< 150 mg/L'),(L('Natamycin (cheese)','Natamycine (fromage)','Natamicina (queijo)'),L('< 1 mg/dm² (absent at 5 mm depth)','< 1 mg/dm² (absente à 5 mm de profondeur)','< 1 mg/dm² (ausente a 5 mm de profundidade)')),(L('Melamine','Mélamine','Melamina'),'< 2,5 mg/kg'),
            (L('GMO-free','Sans OGM','Livre de OGM'),yes),(L('Not irradiated','Non irradié','Livre de irradiação'),yes)]
    allergens = [L('Cereals containing gluten','Céréales contenant du gluten','Cereais que contêm glúten'),L('Crustaceans','Crustacés','Crustáceos'),L('Eggs','Œufs','Ovos'),L('Fish','Poissons','Peixes'),L('Peanuts','Arachides','Amendoins'),L('Soybeans','Soja','Soja'),
                 L('Nuts','Fruits à coque','Frutos de casca rija'),L('Celery','Céleri','Aipo'),L('Mustard','Moutarde','Mostarda'),L('Sesame seeds','Graines de sésame','Sementes de sésamo'),L('Sulphur dioxide and sulphites > 10 mg/kg','Anhydride sulfureux et sulfites > 10 mg/kg','Dióxido de enxofre e sulfitos > 10 mg/kg'),L('Lupin','Lupin','Tremoço'),L('Molluscs','Mollusques','Moluscos')]
    p2 = kv(chem, lang, L('NUTRITIONAL INFORMATION (per 100 g)','INFORMATION NUTRITIONNELLE (pour 100 g)','INFORMAÇÃO NUTRICIONAL (por 100 g)')) + kv(cont, lang, L('CHEMICAL CONTAMINANTS AND OTHER','CONTAMINANTS CHIMIQUES ET AUTRES','CONTAMINANTES QUÍMICOS E OUTROS')) + \
      grid([L('Allergen','Allergène','Alergénio'),L('Contains','Contient','Contém'),L('Does not contain','Ne contient pas','Não contém')],
           [[L('Milk and milk products (including lactose)','Lait et produits laitiers (y compris le lactose)','Leite e produtos lácteos (incluindo lactose)'),'X','']] + [[a,'','X'] for a in allergens], lang, K['allerg']) + \
      f'<p class="note">{E(t(L("May contain traces of cow’s and goat’s milk.","Peut contenir des traces de lait de vache et de chèvre.","Pode conter vestígios de leite de vaca e de cabra."),lang))}</p>'
    regs = ['(CE) 852/2004', '(CE) 853/2004', '(CE) 2073/2005', '(UE) 2023/915', '(UE) 1169/2011']
    REG = L('Regulation','Règlement','Regulamento'); RD = L('Spanish Royal Decree 1113/2006 on quality standards for cheeses','Décret royal espagnol 1113/2006 sur les normes de qualité des fromages','Real Decreto espanhol 1113/2006 relativo às normas de qualidade dos queijos')
    p3 = packing(lang) + '<table><tr class="sec"><th>' + E(t(L('APPLICABLE LEGISLATION (as amended)','LÉGISLATION APPLICABLE (et modifications)','LEGISLAÇÃO APLICÁVEL (e alterações)'),lang)) + '</th></tr>' + \
         ''.join(f'<tr><td>{E(t(REG,lang))} {r}</td></tr>' for r in regs) + f'<tr><td>{E(t(RD,lang))}</td></tr></table>'
    title = L('Aged pure sheep’s cheese «Linsoles»','Fromage pur brebis affiné «Linsoles»','Queijo puro de ovelha velho «Linsoles»')
    line = L('Linsoles brand or private label · wheel of approx. 3 kg','Marque Linsoles ou marque de distributeur · pièce d’env. 3 kg','Marca Linsoles ou marca branca · peça de aprox. 3 kg')
    return doc(lang, [page(lang, p1, title, line, 'Linsoles', '', PFOOT), page(lang, p2, title, line, 'Linsoles', '', PFOOT), page(lang, p3, title, line, 'Linsoles', '', PFOOT)], 'Oveja')

# ---------------- UHT ----------------
UHT = {
 'Entera': dict(code='251000', ean='8437026251000', img='brick-entera.png', name=L('Whole UHT Milk','Lait entier UHT','Leite Gordo UHT'), legal=L('UHT sterilised whole milk','Lait entier stérilisé UHT','Leite gordo esterilizado UHT'), ing=L('Whole milk','Lait entier','Leite gordo'),
   fat='≥ 3,5', kj='271 / 65', g='3,6', sat='2,2', col='#B4232A'),
 'Semidesnatada': dict(code='251017', ean='8437026251017', img='brick-semidesnatada.png', name=L('Semi-skimmed UHT Milk','Lait demi-écrémé UHT','Leite Meio-Gordo UHT'), legal=L('UHT sterilised semi-skimmed milk','Lait demi-écrémé stérilisé UHT','Leite meio-gordo esterilizado UHT'), ing=L('Semi-skimmed milk','Lait demi-écrémé','Leite meio-gordo'),
   fat='1,5 – 1,8', kj='197 / 47', g='1,6', sat='1,0', col='#1D4F8C'),
 'Desnatada': dict(code='251024', ean='8437026251024', img='brick-desnatada.png', name=L('Skimmed UHT Milk','Lait écrémé UHT','Leite Magro UHT'), legal=L('UHT sterilised skimmed milk','Lait écrémé stérilisé UHT','Leite magro esterilizado UHT'), ing=L('Skimmed milk','Lait écrémé','Leite magro'),
   fat='≤ 0,5', kj='138 / 32', g='0', sat='0', col='#2F6E2A'),
}
def uht(lang, k):
    u = UHT[k]
    meta = f'{E(t(L("Code","Code","Código"),lang))}: <b>{u["code"]}</b><br>EAN: <b>{u["ean"]}</b><br>{E(t(L("Updated","Mise à jour","Atualização"),lang))}: <b>27/09/2026</b><br>{E(t(L("Version","Version","Versão"),lang))}: <b>1</b>'
    gen = kv([(L('Legal name','Dénomination légale','Denominação legal'),u['legal']),(L('Ingredients','Ingrédients','Ingredientes'),u['ing']),(L('Brand','Marque','Marca'),'Linsoles'),
              (L('Format','Format','Formato'),L('1 L carton with cap · pack of 6 units','Brique de 1 L avec bouchon · pack de 6 unités','Pacote de 1 L com tampa · pack de 6 unidades')),(L('Origin of the milk','Origine du lait','Origem do leite'),L('France','France','França')),
              (L('GMO','OGM','OGM'),L('Contains no GMOs under Regulations (EC) 1829/2003 and 1830/2003','Ne contient pas d’OGM selon les règlements (CE) 1829/2003 et 1830/2003','Não contém OGM de acordo com os Regulamentos (CE) 1829/2003 e 1830/2003')),
              (L('Ionisation','Ionisation','Ionização'),L('Product not treated with ionising radiation','Produit non traité par rayonnements ionisants','Produto não tratado com radiações ionizantes')),
              (L('Allergens','Allergènes','Alergénios'),L('Contains milk and milk products (including lactose)','Contient du lait et des produits laitiers (y compris le lactose)','Contém leite e produtos lácteos (incluindo lactose)')),
              (L('Contaminants','Contaminants','Contaminantes'),L('Complies with current legislation on contaminants (dioxins, heavy metals, mycotoxins) and pesticide residues','Conforme à la législation en vigueur sur les contaminants (dioxines, métaux lourds, mycotoxines) et résidus de pesticides','Cumpre a legislação em vigor sobre contaminantes (dioxinas, metais pesados, micotoxinas) e resíduos de pesticidas')),
              (L('Storage','Conservation','Conservação'),L('Before opening, keep in a cool, dry place. Once opened, keep refrigerated (max. +6 °C) and consume within 4 days','Avant ouverture, conserver dans un endroit frais et sec. Après ouverture, conserver au réfrigérateur (max. +6 °C) et consommer dans les 4 jours','Antes de abrir, conservar em local fresco e seco. Depois de aberto, manter refrigerado (máx. +6 °C) e consumir no prazo de 4 dias')),
              (L('Best before','À consommer de préférence avant','Consumir de preferência antes de'),L('180 days from packing date','180 jours à compter de la date de conditionnement','180 dias a partir da data de embalamento')),
              (L('Marking','Marquage','Marcação'),L('Batch, date and health registration number printed on the pack','Lot, date et numéro d’enregistrement sanitaire imprimés sur l’emballage','Lote, data e registo sanitário impressos na embalagem'))], lang, L('GENERAL INFORMATION','INFORMATIONS GÉNÉRALES','INFORMAÇÃO GERAL'))
    hero = f'<div class="hero"><img src="{IMG}{u["img"]}" alt=""><div>{gen}</div></div>'
    qual = kv([(L('Fat (%)','Matière grasse (%)','Matéria gorda (%)'),u['fat']),(L('Protein (%)','Protéines (%)','Proteína (%)'),'≥ 3,0'),('pH','6,5 – 6,9'),(L('Total plate count at 30 °C (cfu/0.1 ml)','Flore totale à 30 °C (ufc/0,1 ml)','Flora total a 30 °C (ufc/0,1 ml)'),'< 10')], lang, L('QUALITY INFORMATION','INFORMATIONS QUALITÉ','INFORMAÇÃO DE QUALIDADE'))
    nut = grid([L('Average values','Valeurs moyennes','Valores médios'),L('Per 100 g','Pour 100 g','Por 100 g')],
               [[L('Energy (kJ / kcal)','Énergie (kJ / kcal)','Valor energético (kJ / kcal)'),u['kj']],[L('Fat (g)','Matières grasses (g)','Lípidos (g)'),u['g']],[L('of which saturates (g)','dont acides gras saturés (g)','dos quais saturados (g)'),u['sat']],
                [L('Carbohydrate (g)','Glucides (g)','Hidratos de carbono (g)'),'4,8'],[L('of which sugars (g)','dont sucres (g)','dos quais açúcares (g)'),'4,8'],[L('Protein (g)','Protéines (g)','Proteínas (g)'),'3,3'],[L('Salt (g)','Sel (g)','Sal (g)'),'0,1'],
                [L('Calcium (mg)','Calcium (mg)','Cálcio (mg)'),L('120 (15 % RI)','120 (15 % VNR)','120 (15 % VRN)')]], lang, L('NUTRITION INFORMATION','VALEURS NUTRITIONNELLES','VALORES NUTRICIONAIS'))
    TBA = L('To be assigned','À attribuer','A atribuir')
    log1 = kv([(L('Units / pack','Unités / pack','Unidades / pack'),'6'),(L('Packs / layer','Packs / couche','Packs / camada'),'28'),(L('Layers / pallet','Couches / palette','Camadas / palete'),'5'),(L('Packs / pallet','Packs / palette','Packs / palete'),'140'),(L('Units / pallet','Unités / palette','Unidades / palete'),'840')], lang, L('PALLETISATION','PALETTISATION','PALETIZAÇÃO'))
    log2 = grid(['',L('Unit','Unité','Unidade'),'Pack*',L('Pallet','Palette','Palete')],
                [[L('EAN code','Code EAN','Código EAN'),u['ean'],TBA,TBA],[L('Net weight (kg)','Poids net (kg)','Peso líquido (kg)'),'1,03','6,19','866,88'],[L('Gross weight (kg)','Poids brut (kg)','Peso bruto (kg)'),'1,06','6,40','920,65'],[L('Dimensions (mm)','Dimensions (mm)','Dimensões (mm)'),'90 × 59 × 210','270 × 117 × 210','1200 × 800 × 1217']], lang, L('LOGISTICS INFORMATION','INFORMATIONS LOGISTIQUES','INFORMAÇÃO LOGÍSTICA'))
    notes = [L('* Pack: 6 units grouped under shrink film.','* Pack : 6 unités regroupées sous film rétractable.','* Pack: 6 unidades agrupadas sob filme retrátil.'),
             L('RI: reference intake (Regulation (EU) 1169/2011). cfu: colony-forming units.','VNR : valeur nutritionnelle de référence (règlement (UE) 1169/2011). ufc : unités formant colonie.','VRN: valor de referência do nutriente (Regulamento (UE) 1169/2011). ufc: unidades formadoras de colónias.'),
             L('The information in this sheet is indicative and may change without notice. The information on the pack label always prevails.','Les informations de cette fiche sont indicatives et peuvent être modifiées sans préavis. L’étiquetage de l’emballage prévaut toujours.','A informação desta ficha é indicativa e pode ser alterada sem aviso prévio. Prevalece sempre a informação do rótulo da embalagem.')]
    body = hero + f'<div class="two">{qual}{nut}</div><div style="height:2.6mm"></div><div class="two" style="grid-template-columns:0.7fr 1.3fr">{log1}{log2}</div>' + ''.join(f'<p class="note">{E(t(x,lang))}</p>' for x in notes)
    foot = LFOOT + E(t(LFOOT_C, lang)) + '<br>' + E(t(L('Marketed by: Linsoles Foods, S.L.U.','Commercialisé par : Linsoles Foods, S.L.U.','Responsável pela comercialização: Linsoles Foods, S.L.U.'),lang))
    return doc(lang, [page(lang, body, u['name'], L('Linsoles brand · 1 L carton with cap · Pack 6 × 1 L','Marque Linsoles · brique 1 L avec bouchon · pack 6 × 1 L','Marca Linsoles · pacote 1 L com tampa · pack 6 × 1 L'), 'LINSOLES FOODS, S.L.U.', meta, foot)], k)

JOBS = []
for lang in LANGS:
    for k in BARS: JOBS.append((f'Ficha_Linsoles_Queso_{k}_Barra_3kg_{lang.upper()}', bar(lang, k)))
    JOBS.append((f'Ficha_Linsoles_Queso_Semicurado_Mezcla_{lang.upper()}', semi(lang)))
    JOBS.append((f'Ficha_Linsoles_Queso_Oveja_Anejo_3kg_{lang.upper()}', oveja(lang)))
    for k in UHT: JOBS.append((f'Ficha_Linsoles_Leche_{k}_UHT_1L_{lang.upper()}', uht(lang, k)))
import os
os.makedirs(B + 'i18n/fichas', exist_ok=True)
for name, h in JOBS: open(B + f'i18n/fichas/{name}.html', 'w', encoding='utf-8').write(h)
json.dump([j[0] for j in JOBS], open(B + 'i18n/fichas/list.json', 'w'))
print(len(JOBS))
