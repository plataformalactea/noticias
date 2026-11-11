const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for (const w of [390,1280]){const c=await b.newContext({viewport:{width:w,height:900}});
for (const L of ['','en/','fr/','pt/']){const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://127.0.0.1:8765/'+L+'blog.html',{waitUntil:'networkidle'});
console.log(w,L||'es',await p.evaluate(()=>document.documentElement.scrollWidth));
if(w===1280&&L==='fr/')await p.screenshot({path:'../_blog_fr.png'});}}
console.log('errors',errs);await b.close();})();
