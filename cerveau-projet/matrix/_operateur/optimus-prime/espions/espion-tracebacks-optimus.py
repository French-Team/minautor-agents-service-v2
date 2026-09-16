#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
espion-tracebacks-optimus.py -- Detecteur de traceback/fatal errors dans les outils Optimus.

Deux modes :
  1. SCAN STATIQUE : analyse les fichiers .py pour patterns dangereux
     (bare except, os.exit, sys.exit non garde, variables non initialisees, etc.)
  2. RUN DYNAMIQUE : execute chaque outil avec args minimaux, capte stderr
     pour traceback/exception/Error/Warning.

Usage:
  python espion-tracebacks-optimus.py scan     (scan statique)
  python espion-tracebacks-optimus.py run      (run dynamique)
  python espion-tracebacks-optimus.py tour     (scan + run)
  python espion-tracebacks-optimus.py rapport  (dernier rapport)

Code retour : 0 = RAS, 1 = au moins 1 signal, 2 = erreur espion.
L espion SIGNALE, il ne repare jamais.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
RACINE_MATRIX = next(p for p in [BASE, *BASE.parents] if p.name == "matrix")
DATA = RACINE_MATRIX / "matrice" / "data"
OPERATEUR = RACINE_MATRIX / "_operateur" / "optimus-prime"

# Repertoires a scanner
OUTILS_DIRS = [
    DATA / "outils",
]
ESPIONS_DIR = OPERATEUR / "espions"
REMORQUE_DIR = OPERATEUR / "remorque"

# Patterns dangereux (scan statique)
PATTERNS_STATIQUES = [
    {"nom": "bare-except", "regex": r"except\s*:", "severite": "haute", "desc": "except sans type = attrape tout y compris KeyboardInterrupt/SystemExit"},
    {"nom": "except-all", "regex": r"except\s+Exception\s*:", "severite": "moyenne", "desc": "except Exception trop large"},
    {"nom": "os-exit", "regex": r"os\._exit\(|os\.exit\(", "severite": "haute", "desc": "os.exit() dans un outil = arret brutal"},
    {"nom": "sys-exit", "regex": r"sys\.exit\(", "severite": "moyenne", "desc": "sys.exit() dans un outil = peut interrompre le pilote"},
    {"nom": "eval", "regex": r"\beval\s*\(", "severite": "haute", "desc": "eval() = risque d'injection de code"},
    {"nom": "exec", "regex": r"\bexec\s*\(", "severite": "haute", "desc": "exec() = risque d'injection de code"},
    {"nom": "hardcoded-path", "regex": r'["\'][A-Z]:\\', "severite": "basse", "desc": "Chemin Windows hardcode"},
    {"nom": "print-to-stderr", "regex": r"print\(.*file\s*=\s*sys\.stderr", "severite": "info", "desc": "Print vers stderr (peut polluer les sorties)"},
    {"nom": "global-variable", "regex": r"^global\s+", "severite": "basse", "desc": "Declaration global = fragilise la modularite"},
    {"nom": "todo-fixme", "regex": r"#\s*(TODO|FIXME|HACK|XXX)\b", "severite": "info", "desc": "Marqueur TODO/FIXME non resolu"},
]

# Patterns dynamiques (run)
PATTERNS_DYNAMIQUES = [
    {"nom": "traceback", "regex": r"Traceback \(most recent call last\)", "severite": "critique", "desc": "Python traceback dans stderr"},
    {"nom": "exception", "regex": r"^\w+Error:|^\w+Exception:", "severite": "critique", "desc": "Exception non Interceptee"},
    {"nom": "error-message", "regex": r"(?i)\berror\b(?!.*#.*noqa)", "severite": "moyenne", "desc": "Message contenant 'error' (hors commentaires)"},
    {"nom": "warning", "regex": r"(?i)\bwarning\b", "severite": "basse", "desc": "Warning detecte"},
    {"nom": "permission-denied", "regex": r"(?i)permission denied|access denied", "severite": "haute", "desc": "Permission refused"},
    {"nom": "file-not-found", "regex": r"(?i)no such file|file not found|not a directory", "severite": "moyenne", "desc": "Fichier/dossier introuvable"},
    {"nom": "unicode-decode", "regex": r"(?i)unicode.*decode.*error|encoding.*error", "severite": "moyenne", "desc": "Erreur encodage Unicode"},
    {"nom": "timeout", "regex": r"(?i)timeout|timed out", "severite": "moyenne", "desc": "Timeout detecte"},
]


