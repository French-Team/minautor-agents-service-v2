#!/bin/bash
# guider-parcours.sh
# Guide l'agent case par case (jeu de piste) : affiche la case courante
# (question + indices outil/fichier/regle), suit les branches selon la reponse.
# Version : 0.1.0
# Statut : ebauche

# ============================================================
# GUIDE-PARCOURS - OUTIL DE NAVIGATION EN CASES (version bash)
# ============================================================
# Parite avec guider-parcours.py : meme logique, python embarque
# par heredoc (convention du projet). Si python3 est disponible,
# la logique complete est executee par le bloc python ci-dessous.
# ============================================================
# REGLE IMMUABLE DE NOMMAGE : dossier 'guider/' -> prefixe 'guide-'
# ============================================================

VERSION="0.1.0"
STATUT="ebauche"

# Verifier le nommage (regle immuable)
verifier_nommage() {
    local script_nom=$(basename "$0" | sed 's/\.sh$//')
    [[ "$script_nom" == "outil-template" ]] && return 0
    local chemin_script=$(cd "$(dirname "$0")" 2>/dev/null && pwd)
    local categorie=$(basename "$(dirname "$chemin_script")")
    if [[ -z "$categorie" || "$categorie" == "." || "$categorie" == "/" ]]; then
        return 0
    fi
    if [[ "$script_nom" != "${categorie}-"* ]]; then
        echo "[ERREUR] Nommage invalide : $script_nom"
        echo "  Le nom doit commencer par '${categorie}-' (categorie: ${categorie}/)"
        exit 1
    fi
}

