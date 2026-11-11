import re
B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
D = B + 'Web_Plataforma_Lactea/'
PAGES = ['index','industriales','retail-horeca','catalogos','blog','sobre-nosotros','mision','solicitud','aviso-legal','privacidad','cookies']
LANGS = ['es', 'fr', 'pt', 'en']
spa = open(B + 'make_spa.py', encoding='utf-8').read()
ns = {}
exec(spa[spa.index("dl_="):spa.index("router='''")], ns); DL = ns['dl_']
pid = lambda p: 'inicio' if p == 'index' else p
styles, secs, scripts, head = [], [], [], None
for L in LANGS:
    for p in PAGES:
        h = open(D + ('' if L == 'es' else L + '/') + p + '.html', encoding='utf-8').read()
        if L != 'es':
            h = h.replace('"../img/', '"img/').replace('"../fichas/', '"fichas/').replace('"../catalogos/', '"catalogos/').replace("'../img/", "'img/")
            for k in ('ci', 'cr'):
                for a, b in ((f'id="{k}', f'id="{k}{L}'), (f'for="{k}', f'for="{k}{L}'), (f'#{k}', f'#{k}{L}'), (f'name="{k}"', f'name="{k}{L}"'), (f'cv-{k}', f'cv-{k}{L}')):
                    h = h.replace(a, b)
        if head is None: head = h[:h.index('<style>')]
        for s in re.findall(r'<style>(.*?)</style>', h, re.S):
            if s not in styles: styles.append(s)
        body = h[h.index('<body>') + 6:h.rindex('</body>')]
        root = f'pg-{L}-{pid(p)}'
        for sc in re.findall(r'<script>(.*?)</script>', body, re.S):
            sc = sc.replace("document.getElementById(", "root.querySelector('#'+")
            sc = sc.replace("document.addEventListener('click',function(e){", "document.addEventListener('click',function(e){if(!root.contains(e.target))return;")
            sc = sc.replace('function pilSend(', f'window.pilSend_{L}=function(').replace('function pilReset(', f'window.pilReset_{L}=function(')
            sc = re.sub(r"([\"'])([a-z-]+)\.html\1", lambda m: m.group(1) + f'#{L}/' + pid(m.group(2)) + m.group(1), sc)
            scripts.append(f"(function(){{var root=document.getElementById('{root}');\n{sc}\n}})();")
        body = re.sub(r'<script>.*?</script>', '', body, flags=re.S)
        body = body.replace('onclick="pilSend()"', f'onclick="pilSend_{L}()"').replace('onclick="pilReset()"', f'onclick="pilReset_{L}()"')
        # language switcher links: ../xx/page.html, xx/page.html, ../page.html, page.html with hreflang
        def sw(m):
            lang = m.group(2); return f'href="#{lang}/{pid(p)}" hreflang="{lang}"'
        body = re.sub(r'href="[^"]*?([a-z-]+)\.html" hreflang="([a-z]{2})"', sw, body)
        body = re.sub(r'href="([a-z-]+)\.html"', lambda m: f'href="#{L}/{pid(m.group(1))}"', body)
        body = re.sub(r'href="#(cat-industrial|cat-retail)"', lambda m: f'href="#{L}/{m.group(1)}"', body)
        body = re.sub(r'id="(cat-industrial|cat-retail)"', lambda m: f'id="{L}-{m.group(1)}"', body)
        hidden = '' if (L == 'es' and p == 'index') else ' hidden'
        secs.append(f'<div class="pg" id="{root}" lang="{L}"{hidden}>{body}</div>')
router = '''<script>
(function(){function show(){var h=(location.hash||'#es/inicio').slice(1);var m=h.match(/^(es|fr|pt|en)\\/(.+)$/);var lang=m?m[1]:'es',key=m?m[2]:h;
var el=document.getElementById('pg-'+lang+'-'+key),target=null;
if(!el){var t=document.getElementById(lang+'-'+key);if(t&&t.closest('.pg')){el=t.closest('.pg');target=t;}else{el=document.getElementById('pg-'+lang+'-inicio')||document.getElementById('pg-es-inicio');}}
document.querySelectorAll('.pg').forEach(function(p){p.hidden=(p!==el);});document.documentElement.lang=el.getAttribute('lang');
if(target){target.scrollIntoView();}else{window.scrollTo(0,0);}}
window.addEventListener('hashchange',show);show();})();
</script>'''
head = re.sub(r'<title>[^<]*</title>', '<title>Plataforma Láctea</title>', head)
out = head + '<style>' + '\n'.join(styles) + '\n.pg[hidden]{display:none!important}</style>\n</head>\n<body>\n' + '\n'.join(secs) + '\n' + ''.join('<script>' + s + '</script>' for s in scripts) + router + DL + '\n</body>\n</html>'
open(D + 'web.html', 'w', encoding='utf-8').write(out)
print(len(out), len(styles))
