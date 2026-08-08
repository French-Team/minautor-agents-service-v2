#!/bin/bash
# combos-moteur.sh
# Moteur generique de combos declaratifs (definition-combo.json) : version bash.
# Version : 0.1.0-beta
# Statut : ebauche

# ============================================================
# COMBO-ORCHESTRATEUR (spec-combos-moteur v0.1.0) - version bash
# ============================================================
# Parite avec combos-moteur.py : meme logique, python embarque
# par heredoc (convention du projet). Le bash verifie le nommage
# puis la logique complete est executee par le bloc python.
# ============================================================
# REGLE IMMUABLE DE NOMMAGE : dossier 'combos/' -> prefixe 'combos-'
# ============================================================

VERSION="0.1.0-beta"
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
    export COMBO_MOTEUR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    python3 - "$@" << 'PYEOF'
import argparse
import datetime
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

VERSION = "0.1.0-beta"
STATUT = "ebauche"

class ErreurCombo(Exception):
    """Erreur de definition ou d'execution d'un combo."""


def chemin_racine():
    """Racine du cerveau-projet : via la variable posee par le .sh (sinon __file__)."""
    dossier = os.environ.get("COMBO_MOTEUR_DIR")
    if dossier:
        # dossier combos-moteur -> combos -> tools -> agents -> cerveau-projet
        return Path(dossier).resolve().parent.parent.parent.parent
    return Path(__file__).resolve().parent.parent.parent.parent.parent


def chemin_generateur():
    """Chemin du script generateurs-commande (source de verite des commandes)."""
    return (
        chemin_racine()
        / "agents"
        / "tools"
        / "generateurs"
        / "generateurs-commande"
        / "generateurs-commande.py"
    )


def chemin_classeur():
    """Chemin du stockage du classeur-variables (persistance optionnelle)."""
    return (
        chemin_racine()
        / "classeur-variables"
        / "stockage"
        / "variables-actuelles.md"
    )


def charger_definition(chemin):
    """Charge la definition-combo.json et verifie sa structure de base."""
    p = Path(chemin)
    if not p.is_file():
        raise ErreurCombo("Fichier de definition introuvable: %s" % chemin)
    try:
        with p.open(encoding="utf-8") as fh:
            donnees = json.load(fh)
    except json.JSONDecodeError as exc:
        raise ErreurCombo("JSON invalide dans %s: %s" % (chemin, exc))
    if "combo" not in donnees or "cases" not in donnees:
        raise ErreurCombo("La definition doit contenir 'combo' et 'cases'")
    return donnees


def valider_definition(donnees):
    """Valide la structure complete : case_depart, branches et suivant existants."""
    meta = donnees.get("combo", {})
    cases = donnees.get("cases", {})
    depart = meta.get("case_depart")
    erreurs = []
    if not depart:
        erreurs.append("case_depart manquant dans combo")
    elif depart not in cases:
        erreurs.append("case_depart '%s' introuvable dans cases" % depart)
    for cid, case in cases.items():
        typ = case.get("type")
        if typ not in ("generateur", "outil", "controle", "fin"):
            erreurs.append("case '%s': type inconnu '%s'" % (cid, typ))
            continue
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


def interpoler(texte, variables, contexte):
    """Remplace {var} par la valeur de la variable. Variable inconnue -> erreur."""
    if texte is None:
        return ""
    def remplacer(m):
        nom = m.group(1)
        if nom not in variables:
            raise ErreurCombo(
                "Variable non trouvee: {%s} (%s)" % (nom, contexte)
            )
        return str(variables[nom])
    return re.sub(r"\{([A-Za-z0-9_]+)\}", remplacer, str(texte))


def persister_variable(nom, valeur):
    """Ecrit (ou met a jour) la ligne de la variable dans variables-actuelles.md."""
    chemin = chemin_classeur()
    if not chemin.is_file():
        raise ErreurCombo(
            "Classeur introuvable pour la persistance: %s" % chemin
        )
    valeur_plate = str(valeur).replace("|", "/").replace("\n", " ").strip()
    date = datetime.date.today().strftime("%Y-%m-%d")
    ligne = "| `%s` | %s | combos-moteur | %s | [OK] |" % (nom, valeur_plate, date)

    try:
        texte = chemin.read_text(encoding="utf-8")
    except OSError as exc:
        raise ErreurCombo("Impossible de lire le classeur: %s" % exc)

    pattern = re.compile(
        r"^\| `%s` \|.*\| \[OK\] \|$" % re.escape(nom), re.MULTILINE
    )
    if pattern.search(texte):
        texte = pattern.sub(ligne, texte, count=1)
    else:
        marqueur = "\n---\n"
        index = texte.find(marqueur)
        if index == -1:
            texte = texte.rstrip("\n") + "\n" + ligne + "\n"
        else:
            texte = texte[:index] + "\n" + ligne + "\n" + texte[index:]

    try:
        chemin.write_text(texte, encoding="utf-8")
    except OSError as exc:
        raise ErreurCombo("Impossible d'ecrire le classeur: %s" % exc)
    print("[PERSISTANT] %s = %s" % (nom, valeur_plate))


