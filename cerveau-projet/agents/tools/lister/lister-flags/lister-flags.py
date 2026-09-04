#!/usr/bin/env python3
# -*- coding: ascii -*-
# lister-flags.py
# Liste les flags et arguments des outils et combos du cerveau-projet.
# Les scripts Python sont inspectes avec ast sans etre executes.
# Version : 0.1.1
# Statut : prepare
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

"""
lister-flags.py

Usage:
  lister-flags.py [CIBLES...] [OPTIONS]
"""

import argparse
import ast
import json
import os
import shlex
import sys
import time
from pathlib import Path

VERSION = "0.1.1"
STATUT = "prepare"


_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    nom = Path(script_path).stem
    if nom != "lister-flags":
        print(_couleur("ERREUR: nom de fichier invalide : %s" % nom, "rouge"),
              file=sys.stderr)
        print("  Attendu : lister-flags.py", file=sys.stderr)
        return 2
    return 0


def _doc_chemin(script_path):
    return Path(script_path).with_suffix(".md")


def verifier_doc_presente(script_path):
    doc = _doc_chemin(script_path)
    if not doc.is_file():
        print(_couleur("ERREUR: documentation manquante : %s" % doc, "rouge"),
              file=sys.stderr)
        return 2
    return 0


def afficher_section_utilisation(doc):
    try:
        lignes = doc.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return
    actif = False
    for ligne in lignes:
        if ligne.startswith("## "):
            actif = ligne.strip().lower() == "## utilisation"
            continue
        if actif and ligne.strip():
            print("  " + ligne)


def exiger_confirmation_doc(script_path, dry_run, confirme_doc):
    if dry_run or confirme_doc:
        return 0
    doc = _doc_chemin(script_path)
    print(_couleur("=== DOCUMENTATION OBLIGATOIRE ===", "jaune"))
    print("  Lisez %s avant l usage reel." % doc.name)
    print("")
    afficher_section_utilisation(doc)
    print("")
    print(_couleur("REFUS: relancez avec --confirme-doc.", "rouge"),
          file=sys.stderr)
    return 2


def trouver_racine():
    courant = Path(__file__).resolve().parent
    for candidat in (courant,) + tuple(courant.parents):
        if (candidat / "AGENTS.md").is_file():
            return candidat
    return Path.cwd()


def lire_json(chemin):
    try:
        with open(chemin, encoding="utf-8", errors="replace") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def valeur_litterale(noeud, defaut=None):
    try:
        return ast.literal_eval(noeud)
    except (ValueError, TypeError, SyntaxError):
        return defaut


def nom_type(valeur):
    if valeur is None:
        return "texte"
    if isinstance(valeur, str):
        return {"str": "texte", "string": "texte", "int": "entier",
                "float": "decimal", "bool": "booleen"}.get(valeur, valeur)
    if isinstance(valeur, ast.Name):
        return {"str": "texte", "int": "entier", "float": "decimal",
                "bool": "booleen"}.get(valeur.id, valeur.id)
    if isinstance(valeur, ast.Attribute):
        return valeur.attr
    return "texte"


def normaliser_nom(nom):
    return str(nom or "").lstrip("-").replace("_", "-").lower()


def categorie_script(script):
    morceaux = str(script or "").replace("\\", "/").split("/")
    try:
        index = morceaux.index("tools")
        return morceaux[index + 1] if index + 1 < len(morceaux) else "inconnu"
    except ValueError:
        return "inconnu"


def chemin_script(racine, script):
    return racine / Path(str(script).replace("/", os.sep))


def nouveau_flag(nom, type_flag="inconnu", obligatoire=False, description="",
                 source="inconnu", flag=None, defaut=None, choix=None,
                 positionnel=False, alias=None, cas=None):
    resultat = {
        "nom": nom,
        "flag": flag or (nom if str(nom).startswith("-") else ""),
        "type": type_flag or "inconnu",
        "obligatoire": bool(obligatoire),
        "description": description or "",
        "source": source,
        "positionnel": bool(positionnel),
    }
    if defaut is not None:
        resultat["defaut"] = defaut
    if choix:
        resultat["choix"] = choix
    if alias:
        resultat["alias"] = alias
    if cas:
        resultat["cas"] = cas
    return resultat


