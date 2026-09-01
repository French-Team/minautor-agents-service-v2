#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-processus-residuels.py
#
# Detecte les PROCESSUS RESIDUELS du workspace (demande utilisateur
# 2026-08-16) : les scripts temporaires et les tests laissent parfois des
# processus orphelins actifs (python/node/bash) qui ne meurent pas.
#
# Critere de detection (decision utilisateur : commande projet + orphelins) :
#   - PROJET  : processus python/node/bash dont la COMMANDE reference le
#               projet (chemin Z:/analyste-in-console, /z/analyste-in-console,
#               tmp-*, .zz-*, cerveau-projet/) - nos scripts residuels
#   - ORPHELIN : processus dont le PARENT est mort (PPID inexistant) - un
#                script tue sans attendre son enfant
#
# LISTE BLANCHE PROTEGEE (jamais signales, jamais tuables) :
#   - freebuff : le client (node.exe du runtime Freebuff)
#   - unsloth  : le studio python (python.exe de l utilisateur)
#
# Compatibilite :
#   - Windows (win32) : Get-CimInstance Win32_Process via powershell
#   - Linux/macOS     : ps -eo pid,ppid,comm,args
#
# Sortie : liste des processus residuels (PID + nom + commande + justification
# PROJET/ORPHELIN) + compteur + verdict (0 = AUCUN RESIDUEL, sinon
# RESIDUELS DETECTES avec nombre).
#
# Options :
#   --detail        Detail complet (commande tronquee a 200 car)
#   --rapport <f>   Ecrit le rapport markdown
#   --verbose       Affiche les details de detection
#   --version       Affiche la version
#   --aide          Affiche cette aide
#
# Usage:
#   python3 detecter-processus-residuels.py
#   python3 detecter-processus-residuels.py --detail
#   python3 detecter-processus-residuels.py --rapport rapport-processus.md
#
# Version : 0.1.1
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (detecter-).
# =============================================================================
import argparse
import io
import json
import os
import re
import subprocess
import sys

VERSION = "0.1.1"
STATUT = "ebauche"

# Liste blanche protegee : processus legitimes jamais signales ni tuables.
# PRINCIPE (decision utilisateur 2026-08-30) : on ne melange JAMAIS des
# familles distinctes dans une meme structure. Deux familles, deux tuples
# separes et nommes explicitement : une de l ENVIRONNEMENT de session,
# l autre des DAEMONS du projet. Comparaison insensible a la casse sur le
# nom du processus ET la commande.

# FAMILLE 1 - ENVIRONNEMENT DE SESSION : les outils d edition qui tournent
#   pendant qu on travaille. Sans eux la session serait coupee. Ils existent
#   seulement pendant l interaction, PAS toute la journee.
LISTE_BLANCHE_SESSION = (
    "freebuff",  # le client node.exe (runtime Freebuff, la session en cours)
    "unsloth",  # le studio python (python.exe de l utilisateur)
    "codebuff",  # l assistant de codage (le moteur auquel l agent est relie)
)

# FAMILLE 2 - DAEMONS PERSISTANTS DU PROJET : les serveurs qui tournent
#   TOUTE LA JOURNEE en fond (decision 2026-08-30, baseline v2). Ce sont des
#   serveurs legaux jamais a nettoyer - sinon test-085 les signalerait comme
#   residuels (cause de sa desactivation puis de sa reactivation).
LISTE_BLANCHE_DAEMONS = (
    "oracle-server.py",  # serveur oracle : pilote les cartes/arbres des agents
    "routines-server.py",  # serveur des routines de surveillance v1
)

# Union des deux familles utilisee pour la detection (une seule source de
# verite pour la comparaison, deux listes pour la lisibilite).
LISTE_BLANCHE = LISTE_BLANCHE_SESSION + LISTE_BLANCHE_DAEMONS

# Marquers du projet dans la commande d un processus.
MARQUEURS_PROJET = (
    "analyste-in-console",
    "tmp-",
    ".zz-",
    ".tmp-",
    "cerveau-projet/",
    "cerveau-projet\\",
)


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def est_liste_blanche(nom, commande):
    """Vrai si le processus appartient a la liste blanche (jamais touche)."""
    champs = (nom or "").lower() + " " + (commande or "").lower()
    return any(m in champs for m in LISTE_BLANCHE)


