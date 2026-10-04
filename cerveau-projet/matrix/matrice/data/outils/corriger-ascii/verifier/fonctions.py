"""Fonctions de la categorie verifier : une seule tache chacune."""
from corriger.fonctions import collecter_ecarts


def afficher_caractere(caractere):
    """Retourne une representation SURE du caractere (point de code).

    Jamais de caractere non-ASCII brut vers la console : cp1252 crasherait.
    """
    return "U+" + format(ord(caractere), "04X")


def executer_verification():
    """Scan seul avec capacite de conversion. Retourne le nombre de fichiers touches."""
    resultats = collecter_ecarts()
    if not resultats:
        print("Aucun caractere non-ASCII dans les fichiers cibles.")
        return 0
    total = 0
    for chemin, ecarts in resultats:
        total += len(ecarts)
        print(chemin + " -- " + str(len(ecarts)) + " ecart(s)")
        for ligne, colonne, caractere, remplacement in ecarts:
            sort = "-> '" + remplacement + "'" if remplacement else "NON CONVERTI (signale)"
            print("  ligne " + str(ligne) + ":" + str(colonne) + " " + afficher_caractere(caractere) + " " + sort)
    print("Total : " + str(total) + " ecart(s). Scan seul, rien n'a ete ecrit.")
    return total