def extraire_commande_generateur(sortie, catalogue):
    """Extrait la commande generee : la premiere ligne non vide APRES le marqueur."""
    lignes = sortie.splitlines()
    for i, ligne in enumerate(lignes):
        if "COMMANDE A LANCER" in ligne:
            for suivante in lignes[i + 1:]:
                if suivante.strip():
                    return suivante.strip()
            break
    lignes_nb = [l.strip() for l in lignes if l.strip()]
    if lignes_nb:
        return lignes_nb[-1]
    raise ErreurCombo(
        "Impossible d'extraire la commande generee pour '%s'" % catalogue
    )


def executer_case_generateur(case, cid, variables, dry_run, verbose):
    """Case generateur : compose la commande via generateurs-commande --reponses."""
    catalogue = case.get("catalogue")
    if not catalogue:
        raise ErreurCombo("Case generateur '%s' sans 'catalogue'" % cid)
    entrees = case.get("entrees") or {}
    if verbose:
        print("  [%s] generateur %s" % (cid, catalogue))

    morceaux = []
    for cle, valeur in entrees.items():
        v = interpoler(valeur, variables, "entrees de la case " + cid)
        morceaux.append("%s=%s" % (cle, v))
    reponses = ";".join(morceaux)

    generateur = chemin_generateur()
    if not generateur.is_file():
        raise ErreurCombo("Generateur introuvable: %s" % generateur)

    cmd = [
        sys.executable or "python3",
        str(generateur),
        "--commande",
        catalogue,
        "--reponses",
        reponses,
    ]
    if dry_run:
        print("[DRY-RUN] " + " ".join(cmd))
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ErreurCombo(
            "Echec de l'appel au generateur (case %s): %s" % (cid, exc)
        )

    if proc.returncode != 0:
        raise ErreurCombo(
            "Generateur en erreur (case %s, %s):\n%s"
            % (cid, catalogue, (proc.stderr or proc.stdout))
        )

    commande = extraire_commande_generateur(proc.stdout, catalogue)
    variables[case["sortie"]] = commande
    if verbose:
        print("  -> commande generee: %s" % commande)
    return


