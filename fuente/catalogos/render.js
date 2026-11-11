const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
for(const [n,out] of [['industrial','Catalogo_Linsoles_Lacteos_Industriales'],['retail','Catalogo_Linsoles_Retail_Horeca']]){
 const p=await b.newPage({viewport:{width:1123,height:794},deviceScaleFactor:1.6});
 await p.goto('file://'+path.resolve('catalogos/'+n+'.html'));await p.waitForTimeout(600);
 await p.pdf({path:'catalogos/'+out+'.pdf',width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true});
 const secs=await p.$$('section.page');
 for(let i=0;i<secs.length;i++){await secs[i].screenshot({path:'catalogos/'+n+'-p'+(i+1)+'.png'});}
 console.log(n,secs.length);await p.close();}
await b.close();})();
