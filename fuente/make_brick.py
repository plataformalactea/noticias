import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops

S=2  # supersample
W,H=500,920

def coeffs(dst, src):
    # mapping output (dst) -> input (src) for PIL PERSPECTIVE
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A.append([x,y,1,0,0,0,-u*x,-u*y]); B.append(u)
        A.append([0,0,0,x,y,1,-v*x,-v*y]); B.append(v)
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()

def warp(tex, quad, size):
    w,h=tex.size
    src=[(0,0),(w,0),(w,h),(0,h)]
    out=tex.convert('RGBA').transform(size, Image.PERSPECTIVE, coeffs(quad,src), Image.BICUBIC)
    mask=Image.new('L',size,0); ImageDraw.Draw(mask).polygon(quad,fill=255)
    out.putalpha(ImageChops.multiply(out.split()[3],mask))
    return out

def shade(img, a, b, horizontal=True):
    # multiply by linear gradient a->b
    w,h=img.size
    g=np.linspace(a,b,w if horizontal else h)
    arr=np.asarray(img.convert('RGB')).astype(float)
    arr*= g[None,:,None] if horizontal else g[:,None,None]
    return Image.fromarray(np.clip(arr,0,255).astype('uint8'))

def make(front_path, cap_rgb, out_path):
    front=Image.open(front_path).convert('RGB')
    fw,fh=front.size
    # side texture: stretch a clean edge strip of the front
    sw=int(fw*59/90)
    yel=next((y for y in range(fh) if (lambda q:q[0]>190 and q[1]>160 and q[2]<110)(front.getpixel((fw-3,y)))), int(fh*0.18))
    col=front.getpixel((fw-3,int(fh*0.5)))
    strip=Image.new('RGB',(sw,fh),col)
    dd=ImageDraw.Draw(strip)
    import random; random.seed(7)
    W2=(250,250,248); G2=(150,150,150)
    def lines(x0,x1,y0,y1,step,colr,thick=3,ratio=(0.55,1.0)):
        yy=y0
        while yy<y1:
            dd.rectangle([x0,yy,x0+int((x1-x0)*random.uniform(*ratio)),yy+thick],fill=colr); yy+=step
    m=int(sw*0.12); x0,x1=m,sw-m
    # top: product denomination / ingredients in white text lines on the colour
    lines(x0,x1,int(fh*0.08),int(fh*0.20),11,W2,3,(0.5,1.0))
    # white info panel (conservación, origen)
    dd.rectangle([x0,int(fh*0.23),x1,int(fh*0.33)],fill=W2)
    lines(x0+8,x1-8,int(fh*0.24),int(fh*0.32),10,G2,2,(0.4,0.95))
    # nutrition table
    ny0,ny1=int(fh*0.37),int(fh*0.58)
    dd.rectangle([x0,ny0,x1,ny1],fill=W2)
    dd.rectangle([x0+6,ny0+6,x1-6,ny0+16],fill=col)
    yy=ny0+24
    while yy<ny1-8:
        dd.line([x0+6,yy,x1-6,yy],fill=(205,205,205),width=1)
        dd.rectangle([x0+8,yy+3,x0+8+int((x1-x0)*0.45),yy+6],fill=G2)
        dd.rectangle([x1-8-int((x1-x0)*0.18),yy+3,x1-8,yy+6],fill=G2)
        yy+=12
    # more white text on colour
    lines(x0,x1,int(fh*0.61),int(fh*0.68),10,W2,3,(0.45,0.95))
    # barcode block
    by0,by1=int(fh*0.71),int(fh*0.86)
    dd.rectangle([x0,by0,x1,by1],fill=W2)
    bx0,bx1=x0+int((x1-x0)*0.12),x1-int((x1-x0)*0.12); xx=bx0
    while xx<bx1:
        wdt=random.choice([1,1,2,3]); dd.rectangle([xx,by0+8,xx+wdt-1,by1-16],fill=(30,30,30)); xx+=wdt+random.choice([1,2])
    dd.rectangle([bx0,by1-12,bx1,by1-9],fill=G2)
    # gingham band at the bottom, same as front
    gy=int(fh*0.90)
    ging=front.crop((0,gy,int(fw*0.35),fh))
    x=0
    while x<sw:
        strip.paste(ging,(x,gy)); x+=ging.width
    side=shade(strip,0.82,0.64)
    fr=shade(front,1.0,0.90)
    sz=(W*S,H*S)
    P=lambda pts:[(x*S,y*S) for x,y in pts]
    A,B,C,D=(50,196),(312,222),(312,884),(50,860)
    E,F=(424,190),(424,852)
    G=(162,164)
    canvas=Image.new('RGBA',sz,(0,0,0,0))
    # shadow
    sh=Image.new('L',sz,0); ImageDraw.Draw(sh).ellipse(P([(30,846),(470,904)]),fill=110)
    sh=sh.filter(ImageFilter.GaussianBlur(14*S))
    canvas.paste(Image.new('RGBA',sz,(20,30,30,255)),(0,0),sh)
    canvas.alpha_composite(warp(side,P([B,E,F,C]),sz))
    canvas.alpha_composite(warp(fr,P([A,B,C,D]),sz))
    # top face: white carton with soft shading
    top=Image.new('RGB',(400,200),(246,247,247))
    top=shade(top,0.97,0.86)
    canvas.alpha_composite(warp(top,P([G,E,B,A]),sz))
    d=ImageDraw.Draw(canvas)
    # sealed top fin (crease line across top)
    m1=((A[0]+G[0])/2,(A[1]+G[1])/2); m2=((B[0]+E[0])/2,(B[1]+E[1])/2)
    d.line(P([m1,m2]),fill=(205,210,210,255),width=3*S)
    d.line(P([(m1[0],m1[1]+3),(m2[0],m2[1]+3)]),fill=(255,255,255,200),width=1*S)
    # edges / highlights
    d.line(P([A,B]),fill=(255,255,255,170),width=2*S)
    d.line(P([B,E]),fill=(230,232,232,200),width=2*S)
    d.line(P([B,C]),fill=(255,255,255,90),width=2*S)
    # cap near the front edge of the top face
    cx,cy=B[0]-52+(E[0]-B[0])*0.30,B[1]-14+(E[1]-B[1])*0.30  # near the front-right corner
    rx,ry,hgt=34,12,26
    cap=tuple(cap_rgb); dark=tuple(int(c*0.86) for c in cap)
    d.ellipse(P([(cx-rx-4,cy-ry-4+4),(cx+rx+4,cy+ry+4+4)]),fill=(214,218,218,255))  # base collar
    d.rectangle(P([(cx-rx,cy-hgt),(cx+rx,cy)]),fill=dark+(255,))
    d.ellipse(P([(cx-rx,cy-ry),(cx+rx,cy+ry)]),fill=dark+(255,))
    for i in range(-rx+6,rx-2,9):  # ribs
        d.line(P([(cx+i,cy-hgt+ry*0.4),(cx+i,cy+ry*0.6)]),fill=tuple(int(c*0.78) for c in cap)+(255,),width=2*S)
    d.ellipse(P([(cx-rx,cy-hgt-ry),(cx+rx,cy-hgt+ry)]),fill=cap+(255,),outline=(196,200,200,255),width=2*S)
    d.ellipse(P([(cx-rx+10,cy-hgt-ry+4),(cx+rx-22,cy-hgt+ry-6)]),fill=(255,255,255,170))
    # front-face sheen
    sheen=Image.new('L',sz,0)
    ImageDraw.Draw(sheen).polygon(P([(68,198),(112,203),(112,864),(68,860)]),fill=55)
    sheen=sheen.filter(ImageFilter.GaussianBlur(18*S))
    canvas.alpha_composite(Image.composite(Image.new('RGBA',sz,(255,255,255,255)),Image.new('RGBA',sz,(0,0,0,0)),sheen))
    canvas=canvas.resize((W,H),Image.LANCZOS)
    bbox=canvas.getbbox(); canvas=canvas.crop(bbox)
    canvas.save(out_path, optimize=True)

make('entera-000.png',(244,245,245),'brick_entera.png')
make('semi-000.png',(244,245,245),'brick_semi.png')
make('desn-000.png',(244,245,245),'brick_desnatada.png')
