# -*- coding: ascii -*-
"""fonctions/demarrage.py - UNE tache : la chaine de demarrage et
d'arret de JARVIS (mission [AT-1] 2026-08-23, validee utilisateur).

demarrage :
    1. tic des routines (jarvis EST le planificateur, protocole 16)
    2. verifier l'etat DEFCON (5 = dev gele : alerte)
    3. verifier les files d'attente et les agents bloques
    4. declarer jarvis operationnel (historise)

arret :
    - resume de session (defcon, files, routines)
    - historiser l'arret. Les files sont des JSONL persistes :
      rien a vider, l'etat survive au processus.

Pas de serveur : depuis v0.9.2 les routines tournent a chaque
invocation de jarvis - "lancer le serveur si arrete" est remplace
par le tic immediat des routines dues.
"""

from defcon import niveau_courant, ECHELLE
from routines import charger_etat, infos_routines, executer_routines
from historique import historiser
from hooks import _pid_actuel, routines_demarrer, routines_arreter

JARVIS = None  # rempli par _init_chemins()
import os
from pathlib import Path


def _init_chemins():
    global JARVIS
    if JARVIS is None:
        JARVIS = Path(__file__).parent.parent
    return JARVIS


def _etat_files():
    """(total_actives, details) sur file-asap + file-attente.
    Actives = statut != TERMINE."""
    dossier = _init_chemins() / "files"
    import json
    total = 0
    details = []
    for nom in ("file-asap.jsonl", "file-attente.jsonl"):
        chemin = dossier / nom
        if not chemin.exists():
            continue
        for ligne in chemin.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            try:
                e = json.loads(ligne)
            except ValueError:
                continue
            if e.get("statut") in ("TERMINE", "VIDE", None):
                continue
            total += 1
            details.append("[%s] %s" % (
                nom.replace(".jsonl", "").replace("file-", ""),
                (e.get("mission") or "")[:60]))
    return total, details


def _agents_bloques():
    """Agents avec au moins une priorite 1 non lue."""
    inbox = _init_chemins() / "inbox"
    import json
    bloques = []
    if not inbox.is_dir():
        return bloques
    for nom_fichier in sorted(inbox.glob("*.jsonl")):
        for ligne in nom_fichier.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            try:
                m = json.loads(ligne)
            except ValueError:
                continue
            if not m.get("lu") and m.get("priorite") == 1 \
                    and m.get("type") != "harnais-jarvis":
                bloques.append(nom_fichier.stem)
                break
    return bloques


def cmd_demarrage(args=None):
    """Chaine de demarrage complete : daemon -> DEFCON -> files ->
    operationnel."""
    session = getattr(args, "session", "") or ""
    print("=== JARVIS DEMARRAGE ===")

    # 1. routines : le daemon resident tick EN PERMANENCE (decision
    # utilisateur 2026-08-25) ; le tic immediat reste en filet.
    pid = _pid_actuel()
    if pid:
        print("[1/4] Daemon routines : DEJA EN MARCHE (pid %d)" % pid)
    else:
        routines_demarrer()
        pid = _pid_actuel()
        print("[1/4] Daemon routines : LANCE (pid %s)" % (pid or "?"))
    try:
        executer_routines()
        etat = charger_etat()
        n_routines = len(infos_routines())
        faites = sum(1 for r, _, _, a in infos_routines()
                     if a and etat.get(r, {}).get("derniere"))
        print("      Tic immediat : %d/%d routine(s) executee(s) au "
              "moins une fois" % (faites, n_routines))
    except Exception as e:
        print("      ERREUR tic : %s" % e)

    # 2. etat DEFCON
    niveau = niveau_courant()
    if niveau == 5:
        print("[2/4] DEFCON 5 - ARRET TOTAL : le dev est GELE. "
              "Escalade utilisateur requise avant toute mission.")
    elif niveau is None:
        print("[2/4] DEFCON : aucun niveau journalise (etat nominal)")
    else:
        print("[2/4] DEFCON %d - %s" % (niveau, ECHELLE[niveau]))

    # 3. files + agents bloques
    total, details = _etat_files()
    print("[3/4] Files d'attente : %d mission(s) active(s)" % total)
    for d in details:
        print("      %s" % d)
    bloques = _agents_bloques()
    if bloques:
        print("      AGENTS BLOQUES (P1 non lu) : %s"
              % ", ".join(sorted(set(bloques))))
    else:
        print("      aucun agent bloque")

    # 4. operationnel
    print("[4/4] JARVIS OPERATIONNEL")
    historiser("jarvis", "Demarrage de session : routines tic, "
               "DEFCON=%s, %d mission(s) en file" %
               (niveau if niveau is not None else "aucun", total),
               session=session)


def cmd_arret(args=None):
    """Extinction propre : resume de session + historisation.
    Les files sont persistees (JSONL) : rien a vider."""
    session = getattr(args, "session", "") or ""
    niveau = niveau_courant()
    total, _ = _etat_files()
    print("=== JARVIS ARRET ===")
    routines_arreter()
    print("- DEFCON : %s" % (
        "%d (%s)" % (niveau, ECHELLE[niveau])
        if niveau is not None else "aucun"))
    print("- Files : %d mission(s) active(s) (persistees, rien a vider)"
          % total)
    print("- Routines : daemon arrete ; reprise au prochain "
          "jarvis.py demarrage")
    print("- Etat sauvegarde : session recoverable par jarvis.py demarrage")
    historiser("jarvis", "Arret propre : resume ecrit, %d mission(s) "
               "en file, DEFCON=%s" %
               (total, niveau if niveau is not None else "aucun"),
               session=session)
