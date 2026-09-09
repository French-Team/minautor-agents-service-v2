"""Fonctions simples de la categorie definir : une seule tache chacune."""
from datetime import datetime

from constants import STATUTS


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine_tags:
        return []
    return [morceau.strip() for morceau in chaine_tags.split(",") if morceau.strip()]


def prochain_id(donnees):
    """Retourne le prochain identifiant V-XXX (numerotation continue, zero pad 3)."""
    numero = len(donnees.get("variables", ())) + 1
    return "V-" + str(numero).zfill(3)


def trouver_variable(donnees, cle):
    """Retourne la variable portant cette cle, ou None si absente."""
    for variable in donnees.get("variables", ()):
        if variable.get("cle") == cle:
            return variable
    return None


def definir_variable(donnees, cle, valeur, source, tags):
    """Cree OU met a jour la variable de cette cle dans les donnees (in place).

    Une cle = une valeur courante : re-definir conserve l'identifiant V-XXX.
    Retourne (entree, creee).
    """
    variables = donnees.setdefault("variables", [])
    existante = trouver_variable(donnees, cle)
    if existante is not None:
        existante["valeur"] = valeur
        existante["source"] = source
        existante["tags"] = tags
        existante["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existante["statut"] = STATUTS[0]
        return existante, False
    entree = {
        "id": prochain_id(donnees),
        "cle": cle,
        "valeur": valeur,
        "source": source,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "statut": STATUTS[0],
        "tags": tags,
    }
    variables.append(entree)
    return entree, True
