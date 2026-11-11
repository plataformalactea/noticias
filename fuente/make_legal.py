import re, json, glob
P='web/project/'
tpl=open(P+'Sobre-nosotros.dc.html',encoding='utf-8').read()
head=tpl[:tpl.index('<section>')]
foot=tpl[tpl.index('<footer'):]
head=head.replace('<a href="Sobre-nosotros.dc.html" class="nav" style="color: #2B4F9C">Sobre nosotros</a>','<a href="Sobre-nosotros.dc.html" class="nav">Sobre nosotros</a>')
EMP='Plataforma Interprofesional Láctea, S.L.U.'
DATOS=[('Titular',EMP),('NIF','B10766202'),('VAT intracomunitario','ESB10766202'),('Domicilio','Rosales, 18 · 50008 Zaragoza (España)'),
 ('Teléfono','+34 625 77 97 90'),('Correo electrónico','comercial@plataformalactea.com'),('Registro Mercantil','Registro Mercantil de Zaragoza · [Tomo, Folio, Hoja Z-____]'),
 ('Registro sanitario (RGSEAA)','40.087876/Z'),('Sitio web','www.plataformalactea.com')]
def table(rows):
    return '<div style="background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 16px; padding: 8px 24px">'+''.join(
      f'<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px 16px; padding: 12px 0;{" border-bottom: 1px solid #E0E7F2;" if i<len(rows)-1 else ""}"><span style="color: #4D5D78">{k}</span><span style="font-weight: 700; text-align: right">{v}</span></div>'
      for i,(k,v) in enumerate(rows))+'</div>'
