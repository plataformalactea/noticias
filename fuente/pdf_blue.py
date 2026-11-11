import pypdf,re,sys
from pypdf.generic import NameObject, DecodedStreamObject
src,dst=sys.argv[1],sys.argv[2]
r=pypdf.PdfReader(src); w=pypdf.PdfWriter(); n=0
pat=re.compile(rb'0?\.9[67]\d* 0?\.79\d* 0?\.67\d* (rg|scn|sc)')
for p in r.pages:
    d=p.get_contents().get_data()
    d,k=pat.subn(lambda m:b'.851 .886 .953 '+m.group(1),d); n+=k
    w.add_page(p); s=DecodedStreamObject(); s.set_data(d); w.pages[-1][NameObject('/Contents')]=w._add_object(s)
w.add_metadata(r.metadata or {}); w.write(dst); print(dst,n)
