import sys, io, pypdf
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
LOGO='prodimg/logo-linsoles-web.png'
def stamp(src,dst,right=545,top=14,h=44):
    r=pypdf.PdfReader(src); w=pypdf.PdfWriter()
    for i,p in enumerate(r.pages):
        if i==0:
            W=float(p.mediabox.width); H=float(p.mediabox.height)
            buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(W,H))
            img=ImageReader(LOGO); iw,ih=img.getSize(); lw=h*iw/ih
            c.drawImage(img,right-lw,H-top-h,width=lw,height=h,mask='auto'); c.save()
            p.merge_page(pypdf.PdfReader(buf).pages[0])
        w.add_page(p)
    w.add_metadata(r.metadata or {}); w.write(dst)
stamp(sys.argv[1],sys.argv[2])
