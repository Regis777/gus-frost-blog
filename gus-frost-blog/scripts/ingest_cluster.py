#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ingestion GÉNÉRIQUE d'un cluster produit (dossier Cowork) vers le repo, prêt à déployer.
Encode le staging standard, pour n'avoir RIEN à refaire à la main d'un cluster à l'autre.

À partir d'un dossier source (production Cowork) contenant :
  - articles/cluster-N-<tag>/AAAA-MM-JJ_(PILIER|SATxx)_<slug>_v1.html   (fragments datés)
  - images/1.png … K.png                                                (ordre de création)
  - manifest_C<N>_rows.csv                                              (méta validées)
  - C<N>_prompts_images.md  (optionnel)
… produit dans le repo :
  - articles/cluster-N-<tag>/<slug>.html            (fragments renommés en slug)
  - articles/cluster-N-<tag>/C<N>_images_map.csv    (num, fichier_origine, nouveau_fichier, article_slug, type, role, alt)
  - articles/cluster-N-<tag>/manifest_C<N>_rows.csv (aligné : type PILIER/SATxx, file=chemin repo)
  - images/cluster-N-<tag>/<nouveau_fichier>.png    (hero-<slug>.png / <slug>-n.png)
  - manifest.csv  (append-only des N lignes si absentes)

Le mapping images vient des marqueurs « Image N » présents dans les fragments (clé robuste),
role=hero pour la 1re figure de chaque article, alt = description du marqueur.

--blog chats bascule sur le manifest chat (manifest_chat.csv, créé au besoin) et accepte
la nomenclature Cowork « CH<N>_… » des dossiers chat en plus de « C<N>_… ».

Usage :
  python scripts/ingest_cluster.py --cluster 8 --src "/chemin/vers/C8-<tag>"          # PLAN (aucune écriture)
  python scripts/ingest_cluster.py --cluster 8 --src "/chemin/vers/C8-<tag>" --apply  # exécute le staging
  python scripts/ingest_cluster.py --cluster 10 --src "…/CH10-cohabitation" --blog chats --apply
