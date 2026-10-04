"""Fonction atomique de la categorie montrer : le CONTENU d un element."""

from pathlib import Path

from commun import chemin_relatif, elements_zone
from constants import LIGNES_MONTREES


def montrer(zone, nom):
    """Le CONTENU d un element de la zone, par son SEUL nom.

    Le nom est un NOM, jamais un chemin (un separateur est un REFUS) : la porte
    ne sert pas un fichier hors de sa zone. Un nom absent est refuse en NOMMANT
    ce que la zone porte -- un vide muet se lirait comme une zone vide.
    Rend (code, texte).
    """
    zone = Path(zone)
    if not nom or nom in (".", "..") or "/" in nom or chr(92) in nom:
        return 2, ("REFUS : < montrer > prend un NOM, jamais un chemin (recu : "
                   + str(nom) + ").")
    cible = zone / nom
    if not cible.is_file():
        presents = ", ".join(element["nom"] for element in elements_zone(zone)) or "aucun"
        return 2, ("REFUS : " + nom + " absent de " + chemin_relatif(zone)
                   + " -- presents : " + presents)
    try:
        lignes = cible.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as erreur:
        return 2, ("REFUS : lecture impossible (" + str(erreur) + ").")
    bloc = ["# " + nom + " (" + str(len(lignes)) + " ligne(s))"]
    if len(lignes) > LIGNES_MONTREES:
        bloc.append("... " + str(len(lignes) - LIGNES_MONTREES) + " ligne(s) non affichee(s) ...")
        lignes = lignes[:LIGNES_MONTREES]
    bloc.extend(lignes)
    return 0, "\n".join(bloc)
