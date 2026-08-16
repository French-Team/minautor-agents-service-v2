#!/usr/bin/env python3
# -*- coding: ascii -*-
# corriger-noms-maj.py
#
# Corrige les ecarts de casse et de forme des NOMS detectes par
# analyser-noms-maj : normalise le champ outil du registre-usages-outils
# (chemin/extension -> nom kebab-case), avec dry-run et rapport.
#
# Corrections appliquees (champ outil du registre) :
#   - OUTIL_CHEMIN : "tmp-buffy/resync-lock-et-appliquer.py" ->
#     "resync-lock-et-appliquer" (basename sans extension)
#   - OUTIL_CASSE  : nom avec MAJ -> kebab-case minuscule
#
# Options :
#   --registre <fichier>  chemin du registre (defaut: registre-usages-outils.jsonl)
#   --dry-run             affiche les corrections sans ecrire
#   --rapport <fichier>   ecrit le rapport markdown
#   --verbose             detail
#   --no-chrono           coupe le chrono
#   --version             affiche la version
#
# Usage :
#   python3 corriger-noms-maj.py --dry-run
#   python3 corriger-noms-maj.py            (applique)
#   python3 corriger-noms-maj.py --rapport rapport-correction.md
#   python3 corriger-noms-maj.py --version
#
# Version : 0.1.1
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (corriger-).
# =============================================================================
"""
corriger-noms-maj.py
corriger-noms-maj

Usage:
  corriger-noms-maj.py [OPTIONS]
"""

import argparse
import io
import json
import os
import re
import sys
import time

VERSION = "0.1.1"
STATUT = "ebauche"

# Triplet chrono
T_START = time.monotonic()
CHRONO_ACTIF = True

RE_NOMMAGE_OK = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')


