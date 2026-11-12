#!/bin/bash
# Reconstruye la web, la copia al repositorio y la publica (GitHub sube al hosting por FTPS).
set -e
S=/tmp/claude-0/-home-claude/fd2192db-e962-524a-b2a2-31b0b87be078/scratchpad
R=/home/claude/noticias
MSG="${1:-Actualización de la web}"
cd $R && git pull -q
cp -a $S/Web_Plataforma_Lactea/. $R/sitio/ && rm -f $R/sitio/web.html
cp $S/deploy/*.py $S/deploy/*.sh $S/deploy/*.php $S/deploy/*.css $R/fuente/deploy/ 2>/dev/null || true
cp -a $S/web/project/. $R/fuente/web/project/
cp $S/i18n/*.py $S/i18n/*.sh $R/fuente/i18n/
cp $S/blog_src/noticias.json $R/noticias.json 2>/dev/null || true
date -u +"%Y-%m-%d %H:%M UTC" > $R/sitio/version.txt
cd $R && git add -A && git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01B2imM6iRWCdvVhKN6YyNdZ" && git push -q origin main && git log --oneline -1
