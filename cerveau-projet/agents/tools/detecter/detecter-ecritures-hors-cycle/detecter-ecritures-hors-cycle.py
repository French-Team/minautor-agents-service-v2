#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-ecritures-hors-cycle.py
#
# GARDE-FOU ANTI-DERIVE : detecte les ecritures de fichiers de travail qui
# echappent au cycle d activation (Cerberus -> agent -> Cerberus).
#
# Invariant cible : toute ecriture d un fichier de travail (code, outil, carte,
# fiche) doit etre couverte par une activation d agent dans AGENTS-historique.md.
# Cerberus (coordination) n ecrit JAMAIS de fichier de travail : il n ecrit que
# AGENTS.md / AGENTS-historique.md. Si des fichiers de travail ont ete modifies
# APRES la derniere activation alors que l agent actif est Cerberus, c est une
# derive (travail en solo).
#
# Detection combinee (decision utilisateur) :
#   1. PRIMAIRE : git status --porcelain + git diff --name-only HEAD
#   2. SECOURS  : si git indisponible, marche des fichiers du projet et garde
#                 ceux dont mtime > dernier horodatage d activation
#
# Exclusions (jamais des ecritures de travail) :
#   .git/, workspace/, tmp-*/.tmp-*/.zz-*, __pycache__/, traces/,
#   AGENTS.md, AGENTS-historique.md, + chemins couverts par .tmpignore.
#
# Options :
#   --depuis <horodatage> : remplacer la lecture auto du dernier horodatage
#                           d activation (format YYYY-MM-DD HH:MM)
#   --agent <nom>         : forcer l agent actif (defaut : lu dans AGENTS.md)
#   --rapport <fichier>   : ecrire le rapport markdown
#   --verbose             : detail par fichier (preuve git/mtime)
#   --version             : version
#   --aide                : aide (alias de -h)
#
# Usage:
#   python3 detecter-ecritures-hors-cycle.py
#   python3 detecter-ecritures-hors-cycle.py --rapport ecarts-hors-cycle.md
#   python3 detecter-ecritures-hors-cycle.py --depuis "2026-08-17 19:47"
#
# Version : 0.1.0
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
import os
import re
import subprocess
import sys
from datetime import datetime

VERSION = "0.1.0"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}

# Fichiers/chemins EXCLUS de la detection (coordination, traces, temporaire).
NOMS_EXCLUS = {"AGENTS.md", "AGENTS-historique.md", ".tmpignore"}
PREFIXES_EXCLUS = ("tmp-", ".tmp-", ".zz-", ".git", "__pycache__")
# Coordination/stockage (ecrits par les outils de coordination, jamais des
# fichiers de travail) : workspace, classeur-variables, traces (registres).
DOSSIERS_EXCLUS = ("workspace", "classeur-variables", "traces")


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def chemin_historique(racine):
    return os.path.join(racine, "AGENTS-historique.md")


def chemin_agents(racine):
    return os.path.join(racine, "AGENTS.md")


def lire_tmpignore(racine):
    """Chemins a ignorer depuis .tmpignore (une ligne = un prefixe/chemin)."""
    cible = os.path.join(racine, ".tmpignore")
    if not os.path.isfile(cible):
        return []
    motifs = []
    with io.open(cible, encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#"):
                motifs.append(ligne.rstrip("/"))
    return motifs


def dernier_horodatage(racine):
    """Retourne (horodatage str, agent) de la DERNIERE activation lue dans
    AGENTS-historique.md. Le fichier est en ordre decroissant (le plus recent
    en premier) : la premiere ligne qui matche le format est la derniere
    activation."""
    chemin = chemin_historique(racine)
    if not os.path.isfile(chemin):
        return None, "inconnu"
    pattern = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*\|\s*\S+\s*\|\s*(\S+)\s*\|")
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            m = pattern.match(ligne)
            if m:
                return m.group(1), m.group(2)
    return None, "inconnu"


def agent_actif(racine):
    """Lit l agent actif (Nom Agent) de la session session-llm-1 dans AGENTS.md."""
    chemin = chemin_agents(racine)
    if not os.path.isfile(chemin):
        return "inconnu"
    txt = io.open(chemin, encoding="utf-8", errors="replace").read()
    bloc = txt.split("### Session : session-llm-1", 1)
    if len(bloc) < 2:
        return "inconnu"
    segment = bloc[1].split("\n---", 1)[0]
    for ligne in segment.splitlines():
        if "Nom Agent" in ligne and "|" in ligne:
            val = ligne.split("|")[2].strip().lower()
            return val or "inconnu"
    return "inconnu"


def est_exclu(rel, motifs_tmpignore):
    """Vrai si le chemin relatif est une coordination/trace/temporaire a ignorer."""
    rel_norm = rel.replace("\\", "/")
    parts = [p for p in rel_norm.split("/") if p]
    if not parts:
        return True
    base = parts[-1]
    if base in NOMS_EXCLUS:
        return True
    for part in parts:
        low = part.lower()
        if low.startswith(PREFIXES_EXCLUS):
            return True
        if low in DOSSIERS_EXCLUS:
            return True
    for motif in motifs_tmpignore:
        if rel_norm.startswith(motif.replace("\\", "/")) or parts[0] == motif:
            return True
    return False


def fichiers_git(racine):
    """PRIMAIRE : fichiers modifies selon git (status + diff). Retourne un set
    de chemins relatifs, ou None si git est indisponible."""
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain", "-uall"],
            cwd=racine, capture_output=True, text=True, timeout=60)
        r2 = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=racine, capture_output=True, text=True, timeout=60)
    except Exception:
        return None
    trouves = set()
    for ligne in (r.stdout or "").splitlines():
        # format XY path : X/Y = statut (M/A/D/??/R), puis le chemin
        if not ligne.strip():
            continue
        chemin = ligne[3:].strip()
        # un renommage git se note "old -> new" : prendre la cible
        if " -> " in chemin:
            chemin = chemin.split(" -> ")[-1]
        if chemin:
            trouves.add(chemin.replace("\\", "/"))
    for ligne in (r2.stdout or "").splitlines():
        if ligne.strip():
            trouves.add(ligne.strip().replace("\\", "/"))
    return trouves


