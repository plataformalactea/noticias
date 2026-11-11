import re, os, shutil
SRC='web/project'; OUT='Web_Plataforma_Lactea'
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT+'/img'); os.makedirs(OUT+'/fichas'); os.makedirs(OUT+'/catalogos')
A='/mnt/user-data/attachments/fd2192db-e962-524a-b2a2-31b0b87be078/'
assets={
 '/_blob/41cb0ccdb1020ad91485d43803b21dd9':('logos/pil_logo.png','img/logo-pil.png'),
 '/_blob/304aaad57aec0ac715b2d74a17462b25':(A+'9b972984-image.png','img/logo-linsoles.png'),
 '/_blob/50bad75a0df21ee10fe21e4b79cc972c':('bricks/brick_entera.png','img/brick-entera.png'),
 '/_blob/f455714c58a376d11b9e2a5773a1190c':('bricks/brick_semi.png','img/brick-semidesnatada.png'),
 '/_blob/a807677f36d03b4924f527bb8f5fca21':('bricks/brick_desnatada.png','img/brick-desnatada.png'),
 '/_blob/adcb70b8929a49f68fcfe2e2f30f27c1':('bricks/Ficha_Linsoles_Leche_Entera_UHT_1L.pdf','fichas/Ficha_Linsoles_Leche_Entera_UHT_1L.pdf'),
 '/_blob/0d70266a4b530678b9e8739de61ecccc':('bricks/Ficha_Linsoles_Leche_Semidesnatada_UHT_1L.pdf','fichas/Ficha_Linsoles_Leche_Semidesnatada_UHT_1L.pdf'),
 '/_blob/40669a7edc7a7f3267d7367609912960':('bricks/Ficha_Linsoles_Leche_Desnatada_UHT_1L.pdf','fichas/Ficha_Linsoles_Leche_Desnatada_UHT_1L.pdf'),
}

P='prodimg/';W='webactual/'
for bid,src in {'de78b5c415d7af6dff408530cd1a20c5':P+'bidon-amf.png','6ccdac757cecbc26dea3a6addc60cf81':P+'mantequilla.png',
 '10fab5087967c240497f937871816948':P+'queso-cagliata.png','c6a1f323db558a636943240e61b5a814':P+'queso-edam.png','7b9b4bfb148307f54a3f5c42ffeac220':P+'queso-emmental.png',
 'dbbcab658fcaa5f1cbc2a5a350a17757':P+'queso-gouda.png','e789e19cd668179f3f6b7651230a098f':P+'queso-mozza.png','171f96e8a6de3e29e78fd79b20fcee21':P+'saco-cas-a.png',
 'd028a39f41a370456e3fc195ad7def2b':P+'saco-cas-r.png','9044ddfce9c6ed91d9e8b7166f5f7663':P+'saco-casna.png','27daea58f50dbc4540ba813b45cbf3fe':P+'saco-ffmp.png',
 '17c711b5da9d14c18d8a3987fae3ccd8':P+'saco-mcc.png','34f7e4d95bc1e07fcef9a51f8e3a0be3':P+'saco-perm.png','e46aa2839f3f195604682442c4e86eca':P+'saco-smp.png',
 '27332238bb26b560b4e0b86a954f12b3':P+'saco-smpsl.png','e7dc531667399a4dff03a49a638ea0c6':P+'saco-swp.png','abf4a94eda20bf18ca5bd4dea6dcc3a9':P+'saco-wmp.png',
 'f6f685b070e129f0fc868c3158768664':P+'saco-wpc35.png','66bae784272fee6383ac2e9f75ec13f1':P+'saco-wpc80.png','80f4ba562fc59ad095077583fb00a5e3':P+'saco-wpi.png',
 'f8ba60daed43990dcf036810a05b551c':W+'banner01_pil.jpg','18d78e5f328f0344d22f7db15cd74b7d':W+'banner02_truck.jpg','15afa298573db7ed175291e0cffd5ce0':W+'banner03_lin.jpg','03cd3936624e1c04216961cd0cc48f33':W+'banner04_pil.jpg'}.items():
    assets['/_blob/'+bid]=(src,'img/'+src.split('/')[-1])
