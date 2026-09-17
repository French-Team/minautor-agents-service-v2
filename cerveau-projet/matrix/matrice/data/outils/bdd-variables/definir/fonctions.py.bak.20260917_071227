"""Fonctions simples de la categorie definir : une seule tache chacune."""
from datetime import datetime

from constants import PREFIXE_ID, STATUTS


def separer_tags(chaine_tags):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide)."""
    if not chaine_tags:
        return []
    return [morceau.strip() for morceau in chaine_tags.split(",") if morceau.strip()]


def prochain_id(donnees):
    """Retourne le prochain identifiant V-XXX (numerotation continue, zero pad 3).

    MAX+1, jamais longueur+1 (lecon MO-093) : apres un ecart de structure,
    redefinir une cle existante ne doit PAS creer un doublon d'id.
    """
    plus_haut = 0
    for variable in donnees.get("variables", ()):  
        identifiant = str(variable.get("id") or "")
        if identifiant.startswith(PREFIXE_ID):
            reste = identifiant[len(PREFIXE_ID):]
            if reste.isdigit():
                plus_haut = max(plus_haut, int(reste))
    return PREFIXE_ID + str(plus_haut + 1).zfill(3)


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
        # Valeur vide autorisee UNIQUEMENT en mise a jour (MO-093 : la
        # restauration du perimetre cameleon est une valeur vide).
        existante["source"] = source
        existante["tags"] = tags
        existante["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existante["statut"] = STATUTS[0]
        # Reparer au passage ce qu'une ecriture hors porte a pu casser
        # (MO-093 : V-003 stockee sans id) -- sinon la porte soigne la
        # valeur mais laisse l'ecart structurel que son verifier condamne.
        if not existante.get("id"):
            existante["id"] = prochain_id(donnees)
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
