#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""remplacer-texte.py
Remplacer une liste de paires ancien->nouveau dans plusieurs fichiers d'un dossier.
Usage: remplacer-texte.py <dossier> <ancien1>=<nouveau1> [ancien2=nouveau2 ...] [options]

Options:
  --dry-run   Afficher ce qui SERAIT modifie sans rien ecrire
  --ext       Extensions a traiter (defaut: md,sh,py)
  --exclu-fichier  Nom de fichier a exclure (repetable, defaut: AGENTS-historique.md)
  --exclu-dossier  Nom de dossier a exclure (repetable, defaut: exemples,.git,__pycache__)
  --verbose   Afficher les details (fichiers modifies)
  --help      Afficher cette aide
  --version   Afficher la version

Retour : 0 si au moins une paire a ete appliquee, 1 si AUCUNE paire n'a
         matche (echec explicite : jamais 0 silencieux) ou en cas d'erreur.

Proprietaire : Vulcain (outil partage)
Version : 0.3.1
Statut : prepare
"""

import argparse
import io
import os
import sys

VERSION = "0.3.1"
STATUT = "prepare"

NOM_ATTENDU = "remplacer-texte.py"

# Securite (round 3) : force la sortie en UTF-8 pour ne jamais crasher sur
# l'encodage de la console (cp1252 sous Windows avec des caracteres non-ASCII).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # Python < 3.7 : la console gere l'encodage comme elle peut


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    if nom_script != NOM_ATTENDU:
        print("[ERREUR] Nom de fichier invalide : %s" % nom_script)
        print("  Attendu : %s" % NOM_ATTENDU)
        sys.exit(2)


def lister_fichiers(racine, extensions, exclus_fichiers, exclus_dossiers):
    """Parcourir recursivement et retourner la liste des fichiers a traiter.
    Securite (round 3) : les liens symboliques de fichiers sont IGNORES
    (une ecriture a travers un lien toucherait la cible a l'insu de l'agent)."""
    fichiers = []
    for base, dossiers, noms in os.walk(racine):
        dossiers[:] = [d for d in dossiers if d not in exclus_dossiers]
        for nom in noms:
            if nom in exclus_fichiers:
                continue
            chemin = os.path.join(base, nom)
            if os.path.islink(chemin):
                continue  # securite : jamais d'ecriture a travers un lien
            ext = nom.rsplit('.', 1)[-1] if '.' in nom else ''
            if ext in extensions:
                fichiers.append(chemin)
    return fichiers


def lire_robuste(chemin):
    """Securite (round 3) : lecture UTF-8-sig puis fallback latin-1, jamais de crash."""
    try:
        return io.open(chemin, encoding='utf-8-sig').read()
    except (UnicodeDecodeError, OSError):
        return io.open(chemin, encoding='latin-1').read()


def appliquer(chemin, paires):
    """Appliquer les paires dans l'ordre. Retourne (modifie, contenu, erreur)."""
    try:
        contenu = lire_robuste(chemin)
    except Exception as e:
        return False, None, "lecture impossible: %s" % e
    nouveau = contenu
    for ancien, nouveau_texte in paires:
        nouveau = nouveau.replace(ancien, nouveau_texte)
    return nouveau != contenu, nouveau, None


def main():
    verifier_nommage(os.path.basename(sys.argv[0]))

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('dossier', nargs='?')
    parser.add_argument('paires', nargs='*')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--ext', default='md,sh,py')
    parser.add_argument('--exclu-fichier', action='append', default=['AGENTS-historique.md'])
    parser.add_argument('--exclu-dossier', action='append', default=['exemples', '.git', '__pycache__'])
    parser.add_argument('--verbose', action='store_true')
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

    # Securite (round 3) : octet nul dans le chemin -> refus explicite
    if "\x00" in args.dossier:
        print("[ERREUR] Chemin non sur (octet nul present)")
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
    if args.verbose or args.dry_run:
        for c in modifies:
            mode = "SERAIT MODIFIE" if args.dry_run else "MODIFIE"
            print("  [%s] %s" % (mode, c))
    if args.dry_run:
        print("[DRY-RUN] Aucune modification appliquee")

    if not modifies:
        print("[ERREUR] Aucune paire n'a matche dans le dossier %s" % args.dossier)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
