import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
exec(open('make_prod.py').read().split('# ---------- SACK ----------')[0])  # logo_w, font, centered, wrap
src=cv2.imread('/mnt/user-data/attachments/fd2192db-e962-524a-b2a2-31b0b87be078/17936496-image.jpg')
H,W=src.shape[:2]
TL,TR,BR,BL=np.float32([478,410]),np.float32([706,396]),np.float32([716,456]),np.float32([488,472])
# inpaint old label + oval marks
m=np.zeros((H,W),np.uint8)
cv2.fillConvexPoly(m,np.int32([TL,TR,BR,BL]),255)
hs0=cv2.cvtColor(src,cv2.COLOR_BGR2HSV)
wl=((hs0[...,1]<25)&(hs0[...,2]>225)).astype(np.uint8)
reg=np.zeros_like(wl); reg[350:500,430:760]=1; wl&=reg
n0,l0,st0,_=cv2.connectedComponentsWithStats(wl)
if n0>1:
    k=1+np.argmax(st0[1:,4]); m[l0==k]=255
m=cv2.dilate(m,np.ones((13,13),np.uint8))
cv2.circle(m,(406,382),26,255,-1); cv2.circle(m,(812,479),27,255,-1); cv2.circle(m,(434,374),14,255,-1); cv2.circle(m,(838,477),14,255,-1)
clean=cv2.inpaint(src,m,9,cv2.INPAINT_TELEA)
# background mask (connected to corners, near-white)
hsv=cv2.cvtColor(clean,cv2.COLOR_BGR2HSV)
cand=((hsv[...,1]<28)&(hsv[...,2]>185)).astype(np.uint8)
n,lab=cv2.connectedComponents(cand)
bg=np.zeros((H,W),bool)
for c in {lab[0,0],lab[0,-1],lab[-1,0],lab[-1,-1]}:
    if c: bg|=lab==c