"""
import argparse, csv, glob, io, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import blog_conf, ensure_manifest                            # noqa: E402

HDR = ["cluster_num", "cluster_tag", "type", "slug", "parent_pilier_slug", "title",
       "meta_title", "meta_description", "excerpt", "tags", "file", "prompts_file",
       "links_to_resolve", "images_to_resolve"]
FIG = re.compile(r'<div class="gf-imgph">\s*Image\s*(\d+)\s*-\s*(.*?)</div>', re.S)
FRAG = re.compile(r'_(PILIER|SAT\d+)_(.+?)_v\d+\.html$', re.I)


def find_fragdir(src, n):
    cand = sorted(glob.glob(os.path.join(src, "articles", "cluster-%d-*" % n)))
    if cand:
        return cand[0]
    # sinon : fragments datés directement sous src
    if glob.glob(os.path.join(src, "*_v*.html")):
        return src
    sys.exit("Fragments datés introuvables sous %s" % src)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", type=int, required=True)
    ap.add_argument("--src", required=True, help="dossier de production Cowork du cluster")
    ap.add_argument("--apply", action="store_true", help="exécute (sinon : plan seul)")
    ap.add_argument("--blog", default=None,
                    help="blog cible : chiens (défaut) ou chats. Choisit le manifest.")
    args = ap.parse_args()
    N = args.cluster
    conf = blog_conf(args.blog)
    src = args.src
    fragdir = find_fragdir(src, N)
    tag = os.path.basename(fragdir).split("cluster-%d-" % N)[-1] if "cluster-%d-" % N in fragdir else None

    # fragments datés -> type + slug
    frags = {}
    for fn in os.listdir(fragdir):
        m = FRAG.search(fn)
        if m:
            frags[m.group(2)] = (fn, m.group(1).upper())
    if not frags:
        sys.exit("Aucun fragment daté reconnu dans %s" % fragdir)
    if tag is None:
        tag = "cluster%d" % N

    # Les dossiers Cowork du blog chat préfixent « CH<N> » là où le chien écrit
    # « C<N> » : on accepte les deux nomenclatures.
    pref = "CH" if conf["handle"] == "chats" else "C"

    def find_one(template):
        # template porte un « {p} » pour le préfixe ; on essaie celui du blog d'abord.
        for p in (pref, "C", "CH"):
            hit = glob.glob(os.path.join(src, "**", template.format(p=p, n=N)), recursive=True)
            if hit:
                return hit[0]
        return None

    # méta depuis manifest_C<N>_rows.csv (ou manifest_CH<N>_rows.csv)
    mman = find_one("manifest_{p}{n}_rows.csv")
    if not mman:
        sys.exit("manifest_%s%d_rows.csv introuvable sous %s" % (pref, N, src))
    meta = {r["slug"]: r for r in csv.DictReader(open(mman, encoding="utf-8-sig"))}

    # prompts (optionnel)
    prompts = find_one("{p}{n}_prompts_images.md")
    prompts_name = "PROMPTS-IMAGES_%s%d_%s.md" % (pref, N, tag)

    # cibles repo
    ARTDST = os.path.join(ROOT, "articles", "cluster-%d-%s" % (N, tag))
    IMGDST = os.path.join(ROOT, "images", "cluster-%d-%s" % (N, tag))
    srcimg = None
    for c in (os.path.join(src, "images"), src):
        if glob.glob(os.path.join(c, "*.png")):
            srcimg = c; break

    # ordre de traitement : pilier puis satellites (ordre manifest)
    order = sorted(meta.keys(), key=lambda s: (0 if frags.get(s, ("", ""))[1] == "PILIER" else 1, s))

    # construire images_map depuis les marqueurs des fragments
    maprows = []
    for slug in order:
        fn = frags[slug][0]
        body = open(os.path.join(fragdir, fn), encoding="utf-8").read()
        figs = FIG.findall(body)  # [(num, desc), ...]
        for i, (num, desc) in enumerate(figs):
            desc = re.sub(r"\s+", " ", desc).strip()
            role = "hero" if i == 0 else "secondaire"
            new = ("hero-%s.png" % slug) if i == 0 else ("%s-%d.png" % (slug, i + 1))
            alt = (desc[:1].upper() + desc[1:]).rstrip(".") + "."
            typ = frags[slug][1]
            maprows.append({"num": int(num), "fichier_origine": "%s.png" % num,
                            "nouveau_fichier": new, "article_slug": slug,
                            "type": typ, "role": role, "alt": alt})
    maprows.sort(key=lambda r: r["num"])

    # lignes manifest alignées
    aligned = []
    for slug in order:
        r = meta[slug]; typ = frags[slug][1]
        r = dict(r)
        r["type"] = typ
        r["file"] = "articles/cluster-%d-%s/%s.html" % (N, tag, slug)
        r["prompts_file"] = prompts_name
        aligned.append([r.get(c, "") for c in HDR])

    # plan / exécution
    print("=" * 74)
    print("INGEST %s%d (tag=%s) | blog «%s» | %s"
          % (pref, N, tag, conf["handle"], "APPLY" if args.apply else "PLAN (aucune écriture)"))
    print("  fragments : %d | images (marqueurs) : %d | source images : %s"
          % (len(frags), len(maprows), srcimg or "—"))
    print("  cible articles : %s" % os.path.relpath(ARTDST, ROOT))
    print("  cible images   : %s" % os.path.relpath(IMGDST, ROOT))
    print("  manifest       : %s" % conf["manifest"])
    dup = []
    man = conf["manifest_path"]          # créé au moment d'écrire (le PLAN n'écrit rien)
    existing = set()
    if os.path.exists(man):
        existing = {r["slug"] for r in csv.DictReader(open(man, encoding="utf-8-sig"))}
    dup = [s for s in order if s in existing]
    print("  %-14s %s" % (conf["manifest"] + " :",
                          "déjà présent (%d slugs) -> pas de ré-append" % len(dup) if dup
                          else "+%d lignes en append-only" % len(aligned)))
    miss_img = [r["num"] for r in maprows if srcimg and not os.path.exists(os.path.join(srcimg, "%d.png" % r["num"]))]
    if miss_img:
        print("  ⚠ images source manquantes : %s" % miss_img)
    if not args.apply:
        print("\nPLAN uniquement. Relancer avec --apply pour écrire.")
        return

    os.makedirs(ARTDST, exist_ok=True); os.makedirs(IMGDST, exist_ok=True)
    for slug in order:
        shutil.copy(os.path.join(fragdir, frags[slug][0]), os.path.join(ARTDST, slug + ".html"))
    with open(os.path.join(ARTDST, "%s%d_images_map.csv" % (pref, N)), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["num", "fichier_origine", "nouveau_fichier",
                                          "article_slug", "type", "role", "alt"])
        w.writeheader(); [w.writerow(x) for x in maprows]
    for r in maprows:
        s = os.path.join(srcimg, "%d.png" % r["num"])
        if os.path.exists(s):
            shutil.copy(s, os.path.join(IMGDST, r["nouveau_fichier"]))
    with open(os.path.join(ARTDST, "manifest_%s%d_rows.csv" % (pref, N)), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(HDR); [w.writerow(x) for x in aligned]
    if prompts:
        shutil.copy(prompts, os.path.join(ARTDST, prompts_name))
    if not dup:
        raw = open(ensure_manifest(man), encoding="utf-8").read()
        if not raw.endswith("\n"): raw += "\n"
        sio = io.StringIO(); w = csv.writer(sio); [w.writerow(x) for x in aligned]
        open(man, "w", encoding="utf-8").write(raw + sio.getvalue())
    blogopt = "" if conf["handle"] == "chiens" else " --blog %s" % conf["handle"]
    print("\nStaging terminé. Vérifier : python scripts/check_cluster.py "
          "--dir articles/cluster-%d-%s --faq 5%s" % (N, tag, blogopt))
    print("Puis : python deploy/deploy_cluster.py --cluster %d --tag %s%s --dry-run"
          % (N, tag, blogopt))


if __name__ == "__main__":
    main()
