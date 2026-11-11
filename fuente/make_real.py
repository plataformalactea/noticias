import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
exec(open('make_sack2.py').read().split('def sack2')[0])  # helpers: logo, fonts, warp, shade, shadow, heightmap, lighting, paper...

def shade_face(tex, r, intensity, seed, noise=0.02, film=False, spec=0.06):
    w,h=tex.size
    m=Image.new('L',(w,h),255)
    d=ndimage.distance_transform_edt(np.pad(np.ones((h-2,w-2)),1))
    hh=1-np.exp(-d/r)
    rng=np.random.default_rng(seed)
    n=ndimage.gaussian_filter(rng.standard_normal((h,w)),10);n/=np.abs(n).max()
    hh=hh+noise*n
    if film:
        n2=ndimage.gaussian_filter(rng.standard_normal((h,w)),2.5);n2/=np.abs(n2).max()
        edge=np.exp(-d/(r*2.2))
        hh=hh+0.05*n2*edge
    gy,gx=np.gradient(hh); k=0.02
    nx,ny,nz=-gx/k,-gy/k,np.ones_like(hh);nn=np.sqrt(nx**2+ny**2+nz**2)
    L=np.array([-0.4,-0.6,0.7]);L/=np.linalg.norm(L)
    lam=np.clip((nx*L[0]+ny*L[1]+nz*L[2])/nn,0,1)
    Hh=L+np.array([0,0,1]);Hh/=np.linalg.norm(Hh)
    sp=np.clip((nx*Hh[0]+ny*Hh[1]+nz*Hh[2])/nn,0,1)**(18 if film else 40)
    a=np.asarray(tex.convert('RGB')).astype(float)
    out=a*(intensity*(0.55+0.5*lam))[...,None]+255*(spec*sp)[...,None]
    img=Image.fromarray(np.clip(out,0,255).astype('uint8')).convert('RGBA')
    if film:
        st=Image.new('L',(w,h),0);ds=ImageDraw.Draw(st);random.seed(seed)
        for _ in range(5):
            x=random.uniform(-0.2,1)*w; ds.line([(x,0),(x+random.uniform(0.15,0.4)*w,h)],fill=random.randint(40,90),width=int(random.uniform(0.02,0.06)*w))
        st=st.filter(ImageFilter.GaussianBlur(w*0.025))
        img=Image.composite(Image.new('RGBA',(w,h),(255,255,255,255)),img,st)
    return img

def box_real(front,side,top,path,geom,r,seed,film=False,W=600,H=600,noise=0.02):
    S=2;sz=(W*S,H*S);P=lambda pts:[(x*S,y*S) for x,y in pts]
    A,B,C,D,E,F,G=geom
    c=Image.new('RGBA',sz,(0,0,0,0))
    shadow(c,(S*(A[0]-10),S*(D[1]-22),S*(F[0]+30),S*(D[1]+38)),S*16,130)
    fs=shade_face(front,r,1.0,seed,noise,film); ss=shade_face(side,r,0.72,seed+1,noise,film); ts=shade_face(top,r,1.08,seed+2,noise,film)
    c.alpha_composite(warp(ss,P([B,E,F,C]),sz))
    c.alpha_composite(warp(fs,P([A,B,C,D]),sz))
    c.alpha_composite(warp(ts,P([G,E,B,A]),sz))
    c=c.filter(ImageFilter.GaussianBlur(0.5))
    c=c.resize((W,H),Image.LANCZOS); c=c.crop(c.getbbox()); c.save(path,optimize=True)

