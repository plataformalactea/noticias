import numpy as np, cv2
img=cv2.imread('/mnt/user-data/attachments/fd2192db-e962-524a-b2a2-31b0b87be078/c986067b-image.png')
m=cv2.imread('webactual/_cows3mask.png',0)>0
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV); h,s,v=[hsv[...,i].astype(int) for i in range(3)]
ys=np.arange(img.shape[0])[:,None]
green=(h>=28)&(h<=60)&(s>50)&(v>75)&(ys>300)
m=m&~green
legs=np.zeros_like(m); legs[295:384,74:665]=True
nong=((s<45)|(v<85)|(h<22)|(h>90))&~green
legs=cv2.morphologyEx((legs&nong).astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
legs=cv2.morphologyEx(legs,cv2.MORPH_CLOSE,np.ones((9,3),np.uint8))
n2,l2,st2,_=cv2.connectedComponentsWithStats(legs)
for k in range(1,n2):
    if st2[k,4]<60: legs[l2==k]=0
m=m|(legs>0)
m=cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(m); keep=[k for k in range(1,n) if st[k,4]>400]; m=np.isin(lab,keep).astype(np.uint8)
ys_,xs_=np.where(m); x0,x1,y0,y1=xs_.min(),xs_.max(),ys_.min(),ys_.max()
crop=img[y0:y1+1,x0:x1+1].astype(np.float32); cm=m[y0:y1+1,x0:x1+1].astype(np.float32)
base=cv2.imread('webactual/banner03_nocow.jpg').astype(np.float32); H,W=base.shape[:2]
S=0.62
cw,ch=int(crop.shape[1]*S),int(crop.shape[0]*S)
crop=cv2.resize(crop,(cw,ch),interpolation=cv2.INTER_AREA); cm=cv2.resize(cm,(cw,ch),interpolation=cv2.INTER_AREA)
# match lighting a bit to banner (slightly cooler, haze)
crop=crop*0.93+np.array([225,215,205],np.float32)*0.07
a=cv2.GaussianBlur(cm,(0,0),0.8)[...,None]
px=W-cw-95; feet=478; py=feet-ch
# shadows under each animal
sh=np.zeros((H,W),np.float32)
for fx,fw in [(0.22,0.17),(0.52,0.20),(0.82,0.16)]:
    cv2.ellipse(sh,(px+int(cw*fx),feet-4),(int(cw*fw),7),0,0,360,1,-1)
sh=cv2.GaussianBlur(sh,(0,0),5)[...,None]*0.28
base=base*(1-sh)
reg=base[py:py+ch,px:px+cw]; base[py:py+ch,px:px+cw]=reg*(1-a)+crop*a
# grass blades over hooves: re-blend bottom strip with original banner grass texture
strip=6
g=cv2.imread('webactual/banner03_nocow.jpg').astype(np.float32)
fade=np.clip((np.arange(ch)-(ch-strip-6))/strip,0,1)[:,None,None]*0.6
reg=base[py:py+ch,px:px+cw]; base[py:py+ch,px:px+cw]=reg*(1-fade*a)+g[py:py+ch,px:px+cw]*(fade*a)
cv2.imwrite('webactual/banner03_moved.jpg',np.clip(base,0,255).astype(np.uint8))
print(px,py,cw,ch)
