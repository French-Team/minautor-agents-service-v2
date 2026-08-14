#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
gerer-sous-mission.py
Gere les sorties et retrees du flux principal (sous-missions).

Commandes:
  sauvegarder    Sauvegarder la position actuelle (fichier JSON)
  sortir         Marquer la sortie du flux principal
  revenir        Marquer le retour au flux principal
  lister         Lister les sous-missions et positions
  aide           Afficher cette aide

Usage:
  gerer-sous-mission.py sauvegarder --mission DESCRIPTION --etape NUMERO [--donnees DONNEES]
  gerer-sous-mission.py sortir --raison RAISON --outil OUTIL
  gerer-sous-mission.py revenir --resultat succes/echec --outil-cree oui/non
  gerer-sous-mission.py lister

Retour: 0 si succes, 1 si erreur.

Proprietaire : Buffy (outil partage)
Version : 0.2.0-py
Statut : beta
"""

import argparse
import datetime
import json
import os
import re
import sys

VERSION = "0.2.0-py"
STATUT = "beta"

# Couleurs ANSI
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
NC = "\033[0m"  # No Color

DOSSIER_SAUVEGARDES = "cerveau-projet/agents/vulcain/sauvegardes"


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    attendu = "gerer-sous-mission.py"
    if nom_script != attendu:
        print(RED + "[ERREUR] Nom de fichier invalide : " + nom_script + NC)
        print(YELLOW + "  Attendu : " + attendu + NC)
        sys.exit(2)


def creer_dossier_sauvegardes():
    """Cree le dossier de sauvegardes s'il n'existe pas."""
    os.makedirs(DOSSIER_SAUVEGARDES, exist_ok=True)


def commande_sauvegarder(args):
    """Sauvegarde la position actuelle dans un fichier JSON."""
    if not args.mission or not args.etape:
        print("Erreur: --mission et --etape sont obligatoires")
        return 1

    creer_dossier_sauvegardes()

    date_format = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = re.sub(r"\s+", "_", args.mission.strip().lower())
    fichier = os.path.join(DOSSIER_SAUVEGARDES,
                           nom_fichier + "_" + date_format + ".json")

    donnees = {
        "mission": args.mission,
        "etape": args.etape,
        "donnees": args.donnees,
        "date_sauvegarde": datetime.datetime.now().isoformat(),
        "sous_missions": [],
    }
    # FIGER LF : newline='' evite la traduction CRLF Windows
    with open(fichier, "w", encoding="utf-8", newline="") as f:
        json.dump(donnees, f, ensure_ascii=True, indent=2)

    print(GREEN + "[OK] Position sauvegardee" + NC)
    print("- Mission : " + args.mission)
    print("- Etape : " + args.etape)
    print("- Donnees : " + args.donnees)
    print("- Fichier : " + fichier)
    return 0


def commande_sortir(args):
    """Marque la sortie du flux principal."""
    if not args.raison or not args.outil:
        print("Erreur: --raison et --outil sont obligatoires")
        return 1

    print(YELLOW + "[ROTATION] Sortie du flux principal" + NC)
    print("- Raison : " + args.raison)
    print("- Outil necessaire : " + args.outil)
    print("- Sous-mission : Creer/reprendre " + args.outil)
    print("")
    print(CYAN + "Utilisez gerer-sous-mission.py revenir une fois la sous-mission terminee" + NC)
    return 0


def commande_revenir(args):
    """Marque le retour au flux principal."""
    if not args.resultat or not args.outil_cree:
        print("Erreur: --resultat et --outil-cree sont obligatoires")
        return 1

    print(GREEN + "[OK] Retour au flux principal" + NC)
    print("- Resultat : " + args.resultat)
    print("- Outil cree : " + args.outil_cree)
    print("")

    if args.resultat == "succes" and args.outil_cree == "oui":
        print(GREEN + "L'outil est maintenant disponible !" + NC)
    elif args.resultat == "echec":
        print(RED + "La sous-mission a echoue." + NC)
    return 0


def commande_lister(args):
    """Liste les sauvegardes de sous-missions."""
    creer_dossier_sauvegardes()

    print(BLUE + "[CHECKLIST] Sous-missions et positions sauvegardees" + NC)
    print("")

    fichiers = []
    if os.path.isdir(DOSSIER_SAUVEGARDES):
        for nom in sorted(os.listdir(DOSSIER_SAUVEGARDES)):
            if nom.endswith(".json"):
                fichiers.append(os.path.join(DOSSIER_SAUVEGARDES, nom))
    fichiers = fichiers[:10]

    if not fichiers:
        print("Aucune sauvegarde trouvee.")
        return 0

    for i, fichier in enumerate(fichiers, 1):
        print(CYAN + "--- Sauvegarde " + str(i) + " ---" + NC)
        print("Fichier : " + fichier)
        print("")
        try:
            with open(fichier, encoding="utf-8") as f:
                donnees = json.load(f)
            mission = donnees.get("mission", "")
            etape = donnees.get("etape", "")
            date_sauvegarde = donnees.get("date_sauvegarde", "")
        except (OSError, ValueError):
            mission, etape, date_sauvegarde = "", "", ""
        print("Mission : " + mission)
        print("Etape : " + etape)
        print("Date : " + date_sauvegarde)
        print("")
    return 0


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="gerer-sous-mission.py",
        description="Gere les sorties et retrees du flux principal (sous-missions).",
        add_help=False,
    )
    subparsers = parser.add_subparsers(dest="commande")

    p_sauvegarder = subparsers.add_parser("sauvegarder", add_help=False)
    p_sauvegarder.add_argument("--mission", default="",
                               help="Description de la mission (obligatoire)")
    p_sauvegarder.add_argument("--etape", default="",
                               help="Numero de l'etape en cours (obligatoire)")
    p_sauvegarder.add_argument("--donnees", default="",
                               help="Donnees collectees")

    p_sortir = subparsers.add_parser("sortir", add_help=False)
    p_sortir.add_argument("--raison", default="",
                          help="Raison de la sortie (obligatoire)")
    p_sortir.add_argument("--outil", default="",
                          help="Outil necessaire (obligatoire)")

    p_revenir = subparsers.add_parser("revenir", add_help=False)
    p_revenir.add_argument("--resultat", default="",
                           help="Resultat: succes/echec (obligatoire)")
    p_revenir.add_argument("--outil-cree", default="",
                           help="Outil cree: oui/non (obligatoire)")

    subparsers.add_parser("lister", add_help=False)

    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main(argv=None):
    verifier_nommage(os.path.basename(sys.argv[0]))
    args = construire_parser().parse_args(argv)

    if args.version:
        print("gerer-sous-mission.py v" + VERSION + " (" + STATUT + ")")
        return 0

    if args.aide or not args.commande:
        construire_parser().print_help()
        return 0

    if args.commande == "sauvegarder":
        return commande_sauvegarder(args)
    if args.commande == "sortir":
        return commande_sortir(args)
    if args.commande == "revenir":
        return commande_revenir(args)
    if args.commande == "lister":
        return commande_lister(args)

    print("Commande inconnue: " + args.commande)
    print("Utilisez 'gerer-sous-mission.py aide' pour l'aide")
    return 1


if __name__ == "__main__":
    sys.exit(main())
