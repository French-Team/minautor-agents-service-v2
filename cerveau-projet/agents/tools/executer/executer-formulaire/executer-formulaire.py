#!/usr/bin/env python3
# -*- coding: ascii -*-
# executer-formulaire.py
# DECISION D6/D7 (2026-08-21) : OUTIL = FORMULAIRE. L agent lance l outil,
# l outil lui fournit le formulaire a remplir (mini-description + liste des
# champs/flags), l agent ecrit ses reponses dans un FICHIER JSON (avec
# creer-fichier, jamais de ligne bash geante -> anti-heredoc), l outil
# VALIDE (requis, types) puis COMPOSE la commande depuis le catalogue
# generateurs-commande et L EXECUTE a la place de l agent.
#
# Usage :
#   # 1. Afficher le formulaire (mini-description + champs/flags) d un outil
#   python3 executer-formulaire.py --outil creer-fichier --schema
#
#   # 2. Fournir ses reponses dans un fichier JSON puis EXECUTER :
#   #    (l agent ecrit le JSON avec creer-fichier, pas en argument bash)
#   python3 executer-formulaire.py --outil creer-fichier --reponses reponses.json
#
# Format du fichier de reponses (JSON) :
#   { "<cle-du-champ>": "<valeur>", ... }
#   Cle et exigences de chaque champ = ce que --schema affiche.
#
# Options :
#   --outil <nom>       Outil du catalogue a executer (ex: creer-fichier)
#   --schema            Afficher le formulaire (description + champs + flags)
#   --reponses <chemin> Fichier JSON des reponses (anti-heredoc)
#   --dry-run           Composer la commande sans l executer
#   --version           Afficher la version
#   --aide, -h          Afficher cette aide
#
# Version : 0.1.0
# Statut : prepare
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

"""executer-formulaire.py
executer-formulaire

Usage:
  executer-formulaire.py --outil <nom> [--schema | --reponses <fichier>] [--dry-run]
"""

import argparse
import io
import json
import os
import subprocess
import sys

VERSION = "0.1.0"
STATUT = "prepare"

# outils/executer/executer-formulaire/ -> racine projet (5 niveaux)
_RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
CATALOGUE = os.path.join(
    _RACINE, "cerveau-projet", "agents", "tools", "generateurs",
    "generateurs-commande", "catalogue-commandes.json")


