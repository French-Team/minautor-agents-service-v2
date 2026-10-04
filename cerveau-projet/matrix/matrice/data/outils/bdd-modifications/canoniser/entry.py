"""Categorie canoniser : la MIGRATION des cles non canoniques (EO-363).

Interface entre main.py et les fonctions simples (canoniser/fonctions.py).

Le TEMOIN est le RECENSEMENT des entrees (un multiset), pas leur NOMBRE : un
compte reste juste si une entree disparait pendant qu'une autre est dupliquee.
Si la migration change une seule entree, elle est REFUSEE et la BDD n'est PAS
ecrite. On ne reunit pas deux histoires en en perdant une -- et un refus qui ne
dit pas ce qu'il protege coute trois essais.
"""
from canoniser.fonctions import comparer_recensements, fusionner_cles
from commun import canoniser_cle, charger_bdd, enregistrer_bdd, extraire_options

NOMS_OPTIONS = ("simuler",)

USAGE = "Usage : python main.py canoniser [--simuler oui]"


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    donnees = charger_bdd()
    rapport, avant, apres = fusionner_cles(donnees, canoniser_cle)
    integre, message_integrite = comparer_recensements(avant, apres)
    if not integre:
        print(message_integrite)
        return 1
    total_avant = sum(avant.values())
    total_apres = sum(apres.values())
    simuler = str(options.get("simuler", "") or "").strip().lower() in ("oui", "1", "true")
    if not rapport:
        print("Aucune cle non canonique : la BDD est deja a UN SEUL DOMICILE ("
              + str(total_avant) + " modification(s)).")
        return 0
    for cle, canonique, nombre in rapport:
        print("  " + cle + " -> " + canonique
              + " (" + str(nombre) + " modification(s) reunie(s))")
    print("Cles reunies : " + str(len(rapport)) + " | modifications : " + str(total_avant)
          + " AVANT = " + str(total_apres) + " APRES (" + str(len(avant))
          + "/" + str(len(apres)) + " modification(s) DISTINCTE(s) : "
          + message_integrite + ")")
    if simuler:
        print("SIMULATION : la BDD n'a PAS ete ecrite.")
        return 0
    empreinte = enregistrer_bdd(donnees)
    print("Empreinte recalculee par la porte : " + empreinte[:16] + "...")
    return 0
