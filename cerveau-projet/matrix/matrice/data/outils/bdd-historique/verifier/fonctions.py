"""Fonctions simples de la categorie verifier : une seule tache chacune."""
from constants import CLES_REQUISES, TYPE_MARQUEUR

# Cles requises pour un MARQUEUR obsolete (pas d'evenement : pas de detail).
CLES_MARQUEUR = ("id", "date", "type", "cible", "tags")


def verifier_structure(lignes):
    """Verifie la structure du journal (cles requises SELON LE TYPE, ids uniques, cibles valides).

    Retourne (succes, message).
    """
    ids_vus = set()
    evenements_valides = 0
    for ligne in lignes:
        est_marqueur = ligne.get("type") == TYPE_MARQUEUR
        cles_attendues = CLES_MARQUEUR if est_marqueur else CLES_REQUISES
        for cle_requise in cles_attendues:
            if cle_requise not in ligne:
                return False, "Ecart structurel : ligne sans champ '" + cle_requise + "' : " + repr(ligne.get("id", ligne))
        if ligne.get("id") in ids_vus:
            return False, "Ecart structurel : id duplique : " + repr(ligne.get("id"))
        ids_vus.add(ligne.get("id"))
        if est_marqueur:
            if not ligne.get("cible"):
                return False, "Ecart structurel : marquage obsolete sans cible : " + repr(ligne.get("id"))
        else:
            evenements_valides += 1
    cibles = {l.get("cible") for l in lignes if l.get("type") == TYPE_MARQUEUR}
    for cible in cibles:
        if cible not in ids_vus:
            return False, "Ecart structurel : marquage obsolete vise un id inexistant : " + repr(cible)
    return True, "Verifier : " + str(evenements_valides) + " evenement(s) valide(s), integrite structurelle OK."
