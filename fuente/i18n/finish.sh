set -e
cd /tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad
python3 build_static.py >/dev/null
rm -f Web_Plataforma_Lactea/img/banner0?.jpg Web_Plataforma_Lactea/img/cisterna.png Web_Plataforma_Lactea/img/amf.png
python3 deploy/deploy_prep.py form
python3 i18n/build_i18n.py
python3 deploy/deploy_prep.py post
cp i18n/fichas/*.pdf Web_Plataforma_Lactea/fichas/
cp catalogos/Catalogo_*_EN.pdf catalogos/Catalogo_*_FR.pdf catalogos/Catalogo_*_PT.pdf Web_Plataforma_Lactea/catalogos/
for L in en fr pt; do for n in industrial retail; do for f in catalogos/cat-$n-*-$L.jpg; do i=$(basename $f .jpg | sed "s/cat-$n-//; s/-$L//"); cp $f Web_Plataforma_Lactea/img/catalogo-$n-$i-$L.jpg; done; done; done
python3 deploy/optimize.py
python3 i18n/make_spa_i18n.py