def fichiers_mtime(racine, horodatage):
    """SECOURS : fichiers dont le mtime est POSTERIEUR a horodatage (str
    YYYY-MM-DD HH:MM)."""
    try:
        seuil = datetime.strptime(horodatage, "%Y-%m-%d %H:%M").timestamp()
    except (ValueError, TypeError):
        return set()
    trouves = set()
    for racine_dir, dossiers, fichiers in os.walk(racine):
        dossiers[:] = [d for d in dossiers
                       if d.lower() not in DOSSIERS_EXCLUS
                       and not d.lower().startswith(PREFIXES_EXCLUS)]
        for f in fichiers:
            chemin = os.path.join(racine_dir, f)
            try:
                if os.path.getmtime(chemin) > seuil:
                    trouves.add(os.path.relpath(chemin, racine).replace("\\", "/"))
            except OSError:
                continue
    return trouves


def main():
    parser = argparse.ArgumentParser(
        description="Detecte les ecritures de fichiers de travail hors cycle d activation")
    parser.add_argument("--depuis", type=str, default="",
                        help="Horodatage de reference (YYYY-MM-DD HH:MM) - defaut : derniere activation")
    parser.add_argument("--agent", type=str, default="",
                        help="Forcer l agent actif (defaut : lu dans AGENTS.md)")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true", help="Detail par fichier")
    parser.add_argument("--version", action="version",
                        version="detecter-ecritures-hors-cycle v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                        help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = racine_projet()
    horodatage, agent_dernier = dernier_horodatage(racine)
    agent = (args.agent or agent_actif(racine)).lower()
    if args.depuis:
        horodatage = args.depuis

    motifs_tmpignore = lire_tmpignore(racine)

    git_ok = True
    modifies = fichiers_git(racine)
    if modifies is None:
        git_ok = False
        modifies = fichiers_mtime(racine, horodatage)

    hors_cycle = []
    for chemin in sorted(modifies):
        if est_exclu(chemin, motifs_tmpignore):
            continue
        # Preuve : git (primaire) ou mtime (secours si git absent).
        preuve = "git" if git_ok else "mtime"
        hors_cycle.append((chemin, preuve))

    print(_couleur("=== Detecter les ecritures hors cycle d activation ===", "bleu"))
    print("  Derniere activation : %s (%s)" % (horodatage or "inconnue", agent_dernier))
    print("  Agent actif          : %s" % agent)
    print("  Source de preuve     : %s" % ("git" if git_ok else "mtime (git indisponible)"))
    print("")
    print("  Fichiers de travail modifies : %d" % len(hors_cycle))

    cerberus_actif = agent == "cerberus"
    for chemin, preuve in hors_cycle:
        print("  - %s [%s]" % (chemin, preuve))
        if args.verbose:
            print("      (preuve %s)" % preuve)

    ecart = len(hors_cycle)
    if ecart == 0:
        verdict = "OK"
        couleur = "vert"
    elif cerberus_actif:
        verdict = "KO : %d ecriture(s) hors cycle (agent actif Cerberus)" % ecart
        couleur = "rouge"
    else:
        verdict = "ATTENTION : %d fichier(s) modifies apres activation (agent de travail actif)" % ecart
        couleur = "jaune"

    print("")
    print(_couleur("  Verdict : %s" % verdict, couleur))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport : ecritures hors cycle d activation\n\n")
            fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("- Derniere activation : %s (%s)\n" % (horodatage or "inconnue", agent_dernier))
            fh.write("- Agent actif : %s\n" % agent)
            fh.write("- Source : %s\n" % ("git" if git_ok else "mtime"))
            fh.write("- Verdict : %s\n\n" % verdict)
            if hors_cycle:
                fh.write("## Fichiers de travail modifies\n\n")
                for chemin, preuve in hors_cycle:
                    fh.write("- %s [%s]\n" % (chemin, preuve))
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))

    # Code de sortie : 1 uniquement en cas de derive averee (Cerberus actif).
    return 1 if (ecart and cerberus_actif) else 0


if __name__ == "__main__":
    sys.exit(main())
