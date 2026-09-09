"""Categorie perimetre : reduit (ou restaure) le perimetre de lecture cameleon."""
from commun import lire_perimetre
from constants import CLE_PERIMETRE
from perimetre.fonctions import ecrire_perimetre, normaliser_zones

NOMS_OPTIONS = ("zones",)


def executer(arguments):
    options = {}
    index = 0
    while index < len(arguments):
        if arguments[index] == "--zones" and index + 1 < len(arguments):
            options["zones"] = arguments[index + 1]
            index += 2
        else:
            index += 1
    if "zones" not in options:
        print('Usage : python main.py perimetre --zones "matrice/confidentiel,donnees-privees"')
        print("        (liste vide --zones \"\" = perimetre complet restaure)")
        return 2

    zones = normaliser_zones(options["zones"])
    ecrire_perimetre(zones)
    if zones:
        print("Perimetre cameleon REDUIT (cle '" + CLE_PERIMETRE + "' du classeur) :")
        for zone in zones:
            print("  - " + zone + " (exclue de SA lecture)")
    else:
        print("Perimetre cameleon RESTAURE : aucune zone exclue (cle '" + CLE_PERIMETRE + "' vide).")
    return 0