def flags_catalogue(entree, source="catalogue", cas=None):
    resultat = []
    for parametre in entree.get("parametres", []) or []:
        cle = str(parametre.get("cle", ""))
        if not cle:
            continue
        flag = str(parametre.get("flag", ""))
        nom = flag or cle
        resultat.append(nouveau_flag(
            nom=nom,
            flag=flag,
            type_flag=parametre.get("type", "inconnu"),
            obligatoire=parametre.get("obligatoire", False),
            description=parametre.get("question", parametre.get("description", "")),
            source=source,
            defaut=parametre.get("defaut"),
            choix=parametre.get("choix"),
            positionnel=not bool(flag),
            cas=cas,
        ))
    return resultat


def flags_argparse(script):
    try:
        arbre = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    except (OSError, UnicodeError, SyntaxError):
        return []
    resultat = []
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        if not isinstance(noeud.func, ast.Attribute) or noeud.func.attr != "add_argument":
            continue
        noms = [x.value for x in noeud.args
                if isinstance(x, ast.Constant) and isinstance(x.value, str)]
        if not noms:
            continue
        options = [x for x in noms if x.startswith("-")]
        positionnels = [x for x in noms if not x.startswith("-")]
        nom = max(options, key=len) if options else positionnels[0]
        alias = [x for x in options if x != nom]
        kw = {x.arg: x.value for x in noeud.keywords if x.arg}
        action = valeur_litterale(kw.get("action"), "")
        type_val = nom_type(kw.get("type"))
        if action in ("store_true", "store_false"):
            type_val = "flag"
        elif action:
            type_val = action
        resultat.append(nouveau_flag(
            nom=nom,
            flag=nom if options else "",
            type_flag=type_val,
            obligatoire=valeur_litterale(kw.get("required"), False),
            description=valeur_litterale(kw.get("help"), ""),
            source="argparse",
            defaut=valeur_litterale(kw.get("default")),
            choix=valeur_litterale(kw.get("choices")),
            positionnel=not bool(options),
            alias=alias,
        ))
    return resultat


def fusionner_flags(flags):
    fusion = {}
    ordre = []
    for flag in flags:
        cle = normaliser_nom(flag.get("nom"))
        if not cle:
            continue
        if cle not in fusion:
            fusion[cle] = dict(flag)
            ordre.append(cle)
            continue
        actuel = fusion[cle]
        sources = set(x.strip() for x in actuel.get("source", "").split(",") if x.strip())
        sources.update(x.strip() for x in flag.get("source", "").split(",") if x.strip())
        actuel["source"] = ", ".join(sorted(sources))
        if actuel.get("type") in ("", "inconnu") and flag.get("type"):
            actuel["type"] = flag["type"]
        if not actuel.get("description") and flag.get("description"):
            actuel["description"] = flag["description"]
        if not actuel.get("flag") and flag.get("flag"):
            actuel["flag"] = flag["flag"]
        if flag.get("obligatoire"):
            actuel["obligatoire"] = True
        if flag.get("defaut") is not None and actuel.get("defaut") is None:
            actuel["defaut"] = flag["defaut"]
        if flag.get("choix") and not actuel.get("choix"):
            actuel["choix"] = flag["choix"]
        alias = set(actuel.get("alias", []))
        alias.update(flag.get("alias", []))
        if alias:
            actuel["alias"] = sorted(alias)
    return [fusion[x] for x in ordre]


def extraire_flags_commande(commande, cas=None):
    try:
        morceaux = shlex.split(commande, posix=True)
    except ValueError:
        morceaux = str(commande).split()
    resultat = []
    for index, morceau in enumerate(morceaux):
        if not morceau.startswith("-") or morceau == "-":
            continue
        nom = morceau.split("=", 1)[0]
        if nom in ("--", "-", "{cmd1}"):
            continue
        valeur = ""
        if "=" in morceau:
            valeur = "texte"
        elif index + 1 < len(morceaux) and not morceaux[index + 1].startswith("-"):
            valeur = "texte"
        resultat.append(nouveau_flag(
            nom=nom,
            flag=nom,
            type_flag=valeur or "flag",
            description="Flag trouve dans une commande de combo.",
            source="definition-combo",
            cas=cas,
        ))
    return resultat


