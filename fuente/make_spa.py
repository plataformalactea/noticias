import re
D='Web_Plataforma_Lactea/'
pages=['index','industriales','retail-horeca','catalogos','blog','sobre-nosotros','solicitud','aviso-legal','privacidad','cookies']
styles=[];secs=[];scripts=[];head=None
for p in pages:
    h=open(D+p+'.html',encoding='utf-8').read()
    if head is None: head=h[:h.index('<style>')]
    for s in re.findall(r'<style>(.*?)</style>',h,re.S):
        if s not in styles: styles.append(s)
    body=h[h.index('<body>')+6:h.rindex('</body>')]
    for sc in re.findall(r'<script>(.*?)</script>',body,re.S): scripts.append(sc)
    body=re.sub(r'<script>.*?</script>','',body,flags=re.S)
    def fix(m):
        t=m.group(1); return f'href="#{ "inicio" if t=="index" else t}"'
    body=re.sub(r'href="([a-z-]+)\.html"',fix,body)
    pid='inicio' if p=='index' else p
    secs.append(f'<div class="pg" id="pg-{pid}"{"" if p=="index" else " hidden"}>{body}</div>')
for i in range(len(scripts)): scripts[i]=re.sub(r'([\'"])([a-z-]+)\.html\1',lambda m:m.group(1)+'#'+('inicio' if m.group(2)=='index' else m.group(2))+m.group(1),scripts[i])
dl_='<script>\n(function(){var dlp=(window.claude&&window.claude.use)?window.claude.use("downloads"):Promise.resolve(null);\ndocument.addEventListener(\'click\',function(e){var a=e.target.closest&&e.target.closest(\'a[href^="fichas/"],a[href^="catalogos/"]\');if(!a)return;e.preventDefault();\nvar href=a.getAttribute(\'href\'),name=a.getAttribute(\'download\')||href.split(\'/\').pop();\ndlp.then(function(d){if(!d){window.open(href,\'_blank\');return;}\nreturn fetch(href).then(function(r){if(!r.ok)throw new Error(\'fetch\');return r.blob();}).then(function(b){return d.save({filename:name,data:b});});\n}).catch(function(){});});})();\n</script>'
router='''<script>
(function(){var titles={};
function show(){var h=(location.hash||'#inicio').slice(1);var el=document.getElementById('pg-'+h),target=null;if(!el){var t=document.getElementById(h);if(t&&t.closest('.pg')){el=t.closest('.pg');target=t;}else{el=document.getElementById('pg-inicio');}}
document.querySelectorAll('.pg').forEach(function(p){p.hidden=(p!==el);});if(target){target.scrollIntoView();}else{window.scrollTo(0,0);}}
window.addEventListener('hashchange',show);show();})();
</script>'''
head=re.sub(r'<title>[^<]*</title>','<title>Plataforma Láctea</title>',head)
out=head+'<style>'+'\n'.join(styles)+'\n.pg[hidden]{display:none!important}</style>\n</head>\n<body>\n'+'\n'.join(secs)+'\n'+''.join('<script>'+s+'</script>' for s in scripts)+router+dl_+'\n</body>\n</html>'
open(D+'web.html','w',encoding='utf-8').write(out)
print(len(out), len(styles))