assets['/_blob/e8ef806e56623c82126dd7d7908d5390']=('queso/queso-oveja-linsoles-entero.jpg','img/queso-oveja-linsoles.jpg')
assets['/_blob/c81327f48f1b96f78305b96a837a53d3']=('queso/queso-oveja-marca-blanca-v2.jpg','img/queso-oveja-marca-blanca.jpg')
assets['/_blob/9c842fd576f7289ebc7140aa4bae456d']=('queso/Ficha_Linsoles_Queso_Oveja_Anejo_3kg.pdf','fichas/Ficha_Linsoles_Queso_Oveja_Anejo_3kg.pdf')
assets['/_blob/e88702285801938dcb87b40379ad8f7a']=('queso/queso-entero-recorte.png','img/queso-oveja-entero.png')
assets['/_blob/817cc1692f3f460a257c5125ab252060']=('semi/queso-semicurado-linsoles.jpg','img/queso-semicurado-linsoles.jpg')
assets['/_blob/a3b3813999ee637a3da25146cb5e30e8']=('semi/queso-semicurado-marca-blanca.jpg','img/queso-semicurado-marca-blanca.jpg')
assets['/_blob/270ad03247a15fd4cdefc2d898f86c04']=('semi/semi-entero-recorte.png','img/queso-semicurado-entero.png')
assets['/_blob/6e1c15e8d585f78057410ca2065a11dc']=('semi/Ficha_Linsoles_Queso_Semicurado_Mezcla.pdf','fichas/Ficha_Linsoles_Queso_Semicurado_Mezcla.pdf')
assets['/_blob/2687bfcdb5a7aa36dfc07d55827d796e']=('barras/barra-emmental.jpg','img/barra-emmental.jpg')
assets['/_blob/8fc4c02e72ab669d9b3ff32e80d3368d']=('barras/Ficha_Linsoles_Queso_Emmental_Barra_3kg.pdf','fichas/Ficha_Linsoles_Queso_Emmental_Barra_3kg.pdf')
assets['/_blob/19e2dba64085181239be728452492f2e']=('barras/barra-cheddar.jpg','img/barra-cheddar.jpg')
assets['/_blob/c84d982e3bf9c36c98b6ab05d5932612']=('barras/Ficha_Linsoles_Queso_Cheddar_Barra_3kg.pdf','fichas/Ficha_Linsoles_Queso_Cheddar_Barra_3kg.pdf')
assets['/_blob/4ad68c2b3bd0ca2a39a35def99e22c2f']=('barras/barra-mozza.jpg','img/barra-mozza.jpg')
assets['/_blob/3699cc7e106cd6f65364e06925455599']=('barras/Ficha_Linsoles_Queso_Mozzarella_Barra_3kg.pdf','fichas/Ficha_Linsoles_Queso_Mozzarella_Barra_3kg.pdf')
assets['/_blob/1537994942e86f3d818f0e6a7b9c7971']=('barras/barra-edam.jpg','img/barra-edam.jpg')
assets['/_blob/f5617a81b1a3b37877ffb3fb169b52fb']=('barras/Ficha_Linsoles_Queso_Edam_Barra_3kg.pdf','fichas/Ficha_Linsoles_Queso_Edam_Barra_3kg.pdf')
assets['/_blob/f907181a5b371fc3b2d2648fad9ab71a']=('barras/barra-gouda.jpg','img/barra-gouda.jpg')
assets['/_blob/71c52d8bc9efd1d2c4bc8661f113855f']=('barras/Ficha_Linsoles_Queso_Gouda_Barra_3kg.pdf','fichas/Ficha_Linsoles_Queso_Gouda_Barra_3kg.pdf')
assets['/_blob/d5f70c87f79d053aaa40c5aaa70ad5a0']=('barras/barra-emmental-recorte.png','img/barra-emmental-recorte.png')
assets['/_blob/2906c931645fdc2ace8f36a457f8dca8']=('barras/barra-cheddar-recorte.png','img/barra-cheddar-recorte.png')
assets['/_blob/f9d19e9a38b2da0fcef229d441d103c9']=('barras/barra-mozza-recorte.png','img/barra-mozza-recorte.png')
assets['/_blob/32f1bb60df44083b472df51f1a5550e5']=('barras/barra-edam-recorte.png','img/barra-edam-recorte.png')
assets['/_blob/35eb1f2685514b45eec8c5a32af87929']=('barras/barra-gouda-recorte.png','img/barra-gouda-recorte.png')
assets['/_blob/9dbaf90ef49cc27f167a1d8eabc63f25']=('catalogos/cat-industrial-1.jpg','img/catalogo-industrial-1.jpg')
assets['/_blob/c9429ec6cbee14adaea115a0ed34c54e']=('catalogos/cat-industrial-2.jpg','img/catalogo-industrial-2.jpg')
assets['/_blob/a8d084b23c3c80bc86183c2d99ae0aa3']=('catalogos/cat-industrial-3.jpg','img/catalogo-industrial-3.jpg')
assets['/_blob/dcfc1d038ac2001136d9ca50c6723214']=('catalogos/cat-industrial-4.jpg','img/catalogo-industrial-4.jpg')
assets['/_blob/9e08f6e8a39a3f63e2142aa331ed9829']=('catalogos/cat-industrial-5.jpg','img/catalogo-industrial-5.jpg')
assets['/_blob/d37386050ecb6d210dde19f085278c64']=('catalogos/cat-industrial-6.jpg','img/catalogo-industrial-6.jpg')
assets['/_blob/35a74227fa46122c00534d74249a5300']=('catalogos/cat-industrial-7.jpg','img/catalogo-industrial-7.jpg')
assets['/_blob/cda6270a5ca68c76d8c28b58e81fc9a0']=('catalogos/cat-retail-1.jpg','img/catalogo-retail-1.jpg')
assets['/_blob/b3645ab9b08d6641f341cbdb2dd37d76']=('catalogos/cat-retail-2.jpg','img/catalogo-retail-2.jpg')
assets['/_blob/81eb5799f042dc15eb67de785d8f0d12']=('catalogos/cat-retail-3.jpg','img/catalogo-retail-3.jpg')
assets['/_blob/4422940662207c67deb4d7ba414612bc']=('catalogos/cat-retail-4.jpg','img/catalogo-retail-4.jpg')
assets['/_blob/f27038ba815803a11a7def6e09fc9bcb']=('catalogos/Catalogo_Linsoles_Lacteos_Industriales.pdf','catalogos/Catalogo_Linsoles_Lacteos_Industriales.pdf')
assets['/_blob/6f9b51182fe0b9a576ea6d92cce1f0bd']=('catalogos/Catalogo_Linsoles_Retail_Horeca.pdf','catalogos/Catalogo_Linsoles_Retail_Horeca.pdf')
assets['/_blob/08dbbb186ba4e57c9e401dbf96ce0693']=('prodimg/sacoL-cas-a.png','img/saco-cas-a.png')
assets['/_blob/a9465e2c9a84be4416a06b221f4f96c5']=('prodimg/sacoL-cas-r.png','img/saco-cas-r.png')
assets['/_blob/0fca985555e56d923509ed4fb1cf49a8']=('prodimg/sacoL-casna.png','img/saco-casna.png')
assets['/_blob/5120ea45d551aeda046e8f8cc8d8f741']=('prodimg/sacoL-ffmp.png','img/saco-ffmp.png')
assets['/_blob/f33f02d4f082ea6d8112e0dd047a9521']=('prodimg/sacoL-mcc.png','img/saco-mcc.png')
assets['/_blob/32962cec2d5158e02436f19752a2ce47']=('prodimg/sacoL-perm.png','img/saco-perm.png')
assets['/_blob/215e654f55569d8ef799a62439b13c07']=('prodimg/sacoL-smp.png','img/saco-smp.png')
assets['/_blob/ffbcf8a81eab09be7a61a714f21b4cfd']=('prodimg/sacoL-smpsl.png','img/saco-smpsl.png')
assets['/_blob/1787cdc1aae801d0a9821146a992240d']=('prodimg/sacoL-swp.png','img/saco-swp.png')
assets['/_blob/405e17d50cd7336ef0ee95082a4a7f15']=('prodimg/sacoL-wmp.png','img/saco-wmp.png')
assets['/_blob/1f6b56e7d9ccba9d0aa393bc7d4167cb']=('prodimg/sacoL-ssmp.png','img/saco-ssmp.png')
assets['/_blob/b64567b750b50489c9544268a3b560f9']=('prodimg/sacoL-wpc35.png','img/saco-wpc35.png')
assets['/_blob/e3461e7d858cabc1c3f17dbb502d6ff0']=('prodimg/sacoL-wpc80.png','img/saco-wpc80.png')
assets['/_blob/86422bba257245c36d7ef9214db4a63d']=('prodimg/sacoL-wpi.png','img/saco-wpi.png')
assets['/_blob/0f81c2682c8bed66efbb2f67cc267e23']=('prodimg/camion-linsoles.jpg','img/camion-linsoles.jpg')
assets['/_blob/fd89e34cfc64824404526e88628fd825']=('prodimg/quesoF-cagliata.png','img/queso-cagliata.png')
assets['/_blob/6f6a0e818cf794b0b617e777d5d03885']=('prodimg/quesoF-mozza.png','img/queso-mozza.png')
assets['/_blob/36883d43ccdaa00893930734f72d6f11']=('prodimg/quesoF-edam.png','img/queso-edam.png')
assets['/_blob/199558c1ea9bd27b06d85cb8f056f066']=('prodimg/quesoF-gouda.png','img/queso-gouda.png')
assets['/_blob/745b38f07ed3edce2c5241a40a2f57a7']=('prodimg/quesoF-emmental.png','img/queso-emmental.png')
assets['/_blob/99b7c14e9bab4bff4da22bdfb0c6150f']=('prodimg/quesoF-cheddar.png','img/queso-cheddar.png')
assets['/_blob/dc3677d394015360a65800dae235177d']=('prodimg/mapamundi.svg','img/mapamundi.svg')
assets['/_blob/df2e9333eb926275044fe279380590c5']=('prodimg/planta-linsoles.jpg','img/planta-linsoles.jpg')
assets['/_blob/c113f47800f3fef94d990a9cd1afccee']=('prodimg/logo-pil-web.png','img/logo-pil.png')
assets['/_blob/e43a8dc2e9a31839d6858380121246c9']=('prodimg/logo-linsoles-web.png','img/logo-linsoles.png')
for k,(s,d) in assets.items(): shutil.copy(s,OUT+'/'+d)
NAMES={'Main':'index','Industriales':'industriales','Retail-Horeca':'retail-horeca','Blog':'blog','Sobre-nosotros':'sobre-nosotros','Solicitud':'solicitud','AvisoLegal':'aviso-legal','Privacidad':'privacidad','Cookies':'cookies','Catalogos':'catalogos','Mision':'mision'}

