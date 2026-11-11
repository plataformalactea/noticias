import numpy as np, cv2
from PIL import Image, ImageFilter
from scipy import ndimage
src=np.asarray(Image.open('/mnt/user-data/attachments/fd2192db-e962-524a-b2a2-31b0b87be078/7c41fa2b-image.png').convert('RGB')).astype(np.float32)
H,W=src.shape[:2]
r,g,b=src[...,0],src[...,1],src[...,2]
box=np.zeros((H,W),bool); box[250:680,250:910]=True
M=((g>r+20)|((r-b>118)&(r>185)))&box
M=ndimage.binary_dilation(M,iterations=7)
M=ndimage.binary_fill_holes(M)
Mf=M.astype(np.float32)
# low-frequency fill (normalized convolution)
s=22
num=np.stack([ndimage.gaussian_filter(src[...,c]*(1-Mf),s) for c in range(3)],-1)
den=ndimage.gaussian_filter(1-Mf,s)[...,None]+1e-6
low=num/den
for _ in range(2):
    num=np.stack([ndimage.gaussian_filter(np.where(M[...,None],low,src)[...,c],s) for c in range(3)],-1)
    low=np.where(M[...,None],num,src)
# high-frequency texture from clean kraft patch
patch=src[60:250,200:900]
hp=patch-np.stack([ndimage.gaussian_filter(patch[...,c],8) for c in range(3)],-1)
tex=np.zeros_like(src); ph,pw=hp.shape[:2]
for y in range(0,H,ph):
    for x in range(0,W,pw):
        tex[y:y+ph,x:x+pw]=hp[:min(ph,H-y),:min(pw,W-x)]
filled=np.where(M[...,None],low+tex*0.9,src)
# feather mask edges
Mb=ndimage.gaussian_filter(Mf,2)[...,None]
out=src*(1-Mb)+filled*Mb
# ---- logo
lg=Image.open('/mnt/user-data/attachments/fd2192db-e962-524a-b2a2-31b0b87be078/9b972984-image.png').convert('RGB')
la=np.asarray(lg).astype(float); alpha=np.clip((255-la.min(axis=2))*3,0,255).astype('uint8')
logo=lg.convert('RGBA'); logo.putalpha(Image.fromarray(alpha)); logo=logo.crop(logo.getbbox())
LW=640; logo=logo.resize((LW,int(logo.height*LW/logo.width)),Image.LANCZOS)
lh=logo.height; cx=585; top=448-lh//2
L=np.asarray(logo).astype(np.float32)
x0,y0=cx-LW//2,top
region=out[y0:y0+lh,x0:x0+LW]
lum=region.mean(-1); ref=ndimage.gaussian_filter(out.mean(-1),60)[y0:y0+lh,x0:x0+LW]
fac=np.clip(lum/ref,0.82,1.15)[...,None]
grain=(tex[y0:y0+lh,x0:x0+LW].mean(-1)/255*0.9)[...,None]
col=L[...,:3]*fac*(1+grain)
a=(L[...,3:4]/255)*0.94
out[y0:y0+lh,x0:x0+LW]=region*(1-a)+col*a
out=np.clip(out,0,255).astype(np.uint8)
# ---- remove white background
img=Image.fromarray(out)
wm=(out.min(-1)>238).astype(np.uint8)
n,lab=cv2.connectedComponents(wm)
bg=np.zeros_like(wm)
for c in {lab[0,0],lab[0,-1],lab[-1,0],lab[-1,-1]}:
    if c: bg|=(lab==c)
alpha=(1-bg)*255
alpha=Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
img=img.convert('RGBA'); img.putalpha(alpha); img=img.crop(img.getbbox())
img.save('prodimg/saco-linsoles.png',optimize=True)
img.resize((img.width//2,img.height//2),Image.LANCZOS).save('prodimg/saco-linsoles-small.png')
print(img.size)
