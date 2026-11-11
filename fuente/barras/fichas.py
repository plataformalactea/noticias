from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
H=colors.HexColor('#D9E2F3'); B=colors.black
st=ParagraphStyle('n',fontName='Helvetica',fontSize=8.5,leading=11)
bd=ParagraphStyle('b',fontName='Helvetica-Bold',fontSize=8.5,leading=11)
it=ParagraphStyle('i',fontName='Helvetica-Oblique',fontSize=8,leading=10.5,textColor=colors.HexColor('#33435F'))
def P(t,s=st): return Paragraph(t,s)
W=[55*mm,125*mm]
def block(rows,head=None):
    data=[]; style=[('GRID',(0,0),(-1,-1),0.5,B),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]
    if head: data.append([P(head,bd),'']); style+=[('SPAN',(0,0),(-1,0)),('BACKGROUND',(0,0),(-1,0),H)]
    for r in rows: data.append([P(c, bd if i==0 and not head else st) for i,c in enumerate(r)])
    if not head: style.append(('BACKGROUND',(0,0),(0,-1),H))
    t=Table(data,colWidths=W); t.setStyle(TableStyle(style)); return t
LOGO=ImageReader('prodimg/logo-linsoles-web.png')
def first(c,doc):
    iw,ih=LOGO.getSize(); h=32; w=h*iw/ih; c.drawImage(LOGO,A4[0]-15*mm-w,A4[1]-6-h,width=w,height=h,mask='auto')
def esc(s): return s.replace('≤','&lt;=').replace('≥','&gt;=') if False else s.replace('<','&lt;').replace('>','&gt;')
Q={
 'emmental':dict(n='QUESO EMMENTAL «LINSOLES» · BARRA 3 KG',d='Queso de pasta prensada cocida con ojos, para rallado, loncheado y gratinado.',p=[['Grasa (s/ extracto seco)','≥ 45 %'],['Humedad','≤ 40 %'],['Sal','0,6 – 1,2 %']],v='3–6 meses'),
 'cheddar':dict(n='QUESO CHEDDAR «LINSOLES» · BARRA 3 KG',d='Queso de pasta prensada coloreado con achiote, de color naranja. Para loncheado, rallado, salsas, hamburguesas y platos preparados.',p=[['Grasa (s/ extracto seco)','≥ 48 %'],['Humedad','≤ 39 %'],['Sal','1,4 – 2,0 %'],['Colorante','Achiote (E160b)']],v='6–9 meses'),
 'mozza':dict(n='QUESO MOZZARELLA «LINSOLES» · BARRA 3 KG',d='Queso de pasta hilada con buen fundido, para pizza, platos preparados y hostelería.',p=[['Grasa (s/ extracto seco)','15+ / 40+ / 45+ / 48+ (según tipo)'],['Humedad','≤ 52 %'],['Sal','1,0 – 1,8 %']],v='60–90 días',t='Refrigerada a 0–4 °C'),
 'edam':dict(n='QUESO EDAM «LINSOLES» · BARRA 3 KG',d='Queso semicurado de pasta prensada, para loncheado, rallado e ingrediente.',p=[['Grasa (s/ extracto seco)','30+ / 40+ (según tipo)'],['Humedad','≤ 46 %'],['Sal','1,5 – 2,2 %']],v='3–6 meses'),
 'gouda':dict(n='QUESO GOUDA «LINSOLES» · BARRA 3 KG',d='Queso de pasta prensada semicurado, para loncheado, rallado y venta al corte.',p=[['Grasa (s/ extracto seco)','≥ 48 %'],['Humedad','≤ 42 %'],['Sal','1,5 – 2,2 %']],v='3–6 meses'),
}
NAMES={'emmental':'Emmental','cheddar':'Cheddar','mozza':'Mozzarella','edam':'Edam','gouda':'Gouda'}
for k,q in Q.items():
    els=[block([['PRODUCTO',q['n']]]),Spacer(1,8),
     block([['DENOMINACIÓN',q['d']],['PRESENTACIÓN','Barra de 3 kg aprox.']]),Spacer(1,8),
     block([[a,esc(b)] for a,b in q['p']],head='CARACTERÍSTICAS FÍSICO-QUÍMICAS'),Spacer(1,8),
     block([['CONSERVACIÓN',q.get('t','Refrigerado a 2–8 °C')],['VIDA ÚTIL',q['v']]]),Spacer(1,8),
     block([['ALÉRGENOS','Contiene <b>leche</b> y productos derivados de la leche (incluida la lactosa).']]),Spacer(1,10),
     P('Datos orientativos. Nos adaptamos a la ficha técnica del cliente.',it)]
    fn=f'barras/Ficha_Linsoles_Queso_{NAMES[k]}_Barra_3kg.pdf'
    SimpleDocTemplate(fn,pagesize=A4,leftMargin=15*mm,rightMargin=15*mm,topMargin=15*mm,bottomMargin=12*mm,title=f'Ficha técnica · Queso {NAMES[k]} Linsoles barra 3 kg').build(els,onFirstPage=first)
    print(fn)