def lister_processus_windows():
    """Liste les processus python/node/bash via Get-CimInstance (Windows).
    Retourne une liste de dicts : pid, ppid, nom, commande."""
    script_ps = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.Name -match 'python|node|bash' } | "
        "Select-Object ProcessId,ParentProcessId,Name,CommandLine | "
        "ConvertTo-Json -Compress"
    )
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", script_ps],
            stderr=subprocess.DEVNULL, timeout=30)
        texte = out.decode("utf-8", errors="replace").strip()
        if not texte:
            return []
        data = json.loads(texte)
        if isinstance(data, dict):
            data = [data]
        processus = []
        for p in data:
            processus.append({
                "pid": p.get("ProcessId"),
                "ppid": p.get("ParentProcessId"),
                "nom": p.get("Name", ""),
                "commande": p.get("CommandLine", "") or "",
            })
        return processus
    except Exception:
        return []


def lister_processus_posix():
    """Liste les processus python/node/bash via ps (Linux/macOS)."""
    try:
        out = subprocess.check_output(
            ["ps", "-eo", "pid=,ppid=,comm=,args="],
            stderr=subprocess.DEVNULL, timeout=15)
        processus = []
        for ligne in out.decode("utf-8", errors="replace").splitlines():
            ligne = ligne.strip()
            if not ligne:
                continue
            parts = ligne.split(None, 3)
            if len(parts) < 4:
                continue
            pid, ppid, nom, args = parts
            if not re.search(r"(python|node|bash)", nom, re.IGNORECASE):
                continue
            processus.append({
                "pid": int(pid),
                "ppid": int(ppid),
                "nom": nom,
                "commande": args,
            })
        return processus
    except Exception:
        return []


def lister_processus():
    """Retourne la liste des processus candidats, selon la plateforme."""
    if sys.platform == "win32":
        return lister_processus_windows()
    return lister_processus_posix()


def lister_pids_vivants():
    """Retourne l ENSEMBLE de tous les PID vivants du systeme (toute
    plateforme). Sert a savoir si le PPID d un processus candidat existe
    encore : un processus dont le parent est MORT est un ORPHELIN (residuel),
    un processus dont le parent vit est un processus actif legitime (meme si
    sa commande reference le projet - ex : les autres tests du pool qui
    tournent pendant le scan)."""
    try:
        if sys.platform == "win32":
            out = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command",
                 "Get-CimInstance Win32_Process | Select-Object -ExpandProperty ProcessId | ConvertTo-Json -Compress"],
                stderr=subprocess.DEVNULL, timeout=30)
            texte = out.decode("utf-8", errors="replace").strip()
            if not texte:
                return set()
            data = json.loads(texte)
            if isinstance(data, int):
                return {int(data)}
            return set(int(p) for p in data if str(p).isdigit())
        out = subprocess.check_output(["ps", "-eo", "pid="],
                                      stderr=subprocess.DEVNULL, timeout=15)
        return set(int(l.strip()) for l in out.decode("utf-8", errors="replace").splitlines()
                   if l.strip().isdigit())
    except Exception:
        return set()


def pid_existe(pid):
    """Verifie qu un pid existe encore (toute plateforme)."""
    if not pid:
        return False
    try:
        if sys.platform == "win32":
            out = subprocess.check_output(
                ["tasklist", "/FI", "PID eq %d" % pid, "/FO", "CSV", "/NH"],
                stderr=subprocess.DEVNULL, timeout=15)
            return str(pid) in out.decode("utf-8", errors="replace")
        os.kill(int(pid), 0)
        return True
    except Exception:
        return False


def chaine_parente(processus):
    """Retourne l ensemble des PID de la chaine parente du processus courant.
    Ces processus sont LEGITIMES (le shell qui lance la commande, les parents)
    : ils ne sont jamais des residuels, meme si leur commande reference le
    projet (ce sont les processus du test/scan en cours)."""
    pids = set()
    courant = os.getpid()
    pids.add(courant)
    by_pid = {p["pid"]: p for p in processus if p.get("pid")}
    pid = courant
    for _ in range(20):
        p = by_pid.get(pid)
        if not p:
            break
        ppid = p.get("ppid")
        if not ppid or ppid in pids:
            break
        pids.add(ppid)
        pid = ppid
    return pids


