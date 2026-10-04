#!/usr/bin/env python3
# -*- coding: ascii -*-
# nettoyer-processus-residuels.py
#
# NETTOIE les processus residuels du workspace (demande utilisateur
# 2026-08-16) : terminer les processus python/node/bash orphelins ou
# referencant le projet, detectes par detecter-processus-residuels.
#
# EXCLUSIVITE (regle immuable, regles-groupes-agents.md) : le nettoyage est
# EXCLUSIF a hygie (seul hygie supprime). L outil appelle
# proteger-verrou-habilitation AVANT toute action : un agent non habilite est
# BLOQUE avec la commande d activation de hygie.
#
# SECURITES :
#   - Dry-run PAR DEFAUT : affiche ce qui SERAIT tue, ne tue rien
#   - --kill <pid,...> : ne tue QUE les pid listes (apres verification
#     qu ils existent encore et qu ils ne sont pas en liste blanche)
#   - --tous : tue tous les processus residuels detectes (jamais la liste
#     blanche freebuff/unsloth)
#   - --force : confirme sans relance (sinon une confirmation est demandee)
#   - La liste blanche (freebuff, unsloth) est PROTEGEE : toute tentative de
#     kill sur un pid blanc est refusee.
#
# Compatibilite :
#   - Windows (win32) : taskkill /PID <pid> /F
#   - Linux/macOS     : os.kill(pid, SIGKILL)
#
# Options :
#   --agent <nom>   Nom de l agent appelant (obligatoire, passe au verrou)
#   --kill <pids>   Pids a tuer (separes par des virgules)
#   --tous          Tuer tous les residuels detectes
#   --force         Confirmer sans relance
#   --verbose       Affiche les details
#   --version       Affiche la version
#   --aide          Affiche l aide complete
#
# Usage:
#   python3 nettoyer-processus-residuels.py --agent hygie --tous --force
#   python3 nettoyer-processus-residuels.py --agent hygie --kill 1234,5678
#
# Version : 0.1.1
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (nettoyer-).
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

LISTE_BLANCHE = (
    "freebuff",
    "unsloth",
    "codebuff",
)

MARQUEURS_PROJET = (
    "analyste-in-console",
    "tmp-",
    ".zz-",
    ".tmp-",
    "cerveau-projet/",
    "cerveau-projet\\",
)

VERROU = ("cerveau-projet", "agents", "tools", "proteger",
          "proteger-verrou-habilitation", "proteger-verrou-habilitation.py")
DETECTEUR = ("cerveau-projet", "agents", "tools", "detecter",
             "detecter-processus-residuels", "detecter-processus-residuels.py")


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def _chemin_outil(parts):
    return os.path.join(racine_projet(), *parts)


def verrouiller(agent):
    """Appelle le verrou d habilitation. Retourne (ok, message)."""
    try:
        out = subprocess.check_output(
            [sys.executable, _chemin_outil(VERROU),
             "--agent", agent, "--outil", "nettoyer-processus-residuels"],
            stderr=subprocess.STDOUT, timeout=30)
        return (True, out.decode("utf-8", errors="replace").strip())
    except subprocess.CalledProcessError as exc:
        msg = exc.output.decode("utf-8", errors="replace").strip()
        return (False, msg)
    except Exception as exc:
        return (False, "verrou inaccessible : %s" % exc)


def est_liste_blanche(nom, commande):
    champs = (nom or "").lower() + " " + (commande or "").lower()
    return any(m in champs for m in LISTE_BLANCHE)


def lister_processus_windows():
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
    if sys.platform == "win32":
        return lister_processus_windows()
    return lister_processus_posix()


def pid_existe(pid):
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


def lister_pids_vivants():
    """Ensemble de tous les PID vivants du systeme (pour detecter les
    orphelins : un processus dont le PPID est mort est un residuel)."""
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


def analyser_residuels():
    """Retourne les residuels actuels : processus dont le PARENT EST MORT
    (orphelins). Justification PROJET si la commande reference le projet,
    sinon ORPHELIN. Un processus au parent vivant est un processus actif
    legitime (ex : les autres tests du pool) - jamais un residuel."""
    processus = lister_processus()
    pids_vivants = lister_pids_vivants()
    residuels = []
    for p in processus:
        nom = p.get("nom", "") or ""
        commande = p.get("commande", "") or ""
        pid = p.get("pid")
        ppid = p.get("ppid")
        if est_liste_blanche(nom, commande):
            continue
        if ppid is not None and pid_existe(pid) and ppid not in pids_vivants:
            commande_bas = commande.lower()
            if any(m in commande_bas for m in MARQUEURS_PROJET):
                justif = "PROJET"
            else:
                justif = "ORPHELIN"
            residuels.append({
                "pid": pid,
                "ppid": ppid,
                "nom": nom,
                "commande": commande,
                "justification": justif,
            })
    return residuels


