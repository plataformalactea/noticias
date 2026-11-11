import numpy as np, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage
exec(open('make_prod.py').read().split('# ---------- SACK ----------')[0])  # logo, fonts, helpers

def bez(p0,p1,p2,n=60):
    t=np.linspace(0,1,n)[:,None];p0,p1,p2=map(np.array,(p0,p1,p2))
    return list(map(tuple,((1-t)**2*p0+2*(1-t)*t*p1+t*t*p2)))
def mask_from(pts,sz,S):
    m=Image.new('L',sz,0);ImageDraw.Draw(m).polygon([(x*S,y*S) for x,y in pts],fill=255);return m
def heightmap(mask,R,seed,S,creases=()):
    m=np.asarray(mask)>0
    d=ndimage.distance_transform_edt(m)
    h=1-np.exp(-d/(R*S))
    rng=np.random.default_rng(seed)
    n=ndimage.gaussian_filter(rng.standard_normal(m.shape),12*S); n/=np.abs(n).max()+1e-9
    n2=ndimage.gaussian_filter(rng.standard_normal(m.shape),4*S); n2/=np.abs(n2).max()+1e-9
    h=h+0.06*n+0.012*n2
    if creases:
        cl=Image.new('L',mask.size,0);dc=ImageDraw.Draw(cl)
        for (a,b,w) in creases: dc.line([(a[0]*S,a[1]*S),(b[0]*S,b[1]*S)],fill=255,width=int(w*S))
        c=ndimage.gaussian_filter(np.asarray(cl).astype(float)/255,3*S)
        h=h-0.10*c
    return h*m
def lighting(h,mask,L=(-0.45,-0.65,0.62),k=0.035,amb=0.50,dif=0.62,spec=0.10):
    gy,gx=np.gradient(h)
    nx,ny,nz=-gx/k,-gy/k,np.ones_like(h)
    nn=np.sqrt(nx**2+ny**2+nz**2);nx,ny,nz=nx/nn,ny/nn,nz/nn
    L=np.array(L);L=L/np.linalg.norm(L)
    lam=np.clip(nx*L[0]+ny*L[1]+nz*L[2],0,1)
    Hh=L+np.array([0,0,1]);Hh/=np.linalg.norm(Hh)
    sp=np.clip(nx*Hh[0]+ny*Hh[1]+nz*Hh[2],0,1)**30
    return amb+dif*lam, spec*sp
def paper(sz,base,seed):
    rng=np.random.default_rng(seed)
    a=np.ones((sz[1],sz[0],3))*np.array(base,float)
    a+=rng.normal(0,3.5,(sz[1],sz[0],1))
    img=Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')
    d=ImageDraw.Draw(img);random.seed(seed)
    for _ in range(900):
        x=random.uniform(0,sz[0]);y=random.uniform(0,sz[1]);l=random.uniform(6,22)
        d.line([(x,y),(x+l,y+random.uniform(-2,2))],fill=tuple(int(c*0.96) for c in base)+(255,),width=1)
    return img.filter(ImageFilter.GaussianBlur(0.6))

