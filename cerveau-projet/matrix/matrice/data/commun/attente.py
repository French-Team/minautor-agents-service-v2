"""Attente cooperative partagee : un arret demande n'attend JAMAIS la cadence.

Pourquoi ce motif existe (constat MO-061). Une boucle ecrivait

    time.sleep(intervalle)

en UN SEUL bloc. Consequences, mesurees sur la Matrice :

1. L'ARRET dependait de la cadence. Avec un intervalle de 900 s, un
   `server arret` mettait jusqu'a 15 minutes a faire tomber la routine : on
   attendait pour rien, et on ne pouvait pas verifier une correction sans
   payer la cadence entiere.
2. On croyait verifier une cadence en ATTENDANT. Attendre n'est pas verifier :
   si c'est casse, on a attendu pour rien (parole du createur, 2026-09-13).

La reponse n'est pas d'attendre mieux, c'est de rendre la chose OBSERVABLE :
chaque routine JOURNALISE sa cadence effective a l'allumage (voir les
`demarrer_boucle`), donc on lit la cadence au lieu de l'attendre. Et l'attente
est decoupee pour que le drapeau d'arret soit vu en quelques secondes.

Une seule implementation, partagee (convention zero-duplication) : toute
routine qui dort longtemps passe par ICI.
"""
import time


def attendre(secondes, drapeau=None, pas=2.0):
    """Dort `secondes` en morceaux de `pas` secondes, en surveillant `drapeau`.

    Retourne True si le drapeau est apparu pendant l'attente, False si
    l'attente est allee a son terme. Le drapeau n'est JAMAIS consomme ici :
    c'est la boucle qui le consomme (un seul proprietaire, zero ambiguite).

    `pas` vaut 2 s par defaut : l'arret est vu en 2 s au pire, quelle que soit
    la cadence. Un `pas` n'a aucune raison de depasser la minute.
    """
    if drapeau is None:
        time.sleep(secondes)
        return False
    reste = float(secondes)
    while reste > 0:
        if drapeau.exists():
            return True
        dodo = pas if pas < reste else reste
        time.sleep(dodo)
        reste -= dodo
    return drapeau.exists()
