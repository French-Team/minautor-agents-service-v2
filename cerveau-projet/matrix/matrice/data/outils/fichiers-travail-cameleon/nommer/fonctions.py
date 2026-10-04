"""Fonction atomique de la categorie nommer : poser un fichier de travail."""

from pathlib import Path

from commun import chemin_relatif, journal_noter, nom_canonique
from constants import ACTION_CREE


def nommer(zone, mission, libelle, extension, par, chemin_journal=None):
    """Pose le fichier d une mission sous son NOM CANONIQUE du cameleon.

    Une pose n ECRASE JAMAIS un fichier existant : elle le DIT et laisse le
    contenu intact (meme regle que la pose de template du pilote). L acte est
    journalise dans les DEUX cas, avec son resultat -- un deja-pose est un fait,
    pas rien. Rend (code, message, chemin).
    """
    zone = Path(zone)
    nom, refus = nom_canonique(mission, libelle, extension)
    if refus:
        return 2, refus, None
    if not zone.is_dir():
        return 2, ("REFUS : la zone " + str(zone) + " n existe pas -- elle est creee"
                   " par le pilote de son flux (regle R-005)."), None
    cible = zone / nom
    if cible.exists():
        journal_noter({"action": ACTION_CREE, "resultat": "deja-pose", "nom": nom,
                       "mission": mission.strip().lower(), "par": par}, chemin_journal)
        return 0, ("DEJA POSE : " + nom + " existe -- rien n a ete ecrit, contenu intact."), cible
    try:
        with open(str(cible), "w", encoding="utf-8", newline="\n") as flux:
            flux.write("")
    except OSError as erreur:
        return 1, ("ECHEC : pose impossible (" + str(erreur) + ")."), None
    journal_noter({"action": ACTION_CREE, "resultat": "pose", "nom": nom,
                   "mission": mission.strip().lower(), "par": par,
                   "chemin": chemin_relatif(cible)}, chemin_journal)
    return 0, ("POSE : " + nom + " (" + chemin_relatif(cible) + ")"), cible
