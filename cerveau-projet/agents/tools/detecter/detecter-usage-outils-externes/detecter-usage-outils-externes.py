#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-usage-outils-externes.py
# Detecte les traces d'utilisation d'outils externes (CRLF, non-ASCII, BOM)
# dans les fichiers du cerveau-projet. Nos outils ecrivent en ASCII strict,
# LF et sans BOM : toute trace differente signale un outil externe.
# Version : 0.1.1
# Statut : prepare
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe
# du dossier de categorie (detecter-).
# ============================================================

import argparse
import os
import sys
from pathlib import Path

VERSION = "0.1.1"
STATUT = "prepare"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    """Retourne le texte colore si le terminal le supporte, sinon brut."""
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


EXTENSIONS = (".md", ".sh", ".py", ".txt", ".json")

# ============================================================
# EXCLUSIONS PAR DEFAUT : fichiers/chemins volontairement NON
# conformes aux traces d'outil externe, donc legitimes.
#   - corriger-dictionnaire-accents.txt / dictionnaire-emojis.txt :
#     dictionnaires de CORRECTION qui contiennent par nature les
#     caracteres accents/emojis a corriger (non-ASCII volontaire).
#   - exemples/ : jeux de tests pedagogiques (test-emojis,
#     test-accents-zones-sensibles...) qui DOIVENT contenir du
#     non-ASCII pour prouver que les correcteurs fonctionnent.
#   - docs-dev-cerveau-projet/ : documents externes fournis par
#     l utilisateur (analyses) qui ne suivent pas nos normes.
# Un motif matche des qu il apparait dans le chemin (sous-chaine).
# ============================================================
EXCLUSIONS_PAR_DEFAUT = (
    "corriger-dictionnaire-accents.txt",
    "dictionnaire-emojis.txt",
    os.path.join("exemples", ""),
    os.path.join("docs-dev-cerveau-projet", ""),
)


def est_exclu(chemin, exclusions):
    """Retourne True si le chemin correspond a une exclusion (sous-chaine)."""
    chaine = str(chemin).replace("\\", "/")
    for motif in exclusions:
        m = str(motif).replace("\\", "/")
        if m and m in chaine:
            return True
    return False


def analyser_fichier(chemin):
    """Analyse un fichier et retourne la liste des signes d'outil externe.

    Retourne (liste_signes, contenu_brut) ou None si le fichier est propre.
    """
    signes = []
    try:
        with open(chemin, "rb") as fh:
            brut = fh.read()
    except (OSError, IOError):
        return None

    # BOM UTF-8 : EF BB BF en tete
    if brut.startswith(b"\xef\xbb\xbf"):
        signes.append("BOM UTF-8")

    # CRLF : presence de \r\n
    if b"\r\n" in brut:
        # Compter les lignes CRLF
        nb = brut.count(b"\r\n")
        signes.append("CRLF (%d lignes)" % nb)

    # Non-ASCII : octets > 127
    try:
        texte = brut.decode("utf-8")
        non_ascii = [ch for ch in texte if ord(ch) > 127]
        if non_ascii:
            signes.append("non-ASCII (%d caracteres)" % len(non_ascii))
    except UnicodeDecodeError:
        # Fichier binaire ou encodage exotique : signaler
        signes.append("encodage non UTF-8")

    if not signes:
        return None
    return signes


def main():
    """Point d'entree principal."""
    verifier_nommage(sys.argv[0])

    parser = argparse.ArgumentParser(
        prog="detecter-usage-outils-externes",
        description="Detecte les traces d'outils externes (CRLF, non-ASCII, BOM) "
                    "dans les fichiers. Nos outils ecrivent ASCII strict + LF sans BOM.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("cible", type=str, nargs="?", default=".",
                        help="Fichier ou dossier a analyser (defaut: .)")
    parser.add_argument("--recursive", action="store_true",
                        help="Scanner recursivement les sous-dossiers")
    parser.add_argument("--exclure", action="append", default=[],
                        help="Motif supplementaire a exclure (sous-chaine de chemin)")
    parser.add_argument("--version", action="version",
                        version="detecter-usage-outils-externes v%s" % VERSION)
    args = parser.parse_args()

    exclusions = list(EXCLUSIONS_PAR_DEFAUT) + args.exclure

    cible = Path(args.cible)
    if not cible.exists():
        print(_couleur("ERREUR: Cible introuvable: %s" % cible, "rouge"), file=sys.stderr)
        return 1

    # Collecter les fichiers a analyser
    fichiers = []
    if cible.is_file():
        fichiers = [cible]
    else:
        if args.recursive:
            for racine, _, noms in os.walk(str(cible)):
                # Ignorer les artefacts Python et les dossiers caches
                if "__pycache__" in racine or "/.git" in racine:
                    continue
                for nom in noms:
                    p = Path(racine) / nom
                    if p.suffix in EXTENSIONS:
                        fichiers.append(p)
        else:
            for nom in sorted(cible.iterdir()):
                if nom.is_file() and nom.suffix in EXTENSIONS:
                    fichiers.append(nom)

    fichiers = sorted(fichiers, key=lambda p: str(p))

    total_signes = 0
    fichiers_suspects = 0

    for f in fichiers:
        if est_exclu(f, exclusions):
            continue
        signes = analyser_fichier(f)
        if signes:
            fichiers_suspects += 1
            total_signes += len(signes)
            print(_couleur("SUSPECT: %s" % f, "jaune"))
            for s in signes:
                print("    - %s" % s)
        else:
            print(_couleur("PROPRE : %s" % f, "vert"))

    print("")
    print("=== RESUME ===")
    print("Fichiers analyses : %d" % len(fichiers))
    print("Fichiers suspects  : %d" % fichiers_suspects)
    print("Signes detectes    : %d" % total_signes)

    if fichiers_suspects > 0:
        print(_couleur(
            "VERDICT : traces d'outils externes detectees (CRLF/non-ASCII/BOM)",
            "rouge"))
        return 1

    print(_couleur("VERDICT : aucun signe d'outil externe -- conformite OK", "vert"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
