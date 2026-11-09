# OcoteWorks

Sitio web de [ocoteworks.com](https://ocoteworks.com). Publicado con GitHub Pages desde la rama `main`.

| Página | EN | ES |
|---|---|---|
| Inicio | `/` | `/es/` |
| Servicios | `/services/` | `/es/servicios/` |
| Productos (en construcción) | `/products/` | `/es/productos/` |
| Sobre mí | `/about/` | `/es/sobre-mi/` |
| Bitácora (en construcción) | `/journal/` | `/es/bitacora/` |
| Cotizador | `/quote/` | `/es/cotizar/` |

## Editar el sitio

Los textos de los dos idiomas viven en `src/build.py` (diccionarios `EN` y `ES`). Plantillas en `src/` (home, services, soon, quote, about); cabecera y pie comunes en `header()` / `footer()` de `build.py`; estilos en `src/styles.css`. Después de editar:

```
python3 src/build.py
```

Eso regenera `index.html`, `es/index.html`, `assets/styles.css` y `sitemap.xml`.

Tipografías: kit de Adobe Fonts `atu2ijd` (Dharma Gothic E, DIN 2014, IBM Plex Mono), autorizado para ocoteworks.com, www.ocoteworks.com y manuelgf10.github.io.

## Cotizador

Precios (MXN antes de IVA), tiempos, opciones y paquetes predefinidos viven en el bloque `OW_QUOTE` al inicio de `src/quote.js`. Los textos fijos de la página están en `build.py` (claves `q_*`). Después de editar, corre `python3 src/build.py`.

La solicitud se envía abriendo el correo del cliente hacia hola@ocoteworks.com con el resumen y un link que reconstruye su configuración exacta.