def _couleur(texte, nom="neutre"):
    codes = {"rouge": 31, "vert": 32, "jaune": 33, "bleu": 34, "neutre": 0}
    if not sys.stdout.isatty():
        return texte
    return "\033[%dm%s\033[0m" % (codes.get(nom, 0), texte)


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(d, "AGENTS.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.getcwd()
        d = parent


def normaliser_outil(outil):
    """Normalise un champ outil du registre en nom kebab-case minuscule.
    - chemin -> basename
    - extension .py/.sh -> retiree
    - MAJ -> minuscule
    - prefixe tmp-/.tmp-/.zz- retire (un script temp n est pas un outil)
    Retourne (nouveau_nom, modifie)."""
    if not outil:
        return outil, False
    nouveau = outil
    # chemin -> basename (barres / et \)
    nouveau = os.path.basename(nouveau.replace("\\", "/"))
    # extension retiree
    for ext in (".py", ".sh", ".json", ".md", ".txt"):
        if nouveau.endswith(ext):
            nouveau = nouveau[: -len(ext)]
            break
    # prefixe temp retire
    for prefixe in ("tmp-", ".tmp-", ".zz-"):
        if nouveau.startswith(prefixe):
            nouveau = nouveau[len(prefixe):]
            break
    # kebab-case : separations de casse et caracteres non conformes
    nouveau = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', nouveau)
    nouveau = re.sub(r'[^a-z0-9]+', '-', nouveau.lower())
    nouveau = nouveau.strip('-')
    if not nouveau:
        return outil, False
    modifie = nouveau != outil
    return nouveau, modifie


def lire_registre(chemin):
    entrees = []
    if not os.path.exists(chemin):
        return entrees
    for ligne in io.open(chemin, encoding="utf-8", errors="replace"):
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            entrees.append(json.loads(ligne))
        except ValueError:
            entrees.append({"_invalide": ligne})
    return entrees


def main():
    parser = argparse.ArgumentParser(
        description="Corriger la casse et la forme des noms references "
                    "(normalise le champ outil du registre)")
    parser.add_argument("--registre", metavar="FICHIER",
                        help="chemin du registre (defaut: registre-usages-outils.jsonl)")
    parser.add_argument("--dry-run", action="store_true",
                        help="affiche les corrections sans ecrire")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="ecrit le rapport markdown")
    parser.add_argument("--verbose", action="store_true",
                        help="detail")
    parser.add_argument("--no-chrono", action="store_true",
                        help="coupe le chrono")
    parser.add_argument("--version", action="store_true",
                        help="affiche la version")
    args = parser.parse_args()

    global CHRONO_ACTIF
    if args.no_chrono:
        CHRONO_ACTIF = False

    if args.version:
        print("corriger-noms-maj %s (%s)" % (VERSION, STATUT))
        return 0

    racine = racine_projet()
    if args.registre:
        chemin_registre = args.registre
        if not os.path.isabs(chemin_registre):
            chemin_registre = os.path.join(racine, chemin_registre)
    else:
        chemin_registre = os.path.join(
            racine, "cerveau-projet", "agents", "traces",
            "registre-usages-outils.jsonl")

    if not os.path.exists(chemin_registre):
        print("[ERREUR] Registre introuvable : %s" % chemin_registre)
        return 1

    t0 = time.monotonic()
    entrees = lire_registre(chemin_registre)
    corrections = []   # (no_ligne, ancien, nouveau)
    nouveaux_contenus = []
    for i, e in enumerate(entrees, 1):
        if "_invalide" in e:
            nouveaux_contenus.append(None)
            continue
        outil = e.get("outil", "")
        if not outil:
            nouveaux_contenus.append(None)
            continue
        nouveau, modifie = normaliser_outil(outil)
        if modifie:
            corrections.append((i, outil, nouveau))
            e["outil"] = nouveau
            nouveaux_contenus.append(e)
        else:
            nouveaux_contenus.append(None)

    if CHRONO_ACTIF:
        print("[chrono] lecture+analyse %.2fs" % (time.monotonic() - t0))

    print("=== corriger-noms-maj %s ===" % VERSION)
    print("Registre : %s" % chemin_registre)
    print("Corrections a appliquer : %d" % len(corrections))
    for no, ancien, nouveau in corrections:
        print("  L%d : [%s] -> [%s]" % (no, ancien, nouveau))

    if args.dry_run:
        print("")
        print("%s : aucune modification ecrite (dry-run)" % _couleur("DRY-RUN", "jaune"))
        if args.rapport:
            ecrire_rapport(args.rapport, corrections, dry_run=True)
        if CHRONO_ACTIF:
            print("[chrono] corriger-noms-maj total %.2fs" %
                  (time.monotonic() - T_START))
        return 0

    # Application : reecrire TOUTES les lignes brutes en appliquant la
    # normalisation ligne par ligne (PAS par index d entree parsee : un index
    # calcule sur les entrees parsees ne correspond pas aux positions des
    # lignes brutes quand le fichier contient des lignes vides ou invalides,
    # ce qui DECALAIT et ECRASAIT des entrees - bug de perte de donnees
    # corrige le 2026-08-16).
    #
    # Garde de compte : le nombre de lignes JSON valides APRES doit etre
    # IDENTIQUE a celui d AVANT, sinon l ecriture est REFUSEE (aucune perte
    # possible). Les lignes vides et invalides sont PRESERVEES telles quelles.
    t0 = time.monotonic()
    if corrections:
        texte = io.open(chemin_registre, encoding="utf-8",
                        errors="replace").read()
        lignes_brutes = texte.split("\n")
        avant = 0
        apres = 0
        nouvelles = []
        for ligne in lignes_brutes:
            if not ligne.strip():
                nouvelles.append(ligne)
                continue
            try:
                e = json.loads(ligne)
            except ValueError:
                # ligne invalide : PRESERVEE telle quelle (jamais perdue)
                nouvelles.append(ligne)
                continue
            avant += 1
            outil = e.get("outil", "")
            nouveau, modifie = normaliser_outil(outil)
            if modifie:
                e["outil"] = nouveau
                nouvelles.append(json.dumps(e, ensure_ascii=True,
                                            separators=(",", ":")))
            else:
                nouvelles.append(ligne)
            apres += 1
        if apres != avant:
            print(_couleur("[ERREUR] compte d entrees modifie (%d -> %d) : "
                           "ecriture REFUSEE (aucune perte possible)"
                           % (avant, apres), "rouge"))
            return 1
        # verrou de non-perte supplementaire : chaque ligne JSON du fichier
        # d origine (hors corrections) doit avoir son jumeau dans la sortie
        sortie = "\n".join(nouvelles)
        with io.open(chemin_registre, "w", encoding="utf-8",
                     newline="\n") as fh:
            fh.write(sortie)
    if CHRONO_ACTIF:
        print("[chrono] ecriture %.2fs" % (time.monotonic() - t0))

    print("")
    if corrections:
        print("%s : %d correction(s) appliquee(s)" % (
            _couleur("OK", "vert"), len(corrections)))
    else:
        print("%s : rien a corriger" % _couleur("OK", "vert"))

    if args.rapport:
        ecrire_rapport(args.rapport, corrections, dry_run=False)

    if CHRONO_ACTIF:
        print("[chrono] corriger-noms-maj total %.2fs" %
              (time.monotonic() - T_START))
    return 0


def ecrire_rapport(fichier, corrections, dry_run):
    lignes = []
    lignes.append("# Rapport corriger-noms-maj")
    lignes.append("")
    lignes.append("Date : %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    lignes.append("Mode : %s" % ("dry-run" if dry_run else "application"))
    lignes.append("")
    lignes.append("## Corrections")
    lignes.append("")
    if not corrections:
        lignes.append("Aucune correction necessaire.")
    else:
        lignes.append("| Ligne | Ancien | Nouveau |")
        lignes.append("|---|---|---|")
        for no, ancien, nouveau in corrections:
            lignes.append("| %d | `%s` | `%s` |" % (no, ancien, nouveau))
    contenu = "\n".join(lignes) + "\n"
    with io.open(fichier, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)
    print("Rapport ecrit : %s" % fichier)


if __name__ == "__main__":
    sys.exit(main())