def charger_donnees(racine):
    catalogue_path = racine / "cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json"
    catalogue = lire_json(catalogue_path)
    if not isinstance(catalogue, dict) or not isinstance(catalogue.get("commandes"), list):
        raise RuntimeError("Catalogue introuvable ou invalide : %s" % catalogue_path)

    commandes = {}
    entites = {}
    for entree in catalogue["commandes"]:
        nom = str(entree.get("nom", ""))
        if not nom:
            continue
        script = chemin_script(racine, entree.get("script", ""))
        flags = flags_catalogue(entree)
        if script.is_file() and script.suffix == ".py":
            flags = fusionner_flags(flags + flags_argparse(script))
        entites[nom] = {
            "nom": nom,
            "categorie": categorie_script(entree.get("script", "")),
            "description": entree.get("description", ""),
            "source": "catalogue",
            "chemin": entree.get("script", ""),
            "flags": flags,
        }
        commandes[nom] = entree

    combo_dir = racine / "cerveau-projet/agents/tools/combos"
    if combo_dir.is_dir():
        definitions = sorted(combo_dir.rglob("definition-combo.json"))
    else:
        definitions = []

    for definition_path in definitions:
        definition = lire_json(definition_path)
        combo = definition.get("combo", {}) if isinstance(definition, dict) else {}
        nom = str(combo.get("nom", ""))
        if not nom:
            continue
        entite = entites.setdefault(nom, {
            "nom": nom,
            "categorie": "combos",
            "description": combo.get("description", ""),
            "source": "definition-combo",
            "chemin": str(definition_path.relative_to(racine)).replace(os.sep, "/"),
            "flags": [],
        })
        entite["categorie"] = "combos"
        entite["source"] = "catalogue, definition-combo" if nom in commandes else "definition-combo"
        if combo.get("description"):
            entite["description"] = combo["description"]
        flags = list(entite.get("flags", []))
        if nom in commandes:
            flags.extend(flags_catalogue(commandes[nom], source="catalogue"))
        cases = definition.get("cases", {}) if isinstance(definition, dict) else {}
        for case_id, case in cases.items():
            if not isinstance(case, dict):
                continue
            ref = case.get("catalogue")
            if ref in commandes:
                flags.extend(flags_catalogue(commandes[ref], source="definition-combo, catalogue", cas=case_id))
            commande = case.get("commande")
            if isinstance(commande, str):
                flags.extend(extraire_flags_commande(commande, cas=case_id))
        entite["flags"] = fusionner_flags(flags)

    return sorted(entites.values(), key=lambda x: x["nom"].lower())


def filtrer(entites, args):
    noms = []
    noms.extend(args.cibles or [])
    noms.extend(args.outil or [])
    noms.extend(args.combo or [])
    if noms and not args.tous:
        demandes = {x.lower() for x in noms}
        entites = [x for x in entites if x["nom"].lower() in demandes]
    if args.categorie:
        categorie = args.categorie.lower()
        entites = [x for x in entites if x["categorie"].lower() == categorie]

    if args.source != "tous":
        entites = [dict(x, flags=[f for f in x["flags"]
                                  if args.source in f.get("source", "")])
                   for x in entites]

    partage = {}
    for entite in entites:
        for flag in entite["flags"]:
            cle = normaliser_nom(flag.get("nom"))
            partage.setdefault(cle, set()).add(entite["nom"])
    flags_partages = {cle for cle, utilisateurs in partage.items() if len(utilisateurs) > 1}
    if args.flag_partage:
        cle_demande = normaliser_nom(args.flag_partage)
        if cle_demande not in flags_partages:
            return [], flags_partages
        entites = [dict(x, flags=[f for f in x["flags"]
                                  if normaliser_nom(f.get("nom")) == cle_demande])
                   for x in entites]
    return [x for x in entites if x["flags"] or args.inclure_vides], flags_partages


