#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-fautes-orthographe.py
# Outil de l agent Hermes : detecte les fautes d orthographe francaise les plus
# courantes commises par les agents dans les fichiers du cerveau-projet.
#
# Principe : dictionnaire de fautes frequentes (mot fautif -> mot correct).
# Le francais du projet est redige en ASCII pur (regle-emojis-ascii) : les mots
# corrects sont donc ecrits sans accents (ex: "probleme", "etre", "deja").
# L outil ne signale QUE les mots repertories comme fautifs -- jamais les mots
# corrects -- pour eviter tout faux positif.
#
# Usage :
#   python3 detecter-fautes-orthographe.py --tous
#   python3 detecter-fautes-orthographe.py --fichier <chemin>
#   python3 detecter-fautes-orthographe.py --fichier <chemin> --rapport <md>
#   python3 detecter-fautes-orthographe.py --version
#
# Exclusions par defaut (--tout pour lever) : corrections.md (lecons
# historiques citant d anciennes fautes), tests/ (verifient des contenus),
# rapports*/ (documentent l historique).
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

import argparse
import io
import os
import re
import sys
from pathlib import Path

VERSION = "0.1.0"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


# ---------------------------------------------------------------------------
# Dictionnaire des fautes les plus courantes (fautif -> correct).
# Ajouter une entree = etendre la couverture. Chaque mot correct est en ASCII.
# ---------------------------------------------------------------------------
FAUTES = {
    # doublement de consonne manquant (le mot correct garde ses doubles)
    "aparait": "apparait",
    "aparition": "apparition",
    "apel": "appel",
    "apelle": "appelle",
    "actuelement": "actuellement",
    "adrese": "adresse",
    "accesible": "accessible",
    "atendre": "attendre",
    "atention": "attention",
    "atribuer": "attribuer",
    "comande": "commande",
    "comence": "commence",
    "coment": "comment",
    "comun": "commun",
    "conexion": "connexion",
    "colaboration": "collaboration",
    "coriger": "corriger",
    "corespond": "correspond",
    "demarage": "demarrage",
    "demarer": "demarrer",
    "diferents": "differents",
    "environement": "environnement",
    "ereur": "erreur",
    "esai": "essai",
    "existance": "existence",
    "honete": "honnete",
    "honetete": "honnetete",
    "inteligent": "intelligent",
    "mesage": "message",
    "netoyage": "nettoyage",
    "netoyer": "nettoyer",
    "neamoins": "neanmoins",
    "ocasion": "occasion",
    "outilage": "outillage",
    "paralelle": "parallele",
    "parralelle": "parallele",
    "pasage": "passage",
    "permanant": "permanent",
    "profesionnel": "professionnel",
    "recomandation": "recommandation",
    "recomande": "recommande",
    "suprime": "supprime",
    "supression": "suppression",
    "suces": "succes",
    "toujour": "toujours",
    "toutefoit": "toutefois",
    "toutfois": "toutefois",
    # fautes frequentes relevees dans le projet
    "enchannement": "enchainement",
    "enchannements": "enchainements",
    "enchannent": "enchainent",
    "racourci": "raccourci",
    "racourcis": "raccourcis",
    "racourcir": "raccourcir",
    "courrant": "courant",
    "correspondanc": "correspondance",
}

# Mots a NE PAS signaler (verite : formes ASCII correctes frequentes).
# Utilise pour la doc et les tests -- le filtre est implicite : un mot n est
# signale QUE s il est dans FAUTES.
MOTS_CORRECTS_ASCII = [
    "probleme", "etre", "deja", "tache", "meme", "separe", "verifie",
    "necessaire", "parallele", "developpement", "existant", "utilisateur",
]

EXTENSIONS_MD = (".md",)


def _mot_fautif_present(ligne, mot):
    """Retourne True si le mot fautif apparait comme mot entier."""
    return re.search(r"\b" + re.escape(mot) + r"\b", ligne) is not None


def scanner_fichier(chemin, tout=False):
    """Retourne [(ligne, mot_fautif, mot_correct)] d un fichier."""
    resultats = []
    nom = os.path.basename(chemin)
    parties = chemin.replace("\\", "/").split("/")
    if not tout:
        # Citations legitimes : journal, missions en cours, doc de l outil
        # lui-meme (exemples du dictionnaire), lecons, tests, rapports.
        if nom in ("corrections.md", "AGENTS-historique.md", "AGENTS.md",
                   "detecter-fautes-orthographe.md"):
            return resultats
        if "tests" in parties:
            return resultats
        if "rapports" in parties or nom.startswith("rapport-"):
            return resultats
        if "snapshots" in parties:
            return resultats
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        return resultats
    for i, ligne in enumerate(lignes):
        for fautif, correct in sorted(FAUTES.items(), key=lambda x: -len(x[0])):
            if _mot_fautif_present(ligne, fautif):
                resultats.append((i + 1, fautif, correct, ligne.strip()[:140]))
                break
    return resultats


