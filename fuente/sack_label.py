import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
base=Image.open('prodimg/saco-base.png').convert('RGBA')
B=np.asarray(base).astype(np.float32); H,W=B.shape[:2]
lum=B[...,:3].mean(-1); ref=ndimage.gaussian_filter(lum,40)
fac=np.clip(lum/np.maximum(ref,1),0.85,1.12)
F='/usr/share/fonts/opentype/inter/Inter-%s.otf'
NAVY=(40,62,120)
def wrap(d,txt,f,maxw):
    words=txt.split();lines=[];cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur);cur=w
    lines.append(cur);return lines
def make(name,acr,path):
    lay=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(lay);cx=455
    for fs in (46,42,38,34):
        f=ImageFont.truetype(F%'ExtraBold',fs);lines=wrap(d,name.upper(),f,560)
        if len(lines)<=2: break
    lines=lines+[acr]
    lh=fs+8; total=len(lines)*lh
    y=688-total//2
    for i,ln in enumerate(lines):
        w=d.textlength(ln,font=f);d.text((cx-w/2,y),ln,font=f,fill=NAVY+(255,));y+=lh
    L=np.asarray(lay).astype(np.float32);a=L[...,3:4]/255*0.95
    col=L[...,:3]*fac[...,None]
    out=B.copy();out[...,:3]=B[...,:3]*(1-a)+col*a
    img=Image.fromarray(np.clip(out,0,255).astype(np.uint8),'RGBA')
    img.resize((W//2,H//2),Image.LANCZOS).save(path,optimize=True)
POWDER=[('smp','Leche desnatada en polvo','SMP'),('wmp','Leche entera en polvo','WMP'),('ssmp','Leche semidesnatada en polvo','SSMP'),
 ('ffmp','Leche en polvo con grasa vegetal','FFMP'),('smpsl','Leche desnatada en polvo sin lactosa','LF SMP'),
 ('perm','Permeado de leche en polvo','MPP'),('cas-a','Caseína ácida','AC'),('cas-r','Caseína de cuajo','RC'),
 ('casna','Caseinato de sodio','SC'),('mcc','Caseína micelar','MCC'),('swp','Suero dulce en polvo','SWP'),
 ('wpc35','Concentrado de proteína de suero','WPC 35'),('wpc80','Concentrado de proteína de suero','WPC 80'),('wpi','Aislado de proteína de suero','WPI 90')]
import sys
only=sys.argv[1:]
for pid,n,s_ in POWDER:
    if only and pid not in only: continue
    make(n,s_,f'prodimg/sacoL-{pid}.png')
print('ok')
