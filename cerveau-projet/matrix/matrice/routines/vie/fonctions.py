"""Fonctions simples de l'activateur de vie : une seule tache chacune."""
import os
import subprocess
import sys

from constants import NOM_PID_VEILLE, ENCODAGE


def processus_vivant(pid):
    """True si un processus porte ce PID (Windows : OpenProcess, sinon os.kill sonde 0)."""
    if pid is None or pid <= 0:
        return False
    if os.name == "nt":
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x00100000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if handle:
            kernel32.CloseHandle(handle)
            return True
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
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
    """Lance une boucle en processus DETACHE (survit a la session) et retourne son PID.

    CreationFlags DETACHED_PROCESS + CREATE_NEW_PROCESS_GROUP : pas de console
    accrochee, pas de signal de fermeture de session. Les flux vont a DEVNULL
    (la routine journalise deja elle-meme dans ses propres fichiers).
    """
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    processus = subprocess.Popen(
        [sys.executable, str(chemin_routine / "main.py")] + arguments,
        cwd=str(chemin_routine),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    return processus.pid
