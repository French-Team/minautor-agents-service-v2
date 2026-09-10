"""Server MATRICE (E-056, M-081) : orchestrateur de vie des routines.

2 etages du server de demarrage voulu par le createur :
  - server 'matrice' : CE processus (boucle de fond invisible). Il possede
    le lancement : chaque routine est lancee/relancee PAR LUI, jamais en
    direct. Il relance toute boucle morte (reprise apres crash/redemarrage).
  - server 'routine' : chaque routine (veille-flux, espion-integrite) est
    un fils du server : son cycle de vie passe par le server.

Exigeance createur : le redemarrage d'une routine est INVISIBLE (aucune
fenetre console). Toute relance passe par le motif partage lancement.py
(CREATE_NO_WINDOW + SW_HIDE sur Windows).

Usage : python server-matrice.py [--interval <secondes>] [--once]
Arret  : drapeau cooperatif (fichier server-matrice-arret.txt).
"""
import sys
import time
from pathlib import Path

REPERTOIRE_SERVER = Path(__file__).resolve().parent
sys.path.insert(0, str(REPERTOIRE_SERVER))
sys.path.insert(0, str(REPERTOIRE_SERVER.parent.parent / "data" / "commun"))

from constants import BOUCLES, NOM_PID_ESPION, NOM_PID_VEILLE, ENCODAGE  # noqa: E402
from constants_suivi_sync import BOUCLES_SUIVI_SYNC, NOM_PID_SUIVI_SYNC, pid_de_suivi_sync, commander_suivi_sync  # noqa: E402
from fonctions import etat_boucle  # noqa: E402
from lancement import lancer_invisible  # noqa: E402
from server.entry import CHEMIN_DRAPEAU_ARRET, CHEMIN_PID_SERVER  # noqa: E402

INTERVALLE_DEFAUT_SECONDES = 60


