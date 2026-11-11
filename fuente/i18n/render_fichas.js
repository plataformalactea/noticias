const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();const list=JSON.parse(fs.readFileSync('i18n/fichas/list.json'));
const p=await b.newPage();
for(const n of list){await p.goto('file://'+path.resolve('i18n/fichas/'+n+'.html'));await p.waitForTimeout(150);
 await p.pdf({path:'i18n/fichas/'+n+'.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});}
await b.close();})();
