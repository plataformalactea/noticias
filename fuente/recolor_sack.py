import numpy as np, cv2
from PIL import Image
im=Image.open('prodimg/saco-linsoles.png').convert('RGBA')
a=np.asarray(im).astype(np.float32); rgb=a[...,:3]; al=a[...,3:]
hsv=cv2.cvtColor(rgb.astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)  # H 0-180
H,S,V=hsv[...,0]*2,hsv[...,1]/255,hsv[...,2]/255
def band(x,lo,hi,soft):
    return np.clip(np.minimum((x-lo)/soft+1,(hi-x)/soft+1),0,1)
green=band(H,75,175,12)*np.clip((S-0.18)/0.1,0,1)
kraft=band(H,0,42,4)*np.clip((1.02-S)/0.08,0,1)*np.clip((V-0.12)/0.08,0,1)
kraft=np.maximum(kraft,np.clip((0.16-S)/0.06,0,1)*np.clip((V-0.55)/0.1,0,1))
kraft=kraft*(1-green)
# green -> Linsoles blue
hsv2=hsv.copy()
hsv2[...,0]=np.where(green>0,(222/2),hsv[...,0])
hsv2[...,1]=np.clip(hsv[...,1]*0.95,0,255)
hsv2[...,2]=np.clip(hsv[...,2]*1.05,0,255)
blue=cv2.cvtColor(hsv2.astype(np.uint8),cv2.COLOR_HSV2RGB).astype(np.float32)
# kraft -> white paper keeping shading
lum=(0.299*rgb[...,0]+0.587*rgb[...,1]+0.114*rgb[...,2])
ref=np.percentile(lum[kraft>0.9],60)
w=244*(1-0.55*(1-np.clip(lum/ref,0,1.1)))
white=np.stack([w*0.995,w*0.993,w*0.985],-1)
out=rgb*(1-green[...,None])+blue*green[...,None]
out=out*(1-kraft[...,None])+white*kraft[...,None]
res=np.concatenate([np.clip(out,0,255),al],-1).astype(np.uint8)
img=Image.fromarray(res,'RGBA'); img.save('prodimg/saco-linsoles-blanco.png',optimize=True)
img.resize((img.width//2,img.height//2),Image.LANCZOS).save('prodimg/saco-linsoles-blanco-small.png')
print('ref',ref)
