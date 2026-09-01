#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Balisage FAQPage (JSON-LD) construit À PARTIR du bloc `.gf-faq` de l'article.

Chaque article du blog porte une FAQ de 5 questions rendue en <h3> + réponse.
Sans balisage, Google ne peut pas la reconnaître : le déclarer ouvre les résultats
enrichis en accordéon dans la SERP.

Règle de Google : le balisage doit refléter EXACTEMENT le contenu visible de la
page. On ne réécrit donc rien — questions et réponses sont extraites telles quelles.

  from faq_schema import inject
  body = inject(body)      # idempotent : ne double jamais le bloc
"""
import html as _html
import json
import re

FAQ_OPEN = re.compile(r'<div[^>]*class="[^"]*\bgf-faq\b[^"]*"[^>]*>', re.I)
DIV_TAG = re.compile(r"<(/?)div\b", re.I)
MARKER = '"@type": "FAQPage"'


def _bloc_faq(body):
    """Contenu du div.gf-faq, délimité en comptant les <div> imbriqués.

    Une simple regex non gourmande s'arrête au premier </div> et échoue dès qu'un
    encadré est imbriqué dans la FAQ : c'était le cas de 48 articles des premiers
    clusters, silencieusement privés de balisage.
    """
    m = FAQ_OPEN.search(body)
    if not m:
        return ""
    depth, i = 1, m.end()
    for t in DIV_TAG.finditer(body, m.end()):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return body[i:t.start()]
    return body[i:]


def _texte(fragment):
    """HTML -> texte lisible : les <li> deviennent des phrases, pas des collages."""
    s = re.sub(r"<li\b[^>]*>", " ", fragment)
    s = re.sub(r"</li>", ".", s)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = _html.unescape(s)
    # \s engloberait les insecables : on les preserve, le balisage doit refleter
    # EXACTEMENT le texte visible, insecables francaises comprises.
    s = re.sub(r"[^\S\u00a0\u202f]+", " ", s).strip()
    return re.sub(r"[^\S\u00a0\u202f]+\.", ".", s)


def paires(body):
    """-> [(question, réponse)] extraites du bloc gf-faq, dans l'ordre."""
    inner = _bloc_faq(body)
    if not inner:
        return []
    parts = re.split(r"<h3\b[^>]*>", inner)[1:]
    out = []
    for p in parts:
        q, _, rest = p.partition("</h3>")
        q, r = _texte(q), _texte(rest)
        if q and r:
            out.append((q, r))
    return out


def build(body):
    """-> le <script> JSON-LD, ou '' si l'article n'a pas de FAQ exploitable."""
    qa = paires(body)
    if not qa:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa
        ],
    }
    return ('<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, indent=None)
            + "</script>")


def strip(body):
    """Retire un bloc FAQPage déjà posé (pour le régénérer proprement)."""
    return re.sub(r'<script type="application/ld\+json">\s*\{[^<]*?"@type":\s*"FAQPage".*?</script>\s*',
                  "", body, flags=re.S)


def inject(body):
    """Pose (ou remplace) le balisage juste avant </article>. Idempotent."""
    sc = build(body)
    if not sc:
        return body
    body = strip(body)
    i = body.rfind("</article>")
    if i < 0:
        return body + "\n" + sc
    return body[:i] + sc + "\n" + body[i:]
