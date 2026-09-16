"""Lancement invisible partage (E-056, M-081) : UN motif pour toute la Matrice.

Le createur ne doit JAMAIS voir de fenetre console apparaitre/disparaitre
quand une routine demarre ou redemarre. Tout relancement de processus de
fond passe par ICI (motif unique, convention zero-duplication) :
Windows : CREATE_NO_WINDOW + CREATE_NEW_PROCESS_GROUP + startupinfo SW_HIDE.
POSIX   : start_new_session=True (detache du terminal, aucune fenetre).

Ce module est aussi le DOMICILE du plafond d'un sous-processus (MO-102 / P5 de
la revue MO-098) : un processus qui LANCE un fils declare ici son delai, et les
observateurs le LISENT au lieu de recopier 120 s chacun chez eux. Le meme 120 s
etait ecrit a SIX endroits (trois constantes d'observateurs, deux appels en dur,
une constante de routine) : six occasions de deriver en silence.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

ENCODAGE = "utf-8"

# Plafond DECLARE d'un sous-processus, en secondes : UNE source pour toute la
# Matrice (motif zero-duplication + zero-valeur-en-dur). Un fils qui depasse ce
# delai est tue par son appelant, qui journalise l'incident -- la boucle ne pend
# jamais. Ce n'est PAS une mesure : c'est une politique de survie, assumee.
DELAI_SOUS_PROCESSUS_SECONDES = 120


def delai_sous_processus():
    """Retourne le plafond DECLARE d'un sous-processus (secondes).

    Tout appelant passe par ICI : la valeur n'est jamais recopiee. Le jour ou
    la politique change, elle change ICI et partout a la fois.
    """
    return DELAI_SOUS_PROCESSUS_SECONDES


def drapeaux_invisibles():
    """Retourne (creationflags, startupinfo, start_new_session) pour Popen."""
    if os.name == "nt":
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = 0  # SW_HIDE : la console du fils n'est jamais montree
        return (
            subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP,
            info,
            False,
        )
    return 0, None, True


def lancer_invisible(chemin_routine, arguments, script="main.py"):
    """Lance `python <script> <arguments>` SANS aucune fenetre, retourne (pid, duree_ms).

    Par defaut script='main.py' (convention des routines) ; le server matrice
    passe script='server_matrice.py'. Flux vers DEVNULL : la routine journalise
    deja dans ses propres fichiers. La duree mesuree est celle de l'appel de
    lancement (metrique E-055/E-056).
    """
    debut = time.monotonic()
    creationflags, startupinfo, nouvelle_session = drapeaux_invisibles()
    processus = subprocess.Popen(
        [sys.executable, str(Path(chemin_routine) / script)] + list(arguments),
        cwd=str(chemin_routine),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
        startupinfo=startupinfo,
        start_new_session=nouvelle_session,
    )
    duree_ms = int((time.monotonic() - debut) * 1000)
    return processus.pid, duree_ms