def _jsonl_read(chemin):
    """Lit un fichier JSONL, retourne liste de dicts."""
    if not chemin.is_file():
        return []
    resultats = []
    for ligne in chemin.read_text(encoding="utf-8", errors="replace").splitlines():
        ligne = ligne.strip()
        if ligne:
            try:
                resultats.append(json.loads(ligne))
            except json.JSONDecodeError:
                continue
    return resultats


def _jsonl_append(chemin, entree):
    """Append une ligne JSONL."""
    with open(chemin, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")


# --- SCAN STATIQUE ---

def _est_faux_positif(ligne, nom_pattern):
    """Detecte les faux positifs (definitions de patterns, strings, docstrings)."""
    stripped = ligne.strip()
    # Commentaires et docstrings
    if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
        return True
    # Strings de pattern (contient 'regex' ou 'severite' = c'est une definition)
    if nom_pattern in ("bare-except", "except-all", "sys-exit", "eval", "exec", "os-exit"):
        if "regex" in stripped or "severite" in stripped or "nom" in stripped:
            return True
    # sys.exit dans if __name__ == "__main__" = pattern standard
    if nom_pattern == "sys-exit":
        if "__main__" in stripped or stripped.startswith("if __name__"):
            return True
        # sys.exit(main()) ou sys.exit(envelopper(...)) = pattern entree standard
        if stripped.startswith("sys.exit("):
            if "main" in stripped or "envelopper" in stripped or "principal" in stripped:
                return True
    return False


def scanner_fichier(chemin):
    """Scan un fichier .py pour patterns dangereux.
    Retourne liste de {"ligne": int, "pattern": str, "severite": str, "texte": str, "desc": str}.
    """
    signaux = []
    try:
        texte = chemin.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return signaux

    for i, ligne in enumerate(texte.splitlines(), 1):
        for pat in PATTERNS_STATIQUES:
            if re.search(pat["regex"], ligne):
                stripped = ligne.strip()
                if _est_faux_positif(ligne, pat["nom"]):
                    continue
                signaux.append({
                    "ligne": i,
                    "pattern": pat["nom"],
                    "severite": pat["severite"],
                    "texte": stripped[:120],
                    "desc": pat["desc"],
                })
    return signaux


def scan_statique():
    """Scan tous les .py des outils Optimus.
    Retourne (signaux_par_fichier, nb_total, nb_fichiers).
    """
    resultats = {}
    nb_total = 0

    # Collecte tous les .py
    fichiers = []
    for d in OUTILS_DIRS:
        if d.is_dir():
            for p in d.rglob("*.py"):
                if "__pycache__" not in p.parts:
                    fichiers.append(p)
    for d in [ESPIONS_DIR, REMORQUE_DIR]:
        if d.is_dir():
            for p in d.glob("*.py"):
                fichiers.append(p)

    for fp in fichiers:
        # Exclure l espion lui-meme
        if fp.name == Path(__file__).name:
            continue
        signaux = scanner_fichier(fp)
        if signaux:
            rel = str(fp.relative_to(RACINE_MATRIX.parent.parent)) if fp.is_relative_to(RACINE_MATRIX.parent.parent) else str(fp)
            resultats[rel] = signaux
            nb_total += len(signaux)

    return resultats, nb_total, len(fichiers)


# --- RUN DYNAMIQUE ---

def run_outil(chemin_outil):
    """Execute un outil avec args minimaux, capte stderr.
    Retourne (signaux, stdout, stderr, code, duree_ms).
    """
    signaux = []

    # Determine l'arg pour aider
    args = [sys.executable, str(chemin_outil)]
    # Ajoute --help si main.py
    if chemin_outil.name == "main.py":
        args.append("--help")

    try:
        debut = time.time()
        result = subprocess.run(
            args,
            capture_output=True,
            timeout=15,
            cwd=str(RACINE_MATRIX.parent.parent),
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        duree_ms = int((time.time() - debut) * 1000)
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")
        code = result.returncode

        # Cherche les patterns dans stderr UNIQUEMENT
        # (stdout = aide/utilisation, pas d'erreur reelle)
        for pat in PATTERNS_DYNAMIQUES:
            for match in re.finditer(pat["regex"], stderr, re.MULTILINE):
                debut_ligne = stderr.rfind("\n", 0, match.start()) + 1
                fin_ligne = stderr.find("\n", match.end())
                if fin_ligne == -1:
                    fin_ligne = len(stderr)
                contexte = stderr[debut_ligne:fin_ligne].strip()[:200]

                signaux.append({
                    "pattern": pat["nom"],
                    "severite": pat["severite"],
                    "canal": "stderr",
                    "contexte": contexte,
                    "desc": pat["desc"],
                    "code": code,
                })

        return signaux, stdout, stderr, code, duree_ms

    except subprocess.TimeoutExpired:
        return [{"pattern": "timeout-exec", "severite": "haute", "canal": "systeme", "contexte": "Timeout 15s", "desc": "Out of time", "code": -1}], "", "TIMEOUT", -1, 15000
    except Exception as e:
        return [{"pattern": "run-error", "severite": "critique", "canal": "systeme", "contexte": str(e)[:200], "desc": "Erreur execution", "code": -1}], "", str(e), -1, 0


def run_dynamique():
    """Execute tous les outils main.py et capte les erreurs.
    Retourne (resultats, nb_signaux, nb_outils).
    """
    resultats = {}
    nb_signaux = 0
    nb_outils = 0

    for d in OUTILS_DIRS:
        if not d.is_dir():
            continue
        for outil_dir in sorted(d.iterdir()):
            if not outil_dir.is_dir():
                continue
            main = outil_dir / "main.py"
            if not main.is_file():
                continue
            nb_outils += 1
            signaux, stdout, stderr, code, duree_ms = run_outil(main)
            if signaux:
                resultats[str(outil_dir.relative_to(RACINE_MATRIX.parent.parent))] = {
                    "signaux": signaux,
                    "code": code,
                    "duree_ms": duree_ms,
                    "stderr_preview": stderr[:500] if stderr else "",
                }
                nb_signaux += len(signaux)

    return resultats, nb_signaux, nb_outils


# --- RAPPORT ---

def generer_rapport(scan_resultats, run_resultats, nb_scan_fichiers, nb_run_outils, nb_scan_signaux, nb_run_signaux):
    """Genere le rapport markdown."""
    lignes = []
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    lignes.append(f"---\nidentite:\n  type: rapport-tracebacks\n  date: {ts}\n---\n")
    lignes.append(f"# RAPPORT TRACEBACKS OPTIMUS -- {ts}\n")
    lignes.append(f"## Resume\n")
    lignes.append(f"- Scan statique : {nb_scan_signaux} signaux sur {nb_scan_fichiers} fichiers")
    lignes.append(f"- Run dynamique : {nb_run_signaux} signaux sur {nb_run_outils} outils")
    lignes.append(f"- Total : {nb_scan_signaux + nb_run_signaux} signaux")
    lignes.append("")

    if nb_scan_signaux + nb_run_signaux == 0:
        lignes.append("**RAS** : aucun signal detecte.\n")
    else:
        # Scan statique
        if scan_resultats:
            lignes.append("## Scan Statique (patterns dans le code)\n")
            for fichier, signaux in sorted(scan_resultats.items()):
                lignes.append(f"### {fichier}\n")
                for s in signaux:
                    icon = {"critique": "[!!!]", "haute": "[!!]", "moyenne": "[!]", "basse": "[.]", "info": "[-]"}.get(s["severite"], "[-]")
                    lignes.append(f"- {icon} **{s['pattern']}** (L{s['ligne']}) [{s['severite']}] : `{s['texte'][:80]}`")
                    lignes.append(f"  - {s['desc']}")
                lignes.append("")

        # Run dynamique
        if run_resultats:
            lignes.append("## Run Dynamique (erreurs a l'execution)\n")
            for outil, info in sorted(run_resultats.items()):
                lignes.append(f"### {outil} (code={info['code']}, {info['duree_ms']}ms)\n")
                for s in info["signaux"]:
                    icon = {"critique": "[!!!]", "haute": "[!!]", "moyenne": "[!]", "basse": "[.]", "info": "[-]"}.get(s["severite"], "[-]")
                    lignes.append(f"- {icon} **{s['pattern']}** [{s['severite']}] ({s['canal']}) : `{s['contexte'][:100]}`")
                    lignes.append(f"  - {s['desc']}")
                if info.get("stderr_preview"):
                    lignes.append(f"- Stderr preview : `{info['stderr_preview'][:200]}`")
                lignes.append("")

    return "\n".join(lignes)


# --- MAIN ---

def main():
    """Point d'entree."""
    args = sys.argv[1:]
    mode = args[0] if args else "tour"

    if mode in ("--help", "-h", "help"):
        print(__doc__)
        return 0

    # Journal historique
    historique = OPERATEUR / "espions" / "registre" / "tracebacks-historique.jsonl"

    if mode == "rapport":
        if historique.is_file():
            dernier = _jsonl_read(historique)
            if dernier:
                rapport = dernier[-1].get("rapport", "Aucun rapport")
                # Force UTF-8 pour emojis
                try:
                    sys.stdout.buffer.write(rapport.encode("utf-8"))
                    sys.stdout.buffer.write(b"\n")
                except (AttributeError, OSError):
                    print(rapport)
            else:
                print("Aucun historique")
        else:
            print("Aucun historique")
        return 0

    # Tour : scan + run
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"=== TRACEBACKS OPTIMUS -- {ts} ===\n")

    # Scan statique
    print("--- SCAN STATIQUE ---")
    scan_resultats, nb_scan_signaux, nb_scan_fichiers = scan_statique()
    print(f"Fichiers scannes : {nb_scan_fichiers}")
    print(f"Signaux : {nb_scan_signaux}")
    if scan_resultats:
        for f, signaux in sorted(scan_resultats.items()):
            print(f"  {f} : {len(signaux)} signaux")
    print("")

    # Run dynamique (seulement en mode run ou tour)
    run_resultats = {}
    nb_run_signaux = 0
    nb_run_outils = 0
    if mode in ("run", "tour"):
        print("--- RUN DYNAMIQUE ---")
        run_resultats, nb_run_signaux, nb_run_outils = run_dynamique()
        print(f"Outils executes : {nb_run_outils}")
        print(f"Signaux : {nb_run_signaux}")
        if run_resultats:
            for f, info in sorted(run_resultats.items()):
                print(f"  {f} : {len(info['signaux'])} signaux (code={info['code']})")
        print("")

    # Bilan
    total = nb_scan_signaux + nb_run_signaux
    print(f"=== BILAN : {total} signaux ===")
    if total == 0:
        print("RAS : aucun signal detecte.")
    else:
        # Compte par severite
        compteurs = {}
        for signaux in scan_resultats.values():
            for s in signaux:
                compteurs[s["severite"]] = compteurs.get(s["severite"], 0) + 1
        for info in run_resultats.values():
            for s in info["signaux"]:
                compteurs[s["severite"]] = compteurs.get(s["severite"], 0) + 1
        for sev in ["critique", "haute", "moyenne", "basse", "info"]:
            if sev in compteurs:
                print(f"  {sev} : {compteurs[sev]}")

    # Journal
    rapport = generer_rapport(scan_resultats, run_resultats, nb_scan_fichiers, nb_run_outils, nb_scan_signaux, nb_run_signaux)
    _jsonl_append(historique, {
        "date": ts,
        "scan_signaux": nb_scan_signaux,
        "run_signaux": nb_run_signaux,
        "total": total,
        "rapport": rapport,
    })

    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