V=hsv[...,2].astype(float)
obj=(~bg).astype(np.uint8)
cnts,_=cv2.findContours(obj,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
big=max(cnts,key=cv2.contourArea); hull=cv2.convexHull(big)
inside=np.zeros((H,W),np.uint8); cv2.fillConvexPoly(inside,hull,1)
bg=bg&(inside==0)
alpha=np.where(bg,np.clip((248-V)/70,0,1)*0.75,1.0)
alpha=cv2.GaussianBlur(alpha.astype(np.float32),(0,0),1.2)
# label quad (expanded along label axes)
c=np.float32([530,445])
u=np.float32([800,150]);u/=np.linalg.norm(u)
v=np.float32([-190,130]);v/=np.linalg.norm(v)
w2,h2=175,62
Q=np.float32([c-u*w2-v*h2,c+u*w2-v*h2,c+u*w2+v*h2,c-u*w2+v*h2])
def make(name,sub,variant,path):
    img=clean.copy().astype(np.float32)
    if variant not in ('orig','cheddar2'):
        hh=cv2.cvtColor(clean,cv2.COLOR_BGR2HSV).astype(np.float32)
        if variant=='white': hh[...,1]*=0.22; hh[...,2]=np.clip(hh[...,2]*1.05,0,255)
        if variant=='cream': hh[...,0]=np.clip(hh[...,0]*0.6+22*0.4,0,179); hh[...,1]*=0.78; hh[...,2]=np.clip(hh[...,2]*1.02,0,255)
        if variant=='whitish': hh[...,1]*=0.42; hh[...,2]=np.clip(hh[...,2]*1.04,0,255)
        if variant=='orange':
            V0=hh[...,2].copy(); g0=cv2.GaussianBlur(V0,(0,0),5)
            spec=np.clip((V0-g0)/25,0,1)  # film highlights
            hh[...,0]=12; hh[...,1]=np.clip(205*(1-0.75*spec),0,255); hh[...,2]=np.clip(V0*0.93+18*spec,0,255)
        img=cv2.cvtColor(hh.astype(np.uint8),cv2.COLOR_HSV2BGR).astype(np.float32)
        img=np.where(bg[...,None],clean.astype(np.float32),img)
    if variant=='cheddar2':
        f0=clean.astype(np.float32); hs=cv2.cvtColor(clean,cv2.COLOR_BGR2HSV).astype(np.float32)
        V0=hs[...,2]; S0=cv2.GaussianBlur(hs[...,1],(0,0),2.5)
        body=cv2.GaussianBlur(np.clip((S0-6)/18,0,1),(0,0),2.0)[...,None]
        lum=(V0/np.percentile(V0[~bg],70))[...,None]
        orange=np.float32([22,172,248])[None,None,:]*np.clip(lum,0.45,1.08)   # BGR: strong yellow-orange
        g=cv2.cvtColor(clean,cv2.COLOR_BGR2GRAY).astype(np.float32)
        spec=np.clip((g-cv2.GaussianBlur(g,(0,0),6)-2)/20,0,1)[...,None]
        film=np.repeat(g[...,None],3,2)*0.97+np.float32([0,4,8])   # clear film: neutral, faint warm
        img=orange*body+film*(1-body)
        img=img*(1-spec*0.75)+255*spec*0.75
        img=np.where(bg[...,None],f0,img)
    # label
    LWp,LHp=800,352
    lab_=Image.new('RGB',(LWp,LHp),(250,250,247)); d=ImageDraw.Draw(lab_)
    d.rectangle([0,0,LWp-1,LHp-1],outline=(205,205,200),width=4)
    lw=logo_w(380); lab_.paste(lw,(LWp//2-lw.width//2,26),lw)
    f=font('ExtraBold',62); centered(d,LWp//2,26+lw.height+18,name.upper(),f,BLUE)
    centered(d,LWp//2,26+lw.height+100,sub,font('SemiBold',30),(95,100,120))
    L=cv2.cvtColor(np.asarray(lab_),cv2.COLOR_RGB2BGR)
    Mx=cv2.getPerspectiveTransform(np.float32([[0,0],[LWp,0],[LWp,LHp],[0,LHp]]),Q)
    warped=cv2.warpPerspective(L,Mx,(W,H),flags=cv2.INTER_AREA).astype(np.float32)
    lm=cv2.warpPerspective(np.full((LHp,LWp),255,np.uint8),Mx,(W,H)).astype(np.float32)/255
    lm=cv2.GaussianBlur(lm,(0,0),0.7)[...,None]
    # film: keep surface shading + highlights from cheese below
    g=cv2.cvtColor(clean,cv2.COLOR_BGR2GRAY).astype(np.float32)
    shade=np.clip(g/cv2.GaussianBlur(g,(0,0),25),0.9,1.12)[...,None]
    hi=np.clip(g-cv2.GaussianBlur(g,(0,0),6),0,255)[...,None]*0.5
    lab_on=np.clip(warped*shade*0.97+hi,0,255)
    img=img*(1-lm*0.96)+lab_on*(lm*0.96)
    out=np.dstack([cv2.cvtColor(np.clip(img,0,255).astype(np.uint8),cv2.COLOR_BGR2RGB),(alpha*255).astype(np.uint8)])
    im=Image.fromarray(out,'RGBA'); im=im.crop(im.getbbox())
    im.resize((im.width*3//4,im.height*3//4),Image.LANCZOS).save(path,optimize=True)
for pid,n,s,var in [('cagliata','Cagliata','Bloque 18–20 kg','white'),('mozza','Mozzarella','Bloque 10 kg','white'),
                    ('edam','Edam','Bloque · 30+ / 40+ m.g. ES','cream'),('gouda','Gouda','Bloque · 48 % m.g. ES','cream'),('emmental','Emmental','Bloque · 45 % m.g. ES','cream'),
                    ('cheddar','Cheddar','Bloque · 48 % m.g. ES','cheddar2')]:
    make(n,s,var,f'prodimg/quesoF-{pid}.png')
print('ok')
