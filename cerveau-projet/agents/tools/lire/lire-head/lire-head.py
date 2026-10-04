#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
lire-head.py
Lire le head (en-tete) de un ou plusieurs fichiers, sans configurer le
nombre de lignes : l'outil detecte automatiquement la fin du head
(front-matter YAML, bloc de commentaires, ou premiere ligne vide) et
affiche systematiquement TOUT le contenu du head. Mode comparaison :
rechercher une information commune dans plusieurs heads et reperer
celui qui n'est pas a jour.

Usage:
  lire-head.py [OPTIONS] <fichier> [fichier2 ...]

Options:
  --info-commune MOTIF   Chercher un motif (texte) dans chaque head et
                         afficher PRESENT/ABSENT par fichier
  --lignes N             Forcer la lecture de N lignes (derogation a la
                         detection automatique)
  --max-lignes N         Borne de securite de la detection (defaut 100)
  --verbose              Afficher les details (mode de detection, lignes)
  --dry-run              Simuler sans afficher le contenu (decouverte)
  --version              Afficher la version
  --aide, -h             Afficher cette aide

Retour: 0 si succes, 1 si erreur (fichier introuvable), 2 si usage invalide.

Proprietaire : Vulcain (constructeur d'outils)
Version : 0.1.1
Statut : ebauche
"""

import argparse
import os
import sys

VERSION = "0.1.1"
STATUT = "ebauche"

# Securite : force la sortie en UTF-8 pour ne jamais crasher sur l'encodage
# de la console (cp1252 sous Windows avec des caracteres non-ASCII).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"

# Marqueurs de commentaires courants pour la detection d'un bloc d'en-tete
MARQUEURS_COMMENTAIRES = ("#", "//", ";", "*", "--", "%", "REM ", "/*")

# Bornes
MAX_LIGNES_DEFAUT = 100


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "lire-head.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def verifier_chemin_sur(chemin):
    """Securite : refuse un chemin contenant un octet nul."""
    if "\x00" in chemin:
        print(RED + "[ERREUR] Chemin non sur (octet nul present)" + NC)
        sys.exit(1)


def decoder_ligne(octets):
    """Decode une ligne sans jamais crasher : UTF-8-sig (BOM nettoye) puis
    latin-1 en secours (decode toujours). Les lignes purement ASCII sont
    identiques dans les deux encodages : le resultat est donc exact."""
    try:
        return octets.decode("utf-8-sig")
    except UnicodeDecodeError:
        return octets.decode("latin-1")


def lire_lignes(fichier):
    """Lit toutes les lignes du fichier (mode binaire + decodage robuste)."""
    lignes = []
    try:
        with open(fichier, "rb") as f:
            for octets in f:
                lignes.append(decoder_ligne(octets).rstrip("\r\n"))
    except OSError as e:
        print(RED + "[ERREUR] Lecture impossible: " + str(e) + NC)
        return None
    return lignes


def detecter_fin_head(lignes, max_lignes, verbose):
    """Detecte automatiquement la fin du head et retourne le nombre de
    lignes a afficher. Strategie (dans l'ordre) :
      1. Front-matter YAML : premiere ligne '---' -> fin a la ligne
         de fermeture '---' ou '...'
      2. Bloc de commentaires d'en-tete : lignes qui commencent par un
         marqueur de commentaire -> le head continue tant que les lignes
         sont des commentaires (une ligne vide est toleree si la suivante
         est encore un commentaire)
      3. Fallback : jusqu'a la premiere ligne vide (titre + description),
         borne par max_lignes
    """
    n = len(lignes)
    if n == 0:
        return 0

    # Ignorer les eventuelles lignes vides initiales
    i = 0
    while i < n and lignes[i].strip() == "":
        i += 1
    if i >= n:
        return 0

    # Cas 1 : front-matter YAML
    if lignes[i].strip() == "---":
        if verbose:
            print(BLUE + "[INFO] Mode de detection : front-matter YAML" + NC)
        for j in range(i + 1, min(n, max_lignes)):
            if lignes[j].strip() in ("---", "..."):
                return j + 1  # inclure la ligne de fermeture
        # Pas de fermeture trouvee : couper a max_lignes
        if verbose:
            print(YELLOW + "[INFO] Front-matter non ferme : coupe a " +
                  str(max_lignes) + " lignes" + NC)
        return min(n, i + max_lignes)

    # Cas 2 : bloc de commentaires d'en-tete
    if lignes[i].strip().startswith(MARQUEURS_COMMENTAIRES):
        if verbose:
            print(BLUE + "[INFO] Mode de detection : bloc de commentaires" + NC)
        j = i
        while j < n and j < max_lignes:
            ligne = lignes[j].strip()
            if ligne == "":
                # Ligne vide : continuer seulement si la suivante est encore
                # un commentaire (le bloc peut contenir des lignes vides)
                if j + 1 < n and lignes[j + 1].strip().startswith(
                        MARQUEURS_COMMENTAIRES):
                    j += 1
                    continue
                break
            if ligne.startswith(MARQUEURS_COMMENTAIRES):
                j += 1
                continue
            break
        return j

    # Cas 3 : fallback - jusqu'a la premiere ligne vide
    if verbose:
        print(BLUE + "[INFO] Mode de detection : premiere ligne vide" + NC)
    j = i
    while j < n and j < max_lignes and lignes[j].strip() != "":
        j += 1
    if j == max_lignes and j < n and lignes[j].strip() != "":
        if verbose:
            print(YELLOW + "[INFO] Borne --max-lignes atteinte (" +
                  str(max_lignes) + " lignes)" + NC)
    return j


def afficher_head(chemin, lignes, nb_lignes, verbose):
    """Affiche le head d'un fichier."""
    print(GREEN + "=== HEAD : " + chemin + " ===" + NC)
    if nb_lignes == 0:
        print(YELLOW + "(fichier vide ou sans contenu)" + NC)
        return
    for num in range(nb_lignes):
        print(lignes[num])
    if verbose:
        print(BLUE + "[INFO] " + str(nb_lignes) + " lignes lues" + NC)
    print("")


def chercher_info_commune(chemin, lignes, nb_lignes, motif):
    """Cherche le motif dans le head et retourne (present, lignes_trouvees)."""
    trouves = []
    for num in range(nb_lignes):
        if motif in lignes[num]:
            trouves.append(num + 1)
    return (len(trouves) > 0, trouves)


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lire-head.py",
        description="Lire le head (en-tete) de fichiers sans configurer le "
                    "nombre de lignes, et comparer plusieurs heads.",
        add_help=False,
    )
    parser.add_argument("fichiers", nargs="*", default=[],
                        help="Fichiers a lire (un ou plusieurs)")
    parser.add_argument("--info-commune", type=str, default=None,
                        help="Chercher un motif dans chaque head (PRESENT/ABSENT)")
    parser.add_argument("--lignes", type=int, default=None,
                        help="Forcer la lecture de N lignes (derogation)")
    parser.add_argument("--max-lignes", type=int, default=MAX_LIGNES_DEFAUT,
                        help="Borne de securite de la detection (defaut 100)")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans afficher le contenu")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.aide:
        construire_parser().print_help()
        return 0
    if args.version:
        print("lire-head.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if not args.fichiers:
        print(RED + "[ERREUR] Aucun fichier specifie" + NC)
        construire_parser().print_help()
        return 1

    if args.max_lignes < 1:
        print(RED + "[ERREUR] --max-lignes doit etre >= 1 (recu: " +
              str(args.max_lignes) + ")" + NC)
        return 1
    if args.lignes is not None and args.lignes < 1:
        print(RED + "[ERREUR] --lignes doit etre >= 1 (recu: " +
              str(args.lignes) + ")" + NC)
        return 1

    # Verifier que tous les fichiers existent avant de lire
    for chemin in args.fichiers:
        verifier_chemin_sur(chemin)
        if not os.path.isfile(chemin):
            print(RED + "[ERREUR] Fichier non trouve: " + chemin + NC)
            return 1

    if args.dry_run:
        print(YELLOW + "[DRY-RUN] Fichiers a lire : " +
              str(len(args.fichiers)) + NC)
        for chemin in args.fichiers:
            print("  - " + chemin)
        return 0

    resultats = []
    for chemin in args.fichiers:
        lignes = lire_lignes(chemin)
        if lignes is None:
            return 1
        if args.lignes is not None:
            nb = min(args.lignes, len(lignes))
            mode = "force (--lignes " + str(args.lignes) + ")"
        else:
            nb = detecter_fin_head(lignes, args.max_lignes, args.verbose)
            mode = "automatique"
        if args.verbose:
            print(BLUE + "[INFO] " + chemin + " : detection " + mode + NC)
        afficher_head(chemin, lignes, nb, args.verbose)
        resultats.append((chemin, lignes, nb))

    # Mode comparaison : information commune
    if args.info_commune is not None:
        print(GREEN + "=== COMPARAISON : information commune '" +
              args.info_commune + "' ===" + NC)
        tous_presents = True
        for chemin, lignes, nb in resultats:
            present, trouves = chercher_info_commune(
                chemin, lignes, nb, args.info_commune)
            if present:
                print(GREEN + "  [PRESENT] " + chemin +
                      " (lignes " + ",".join(str(t) for t in trouves) + ")" + NC)
            else:
                print(RED + "  [ABSENT] " + chemin + NC)
                tous_presents = False
        if tous_presents:
            print(GREEN + "=> Tous les heads contiennent l'information." + NC)
        else:
            print(YELLOW + "=> Au moins un head ne contient PAS l'information "
                  "(fichier probablement pas a jour)." + NC)

    return 0


if __name__ == "__main__":
    sys.exit(main())
