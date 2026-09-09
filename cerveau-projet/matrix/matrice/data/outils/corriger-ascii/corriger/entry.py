"""Categorie corriger : orchestre la correction ASCII (rapport ou application).

Interface entre main.py et les fonctions simples (corriger/fonctions.py).
"""
from corriger.fonctions import collecter_ecarts, corriger_fichier


def afficher_caractere(caractere):
    """Representation sure du caractere (point de code) : jamais brut en console."""
    return "U+" + format(ord(caractere), "04X")


def executer(arguments):
    appliquer = "--appliquer" in arguments[1:]
    resultats = collecter_ecarts()
    if not resultats:
        print("Aucun caractere non-ASCII dans les fichiers cibles. Rien a corriger.")
        return 0

    total_corriges = 0
    total_non_convertis = []
    for chemin, ecarts in resultats:
        print(chemin + " -- " + str(len(ecarts)) + " ecart(s)")
        if not appliquer:
            for ligne, colonne, caractere, remplacement in ecarts:
                sort = "-> '" + remplacement + "'" if remplacement else "NON CONVERTI (signale)"
                print("  ligne " + str(ligne) + ":" + str(colonne) + " " + afficher_caractere(caractere) + " " + sort)
            continue
        corriges, non_convertis = corriger_fichier(chemin)
        total_corriges += corriges
        total_non_convertis.extend(non_convertis)
        print("  corrige (ecriture atomique LF)")

    if not appliquer:
        print("Rapport seul (sans --appliquer, rien n'a ete ecrit).")
        return 0

    if total_non_convertis:
        uniques = sorted(set(total_non_convertis))
        print("ATTENTION : caracteres non convertis laisses en place : " + ", ".join(afficher_caractere(c) for c in uniques))
        print("Probleme plus grave -> decision du createur (aucune perte de donnees).")
        return 1
    print("Corrections appliquees. A noter en BDD (porte unique).")
    return 0
