#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
valider-conformite-ascii.py

Valide la conformite ASCII stricte du projet.
Regle : AUCUN caractere non-ASCII n'est tolere (accents, emojis, symboles).
Seules exceptions : le dossier exemples/ (zone de test volontaire) et les
dictionnaires fonctionnels (corriger-dictionnaire-accents, dictionnaire-emojis)
qui DOIVENT contenir les caracteres qu'ils mappent (exceptions declarees).

Utilisation:
  valider-conformite-ascii.py [OPTIONS] [DOSSIER]

Options :
  --dry-run       Afficher les erreurs sans corriger
  --exclure       Exclure des motifs supplementaires
  --help          Afficher cette aide

Proprietaire : Vulcain (outil partage)
Version : 0.3.0-py
Statut : prepare
"""

import io
import os
import sys

VERSION = "0.3.0-py"
STATUT = "prepare"

EXTENSIONS_VALIDEES = (".md", ".sh", ".py", ".txt", ".json", ".yaml", ".yml", ".js")

MOTIFS_EXCLUS = [
    "exemples",
    "corriger-dictionnaire-accents",
    "dictionnaire-emojis",
    ".git",
    ".agents",
    ".backup",
    ".tmp",
]


def afficher_aide():
    print("=== valider-conformite-ascii v%s ===" % VERSION)
    print("")
    print("Usage: valider-conformite-ascii.py [OPTIONS] [DOSSIER]")
    print("")
    print("Valide que TOUT le contenu est ASCII pur (regle immuable : aucun")
    print("accent, emoji ou symbole Unicode). Les seules exceptions sont le")
    print("dossier exemples/ (test volontaire) et les dictionnaires fonctionnels.")
    print("")
    print("Options :")
    print("  --dry-run       Afficher les erreurs sans corriger")
    print("  --exclure       Exclure des motifs supplementaires")
    print("  --help          Afficher cette aide")
    print("")
    print("Exemples :")
    print("  valider-conformite-ascii.py cerveau-projet/")
    print("  valider-conformite-ascii.py --dry-run cerveau-projet/")


def lister_fichiers(cible):
    fichiers = []
    if os.path.isfile(cible):
        return [cible]
    if not os.path.isdir(cible):
        return fichiers
    for r, dossiers, fs in os.walk(cible):
        if any(m in r for m in [".git", ".agents"]):
            continue
        for f in fs:
            fichiers.append(os.path.join(r, f))
    return fichiers


def analyser(fichier):
    """Retourne la liste des lignes non-ASCII (index, nombre, detail)."""
    try:
        with io.open(fichier, encoding="utf-8") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        return []
    lignes_bad = []
    for i, ligne in enumerate(lignes, 1):
        mauvais = [ch for ch in ligne if ord(ch) > 127]
        if mauvais:
            uniq = {}
            for ch in mauvais:
                uniq[ch] = uniq.get(ch, 0) + 1
            detail = ", ".join("%s(x%d)" % (ch, n) for ch, n in list(uniq.items())[:5])
            lignes_bad.append((i, len(mauvais), detail))
    return lignes_bad


def main(argv):
    dossier = "."
    dry_run = False
    exclure_extra = ""

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--dry-run":
            dry_run = True
        elif arg == "--exclure":
            if i + 1 < len(argv):
                exclure_extra = argv[i + 1]
                i += 1
        elif arg in ("--help", "-h"):
            afficher_aide()
            return 0
        elif arg == "--version":
            print("valider-conformite-ascii v%s (%s)" % (VERSION, STATUT))
            return 0
        elif arg.startswith("-"):
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        else:
            dossier = arg
        i += 1

    print("=== Valider conformite ASCII stricte ===")
    print("Version : %s" % VERSION)
    print("Dossier : %s" % dossier)
    print("")

    if not os.path.exists(dossier):
        print("[ERREUR] Le chemin n'existe pas : %s" % dossier)
        return 1

    motifs = list(MOTIFS_EXCLUS)
    if exclure_extra:
        motifs += [m.strip() for m in exclure_extra.split(",") if m.strip()]

    fichiers = lister_fichiers(dossier)
    rapports = []
    for fichier in fichiers:
        if any(m in fichier for m in motifs):
            continue
        ext = os.path.splitext(fichier)[1].lower()
        if ext not in EXTENSIONS_VALIDEES:
            continue
        lignes_bad = analyser(fichier)
        if lignes_bad:
            rapports.append((fichier, lignes_bad))

    nb_fichiers = len(rapports)
    nb_lignes = sum(len(lb) for _, lb in rapports)
    nb_caracteres = sum(n for _, lb in rapports for _, n, _ in lb)

    for fichier, lignes_bad in rapports:
        print("  [%s]" % fichier)
        for idx, n, detail in lignes_bad[:5]:
            print("      ligne %d : %d caractere(s) (%s)" % (idx, n, detail))
        if len(lignes_bad) > 5:
            print("      ... et %d autre(s) ligne(s)" % (len(lignes_bad) - 5))

    print("=== Resume ===")
    print("Fichiers non conformes : %d" % nb_fichiers)
    print("Lignes concernees : %d" % nb_lignes)
    print("Caracteres non-ASCII : %d" % nb_caracteres)

    if nb_fichiers == 0:
        print("[OK] Conformite ASCII stricte validee")
        return 0

    print("")
    print("[ATTENTION] Des caracteres non-ASCII ont ete detectes")
    print("Regle immuable : aucun accent, emoji ou symbole Unicode n'est tolere.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