def convert(name, body_fix=None, extra_js=''):
    s=open(f'{SRC}/{name}.dc.html',encoding='utf-8').read()
    title=re.search(r'<title>(.*?)</title>',s).group(1)
    helmet=re.search(r'<helmet>(.*?)</helmet>',s,re.S).group(1)
    body=re.search(r'<x-dc>(.*?)</x-dc>',s,re.S).group(1)
    body=re.sub(r'<helmet>.*?</helmet>','',body,flags=re.S)
    if body_fix: body=body_fix(body,s)
    html=f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{helmet.strip()}
</head>
<body>
{body.strip()}
{extra_js}
</body>
</html>
'''
    for k,(_,d) in assets.items(): html=html.replace(k,d)
    for n,o in NAMES.items(): html=html.replace(f'href="{n}.dc.html"',f'href="{o}.html"')
    assert '{{' not in html and 'sc-for' not in html and 'sc-if' not in html and '.dc.html' not in html and '/_blob/' not in html, name
    open(f'{OUT}/{NAMES[name]}.html','w',encoding='utf-8').write(html)

for n in ['Main','Retail-Horeca','Sobre-nosotros','AvisoLegal','Privacidad','Cookies','Catalogos','Mision']: convert(n)
convert('Blog', extra_js=open('deploy/blog_filter.html',encoding='utf-8').read() if os.path.exists('deploy/blog_filter.html') else '')

# --- Solicitud: form -> thank you
def fix_sol(b,s):
    b=b.replace('<sc-if value="{{showForm}}" hint-placeholder-val="{{true}}">','<div id="form-wrap">',1)
    b=b.replace('<sc-if value="{{sent}}" hint-placeholder-val="{{false}}">','<div id="sent-wrap" style="display: none">',1)
    b=b.replace('</sc-if>','</div>')
    b=b.replace('onClick="{{send}}"','onclick="pilSend()"').replace('onClick="{{reset}}"','onclick="pilReset()"')
    return b
convert('Solicitud',fix_sol,'''<script>
function pilSend(){document.getElementById('form-wrap').style.display='none';document.getElementById('sent-wrap').style.display='block';}
function pilReset(){document.getElementById('sent-wrap').style.display='none';document.getElementById('form-wrap').style.display='block';}
</script>''')

# --- Industriales: list + ficha rendered with plain JS
src=open(f'{SRC}/Industriales.dc.html',encoding='utf-8').read()
script=re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>',src,re.S).group(1)
data=script[script.index('var CATS'):script.index('function rowStyle')]
def fix_ind(b,s):
    a=b.index('<section>\n<div style="max-width: 1240px; margin: 0 auto; padding: 32px 24px 0;')
    z=b.index('<footer')
    return b[:a]+'''<section>