def analyser(verbose=False):
    """Detecte les processus residuels. Retourne la liste des dicts :
    pid, ppid, nom, commande, justification (PROJET/ORPHELIN).
    CRITERE (decision utilisateur : commande projet + orphelins) : un
    processus est un RESIDUEL si et seulement si son PARENT EST MORT (PPID
    absent des PID vivants du systeme) - c est un orphelin. La justification
    est PROJET si la commande reference le projet, sinon ORPHELIN. Un
    processus dont le parent VIT est un processus actif legitime (ex : les
    autres tests du pool qui tournent pendant le scan) - jamais signale.
    Exclut la chaine parente du processus courant (le scan en cours) et la
    liste blanche (freebuff/unsloth/codebuff)."""
    processus = lister_processus()
    pids_vivants = lister_pids_vivants()
    exclus = chaine_parente(processus)
    residuels = []
    for p in processus:
        nom = p.get("nom", "") or ""
        commande = p.get("commande", "") or ""
        pid = p.get("pid")
        ppid = p.get("ppid")
        if pid in exclus:
            if verbose:
                print("  [chaine] pid=%s %s (processus du scan en cours)" % (pid, nom))
            continue
        if est_liste_blanche(nom, commande):
            if verbose:
                print("  [blanche] pid=%s %s (jamais signale)" % (pid, nom))
            continue
        if ppid is not None and pid_existe(pid) and ppid not in pids_vivants:
            # Parent MORT : orphelin -> residuel.
            commande_bas = commande.lower()
            if any(m in commande_bas for m in MARQUEURS_PROJET):
                justif = "PROJET"
            else:
                justif = "ORPHELIN"
            if verbose:
                print("  [orphelin] pid=%s ppid=%s %s" % (pid, ppid, nom))
            residuels.append({
                "pid": pid,
                "ppid": ppid,
                "nom": nom,
                "commande": commande,
                "justification": justif,
            })
        elif verbose and ppid is not None:
            print("  [actif] pid=%s ppid=%s %s (parent vivant, legitime)" % (pid, ppid, nom))
    return residuels


def formater_commande(commande, detail=False):
    if not commande:
        return "(sans commande)"
    if detail and len(commande) <= 200:
        return commande
    if detail:
        return commande[:200] + "..."
    return commande[:90] + ("..." if len(commande) > 90 else "")


def main():
    parser = argparse.ArgumentParser(
        prog="detecter-processus-residuels",
        description="Detecte les processus residuels du workspace (PID).")
    parser.add_argument("--detail", action="store_true",
                        help="detail complet des commandes")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="ecrit le rapport markdown")
    parser.add_argument("--verbose", action="store_true",
                        help="affiche les details de detection")
    parser.add_argument("--version", action="store_true",
                        help="affiche la version")
    parser.add_argument("--aide", action="store_true",
                        help="affiche l aide complete")
    args = parser.parse_args()

    if args.version:
        print("detecter-processus-residuels %s (%s)" % (VERSION, STATUT))
        return 0
    if args.aide:
        print(__doc__)
        return 0

    residuels = analyser(verbose=args.verbose)
    total = len(residuels)

    print("=" * 60)
    print("DETECTION DES PROCESSUS RESIDUELS (PID)")
    print("=" * 60)
    if not residuels:
        print("AUCUN RESIDUEL : tous les processus python/node/bash actifs")
        print("sont legitimes (liste blanche) ou ne referencent pas le projet.")
        if args.rapport:
            _ecrire_rapport(args.rapport, residuels, total)
        return 0

    print("RESIDUELS DETECTES : %d processus" % total)
    print("-" * 60)
    for r in residuels:
        ligne = "PID %-7s | %-14s | %-8s | %s" % (
            str(r["pid"]), r["nom"][:14], r["justification"],
            formater_commande(r["commande"], args.detail))
        print(ligne)
    print("-" * 60)
    print("VERDICT : %d processus residuel(s) - utiliser le NETTOYEUR" % total)
    print("          (nettoyer-processus-residuels, exclusif Hygie) pour les")
    print("          terminer. La liste blanche (freebuff, unsloth) est")
    print("          protegee : jamais signalee, jamais tuee.")

    if args.rapport:
        _ecrire_rapport(args.rapport, residuels, total)
        print("Rapport ecrit : %s" % args.rapport)
    return 0


def _ecrire_rapport(chemin, residuels, total):
    racine = racine_projet()
    if not os.path.isabs(chemin):
        chemin = os.path.join(racine, chemin)
    lignes = []
    lignes.append("# Rapport detecter-processus-residuels")
    lignes.append("")
    lignes.append("- Version outil : %s (%s)" % (VERSION, STATUT))
    lignes.append("- Date : %s" % _date_courante())
    lignes.append("- Processus residuels : %d" % total)
    lignes.append("")
    if not residuels:
        lignes.append("AUCUN RESIDUEL : etat PROPRE.")
    else:
        lignes.append("| PID | Nom | Justification | Commande |")
        lignes.append("|---|---|---|---|")
        for r in residuels:
            cmd = (r["commande"] or "").replace("|", "/")
            if len(cmd) > 120:
                cmd = cmd[:120] + "..."
            lignes.append("| %s | %s | %s | %s |" % (
                r["pid"], r["nom"], r["justification"], cmd))
    try:
        with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lignes) + "\n")
    except (IOError, OSError) as exc:
        print("ERREUR : impossible d ecrire le rapport %s (%s)" % (chemin, exc))


def _date_courante():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    sys.exit(main())
