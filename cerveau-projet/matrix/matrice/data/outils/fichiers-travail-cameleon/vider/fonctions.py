"""Fonction atomique de la categorie vider : le solde de la zone."""

import shutil
from pathlib import Path

from commun import elements_zone, journal_noter, mission_du_nom
from constants import ACTION_PURGE
from zone_tmp import contenu as contenu_zone, vider as vider_zone


def vider(zone, mission, par, chemin_journal=None):
    """VIDE la zone (ou les elements d UNE mission) et journalise chaque retrait.

    La purge de TOUTE la zone passe par le moteur PARTAGE (zone_tmp.vider) : ce
    n est pas la logique de cette porte, c est celle des DEUX flux, et elle rend
    ses echecs au lieu de les avaler. La purge CIBLEE ne traite que les elements
    dont le nom porte la mission (forme canonique) ou commence par son prefixe.
    Rend (code, rapport) : le rapport porte supprimes, echecs et restants, et le
    SOLDE est journalise avec chaque retrait.
    """
    zone = Path(zone)
    if not zone.is_dir():
        return 0, {"supprimes": [], "echecs": [], "restants": []}
    mission = (mission or "").strip().lower()
    if mission:
        prefixe = mission + "-"
        supprimes, echecs = [], []
        for element in contenu_zone(zone):
            nom = element.name
            if mission_du_nom(nom) != mission and not nom.startswith(prefixe):
                continue
            try:
                if element.is_dir():
                    shutil.rmtree(str(element))
                else:
                    element.unlink()
                supprimes.append(nom)
            except OSError:
                echecs.append(nom)
    else:
        supprimes, echecs = vider_zone(zone)
    restants = [element["nom"] for element in elements_zone(zone, chemin_journal)]
    for nom in supprimes:
        journal_noter({"action": ACTION_PURGE, "nom": nom,
                       "mission": mission_du_nom(nom) or "", "par": par,
                       "solde": len(restants)}, chemin_journal)
    rapport = {"supprimes": supprimes, "echecs": echecs, "restants": restants}
    return (1 if echecs else 0), rapport
