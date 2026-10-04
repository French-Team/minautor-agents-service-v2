#!/usr/bin/env python3
"""revert-fichier.py -- SECOURS : rendre un fichier a sa version d avant.

Usage: python revert-fichier.py --fichier <chemin> [--depuis-bak]

PORTE DE SECOURS (EO-159, mesure MO-169) : elle ecrit SANS passer par la porte
ecrire, et c est VOULU -- elle sert precisement quand la porte est CASSEE (un
import pose avant sa constante a rendu la porte injouable : plus aucune ecriture
possible dans tout le workspace, toute ecriture passant par elle).
Elle consomme le POINT DE RESTAURATION que la porte laisse derriere elle a
chaque ecriture : le .bak horodate.
Limites DITES : aucune validation, aucun SHA, aucun nouveau .bak (la version
courante est perdue) -- le fichier rendu est celui du .bak le plus recent.
"""
import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Secours : revert depuis le point de restauration .bak")
    parser.add_argument("--fichier", required=True, help="Fichier a rendre")
    parser.add_argument("--depuis-bak", action="store_true", help="Prendre le .bak le plus recent (defaut)")
    args = parser.parse_args()

    fichier = Path(args.fichier)
    baks = sorted(fichier.parent.glob(fichier.name + ".bak.*"), key=lambda p: p.stat().st_mtime)
    if not baks:
        print("REFUS : aucun point de restauration (.bak.*) pour " + str(fichier))
        return 2
    dernier = baks[-1]
    contenu = dernier.read_text(encoding="utf-8")
    # LF forces : la porte force LF, un secours qui rend du CRLF casserait l invariant.
    contenu = contenu.replace("\r\n", "\n").replace("\r", "\n")
    fichier.write_text(contenu, encoding="utf-8", newline="\n")
    print("SECOURS : " + str(fichier) + " rendu depuis " + dernier.name)
    print("Limites : aucune validation, aucun SHA, la version courante n a pas ete sauvee.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
