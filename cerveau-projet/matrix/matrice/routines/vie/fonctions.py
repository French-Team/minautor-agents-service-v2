"""Fonctions simples de l'activateur de vie : une seule tache chacune."""
import importlib.util

from constants import CADENCE_PAR_NOM, NOM_PID_VEILLE, ENCODAGE

# La sonde de VIVACITE est le motif PARTAGE (data/commun/vivacite.py, M-076) : elle
# vivait ici ET dans le maillon 7 du flux, et une TROISIEME copie allait naitre
# pour la garde de double lancement du routeur (EO-404). Trois copies de la meme
# sonde, c'est trois verites sur la vie d'une routine -- et c'est ce qui a laisse
# une relance echouer en silence. Le chemin est joignable sans rien refaire :
# `constants.py` a deja installe data/commun dans `sys.path` (invariant 1 du moule).
from vivacite import processus_vivant  # noqa: F401  (reexport : etat.py et le serveur l'importent d'ici)

# La CAUSE du dernier lancement d une routine (EO-409) : la porte vie la NOMME
# quand elle CONSTATE un arret. La lecture vit dans le motif PARTAGE
# (data/commun/lancement.py : journal de lancement, lecture BORNEE) et elle est
# reexportee ici pour que etat.py et le maillon 7 du flux lisent la MEME chose.
from lancement import cause_du_dernier_lancement  # noqa: F401  (reexport : etat.py et le flux l'importent d'ici)


def lire_pid(chemin_pid):
    """Retourne le PID note dans le fichier, ou None si absent ou illisible."""
    if not chemin_pid.exists():
        return None
    try:
        contenu = chemin_pid.read_text(encoding=ENCODAGE).strip()
        return int(contenu) if contenu else None
    except (ValueError, OSError):
        return None


def etat_boucle(nom, chemin_routine, nom_pid):
    """Retourne (ligne_etat, pid) d'une boucle : ARRET / ACTIVE (PID) / FANTOME nettoye."""
    chemin_pid = chemin_routine / nom_pid
    pid = lire_pid(chemin_pid)
    if pid is not None and not processus_vivant(pid):
        chemin_pid.unlink()
        return nom + " : ARRET (PID fantome " + str(pid) + " nettoye)", None
    if pid is not None:
        return nom + " : ACTIVE (PID " + str(pid) + ")", pid
    return nom + " : ARRET", None


def cadence_declaree(nom, chemin_routine):
    """Retourne la cadence DECLAREE par la routine, sans la lancer ni l'attendre.

    Pourquoi (2026-09-13) : attendre 900 s pour savoir si une routine bat a son
    rythme est une fausse verification -- si c'est casse, on a attendu pour
    rien. On LIT donc la valeur declaree chez la routine (voix unique : elle
    n'est jamais recopiee ici) via la table `CADENCE_PAR_NOM`, qui indique
    seulement OU la lire.

    Le module est charge sous un nom UNIQUE (`cadence_<routine>`) : six fichiers
    s'appellent `constants.py`, les importer sous leur nom se mascheraient
    mutuellement. Retourne None si la lecture echoue (on l'AVOUE a l'affichage).
    """
    source = CADENCE_PAR_NOM.get(nom)
    if source is None:
        return None
    fichier, nom_constante = source
    chemin = chemin_routine / fichier
    if not chemin.is_file():
        return None
    nom_module = "cadence_" + nom.replace("-", "_")
    try:
        specification = importlib.util.spec_from_file_location(nom_module, str(chemin))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception:
        return None
    valeur = getattr(module, nom_constante, None)
    return valeur if isinstance(valeur, int) else None


def lancer_detache(chemin_routine, arguments):
    """Lance une boucle en processus DETACHE sans AUCUNE fenetre (E-056, M-081).

    Motif UNIQUE partage data/commun/lancement.py (fini la duplication) :
    Windows : CREATE_NO_WINDOW + CREATE_NEW_PROCESS_GROUP + startupinfo SW_HIDE.
    POSIX   : start_new_session=True.
    Retourne (pid, duree_ms) -- la duree du lancement est la metrique E-055.
    """
    from lancement import lancer_invisible

    return lancer_invisible(chemin_routine, arguments)
