# Plataforma Interprofesional Láctea — web y noticias

- `sitio/` — la web tal como se publica en https://www.plataformalactea.com (4 idiomas). Lo que hay aquí es lo que se sube al hosting.
- `fuente/` — archivos de trabajo: páginas de diseño (`fuente/web/project`), traducciones (`fuente/i18n`), generador del blog (`fuente/deploy/blog_week.py`), catálogos, fichas e imágenes originales.
- `noticias.json` — datos del blog.

Reconstruir la web: `bash fuente/i18n/finish.sh` (las rutas de los scripts apuntan al espacio de trabajo original; ajustarlas si se usan en otro sitio).
