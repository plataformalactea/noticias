import re, sys, os, glob, shutil
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
D = B + 'Web_Plataforma_Lactea/'

FORM_JS = r'''<script>
(function(){
var f=document.getElementById('contact-form');if(!f)return;
var T={es:{sending:'Enviando…',send:'Enviar solicitud',err:'No hemos podido enviar su solicitud. Por favor, escríbanos a <a href="mailto:comercial@plataformalactea.com">comercial@plataformalactea.com</a> o llámenos al <a href="tel:+34625779790">+34 625 77 97 90</a>.',req:'Revise los campos obligatorios y acepte la política de privacidad.'},
fr:{sending:'Envoi…',send:'Envoyer la demande',err:'Nous n’avons pas pu envoyer votre demande. Écrivez-nous à <a href="mailto:comercial@plataformalactea.com">comercial@plataformalactea.com</a> ou appelez le <a href="tel:+34625779790">+34 625 77 97 90</a>.',req:'Vérifiez les champs obligatoires et acceptez la politique de confidentialité.'},
pt:{sending:'A enviar…',send:'Enviar pedido',err:'Não foi possível enviar o seu pedido. Escreva-nos para <a href="mailto:comercial@plataformalactea.com">comercial@plataformalactea.com</a> ou ligue para o <a href="tel:+34625779790">+34 625 77 97 90</a>.',req:'Reveja os campos obrigatórios e aceite a política de privacidade.'},
en:{sending:'Sending…',send:'Send request',err:'We could not send your request. Please email us at <a href="mailto:comercial@plataformalactea.com">comercial@plataformalactea.com</a> or call <a href="tel:+34625779790">+34 625 77 97 90</a>.',req:'Please check the required fields and accept the privacy policy.'}};
function L(){var l=(f.closest('[lang]')||document.documentElement).getAttribute('lang')||'es';return T[l]||T.es;}
var tf=f.querySelector('input[name=t]');tf.value=Math.floor(Date.now()/1000);
f.querySelector('input[name=idioma]').value=(f.closest('[lang]')||document.documentElement).getAttribute('lang')||'es';
var box=document.getElementById('form-error'),btn=f.querySelector('button[type=submit]');
var fw=document.getElementById('form-wrap'),sw=document.getElementById('sent-wrap');
function showErr(html){box.innerHTML=html;box.hidden=false;box.scrollIntoView({block:'center',behavior:'smooth'});}
function sent(){fw.style.display='none';sw.style.display='block';sw.scrollIntoView({block:'start'});}
if(location.hash==='#enviado'){sent();}else if(location.hash==='#error'){showErr(L().err);}
f.addEventListener('submit',function(e){
  e.preventDefault();box.hidden=true;
  if(!f.checkValidity()){f.reportValidity&&f.reportValidity();showErr(L().req);return;}
  btn.disabled=true;btn.textContent=L().sending;
  fetch(f.getAttribute('action'),{method:'POST',body:new FormData(f),headers:{'X-Requested-With':'fetch','Accept':'application/json'}})
   .then(function(r){return r.json().catch(function(){return {ok:false};});})
   .then(function(j){if(j&&j.ok){f.reset();tf.value=Math.floor(Date.now()/1000);sent();}else{showErr(L().err);}})
   .catch(function(){showErr(L().err);})
   .then(function(){btn.disabled=false;btn.textContent=L().send;});
});
var again=document.getElementById('send-again');if(again)again.addEventListener('click',function(){sw.style.display='none';fw.style.display='block';box.hidden=true;});
})();
</script>'''