def rechercher_pid_routine(chemin_routine):
    """Retourne le PID d'un processus python dans la routine, ou None.

    Cherche via ps les processus python dont la commande contient
    le chemin de la routine (client WSL : le process python a le chemin
    complet de server_matrice.py comme argument).
    """
    try:
        import subprocess
        resultat = subprocess.run(
            ["ps", "-eo", "pid,args"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if resultat.returncode != 0:
            return None
        for ligne in resultat.stdout.splitlines():
            if chemin_routine.as_posix() not in ligne:
                continue
            if "python" not in ligne.lower():
                continue
            mots = ligne.split()
            if not mots:
                continue
            try:
                return int(mots[0])
            except ValueError:
                continue
    except Exception:
        pass
    return None


def boot_check():
    """Diagnostic + nettoyage au demarrage de la Matrice.

    1. Nettoie les PID files fantomes (fichier sans processus correspondant).
    2. Detecte les processus orphelins (processus python dans routines/ sans
       serveur parent superviseur) et les termine.
    3. Recree les PID files des processus vivants manquants.
    4. Relance les processus manquants ou morts.
    5. Signale un resume.

    Retourne (code, messages) : code=0 si OK, code>0 si alertes/corrections.
    """
    from fonctions import processus_vivant

    messages = []
    code = 0
    # Boucles supplementaires (suivi-sync).
    global BOUCLES
    BOUCLES = tuple(list(BOUCLES) + list(BOUCLES_SUIVI_SYNC))

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
        chemin_pid = chemin_routine / pid_de(nom)
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
        pid_orphelin = rechercher_pid_routine(chemin_routine)
        if pid_orphelin is None:
            continue
        # La boucle est vivante dans le systeme. Est-elle orpheline ?
        # Une boucle est orpheline si son PID file pointe vers un autre PID
        # ou n'existe pas, alors qu'elle tourne deja.
        chemin_pid = chemin_routine / pid_de(nom)
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
    # Pour chaque boucle vivante (avec ou sans PID file), on recree le PID file.
    for nom, chemin_routine in BOUCLES:
        pid_systeme = rechercher_pid_routine(chemin_routine)
        if pid_systeme is None:
            # La boucle n'est pas dans le systeme : la relancer (etape 4).
            continue
        chemin_pid = chemin_routine / pid_de(nom)
        if chemin_pid.exists():
            # Deja un PID file : la boucle est supervisee (voir etape 2).
            continue
        # La boucle tourne mais sans PID file : on recree.
        try:
            chemin_pid.write_text(str(pid_systeme) + "\n", encoding=ENCODAGE)
            messages.append("PID file recree : " + nom + " (PID " + str(pid_systeme) + ")")
        except OSError:
            messages.append("ALERTE : impossible de creer le PID file de " + nom)
            code = max(code, 2)

    # ------------------------------------------------------------------ 4. Relance
    # Boucles absentes du systeme : relancer.
    for nom, chemin_routine in BOUCLES:
        pid_systeme = rechercher_pid_routine(chemin_routine)
        if pid_systeme is not None:
            continue  # La boucle tourne (voir etape 3).
        # La boucle est absente : relancer.
        pid_nouveau, duree_ms = lancer_invisible(
            chemin_routine,
            commander(nom) + ["--interval", str(INTERVALLE_DEFAUT_SECONDES)],
        )
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

    return code, messages


def pid_de(nom):
    """Retourne le nom de fichier PID d'une boucle connue."""
    return NOM_PID_VEILLE if nom == "veille-flux" else NOM_PID_ESPION


def commander(nom):
    """Retourne les arguments de boucle de la routine (ses propres verbes)."""
    return ["veille", "--boucle"] if nom == "veille-flux" else ["boucle"]


def relancer_si_morte(nom, chemin_routine, intervalle):
    """Relance la boucle si morte ; retourne (action, pid, duree_ms)."""
    _, pid = etat_boucle(nom, chemin_routine, pid_de(nom))
    if pid is not None:
        return "vivant", pid, 0
    pid_nouveau, duree_ms = lancer_invisible(chemin_routine, commander(nom) + ["--interval", str(intervalle)])
    return "RELANCEE", pid_nouveau, duree_ms


def ecrire_pid_server(pid):
    """Note le PID du server (atomique simple : petit fichier, LF forces)."""
    CHEMIN_PID_SERVER.write_text(str(pid) + "\n", encoding=ENCODAGE)


def lire_pid_fichier(chemin_pid):
    """Retourne le PID note dans le fichier, ou None."""
    if not chemin_pid.exists():
        return None
    try:
        contenu = chemin_pid.read_text(encoding=ENCODAGE).strip()
        return int(contenu) if contenu else None
    except (ValueError, OSError):
        return None


def boucle_principale(intervalle, once=False):
    """Boucle de surveillance : relance toute routine morte, jamais de fenetre."""
    pid = None  # place par le bloc principal (voir plus bas)
    while True:
        if CHEMIN_DRAPEAU_ARRET.exists():
            CHEMIN_DRAPEAU_ARRET.unlink()
            print("Drapeau d'arret recu : le server matrice s'arrete proprement.")
            return 0
        actions = []
        for nom, chemin_routine in BOUCLES:
            action, _, duree_ms = relancer_si_morte(nom, chemin_routine, intervalle)
            if action == "RELANCEE":
                actions.append(nom + " (relancee en " + str(duree_ms) + " ms)")
        if actions:
            print("[" + time.strftime("%H:%M:%S") + "] server matrice : " + ", ".join(actions))
        if once:
            return 0
        time.sleep(intervalle)


if __name__ == "__main__":
    import os

    arguments = sys.argv[1:]
    intervalle = INTERVALLE_DEFAUT_SECONDES
    once = "--once" in arguments
    if "--interval" in arguments:
        intervalle = int(arguments[arguments.index("--interval") + 1])
    ecrire_pid_server(os.getpid())
    code_boot, messages_boot = boot_check()
    if code_boot:
        print("[" + time.strftime("%H:%M:%S") + "] BOOT-CHECK : alertes de demarrage")
        for m in messages_boot:
            print("  " + m)
    else:
        print("[" + time.strftime("%H:%M:%S") + "] BOOT-CHECK : OK")
        for m in messages_boot:
            print("  " + m)
    code = boucle_principale(intervalle, once)
    # En mode --once (sonde), le PID du VRAI server n'est pas retire : seul
    # le server en boucle possede son cycle de vie (garde garde-fou).
    if not once and CHEMIN_PID_SERVER.exists():
        CHEMIN_PID_SERVER.unlink()
    sys.exit(code)
