#!/usr/bin/env python3
# -*- coding: ascii -*-
"""remplacer-texte.py
Remplacer une liste de paires ancien->nouveau dans plusieurs fichiers d'un dossier.
Usage: remplacer-texte.py <dossier> <ancien1>=<nouveau1> [ancien2=nouveau2 ...] [options]

Options:
  --dry-run   Afficher ce qui SERAIT modifie sans rien ecrire
  --ext       Extensions a traiter (defaut: md,sh,py)
  --exclu-fichier  Nom de fichier a exclure (repetable, defaut: AGENTS-historique.md)
  --exclu-dossier  Nom de dossier a exclure (repetable, defaut: exemples,.git,__pycache__)
  --help      Afficher cette aide
"""

import argparse
import io
import os
import sys

VERSION = "0.1.0-beta"
STATUT = "ebauche"


def lister_fichiers(racine, extensions, exclus_fichiers, exclus_dossiers):
    """Parcourir recursivement et retourner la liste des fichiers a traiter."""
    fichiers = []
    for base, dossiers, noms in os.walk(racine):
        dossiers[:] = [d for d in dossiers if d not in exclus_dossiers]
        for nom in noms:
            if nom in exclus_fichiers:
                continue
            ext = nom.rsplit('.', 1)[-1] if '.' in nom else ''
            if ext in extensions:
                fichiers.append(os.path.join(base, nom))
    return fichiers


def appliquer(chemin, paires):
    """Appliquer les paires dans l'ordre. Retourne (modifie, contenu)."""
    try:
        contenu = io.open(chemin, encoding='utf-8').read()
    except Exception as e:
        return False, None, "lecture impossible: %s" % e
    nouveau = contenu
    for ancien, nouveau_texte in paires:
        nouveau = nouveau.replace(ancien, nouveau_texte)
    return nouveau != contenu, nouveau, None


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('dossier', nargs='?')
    parser.add_argument('paires', nargs='*')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--ext', default='md,sh,py')
    parser.add_argument('--exclu-fichier', action='append', default=['AGENTS-historique.md'])
    parser.add_argument('--exclu-dossier', action='append', default=['exemples', '.git', '__pycache__'])
    parser.add_argument('--help', action='store_true')
    parser.add_argument('--version', action='store_true')
    args = parser.parse_args()

    if args.help:
        print(__doc__)
        sys.exit(0)
    if args.version:
        print("remplacer-texte v%s (%s)" % (VERSION, STATUT))
        sys.exit(0)
    if not args.dossier:
        print("[ERREUR] Aucun dossier fourni")
        print("Exemple: remplacer-texte.py dossier 'ancien=nouveau'")
        sys.exit(1)

    if not args.paires:
        print("[ERREUR] Aucune paire ancien=nouveau fournie")
        print("Exemple: remplacer-texte.py dossier 'ancien=nouveau'")
        sys.exit(1)
    if not os.path.isdir(args.dossier):
        print("[ERREUR] Dossier introuvable: %s" % args.dossier)
        sys.exit(1)

    paires = []
    for p in args.paires:
        if '=' not in p:
            print("[ERREUR] Paire invalide (format ancien=nouveau): %s" % p)
            sys.exit(1)
        ancien, nouveau_texte = p.split('=', 1)
        paires.append((ancien, nouveau_texte))

    extensions = set(e.strip().lstrip('.') for e in args.ext.split(',') if e.strip())
    fichiers = lister_fichiers(args.dossier, extensions,
                               set(args.exclu_fichier), set(args.exclu_dossier))

    modifies = []
    analyses = 0
    for chemin in fichiers:
        analyses += 1
        modifie, contenu, erreur = appliquer(chemin, paires)
        if erreur:
            print("[ERREUR] %s: %s" % (chemin, erreur))
            continue
        if modifie:
            modifies.append(chemin)
            if not args.dry_run:
                io.open(chemin, 'w', encoding='utf-8', newline='').write(contenu)

    print("=== remplacer-texte v%s ===" % VERSION)
    print("Fichiers analyses: %d | Modifies: %d" % (analyses, len(modifies)))
    for c in modifies:
        mode = "SERAIT MODIFIE" if args.dry_run else "MODIFIE"
        print("  [%s] %s" % (mode, c))
    if args.dry_run:
        print("[DRY-RUN] Aucune modification appliquee")


if __name__ == '__main__':
    main()
