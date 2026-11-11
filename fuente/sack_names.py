import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
im=Image.open('prodimg/saco-linsoles-blanco.png').convert('RGBA')
A=np.asarray(im).astype(np.float32); rgb=A[...,:3].copy(); al=A[...,3]
H,W=rgb.shape[:2]
lum=rgb.mean(-1)
r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
blue=(b>r+25)
white=(lum>185)&(np.abs(r-b)<25)

def fill_white(region):
    """replace pixels in region with paper estimated from surrounding white pixels"""
    known=white&~region&(al>250)
    s=18;num=np.zeros_like(rgb);den=ndimage.gaussian_filter(known.astype(np.float32),s)+1e-6
    for c in range(3): num[...,c]=ndimage.gaussian_filter(rgb[...,c]*known,s)/den
    # second pass larger sigma where den small
    s2=45;den2=ndimage.gaussian_filter(known.astype(np.float32),s2)+1e-6
    num2=np.stack([ndimage.gaussian_filter(rgb[...,c]*known,s2)/den2 for c in range(3)],-1)
    wgt=np.clip(den[...,None]*4,0,1)
    est=num*wgt+num2*(1-wgt)
    patch=A[120:300,180:760,:3]
    hp=patch-np.stack([ndimage.gaussian_filter(patch[...,c],6) for c in range(3)],-1)
    tex=np.zeros_like(rgb); ph,pw=hp.shape[:2]
    for yy in range(0,H,ph):
        for xx in range(0,W,pw):
            tex[yy:yy+ph,xx:xx+pw]=hp[:min(ph,H-yy),:min(pw,W-xx)]
    est=est+tex*0.95
    m=ndimage.gaussian_filter(region.astype(np.float32),1.2)[...,None]
    return rgb*(1-m)+est*m

# 1) slogan text region (keep the side rules)
slog=np.zeros((H,W),bool); slog[694:764,150:846]=True
slog&=(lum<215)
slog=ndimage.binary_dilation(slog,iterations=3)
rgb=fill_white(slog)
lum=rgb.mean(-1); r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]; blue=(b>r+25); white=(lum>185)&(np.abs(r-b)<25)

# 2) leaf + swoosh: everything blue above the band edge curve, in the right part of the front
ox,oy=380,640
xs=[];ys=[]
for x in range(150,470,4):
    col=blue[oy+250:oy+430,ox+x]; wcol=white[oy+250:oy+430,ox+x]
    # lowest white->blue transition in this window
    idx=[i for i in range(1,len(col)) if wcol[i-1] and col[i]]
    if idx: xs.append(ox+x); ys.append(oy+250+idx[-1])
p=np.polyfit(xs,ys,2)
print('fit pts',len(xs))
X=np.arange(W); edge=np.polyval(p,X)
# join with left band edge: find band top at x=ox+100
leaf=np.zeros((H,W),bool)
Y=np.arange(H)[:,None]
x0,x1=ox+105,ox+474
region=(Y<edge[None,:]-1)&(Y>oy+90)&(X[None,:]>=x0)&(X[None,:]<=x1)
leaf=region&(lum<215)
leaf=ndimage.binary_dilation(leaf,iterations=2)&region
rgb=fill_white(leaf)
base=np.concatenate([np.clip(rgb,0,255),al[...,None]],-1).astype(np.uint8)
Image.fromarray(base,'RGBA').save('prodimg/saco-base.png')
print('edge at x0,x1',edge[x0],edge[x1])
