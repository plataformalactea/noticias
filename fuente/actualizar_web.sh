#!/bin/bash
# Reconstruye la web completa desde fuente/ y deja el resultado en sitio/.
# Uso (desde cualquier carpeta):  bash fuente/actualizar_web.sh
# Después: git add -A && git commit && git push  → GitHub la sube sola al hosting.
set -e
W=$(cd "$(dirname "$0")/.." && pwd)
OLD=/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad   # ruta que usan los scripts
if [ ! -e "$OLD" ]; then mkdir -p "$(dirname "$OLD")"; ln -s "$W/fuente" "$OLD"; fi
if [ "$(readlink -f "$OLD")" != "$(readlink -f "$W/fuente")" ]; then echo "La ruta $OLD ya existe y no apunta a $W/fuente"; exit 1; fi
cd "$OLD"
python3 deploy/blog_week.py
bash i18n/finish.sh > /dev/null
rm -f Web_Plataforma_Lactea/web.html
cp -a Web_Plataforma_Lactea/. "$W/sitio/"
date -u +"%Y-%m-%d %H:%M UTC" > "$W/sitio/version.txt"
cp blog_src/noticias.json "$W/noticias.json"
echo "web reconstruida en $W/sitio"