def format_json(entites, flags_partages):
    donnees = []
    for entite in entites:
        donnees.append({
            "nom": entite["nom"],
            "categorie": entite["categorie"],
            "description": entite["description"],
            "source": entite["source"],
            "flags": entite["flags"],
        })
    return json.dumps({
        "version": VERSION,
        "flags_partages": sorted(flags_partages),
        "entites": donnees,
    }, ensure_ascii=True, indent=2)


def afficher_table(entites, flags_partages, verbose=False):
    print(_couleur("=== lister-flags v%s ===" % VERSION, "bleu"))
    print("Entites : %d | Flags partages : %d" % (len(entites), len(flags_partages)))
    for entite in entites:
        print("")
        print("[%s] %s" % (entite["categorie"], entite["nom"]))
        if entite["description"]:
            print("  %s" % entite["description"])
        for flag in entite["flags"]:
            requis = "requis" if flag.get("obligatoire") else "optionnel"
            nom = flag.get("nom", "?")
            description = flag.get("description", "")
            ligne = "  %-24s %-10s %-9s" % (nom, flag.get("type", "inconnu"), requis)
            if description:
                ligne += " %s" % description
            print(ligne)
            if verbose:
                print("    source=%s%s" % (
                    flag.get("source", "inconnu"),
                    " | cas=%s" % flag["cas"] if flag.get("cas") else ""))


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="lister-flags.py",
        description="Lister les flags des outils et combos du cerveau-projet.",
    )
    parser.add_argument("cibles", nargs="*", help="Noms d outils ou de combos")
    parser.add_argument("--outil", action="append", default=[],
                        help="Outil cible (repetable)")
    parser.add_argument("--combo", action="append", default=[],
                        help="Combo cible (repetable)")
    parser.add_argument("--tous", action="store_true",
                        help="Lister toutes les entites")
    parser.add_argument("--categorie", default="",
                        help="Filtrer par categorie, par exemple lister ou combos")
    parser.add_argument("--flag-partage", default="",
                        help="Afficher un flag utilise par plusieurs entites")
    parser.add_argument("--source", choices=("tous", "catalogue", "argparse", "definition-combo"),
                        default="tous", help="Limiter la source des flags")
    parser.add_argument("--format", choices=("table", "json"), default="table",
                        help="Format de sortie")
    parser.add_argument("--json", action="store_true",
                        help="Alias de --format json")
    parser.add_argument("--inclure-vides", action="store_true",
                        help="Inclure les entites sans flag apres filtrage")
    parser.add_argument("--verbose", action="store_true", help="Afficher la source de chaque flag")
    parser.add_argument("--dry-run", action="store_true", help="Mode lecture explicite, sans modification")
    parser.add_argument("--chrono", action="store_true", help="Afficher la duree d execution")
    parser.add_argument("--doc", action="store_true",
                        help="Afficher la documentation complete et sortir")
    parser.add_argument("--confirme-doc", action="store_true",
                        help="Confirmer la lecture de la documentation")
    parser.add_argument("--version", action="version",
                        version="lister-flags.py v%s (%s)" % (VERSION, STATUT))
    return parser


def main(argv=None):
    debut = time.perf_counter()
    script = sys.argv[0]
    erreur = verifier_nommage(script)
    if erreur:
        return erreur
    erreur = verifier_doc_presente(script)
    if erreur:
        return erreur
    parser = construire_parser()
    args = parser.parse_args(argv)
    if args.doc:
        print(_doc_chemin(script).read_text(encoding="utf-8"))
        return 0
    erreur = exiger_confirmation_doc(script, args.dry_run, args.confirme_doc)
    if erreur:
        return erreur
    if args.json:
        args.format = "json"

    try:
        entites = charger_donnees(trouver_racine())
    except RuntimeError as exc:
        print("Erreur: %s" % exc, file=sys.stderr)
        return 1
    entites, flags_partages = filtrer(entites, args)
    if args.format == "json":
        print(format_json(entites, flags_partages))
    else:
        afficher_table(entites, flags_partages, args.verbose)
    if not entites:
        print("Aucune entite ou aucun flag ne correspond aux filtres.", file=sys.stderr)
        return 1
    if args.chrono:
        print("Duree : %.3fs" % (time.perf_counter() - debut))
    return 0


if __name__ == "__main__":
    sys.exit(main())