def _charger_catalogue():
    try:
        with io.open(CATALOGUE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _trouver_outil(catalogue, nom):
    for c in catalogue.get("commandes", []):
        if c.get("nom") == nom:
            return c
    return None


def _afficher_schema(outil):
    print("=== FORMULAIRE : %s ===" % outil["nom"])
    print("Description : %s" % outil.get("description", ""))
    print("Script      : %s" % outil.get("script", ""))
    print("")
    print("Champs a renseigner (JSON de reponses) :")
    for p in outil.get("parametres", []):
        requis = "REQUIS" if p.get("obligatoire") else "optionnel"
        flag = p.get("flag", "")
        ligne = "  - %s : type=%s (%s)" % (p["cle"], p.get("type", "texte"), requis)
        if flag:
            ligne += " [flag=%s]" % flag
        if p.get("defaut"):
            ligne += " [defaut=%r]" % p["defaut"]
        print(ligne)
        question = p.get("question", "")
        if question:
            print("      %s" % question)
    print("")
    print("Exemple de fichier de reponses (ecrit avec creer-fichier) :")
    ex = {}
    for p in outil.get("parametres", []):
        if p.get("type") == "flag":
            ex[p["cle"]] = True
        elif p.get("defaut"):
            ex[p["cle"]] = p["defaut"]
        else:
            ex[p["cle"]] = "<valeur>"
    print(json.dumps(ex, ensure_ascii=True, indent=1))


def _valider(outil, reponses):
    erreurs = []
    for p in outil.get("parametres", []):
        cle = p["cle"]
        if p.get("obligatoire") and cle not in reponses:
            erreurs.append("Champ requis manquant: %s" % cle)
            continue
        if cle not in reponses:
            continue
        valeur = reponses[cle]
        type_p = p.get("type", "texte")
        if type_p == "flag":
            if not isinstance(valeur, bool):
                erreurs.append("Champ %s doit etre true/false (boolean)" % cle)
        elif type_p == "nombre":
            try:
                int(valeur)
            except (TypeError, ValueError):
                erreurs.append("Champ %s doit etre un nombre" % cle)
        else:
            if not isinstance(valeur, str):
                erreurs.append("Champ %s doit etre une chaine" % cle)
    if erreurs:
        print("[ERREUR] Formulaire INVALIDE (refus avant execution) :")
        for e in erreurs:
            print("  - %s" % e)
        return False
    return True


def _composer(outil, reponses, dry_run):
    """Compose la commande a partir du modele du catalogue. Retourne argv."""
    modele = outil.get("modele", "")
    # Remplacement simple : chaque {cle} -> valeur / flag active / vide
    argv = []
    for segment in modele.split():
        if segment.startswith("{") and segment.endswith("}"):
            cle = segment[1:-1]
            p = next((x for x in outil.get("parametres", []) if x["cle"] == cle), None)
            valeur = reponses.get(cle)
            if p and p.get("type") == "flag":
                if valeur:
                    argv.append(p.get("flag", "--" + cle))
            elif p and p.get("flag"):
                # Flag texte (ex: --contenu-chemin <valeur>) : le flag n est
                # passe que si la valeur est fournie.
                if valeur is not None and str(valeur) != "":
                    argv.append(p["flag"])
                    argv.append(str(valeur))
            elif valeur is not None and valeur != "":
                argv.append(str(valeur))
        elif "{" in segment:
            # modele avec flag prefixe ex: --debut {debut}
            prefixe, cle = segment.split("{", 1)
            cle = cle.rstrip("}").strip()
            valeur = reponses.get(cle)
            if valeur is not None and valeur != "":
                argv.append(prefixe)
                argv.append(str(valeur))
        else:
            argv.append(segment)
    cmd = [outil.get("interpreteur", "python3"), outil.get("script", "")] + argv
    if dry_run:
        print("[DRY-RUN] Commande composee :")
        print("  " + " ".join(cmd))
        return None
    return cmd


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="executer-formulaire",
        description="DECISION D6/D7 : l agent remplit un formulaire (fichier JSON), "
                    "l outil valide, compose et execute la commande.",
        add_help=False,
    )
    parser.add_argument("--outil", default=None, help="Nom de l outil du catalogue")
    parser.add_argument("--schema", action="store_true",
                        help="Afficher le formulaire (description + champs + flags)")
    parser.add_argument("--reponses", default=None,
                        help="Fichier JSON des reponses (anti-heredoc)")
    parser.add_argument("--dry-run", action="store_true", help="Composer sans executer")
    parser.add_argument("--version", action="store_true", help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true", help="Afficher l aide")

    args = parser.parse_args(argv)

    if args.aide:
        parser.print_help()
        return 0
    if args.version:
        print("executer-formulaire %s (%s)" % (VERSION, STATUT))
        return 0
    if not args.outil:
        print("[ERREUR] --outil obligatoire")
        parser.print_help()
        return 2

    catalogue = _charger_catalogue()
    if catalogue is None:
        print("[ERREUR] Catalogue introuvable : %s" % CATALOGUE)
        return 2
    outil = _trouver_outil(catalogue, args.outil)
    if outil is None:
        print("[ERREUR] Outil '%s' absent du catalogue" % args.outil)
        return 2

    if args.schema:
        _afficher_schema(outil)
        return 0
    if not args.reponses:
        print("[ERREUR] Fournir --schema OU --reponses <fichier.json>")
        return 2

    # Charger les reponses depuis le fichier (ANTI-HEREDOC : jamais d argument
    # bash geant ; l agent a ecrit ce JSON avec creer-fichier).
    try:
        with io.open(args.reponses, "r", encoding="utf-8") as fh:
            reponses = json.load(fh)
    except (OSError, ValueError) as e:
        print("[ERREUR] Fichier de reponses illisible : %s" % e)
        return 1
    if not isinstance(reponses, dict):
        print("[ERREUR] Le fichier de reponses doit etre un objet JSON")
        return 1

    # VALIDATION AVANT EXECUTION (D7 : un formulaire invalide n est JAMAIS execute)
    if not _valider(outil, reponses):
        return 1

    cmd = _composer(outil, reponses, args.dry_run)
    if cmd is None:
        return 0

    # EXECUTION AUTOMATIQUE a la place de l agent (D6)
    try:
        proc = subprocess.run(cmd, cwd=_RACINE, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        print("[ERREUR] Execution impossible : %s" % e)
        return 1
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    # Regle immuable de nommage : prefixe de la categorie
    base = os.path.basename(sys.argv[0])
    dossier = os.path.basename(os.path.dirname(os.path.abspath(sys.argv[0])))
    if not base.startswith(dossier.split("-")[0] + "-"):
        print("[ERREUR] Nommage invalide : %s doit commencer par %s-"
              % (base, dossier.split("-")[0]))
        sys.exit(2)
    sys.exit(main())