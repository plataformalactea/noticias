#!/bin/bash
# Reconstruye la web completa desde fuente/ y deja el resultado en sitio/.
# Uso (desde cualquier carpeta):  bash fuente/actualizar_web.sh
# Después: git add -A && git commit && git push  → GitHub la sube sola al hosting.
set -e
W=$(cd "$(dirname "$0")/.." && pwd)
export PIL_FUENTE="$W/fuente"
cd "$PIL_FUENTE"
python3 deploy/blog_week.py
bash i18n/finish.sh > /dev/null
rm -f Web_Plataforma_Lactea/web.html
cp -a Web_Plataforma_Lactea/. "$W/sitio/"
date -u +"%Y-%m-%d %H:%M UTC" > "$W/sitio/version.txt"
cp blog_src/noticias.json "$W/noticias.json"
echo "web reconstruida en $W/sitio"
