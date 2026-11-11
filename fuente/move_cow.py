import numpy as np, cv2
img=cv2.imread('webactual/banner03.jpg'); H,W=img.shape[:2]
f=img.astype(np.int32); b,g,r=f[...,0],f[...,1],f[...,2]
HZ=392
sky=(b-r>14)&(np.arange(H)[:,None]<HZ+8)
grass=(g-r>8)&(g-b>8)&(np.arange(H)[:,None]>HZ-10)
box=np.zeros((H,W),bool); box[105:H,820:1185]=True
cand=box&~sky&~grass
cand=cv2.morphologyEx(cand.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(cand); k=1+np.argmax(st[1:,4]); col=(lab==k).astype(np.uint8)
# grabcut refine from color mask
gm=np.full((H,W),cv2.GC_BGD,np.uint8)
gm[box]=cv2.GC_PR_BGD
gm[(col>0)]=cv2.GC_PR_FGD
gm[cv2.erode(col,np.ones((9,9),np.uint8))>0]=cv2.GC_FGD
gm[box&sky&~(cv2.dilate(col,np.ones((5,5),np.uint8))>0)]=cv2.GC_BGD
bgd=np.zeros((1,65)); fgd=np.zeros((1,65))
cv2.grabCut(img,gm,None,bgd,fgd,5,cv2.GC_INIT_WITH_MASK)
cow=((gm==1)|(gm==3)).astype(np.uint8)
n,lab,st,_=cv2.connectedComponentsWithStats(cow); k=1+np.argmax(st[1:,4]); cow=(lab==k).astype(np.uint8)
cow=cv2.morphologyEx(cow,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
# lower body/legs: everything that is not grass-coloured
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV); Hh,Ss,Vv=hsv[...,0],hsv[...,1],hsv[...,2]
grass2=(Hh>=20)&(Hh<=55)&(Ss>45)&(Vv>60)
low=(box&~grass2).astype(np.uint8)
low=cv2.morphologyEx(low,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(cow); k=1+np.argmax(st[1:,4]); cow=(lab==k).astype(np.uint8)
row=np.where(cow[HZ-28]>0)[0]; cl,cr=row.min(),row.max()
cow[HZ-12:,:cl-4]=0; cow[HZ-12:,cr+5:]=0
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV); Hh,Ss,Vv=hsv[...,0],hsv[...,1],hsv[...,2]
grass2=(Hh>=24)&(Hh<=55)&(Ss>55)&(Vv>60)
legs=np.zeros((H,W),np.uint8); legs[HZ+6:520,cl-6:cr+8]=1
legs=(legs>0)&~grass2
legs=cv2.morphologyEx(legs.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
legs=cv2.morphologyEx(legs,cv2.MORPH_CLOSE,np.ones((15,5),np.uint8))
cow[HZ+6:]=0
cow=np.maximum(cow,legs)
cow=cv2.morphologyEx(cow,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(cow); keep=[k for k in range(1,n) if st[k,4]>120]; cow=np.isin(lab,keep).astype(np.uint8)
ys,xs=np.where(cow); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max(); print('bbox',x0,x1,y0,y1)
cv2.imwrite('webactual/_cowmask.png',cow*255)
# clean background
bg=img.copy()
for x in range(820,1064): bg[:,x]=img[:,1640-x]
for x in range(1064,1174): bg[:,x]=img[:,min(W-1,2344-x)]
w_=np.linspace(0,1,30)[None,:,None]
left=np.stack([img[:,1640-x] for x in range(1050,1080)],1).astype(np.float32)
right=np.stack([img[:,min(W-1,2344-x)] for x in range(1050,1080)],1).astype(np.float32)
bg[:,1050:1080]=(left*(1-w_)+right*w_).astype(np.uint8)
# remove mirrored dry bush
hs=cv2.cvtColor(bg,cv2.COLOR_BGR2HSV)
bush=((hs[...,0]<24)|(hs[...,1]<50)).astype(np.uint8); reg=np.zeros_like(bush); reg[405:H,960:1090]=1; bush=bush&reg
bush=cv2.dilate(cv2.morphologyEx(bush,cv2.MORPH_OPEN,np.ones((3,3),np.uint8)),np.ones((9,9),np.uint8))
shifted=np.roll(bg,-110,axis=1)
bm=cv2.GaussianBlur(cv2.dilate(bush,np.ones((7,7),np.uint8)).astype(np.float32),(0,0),6)[...,None]
bg=(bg*(1-bm)+shifted*bm).astype(np.uint8)
big=cv2.GaussianBlur(cv2.dilate(cow,np.ones((25,25),np.uint8)).astype(np.float32),(0,0),5)[...,None]
base=img*(1-big)+bg*big
# small cow far away
s=0.48
crop=img[y0:y1+1,x0:x1+1]; cm=cow[y0:y1+1,x0:x1+1].astype(np.float32)
cw,ch=int(crop.shape[1]*s),int(crop.shape[0]*s)
crop=cv2.resize(crop,(cw,ch),interpolation=cv2.INTER_AREA).astype(np.float32)
cm=cv2.resize(cm,(cw,ch),interpolation=cv2.INTER_AREA)
# atmospheric perspective: slight haze toward sky color
haze=np.array([225,215,205],np.float32); crop=crop*0.9+haze*0.1
px=W-cw-60; feet=HZ+40; py=feet-ch
a=cv2.GaussianBlur(cm,(0,0),1.2)[...,None]
lowfeather=np.ones_like(a); hb=int((HZ+6-y0)*s)
if 0<hb<ch:
    fade=np.clip((np.arange(ch)-hb)/max(1,ch-hb),0,1)[:,None,None]
    edge=np.minimum(np.clip(np.arange(cw)/8,0,1),np.clip((cw-1-np.arange(cw))/8,0,1))[None,:,None]
    lowfeather=np.ones_like(a)
a=a*lowfeather
reg=base[py:py+ch,px:px+cw]; base[py:py+ch,px:px+cw]=reg*(1-a)+crop*a
# soft shadow
sh=np.zeros((H,W),np.float32); cv2.ellipse(sh,(px+cw//2,feet-2),(cw//2,6),0,0,360,1,-1); sh=cv2.GaussianBlur(sh,(0,0),4)[...,None]*0.25
base=base*(1-sh)
res=np.clip(base,0,255).astype(np.uint8)
cv2.imwrite('webactual/banner03_moved.jpg',res)
