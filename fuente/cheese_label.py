import numpy as np, cv2, sys
D=sys.argv[1]
img=cv2.imread(D+'/foto.png'); H,W=img.shape[:2]
lab=cv2.imread(D+'/etiqueta.png',cv2.IMREAD_UNCHANGED)
if lab.shape[2]==3: lab=np.dstack([lab,np.full(lab.shape[:2],255,np.uint8)])
lh,lw=lab.shape[:2]
circ=np.zeros((lh,lw),np.uint8); cv2.circle(circ,(lw//2,lh//2),min(lw,lh)//2-6,255,-1,cv2.LINE_AA)
lab[...,3]=np.minimum(lab[...,3],circ)
cx0,cy0,a,b=532,296,462,172; s=0.70
cx=cx0-0.20*a; cy=cy0-0.20*b
M=np.float32([[a*s*2/lw,0,cx-a*s],[0,b*s*2/lh,cy-b*s]])
warp=cv2.warpAffine(lab,M,(W,H),flags=cv2.INTER_AREA,borderValue=(0,0,0,0)).astype(np.float32)
alpha=warp[...,3:4]/255
# exclude cut paste face
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
paste=((hsv[...,2]>150)&(hsv[...,1]<110)).astype(np.uint8)
paste=cv2.morphologyEx(paste,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
n,l,st,_=cv2.connectedComponentsWithStats(paste); keep=[k for k in range(1,n) if st[k,4]>3000]; paste=np.isin(l,keep).astype(np.uint8)
paste=cv2.dilate(paste,np.ones((3,3),np.uint8))
pm=cv2.GaussianBlur(paste.astype(np.float32),(0,0),1.0)[...,None]
alpha=alpha*(1-pm)
# shading from rind luminance (very soft) + slight warm tint
lum=cv2.GaussianBlur(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32),(0,0),25)[...,None]
ref=np.percentile(lum[alpha[...,0]>0.5],60)
fac=np.clip(0.88+0.12*lum/ref,0.85,1.03)
col=warp[...,:3]*fac
# drop shadow of label edge (thin paper)
sh=cv2.GaussianBlur(alpha,(0,0),3)[...,None] if alpha.ndim==2 else cv2.GaussianBlur(alpha[...,0],(0,0),3)[...,None]
out=img.astype(np.float32)*(1-0.25*np.clip(sh-alpha,0,1))
out=out*(1-alpha)+col*alpha
cv2.imwrite(D+'/queso_linsoles.png',np.clip(out,0,255).astype(np.uint8))
