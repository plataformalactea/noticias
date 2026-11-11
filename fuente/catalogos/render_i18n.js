const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
const names={industrial:'Catalogo_Linsoles_Lacteos_Industriales',retail:'Catalogo_Linsoles_Retail_Horeca'};
for(const L of ['en','fr','pt']) for(const n of ['industrial','retail']){
 const p=await b.newPage({viewport:{width:1123,height:794},deviceScaleFactor:1.6});
 await p.goto('file://'+path.resolve('catalogos/'+n+'_'+L+'.html'));await p.waitForTimeout(500);
 await p.pdf({path:'catalogos/'+names[n]+'_'+L.toUpperCase()+'.pdf',width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true});
 const secs=await p.$$('section.page');for(let i=0;i<secs.length;i++){await secs[i].screenshot({path:'catalogos/'+n+'-'+L+'-p'+(i+1)+'.png'});}
 await p.close();}
await b.close();})();