# Executer la logique python (parite avec le .py)
executer_python() {
    python3 - "$@" << 'PYEOF'
import argparse
import json
import sys
from pathlib import Path

VERSION = "0.1.0"
STATUT = "ebauche"

def charger_parcours(chemin):
    p = Path(chemin)
    if not p.is_file():
        print("ERREUR: Fichier de parcours introuvable: %s" % chemin, file=sys.stderr)
        sys.exit(1)
    try:
        with p.open(encoding="utf-8") as fh:
            donnees = json.load(fh)
    except json.JSONDecodeError as exc:
        print("ERREUR: JSON invalide dans %s: %s" % (chemin, exc), file=sys.stderr)
        sys.exit(1)
    if "parcours" not in donnees or "cases" not in donnees:
        print("ERREUR: Le parcours doit contenir 'parcours' et 'cases'", file=sys.stderr)
        sys.exit(1)
    return donnees

def valider_parcours(donnees):
    meta = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    depart = meta.get("case_depart")
    erreurs = []
    if not depart:
        erreurs.append("case_depart manquant dans parcours")
    elif depart not in cases:
        erreurs.append("case_depart '%s' introuvable dans cases" % depart)
    for cid, case in cases.items():
        suivant = case.get("suivant")
        branches = case.get("branches")
        if suivant and suivant not in cases:
            erreurs.append("case '%s': suivant '%s' introuvable" % (cid, suivant))
        for b in branches or []:
            vers = b.get("vers")
            if vers and vers not in cases:
                erreurs.append("case '%s': branche vers '%s' introuvable" % (cid, vers))
    if erreurs:
        for e in erreurs:
            print("ERREUR: " + e, file=sys.stderr)
        sys.exit(1)
    return True

def lister_cases(donnees):
    meta = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    print("=== Parcours %s v%s ===" % (meta.get("nom", "?"), meta.get("version", "?")))
    print("Agent : %s | Depart : %s" % (meta.get("agent", "?"), meta.get("case_depart", "?")))
    print("")
    for cid, case in cases.items():
        print("  [%s] %-8s %s" % (cid, case.get("type", "?"), case.get("titre", "")))
    return 0

def afficher_indices(indices):
    if not indices:
        return
    print("")
    for ind in indices:
        typ = ind.get("type", "")
        if typ == "regle":
            print("[REGLE] " + ind.get("texte", ""))
        elif typ == "outil":
            nom = ind.get("nom", "?")
            chemin = ind.get("chemin", "")
            print("[OUTIL] %s" % nom)
            if chemin:
                print("         chemin: %s" % chemin)
            if ind.get("commande"):
                print("         > " + ind.get("commande"))
        elif typ == "fichier":
            print("[FICHIER] " + ind.get("chemin", "?"))
            if ind.get("raison"):
                print("         raison: %s" % ind.get("raison"))
        else:
            print("[INDICE] " + str(ind.get("texte", "")))

def afficher_case(cid, case, total, position):
    print("")
    print("=== [%s/%s] %s ===" % (position, total, case.get("titre", cid)))
    afficher_indices(case.get("indices"))
    question = case.get("question")
    branches = case.get("branches") or []
    if question:
        print("")
        print("QUESTION : %s" % question)
    for i, b in enumerate(branches, 1):
        print("  [%d] %s" % (i, b.get("reponse", "?")))
    print("")

def reponse_exacte(branches, reponse):
    rep = reponse.strip()
    if rep.isdigit():
        idx = int(rep) - 1
        if 0 <= idx < len(branches):
            return branches[idx]
        return None
    for b in branches:
        if b.get("reponse", "").strip().lower() == rep.lower():
            return b
    return None

def naviguer(donnees, case_debut, reponses_predefinies):
    meta = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    cid = case_debut
    idx_reponses = 0
    ordre = list(cases.keys())
    total = len(cases)

    while True:
        case = cases[cid]
        typ = case.get("type", "question")
        if typ == "fin":
            print("=== PARCOURS TERMINE ===")
            print("Fin de parcours atteinte : case '%s' (%s)" % (cid, case.get("titre", "")))
            if case.get("message"):
                print(case.get("message"))
            return 0

        position = ordre.index(cid) + 1
        afficher_case(cid, case, total, position)

        branches = case.get("branches") or []
        if typ == "indice":
            suivant = case.get("suivant")
            if not suivant:
                print("ERREUR: case indice '%s' sans 'suivant'" % cid, file=sys.stderr)
                return 1
            cid = suivant
            continue

        if reponses_predefinies is not None:
            if idx_reponses >= len(reponses_predefinies):
                print("ERREUR: plus de reponses fournies que de questions (case '%s')" % cid, file=sys.stderr)
                return 1
            rep = reponses_predefinies[idx_reponses].strip()
            idx_reponses += 1
            if rep == "":
                rep = input("> ").strip()
        else:
            try:
                rep = input("> ").strip()
            except EOFError:
                print("ERREUR: aucune reponse fournie (fin d'entree)", file=sys.stderr)
                return 1

        if not branches:
            suivant = case.get("suivant")
            if not suivant:
                print("=== PARCOURS TERMINE ===")
                return 0
            cid = suivant
        else:
            b = reponse_exacte(branches, rep)
            if b is None:
                print("REPONSE INCONNUE: '%s'. Reponses possibles : %s" % (
                    rep, " / ".join(br.get("reponse", "?") for br in branches)))
                if reponses_predefinies is not None:
                    return 1
                continue
            cid = b.get("vers")

def main():
    args = sys.argv[1:]
    parcours = None
    case_debut = None
    reponses = None
    liste = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--case":
            i += 1
            if i >= len(args):
                print("ERREUR: --case attend un argument", file=sys.stderr)
                return 1
            case_debut = args[i]
        elif a == "--reponses":
            i += 1
            if i >= len(args):
                print("ERREUR: --reponses attend un argument", file=sys.stderr)
                return 1
            reponses = [r.strip() for r in args[i].split("|")]
        elif a == "--liste":
            liste = True
        elif a == "--version":
            print("guider-parcours v%s" % VERSION)
            return 0
        elif a == "--help" or a == "-h":
            print("=== guider-parcours v%s ===" % VERSION)
            print("Usage: guider-parcours.sh <parcours.json> [options]")
            print("Options :")
            print("  --case <id>         Case de depart (ex: c3)")
            print("  --reponses <liste>  Reponses fournies d'un coup, separees par |")
            print("  --liste             Lister les cases sans naviguer")
            print("  --version           Afficher la version")
            return 0
        else:
            parcours = a
        i += 1

    if not parcours:
        print("ERREUR: chemin du parcours JSON obligatoire", file=sys.stderr)
        return 1

    donnees = charger_parcours(parcours)
    valider_parcours(donnees)
    if liste:
        return lister_cases(donnees)
    meta = donnees.get("parcours", {})
    case_debut = case_debut or meta.get("case_depart")
    return naviguer(donnees, case_debut, reponses)

if __name__ == "__main__":
    sys.exit(main())
PYEOF
}

# Main
main() {
    verifier_nommage
    if ! command -v python3 >/dev/null 2>&1; then
        echo "[ERREUR] python3 est requis pour guider-parcours.sh (parite avec le .py)"
        exit 1
    fi
    executer_python "$@"
}

main "$@"
