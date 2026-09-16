"""Server MATRICE (E-056, M-081) : orchestrateur de vie des routines.

2 etages du server de demarrage voulu par le createur :
  - server 'matrice' : CE processus (boucle de fond invisible). Il possede
    le lancement : chaque routine est lancee/relancee PAR LUI, jamais en
    direct. Il relance toute boucle morte (reprise apres crash/redemarrage).
  - server 'routine' : chaque routine de la table BOUCLES (constants.py) est
    une fille du server : son cycle de vie passe par le server. La liste n'est
    PAS enumeree ici -- l'enumerer serait une deuxieme table, donc une
    deuxieme verite (c'est ainsi que le routeur de maintenance est reste hors
    supervision sans que personne ne le voie).

Exigeance createur : le redemarrage d'une routine est INVISIBLE (aucune
fenetre console). Toute relance passe par le motif partage lancement.py
(CREATE_NO_WINDOW + SW_HIDE sur Windows).

Usage : python server_matrice.py [--interval <secondes>] [--once]
Arret  : drapeau cooperatif (fichier server-matrice-arret.txt).

CADENCE : aucun ordre global n'est passe aux routines. Chacune garde SON
intervalle declare dans ses propres constantes ; `--interval <s>` n'est qu'un
override EXPLICITE de l'operateur. La valeur interne de 60 s est la cadence de
SUPERVISION du server (sa propre sonde de vie), pas celle des routines.
"""
import sys
import time
from pathlib import Path

REPERTOIRE_SERVER = Path(__file__).resolve().parent
sys.path.insert(0, str(REPERTOIRE_SERVER))
sys.path.insert(0, str(REPERTOIRE_SERVER.parent.parent / "data" / "commun"))

from constants import (
    BOUCLES,
    COMMANDE_PAR_NOM,
    DRAPEAU_PAR_NOM,
    NOM_PID_SERVER,
    PID_PAR_NOM,
    ENCODAGE,
)  # noqa: E402
from attente import attendre  # noqa: E402
from fonctions import processus_vivant  # noqa: E402
from lancement import lancer_invisible  # noqa: E402
from server.entry import CHEMIN_DRAPEAU_ARRET, CHEMIN_PID_SERVER  # noqa: E402

# CADENCE DE SUPERVISION : le temps du SERVER (combien il attend entre deux
# sondes de vie des routines). C'est SON temps -- il n'est pas celui des
# routines et ne leur est JAMAIS impose.
INTERVALLE_SUPERVISION_SECONDES = 60

# CADENCE DES ROUTINES : aucun ordre global. None = le server ne touche pas au
# temps des routines ; chacune garde SON intervalle declare (veille-flux 300 s,
# espion-integrite 300 s, vigie-profil 900 s, vigie-portes 900 s, suivi-sync le
# sien). Un `--interval <s>` reste un override global VOLONTAIRE de l'operateur.
# (Bug corrige : un ordre unique de 60 s etait passe a TOUTES les routines, ce
# qui ecrasait leurs cadences declarees -- 900 s annoncees, 60 s reelles.)
INTERVALLE_OVERRIDE_DEFAUT = None

# BOUCLES, COMMANDE_PAR_NOM, PID_PAR_NOM et DRAPEAU_PAR_NOM viennent de
# constants.py (UNE SEULE table chacun, partagee avec vie/etat.py : deux
# tables = deux verites). Le server ne reassemble plus la liste des routines.


def lire_pid_fichier(chemin_pid):
    """Retourne le PID note dans le fichier, ou None."""
    if not chemin_pid.exists():
        return None
    try:
        contenu = chemin_pid.read_text(encoding=ENCODAGE).strip()
        return int(contenu) if contenu else None
    except (ValueError, OSError):
        return None


