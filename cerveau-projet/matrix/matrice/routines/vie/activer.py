"""Categorie activer : orchestre le lancement des boucles de fond de la Matrice.

Interface entre main.py et les fonctions simples (fonctions.py).
Le lancement est DETACHE : la boucle survit a la session qui l'a demarree.
Le garde de double lancement vit dans CHAQUE routine (leur propre PID) :
l'activateur le respecte, il ne le contourne jamais.
"""
from constants import (
    BOUCLES,
    COMMANDE_ESPION,
    COMMANDE_VEILLE,
    NOM_PID_ESPION,
    NOM_PID_VEILLE,
)
from fonctions import etat_boucle, lancer_detache


def verifier_avant_lancement(nom, pid):
    """Refuse si une boucle du meme nom vit deja (protection locale confirmee)."""
    if pid is not None:
        print("REFUS : " + nom + " vit deja (PID " + str(pid) + "). Une seule boucle par routine.")
        return False
    return True


def executer(arguments):
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau == "--intervalle" and index + 1 < len(arguments):
            options["intervalle"] = arguments[index + 1]
            index += 2
        else:
            index += 1
    intervalle = options.get("intervalle")

    lancees = []
    for nom, chemin_routine in BOUCLES:
        if nom == "veille-flux":
            nom_pid, commande = NOM_PID_VEILLE, COMMANDE_VEILLE
        else:
            nom_pid, commande = NOM_PID_ESPION, COMMANDE_ESPION
        ligne, pid = etat_boucle(nom, chemin_routine, nom_pid)
        if not verifier_avant_lancement(nom, pid):
            continue
        arguments_boucle = [commande]
        if nom == "veille-flux":
            arguments_boucle.append("--boucle")
            if intervalle:
                arguments_boucle += ["--intervalle", intervalle]
        elif intervalle:
            arguments_boucle += ["--interval", intervalle]
        pid_nouveau, duree_ms = lancer_detache(chemin_routine, arguments_boucle)
        lancees.append(nom + " (PID " + str(pid_nouveau) + ", lance en " + str(duree_ms) + " ms)")

    if lancees:
        print("Boucles lancees en detache (survivent a la session) : " + ", ".join(lancees))
    else:
        print("Aucune boucle lancee (toutes deja actives ou refusees).")
    return 0
