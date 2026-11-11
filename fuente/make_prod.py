import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
OUT='prodimg/'
BLUE=(61,87,147); YEL=(228,200,43)
F='/usr/share/fonts/opentype/inter/Inter-%s.otf'
def font(w,s): return ImageFont.truetype(F%w,s)

# Linsoles logo -> transparent
lg=Image.open('/mnt/user-data/attachments/fd2192db-e962-524a-b2a2-31b0b87be078/9b972984-image.png').convert('RGB')
a=np.asarray(lg).astype(float); alpha=np.clip((255-a.min(axis=2))*3,0,255).astype('uint8')
logo=lg.convert('RGBA'); logo.putalpha(Image.fromarray(alpha)); logo=logo.crop(logo.getbbox())
def logo_w(w):
    return logo.resize((w,int(logo.height*w/logo.width)),Image.LANCZOS)

def coeffs(dst,src):
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A.append([x,y,1,0,0,0,-u*x,-u*y]);B.append(u);A.append([0,0,0,x,y,1,-v*x,-v*y]);B.append(v)
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()
def warp(tex,quad,size):
    w,h=tex.size
    out=tex.convert('RGBA').transform(size,Image.PERSPECTIVE,coeffs(quad,[(0,0),(w,0),(w,h),(0,h)]),Image.BICUBIC)
    m=Image.new('L',size,0);ImageDraw.Draw(m).polygon(quad,fill=255)
    out.putalpha(ImageChops.multiply(out.split()[3],m));return out
def shade(img,a,b,horizontal=True):
    arr=np.asarray(img.convert('RGBA')).astype(float);w,h=img.size
    g=np.linspace(a,b,w if horizontal else h)
    arr[...,:3]*= g[None,:,None] if horizontal else g[:,None,None]
    return Image.fromarray(np.clip(arr,0,255).astype('uint8'))
def shadow(canvas,box,blur,op=110):
    sh=Image.new('L',canvas.size,0);ImageDraw.Draw(sh).ellipse(box,fill=op)
    sh=sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.paste(Image.new('RGBA',canvas.size,(20,30,30,255)),(0,0),sh)
def centered(d,cx,y,txt,f,fill):
    w=d.textlength(txt,font=f);d.text((cx-w/2,y),txt,font=f,fill=fill)
def wrap(d,txt,f,maxw):
    words=txt.split();lines=[];cur=''
    for wd in words:
        t=(cur+' '+wd).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur);cur=wd
    lines.append(cur);return lines
def finish(c,path,size):
    c=c.resize(size,Image.LANCZOS);c.save(path,optimize=True)

