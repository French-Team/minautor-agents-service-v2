"""Fonctions simples de l'activateur de vie : une seule tache chacune."""
import os
import sys

from constants import NOM_PID_VEILLE, ENCODAGE


def processus_vivant(pid):
    """True si un processus porte ce PID.

    Sur WSL, os.kill(pid, 0) peut echouer (pid Linux vs pid Windows).
    On utilise d'abord os.kill, puis ctypes OpenProcess (win32), puis
    un test via subprocess + ps en dernier recours.
    """
    if pid is None or pid <= 0:
        return False
    # Methode 1 : os.kill (marche sur Linux pur et sur les pid WSL visibles)
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        pass
    # Methode 2 : ctypes OpenProcess (Windows natif)
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
    # Methode 3 : test via ps (marche aussi sur WSL avec les pid Windows)
    try:
        import subprocess
        r = subprocess.run(
            ["ps", "-p", str(pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
        if r.returncode == 0:
            return True
    except Exception:
        pass
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


def lancer_detache(chemin_routine, arguments):
    """Lance une boucle en processus DETACHE sans AUCUNE fenetre (E-056, M-081).

    Motif UNIQUE partage data/commun/lancement.py (fini la duplication) :
    Windows : CREATE_NO_WINDOW + CREATE_NEW_PROCESS_GROUP + startupinfo SW_HIDE.
    POSIX   : start_new_session=True.
    Retourne (pid, duree_ms) -- la duree du lancement est la metrique E-055.
    """
    from lancement import lancer_invisible

    return lancer_invisible(chemin_routine, arguments)
