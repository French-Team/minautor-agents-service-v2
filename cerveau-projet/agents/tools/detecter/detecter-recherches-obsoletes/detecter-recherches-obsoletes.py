#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
detecter-recherches-obsoletes.py

Detecter les recherches web devenues obsoletes (demande utilisateur
2026-08-16 : les agents doivent travailler avec des souvenirs VRAIS et
D ACTUALITE - recherches-web/ est leur memoire factuelle).

Critere d obsolescence (une recherche est a re-verifier si) :
  1. statut = "obsolete"                       (declaree obsolete)
  2. date_validite depassee (champ YAML)       (validite expiree)
  3. age > SEUIL_JOURS (defaut 30) depuis date (plus assez fraiche)

Options:
  --seuil <jours>    Age max avant signalement (defaut 30)
  --tous             Inclure les recherches deja marquees obsolete
  --rapport <fich>   Ecrire un rapport markdown
  --verbose          Afficher les details (chemins)
  --version          Afficher la version
  --aide             Afficher cette aide (alias de -h)
  --chrono           Afficher le chrono (defaut actif)

Protections : triplet chrono (template v0.3.0), ASCII strict + LF.
Lecture seule : ne modifie jamais recherches-web/.

Proprietaire : Atlas (explorateur - fraicheur de la memoire)
Version : 0.1.0
Statut : ebauche
"""

import argparse
import glob
import io
import os
import re
import sys
import time
from datetime import datetime

VERSION = "0.1.0"
STATUT = "ebauche"

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []

SEUIL_JOURS_DEFAUT = 30

_COULEURS = {
    "rouge": "\033[0;31m", "vert": "\033[0;32m", "jaune": "\033[1;33m",
    "bleu": "\033[0;34m", "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte,
                       _COULEURS["neutre"])


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO detecter-recherches-obsoletes (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def lister_recherches(racine):
    """Liste les fichiers de recherche (recherches-web/[theme]/*.md, hors
    index et templates - le template a un header placeholder). Retourne
    [(chemin, yaml, texte)]."""
    base = os.path.join(racine, "cerveau-projet", "recherches-web")
    base_n = base.replace("\\", "/")
    motif = os.path.join(base, "*", "*.md")
    resultats = []
    for chemin in sorted(glob.glob(motif)):
        rel = chemin.replace("\\", "/")
        rel_sans_base = rel.replace(base_n, "").lstrip("/")
        if rel_sans_base.split("/")[0] == "templates":
            continue  # le template a un header placeholder : non scanne
        nom = os.path.basename(chemin)
        if nom in ("index.md",) or chemin.endswith("index-recherches-web.md"):
            continue
        try:
            texte = io.open(chemin, encoding="utf-8", errors="replace").read()
        except IOError:
            continue
        yaml = ""
        m = re.search(r"^---\n(.*?)\n---", texte, re.S)
        if m:
            yaml = m.group(1)
        else:
            # header de secours : bloc ```yaml recherche: ...
            m2 = re.search(r"recherche:\s*\n(.*?)\n```", texte, re.S)
            if m2:
                yaml = m2.group(1)
        resultats.append((chemin, yaml, texte))
    return resultats


def _champ(yaml, cle):
    """Extrait la valeur d une cle YAML simple ('cle: valeur')."""
    m = re.search(r"^\s*" + re.escape(cle) + r"\s*:\s*\"?([^\"\n#]+)\"?",
                  yaml, re.M)
    return m.group(1).strip() if m else ""


def analyser(racine, seuil_jours, inclure_obsoletes, verbose):
    """Retourne (problemes, total) : probleme = dict(chemin, titre,
    raison, age_jours, statut)."""
    aujourd = datetime.now().date()
    problemes = []
    total = 0
    for chemin, yaml, texte in lister_recherches(racine):
        total += 1
        statut = _champ(yaml, "statut").lower()
        date_s = _champ(yaml, "date")
        validite_s = _champ(yaml, "date_validite")
        titre = _champ(yaml, "titre") or os.path.basename(chemin)
        raison = ""
        age = None
        try:
            date_recherche = datetime.strptime(date_s[:10], "%Y-%m-%d").date()
            age = (aujourd - date_recherche).days
        except (ValueError, TypeError):
            date_recherche = None
            raison = "date absente ou illisible"
        if statut == "obsolete":
            if inclure_obsoletes:
                problemes.append({"chemin": chemin, "titre": titre,
                                  "raison": "statut obsolete", "age_jours": age,
                                  "statut": statut})
            continue
        if validite_s:
            try:
                fin = datetime.strptime(validite_s[:10], "%Y-%m-%d").date()
                if fin < aujourd:
                    problemes.append({"chemin": chemin, "titre": titre,
                                      "raison": "date_validite expiree (%s)" % validite_s,
                                      "age_jours": age, "statut": statut})
                    continue
            except ValueError:
                pass
        deja_signale = any(p["chemin"] == chemin for p in problemes)
        if age is not None and age > seuil_jours:
            problemes.append({"chemin": chemin, "titre": titre,
                              "raison": "age %d jours > seuil %d" % (age, seuil_jours),
                              "age_jours": age, "statut": statut})
        elif raison and not deja_signale:
            # date absente/illisible : la fraicheur ne peut pas etre
            # etablie - a corriger dans la recherche elle-meme
            problemes.append({"chemin": chemin, "titre": titre,
                              "raison": raison, "age_jours": age,
                              "statut": statut})
    return problemes, total


def main():
    parser = argparse.ArgumentParser(
        prog="detecter-recherches-obsoletes",
        description="Detecte les recherches web obsoletes (memoire a rafraichir).")
    parser.add_argument("--seuil", type=int, default=SEUIL_JOURS_DEFAUT,
                        help="Age max avant signalement (defaut 30 jours)")
    parser.add_argument("--tous", action="store_true",
                        help="Inclure les recherches deja marquees obsolete")
    parser.add_argument("--rapport", default="", help="Fichier rapport markdown")
    parser.add_argument("--verbose", action="store_true", help="Details")
    parser.add_argument("--chrono", action="store_true", help="Chrono (defaut actif)")
    parser.add_argument("--version", action="version",
                        version="detecter-recherches-obsoletes %s (%s)"
                                % (VERSION, STATUT))
    parser.add_argument("--aide", action="help", help="Afficher cette aide")
    args = parser.parse_args()

    t0 = time.monotonic()
    racine = racine_projet()
    problemes, total = analyser(racine, args.seuil, args.tous, args.verbose)
    chrono_etape("scan recherches-web", t0)

    print("")
    print(_couleur("=== RECHERCHES OBSOLETES A RE-VERIFIER : %d / %d ==="
                   % (len(problemes), total),
                   "rouge" if problemes else "vert"))
    for p in problemes:
        print("")
        print(_couleur("- %s" % p["titre"], "jaune"))
        print("   %s" % p["chemin"].replace(racine + os.sep, ""))
        print("   raison : %s" % p["raison"])
        if p["age_jours"] is not None:
            print("   age : %d jour(s)" % p["age_jours"])
        print("   statut : %s" % p["statut"])

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport detecter-recherches-obsoletes\n\n")
            fh.write("- Date : %s\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("- Seuil : %d jours\n" % args.seuil)
            fh.write("- Recherches scannees : %d\n" % total)
            fh.write("- A re-verifier : %d\n\n" % len(problemes))
            for p in problemes:
                fh.write("- **%s** : %s (age %s)\n" % (
                    p["titre"], p["raison"],
                    "%d j" % p["age_jours"] if p["age_jours"] is not None else "?"))
        print(_couleur("[rapport] %s" % args.rapport, "jaune"))

    bilan_chrono()
    return 1 if problemes else 0


if __name__ == "__main__":
    sys.exit(main())
