#!/usr/bin/env python3
"""Copie de test de l'appli, publiée sur /beta/ (même site, mêmes fichiers).
  python3 tools/beta.py make     # index.html -> beta/index.html (+ sw.js, icônes, statut.json)
  python3 tools/beta.py promote  # beta/index.html -> index.html (retire les réglages « test »)
Réglages propres à la copie : titre « TEST », pastille « TEST », manifest (start_url /beta/), stockage local préfixé
« beta: » (session et réglages séparés de la vraie appli ; « dp-access » reste partagé pour passer l'écran d'accès)."""
import re, sys, base64, json, shutil, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX, BETA = os.path.join(ROOT, "index.html"), os.path.join(ROOT, "beta", "index.html")
SHIM = ('<script>/*BETA-SHIM*/(function(){var P="beta:",g=Storage.prototype.getItem,s=Storage.prototype.setItem,r=Storage.prototype.removeItem;'
        'function k(o,n){return o===window.localStorage&&n!=="dp-access"?P+n:n}'
        'Storage.prototype.getItem=function(n){return g.call(this,k(this,n))};'
        'Storage.prototype.setItem=function(n,v){return s.call(this,k(this,n),v)};'
        'Storage.prototype.removeItem=function(n){return r.call(this,k(this,n))};})();/*/BETA-SHIM*/</script>')
MAN = re.compile(r'(<link rel="manifest" href="data:application/manifest\+json;base64,)([^"]+)(")')
TITLE = re.compile(r'<title>.*?</title>', re.S)

def make():
    s = open(IDX, encoding="utf-8").read()
    def man(m):
        d = json.loads(base64.b64decode(m.group(2)))
        d.update({"name": "Deux Places TEST", "short_name": "DP TEST", "start_url": "/beta/", "scope": "/beta/"})
        return m.group(1) + base64.b64encode(json.dumps(d, ensure_ascii=False).encode()).decode() + m.group(3)
    s = MAN.sub(man, s, count=1)
    s = TITLE.sub('<title>Deux Places · TEST</title>', s, count=1)
    s = s.replace('class=\\"beta-badge\\">Beta<', 'class=\\"beta-badge\\">TEST<')
    i = s.index("<head>") + len("<head>")
    s = s[:i] + SHIM + s[i:]
    os.makedirs(os.path.dirname(BETA), exist_ok=True)
    open(BETA, "w", encoding="utf-8").write(s)
    for f in ("sw.js", "icon-192.png", "badge-96.png", "statut.json"):
        shutil.copy(os.path.join(ROOT, f), os.path.join(ROOT, "beta", f))
    print("beta/ à jour")

def promote():
    b = open(BETA, encoding="utf-8").read()
    o = open(IDX, encoding="utf-8").read()
    b = re.sub(r'<script>/\*BETA-SHIM\*/.*?/\*/BETA-SHIM\*/</script>', '', b, count=1, flags=re.S)
    b = MAN.sub(lambda m: MAN.search(o).group(0), b, count=1)
    b = TITLE.sub(lambda m: TITLE.search(o).group(0), b, count=1)
    b = b.replace('class=\\"beta-badge\\">TEST<', 'class=\\"beta-badge\\">Beta<')
    open(IDX, "w", encoding="utf-8").write(b)
    print("index.html mis à jour depuis beta/")

if __name__ == "__main__":
    {"make": make, "promote": promote}[sys.argv[1]]()