def tuer_pid(pid, nom, commande):
    """Tue un processus. Retourne (ok, message)."""
    if est_liste_blanche(nom, commande):
        return (False, "REFUSE : pid %s (%s) est en liste blanche (protege)" % (pid, nom))
    if not pid_existe(pid):
        return (False, "pid %s n existe plus (deja termine)" % pid)
    try:
        if sys.platform == "win32":
            subprocess.check_call(
                ["taskkill", "/PID", str(pid), "/F"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=15)
        else:
            os.kill(int(pid), 9)
        return (True, "pid %s (%s) termine" % (pid, nom))
    except subprocess.CalledProcessError:
        return (False, "echec taskkill sur pid %s" % pid)
    except Exception as exc:
        return (False, "echec kill pid %s : %s" % (pid, exc))


def _confirmer(texte):
    try:
        rep = input("%s [o/N] : " % texte).strip().lower()
        return rep in ("o", "oui", "y", "yes")
    except EOFError:
        return False


def main():
    parser = argparse.ArgumentParser(
        prog="nettoyer-processus-residuels",
        description="Nettoie les processus residuels du workspace (exclusif Hygie).")
    parser.add_argument("--version", action="store_true",
                        help="affiche la version")
    parser.add_argument("--aide", action="store_true",
                        help="affiche l aide complete")
    parser.add_argument("--agent", metavar="NOM", required=False,
                        help="nom de l agent appelant (verrou d habilitation)")
    parser.add_argument("--kill", metavar="PIDS",
                        help="pids a tuer (separes par des virgules)")
    parser.add_argument("--tous", action="store_true",
                        help="tue tous les residuels detectes")
    parser.add_argument("--force", action="store_true",
                        help="confirme sans relance")
    parser.add_argument("--verbose", action="store_true",
                        help="affiche les details")
    args = parser.parse_args()

    if args.version:
        print("nettoyer-processus-residuels %s (%s)" % (VERSION, STATUT))
        return 0
    if args.aide:
        print(__doc__)
        return 0

    # L agent est obligatoire SAUF pour --version/--aide (verifie apres).
    if not args.agent:
        print("ERREUR : --agent <nom> est obligatoire (verrou d habilitation).")
        print("Usage : python3 nettoyer-processus-residuels.py --agent <nom> [--tous|--kill <pids>]")
        return 2

    # 1. VERROU : exclusivite hygie AVANT toute action.
    ok, msg = verrouiller(args.agent)
    if not ok:
        print("BLOQUE : %s" % msg)
        return 1
    if args.verbose:
        print("[verrou] %s" % msg)

    # 2. Cibles.
    residuels = analyser_residuels()
    if args.kill:
        pids_demandes = [int(p.strip()) for p in args.kill.split(",") if p.strip()]
        cibles = [r for r in residuels if r["pid"] in pids_demandes]
        # Les pids demandes absents des residuels : verifier s ils existent
        # encore et ne sont pas en liste blanche (cas pid connu non detecte).
        for pid in pids_demandes:
            if pid in [r["pid"] for r in cibles]:
                continue
            proc = next((p for p in lister_processus() if p.get("pid") == pid), None)
            if proc:
                cibles.append({
                    "pid": pid,
                    "ppid": proc.get("ppid"),
                    "nom": proc.get("nom", ""),
                    "commande": proc.get("commande", "") or "",
                    "justification": "DEMANDE",
                })
    elif args.tous:
        cibles = residuels
    else:
        # Dry-run par defaut.
        print("=" * 60)
        print("DRY-RUN : rien n a ete tue (pas de --kill ni --tous)")
        print("=" * 60)
        if not residuels:
            print("AUCUN RESIDUEL detecte : etat PROPRE.")
            return 0
        print("Seraient termines (%d) :" % len(residuels))
        for r in residuels:
            print("  PID %-7s | %-14s | %s" % (
                str(r["pid"]), r["nom"][:14], r["justification"]))
        print("Utilisez : --kill <pid,...> pour cibler ou --tous pour tout.")
        return 0

    if not cibles:
        print("AUCUN processus a terminer (aucun residuel correspondant).")
        return 0

    print("=" * 60)
    print("NETTOYAGE DES PROCESSUS RESIDUELS (%d cible(s))" % len(cibles))
    print("=" * 60)
    for c in cibles:
        print("  PID %-7s | %-14s | %-8s | %s" % (
            str(c["pid"]), c["nom"][:14], c["justification"],
            (c["commande"] or "")[:80]))

    if not args.force and not _confirmer("Confirmer le nettoyage ?"):
        print("Annule (aucun processus tue).")
        return 0

    ok_count = 0
    ko_count = 0
    for c in cibles:
        ok, msg = tuer_pid(c["pid"], c["nom"], c["commande"])
        if ok:
            ok_count += 1
            print("  [OK] %s" % msg)
        else:
            ko_count += 1
            print("  [KO] %s" % msg)

    print("-" * 60)
    print("RESULTAT : %d termine(s), %d echec(s)." % (ok_count, ko_count))
    if ko_count:
        print("VERDICT : KO - certains processus n ont pas pu etre termines.")
        return 1
    print("VERDICT : OK - aucun processus residuel restant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