# ---------- SACK ----------
def sack(name,sub,path):
    S=2;W=H=600;sz=(W*S,H*S);P=lambda v:v*S
    c=Image.new('RGBA',sz,(0,0,0,0))
    shadow(c,(P(110),P(520),P(490),P(575)),P(16))
    # outline (pillow)
    pts=[]
    def bez(p0,p1,p2,n=40):
        return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in np.linspace(0,1,n)]
    pts+=bez((160,92),(300,80),(440,92))
    pts+=bez((440,92),(486,320),(452,540))[1:]
    pts+=bez((452,540),(300,560),(148,540))[1:]
    pts+=bez((148,540),(114,320),(160,92))[1:]
    poly=[(P(x),P(y)) for x,y in pts]
    mask=Image.new('L',sz,0);ImageDraw.Draw(mask).polygon(poly,fill=255)
    body=Image.new('RGBA',sz,(242,238,229,255));d=ImageDraw.Draw(body)
    # blue band + yellow line
    d.rectangle([0,P(420),sz[0],P(500)],fill=BLUE+(255,))
    d.rectangle([0,P(410),sz[0],P(418)],fill=YEL+(255,))
    # stitched top seam
    d.rectangle([0,P(84),sz[0],P(122)],fill=(226,221,210,255))
    for x in range(150,450,14): d.line([(P(x),P(110)),(P(x+7),P(110))],fill=(150,140,120,255),width=P(2))
    # logo
    lw=logo_w(P(250)); body.alpha_composite(lw,(sz[0]//2-lw.width//2,P(150)))
    # texts
    f2=font('Medium',P(19)); f3=font('Bold',P(26))
    for fs in (34,30,26,23):
        f1=font('ExtraBold',P(fs)); lines=wrap(d,name,f1,P(270))
        if len(lines)<=2: break
    y=P(282)
    for ln in lines: centered(d,sz[0]//2,y,ln,f1,BLUE+(255,)); y+=P(fs+6)
    centered(d,sz[0]//2,y+P(4),sub,f2,(110,110,104,255))
    centered(d,sz[0]//2,P(446),'25 kg  ·  Peso neto',f3,(255,255,255,255))
    # cylindrical shading
    arr=np.asarray(body).astype(float); xs=np.linspace(-1,1,sz[0]); g=1-0.22*xs**2-0.06*xs
    ys=np.linspace(0,1,sz[1]); gv=1-0.08*ys
    arr[...,:3]*=g[None,:,None]*gv[:,None,None]
    body=Image.fromarray(np.clip(arr,0,255).astype('uint8'))
    # wrinkles
    wr=Image.new('L',sz,0);dw=ImageDraw.Draw(wr)
    random.seed(len(name))
    for i in range(7):
        x0=random.choice([random.uniform(150,210),random.uniform(390,450)]);y0=random.uniform(140,520)
        dw.line([(P(x0),P(y0)),(P(x0+random.uniform(-20,20)),P(y0+random.uniform(30,70)))],fill=60,width=P(3))
    wr=wr.filter(ImageFilter.GaussianBlur(P(3)))
    dark=Image.new('RGBA',sz,(0,0,0,255)); body=Image.composite(dark,body,wr.point(lambda v:v*0.5)).convert('RGBA')
    body.putalpha(mask)
    # soft edge darkening
    edge=mask.filter(ImageFilter.GaussianBlur(P(14)));inv=ImageChops.invert(edge)
    inv=ImageChops.multiply(inv,mask).point(lambda v:int(v*0.55))
    body=Image.composite(Image.new('RGBA',sz,(60,50,40,255)),body,inv);body.putalpha(mask)
    c.alpha_composite(body)
    finish(c,path,(W,H))

# ---------- BOX (butter carton / cheese block) ----------
def box3d(front,side,top,path,W=600,H=600,geom=None):
    S=2;sz=(W*S,H*S);P=lambda pts:[(x*S,y*S) for x,y in pts]
    A,B,C,D,E,F,G=geom
    c=Image.new('RGBA',sz,(0,0,0,0))
    shadow(c,(S*(A[0]-20),S*(D[1]-20),S*(F[0]+30),S*(D[1]+40)),S*16)
    c.alpha_composite(warp(shade(side,0.78,0.62),P([B,E,F,C]),sz))
    c.alpha_composite(warp(shade(front,1.0,0.9),P([A,B,C,D]),sz))
    c.alpha_composite(warp(shade(top,1.0,0.9,False),P([G,E,B,A]),sz))
    d=ImageDraw.Draw(c)
    d.line(P([A,B]),fill=(255,255,255,140),width=2*S);d.line(P([B,C]),fill=(255,255,255,70),width=2*S)
    finish(c,path,(W,H))

def butter(path):
    kraft=(196,160,112)
    front=Image.new('RGB',(600,300),kraft);d=ImageDraw.Draw(front)
    d.rounded_rectangle([60,40,540,260],radius=18,fill=(250,248,242))
    lw=logo_w(200);front.paste(lw,(300-lw.width//2,58),lw)
    centered(d,300,168,'Mantequilla 82 %',font('ExtraBold',36),BLUE)
    centered(d,300,214,'Bloque 25 kg  ·  Uso industrial',font('Medium',20),(110,110,104))
    side=Image.new('RGB',(400,300),kraft);ds=ImageDraw.Draw(side)
    ds.rectangle([0,120,400,150],fill=BLUE)
    top=Image.new('RGB',(600,400),tuple(int(v*1.06) for v in kraft));dt=ImageDraw.Draw(top)
    dt.rectangle([0,190,600,210],fill=(180,146,100))  # tape seam
    box3d(front,side,top,path,geom=[(70,250),(400,272),(400,470),(70,452),(520,240),(520,438),(190,220)])

def cheese(name,sub,col,path):
    front=Image.new('RGB',(600,260),col);d=ImageDraw.Draw(front)
    d.rounded_rectangle([150,50,450,210],radius=16,fill=(255,255,255))
    lw=logo_w(170);front.paste(lw,(300-lw.width//2,62),lw)
    centered(d,300,140,name,font('ExtraBold',30),BLUE)
    centered(d,300,178,sub,font('Medium',16),(110,110,104))
    side=Image.new('RGB',(400,260),col)
    top=Image.new('RGB',(600,400),tuple(min(255,int(v*1.05)) for v in col))
    # shrink-wrap sheen on top
    dt=ImageDraw.Draw(top);dt.ellipse([80,80,520,260],fill=tuple(min(255,int(v*1.12)) for v in col))
    top=top.filter(ImageFilter.GaussianBlur(30))
    box3d(front,side,top,path,geom=[(60,280),(410,302),(410,470),(60,452),(530,262),(530,432),(180,240)])

# ---------- DRUM ----------
def drum(path):
    S=2;W=H=600;sz=(W*S,H*S)
    c=Image.new('RGBA',sz,(0,0,0,0));shadow(c,(S*140,S*520,S*470,S*575),S*16)
    x0,x1,y0,y1=170,430,110,530;ry=34
    body=Image.new('RGBA',sz,(0,0,0,0));d=ImageDraw.Draw(body)
    base=(52,92,160)
    d.rectangle([S*x0,S*y0,S*x1,S*y1],fill=base+(255,));d.ellipse([S*x0,S*(y1-ry),S*x1,S*(y1+ry)],fill=base+(255,))
    arr=np.asarray(body).astype(float);xs=np.linspace(0,1,sz[0]);
    t=np.clip((xs-x0/W)/((x1-x0)/W),0,1);g=0.62+0.6*np.sin(t*math.pi)**0.8-0.15*t
    arr[...,:3]*=g[None,:,None];body=Image.fromarray(np.clip(arr,0,255).astype('uint8'))
    d=ImageDraw.Draw(body)
    for yy in (230,410):
        d.arc([S*x0,S*(yy-ry),S*x1,S*(yy+ry)],0,180,fill=(30,50,90,255),width=S*6)
        d.arc([S*x0,S*(yy-ry+6),S*x1,S*(yy+ry+6)],0,180,fill=(140,170,220,200),width=S*3)
    # label
    lab=Image.new('RGBA',(240,150),(250,250,248,255));dl=ImageDraw.Draw(lab)
    lw=logo_w(170);lab.alpha_composite(lw,(120-lw.width//2,10))
    centered(dl,120,78,'Grasa láctea anhidra',font('Bold',17),BLUE)
    centered(dl,120,104,'AMF  ·  200 kg',font('Medium',16),(110,110,104))
    lab=lab.resize((S*240,S*150),Image.LANCZOS);body.alpha_composite(lab,(S*180,S*262))
    c.alpha_composite(body)
    # top lid
    d=ImageDraw.Draw(c)
    d.ellipse([S*x0,S*(y0-ry),S*x1,S*(y0+ry)],fill=(70,110,175,255),outline=(30,50,90,255),width=S*4)
    d.ellipse([S*(x0+18),S*(y0-ry+8),S*(x1-18),S*(y0+ry-8)],fill=(95,135,195,255))
    d.ellipse([S*340,S*(y0-12),S*372,S*(y0+6)],fill=(40,60,100,255))
    finish(c,path,(W,H))

# ---------- TANKER TRUCK ----------
def tanker(path):
    S=2;W,H=900,460;sz=(W*S,H*S);P=lambda v:int(v*S)
    c=Image.new('RGBA',sz,(0,0,0,0));shadow(c,(P(40),P(380),P(880),P(430)),P(14),90)
    d=ImageDraw.Draw(c)
    # chassis
    d.rectangle([P(60),P(318),P(860),P(338)],fill=(40,44,48,255))
    # tank (stainless)
    tank=Image.new('RGBA',sz,(0,0,0,0));dt=ImageDraw.Draw(tank)
    dt.rounded_rectangle([P(270),P(110),P(870),P(318)],radius=P(100),fill=(200,206,210,255))
    arr=np.asarray(tank).astype(float);ys=np.linspace(0,1,sz[1])
    t=np.clip((ys-110/H)/(208/H),0,1);g=0.70+0.45*np.exp(-((t-0.28)/0.16)**2)-0.25*t
    arr[...,:3]*=g[:,None,None];tank=Image.fromarray(np.clip(arr,0,255).astype('uint8'));dt=ImageDraw.Draw(tank)
    for x in (330,815): dt.line([(P(x),P(112)),(P(x),P(316))],fill=(150,156,160,255),width=P(3))
    dt.rectangle([P(330),P(96),P(820),P(110)],fill=(120,126,130,255))  # walkway
    for x in (420,560,700): dt.rounded_rectangle([P(x),P(86),P(x+50),P(98)],radius=P(4),fill=(150,156,160,255))
    # brand panel on tank
    lw=logo_w(P(270));tank.alpha_composite(lw,(P(570)-lw.width//2,P(132)))
    fnt=font('ExtraBold',P(22));w=dt.textlength('Productos lácteos a granel',font=fnt);dt.text((P(570)-w/2,P(236)),'Productos lácteos a granel',font=fnt,fill=(30,50,100,255))
    c.alpha_composite(tank)
    d=ImageDraw.Draw(c)
    # cab
    cab=[(P(60),P(330)),(P(60),P(170)),(P(95),P(120)),(P(200),P(112)),(P(250),P(130)),(P(258),P(330))]
    d.polygon(cab,fill=BLUE+(255,))
    d.polygon([(P(80),P(178)),(P(108),P(138)),(P(190),P(132)),(P(196),P(200)),(P(80),P(204))],fill=(170,205,230,255))
    d.line([(P(205),P(140)),(P(208),P(320))],fill=(40,60,110,255),width=P(3))
    d.rectangle([P(60),P(270),P(258),P(282)],fill=YEL+(255,))
    d.rectangle([P(48),P(292),P(70),P(330)],fill=(60,64,68,255))  # bumper
    d.ellipse([P(58),P(240),P(74),P(258)],fill=(255,240,180,255))  # light
    # wheels
    for x in (130,470,560,760,840):
        d.ellipse([P(x-40),P(300),P(x+40),P(380)],fill=(28,30,32,255))
        d.ellipse([P(x-20),P(320),P(x+20),P(360)],fill=(150,156,160,255))
        d.ellipse([P(x-7),P(333),P(x+7),P(347)],fill=(60,64,68,255))
    finish(c,path,(W,H))

POWDER=[('smp','Leche desnatada en polvo','Skimmed Milk Powder'),('wmp','Leche entera en polvo','Whole Milk Powder'),
 ('ffmp','Leche en polvo con grasa vegetal','Fat Filled Milk Powder'),('smpsl','Leche desnatada en polvo sin lactosa','Lactose free SMP'),
 ('perm','Permeado de leche en polvo','Milk Permeate Powder'),('cas-a','Caseína ácida','Acid Casein'),('cas-r','Caseína de cuajo','Rennet Casein'),
 ('casna','Caseinato de sodio','Sodium Caseinate'),('mcc','Caseína micelar','Micellar Casein'),('swp','Suero dulce en polvo','Sweet Whey Powder'),
 ('wpc35','Proteína de suero WPC 35','Whey Protein Concentrate'),('wpc80','Proteína de suero WPC 80','Whey Protein Concentrate'),('wpi','Aislado de proteína de suero','WPI 90 · Whey Protein Isolate')]
for pid,n,s in POWDER: sack(n,s,OUT+f'saco-{pid}.png')
tanker(OUT+'cisterna.png'); butter(OUT+'mantequilla.png'); drum(OUT+'amf.png')
for pid,n,s,col in [('cagliata','Cagliata','Bloque 18–20 kg',(246,243,232)),('mozza','Mozzarella','Bloque 2,5 / 10 kg',(246,243,232)),
                    ('edam','Edam 40+','Bloque',(236,190,72)),('gouda','Gouda 48+','Bloque',(232,180,60)),('emmental','Emmental','Bloque',(240,214,130))]:
    cheese(n,s,col,OUT+f'queso-{pid}.png')
print('done')
