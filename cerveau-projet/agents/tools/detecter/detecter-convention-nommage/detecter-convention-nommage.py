#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-convention-nommage.py
# Garde-fou anti-recurrence (audit Themis 2026-08-11) : detecte les mentions
# de la convention de nommage `c<numero>[a-z]?` HORS contexte etendu cT*
# (`c[<prefixe-alpha-maj>]<numero>[a-z]?` : cas normal + prefixe thematique
# majuscule optionnel cT1..cT10, ligne Trio de Janus).
#
# Methode validee par Themis : une mention `c<numero>[a-z]?` est CONFORME si
# elle est dans une fenetre de +/- 2 lignes contenant `c[<prefixe-alpha-maj>]`
# ou `cT1`..`cT10` (le cas normal documente comme PARTIE de la convention
# etendue) ; sinon elle est un ECART.
#
# Exclusions par defaut (--tout pour lever) :
#   - corrections.md : lecons historiques qui citent legitiment l'ancienne forme
#   - tests/         : les tests verifient les ids GENERES par les outils
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
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    """Verifie que le nom du fichier commence par le prefixe du dossier."""
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(
            _couleur(
                "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
                % (nom_fichier, prefixe),
                "rouge",
            ),
            file=sys.stderr,
        )
        sys.exit(1)


# Regex : mention de la convention c<numero>[a-z]? (avec ou sans backticks)
PATTERN_MENTION = re.compile(r"c<numero>\[a-z\]\?")
# Contexte etendu : c[<prefixe-alpha-maj>], cT1..cT10 ou la forme abregee cT*
PATTERN_ETENDU = re.compile(r"c\[<prefixe-alpha-maj>\]|cT\d|cT\*")
FENETRE = 2  # +/- 2 lignes autour de la mention

EXTENSIONS = (".md", ".py", ".sh")


def scanner_fichier(chemin, tout=False):
    """Retourne la liste des ecarts (numero de ligne, extrait) d'un fichier."""
    ecarts = []
    nom = os.path.basename(chemin)
    # Exclusions par defaut (--tout pour lever)
    if not tout:
        if nom == "corrections.md":
            return ecarts
        parties = chemin.replace("\\", "/").split("/")
        # tests/ : verifient les ids GENERES ; rapports/ + rapports-audit :
        # documentent l'HISTORIQUE des ecarts (comme corrections.md)
        if "tests" in parties:
            return ecarts
        if "rapports" in parties or nom.startswith("rapport-audit-"):
            return ecarts
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        return ecarts
    for i, ligne in enumerate(lignes):
        if not PATTERN_MENTION.search(ligne):
            continue
        debut = max(0, i - FENETRE)
        fin = min(len(lignes), i + FENETRE + 1)
        contexte = " ".join(lignes[debut:fin])
        if PATTERN_ETENDU.search(contexte):
            continue  # cas normal documente comme partie de la convention etendue
        ecarts.append((i + 1, ligne.strip()[:120]))
    return ecarts


def scanner_racine(racine, tout=False):
    """Scan recursif : retourne {chemin: [ecarts]}."""
    resultats = {}
    racine_abs = os.path.abspath(racine)
    if not os.path.isdir(racine_abs):
        print(_couleur("ERREUR : racine introuvable : %s" % racine, "rouge"),
              file=sys.stderr)
        sys.exit(1)
    for dossier, sous_dossiers, fichiers in os.walk(racine_abs):
        sous_dossiers[:] = [d for d in sous_dossiers if d != "__pycache__"]
        for nom in fichiers:
            if not nom.endswith(EXTENSIONS):
                continue
            chemin = os.path.join(dossier, nom)
            ecarts = scanner_fichier(chemin, tout=tout)
            if ecarts:
                resultats[chemin] = ecarts
    return resultats


def main(argv):
    parser = argparse.ArgumentParser(
        prog="detecter-convention-nommage",
        description="Detecte les mentions de la convention c<numero>[a-z]? "
                    "hors contexte etendu cT* (garde-fou anti-recurrence).",
        add_help=True)
    parser.add_argument("--aide", action="help",
                        help="Affiche cette aide (alias de --help)")
    parser.add_argument("--version", action="store_true",
                        help="Affiche la version")
    parser.add_argument("--racine", default="cerveau-projet",
                        help="Racine du scan (defaut: cerveau-projet)")
    parser.add_argument("--tout", action="store_true",
                        help="Inclure corrections.md et tests/ (lever les exclusions)")
    parser.add_argument("--rapport", default="",
                        help="Chemin du rapport markdown (optionnel, rien par defaut)")
    args = parser.parse_args(argv)

    if args.version:
        print("detecter-convention-nommage v%s (%s)" % (VERSION, STATUT))
        return 0

    verifier_nommage(os.path.abspath(__file__))

    resultats = scanner_racine(args.racine, tout=args.tout)
    total = sum(len(e) for e in resultats.values())

    print("=== detecter-convention-nommage v%s ===" % VERSION)
    print("Racine : %s | %d ecart(s) dans %d fichier(s)"
          % (args.racine, total, len(resultats)))
    if total:
        for chemin in sorted(resultats):
            for num, extrait in resultats[chemin]:
                print("  [ECART] %s:%d : %s" % (chemin, num, extrait))
        print(_couleur("VERDICT : ECART(S) DETECTE(S) (%d)" % total, "rouge"))
    else:
        print(_couleur("VERDICT : CONFORME (aucune mention hors contexte etendu)", "vert"))

    # Rapport optionnel (Pattern 12 : jamais de fichier cree sans --rapport)
    if args.rapport:
        L = ["# Rapport detecter-convention-nommage", "",
             "**Date** : %s | **Outil** : v%s | **Racine** : %s" % (
                 __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
                 VERSION, args.racine), "",
             "## Verdict", "", "**%s**" % ("ECARTS (%d)" % total if total else "CONFORME"), "",
             "| Fichier | Ligne | Extrait |", "|---|---|---|"]
        for chemin in sorted(resultats):
            for num, extrait in resultats[chemin]:
                L.append("| %s | %d | %s |" % (chemin, num, extrait))
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(L) + "\n")
        print("RAPPORT ECRIT : %s" % os.path.abspath(args.rapport))

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
