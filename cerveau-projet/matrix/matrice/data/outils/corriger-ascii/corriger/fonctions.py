"""Fonctions de la categorie corriger : une seule tache chacune."""
from commun import (
    convertir_texte,
    ecrire_texte_atomique,
    lister_fichiers_cibles,
    lire_texte,
    scanner_texte,
)


def collecter_ecarts():
    """Scanne les cibles. Retourne [(chemin, ecarts)], fichiers touches seulement."""
    resultats = []
    for chemin in lister_fichiers_cibles():
        ecarts = scanner_texte(lire_texte(chemin))
        if ecarts:
            resultats.append((chemin, ecarts))
    return resultats


def corriger_fichier(chemin):
    """Applique la conversion sur UN fichier. Retourne (corriges, non_convertis)."""
    texte = lire_texte(chemin)
    converti, non_convertis = convertir_texte(texte)
    ecrire_texte_atomique(chemin, converti)
    return len(non_convertis), sorted(set(non_convertis))
