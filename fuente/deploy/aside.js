const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for (const [w,L,f] of [[1280,'','../_aside_es.png'],[390,'en/','../_aside_en_m.png']]){const c=await b.newContext({viewport:{width:w,height:900}});const p=await c.newPage();
await p.goto('http://127.0.0.1:8765/'+L+'blog.html',{waitUntil:'networkidle'});const a=await p.$('aside');await a.screenshot({path:f});console.log(w,await p.evaluate(()=>document.documentElement.scrollWidth));}
await b.close();})();
