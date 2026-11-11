B = '/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad/'
IND = ['9dbaf90ef49cc27f167a1d8eabc63f25','c9429ec6cbee14adaea115a0ed34c54e','a8d084b23c3c80bc86183c2d99ae0aa3','dcfc1d038ac2001136d9ca50c6723214','9e08f6e8a39a3f63e2142aa331ed9829','d37386050ecb6d210dde19f085278c64','35a74227fa46122c00534d74249a5300']
RET = ['cda6270a5ca68c76d8c28b58e81fc9a0','b3645ab9b08d6641f341cbdb2dd37d76','81eb5799f042dc15eb67de785d8f0d12','4422940662207c67deb4d7ba414612bc']
IND_T = ['Portada','Leches en polvo','Proteínas lácteas','Sueros en polvo','Grasas lácteas','Líquidos lácteos','Quesos']
RET_T = ['Portada','Leche UHT en brik','Quesos nacionales','Quesos Horeca']
BASE_CSS = '''
.cv{display:flex;flex-direction:column;gap:14px}
.cv input{position:absolute;opacity:0;pointer-events:none}
.cv-stage{position:relative;background:#FFFFFF;border:1px solid #D3DCEA;border-radius:16px;overflow:hidden;box-shadow:0 14px 34px rgba(14,42,79,.12);aspect-ratio:297/210}
.cv-pg{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;display:block;opacity:0;transition:opacity .25s}
.cv-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 16px}
.cv-ctl{display:none;align-items:center;gap:10px}
.cv-btn{cursor:pointer;user-select:none;font-weight:700;font-size:14px;padding:10px 16px;border-radius:999px;border:1.5px solid #0E2A4F;background:#FFFFFF;color:#0E2A4F}
.cv-btn:hover{background:#0E2A4F;color:#FFFFFF}
.cv-btn.off{opacity:.3;pointer-events:none}
.cv-num{font-size:14px;font-weight:700;color:#4D5D78;min-width:110px;text-align:center}
.cv-th{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px}
.cv-th label{flex:none;cursor:pointer;width:112px;border:2px solid transparent;border-radius:8px;overflow:hidden;background:#FFFFFF;opacity:.7}
.cv-th label:hover{opacity:1}
.cv-th img{width:100%;aspect-ratio:297/210;object-fit:cover;display:block}
.cv-th span{display:block;font-size:11px;font-weight:700;color:#0E2A4F;padding:4px 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
'''

def viewer(prefix, ids, titles, pdf, fname, title, sub):
    n = len(ids)
    css = []
    for i in range(1, n + 1):
        sel = f'.cv-{prefix}:has(#{prefix}{i}:checked)'
        if i == 1:
            sel = f'.cv-{prefix}:not(:has(.cvr:checked)), .cv-{prefix}:has(#{prefix}1:checked)'
            css.append(f'.cv-{prefix}:not(:has(.cvr:checked)) .cv-p1, .cv-{prefix}:has(#{prefix}1:checked) .cv-p1{{opacity:1;z-index:1}}')
            css.append(f'.cv-{prefix}:not(:has(.cvr:checked)) .cv-c1, .cv-{prefix}:has(#{prefix}1:checked) .cv-c1{{display:flex}}')
            css.append(f'.cv-{prefix}:not(:has(.cvr:checked)) .cv-t1, .cv-{prefix}:has(#{prefix}1:checked) .cv-t1{{border-color:#2B4F9C;opacity:1}}')
        else:
            css.append(f'{sel} .cv-p{i}{{opacity:1;z-index:1}}')
            css.append(f'{sel} .cv-c{i}{{display:flex}}')
            css.append(f'{sel} .cv-t{i}{{border-color:#2B4F9C;opacity:1}}')
    radios = ''.join(f'<input type="radio" class="cvr" name="{prefix}" id="{prefix}{i}">' for i in range(1, n + 1))
    imgs = ''.join(f'<img class="cv-pg cv-p{i}" src="/_blob/{b}" alt="Catálogo, página {i}: {titles[i-1]}">' for i, b in enumerate(ids, 1))
    ctls = ''
    for i in range(1, n + 1):
        prev = f'<label class="cv-btn" for="{prefix}{i-1}">‹ Anterior</label>' if i > 1 else '<span class="cv-btn off">‹ Anterior</span>'
        nxt = f'<label class="cv-btn" for="{prefix}{i+1}">Siguiente ›</label>' if i < n else '<span class="cv-btn off">Siguiente ›</span>'
        ctls += f'<div class="cv-ctl cv-c{i}">{prev}<span class="cv-num">Página {i} de {n}</span>{nxt}</div>'
    thumbs = ''.join(f'<label class="cv-t{i}" for="{prefix}{i}"><img src="/_blob/{b}" alt=""><span>{titles[i-1]}</span></label>' for i, b in enumerate(ids, 1))
    html = f'''<section id="catalogo">
<div style="max-width: 1240px; margin: 0 auto; padding: 40px 24px 8px; display: flex; flex-direction: column; gap: 18px">
<div style="display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 12px 24px">
<div style="display: flex; flex-direction: column; gap: 6px"><span style="font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2B4F9C">Catálogo</span><h2 style="margin: 0; font-family: Archivo, sans-serif; font-weight: 800; font-size: 32px">{title}</h2><p style="margin: 0; font-size: 15px; color: #4D5D78">{sub}</p></div>
<a href="/_blob/{pdf}" download="{fname}" target="_blank" class="cta">Descargar catálogo (PDF)</a>
</div>
<div class="cv cv-{prefix}">{radios}<div class="cv-stage">{imgs}</div><div class="cv-bar">{ctls}</div><div class="cv-th">{thumbs}</div></div>
</div>
</section>
'''
    return html, '\n'.join(css)

def apply(path, prefix, ids, titles, pdf, fname, title, sub):
    s = open(path, encoding='utf-8').read()
    assert 'id="catalogo"' not in s
    h, css = viewer(prefix, ids, titles, pdf, fname, title, sub)
    i = s.index('</section>') + len('</section>')
    s = s[:i] + '\n\n' + h + s[i:]
    j = s.index('</style>')
    s = s[:j] + BASE_CSS + css + '\n' + s[j:]
    open(path, 'w', encoding='utf-8').write(s)

apply(B + 'web/project/Industriales.dc.html', 'ci', IND, IND_T, 'f27038ba815803a11a7def6e09fc9bcb', 'Catalogo_Linsoles_Lacteos_Industriales.pdf',
      'Lácteos industriales', 'Hojee el catálogo página a página o descárguelo en PDF.')
apply(B + 'web/project/Retail-Horeca.dc.html', 'cr', RET, RET_T, '6f9b51182fe0b9a576ea6d92cce1f0bd', 'Catalogo_Linsoles_Retail_Horeca.pdf',
      'Lácteos Retail / Horeca', 'Hojee el catálogo página a página o descárguelo en PDF.')
print('ok')
