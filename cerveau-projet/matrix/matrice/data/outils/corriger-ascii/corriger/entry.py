"""Categorie corriger : orchestre la correction ASCII (rapport ou application).

Interface entre main.py et les fonctions simples (corriger/fonctions.py).
"""
from corriger.fonctions import collecter_ecarts, corriger_fichier, resumer_exemptions

USAGE = "Usage : python main.py corriger [--appliquer]"
# Options DECLAREES par ce verbe : --appliquer est un DRAPEAU (sans valeur). Le
# domicile refuse tout le reste et NOMME le fautif (T2 de PB-002).
OPTIONS = ("appliquer",)


def afficher_caractere(caractere):
    """Representation sure du caractere (point de code) : jamais brut en console."""
    return "U+" + format(ord(caractere), "04X")


def executer(arguments):
    # Parsing d options par le DOMICILE (options.py) : avant, --appliquerx etait
    # simplement ABSENT de la liste, et l outil partait en mode RAPPORT -- le
    # resultat du DEFAUT, pris pour le resultat demande (EO-179, L-055).
    from options import extraire_options
    options = extraire_options(arguments, OPTIONS, drapeaux=OPTIONS,
                               outil="corriger-ascii", usage=USAGE)
    appliquer = "appliquer" in options
    resultats = collecter_ecarts()

    total_corriges = 0
    total_non_convertis = []
    if not resultats:
        print("Aucun caractere non-ASCII dans les fichiers cibles. Rien a corriger.")
    else:
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

    # Les EXEMPTES sont RAPPORTES dans les deux modes (rapport et application) :
    # c'est ce qui rend l'angle mort visible au lieu de le taire (MO-075).
    for ligne in resumer_exemptions():
        print(ligne)

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