def executer_case_outil(case, cid, variables, dry_run, verbose):
    """Case outil : execute la commande (interpolee) en subprocess."""
    commande_brute = case.get("commande")
    if not commande_brute:
        raise ErreurCombo("Case outil '%s' sans 'commande'" % cid)
    commande = interpoler(commande_brute, variables, "commande de la case " + cid)
    if verbose:
        print("  [%s] outil : %s" % (cid, commande))

    if dry_run:
        print("[DRY-RUN] " + commande)
        return

    try:
        args_list = shlex.split(commande)
    except ValueError as exc:
        raise ErreurCombo("Commande invalide (case %s): %s" % (cid, exc))

    try:
        proc = subprocess.run(
            args_list,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ErreurCombo("Echec d'execution (case %s): %s" % (cid, exc))

    resultat = (proc.stdout or "") + (proc.stderr or "")
    variables[case["sortie"]] = resultat.strip()
    if verbose:
        print("  -> sortie: %s" % resultat.strip()[:200])
    if case.get("persistant"):
        persister_variable(case["sortie"], resultat.strip())
    return


def trouver_branche(branches, reponse):
    """Trouve la branche correspondant a la reponse (numero ou texte)."""
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


def resoudre_controle(case, cid, variables, reponses_predefinies, verbose):
    """Case controle : pose la question et retourne la prochaine case."""
    question = case.get("question", "Quelle reponse ?")
    branches = case.get("branches") or []
    if verbose:
        print("  [%s] controle : %s" % (cid, question))
    print("QUESTION : %s" % question)
    for i, b in enumerate(branches, 1):
        print("  [%d] %s" % (i, b.get("reponse", "?")))

    rep = None
    if reponses_predefinies is not None:
        if cid in reponses_predefinies:
            rep = reponses_predefinies[cid].strip()
        else:
            raise ErreurCombo(
                "Controle '%s': reponse manquante dans --reponses" % cid
            )
    else:
        try:
            rep = input("> ").strip()
        except EOFError:
            raise ErreurCombo(
                "Controle '%s': aucune reponse fournie (fin d'entree)" % cid
            )

    b = trouver_branche(branches, rep)
    if b is None:
        raise ErreurCombo(
            "Controle '%s': reponse inconnue '%s' (possibles: %s)"
            % (cid, rep, " / ".join(br.get("reponse", "?") for br in branches))
        )
    return b.get("vers")


def lister_cases(donnees):
    """Mode --liste : affiche les cases sans executer."""
    meta = donnees.get("combo", {})
    cases = donnees.get("cases", {})
    print("=== Combo %s v%s ===" % (meta.get("nom", "?"), meta.get("version", "?")))
    if meta.get("description"):
        print(meta.get("description"))
    print("Depart : %s" % meta.get("case_depart", "?"))
    print("")
    for cid, case in cases.items():
        print("  [%s] %-10s %s" % (cid, case.get("type", "?"), case.get("titre", "")))
    return 0


def executer(donnees, reponses_predefinies, dry_run, verbose):
    """Parcourt la definition case par case jusqu'a une case fin."""
    meta = donnees.get("combo", {})
    cases = donnees.get("cases", {})
    variables = {}
    cid = meta.get("case_depart")

    print("=== Combo %s v%s ===" % (meta.get("nom", "?"), meta.get("version", "?")))
    if meta.get("description"):
        print(meta.get("description"))
    print("")

    while True:
        if cid not in cases:
            raise ErreurCombo("Case suivante introuvable: '%s'" % cid)
        case = cases[cid]
        typ = case.get("type")
        titre = case.get("titre", cid)

        if typ == "fin":
            print("=== COMBO TERMINE ===")
            print("Fin de combo atteinte : case '%s' (%s)" % (cid, titre))
            if case.get("message"):
                print(case.get("message"))
            print("")
            if verbose:
                print("Variables finales :")
                for k, v in sorted(variables.items()):
                    print("  %s = %s" % (k, str(v)[:120]))
            return 0

        if verbose:
            print("")
            print("--- [%s] %s ---" % (cid, titre))

        if typ == "generateur":
            executer_case_generateur(case, cid, variables, dry_run, verbose)
        elif typ == "outil":
            executer_case_outil(case, cid, variables, dry_run, verbose)
        elif typ == "controle":
            suivant = resoudre_controle(case, cid, variables, reponses_predefinies, verbose)
            cid = suivant
            continue
        else:
            raise ErreurCombo("Case '%s': type inconnu '%s'" % (cid, typ))

        cid = case.get("suivant")
        if not cid:
            print("=== COMBO TERMINE ===")
            return 0


def parser_reponses_controles(chaine):
    """Parse --reponses 'c1=OUI;c3=NON' -> dict {case: reponse}."""
    reponses = {}
    if not chaine:
        return reponses
    for morceau in chaine.split(";"):
        morceau = morceau.strip()
        if not morceau:
            continue
        if "=" not in morceau:
            raise ErreurCombo("Reponse mal formee (case=reponse) : %s" % morceau)
        cle, valeur = morceau.split("=", 1)
        reponses[cle.strip()] = valeur.strip()
    return reponses


def main():
    args = sys.argv[1:]
    definition = None
    liste = False
    reponses = None
    dry_run = False
    verbose = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--liste":
            liste = True
        elif a == "--reponses":
            i += 1
            if i >= len(args):
                print("ERREUR: --reponses attend un argument", file=sys.stderr)
                return 1
            reponses = parser_reponses_controles(args[i])
        elif a == "--dry-run":
            dry_run = True
        elif a == "--verbose":
            verbose = True
        elif a == "--version":
            print("combos-moteur v%s" % VERSION)
            return 0
        elif a == "--help" or a == "-h":
            print("=== combos-moteur v%s === (Statut : %s)" % (VERSION, STATUT))
            print("Usage: combos-moteur.sh <definition-combo.json> [options]")
            print("Options :")
            print("  --liste             Lister les cases sans executer")
            print("  --reponses <liste>  Reponses des controles : case=reponse;case2=reponse2")
            print("  --dry-run           Afficher les commandes sans les executer")
            print("  --verbose           Afficher les details de chaque case")
            print("  --version           Afficher la version")
            return 0
        else:
            if definition is None:
                definition = a
            else:
                print("ERREUR: argument inattendu : %s" % a, file=sys.stderr)
                return 1
        i += 1

    if not definition:
        print("ERREUR: chemin de la definition-combo.json obligatoire", file=sys.stderr)
        return 1

    try:
        donnees = charger_definition(definition)
        valider_definition(donnees)
        if liste:
            return lister_cases(donnees)
        return executer(donnees, reponses, dry_run, verbose)
    except ErreurCombo as exc:
        print("[ERREUR] %s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
PYEOF
}

# Main
main() {
    verifier_nommage
    if ! command -v python3 >/dev/null 2>&1; then
        echo "[ERREUR] python3 est requis pour combos-moteur.sh (parite avec le .py)"
        exit 1
    fi
    executer_python "$@"
}

main "$@"
