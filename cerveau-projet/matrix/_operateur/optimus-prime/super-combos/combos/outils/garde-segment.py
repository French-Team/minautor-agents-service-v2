#!/usr/bin/env python3
"""GARDE BLOQUANT avant tout depot de segment (MO-549, premiere table ronde).

Le segment est le TEMOIN d une deliberation : il ne decrit pas, il tranche.
Une trace corrompue ne peut donc pas rester -- elle ferme une decision avec du
texte qui n existe pas. Mesure MO-549 : trois contaminations ont traverse le
controle ASCII du projet (fragment sans sens colle a un point, caracteres CJK
glisses, accent la ou l ASCII est impose). La cause n etait pas le hasard : le
controle signalait et sortait 0, donc l appelant enchainait quand meme. Un
garde qui rapporte et laisse passer est un rapport, pas un garde. Ici il BLOQUE.

Usage : garde-segment.py <fichier-a-deposer>

    bdd-raisonnement ajouter --segment "$(cat <fichier>)" ...

Le garde sort en 1 sur une faute : l appelant doit donc l enclencher sur `&&`.

CALIBRAGE. Une regle de fragment posee sur une intuition produit des faux
positives, et un faux positif dans un garde BLOQUANT arrete le travail : plus
cher que la faute qu il traque. Mesure : la premiere regle lisait un nom de
fichier suivi de son extension comme une soudure. D ou la LISTE BLANCHE des
extensions reelles du projet, et le contre-temoin joue (epargner le nom de
fichier, bloquer la soudure).
"""
import re
import sys

# Extensions reelles du projet : derriere un point, c est un fichier, pas une
# soudure. La liste s elargit avec le parc, jamais par assouplissement du regle.
EXTENSIONS = {
    "db", "md", "py", "json", "jsonl", "txt", "csv", "svg", "bak", "log",
    "js", "ts", "sh", "cfg", "toml", "yml", "yaml", "html", "css", "pid",
}

FRAGMENT = re.compile(r"[a-z]\.([A-Za-z]+)")


def fautes(texte):
    trouvees = []
    for i, c in enumerate(texte):
        if ord(c) > 127:
            # Le rapport porte le CODE POINT, jamais le caractere : sous
            # Windows (cp1252) afficher un CJK ou un cyrillique fait PLANTER le
            # garde au moment exact ou il doit parler. Un garde qui meurt sur la
            # faute qu il traque ne la declare pas (mesure MO-540).
            autour = ascii(texte[max(0, i - 25):i + 15])
            trouvees.append("non-ASCII " + hex(ord(c)) + " vers " + autour)
    for m in FRAGMENT.finditer(texte):
        suite = m.group(1)
        if suite.lower() in EXTENSIONS:
            continue
        autour = ascii(texte[max(0, m.start() - 25):m.start() + 25])
        trouvees.append("fragment colle a un point : " + autour)
    return trouvees


def main(argv):
    if len(argv) < 2:
        print("usage : garde-segment.py <fichier>")
        return 2
    with open(argv[1], encoding="utf-8") as f:
        texte = f.read()
    trouvees = fautes(texte)
    if trouvees:
        print("GARDE BLOQUANT : " + str(len(trouvees)) + " faute(s) -- depot EMPECHE")
        for f in trouvees[:10]:
            print("  " + f)
        return 1
    print("garde vert : " + str(len(texte)) + " caracteres, 0 faute")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))