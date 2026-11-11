const { chromium } = require('playwright');
const BASE = 'http://127.0.0.1:8765/';
const PAGES = ['index','industriales','retail-horeca','catalogos','blog','sobre-nosotros','mision','solicitud','aviso-legal','privacidad','cookies'];
(async () => {
  const b = await chromium.launch();
  const urls = [];
  for (const L of ['', 'en/', 'fr/', 'pt/']) for (const p of PAGES) urls.push(BASE + L + p + '.html');
  urls.push(BASE + 'no-existe.html', BASE + 'en/nada.html');
  const bad = [], ext = new Set(), errs = [];
  const linkSet = new Set();
  for (const vw of [{ width: 1280, height: 900 }, { width: 390, height: 844 }]) {
    const ctx = await b.newContext({ viewport: vw });
    for (const u of urls) {
      const pg = await ctx.newPage(); let bytes = 0;
      pg.on('pageerror', e => errs.push(u + ' ' + e.message));
      pg.on('response', async r => { const url = r.url(); if (!url.startsWith(BASE)) ext.add(url); else if (r.status() >= 400 && !/no-existe|nada/.test(url)) bad.push(r.status() + ' ' + url); try { bytes += (await r.body()).length } catch (e) {} });
      pg.on('request', r => { if (!r.url().startsWith(BASE) && !r.url().startsWith('data:')) ext.add(r.url()); });
      const resp = await pg.goto(u, { waitUntil: 'networkidle' });
      await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } });
      await pg.waitForTimeout(300);
      const info = await pg.evaluate(() => ({
        sw: document.documentElement.scrollWidth, title: document.title,
        desc: (document.querySelector('meta[name=description]') || {}).content || '',
        hl: document.querySelectorAll('link[hreflang]').length,
        links: [...document.querySelectorAll('a[href]')].map(a => a.href),
        broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src),
      }));
      info.links.forEach(l => linkSet.add(l.split('#')[0]));
      if (info.sw > vw.width + 1) bad.push(`overflow ${vw.width} ${info.sw} ${u}`);
      info.broken.forEach(s => bad.push('img ' + s + ' on ' + u));
      if (!/no-existe|nada/.test(u) && (!info.desc || info.hl !== 5)) bad.push('meta ' + u);
      if (vw.width === 1280 && /\/(en\/|fr\/|pt\/)?index\.html$/.test(u)) console.log('weight', u, (bytes / 1e6).toFixed(2) + ' MB');
      if (/no-existe|nada/.test(u) && vw.width === 1280) console.log('404', resp.status(), info.title);
      await pg.close();
    }
    await ctx.close();
  }
  // check internal links
  const ctx = await b.newContext();
  for (const l of linkSet) {
    if (!l.startsWith(BASE)) { if (!/^(mailto|tel):/.test(l)) ext.add('link ' + l); continue; }
    const r = await ctx.request.get(l); if (r.status() >= 400) bad.push('link ' + r.status() + ' ' + l);
  }
  console.log('links checked', linkSet.size);
  console.log('external:', [...ext].filter(x => !x.startsWith('link mailto')));
  console.log('errors:', errs);
  console.log('bad:', bad);
  await b.close();
})();