def rechercher_pid_processus_posix(chemin_routine):
    """Recherche de secours POSIX par ligne de commande."""
    import subprocess

    resultat = subprocess.run(
        ["ps", "-eo", "pid,args"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    if resultat.returncode != 0:
        return None
    chemin = chemin_routine.as_posix()
    for ligne in resultat.stdout.splitlines():
        if chemin not in ligne or "python" not in ligne.lower():
            continue
        morceaux = ligne.split()
        try:
            return int(morceaux[0])
        except (IndexError, ValueError):
            continue
    return None


def rechercher_pid_processus_windows(chemin_routine):
    """Recherche de secours Windows par ligne de commande PowerShell."""
    import shutil
    import subprocess

    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if powershell is None:
        return None
    chemin = str(chemin_routine).replace("'", "''")
    script = (
        "Get-CimInstance Win32_Process -Filter \"Name = 'python.exe' OR Name = 'pythonw.exe'\" "
        "| Where-Object { $_.CommandLine -like '*" + chemin + "*' } "
        "| Select-Object -First 1 -ExpandProperty ProcessId"
    )
    try:
        resultat = subprocess.run(
            [powershell, "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if resultat.returncode != 0:
        return None
    for ligne in resultat.stdout.splitlines():
        try:
            return int(ligne.strip())
        except ValueError:
            continue
    return None


def rechercher_pid_routine(nom, chemin_routine):
    """Retourne le PID d'une routine sans relance intempestive.

    Source prioritaire : le PID file propre de la routine, puis recherche
    systeme compatible POSIX/Windows si le PID file manque.
    """
    nom_pid = PID_PAR_NOM[nom]
    chemin_pid = chemin_routine / nom_pid
    pid_fichier = lire_pid_fichier(chemin_pid)
    if pid_fichier is not None and processus_vivant(pid_fichier):
        return pid_fichier
    if pid_fichier is not None:
        try:
            chemin_pid.unlink()
        except OSError:
            pass

    if sys.platform == "win32" or __import__("os").name == "nt":
        pid = rechercher_pid_processus_windows(chemin_routine)
    else:
        pid = rechercher_pid_processus_posix(chemin_routine)
    return pid if pid is not None and processus_vivant(pid) else None


def recreer_pid_files():
    """Republie le PID file de toute routine VIVANTE qui n'en a plus.

    Pourquoi a CHAQUE cycle et pas seulement au demarrage (2026-09-13) : un PID
    file efface rend la routine INVISIBLE pour `vie etat` et pour la
    non-regression du flux, pendant que le serveur, lui, la voit vivante par
    recherche systeme. Deux verites sur la meme chose -- l'etat disait ARRET, le
    serveur disait vivant -- et personne ne relancait : l'orphelin durait.
    Le serveur est l'AUTORITE de la vie des routines : quand il trouve une
    vivante sans PID file, il PUBLIE le PID file (la verite partagee par tous).

    Retourne (messages, erreurs).
    """
    messages = []
    erreurs = 0
    for nom, chemin_routine in BOUCLES:
        chemin_pid = chemin_routine / PID_PAR_NOM[nom]
        if chemin_pid.exists():
            continue  # deja publie : la routine est visible de tout le monde
        pid_systeme = rechercher_pid_routine(nom, chemin_routine)
        if pid_systeme is None:
            continue  # absente du systeme : c'est la relance qui s'en charge
        try:
            chemin_pid.write_text(str(pid_systeme) + "\n", encoding=ENCODAGE)
            messages.append("PID file recree : " + nom + " (PID " + str(pid_systeme) + ")")
        except OSError:
            messages.append("ALERTE : impossible de creer le PID file de " + nom)
            erreurs += 1
    return messages, erreurs


def boot_check(intervalle=INTERVALLE_OVERRIDE_DEFAUT):
    """Diagnostic + nettoyage au demarrage de la Matrice.

    1. Nettoie les PID files fantomes (fichier sans processus correspondant).
    2. Detecte les processus orphelins (processus python dans routines/ sans
       serveur parent superviseur) et les termine.
    3. Recree les PID files des processus vivants manquants.
    4. Relance les processus manquants ou morts (chaque routine repart avec
       SON intervalle declare, sauf override explicite de l'operateur).
    5. Signale un resume.

    Retourne (code, messages) : code=0 si OK, code>0 si alertes/corrections.
    """
    from fonctions import processus_vivant

    messages = []
    code = 0

    # ------------------------------------------------------------------ 1. Fantomes
    # Nettoyage des PID files fantomes (serveur + boucles).
    fantomes_netoyes = 0
    # Serveur.
    if CHEMIN_PID_SERVER.exists():
        pid_serveur = lire_pid_fichier(CHEMIN_PID_SERVER)
        if pid_serveur is not None and not processus_vivant(pid_serveur):
            try:
                CHEMIN_PID_SERVER.unlink()
                fantomes_netoyes += 1
                messages.append("fantome nettoye : serveur (PID " + str(pid_serveur) + ")")
            except OSError:
                pass
    # Boucles.
    for nom, chemin_routine in BOUCLES:
        chemin_pid = chemin_routine / PID_PAR_NOM[nom]
        if chemin_pid.exists():
            pid_boucle = lire_pid_fichier(chemin_pid)
            if pid_boucle is not None and not processus_vivant(pid_boucle):
                try:
                    chemin_pid.unlink()
                    fantomes_netoyes += 1
                    messages.append("fantome nettoye : " + nom + " (PID " + str(pid_boucle) + ")")
                except OSError:
                    pass

    # ------------------------------------------------------------------ 2. Orphelins
    # Un processus orphelin = un processus python dans routines/ dont le
    # parent (serveur) n'est pas le serveur demarre (ou n'existe pas).
    # On les termine et on recree leur PID file a zero.
    orphelins_termines = 0
    for nom, chemin_routine in BOUCLES:
        pid_orphelin = rechercher_pid_routine(nom, chemin_routine)
        if pid_orphelin is None:
            continue
        # La boucle est vivante dans le systeme. Est-elle orpheline ?
        # Une boucle est orpheline si son PID file pointe vers un autre PID
        # ou n'existe pas, alors qu'elle tourne deja.
        chemin_pid = chemin_routine / PID_PAR_NOM[nom]
        pid_file = lire_pid_fichier(chemin_pid)
        if pid_file is not None and pid_file == pid_orphelin:
            # La boucle a deja son PID file correct : elle est supervisee.
            messages.append(nom + " : deja supervisee (PID " + str(pid_orphelin) + ")")
            continue
        if pid_file is not None and pid_file != pid_orphelin:
            # Le PID file pointe vers un autre PID : l'ancien est fantome,
            # celui-ci est orphelin (ou un relance manuellement).
            messages.append("orphelin detecte : " + nom + " (PID systeme " + str(pid_orphelin) + ", PID file " + str(pid_file) + ")")
            try:
                chemin_pid.unlink()
            except OSError:
                pass
            # On laisse le processus tourner : il sera supervise par le serveur
            # quand celui-ci recrira le PID file (etape 3).
        else:
            # La boucle tourne mais sans PID file : orpheline (perdue au redemarrage).
            messages.append("orphelin : " + nom + " (PID " + str(pid_orphelin) + ", sans PID file)")

    # ------------------------------------------------------------------ 3. Recreation PID files
    # UNE SEULE implementation, partagee avec la boucle principale.
    messages_recree, erreurs_recree = recreer_pid_files()
    messages.extend(messages_recree)
    if erreurs_recree:
        code = max(code, 2)

    # ------------------------------------------------------------------ 4. Relance
    # Boucles absentes du systeme : relancer avec l'intervalle du server.
    for nom, chemin_routine in BOUCLES:
        pid_systeme = rechercher_pid_routine(nom, chemin_routine)
        if pid_systeme is not None:
            continue  # La boucle tourne (voir etape 3).
        # La boucle est absente : relancer. On retire SON drapeau d'arret :
        # un drapeau laisse par un `server arret` pendant que la routine etait
        # deja morte ferait s'arreter la routine a peine relancee.
        chemin_drapeau = chemin_routine / DRAPEAU_PAR_NOM[nom]
        if chemin_drapeau.exists():
            try:
                chemin_drapeau.unlink()
            except OSError:
                pass
        script, arguments = commander(nom, intervalle)
        pid_nouveau, duree_ms = lancer_invisible(chemin_routine, arguments, script=script)
        messages.append("relance : " + nom + " (PID " + str(pid_nouveau) + ")")
        code = max(code, 1)

    # ------------------------------------------------------------------ 5. Serveur
    # Le serveur vient de s'ecrire un PID (juste au-dessus dans __main__).
    # On verifie que le PID file est coherent.
    if CHEMIN_PID_SERVER.exists():
        pid_serveur = lire_pid_fichier(CHEMIN_PID_SERVER)
        if pid_serveur is not None and processus_vivant(pid_serveur):
            messages.append("serveur demarre (PID " + str(pid_serveur) + ")")
        else:
            if pid_serveur is not None:
                messages.append("ALERTE : serveur (PID " + str(pid_serveur) + ") inactive")
                code = max(code, 2)
            else:
                messages.append("ALERTE : PID file serveur illisible")
                code = max(code, 2)
    else:
        messages.append("ALERTE : PID file serveur absent")
        code = max(code, 2)

    if fantomes_netoyes:
        messages.insert(0, "[" + str(fantomes_netoyes) + "] fantome(s) nettoye(s)")
    if orphelins_termines:
        messages.insert(0, "[" + str(orphelins_termines) + "] orphelin(s) termine(s)")

    return code, messages


def commander(nom, intervalle_override=None):
    """Retourne (script, arguments) de lancement d'une routine (table UNIQUE).

    L'ordre vient de COMMANDE_PAR_NOM (constants.py) : le server ne recopie
    plus ni les verbes ni le SCRIPT de lancement (deux tables = deux verites).
    Le script compte : le lanceur supposait `main.py`, ce qui excluait de fait
    le routeur de maintenance (dont le fichier est `routeur.py`) de la
    supervision -- il est reste mort du 2026-09-12 au 2026-09-13 avec 18
    alertes bloquees derriere lui.
    L'option d'intervalle n'est ajoutee QUE si l'operateur a demande un override
    explicite : par defaut la routine repart avec SON temps declare.
    """
    script, commande, option_intervalle = COMMANDE_PAR_NOM[nom]
    arguments = list(commande)
    if intervalle_override is not None and option_intervalle:
        arguments += [option_intervalle, str(intervalle_override)]
    return script, arguments


def demander_arret_routines():
    """Pose les drapeaux cooperatifs de toutes les routines supervisees."""
    messages = []
    for nom, chemin_routine in BOUCLES:
        chemin_drapeau = chemin_routine / DRAPEAU_PAR_NOM[nom]
        try:
            chemin_drapeau.write_text("arret\\n", encoding=ENCODAGE)
            messages.append("arret demande : " + nom)
        except OSError as erreur:
            messages.append("ALERTE arret " + nom + " : " + str(erreur))
    return messages


def relancer_si_morte(nom, chemin_routine, intervalle_override=None):
    """Relance la routine si morte ; retourne (action, pid, duree_ms)."""
    pid = rechercher_pid_routine(nom, chemin_routine)
    if pid is not None:
        return "vivant", pid, 0
    script, arguments = commander(nom, intervalle_override)
    pid_nouveau, duree_ms = lancer_invisible(chemin_routine, arguments, script=script)
    return "RELANCEE", pid_nouveau, duree_ms


def ecrire_pid_server(pid):
    """Note le PID du server (atomique simple : petit fichier, LF forces)."""
    CHEMIN_PID_SERVER.write_text(str(pid) + "\n", encoding=ENCODAGE)


def boucle_principale(intervalle_override, once=False):
    """Boucle de surveillance : relance toute routine morte, jamais de fenetre."""
    pid = None  # place par le bloc principal (voir plus bas)
    while True:
        if CHEMIN_DRAPEAU_ARRET.exists():
            CHEMIN_DRAPEAU_ARRET.unlink()
            messages_arret = demander_arret_routines()
            print("Drapeau d'arret recu : le server matrice s'arrete proprement.")
            for message in messages_arret:
                print("  " + message)
            return 0
        # Avant de relancer, on republie les PID files manquants : c'est ce qui
        # empeche l'etat et le flux de croire morte une routine que le serveur
        # voit vivante (deux verites sur la meme chose).
        messages_recree, _ = recreer_pid_files()
        for message in messages_recree:
            print("[" + time.strftime("%H:%M:%S") + "] server matrice : " + message)
        actions = []
        for nom, chemin_routine in BOUCLES:
            action, _, duree_ms = relancer_si_morte(nom, chemin_routine, intervalle_override)
            if action == "RELANCEE":
                actions.append(nom + " (relancee en " + str(duree_ms) + " ms)")
        if actions:
            print("[" + time.strftime("%H:%M:%S") + "] server matrice : " + ", ".join(actions))
        if once:
            return 0
        # Attente DECOUPEE : `server arret` ne doit pas se payer la cadence de
        # supervision (60 s). Avec une attente en un bloc, l'arret du SERVEUR
        # etait lui aussi une attente a l'aveugle -- exactement ce qu'on refuse
        # pour les routines. Le drapeau est consomme en tete de boucle (un seul
        # proprietaire), donc on se contente de le SURVEILLER ici.
        attendre(INTERVALLE_SUPERVISION_SECONDES, CHEMIN_DRAPEAU_ARRET)


if __name__ == "__main__":
    import os

    arguments = sys.argv[1:]
    intervalle = INTERVALLE_OVERRIDE_DEFAUT
    once = "--once" in arguments
    if "--interval" in arguments:
        intervalle = int(arguments[arguments.index("--interval") + 1])
    pid_existant = lire_pid_fichier(CHEMIN_PID_SERVER)
    if pid_existant is not None and processus_vivant(pid_existant) and pid_existant != os.getpid():
        print("REFUS : server matrice deja actif (PID " + str(pid_existant) + ").")
        sys.exit(1)
    ecrire_pid_server(os.getpid())
    code_boot, messages_boot = boot_check(intervalle)
    if code_boot:
        print("[" + time.strftime("%H:%M:%S") + "] BOOT-CHECK : alertes de demarrage")
        for m in messages_boot:
            print("  " + m)
    else:
        print("[" + time.strftime("%H:%M:%S") + "] BOOT-CHECK : OK")
        for m in messages_boot:
            print("  " + m)
    code = boucle_principale(intervalle, once)
    # Le PID appartient a ce processus : une sonde --once le retire aussi,
    # sinon elle laisserait un PID fantome et bloquerait le prochain demarrage.
    if CHEMIN_PID_SERVER.exists():
        pid_note = lire_pid_fichier(CHEMIN_PID_SERVER)
        if pid_note == os.getpid():
            CHEMIN_PID_SERVER.unlink()
    sys.exit(code)
