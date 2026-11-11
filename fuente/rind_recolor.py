import numpy as np, cv2
img=cv2.imread('foto.png'); H,W=img.shape[:2]
ent=cv2.imread('entero.png'); eh,ew=ent.shape[:2]
yy,xx=np.mgrid[:eh,:ew]; r=np.hypot(xx-ew/2,yy-eh/2)
ring=(r>540)&(r<585)
el=cv2.cvtColor(ent,cv2.COLOR_BGR2LAB).astype(np.float32)
tm=np.median(el[ring],0); ts=el[ring].std(0); print('target',tm,ts)
S=1.254
wheel=[(36,380),(48,240),(90,165),(200,120),(420,98),(620,112),(740,155),(788,218),(806,300),(806,432),(755,432),(752,292),(465,226),(518,342),(524,750),(300,758),(100,712),(42,620)]
piece=[(665,430),(952,438),(968,560),(970,790),(905,892),(872,897),(878,515)]
poly=np.zeros((H,W),np.uint8)
for p in (wheel,piece): cv2.fillPoly(poly,[(np.array(p)*S).astype(np.int32)],1)
gm=np.full((H,W),cv2.GC_BGD,np.uint8)
dil=cv2.dilate(poly,np.ones((25,25),np.uint8)); ero=cv2.erode(poly,np.ones((25,25),np.uint8))
gm[dil>0]=cv2.GC_PR_BGD; gm[poly>0]=cv2.GC_PR_FGD; gm[ero>0]=cv2.GC_FGD
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
paste=((hsv[...,2]>130)&(hsv[...,1]<105)).astype(np.uint8)
paste=cv2.morphologyEx(paste,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
n,l,st,_=cv2.connectedComponentsWithStats(paste); keep=[k for k in range(1,n) if st[k,4]>3000]; paste=np.isin(l,keep).astype(np.uint8)
paste=cv2.morphologyEx(paste,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
gm[(paste>0)&(gm!=cv2.GC_BGD)]=cv2.GC_PR_BGD
bg=np.zeros((1,65));fg=np.zeros((1,65))
cv2.grabCut(img,gm,None,bg,fg,5,cv2.GC_INIT_WITH_MASK)
rind=((gm==1)|(gm==3))&(paste==0)
rind=cv2.morphologyEx(rind.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
cv2.imwrite('_rindmask.png',rind*255)
lab=cv2.cvtColor(img,cv2.COLOR_BGR2LAB).astype(np.float32)
src=lab[rind>0]; sm=np.median(src,0); ss=src.std(0); print('src',sm,ss)
new=lab.copy()
new[...,0]=(lab[...,0]-sm[0])*0.9+tm[0]-4
new[...,1]=(lab[...,1]-sm[1])*1.2+tm[1]-6
new[...,2]=(lab[...,2]-sm[2])*1.2+tm[2]-6
rec=cv2.cvtColor(np.clip(new,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR).astype(np.float32)
a=cv2.GaussianBlur(rind.astype(np.float32),(0,0),1.2)[...,None]
out=img*(1-a)+rec*a
cv2.imwrite('queso_corteza.png',np.clip(out,0,255).astype(np.uint8))