def scanner_chemin(chemin, tout=False):
    """Scan d un fichier ou d un dossier : {chemin: [resultats]}."""
    resultats = {}
    if os.path.isfile(chemin):
        if chemin.endswith(EXTENSIONS_MD):
            r = scanner_fichier(chemin, tout)
            if r:
                resultats[chemin] = r
        return resultats
    for dossier, sous_dossiers, fichiers in os.walk(chemin):
        sous_dossiers[:] = [d for d in sous_dossiers
                            if d != "__pycache__" and d != ".git"]
        for f in fichiers:
            if f.endswith(EXTENSIONS_MD):
                p = os.path.join(dossier, f)
                r = scanner_fichier(p, tout)
                if r:
                    resultats[p] = r
    return resultats


def scanner_tous(tout=False):
    """Scan de tout le projet (racine) : cerveau-projet/ + README/readme-dev + regles."""
    resultats = {}
    for dossier, sous_dossiers, fichiers in os.walk("."):
        sous_dossiers[:] = [d for d in sous_dossiers
                            if d != "__pycache__" and d != ".git"
                            and not d.startswith("tmp-")
                            and d != "workspace"]
        for f in fichiers:
            if not f.endswith(EXTENSIONS_MD):
                continue
            p = os.path.join(dossier, f)
            r = scanner_fichier(p, tout)
            if r:
                resultats[p] = r
    return resultats


def _ecrire_rapport(resultats, chemin_rapport):
    lignes = []
    lignes.append("# Rapport detecter-fautes-orthographe")
    lignes.append("")
    lignes.append("**Outil** : detecter-fautes-orthographe v" + VERSION)
    lignes.append("")
    total = 0
    for chemin, r in sorted(resultats.items()):
        total += len(r)
        lignes.append("## " + chemin)
        lignes.append("")
        lignes.append("| Ligne | Mot fautif | Correction | Contexte |")
        lignes.append("|---|---|---|---|")
        for num, fautif, correct, ctx in r:
            lignes.append("| %d | `%s` | `%s` | %s |" % (num, fautif, correct, ctx))
        lignes.append("")
    lignes.append("## Verdict")
    lignes.append("")
    if total == 0:
        lignes.append("**OK** : 0 faute detectee.")
    else:
        lignes.append("**KO** : %d faute(s) detectee(s)." % total)
    lignes.append("")
    with io.open(chemin_rapport, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lignes) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Detecte les fautes d orthographe francaise courantes "
                    "dans les fichiers markdown du cerveau-projet (agent Hermes).")
    parser.add_argument("--tous", action="store_true",
                        help="Scanner tout le cerveau-projet + readme* a la racine")
    parser.add_argument("--fichier", metavar="CHEMIN",
                        help="Scanner un fichier ou un dossier")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="Ecrire le rapport markdown dans FICHIER")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher le detail des exclusions")
    parser.add_argument("--tout", action="store_true",
                        help="Lever les exclusions (corrections, tests, rapports)")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    args = parser.parse_args()

    if args.version:
        print("detecter-fautes-orthographe v%s (%s)" % (VERSION, STATUT))
        return 0

    if args.tous and args.fichier:
        print(_couleur("ERREUR : --tous et --fichier sont exclusifs", "rouge"),
              file=sys.stderr)
        return 2

    if args.tous:
        resultats = scanner_tous(tout=args.tout)
    elif args.fichier:
        chemin = args.fichier
        if not os.path.exists(chemin):
            print(_couleur("ERREUR : chemin introuvable : %s" % chemin, "rouge"),
                  file=sys.stderr)
            return 2
        resultats = scanner_chemin(chemin, tout=args.tout)
    else:
        parser.print_help()
        return 2

    total = sum(len(r) for r in resultats.values())
    if not resultats:
        print(_couleur("OK : 0 faute detectee.", "vert"))
    else:
        print(_couleur("KO : %d faute(s) detectee(s) dans %d fichier(s)."
                       % (total, len(resultats)), "rouge"))
        for chemin, r in sorted(resultats.items()):
            print("  %s : %d faute(s)" % (chemin, len(r)))
            if args.verbose:
                for num, fautif, correct, ctx in r[:10]:
                    print("    L%d : '%s' -> '%s' | %s"
                          % (num, fautif, correct, ctx))
    if args.rapport:
        _ecrire_rapport(resultats, args.rapport)
        print("Rapport ecrit : %s" % args.rapport)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
