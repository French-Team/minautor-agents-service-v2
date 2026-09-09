"""Fonctions simples de la categorie lire : une seule tache chacune."""


def filtrer(donnees, cle=None, tag=None):
    """Retourne les variables, toutes ou filtrees par cle (unique) et/ou tag."""
    resultats = donnees.get("variables", ())
    if cle:
        resultats = [v for v in resultats if v.get("cle") == cle]
    if tag:
        resultats = [v for v in resultats if tag in v.get("tags", ())]
    return resultats


def afficher(variables):
    """Affiche les variables en format lisible (ASCII strict)."""
    if not variables:
        print("Aucune variable.")
        return
    for variable in variables:
        ligne = (
            variable["id"] + "  " + variable["cle"] + " = " + variable["valeur"]
            + "  [" + variable["statut"] + "]  (" + variable["date"]
            + ", source : " + (variable.get("source") or "-")
            + ", tags : " + ", ".join(variable.get("tags", ())) + ")"
        )
        print(ligne)
    print(str(len(variables)) + " variable(s) affichee(s).")
