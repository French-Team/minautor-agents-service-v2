#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
verifier-restauration-sure.py

Detecte les fichiers non commites avant toute restauration git (git status
automatique). Applique la regle Restauration securisee (regles-general-global.md
+ protocole-gestion-defaillances Etape 3) : JAMAIS de git checkout / git restore
/ git reset --hard sur des fichiers NON COMMITES.

Mode --fichier <chemin> : verifie si LE fichier cible a des modifications non
  commitees (code 0 = sur / non-modifie, code 1 = non-commite detecte).
Mode global (sans --fichier) : liste tous les fichiers non commites du workspace
  et rend un verdict (OK si aucun, ATTENTION sinon avec rappel de la regle).

Utilisation:
  verifier-restauration-sure.py [OPTIONS]

Options:
  --fichier CHEMIN   Verifier un fichier specifique (relatif a la racine du workspace)
  --verbose          Afficher le detail des fichiers non commites
  --version          Afficher la version
  --aide, -h         Afficher cette aide

Proprietaire : Vulcain (outil partage)
Version : 0.1.0
Statut : prepare
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

VERSION = "0.1.0"
STATUT = "prepare"

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


def verifier_nommage(script_path):
    """Verifie que le nom du fichier commence par le prefixe du dossier de categorie."""
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print("ERREUR: nommage invalide - le fichier doit commencer par '%s' (dossier %s)" % (prefixe, dossier))
        sys.exit(2)


def racine_workspace():
    """Retourne la racine du workspace (dossier contenant le .git)."""
    courant = Path.cwd()
    for parent in [courant] + list(courant.parents):
        if (parent / ".git").exists() or (parent / ".git").is_dir():
            return parent
    return courant


def git_status_porcelain(racine):
    """Retourne la liste des lignes de git status --porcelain (non commitees)."""
    try:
        resultat = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(racine),
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception as exc:
        print("ERREUR: impossible d'executer git status --porcelain: %s" % exc)
        sys.exit(3)
    if resultat.returncode != 0:
        print("ERREUR: git status a echoue: %s" % resultat.stderr.strip())
        sys.exit(3)
    lignes = [l for l in resultat.stdout.splitlines() if l.strip()]
    return lignes


def parser_lignes(lignes):
    """Decoupe chaque ligne porcelain en (code_status, chemin)."""
    fichiers = []
    for ligne in lignes:
        if len(ligne) < 4:
            continue
        code = ligne[:2]
        chemin = ligne[3:].strip()
        # enlever les guillemets des noms avec espaces et le suffixe ->/ pour les renommages
        if chemin.startswith('"') and chemin.endswith('"'):
            chemin = chemin[1:-1]
        fichiers.append((code, chemin))
    return fichiers


def rappel_regle():
    return ("REGLE RESTAURATION SECURISEE : JAMAIS de git checkout / git restore / "
            "git reset --hard si des fichiers non commites existent. Verifier git status "
            "avant, sauvegarder (cp) ou git stash.")


def mode_global(verbose):
    racine = racine_workspace()
    lignes = git_status_porcelain(racine)
    fichiers = parser_lignes(lignes)
    if not fichiers:
        print(_couleur("[OK] AUCUN fichier non commite - la restauration git est sure.", "vert"))
        print("Rappel : verifier quand meme git status avant toute restauration (regle immuable).")
        return 0
    print(_couleur("[ATTENTION] %d fichier(s) non commite(s) - restauration git INTERDITE." % len(fichiers), "rouge"))
    print("Fichiers non commites :")
    for code, chemin in fichiers:
        print("  [%s] %s" % (code, chemin))
    print()
    print(rappel_regle())
    return 1


def mode_fichier(chemin_cible, verbose):
    racine = racine_workspace()
    cible = (racine / chemin_cible).resolve()
    lignes = git_status_porcelain(racine)
    fichiers = parser_lignes(lignes)
    # normaliser : chemin cible relatif au workspace, avec separateurs /
    try:
        relatif = cible.relative_to(racine.resolve()).as_posix()
    except ValueError:
        print("ERREUR: le fichier '%s' est hors du workspace." % chemin_cible)
        sys.exit(2)
    touches = [(code, ch) for code, ch in fichiers if ch.rstrip("/") == relatif]
    if not touches:
        print(_couleur("[OK] Le fichier '%s' est SUR (aucune modification non commitee)." % relatif, "vert"))
        print("Rappel : verifier git status avant toute restauration globale.")
        return 0
    print(_couleur("[ATTENTION] Le fichier '%s' a des modifications NON COMMITEES :" % relatif, "rouge"))
    for code, ch in touches:
        print("  [%s] %s" % (code, ch))
    print()
    print(rappel_regle())
    return 1


def main():
    verifier_nommage(__file__)
    parser = argparse.ArgumentParser(
        description="Detecte les fichiers non commites avant toute restauration git (regle Restauration securisee).",
        add_help=False,
    )
    parser.add_argument("--fichier", dest="fichier", default=None, help="Verifier un fichier specifique")
    parser.add_argument("--verbose", action="store_true", help="Afficher le detail")
    parser.add_argument("--version", action="store_true", help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true", help="Afficher cette aide")
    args = parser.parse_args()

    if args.aide:
        print(__doc__)
        return 0
    if args.version:
        print("verifier-restauration-sure v%s (%s)" % (VERSION, STATUT))
        return 0
    if args.fichier:
        return mode_fichier(args.fichier, args.verbose)
    return mode_global(args.verbose)


if __name__ == "__main__":
    sys.exit(main())