<div id="chips" style="max-width: 1240px; margin: 0 auto; padding: 32px 24px 0; display: flex; flex-wrap: wrap; gap: 8px"></div>
</section>
<section>
<div style="max-width: 1240px; margin: 0 auto; padding: 24px 24px 80px; display: flex; flex-wrap: wrap; gap: 28px; align-items: flex-start">
<div id="lista" style="flex: 1 1 320px; min-width: 0; background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 18px"></div>
<article id="ficha" style="flex: 999 1 560px; min-width: 0; background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 20px; overflow: hidden"></article>
</div>
</section>

'''+b[z:]
js='<script>\n'+data+r'''
var state={cat:'all',sel:'smp'};
function rowStyle(i){return 'display: flex; justify-content: space-between; gap: 16px; padding: 12px 16px; font-size: 15px; background: '+(i%2?'#FFFFFF':'#F4F7FB');}
function rows(list){return list.map(function(r,i){return '<div style="'+rowStyle(i)+'"><span style="color: #4D5D78">'+r[0]+'</span><span style="font-weight: 700; text-align: right">'+r[1]+'</span></div>';}).join('');}
var H3='margin: 0; font-size: 14px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #2B4F9C';
var BOX='background: #F4F7FB; border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 6px';
var LBL='font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #4D5D78';
function render(){
  var all=[{id:'all',label:'Todos'}].concat(CATS);
  document.getElementById('chips').innerHTML=all.map(function(c){var on=c.id===state.cat;
    return '<button type="button" class="chip" data-cat="'+c.id+'" style="'+(on?'border: 1.5px solid #0E2A4F; background: #0E2A4F; color: #FFFFFF':'border: 1.5px solid #D3DCEA; background: #FFFFFF; color: #0E2A4F')+'">'+c.label+'</button>';}).join('');
  document.getElementById('lista').innerHTML=CATS.filter(function(c){return state.cat==='all'||c.id===state.cat;}).map(function(c){
    return '<div style="display: flex; flex-direction: column; gap: 4px"><span style="align-self: flex-start; margin: 2px 0 6px; font-size: 13px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; color: #FFFFFF; background: #0E2A4F; border-radius: 999px; padding: 7px 18px; box-shadow: 0 2px 6px rgba(14,42,79,.18)">'+c.label+'</span>'+
      PRODUCTS.filter(function(p){return p.cat===c.id;}).map(function(p){var on=p.id===state.sel;
        return '<button type="button" class="item" data-sel="'+p.id+'" style="'+(on?'border: none; background: #2B4F9C; color: #FFFFFF; font-weight: 700':'border: none; background: transparent; color: #0E2A4F; font-weight: 600')+'"><span>'+p.name+'</span><span style="font-size: 12px; opacity: 0.8">'+p.short+'</span></button>';}).join('')+'</div>';}).join('');
  var p=PRODUCTS.filter(function(x){return x.id===state.sel;})[0]||PRODUCTS[0];
  var ref='PIL-'+('00'+(PRODUCTS.indexOf(p)+1)).slice(-3);
  var catLabel=CATS.filter(function(c){return c.id===p.cat;})[0].label;
  document.getElementById('ficha').innerHTML=
   '<div style="background: #0E2A4F; color: #FFFFFF; padding: 32px 36px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; align-items: flex-start"><div style="display: flex; flex-direction: column; gap: 8px"><span style="font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #E8B84A">Ficha técnica orientativa · '+ref+'</span><h2 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 34px; line-height: 1.1">'+p.name+'</h2><span style="color: #CBD8EE; font-size: 15px">'+p.alt+'</span></div><span style="background: rgba(255,255,255,.1); border-radius: 999px; padding: 8px 14px; font-size: 13px; font-weight: 700">'+catLabel+'</span></div>'+
   '<div style="padding: 32px 36px; display: flex; flex-direction: column; gap: 28px">'+
   (p.cat==='liq'||p.cat==='queso' ? '<div style="display: flex; flex-direction: column; gap: 20px"><img src="'+(IMG[p.id]||TANK)+'" alt="'+p.name+'" style="'+(p.cat==='liq'?'width: 100%; height: 320px; object-fit: cover; object-position: 40% 30%; border-radius: 16px; display: block':'width: 100%; height: 280px; object-fit: contain; background: #F4F7FB; border-radius: 16px; display: block; padding: 20px; box-sizing: border-box')+'"><p style="margin: 0; font-size: 17px; line-height: 1.6; color: #33435F">'+p.desc+'</p></div>' :
   '<div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: center"><div style="flex: 0 0 220px; height: 220px; background: #F4F7FB; border-radius: 16px; display: flex; align-items: center; justify-content: center; padding: 14px; box-sizing: border-box"><img src="'+(IMG[p.id]||TANK)+'" alt="'+p.name+'" style="max-width: 100%; max-height: 100%; object-fit: contain"></div><p style="flex: 1 1 280px; margin: 0; font-size: 17px; line-height: 1.6; color: #33435F">'+p.desc+'</p></div>')+
   '<div style="display: flex; flex-direction: column; gap: 10px"><h3 style="'+H3+'">Parámetros fisicoquímicos</h3><div style="border: 1px solid #D3DCEA; border-radius: 12px; overflow: hidden">'+rows(p.params)+'</div></div>'+
   (p.micro?'<div style="display: flex; flex-direction: column; gap: 10px"><h3 style="'+H3+'">Parámetros microbiológicos</h3><div style="border: 1px solid #D3DCEA; border-radius: 12px; overflow: hidden">'+rows(MICRO)+'</div></div>':'')+
   '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px">'+
     '<div style="'+BOX+'"><span style="'+LBL+'">Presentación</span><span style="line-height: 1.45; font-weight: 600">'+p.pack+'</span></div>'+
     '<div style="'+BOX+'"><span style="'+LBL+'">Conservación</span><span style="line-height: 1.45; font-weight: 600">'+p.store+'</span></div>'+
     '<div style="'+BOX+'"><span style="'+LBL+'">Vida útil</span><span style="line-height: 1.45; font-weight: 600">'+p.life+'</span></div></div>'+
   '<div style="background: #DCE6F5; border-radius: 12px; padding: 18px 20px"><p style="margin: 0; line-height: 1.55; color: #33435F; font-size: 15px"><strong>Estos datos son orientativos.</strong> Nos adaptamos a la ficha técnica del cliente: envíenos sus especificaciones y le ofertamos el producto que las cumpla.</p></div>'+
   '<div style="display: flex; flex-wrap: wrap; gap: 12px"><a href="solicitud.html" class="cta">Solicitar este producto</a></div></div>';
}
document.addEventListener('click',function(e){
  var c=e.target.closest('[data-cat]'); if(c){state.cat=c.getAttribute('data-cat'); render(); return;}
  var s=e.target.closest('[data-sel]'); if(s){state.sel=s.getAttribute('data-sel'); render(); if(window.innerWidth<900) document.getElementById('ficha').scrollIntoView({behavior:'smooth'});}
});
render();
</script>'''
convert('Industriales',fix_ind,js)
print(sorted(os.listdir(OUT)))