def sack2(name,sub,path,seed=1):
    S=2;W,H=600,640;sz=(W*S,H*S)
    canvas=Image.new('RGBA',sz,(0,0,0,0))
    shadow(canvas,(S*105,S*560,S*530,S*628),S*18,130)
    base=(236,231,219)
    # ---- shapes
    front=bez((138,128),(280,112),(418,126))+bez((418,126),(452,360),(432,592))[1:]+bez((432,592),(290,612),(146,598))[1:]+bez((146,598),(112,360),(138,128))[1:]
    side=bez((418,126),(470,132),(506,150))+bez((506,150),(526,370),(508,574))[1:]+bez((508,574),(470,590),(432,592))[1:]+bez((432,592),(452,360),(418,126))[1:]
    fm=mask_from(front,sz,S); sm=mask_from(side,sz,S)
    # ---- side gusset
    hs=heightmap(sm,40,seed+7,S,creases=[((462,150),(472,580),5)])
    sh_s,sp_s=lighting(hs,sm,amb=0.42,dif=0.42)
    alb=np.asarray(paper(sz,base,seed+3)).astype(float)[...,:3]
    out=alb*sh_s[...,None]*0.86+255*sp_s[...,None]
    sideimg=Image.fromarray(np.clip(out,0,255).astype('uint8')).convert('RGBA');sideimg.putalpha(sm.filter(ImageFilter.GaussianBlur(0.8)))
    canvas.alpha_composite(sideimg)
    # ---- front: albedo with print
    alb=paper(sz,base,seed);d=ImageDraw.Draw(alb)
    cx=285*S
    lw=logo_w(int(230*S));alb.alpha_composite(lw,(cx-lw.width//2,int(185*S)))
    for fs in (32,28,25,22):
        f1=font('ExtraBold',int(fs*S));lines=wrap(d,name,f1,int(250*S))
        if len(lines)<=2: break
    y=int(318*S)
    for ln in lines: centered(d,cx,y,ln,f1,BLUE+(255,));y+=int((fs+6)*S)
    centered(d,cx,y+int(6*S),sub,font('Medium',int(17*S)),(95,95,90,255))
    d.line([(int(190*S),int(445*S)),(int(380*S),int(445*S))],fill=YEL+(255,),width=int(4*S))
    centered(d,cx,int(462*S),'Peso neto 25 kg',font('Bold',int(22*S)),BLUE+(255,))
    centered(d,cx,int(494*S),'Net weight 25 kg  ·  Poids net 25 kg',font('Medium',int(14*S)),(95,95,90,255))
    d.rectangle([int(215*S),int(528*S),int(355*S),int(562*S)],outline=(120,120,115,255),width=int(1.5*S))
    d.text((int(224*S),int(533*S)),'LOTE / BBD:',font=font('Medium',int(12*S)),fill=(110,110,105,255))
    creases=[((150,150),(205,230),6),((410,145),(360,225),6),((160,560),(215,520),5),((420,560),(372,525),5),((300,140),(292,175),4)]
    hf=heightmap(fm,55,seed,S,creases=creases)
    sh_f,sp_f=lighting(hf,fm)
    a=np.asarray(alb).astype(float)[...,:3]
    out=a*sh_f[...,None]+255*sp_f[...,None]
    frontimg=Image.fromarray(np.clip(out,0,255).astype('uint8')).convert('RGBA');frontimg.putalpha(fm.filter(ImageFilter.GaussianBlur(0.8)))
    canvas.alpha_composite(frontimg)
    # ---- sewn top with crepe tape
    top=[(128,96),(300,84),(512,110),(512,150),(300,124),(128,134)]
    tm=mask_from(top,sz,S)
    tape=Image.new('RGBA',sz,(222,212,190,255));dt=ImageDraw.Draw(tape)
    for yy in range(80*S,160*S,3): dt.line([(0,yy),(sz[0],yy)],fill=(208,197,172,255),width=1)
    ht=heightmap(tm,10,seed+11,S); sh_t,sp_t=lighting(ht,tm,amb=0.6,dif=0.45)
    a=np.asarray(tape).astype(float)[...,:3]*sh_t[...,None]
    tapeimg=Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA');tapeimg.putalpha(tm.filter(ImageFilter.GaussianBlur(0.8)))
    canvas.alpha_composite(tapeimg)
    dd=ImageDraw.Draw(canvas)
    for i in range(0,48):
        x=136+i*7.7; y=112-0.0+((x-128)/(512-128))*(14) - 2*np.sin((x-128)/384*np.pi)*3
        dd.line([(x*S,y*S),((x+4)*S,(y+0.4)*S)],fill=(120,100,70,255),width=int(1.6*S))
    canvas=canvas.resize((W,H),Image.LANCZOS)
    canvas=canvas.crop(canvas.getbbox())
    canvas.save(path,optimize=True)

POWDER=[('smp','Leche desnatada en polvo','Skimmed Milk Powder'),('wmp','Leche entera en polvo','Whole Milk Powder'),
 ('ffmp','Leche en polvo con grasa vegetal','Fat Filled Milk Powder'),('smpsl','Leche desnatada en polvo sin lactosa','Lactose free SMP'),
 ('perm','Permeado de leche en polvo','Milk Permeate Powder'),('cas-a','Caseína ácida','Acid Casein'),('cas-r','Caseína de cuajo','Rennet Casein'),
 ('casna','Caseinato de sodio','Sodium Caseinate'),('mcc','Caseína micelar','Micellar Casein'),('swp','Suero dulce en polvo','Sweet Whey Powder'),
 ('wpc35','Proteína de suero WPC 35','Whey Protein Concentrate'),('wpc80','Proteína de suero WPC 80','Whey Protein Concentrate'),('wpi','Aislado de proteína de suero','WPI 90 · Whey Protein Isolate')]
import sys
only=sys.argv[1:]
for i,(pid,n,s) in enumerate(POWDER):
    if only and pid not in only: continue
    sack2(n,s,f'prodimg/saco-{pid}.png',seed=i+3)
print('ok')
