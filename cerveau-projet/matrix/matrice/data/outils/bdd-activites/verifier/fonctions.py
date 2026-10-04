"""Fonctions simples de la categorie verifier : une seule tache chacune."""
from constants import CLES_REQUISES, SECTIONS, TAILLE_SECTION


def verifier_structure(donnees):
    """Verifie la structure du registre (sections figees, cles requises, tailles).

    Retourne (succes, message).
    """
    sections = donnees.get("sections", {})
    for nom, activites in sections.items():
        if nom not in SECTIONS:
            return False, "Ecart structurel : section non declaree : " + repr(nom)
        if len(activites) > TAILLE_SECTION:
            return (
                False,
                "Ecart structurel : section " + nom + " depasse la rotation ("
                + str(len(activites)) + " > " + str(TAILLE_SECTION) + ")",
            )
        for activite in activites:
            for cle_requise in CLES_REQUISES:
                if cle_requise not in activite:
                    return False, "Ecart structurel : activite sans champ '" + cle_requise + "' dans " + nom
            if not activite.get("tags"):
                return False, "Ecart structurel : activite sans tags dans " + nom
    return True, "Verifier : " + str(len(sections)) + " section(s) valide(s), integrite structurelle OK."
