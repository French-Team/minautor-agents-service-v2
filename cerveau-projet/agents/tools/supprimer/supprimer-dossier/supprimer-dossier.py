#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
supprimer-dossier.py

Supprimer un dossier recursivement (avec protections).

Options:
  --force         Executer la suppression (sans : dry-run)
  --verbose       Afficher les details
  --help          Afficher cette aide

Protections:
  - Refus des chemins sensibles (/, ., .., racine du projet, tools/)
  - Dry-run par defaut : il faut --force pour supprimer reellement

Proprietaire : Buffy (outil partage)
Version : 0.2.1-py
Statut : prepare
"""

import os
import shutil
import sys

VERSION = "0.2.1-py"
STATUT = "prepare"

CHEMINS_SENSIBLES = {"", "/", ".", "..", "./", "../"}
DOSSIER_OUTILS = "cerveau-projet/agents/tools"


def afficher_aide():
    print("=== supprimer-dossier v%s ===" % VERSION)
    print("")
    print("Usage: supprimer-dossier.py [OPTIONS] <dossier>")
    print("")
    print("Arguments :")
    print("  <dossier>       Dossier a supprimer (recursif)")
    print("")
    print("Options :")
    print("  --force         Executer la suppression (sans : dry-run)")
    print("  --verbose       Afficher les details")
    print("  --help          Afficher cette aide")
    print("")
    print("Exemples :")
    print("  supprimer-dossier.py dossier-temporaire          # Dry-run")
    print("  supprimer-dossier.py --force dossier-temporaire  # Suppression reelle")


def verrouiller_habilitation(agent, outil, audit=False):
    """Appelle proteger-verrou-habilitation et retourne (code, message).
    Source de verite : les cartes de decision (aucune liste en dur).
    audit=True (v0.2.0) : mode tests - pas de verification d identite reelle."""
    import subprocess
    courant = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, "AGENTS.md")):
            break
        parent = os.path.dirname(courant)
        if parent == courant:
            return (2, "[ERREUR] Racine du projet introuvable (AGENTS.md absent)")
        courant = parent
    verrou = os.path.join(
        courant, "cerveau-projet", "agents", "tools", "proteger",
        "proteger-verrou-habilitation", "proteger-verrou-habilitation.py")
    if not os.path.isfile(verrou):
        return (2, "[ERREUR] Verrou introuvable : %s" % verrou)
    cmd = [sys.executable, verrou, "--agent", agent, "--outil", outil]
    if audit:
        cmd.append("--audit")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    message = (r.stdout + r.stderr).strip()
    return (r.returncode, message)


def main(argv):
    dossier = ""
    agent = ""
    audit = False
    force = False
    verbose = False
    help_demande = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--force":
            force = True
            i += 1
            continue
        if arg in ("--verbose", "-v"):
            verbose = True
            i += 1
            continue
        if arg in ("--help", "--aide", "-h"):
            help_demande = True
            i += 1
            continue
        if arg == "--audit":
            audit = True
            i += 1
            continue
        if arg == "--agent":
            if i + 1 >= len(argv):
                print("[ERREUR] --agent requiert un nom d agent")
                return 2
            agent = argv[i + 1]
            i += 2
            continue
        if arg == "--version":
            print("supprimer-dossier v%s (%s)" % (VERSION, STATUT))
            return 0
        if dossier:
            print("[ERREUR] Trop d'arguments: %s" % arg)
            afficher_aide()
            return 1
        dossier = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not dossier:
        print("[ERREUR] Aucun dossier specifie")
        afficher_aide()
        return 1

    # VERROU D HABILITATION (regle immuable : seul hygie supprime). --agent
    # est OBLIGATOIRE et le verrou est appele AVANT toute action : si l agent
    # n est pas habilite, la suppression est refusee et le message indique
    # QUI est habilite (cycle Cerberus -> agent).
    if not agent:
        print("[ERREUR] --agent est OBLIGATOIRE : l outil doit connaitre "
              "l agent appelant (verrou d habilitation).")
        return 2
    code, message = verrouiller_habilitation(agent, "supprimer-dossier", audit=audit)
    if code != 0:
        print(message)
        return 1 if code == 1 else 2

    if not os.path.isdir(dossier):
        print("[ERREUR] Dossier non trouve ou pas un dossier: %s" % dossier)
        return 1

    # Normaliser le chemin (supprimer les / finaux)
    dossier = dossier.rstrip("/\\")

    # PROTECTION : chemins sensibles absolument interdits
    if dossier in CHEMINS_SENSIBLES:
        print("[ERREUR] Suppression interdite de ce chemin sensible: %s" % dossier)
        return 1

    # PROTECTION : ne pas supprimer la racine du projet ni le dossier des outils
    cible_abs = os.path.abspath(dossier)
    if cible_abs == os.path.abspath("."):
        print("[ERREUR] Refus : ce dossier est la racine du projet")
        return 1
    if cible_abs == os.path.abspath(DOSSIER_OUTILS):
        print("[ERREUR] Refus : ce dossier contient les outils partages")
        return 1

    nb_fichiers = 0
    nb_dossiers = 0
    for racine, dossiers, fichiers in os.walk(dossier):
        nb_fichiers += len(fichiers)
        nb_dossiers += len(dossiers)

    if verbose:
        print("[INFO] Dossier cible: %s" % dossier)
        print("[INFO] Contenu: %d fichiers, %d sous-dossiers" % (nb_fichiers, nb_dossiers))

    if not force:
        print("[DRY-RUN] Aucune suppression effectuee (utiliser --force pour executer)")
        print("[INFO] %d fichiers et %d dossiers seraient supprimes" % (nb_fichiers, nb_dossiers))
        return 0

    try:
        shutil.rmtree(dossier)
    except OSError:
        print("[ERREUR] La suppression a echoue")
        return 1

    print("[OK] Dossier supprime : %s (%d fichiers, %d dossiers)" % (dossier, nb_fichiers, nb_dossiers))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
