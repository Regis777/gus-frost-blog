# -*- coding: utf-8 -*-
"""Construction de balises <img> optimisées pour le CDN Shopify.
Le CDN redimensionne + sert en WebP dès qu'on ajoute ?width=N (vérifié : hero PNG
1,8 Mo -> WebP 61 Ko à width=1100). On émet donc src + srcset multi-largeurs + sizes,
width/height (ratio réel, anti-CLS), et lazy/eager selon hero.
Conteneur article = .gf-article max-width 760px (~740px utile) -> sizes calibré dessus.
"""
import struct

WIDTHS = [400, 600, 800, 1200, 1536]
SIZES = "(max-width: 760px) 100vw, 740px"
SRC_DEFAULT = 1100  # largeur du src de repli (navigateurs sans srcset)


def png_dims(path):
    """(w, h) d'un PNG via l'entête IHDR, sans dépendance externe. None si échec."""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
    except OSError:
        pass
    return None


def _with_width(base, w):
    return base + ("&amp;" if "?" in base else "?") + "width=%d" % w


def build_img(base_url, alt, dims=None, hero=False):
    """Balise <img> optimisée. base_url = URL CDN (avec ?v=...). dims=(w,h) ou None."""
    native_w = dims[0] if dims else max(WIDTHS)
    caps = sorted({w for w in WIDTHS if w < native_w} | {native_w})
    srcset = ", ".join("%s %dw" % (_with_width(base_url, w), w) for w in caps)
    src = _with_width(base_url, min(SRC_DEFAULT, native_w))
    load = 'loading="eager" fetchpriority="high"' if hero else 'loading="lazy"'
    dim = (' width="%d" height="%d"' % (dims[0], dims[1])) if dims else ""
    return ('<img src="%s" srcset="%s" sizes="%s"%s %s decoding="async" alt="%s">'
            % (src, srcset, SIZES, dim, load, alt))