def form_step():
    p = D + 'solicitud.html'
    h = open(p, encoding='utf-8').read()
    names = [('autocomplete="name">', 'nombre', 120, True), ('autocomplete="organization">', 'empresa', 160, True), ('autocomplete="email">', 'email', 160, True), ('autocomplete="tel">', 'telefono', 40, False)]
    for key, n, mx, req in names:
        assert h.count(key) == 1, key
        h = h.replace(key, f'autocomplete="{key.split(chr(34))[1]}" name="{n}" maxlength="{mx}"' + (' required' if req else '') + '>')
    sel = re.findall(r'<select class="inp"', h); assert len(sel) == 2
    _n = iter(['pais', 'tipo'])
    h = re.sub(r'<select class="inp"(?= |>)', lambda m: f'<select class="inp" name="{next(_n)}" required', h)
    h = re.sub(r'<option>([^<]+)</option>', lambda m: f'<option value="{m.group(1)}">{m.group(1)}</option>', h)
    h = h.replace('placeholder="p. ej. leche desnatada en polvo">', 'placeholder="p. ej. leche desnatada en polvo" name="producto" maxlength="200">')
    h = h.replace('placeholder="p. ej. 2 cisternas / mes, 20 t">', 'placeholder="p. ej. 2 cisternas / mes, 20 t" name="volumen" maxlength="120">')
    h = re.sub(r'<textarea class="inp"', '<textarea class="inp" name="mensaje" maxlength="5000" required', h, count=1)
    h = re.sub(r'<input type="checkbox"', '<input type="checkbox" name="privacidad" value="1" required', h, count=1)
    hp = ('<div aria-hidden="true" style="position: absolute; left: -10000px; top: auto; width: 1px; height: 1px; overflow: hidden">'
          '<label>Web<input type="text" name="web" tabindex="-1" autocomplete="off"></label></div>'
          '<input type="hidden" name="t" value=""><input type="hidden" name="idioma" value="es">')
    h = re.sub(r'<form style="', '<form id="contact-form" action="enviar.php" method="post" style="position: relative; ', h, count=1)
    h = h.replace('<form id="contact-form" action="enviar.php" method="post" style="position: relative; display: flex; flex-direction: column; gap: 20px">',
                  '<form id="contact-form" action="enviar.php" method="post" style="position: relative; display: flex; flex-direction: column; gap: 20px">' + hp, 1)
    assert 'name="web"' in h
    err = ('<div id="form-error" role="alert" hidden style="background: #FDECEC; border: 1px solid #E8A3A3; color: #7A1C1C; border-radius: 12px; '
           'padding: 14px 18px; font-size: 15px; line-height: 1.5"></div>')
    h = h.replace('<button type="button" onclick="pilSend()"', err + '<button type="submit"', 1)
    h = h.replace('<button type="button" onclick="pilReset()"', '<button type="button" id="send-again"', 1)
    h = re.sub(r'<script>\s*function pilSend\(\).*?</script>', FORM_JS, h, flags=re.S)
    assert 'pilSend' not in h and 'contact-form' in h
    open(p, 'w', encoding='utf-8').write(h)

FONT_LINKS = re.compile(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">')

def post_step():
    os.makedirs(D + 'fonts', exist_ok=True)
    for f in glob.glob(B + 'fonts_in/*/*.woff2'): shutil.copy(f, D + 'fonts/')
    shutil.copy(B + 'deploy/fonts.css', D + 'fonts/fonts.css')
    shutil.copy(B + 'deploy/enviar.php', D + 'enviar.php')
    for p in glob.glob(D + '*.html') + glob.glob(D + '*/*.html'):
        if p.endswith('/web.html'): continue
        sub = os.path.dirname(p) != D.rstrip('/')
        h = open(p, encoding='utf-8').read()
        h, n = FONT_LINKS.subn(f'<link rel="stylesheet" href="{"../" if sub else ""}fonts/fonts.css">', h)
        assert n == 1, p
        if sub: h = h.replace('action="enviar.php"', 'action="../enviar.php"')
        open(p, 'w', encoding='utf-8').write(h)

if __name__ == '__main__':
    {'form': form_step, 'post': post_step}[sys.argv[1]]()
    print('ok', sys.argv[1])
