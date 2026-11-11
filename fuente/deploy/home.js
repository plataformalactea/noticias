const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();for (const [w,f] of [[1280,'../_home_news.png'],[390,'../_home_news_m.png']]){const c=await b.newContext({viewport:{width:w,height:900}});const p=await c.newPage();
await p.goto('http://127.0.0.1:8765/fr/index.html',{waitUntil:'networkidle'});const g=await p.$('#home-noticias');await g.screenshot({path:f});console.log(w,await p.evaluate(()=>document.documentElement.scrollWidth));}await b.close();})();
