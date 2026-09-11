#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Icones au trait de la section « Chez nous on montre patte blanche ».

POURQUOI CE SCRIPT
Les banques d'icones imposent une licence, un compte, et un style qui n'est pas
le notre. Ces quatre-la sont dessinees ici : libres de droits, a la couleur des
titres du pied de page (#a8ff6a), et regenerables si la charte bouge.

METHODE
Dessin sur une grille de 64x64 unites (celle des SVG au trait), rendu en 2048px
puis reduit a 512 en LANCZOS : c'est ce sur-echantillonnage qui donne un trait
lisse, Pillow ne sachant pas antialiaser une ligne epaisse.

PIEGE SHOPIFY
Ne pas livrer de SVG : le selecteur d'image d'une section de theme n'accepte que
des fichiers image (PNG/JPG/WEBP), un SVG televerse arrive en « fichier
generique » et n'apparait pas dans la liste.

  python scripts/gen_icones.py --dest <dossier>
  python scripts/gen_icones.py --dest <dossier> --couleur 314431 --suffixe fonce
Puis televersement par scripts/upload_images.py (staged_upload + file_create).

VARIANTES
Vert clair #a8ff6a (defaut) : pour un fond vert fonce.
Vert fonce #314431 (--suffixe fonce) : pour une capsule creme — c'est la
version en ligne depuis le 11/09/2026, la page d'accueil reservant le couple
vert fonce / vert clair a l'en-tete et au pied de page.
"""
import argparse, math, os
from PIL import Image, ImageDraw

S, SS = 512, 4
N = S * SS
U = N / 64.0
W = int(round(2.6 * U))
COUL = (168, 255, 106, 255)   # #a8ff6a, modifiable par --couleur
SUFFIXE = ""


def P(x, y):
    return (x * U, y * U)


def poly(d, pts):
    p = [P(*q) for q in pts]
    d.line(p, fill=COUL, width=W, joint="curve")
    r = W / 2.0
    for (x, y) in (p[0], p[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=COUL)


def arc(d, cx, cy, rayon, a0, a1, pas=2):
    pts = [(cx + rayon * math.cos(math.radians(a)), cy + rayon * math.sin(math.radians(a)))
           for a in range(int(a0), int(a1) + 1, pas)]
    poly(d, pts)
    return pts


def rect_arrondi(d, x0, y0, x1, y1, r):
    d.rounded_rectangle([P(x0, y0)[0], P(x0, y0)[1], P(x1, y1)[0], P(x1, y1)[1]],
                        radius=r * U, outline=COUL, width=W)


def bezier(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / float(n)
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


def toile():
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def sauver(img, dest, nom):
    if SUFFIXE:
        racine, ext = os.path.splitext(nom)
        nom = "%s-%s%s" % (racine, SUFFIXE, ext)
    chemin = os.path.join(dest, nom)
    img.resize((S, S), Image.LANCZOS).save(chemin, "PNG", optimize=True)
    return chemin


def service_client(dest):
    img, d = toile()
    arc(d, 32, 33, 18, 180, 360)
    rect_arrondi(d, 8, 33, 19, 48, 4)
    rect_arrondi(d, 45, 33, 56, 48, 4)
    poly(d, [(50.5, 48), (50.5, 52)] + bezier((50.5, 52), (50.5, 57), (45, 57.5), (38, 57.5)))
    return sauver(img, dest, "gf-icone-service-client.png")


def expedition(dest):
    img, d = toile()
    poly(d, [(9, 20), (32, 10), (55, 20), (55, 44), (32, 54), (9, 44), (9, 20)])
    poly(d, [(9, 20), (32, 30), (55, 20)])
    poly(d, [(32, 30), (32, 54)])
    poly(d, [(20.5, 15), (43.5, 25), (43.5, 33)])
    return sauver(img, dest, "gf-icone-expedition.png")


def retractation(dest):
    """Fleche circulaire. La pointe est calculee sur la tangente du dernier
       point de l'arc : dessinee « a la main », elle tombait de travers."""
    img, d = toile()
    cx, cy, R, a0, a1 = 32, 33, 19, -70, 250
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a)))
           for a in range(a1, a0 - 1, -2)]
    poly(d, pts)
    ax, ay = pts[-1]
    tang = math.radians(a0 - 90)
    for dev in (150, -150):
        ang = tang + math.radians(dev)
        poly(d, [(ax, ay), (ax + 7.0 * math.cos(ang), ay + 7.0 * math.sin(ang))])
    return sauver(img, dest, "gf-icone-retractation.png")


def conseils(dest):
    img, d = toile()
    gauche = (bezier((32, 18), (24, 13), (15, 12), (8, 13))
              + bezier((8, 13), (8, 30), (8, 36), (8, 47))[1:]
              + bezier((8, 47), (16, 47), (25, 49), (32, 53))[1:])
    poly(d, gauche)
    poly(d, [(64 - x, y) for (x, y) in gauche])
    poly(d, [(32, 18), (32, 53)])
    return sauver(img, dest, "gf-icone-conseils.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", required=True, help="dossier de sortie")
    ap.add_argument("--couleur", default="a8ff6a", help="couleur du trait, hexa sans #")
    ap.add_argument("--suffixe", default="", help="ajoute au nom de fichier (ex. fonce)")
    a = ap.parse_args()
    global COUL, SUFFIXE
    h = a.couleur.lstrip("#")
    COUL = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
    SUFFIXE = a.suffixe
    os.makedirs(a.dest, exist_ok=True)
    for f in (service_client, expedition, retractation, conseils):
        print("OK", f(a.dest))


if __name__ == "__main__":
    main()
