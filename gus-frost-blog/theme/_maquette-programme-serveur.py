"""Sert le dossier des maquettes en local, avec CORS, pour que Chrome les charge.
Assemble a la volee /page.js : sections retenues + variantes de la section en cours."""
import http.server, os, re, sys

THEME = r"C:\Users\regis\gfbrepo\gus-frost-blog\theme"
# section -> variante retenue ; None = section en cours (on garde les deux)
CHOIX = [("1-ouverture", "gfpA"), ("2-jour10", "A"), ("3-contenu", "B"), ("4-prix", "B"),
         ("5-garantie", "A"), ("6-accompagne", "A")]

def page():
    out = ["document.querySelector('#MainContent').innerHTML='';",
           "document.querySelector('#MainContent').insertAdjacentHTML('beforeend','<div class=\"gfp\"></div>');"]
    for nom, a_retirer in CHOIX:
        src = open(os.path.join(THEME, "_maquette-programme-%s.js" % nom), encoding="utf-8").read()
        if nom == "1-ouverture":
            # ce fichier remplace tout #MainContent : on le laisse faire, puis on retire la variante A
            out.append(src.strip().rstrip(";") + ";")
            out.append("(()=>{const g=document.querySelector('.gfp');g.querySelectorAll('.gfp-lbl')[0].remove();g.querySelector('.gfpA').remove();g.querySelector('.gfp-lbl').remove();})();")
            continue
        if nom == "2-jour10":
            # ce fichier retire lui-meme la variante A de l'ouverture : neutraliser
            src = src.replace("g.querySelectorAll('.gfp-lbl')[0].remove(); g.querySelector('.gfpA').remove();\ng.querySelector('.gfp-lbl').textContent = 'Section 1 retenue : ouverture B';", "")
        src = re.sub(r"localStorage\.setItem\([^;]*;", "", src)
        src = re.sub(r"g\.querySelectorAll\('\[data-s\d=\"B\"\]'\)\.forEach\(e => e\.remove\(\)\);", "", src)
        src = re.sub(r"g\.querySelector\('\[data-s\d=\"A\"\]'\)\.scrollIntoView\(\);", "", src)
        src = re.sub(r"document\.title = [^;]*;", "", src)
        src = re.sub(r"document\.getElementById\('gfp-ov'\)\?\.remove\(\);", "", src)
        out.append(src.strip().rstrip(";") + ";")
        if nom == "2-jour10":
            out.append("(()=>{const g=document.querySelector('.gfp');const l=[...g.querySelectorAll('.gfp-lbl')];const c=[...g.querySelectorAll('.gfp-cap')];l[l.length-2].remove();c[c.length-2].remove();l[l.length-1].remove();})();")
        elif a_retirer:
            n = nom[0]
            out.append("document.querySelectorAll('[data-s%s=\"%s\"]').forEach(e=>e.remove());" % (n, a_retirer))
            if n != "6":
                out.append("document.querySelectorAll('[data-s%s]').forEach(e=>{if(e.classList.contains('gfp-lbl'))e.remove()});" % n)
    return "\n".join(out)

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

if len(sys.argv) > 1 and sys.argv[1] == "--print":
    print(page())
else:
    http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
