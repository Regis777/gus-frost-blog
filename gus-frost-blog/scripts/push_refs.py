#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
push_refs.py : pousse le bloc « Sources et références » (<aside class="gf-refs">) des
articles du repo vers les articles Shopify EN LIGNE, en ne modifiant QUE body_html.

Pourquoi un script dédié : deploy_cluster.py rebâtit tout le corps (images, placeholders,
FAQ) et exige images/ + *images_map.csv, absents pour plusieurs clusters. Ici on part du
corps en ligne, on y insère ou remplace le bloc gf-refs pris dans articles/<dossier>/<slug>.html,
et on renvoie le corps. Statut de publication, titre, tags, métas, image à la une : intouchés.

  python scripts/push_refs.py --blog chats                       # dry-run, tous les clusters chat
  python scripts/push_refs.py --blog chiens --dir cluster-1-anxiete-separation
  python scripts/push_refs.py --blog chats --dir cluster-19-chaton-socialisation-chat --apply
  python scripts/push_refs.py --blog chiens --slug anxiete-separation-chien --apply

Sortie : une ligne par article : INSERT (bloc ajouté), REPLACE (bloc existant remplacé),
IDENTIQUE (déjà à jour), SANS-BLOC (le fichier repo n'a pas de bloc : ignoré),
ABSENT-SHOPIFY (article introuvable en ligne), ERREUR (pas de </article> dans le corps en ligne).
Rien n'est écrit sans --apply.
"""
import argparse, csv, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from publish import load_env, Shopify, blog_conf, read_manifest   # noqa: E402

RE_BLOCK = re.compile(r'\s*<aside class="gf-refs">.*?</aside>\s*', re.S)


def local_block(path):
    t = open(path, encoding="utf-8").read()
    m = RE_BLOCK.search(t)
    return m.group(0).strip() if m else None


def merge(live, block):
    """Retourne (nouveau corps, action)."""
    if RE_BLOCK.search(live):
        new = RE_BLOCK.sub("\n" + block + "\n", live, count=1)
        return new, ("IDENTIQUE" if new == live else "REPLACE")
    i = live.rfind("</article>")
    if i < 0:
        return live, "ERREUR"
    new = live[:i].rstrip("\n") + "\n" + block + "\n" + live[i:]
    return new, "INSERT"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", required=True, help="chiens ou chats")
    ap.add_argument("--dir", help="dossier articles/<dir> à traiter (ex. cluster-1-langage-chat)")
    ap.add_argument("--slug", help="un seul slug")
    ap.add_argument("--apply", action="store_true", help="écrit sur Shopify (sinon dry-run)")
    ap.add_argument("--sleep", type=float, default=0.6, help="pause entre appels API (s)")
    a = ap.parse_args()

    conf = blog_conf(a.blog)
    rows = read_manifest(conf["manifest_path"])
    if a.dir:
        rows = [r for r in rows if r["file"].replace(os.sep, "/").startswith("articles/%s/" % a.dir)]
    if a.slug:
        rows = [r for r in rows if r["slug"] == a.slug]
    if not rows:
        sys.exit("Aucune ligne de manifest ne correspond.")

    sh = Shopify(load_env())
    blog_id = sh.find_blog_id(conf["handle"])
    print("Blog %s (%s) : %d articles à examiner, mode %s" % (conf["handle"], blog_id, len(rows),
          "APPLY" if a.apply else "DRY-RUN"))
    stats = {}
    for r in rows:
        path = os.path.join(ROOT, r["file"])
        block = local_block(path) if os.path.exists(path) else None
        if not block:
            act = "SANS-BLOC"
        else:
            art = sh.find_article(blog_id, r["slug"])
            if not art:
                act = "ABSENT-SHOPIFY"
            else:
                new, act = merge(art.get("body_html") or "", block)
                if a.apply and act in ("INSERT", "REPLACE"):
                    sh._req("PUT", "/blogs/%s/articles/%s.json" % (blog_id, art["id"]),
                            {"article": {"id": art["id"], "body_html": new}})
                    time.sleep(a.sleep)
            time.sleep(a.sleep / 3)
        stats[act] = stats.get(act, 0) + 1
        print("%-16s %s" % (act, r["slug"]))
    print("\nBilan :", ", ".join("%s=%d" % kv for kv in sorted(stats.items())))
    if not a.apply:
        print("Dry-run : rien n'a été écrit. Relancer avec --apply pour pousser.")


if __name__ == "__main__":
    main()
