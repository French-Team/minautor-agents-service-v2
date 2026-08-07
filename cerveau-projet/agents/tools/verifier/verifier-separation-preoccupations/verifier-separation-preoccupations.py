#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
verifier-separation-preoccupations.py

Verifie la separation des preoccupations dans les fichiers :
les index ne doivent pas contenir de sections de suivi, les
conventions pas de TODO/historique de suivi, les protocoles pas
de suivi (sauf descriptions de templates).

Utilisation:
  verifier-separation-preoccupations.py [DOSSIER]

Proprietaire : Vulcain (outil partage)
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "prepare"

SUIVI_INDEX = r"^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut du|^## .*Corrections recentes"
SUIVI_CONVENTION = r"^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut|^## .*Historique"
SUIVI_PROTOCOLE = r"^## .*Prochaines etapes|^## .*TODO|^## .*A faire|^## .*Faire|^## .*Statut|^## .*Historique"


def afficher_aide():
    print("=== verifier-separation-preoccupations v%s ===" % VERSION)
    print("")
    print("Usage: verifier-separation-preoccupations.py [DOSSIER]")
    print("")
    print("Verifie que les fichiers ne melangent pas plusieurs preoccupations :")
    print("  - Les index ne contiennent pas de sections de suivi")
    print("  - Les conventions ne contiennent pas de TODO/historique de suivi")
    print("  - Les protocoles ne contiennent pas de sections de suivi (sauf descriptions)")


def verifier(dossier):
    print("=== Verification de la separation des preoccupations ===")
    print("")

    total_erreurs = 0

    print("--- Verification des index ---")
    for fichier in sorted(trouver(dossier, "index-*.md")):
        erreurs = chercher_sections(fichier, SUIVI_INDEX, "index")
        total_erreurs += erreurs

    print("")
    print("--- Verification des conventions ---")
    for fichier in sorted(trouver(dossier, "convention-*.md")):
        erreurs = chercher_sections(fichier, SUIVI_CONVENTION, "convention")
        total_erreurs += erreurs

    print("")
    print("--- Verification des protocoles ---")
    for fichier in sorted(trouver(dossier, "protocole-*.md")):
        contenu = lire(fichier)
        if re.search(r"template|modele", contenu, re.IGNORECASE):
            continue  # Description de template : pas de suivi
        erreurs = chercher_sections(fichier, SUIVI_PROTOCOLE, "protocole")
        total_erreurs += erreurs

    print("")
    print("=== Termine ===")
    return 1 if total_erreurs > 0 else 0


def trouver(dossier, pattern):
    resultats = []
    import fnmatch
    for r, dossiers, fs in os.walk(dossier):
        for f in fs:
            if fnmatch.fnmatch(f, pattern):
                resultats.append(os.path.join(r, f))
    return resultats


def lire(fichier):
    try:
        with io.open(fichier, encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return ""


def chercher_sections(fichier, pattern, type_fichier):
    contenu = lire(fichier)
    lignes = contenu.split("\n")
    trouvees = [(i, l) for i, l in enumerate(lignes, 1) if re.match(pattern, l)]
    if trouvees:
        print("[ERREUR] %s contient une section de suivi" % fichier)
        for i, l in trouvees:
            print("  %d: %s" % (i, l))
        return 1
    return 0


def main(argv):
    dossier = "."

    if argv and argv[0] in ("--aide", "--help", "-h"):
        afficher_aide()
        return 0
    if argv and argv[0] == "--version":
        print("verifier-separation-preoccupations v%s (%s)" % (VERSION, STATUT))
        return 0

    if argv:
        dossier = argv[0]

    if not os.path.isdir(dossier):
        print("[ERREUR] Dossier non trouve : %s" % dossier)
        return 1

    return verifier(dossier)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
