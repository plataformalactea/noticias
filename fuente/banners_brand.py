import numpy as np, cv2, math
from PIL import Image
D='webactual/'
def rgba_logo(path, white_thr=235):
    im=Image.open(path).convert('RGBA'); a=np.asarray(im).astype(np.float32)
    if a[...,3].min()==255:
        mn=a[...,:3].min(-1); a[...,3]=np.clip((255-mn)*4,0,255)
    im=Image.fromarray(a.astype(np.uint8),'RGBA'); return im.crop(im.getbbox())
LIN=rgba_logo('/mnt/user-data/attachments/fd2192db-e962-524a-b2a2-31b0b87be078/9b972984-image.png')
PIL_=rgba_logo('prodimg/logo-pil-web.png')
def paste_print(base, logo, cx, cy, w, opacity=0.95, cyl=False, shade=True):
    """print logo on surface: keep base shading via multiply-ish blend"""
    h=int(logo.height*w/logo.width)
    lg=logo.resize((w,h),Image.LANCZOS)
    L=np.asarray(lg).astype(np.float32)
    if cyl:  # horizontal compression toward edges (cylinder wrap)
        xs=np.linspace(-1,1,w); src=np.sin(xs*math.pi/2*0.85)/math.sin(math.pi/2*0.85)
        mapx=((src+1)/2*(w-1)).astype(np.float32); mapx=np.tile(mapx,(h,1)); mapy=np.tile(np.arange(h,dtype=np.float32)[:,None],(1,w))
        L=cv2.remap(L,mapx,mapy,cv2.INTER_LINEAR)
    B=np.asarray(base).astype(np.float32)
    x0,y0=int(cx-w/2),int(cy-h/2)
    reg=B[y0:y0+h,x0:x0+w,:3]
    a=L[...,3:4]/255*opacity
    if shade:
        lum=reg.mean(-1,keepdims=True); ref=np.percentile(lum,90)
        fac=np.clip(lum/ref,0.55,1.05)
    else: fac=1
    col=L[...,:3]*fac
    B[y0:y0+h,x0:x0+w,:3]=reg*(1-a)+col*a
    return Image.fromarray(np.clip(B,0,255).astype(np.uint8))
# 01 & 04: PIL logo on lab coat chest
b1=Image.open(D+'banner01.jpg').convert('RGB'); b1=paste_print(b1,PIL_,712,365,60,0.97); b1.save(D+'banner01_pil.jpg',quality=88)
b4=Image.open(D+'banner04.jpg').convert('RGB'); b4=paste_print(b4,PIL_,842,276,54,0.97); b4.save(D+'banner04_pil.jpg',quality=88)
# 03: Linsoles on every tank
b3=Image.open(D+'banner03_moved.jpg').convert('RGB')
tanks=[(157,150,78),(246,170,52),(318,180,46),(381,185,46),(248,372,86),(341,380,46),(403,382,48),(469,384,52),(532,384,42)]
for cx,cy,w in tanks: b3=paste_print(b3,LIN,cx,cy,w,0.93,cyl=True)
b3.save(D+'banner03_lin.jpg',quality=88)
# 02: our truck, smaller and further right, scene extended
b2=np.asarray(Image.open(D+'banner02.jpg').convert('RGB')).astype(np.float32); H,W=b2.shape[:2]
tr=Image.open('/mnt/user-data/attachments/fd2192db-e962-524a-b2a2-31b0b87be078/77966e5a-image.png').convert('RGB')
th=int(H*0.64); tw=int(tr.width*th/tr.height); tr=np.asarray(tr.resize((tw,th),Image.LANCZOS)).astype(np.float32)
X0=600; TW=W-X0
tile=np.zeros((H,TW,3),np.float32)
tile[H-th:,TW-tw:]=tr
top=H-th
row=np.median(tr[:6].reshape(-1,3),axis=0)
g=np.linspace(0.86,1.0,top)[:,None,None]
sky=np.ones((top,tw,3),np.float32)*row[None,None,:]*g
tile[:top,TW-tw:]=sky
bl=40; w_=np.linspace(0,1,bl)[:,None,None]
tile[top:top+bl,TW-tw:]=row[None,None,:]*(1-w_)+tr[:bl]*w_
ext=TW-tw
tile[:,:ext]=tile[:,ext:2*ext][:,::-1]
ramp=np.clip(np.arange(TW)/70,0,1)[None,:,None]
canvas=b2.copy(); canvas[:,X0:]=b2[:,X0:]*(1-ramp)+tile*ramp
Image.fromarray(canvas.astype(np.uint8)).save(D+'banner02_truck.jpg',quality=88)
for n in ['01_pil','02_truck','03_lin','04_pil']:
    Image.open(D+'banner'+n+'.jpg').resize((800,327)).save(D+'_p'+n+'.png')
print('ok',tw,X0)
