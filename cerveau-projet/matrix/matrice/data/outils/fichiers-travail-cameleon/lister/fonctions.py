"""Fonctions de la categorie lister : la VUE de la zone du cameleon."""

import json

from commun import chemin_relatif, elements_zone, journal_lire
from constants import ACTION_CREE, ACTION_PURGE


def afficher_lister(zone, elements, mission_filtre=None):
    """La VUE de la zone : chaque element, sa classe, et le compte par classe."""
    lignes = ["ZONE : " + chemin_relatif(zone)]
    vus = elements
    hors_filtre = []
    if mission_filtre:
        mission_filtre = mission_filtre.strip().lower()
        vus = [element for element in elements if element["mission"] == mission_filtre]
        hors_filtre = [element for element in elements if element["mission"] != mission_filtre]
    if not elements:
        lignes.append("  (zone vide : aucun fichier de travail, aucun residu)")
        return lignes
    for element in vus:
        marque = "dossier" if element["dossier"] else str(element["taille"]) + " o"
        lignes.append("  [" + element["classe"].upper() + "] " + element["nom"]
                      + "  (" + marque + ", " + element["modifie"] + ")")
    comptes = {}
    for element in elements:
        comptes[element["classe"]] = comptes.get(element["classe"], 0) + 1
    lignes.append("  TOTAL : " + str(len(elements)) + " element(s) -- "
                  + ", ".join(cle + " " + str(valeur) for cle, valeur in sorted(comptes.items())))
    if mission_filtre is not None:
        lignes.append("  HORS FILTRE (" + str(mission_filtre) + ") : " + str(len(hors_filtre))
                      + " element(s) -- aucun n est cache")
    return lignes


def executer_lister(zone, chemin_journal, mission_filtre, strict, as_json):
    """Rend la vue (ou le JSON) de la zone ; code 1 si --strict devant un ecart."""
    elements = elements_zone(zone, chemin_journal)
    if as_json:
        print(json.dumps({"zone": chemin_relatif(zone), "elements": elements}, ensure_ascii=True))
    else:
        for ligne in afficher_lister(zone, elements, mission_filtre):
            print(ligne)
        entrees = journal_lire(chemin_journal)
        poses = len([e for e in entrees if e.get("action") == ACTION_CREE])
        purges = len([e for e in entrees if e.get("action") == ACTION_PURGE])
        print("  JOURNAL : " + str(len(entrees)) + " entree(s) -- " + str(poses)
              + " cree(s), " + str(purges) + " purge(s)")
    ecarts = [element for element in elements if element["classe"] != "canonique"]
    if strict and ecarts:
        print("ECART : " + str(len(ecarts)) + " element(s) hors forme canonique"
              " (residu ou non journalise) -- la porte les a NOMMES.")
        return 1
    return 0
