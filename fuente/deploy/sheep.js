const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for (const [w,L,f] of [[1280,'','../_sheep_es.png'],[390,'en/','../_sheep_en_m.png']]){const c=await b.newContext({viewport:{width:w,height:900}});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://127.0.0.1:8765/'+L+'blog.html',{waitUntil:'networkidle'});
const h=await p.evaluateHandle(()=>[...document.querySelectorAll('section')].find(s=>/Leche de oveja|Sheep milk/.test(s.querySelector('h2')?.textContent||'')));
await h.asElement().screenshot({path:f});console.log(w,await p.evaluate(()=>document.documentElement.scrollWidth));}
console.log(errs);await b.close();})();
