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

Ce module est ENFIN le DOMICILE DE LA TRACE DU LANCEMENT (EO-409). Mesure MO-397 :
le routeur-maintenance est reste mort 26 h sans que personne ne puisse lire
POURQUOI, et la cause (un NameError a l'allumage) n'a ete trouvee qu'en
REPRODUISANT A LA MAIN -- parce que la sortie du fils partait dans DEVNULL : le
traceback d'un enfant qui meurt au demarrage n'existait NULLE PART. Ici : la sortie
du fils va dans un JOURNAL DE LANCEMENT, dans le dossier de la routine, REEcrit a
chaque lancement (il dit LE DERNIER lancement, jamais une histoire sans fin), et la
lecture en est BORNEE. Les observateurs qui CONSTATENT la mort -- la porte `vie` et
le maillon 7 du flux -- peuvent donc NOMMER la cause, et ils le font SANS ATTENDRE
(l'attente ne prouve rien) : la trace existe apres coup.
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


def console_de_ce_processus():
    """Vrai si CE processus possede une console -- donc si ses fils y aboutissent.

    MESURE DU 2026-09-25 (defaut introduit par le lot EO-430, corrige ici) : les
    drapeaux etaient poses INCONDITIONNELLEMENT. Un fils lance ainsi recoit une
    console a LUI, invisible : sa SORTIE N'ARRIVE PLUS au parent. Constate sur le
    LANCEUR lui-meme -- `lancer.py <outil>` ne rendait plus une seule ligne, ni un
    rapport, ni meme un REFUS, alors que le meme appel en DIRECT parlait. Deux
    juges de la suite (titre, cartes) le mordaient : `code 2, refus ABSENT`.
    La regle juste n'est pas "toujours cacher la console" mais "n'en ouvrir AUCUNE
    quand on n'en a pas" : un parent SANS console qui engendre un fils console
    ferait apparaitre une fenetre (c'est le seul cas a couvrir) ; un parent QUI EN A
    UNE transmet la sienne, aucune fenetre ne nait, et la sortie est visible.
    """
    if os.name != "nt":
        return True
    try:
        import ctypes
        return bool(ctypes.windll.kernel32.GetConsoleWindow())
    except Exception:
        return False


def drapeaux_invisibles():
    """Retourne (creationflags, startupinfo, start_new_session) pour Popen.

    Windows : les drapeaux ne sont poses QUE si ce processus n'a pas de console
    (voir `console_de_ce_processus`) -- sinon le fils herite la notre, la sortie
    reste lisible, et aucune fenetre ne nait.
    """
    if os.name == "nt":
        if console_de_ce_processus():
            return 0, None, False
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = 0  # SW_HIDE : la console du fils n'est jamais montree
        return (
            subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP,
            info,
            False,
        )
    return 0, None, True


def drapeaux_popen():
    """Les kwargs a SPLATTER dans un subprocess.run/Popen : le fils jamais montre.

    Le domicile rend ici ce qu un appelant DIRECT de subprocess doit ajouter pour se
    conformer a la regle du zero-fenetre : creationflags + startupinfo sur Windows,
    start_new_session ailleurs. Cette forme existe pour les appelants qui ne peuvent
    pas passer par `lancer_invisible` (appels SYNCHRONES dont on lit la sortie :
    tasklist, powershell, py_compile, une porte de la Matrice) :

        from lancement import drapeaux_popen
        resultat = subprocess.run(commande, capture_output=True, **drapeaux_popen())

    Un appelant qui lance un processus SANS ce dictionnaire est un lancement A NU :
    la convention le refuse (mesure EO-428 : 139 sites a nu dont 8 atteints par un
    processus de fond) et le controle `verifier-contrats-outils` le MORD.
    L import de ce module depuis une routine doit etre DIFFERE (dans la fonction) :
    `data/commun` n entre dans sys.path qu avec `constants`, jamais avant.
    """
    creationflags, startupinfo, nouvelle_session = drapeaux_invisibles()
    if os.name == "nt":
        return {"creationflags": creationflags, "startupinfo": startupinfo}
    return {"start_new_session": nouvelle_session}


# --- LA TRACE DU LANCEMENT (EO-409) ----------------------------------------
# Ou va la sortie du fils, et comment on la lit SANS attendre.
# Le journal vit dans le dossier de la ROUTINE (le lanceur ne connait qu'elle) et
# il est REEcrit a chaque lancement : il dit le DERNIER lancement, ce qui est
# exactement la question posee quand une routine est morte. Rien ne s'accumule
# d'un lancement a l'autre.
NOM_JOURNAL_LANCEMENT = "journal-lancement.log"

# LECTURE BORNEE : un observateur ne paie jamais la verbosite d'un enfant. On ne
# lit que la QUEUE du journal, jusqu'a ce plafond, et la lecture DIT combien
# d'octets ont ete lus sur la taille reelle.
PLAFOND_OCTETS_LUS = 4096
# La CAUSE rendue a l'affichage est UNE ligne, bornee : un message d'erreur geant
# ne doit ni noyer l'etat des routines ni le verdict du flux.
PLAFOND_CARACTERES_CAUSE = 200


def chemin_journal_lancement(chemin_routine):
    """Le journal de lancement d'une routine -- dans SON dossier."""
    return Path(chemin_routine) / NOM_JOURNAL_LANCEMENT


def lire_trace_lancement(chemin_routine, octets=PLAFOND_OCTETS_LUS):
    """(texte borne, information de lecture) du journal de lancement.

    Rend ("", motif) quand il n'y a rien a lire : le motif NOMME la raison (journal
    absent, illisible), jamais un silence. L'information dit COMBIEN d'octets ont
    ete lus sur la taille reelle -- une lecture bornee qui ne se mesure pas est une
    intention.
    """
    chemin = chemin_journal_lancement(chemin_routine)
    if not chemin.is_file():
        return "", NOM_JOURNAL_LANCEMENT + " ABSENT"
    try:
        taille = chemin.stat().st_size
        with open(str(chemin), "rb") as flux:
            if taille > octets:
                flux.seek(taille - octets)
            bloc = flux.read()
    except OSError as erreur:
        return "", NOM_JOURNAL_LANCEMENT + " ILLISIBLE (" + str(erreur)[:60] + ")"
    information = (NOM_JOURNAL_LANCEMENT + " : " + str(len(bloc)) + " o lus sur "
                   + str(taille) + " o")
    return bloc.decode(ENCODAGE, errors="replace"), information


def cause_du_dernier_lancement(chemin_routine, octets=PLAFOND_OCTETS_LUS,
                               caracteres=PLAFOND_CARACTERES_CAUSE):
    """La DERNIERE ligne non vide du journal : la CAUSE d'un arret, ou None.

    Un traceback finit TOUJOURS par la ligne de l'exception : c'est elle qui NOMME
    la cause, et c'est elle qui est rendue. None vaut "rien a dire" (journal absent
    ou vide) -- l'appelant le DIT alors, il ne l'invente pas, et il n'attend pas
    pour le savoir.
    """
    texte, _ = lire_trace_lancement(chemin_routine, octets)
    for ligne in reversed(texte.splitlines()):
        propre = ligne.strip()
        if propre:
            return propre[:caracteres]
    return None


def lancer_invisible(chemin_routine, arguments, script="main.py"):
    """Lance `python <script> <arguments>` SANS aucune fenetre, retourne (pid, duree_ms).

    Par defaut script='main.py' (convention des routines) ; le server matrice
    passe script='server_matrice.py'.
    LA SORTIE DU FILS VA DANS SON JOURNAL DE LANCEMENT (EO-409), plus dans DEVNULL :
    un enfant qui meurt a l'allumage laisse desormais son traceback, et
    l'observateur qui CONSTATE la mort peut le NOMMER. Le parent REFERME le fichier
    aussitot apres le Popen (le fils garde son propre descripteur) : une poignee
    laissee ouverte bloquerait la reecriture au prochain lancement. Si le journal
    est IMPOSSIBLE a ouvrir, on lance quand meme (jamais de fenetre, jamais un
    lancement perdu) -- la trace en moins, et personne n'est prevenu : c'est DIT ici.
    La duree mesuree est celle de l'appel de lancement (metrique E-055/E-056).
    """
    debut = time.monotonic()
    creationflags, startupinfo, nouvelle_session = drapeaux_invisibles()
    try:
        trace = open(str(chemin_journal_lancement(chemin_routine)), "w",
                     encoding=ENCODAGE, errors="replace", newline="\n")
    except OSError:
        trace = None
    processus = subprocess.Popen(
        # `-u` (non bufferise) : sans lui, un fils VIVANT garde sa sortie dans son
        # tampon (8 Ko) et le journal resterait VIDE -- mesure du 2026-09-24, juste
        # apres la relance des 7 routines : 8 journaux crees, tous a 0 o. Avec `-u`,
        # la trace arrive A LA MESURE, et une mort brutale ne perd pas le prelude.
        [sys.executable, "-u", str(Path(chemin_routine) / script)] + list(arguments),
        cwd=str(chemin_routine),
        stdout=trace if trace is not None else subprocess.DEVNULL,
        stderr=(subprocess.STDOUT if trace is not None else subprocess.DEVNULL),
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
        startupinfo=startupinfo,
        start_new_session=nouvelle_session,
    )
    if trace is not None:
        trace.close()
    duree_ms = int((time.monotonic() - debut) * 1000)
    return processus.pid, duree_ms
