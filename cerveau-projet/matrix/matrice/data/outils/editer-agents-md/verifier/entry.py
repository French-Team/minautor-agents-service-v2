"""Categorie verifier : integrite de l'encart session-matrix et de AGENTS.md."""
import hashlib

from commun import charger_texte, lire_empreinte_enregistree, trouver_agents_md
from constants import MARQUEUR_DEBUT, MARQUEUR_FIN, TAILLE_BLOC_LECTURE


def executer(arguments):
    chemin = trouver_agents_md()
    texte = charger_texte(chemin)
    if (MARQUEUR_DEBUT in texte) != (MARQUEUR_FIN in texte):
        print("ECART : marqueurs session-matrix non apparies (DEBUT sans FIN, ou l'inverse).")
        return 1
    if MARQUEUR_DEBUT not in texte:
        print("Encart session-matrix absent de AGENTS.md (jamais cree par l'outil).")
        return 1

    hacheur = hashlib.sha256()
    with open(chemin, "rb") as flux:
        for bloc in iter(lambda: flux.read(TAILLE_BLOC_LECTURE), b""):
            hacheur.update(bloc)
    empreinte_reelle = hacheur.hexdigest()
    empreinte_enregistree = lire_empreinte_enregistree()
    if empreinte_enregistree is None:
        print("ECART : aucune empreinte enregistree (l'etalon vit dans data/).")
        return 1
    if empreinte_reelle != empreinte_enregistree:
        print("ECART : empreinte reelle != etalon (AGENTS.md modifie hors de la porte unique ?).")
        return 1
    print("Verifier : encart session-matrix present, empreinte OK (" + empreinte_reelle[:16] + "...).")
    return 0
