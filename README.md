# OcoteWorks

Sitio web de [ocoteworks.com](https://ocoteworks.com). Publicado con GitHub Pages desde la rama `main`.

- `/` — inglés (versión principal)
- `/es/` — español

## Editar el sitio

Los textos de los dos idiomas viven en `src/build.py` (diccionarios `EN` y `ES`). La estructura está en `src/page.html` y los estilos en `src/styles.css`. Después de editar:

```
python3 src/build.py
```

Eso regenera `index.html`, `es/index.html`, `assets/styles.css` y `sitemap.xml`.

Tipografías: kit de Adobe Fonts `atu2ijd` (Dharma Gothic E, DIN 2014, IBM Plex Mono), autorizado para ocoteworks.com, www.ocoteworks.com y manuelgf10.github.io.