def h2(t): return f'<h2 style="margin: 16px 0 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 24px; color: #0E2A4F">{t}</h2>'
def p(t): return f'<p style="margin: 0; font-size: 16px; line-height: 1.7; color: #33435F">{t}</p>'
def ul(items): return '<ul style="margin: 0; padding-left: 22px; display: flex; flex-direction: column; gap: 6px; font-size: 16px; line-height: 1.6; color: #33435F">'+''.join(f'<li>{i}</li>' for i in items)+'</ul>'
def page(title,kicker,updated,body,others):
    nav=' · '.join(f'<a href="{f}">{t}</a>' for f,t in others)
    return (head+f'''<section>
<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px 88px; display: flex; flex-direction: column; gap: 16px">
<span style="font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2B4F9C">{kicker}</span>
<h1 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 42px; line-height: 1.1">{title}</h1>
<p style="margin: 0; font-size: 14px; color: #4D5D78">Última actualización: {updated} · Ver también: {nav}</p>
{body}
</div>
</section>

'''+foot)
U='[fecha de publicación]'
# ---------- AVISO LEGAL
aviso=''.join([
 h2('1. Datos identificativos'),
 p('En cumplimiento del artículo 10 de la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:'),
 table(DATOS),
 h2('2. Objeto'),
 p('Este sitio web tiene como finalidad presentar la actividad de '+EMP+' como operador de comercio B2B de leche y productos lácteos, informar sobre los productos que comercializa, incluidos los de la marca Linsoles, y facilitar el contacto con clientes y proveedores profesionales.'),
 p('El acceso y uso del sitio atribuye la condición de usuario e implica la aceptación de este aviso legal. Si no está de acuerdo con él, le rogamos que no utilice el sitio.'),
 h2('3. Información sobre productos y precios'),
 p('Las fichas técnicas publicadas son orientativas y no constituyen una oferta vinculante. Los productos pueden adaptarse a las especificaciones de cada cliente. Las cotizaciones y precios de mercado que se muestran en el blog tienen carácter meramente informativo. Cualquier operación comercial se regirá por la oferta y las condiciones acordadas por escrito con cada cliente.'),
 h2('4. Propiedad intelectual e industrial'),
 p('Los textos, diseños, imágenes, logotipos y marcas de este sitio, incluidas las marcas P.I.L. y Linsoles, son titularidad de '+EMP+', de Linsoles Foods, S.L.U. o de terceros que han autorizado su uso. Queda prohibida su reproducción, distribución, comunicación pública o transformación sin autorización expresa, salvo para uso personal y privado.'),
 h2('5. Responsabilidad'),
 p('El titular procura que la información del sitio sea exacta y esté actualizada, pero no garantiza la ausencia de errores ni la disponibilidad ininterrumpida del sitio. No se hace responsable de los daños que pudieran derivarse del uso de la información publicada ni de los contenidos de sitios de terceros enlazados desde esta web.'),
 h2('6. Enlaces'),
 p('Los enlaces a sitios de terceros se ofrecen solo como referencia. El titular no controla ni asume responsabilidad sobre su contenido. Para establecer un enlace a este sitio no es necesaria autorización, siempre que no se presente de forma engañosa ni se atribuya al titular un respaldo que no existe.'),
 h2('7. Protección de datos y cookies'),
 p('El tratamiento de los datos personales que nos facilite se rige por nuestra <a href="Privacidad.dc.html">Política de privacidad</a>. El uso de cookies se explica en la <a href="Cookies.dc.html">Política de cookies</a>.'),
 h2('8. Legislación aplicable y jurisdicción'),
 p('Este aviso legal se rige por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales de Zaragoza, salvo que la normativa aplicable establezca otro fuero.'),
])
# ---------- PRIVACIDAD
priv=''.join([
 p('En '+EMP+' tratamos los datos personales conforme al Reglamento (UE) 2016/679 (RGPD) y a la Ley Orgánica 3/2018 de Protección de Datos Personales y garantía de los derechos digitales (LOPDGDD). A continuación le explicamos cómo lo hacemos.'),
 h2('1. Responsable del tratamiento'),
 table([('Responsable',EMP),('NIF','B10766202'),('Domicilio','Rosales, 18 · 50008 Zaragoza (España)'),('Teléfono','+34 625 77 97 90'),('Correo electrónico','comercial@plataformalactea.com')]),
 h2('2. Qué datos tratamos'),
 ul(['Datos de contacto que nos facilita en el formulario o por correo: nombre y apellidos, empresa, cargo, correo electrónico, teléfono y país.',
     'Información sobre su consulta: producto de interés, volúmenes, especificaciones y el contenido de su mensaje.',
     'Datos de clientes y proveedores necesarios para la relación comercial: datos de facturación, entrega y contacto de las personas de su organización.']),
 p('No solicitamos categorías especiales de datos. Le pedimos que no nos los envíe.'),
 h2('3. Para qué y con qué base legal'),
 ul(['<strong>Atender su solicitud de contacto o de oferta.</strong> Base: su consentimiento y la aplicación de medidas precontractuales a petición suya (art. 6.1.a y 6.1.b RGPD).',
     '<strong>Gestionar la relación comercial</strong> con clientes y proveedores: pedidos, entregas, facturación y cobros. Base: ejecución del contrato y cumplimiento de obligaciones legales, fiscales y contables (art. 6.1.b y 6.1.c RGPD).',
     '<strong>Enviar información comercial</strong> sobre nuestros productos y el mercado lácteo a clientes y contactos profesionales. Base: interés legítimo en el caso de clientes (art. 21.2 LSSI-CE) y consentimiento en los demás casos. Puede oponerse en cualquier momento.']),
 h2('4. Cuánto tiempo conservamos los datos'),
 p('Los datos de las solicitudes de contacto se conservan mientras se atiende la consulta y, si no se inicia una relación comercial, durante un máximo de dos años. Los datos de clientes y proveedores se conservan mientras dure la relación y, después, durante los plazos de prescripción legales (con carácter general, seis años a efectos mercantiles y los plazos previstos en la normativa tributaria).'),
 h2('5. A quién comunicamos los datos'),
 p('No cedemos sus datos a terceros, salvo obligación legal (por ejemplo, a la Agencia Tributaria o a las autoridades competentes) o cuando sea necesario para ejecutar una operación que usted haya solicitado, como su comunicación a transportistas, aseguradoras de crédito o entidades bancarias.'),
 p('Contamos con proveedores que tratan datos por nuestra cuenta (alojamiento web, correo electrónico, gestoría o servicios informáticos), con los que hemos firmado los correspondientes contratos de encargo del tratamiento.'),
 h2('6. Transferencias internacionales'),
 p('Por la naturaleza internacional de nuestra actividad, puede ser necesario comunicar datos de contacto a clientes, proveedores o transportistas situados fuera del Espacio Económico Europeo para ejecutar una operación solicitada por usted. En esos casos la transferencia se ampara en el art. 49.1.b) y c) RGPD o en las garantías adecuadas que correspondan.'),
 h2('7. Sus derechos'),
 p('Puede ejercer los derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, así como retirar su consentimiento en cualquier momento, escribiendo a <a href="mailto:comercial@plataformalactea.com">comercial@plataformalactea.com</a> o por correo postal a nuestro domicilio, indicando el derecho que ejercita y acreditando su identidad.'),
 p('Si considera que no hemos atendido correctamente su solicitud, puede presentar una reclamación ante la Agencia Española de Protección de Datos (www.aepd.es).'),
 h2('8. Seguridad'),
 p('Aplicamos medidas técnicas y organizativas adecuadas para proteger sus datos frente a pérdida, acceso no autorizado o alteración, teniendo en cuenta el estado de la técnica y los riesgos del tratamiento.'),
 h2('9. Cambios en esta política'),
 p('Podemos actualizar esta política para adaptarla a cambios normativos o en nuestra actividad. La versión vigente es siempre la publicada en esta página.'),
])
# ---------- COOKIES
ck=[('Cookie técnica del aviso de cookies','Propia','Recordar si ha aceptado o rechazado las cookies','1 año'),
    ('[Nombre de la cookie de analítica, si se instala]','Tercero','Medir de forma agregada las visitas al sitio','[Duración]')]
