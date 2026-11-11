const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();
const B='http://127.0.0.1:8099/';const pages=['index','industriales','retail-horeca','catalogos','blog','sobre-nosotros','mision','solicitud','aviso-legal','privacidad','cookies'];
const res={bad:new Set(),ext:new Set(),js:[],hash:{},weight:{},links:new Set(),cons:[]};
p.on('response',r=>{if(r.status()>=400)res.bad.add(r.status()+' '+r.url())});
p.on('requestfailed',r=>res.bad.add('FAIL '+r.url()));
p.on('request',r=>{if(!r.url().startsWith(B)&&!r.url().startsWith('data:'))res.ext.add(r.url())});
p.on('pageerror',e=>res.js.push(e.message));p.on('console',m=>{if(m.type()==='error')res.cons.push(m.text())});
for(const L of ['','fr/','pt/','en/'])for(const pg of pages){
 let bytes=0;const h=r=>{r.sizes().then(s=>bytes+=s.responseBodySize+s.responseHeadersSize).catch(()=>{})};p.on('requestfinished',h);
 await p.goto(B+L+pg+'.html',{waitUntil:'networkidle'});await p.waitForTimeout(200);p.off('requestfinished',h);res.weight[L+pg]=Math.round(bytes/1024);
 const ls=await p.$$eval('a[href]',as=>as.map(a=>a.getAttribute('href')));
 for(const l of ls){if(l==='#'){res.hash[L+pg]=(res.hash[L+pg]||0)+1;continue;} if(/^(mailto|tel|https?):/.test(l)){if(/^https?:/.test(l))res.ext.add('LINK '+l);continue;} res.links.add(new URL(l,B+L+pg+'.html').href.split('#')[0]);}
}
for(const u of res.links){const r=await p.request.get(u);if(r.status()>=400)res.bad.add('LINK '+r.status()+' '+u);}
console.log(JSON.stringify({bad:[...res.bad],ext:[...res.ext],js:res.js,cons:[...new Set(res.cons)],hash:res.hash,weight:res.weight,nlinks:res.links.size},null,1));await b.close();})();
