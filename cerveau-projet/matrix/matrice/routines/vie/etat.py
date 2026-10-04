"""Categorie etat : affiche l'etat des routines supervisees.

La table nom -> PID ET la liste des routines viennent de constants.py (UNE
SEULE definition chacune, partagees avec le serveur : deux tables = deux
verites, cf. bug MO-043 ou l'ajout d'une routine faisait planter l'etat avec
un KeyError). L'etat ne reassemble plus la liste : il IMPORTE `BOUCLES`.

Chaque ligne porte aussi la cadence DECLAREE par la routine, LUE a sa source
(`CADENCE_PAR_NOM` dit seulement ou la lire). C'est ce qui permet de VERIFIER
sans ATTENDRE : on lit 300 s / 900 s au lieu de patienter 15 minutes pour voir
si la routine bat a son rythme (attendre n'est pas verifier, 2026-09-13).

Le MODE d allumage vient du PLANNING (decision du createur D1, MO-429) : une
routine en mode PASSE est ETEINTE entre deux passes PAR CONCEPTION, le service
la reallume a echeance. La porte ne compte donc PLUS une passe eteinte comme
une routine ARRETEE (faux verdict mesure le 2026-09-26 : la bascule en passe
faisait dire < 6/7, ARRET vigie-profil > a un etat normal). Un planning absent
ou illisible se DIT sur la ligne (L-055), jamais perdu en silence.

Le SERVEUR est affiche aussi, et compte dans le verdict : des routines vivantes
avec un serveur mort, c'est une Matrice qui n'est plus conduite. L'etat ne doit
jamais dire "sain" dans ce cas (le garde muet du selecteur a deja coute une
journee).
"""
from constants import BOUCLES, PID_PAR_NOM
from fonctions import (
    cadence_declaree,
    cause_du_dernier_lancement,
    etat_boucle,
    lire_pid,
    processus_vivant,
)
from server.entry import CHEMIN_PID_SERVER

# Le mode (passe | boucle) se lit au PLANNING -- la source de la rotation
# d allumage (M-076 : le motif partage, jamais recopie ici).
from planning_routines import PlanningIllisible
from planning_routines import mode as mode_planning


def _mode(nom):
    """Mode d allumage de la routine, ou None si le planning refuse (dit plus bas)."""
    try:
        return mode_planning(nom)
    except PlanningIllisible:
        return None


def _etat_serveur():
    """Retourne (ligne, actif) pour le server matrice."""
    pid_serveur = lire_pid(CHEMIN_PID_SERVER)
    if pid_serveur is not None and processus_vivant(pid_serveur):
        return "serveur matrice : ACTIVE (PID " + str(pid_serveur) + ")", True
    if CHEMIN_PID_SERVER.exists():
        CHEMIN_PID_SERVER.unlink()
        return "serveur matrice : ARRET (PID fantome " + str(pid_serveur) + " nettoye)", False
    return "serveur matrice : ARRET", False


def executer(arguments):
    print("Etat des boucles de fond de la Matrice :")
    codes = 0
    arrets = []
    en_passe = []
    modes_illisibles = []
    for nom, chemin_routine in BOUCLES:
        mode = _mode(nom)
        ligne, pid = etat_boucle(nom, chemin_routine, PID_PAR_NOM[nom])
        cadence = cadence_declaree(nom, chemin_routine)
        if cadence is None:
            suffixe = " | cadence : ILLISIBLE"
        else:
            suffixe = " | cadence declaree : " + str(cadence) + "s"
        if mode == "passe":
            # Eteinte entre deux passes = l etat NORMAL d une routine en passe :
            # elle ne compte ni parmi les actives ni parmi les arrets.
            if pid is not None:
                ligne = nom + " : EN PASSE (PID " + str(pid) + ")"
                codes += 1
            else:
                ligne = nom + " : PASSE (eteinte, allumee par le service)"
                en_passe.append(nom)
        elif pid is not None:
            codes += 1
        else:
            arrets.append(nom)
        print("  " + ligne + suffixe)
        if pid is None and mode != "passe":
            # EO-409 : la porte qui CONSTATE l arret NOMME la cause. Le journal de
            # lancement (data/commun/lancement.py) garde la sortie du DERNIER lancement :
            # sa derniere ligne est celle de l exception quand la routine est morte a
            # l allumage -- c'est ce qui manquait pendant les 26 h du routeur muet.
            # Rien a lire = SILENCE : une routine arretee proprement n a pas de cause a
            # crier, et un message vide serait du BRUIT (contre-temoin de l item).
            cause = cause_du_dernier_lancement(chemin_routine)
            if cause:
                print("      " + nom + " : dernier lancement : " + cause)
        if mode is None:
            modes_illisibles.append(nom)

    if modes_illisibles:
        # Un mode qu on ne peut pas lire n est pas un mode : la ligne le dit
        # plutot que de faire passer un faux verdict pour un verdict (L-055).
        print(
            "ATTENTION : mode d allumage ILLISIBLE au planning : "
            + ", ".join(modes_illisibles) + "."
        )

    ligne_serveur, serveur_actif = _etat_serveur()
    print("  " + ligne_serveur)

    total = len(BOUCLES)
    detail_passe = (
        " ; " + str(len(en_passe)) + " en passe (allumeees par le service)"
        if en_passe else ""
    )
    if codes == total and serveur_actif:
        print(
            "La Matrice vit (serveur + " + str(codes) + "/" + str(total)
            + " routines saines" + detail_passe + ")."
        )
    elif codes == 0 and not serveur_actif:
        print("La Matrice dort (serveur et routines arretes).")
    elif not serveur_actif:
        print(
            "ATTENTION : le SERVEUR est arrete -- " + str(codes) + "/" + str(total)
            + " routines vivent sans surveillance : personne ne les relancera."
        )
    elif arrets:
        # QUI manque, et non seulement COMBIEN (EO-404) : "6/7" sans nom a laisse
        # une routine morte (le routeur, une journee entiere) se lire comme un
        # detail. Le nom sort ICI, a cote de la ligne qui porte deja sa cadence
        # declaree -- et la source est la MEME : la table unique de constants.py.
        print(
            "La Matrice vit partiellement (" + str(codes) + "/" + str(total)
            + " routines saines) : ARRET " + ", ".join(arrets) + "."
        )
    elif not arrets and en_passe and codes == 0:
        # 100 % en mode passe = l ETAT NORMAL decide (D2a), jamais un 0/7 : le
        # voyant ne doit pas crier sur ce que le createur a choisi.
        print(
            "La Matrice vit (serveur actif, " + str(len(en_passe))
            + " routines en passe servies par le service)."
        )
    else:
        print(
            "La Matrice vit (serveur actif, " + str(codes) + "/" + str(total)
            + " routines saines" + detail_passe + ")."
        )
    return 0