cktable='<div style="overflow-x: auto; background: #FFFFFF; border: 1px solid #D3DCEA; border-radius: 16px"><table style="width: 100%; border-collapse: collapse; font-size: 15px; min-width: 560px"><thead><tr>'+''.join(f'<th style="text-align: left; padding: 12px 16px; background: #E6EDF8; color: #0E2A4F">{h}</th>' for h in ['Cookie','Titular','Finalidad','Duración'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td style="padding: 12px 16px; border-top: 1px solid #E0E7F2; color: #33435F">{c}</td>' for c in r)+'</tr>' for r in ck)+'</tbody></table></div>'
cook=''.join([
 h2('1. Qué son las cookies'),
 p('Las cookies son pequeños archivos que un sitio web guarda en su navegador para recordar información sobre su visita. Algunas son necesarias para que la web funcione y otras sirven, por ejemplo, para analizar cómo se usa.'),
 h2('2. Qué cookies utiliza este sitio'),
 p('Este sitio utiliza únicamente las cookies técnicas imprescindibles para su funcionamiento y para recordar sus preferencias sobre cookies. Estas cookies no requieren su consentimiento.'),
 p('Solo si en el futuro se instalan herramientas de analítica u otras cookies no necesarias, se le pedirá previamente su consentimiento mediante el aviso de cookies, en el que podrá aceptarlas, rechazarlas o configurarlas con la misma facilidad. La tabla siguiente se actualizará en ese caso.'),
 cktable,
 h2('3. Cómo gestionar o retirar el consentimiento'),
 p('Puede cambiar su elección en cualquier momento desde el enlace «Configurar cookies» del pie de página, o eliminar las cookies desde la configuración de su navegador (Chrome, Firefox, Safari, Edge u otros). Si bloquea las cookies técnicas, es posible que algunas partes del sitio no funcionen correctamente.'),
 h2('4. Más información'),
 p('Para cualquier duda sobre el uso de cookies o sobre el tratamiento de sus datos, consulte nuestra <a href="Privacidad.dc.html">Política de privacidad</a> o escríbanos a <a href="mailto:comercial@plataformalactea.com">comercial@plataformalactea.com</a>.'),
])
pages={'AvisoLegal.dc.html':page('Aviso legal','Información legal',U,aviso,[('Privacidad.dc.html','Política de privacidad'),('Cookies.dc.html','Política de cookies')]),
       'Privacidad.dc.html':page('Política de privacidad','Protección de datos',U,priv,[('AvisoLegal.dc.html','Aviso legal'),('Cookies.dc.html','Política de cookies')]),
       'Cookies.dc.html':page('Política de cookies','Cookies',U,cook,[('AvisoLegal.dc.html','Aviso legal'),('Privacidad.dc.html','Política de privacidad')])}
for fn,html in pages.items():
    html=re.sub(r'<title>[^<]*</title>','<title>'+{'AvisoLegal.dc.html':'Aviso legal','Privacidad.dc.html':'Política de privacidad','Cookies.dc.html':'Política de cookies'}[fn]+' · Plataforma Láctea</title>',html,1)
    html=re.sub(r'"\$preview":\{"width":1440,"height":\d+\}','"$preview":{"width":1440,"height":2600}',html)
    open(P+fn,'w',encoding='utf-8').write(html)
# footer links everywhere
for f in glob.glob(P+'*.dc.html'):
    s=open(f,encoding='utf-8').read()
    s=s.replace('<a href="#">Aviso legal</a>','<a href="AvisoLegal.dc.html">Aviso legal</a>').replace('<a href="#">Política de privacidad</a>','<a href="Privacidad.dc.html">Política de privacidad</a>').replace('<a href="#">Política de cookies</a>','<a href="Cookies.dc.html">Política de cookies</a>')
    s=s.replace('Más información en la Política de privacidad.','Más información en la <a href="Privacidad.dc.html">Política de privacidad</a>.')
    s=s.replace('He leído la política de privacidad','He leído la <a href="Privacidad.dc.html">política de privacidad</a>')
    open(f,'w',encoding='utf-8').write(s)
# canvas
c=json.load(open(P+'canvas.json'))
for i,(fn,t) in enumerate([('AvisoLegal.dc.html','Aviso legal'),('Privacidad.dc.html','Política de privacidad'),('Cookies.dc.html','Política de cookies')]):
    c['boards'][fn]={'x':9120+i*1520,'y':0,'w':1440,'h':2600,'title':t,'expand':'fill'}
    if fn not in c['order']: c['order'].append(fn)
json.dump(c,open(P+'canvas.json','w'),ensure_ascii=False,separators=(',',':'))
print('ok')
