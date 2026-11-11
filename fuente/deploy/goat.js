const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for (const [w,L,f] of [[1280,'','../_goat_es.png'],[390,'fr/','../_goat_fr_m.png']]){const c=await b.newContext({viewport:{width:w,height:900}});const p=await c.newPage();
await p.goto('http://127.0.0.1:8765/'+L+'blog.html',{waitUntil:'networkidle'});
const sec=(await p.$$('section')).slice(-1)[0];
const h=await p.evaluateHandle(()=>[...document.querySelectorAll('section')].find(s=>s.textContent.includes('Apartado')||s.textContent.includes('Rubrique')));
await h.asElement().screenshot({path:f});console.log(w,await p.evaluate(()=>document.documentElement.scrollWidth));}
await b.close();})();
