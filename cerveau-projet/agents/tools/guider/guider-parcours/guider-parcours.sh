#!/bin/bash
# guider-parcours.sh
# Guide l'agent case par case (jeu de piste) : affiche la case courante
# (question + indices outil/fichier/regle), suit les branches selon la reponse.
# Version : 0.2.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# GUIDE-PARCOURS - OUTIL DE NAVIGATION EN CASES (version bash)
# ============================================================
# Parite avec guider-parcours.py : meme logique, python embarque
# par heredoc (convention du projet). Si python3 est disponible,
# la logique complete est executee par le bloc python ci-dessous.
# ============================================================
# REGLE IMMUABLE DE NOMMAGE : dossier 'guider/' -> prefixe 'guide-'
# ============================================================

VERSION="0.2.0"
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

VERSION = "0.2.0"
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
    for cid, case in cases.items():
        # Regle 10 (spec v0.2.10) : AUCUNE BOUCLE D'ATTENTE. Une case dont le
        # titre evoque l'attente (attendre/attente) ne doit JAMAIS avoir une
        # branche vers elle-meme : l'attente est une FIN, pas une boucle.
        titre = (case.get("titre", "") + " " + case.get("question", "")).lower()
        if "attendre" in titre or "attente" in titre:
            for b in case.get("branches") or []:
                if b.get("vers") == cid:
                    erreurs.append(
                        "case '%s': BOUCLE D'ATTENTE interdite (branche '%s' -> elle-meme). "
                        "L'attente est une case fin, pas une boucle (spec v0.2.10 regle 10)" % (cid, b.get("reponse"))
                    )
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

def naviguer(donnees, case_debut, reponses_predefinies, interactif=False):
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

        if interactif:
            try:
                rep = input("> ").strip()
            except EOFError:
                print("=== PARCOURS INTERROMPU (fin d'entree) ===")
                return 0
        elif reponses_predefinies is not None and idx_reponses < len(reponses_predefinies):
            rep = reponses_predefinies[idx_reponses].strip()
            idx_reponses += 1
        else:
            # Mode agent : la question est destinee a l'agent. Un agent vit
            # dans la console : il ne repond JAMAIS a une invite interactive.
            # Il repond selon son etat reel puis fournit sa reponse PAR LA
            # CONSOLE en relancant avec --reponses 'REPONSE'.
            print("")
            print("=== QUESTION POUR L'AGENT ===")
            print("Tu es un AGENT, tu vis dans la console : tu n'es pas un humain,")
            print("tu ne reponds a aucune invite interactive. Reponds a la question")
            print("ci-dessus selon ton etat reel, puis fournis ta reponse PAR LA CONSOLE")
            print("en relancant DEPUIS CETTE CASE (pour ne pas rejouer c0) :")
            print("  guider-parcours <parcours.json> --case %s --reponses 'REPONSE'" % cid)
            if branches:
                print("Reponses possibles : %s" % " / ".join(b.get("reponse", "?") for b in branches))
            print("")
            return 0

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
    interactif = False
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
        elif a == "--interactif":
            interactif = True
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
            print("  --reponses <liste>  Reponses fournies d'un coup, separees par | (mode agent)")
            print("  --interactif        Mode interactif (input clavier) pour usage humain")
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
    return naviguer(donnees, case_debut, reponses, interactif)

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
