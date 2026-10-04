"""Fonctions simples de la categorie verifier : une seule tache chacune."""
from constants import CLES_REQUISES


def verifier_structure(donnees):
    """Verifie la structure de chaque variable (cles requises, tags non vides).

    Retourne (succes, message).
    """
    variables = donnees.get("variables", ())
    cles_vues = set()
    for variable in variables:
        for cle_requise in CLES_REQUISES:
            if cle_requise not in variable:
                return False, "Ecart structurel : variable sans champ '" + cle_requise + "' : " + repr(variable.get("cle"))
        if not variable.get("tags"):
            return False, "Ecart structurel : variable sans tags : " + repr(variable.get("cle"))
        cle_valeur = variable.get("cle")
        if cle_valeur in cles_vues:
            return False, "Ecart structurel : cle dupliquee : " + repr(cle_valeur)
        cles_vues.add(cle_valeur)
    return True, "Verifier : " + str(len(variables)) + " variable(s) valide(s), integrite structurelle OK."
