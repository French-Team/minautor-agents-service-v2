"""Porte de verification du registre de conservation."""
from commun import charger_bdd, calculer_empreinte_si_existe, lire_empreinte
from constants import CHEMIN_BDD
from verifier.fonctions import verifier_integrite, verifier_structure


def executer(arguments):
    donnees = charger_bdd()
    erreurs = verifier_structure(donnees) if CHEMIN_BDD.exists() else ["BDD absente"]
    ok, message = verifier_integrite(
        calculer_empreinte_si_existe(CHEMIN_BDD), lire_empreinte()
    )
    if erreurs:
        print("ECARTS structurels : " + " | ".join(erreurs))
        return 1
    print(message)
    return 0 if ok else 1
