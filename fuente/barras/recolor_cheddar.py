import numpy as np, cv2
from PIL import Image
eb=np.asarray(Image.open('prodimg/quesoF-cheddar.png').convert('RGBA')).astype(np.float32)
hs=cv2.cvtColor(eb[...,:3].astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
m=(eb[...,3]>200)&(hs[...,1]>120)
tH,tS,tV=[np.median(hs[...,i][m]) for i in range(3)]; print('target HSV',tH,tS,tV)
def rec(rgba):
    a=np.asarray(rgba).astype(np.float32); rgb=a[...,:3].astype(np.uint8)
    h=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV).astype(np.float32)
    om=(h[...,0]>=4)&(h[...,0]<=21)&(h[...,1]>90)
    sH,sS,sV=[np.median(h[...,i][om]) for i in range(3)]
    w=cv2.GaussianBlur(om.astype(np.float32),(0,0),1.2)
    nh=h.copy(); nh[...,0]=h[...,0]+(tH-sH); nh[...,1]=np.clip(h[...,1]*(tS/sS),0,255); nh[...,2]=np.clip(h[...,2]*(tV/sV),0,255)
    out=h*(1-w[...,None])+nh*w[...,None]
    o=cv2.cvtColor(out.astype(np.uint8),cv2.COLOR_HSV2RGB)
    if a.shape[2]==4: o=np.dstack([o,a[...,3].astype(np.uint8)])
    print('src',sH,sS,sV); return Image.fromarray(o)
rec(Image.open('barras/barra-cheddar-recorte.png').convert('RGBA')).save('barras/barra-cheddar-recorte.png')
rec(Image.open('barras/barra-cheddar.jpg').convert('RGB')).save('barras/barra-cheddar.jpg',quality=86)
