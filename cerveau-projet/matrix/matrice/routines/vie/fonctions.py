"""Fonctions simples de l'activateur de vie : une seule tache chacune."""
import importlib.util
import os
import sys

from constants import CADENCE_PAR_NOM, NOM_PID_VEILLE, ENCODAGE


def processus_vivant(pid):
    """True si un processus porte ce PID.

Sur Windows natif, la sonde Win32 est prioritaire : os.kill() et ps peuvent
voir une couche Git/WSL differente et produire un faux negatif. Sur POSIX,
os.kill() reste la sonde principale avec ps en secours.
"""
    if pid is None or pid <= 0:
        return False

    if sys.platform == "win32" or os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(0x00100000, False, pid)
            if handle:
                kernel32.CloseHandle(handle)
                return True
        except Exception:
            pass
        return False

    try:
        os.kill(pid, 0)
        return True
    except OSError:
        pass
    try:
        import subprocess
        r = subprocess.run(
            ["ps", "-p", str(pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
        return r.returncode == 0
    except Exception:
        return False


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
