"""Fonctions de la categorie corriger : une seule tache chacune."""
from commun import (
    classer_fichiers_cibles,
    convertir_texte,
    ecrire_texte_atomique,
    lire_texte,
    scanner_texte,
)


def collecter_ecarts():
    """Scanne les cibles. Retourne [(chemin, ecarts)], fichiers touches seulement."""
    resultats = []
    cibles, _ = classer_fichiers_cibles()
    for chemin in cibles:
        ecarts = scanner_texte(lire_texte(chemin))
        if ecarts:
            resultats.append((chemin, ecarts))
    return resultats


def resumer_exemptions():
    """Retourne les lignes du rapport des EXEMPTIONS (visibles, jamais touchees).

    Le rapport ne cite AUCUN point de code Unicode : il dit seulement QUELS
    fichiers sont hors du champ de reecriture et POURQUOI. La raison est mesurable
    -- un exempte est un angle mort : le taire, c'est laisser croire que le scan
    couvre tout (540 fichiers scannes contre 569 pour garde-ascii, EO-103).
    """
    cibles, exemptes = classer_fichiers_cibles()
    lignes = [
        "Fichiers examines : " + str(len(cibles)) + " reecrivables, "
        + str(len(exemptes)) + " exemptes de reecriture (jamais touches)."
    ]
    if not exemptes:
        lignes.append("Aucun fichier exempte : le scan couvre tout le perimetre.")
        return lignes
    motifs = []
    for _, motif in exemptes:
        if motif not in motifs:
            motifs.append(motif)
    for motif in motifs:
        du_motif = [chemin for chemin, m in exemptes if m == motif]
        lignes.append("  EXEMPTE [" + motif + "] " + str(len(du_motif)) + " fichier(s) :")
        for chemin in du_motif:
            lignes.append("    " + chemin)
    return lignes


def corriger_fichier(chemin):
    """Applique la conversion sur UN fichier. Retourne (corriges, non_convertis)."""
    texte = lire_texte(chemin)
    converti, non_convertis = convertir_texte(texte)
    ecrire_texte_atomique(chemin, converti)
    return len(non_convertis), sorted(set(non_convertis))