def label(w,h,lines,scale=1.0):
    lab=paper((w,h),(250,249,245),7);d=ImageDraw.Draw(lab)
    d.rectangle([0,0,w-1,h-1],outline=(200,200,195,255),width=2)
    lw=logo_w(int(w*0.62));lab.alpha_composite(lw,(w//2-lw.width//2,int(h*0.07)))
    y=int(h*0.07)+lw.height+int(h*0.04)
    for txt,wt,sz_,col in lines:
        f=font(wt,int(sz_*scale)); centered(d,w//2,y,txt,f,col); y+=int(sz_*scale*1.35)
    return lab

def cheese(name,sub,col,path,seed):
    S=1
    front=Image.new('RGB',(700,300),col); 
    # subtle cheese texture
    a=np.asarray(front).astype(float); rng=np.random.default_rng(seed)
    a+=ndimage.gaussian_filter(rng.normal(0,10,(300,700,1)),(3,3,0)); front=Image.fromarray(np.clip(a,0,255).astype('uint8'))
    lab=label(300,190,[(name,'ExtraBold',30,BLUE),(sub,'Medium',16,(100,100,95))])
    front=front.convert('RGBA'); front.alpha_composite(lab,(200,55))
    side=Image.fromarray(np.clip(np.asarray(Image.new('RGB',(420,300),col)).astype(float)+ndimage.gaussian_filter(rng.normal(0,10,(300,420,1)),(3,3,0)),0,255).astype('uint8'))
    top=Image.fromarray(np.clip(np.asarray(Image.new('RGB',(700,420),col)).astype(float)+ndimage.gaussian_filter(rng.normal(0,10,(420,700,1)),(3,3,0)),0,255).astype('uint8'))
    box_real(front,side,top,path,[(60,282),(410,304),(410,470),(60,450),(530,264),(530,432),(180,242)],r=26,seed=seed,film=True)

def butter(path):
    kraft=(190,152,104); rng=np.random.default_rng(5)
    def kraft_tex(w,h,flutes=True):
        a=np.ones((h,w,3))*np.array(kraft,float)+rng.normal(0,5,(h,w,1))
        if flutes: a*= (1+0.025*np.sin(np.arange(w)/3.2))[None,:,None]
        return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')
    front=kraft_tex(700,320)
    lab=label(360,220,[('Mantequilla 82 %','ExtraBold',30,BLUE),('Bloque 25 kg · Uso industrial','Medium',15,(100,100,95)),('Conservar a 0–6 °C / –18 °C','Medium',13,(100,100,95))])
    front.alpha_composite(lab,(170,50))
    side=kraft_tex(440,320); ds=ImageDraw.Draw(side)
    ds.text((40,250),'25 kg',font=font('ExtraBold',40),fill=(60,50,40,200))
    top=kraft_tex(700,440,False); dt=ImageDraw.Draw(top)
    dt.rectangle([0,205,700,235],fill=(206,184,140,255)); dt.line([(0,220),(700,220)],fill=(160,130,90,255),width=2)  # tape + flap seam
    box_real(front,side,top,'prodimg/mantequilla.png',[(70,250),(400,272),(400,470),(70,452),(520,240),(520,438),(190,220)],r=8,seed=11,noise=0.03)

def drum(path):
    S=2;W,H=600,620;sz=(W*S,H*S)
    c=Image.new('RGBA',sz,(0,0,0,0));shadow(c,(S*135,S*545,S*480,S*605),S*18,130)
    x0,x1,y0,y1=170,430,120,550;ry=30
    cw=(x1-x0)*S; ch=(y1-y0)*S
    # cylindrical shading per column
    xs=np.linspace(-1,1,cw); th=np.arcsin(np.clip(xs,-1,1))
    light=math.radians(-35)
    lam=np.clip(np.cos(th-light),0,1); spec=np.clip(np.cos(th-math.radians(-20)),0,1)**60
    base=np.array((40,82,150),float)
    col=base[None,:]*(0.35+0.75*lam)[:,None]+255*0.55*spec[:,None]
    body=np.tile(col[None,:,:],(ch,1,1))
    rng=np.random.default_rng(3); body+=rng.normal(0,2.5,(ch,cw,1))
    bimg=Image.fromarray(np.clip(body,0,255).astype('uint8')).convert('RGBA')
    # label wrapped on cylinder
    lab=label(260,200,[('Grasa láctea anhidra','Bold',22,BLUE),('AMF · 200 kg','Medium',18,(100,100,95))],scale=1.0)
    lab=lab.resize((260*S,200*S),Image.LANCZOS)
    la=np.asarray(lab).astype(float); lh,lwid=la.shape[:2]
    # map: label spans theta in [-0.8,0.8]
    out=np.zeros((lh,cw,4))
    tl=np.linspace(-0.85,0.85,lwid); xl=np.sin(tl)  # positions in [-1,1]
    cols=((xl+1)/2*(cw-1)).astype(int)
    for i,cx in enumerate(cols): out[:,cx,:]=la[:,i,:]
    # fill gaps
    o=Image.fromarray(np.clip(out,0,255).astype('uint8'),'RGBA').filter(ImageFilter.MaxFilter(3))
    oa=np.asarray(o).astype(float); shadecol=(0.45+0.65*lam)[None,:,None]
    oa[...,:3]*=shadecol; o=Image.fromarray(np.clip(oa,0,255).astype('uint8'),'RGBA')
    bimg.alpha_composite(o,(0,int(142*S)))
    # hoops
    d=ImageDraw.Draw(bimg)
    for yy in (112,372):
        for k,(dy,colr) in enumerate([(-6,(20,40,80)),(0,(110,150,210)),(6,(25,50,95))]):
            d.line([(0,(yy+dy)*S),(cw,(yy+dy)*S)],fill=colr+(255,),width=int(4*S))
    hoop=np.asarray(bimg).astype(float); hoop[...,:3]=hoop[...,:3]  # keep
    # curve body top/bottom with ellipse mask
    m=Image.new('L',(cw,ch+ry*S),0);dm=ImageDraw.Draw(m)
    dm.rectangle([0,0,cw,ch],fill=255);dm.ellipse([0,ch-ry*S,cw,ch+ry*S],fill=255)
    full=Image.new('RGBA',(cw,ch+ry*S),(0,0,0,0)); full.paste(bimg,(0,0))
    bot=bimg.crop((0,ch-2,cw,ch)).resize((cw,ry*S+2)); full.paste(bot,(0,ch-2))
    full.putalpha(m)
    c.alpha_composite(full,(x0*S,y0*S))
    # lid
    lid=Image.new('RGBA',(cw,2*ry*S),(0,0,0,0)); dl=ImageDraw.Draw(lid)
    dl.ellipse([0,0,cw-1,2*ry*S-1],fill=(58,98,165,255),outline=(25,45,85,255),width=int(5*S))
    dl.ellipse([int(16*S),int(7*S),cw-int(16*S),2*ry*S-int(7*S)],fill=(78,120,186,255))
    dl.ellipse([int(175*S),int(18*S),int(205*S),int(34*S)],fill=(35,55,95,255))
    dl.ellipse([int(50*S),int(22*S),int(70*S),int(34*S)],fill=(35,55,95,255))
    lid=lid.filter(ImageFilter.GaussianBlur(0.8))
    c.alpha_composite(lid,(x0*S,(y0-ry)*S))
    c=c.resize((W,H),Image.LANCZOS); c=c.crop(c.getbbox()); c.save(path,optimize=True)

for i,(pid,n,s,col) in enumerate([('cagliata','Cagliata','Bloque 18–20 kg',(244,240,226)),('mozza','Mozzarella','Bloque 2,5 / 10 kg',(244,240,226)),
                    ('edam','Edam 40+','Bloque · Block',(234,186,70)),('gouda','Gouda 48+','Bloque · Block',(228,174,56)),('emmental','Emmental','Bloque · Block',(238,210,124))]):
    cheese(n,s,col,f'prodimg/queso-{pid}.png',seed=20+i)
butter('prodimg/mantequilla.png'); drum('prodimg/amf.png')
print('ok')
