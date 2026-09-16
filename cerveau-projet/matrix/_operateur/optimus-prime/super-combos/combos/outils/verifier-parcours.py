#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-parcours.py -- Garde : tout theme PRET est-il ROUTE, et toute route MENE-t-elle quelque part ?

Pourquoi (lacune trouvee le 2026-09-14, mission MO-087) : le catalogue d'Optimus
declarait DOUZE themes `statut: pret` (index-themes.json), mais son PARCOURS
(index-parcours.json) n'en routait que CINQ. Sept themes -- FICHIER, AUTO-CORRECTION,
AUTO-TESTING, AUTO-OPTIMISATION, AUTO-PERFORMANCE, AUTO-AUDIT-NEMESIS, AUTO-XXX --
etaient donc PRETS MAIS INATTEIGNABLES : ecrits, testes, jamais routes. Personne ne
s'en plaignait, parce qu'AUCUN controle ne croisait les deux index : c'est le motif
qu'on vient de nommer quatre fois (une chose ecrite n'est pas une chose LUE). Le meme
jour, la chaine `[purification]` demandait une case `[decision]` -- et une case qu'on
ne route pas n'existe pas.

CE QU'IL EXIGE :
  1. tout theme du CATALOGUE est ROUTE par le PARCOURS (aucun theme orphelin) ;
  2. toute route du PARCOURS vise un theme du CATALOGUE (aucune route morte) ;
  3. le fichier de chaque theme EXISTE (essaye sous themes/, puis sous la racine de
     l'operateur -- `AUTO-XXX` designe `super-combos/sc-001-auto-xxx/main.py`) ;
  4. aucun DOUBLON, ni dans le catalogue, ni dans le parcours.

L'AUTOTEST le PIEGE (lecon L-032) : un cobaye complet est ACCEPTE, un theme non
route est ACCUSE, une route morte est ACCUSE. Un detecteur jamais vu crier ne
prouve rien.

CE QU'IL NE FAIT PAS : lecture seule -- il lit deux index et des chemins.

Usage: python verifier-parcours.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

# --- REFERENCES (aucune valeur en dur dans la logique) -----------------------
CHEMIN_INDEX_PARCOURS = Path("_operateur") / "optimus-prime" / "parcours" / "index-parcours.json"
CHEMIN_INDEX_THEMES = (Path("_operateur") / "optimus-prime" / "parcours" / "themes"
                       / "index-themes.json")
DOSSIER_THEMES = Path("_operateur") / "optimus-prime" / "parcours" / "themes"
RACINE_OPERATEUR = Path("_operateur") / "optimus-prime"

RESULTATS = []


def trouver_matrix(racine):
    """Retourne le dossier matrix/, ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / "matrice").is_dir():
            return candidat
    return None


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def lire_json(chemin):
    """JSON d'un fichier, ou {} (un index illisible est un ECHEC dit, pas un plantage)."""
    try:
        return json.loads(Path(chemin).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def themes_du_catalogue(catalogue):
    """Noms des themes declares par le catalogue."""
    return [str(entree.get("nom")) for entree in catalogue.get("themes", [])]


def routes_du_parcours(parcours):
    """Noms des themes routes par le parcours."""
    return [str(entree.get("theme")) for entree in parcours.get("parcours", [])]


def fichiers_du_catalogue(catalogue):
    """(nom, fichier) des themes du catalogue."""
    return [(str(entree.get("nom")), str(entree.get("fichier") or ""))
            for entree in catalogue.get("themes", [])]


def resoudre_fichier(matrix, fichier):
    """Chemin du fichier d'un theme : themes/, puis racine de l'operateur, puis matrix/."""
    if not fichier:
        return None
    for base in (matrix / DOSSIER_THEMES, matrix / RACINE_OPERATEUR, matrix):
        candidat = base / fichier
        if candidat.is_file():
            return candidat
    return None


def controler_parcours(matrix):
    """Croise les DEUX index : aucun theme orphelin, aucune route morte."""
    parcours = lire_json(matrix / CHEMIN_INDEX_PARCOURS)
    catalogue = lire_json(matrix / CHEMIN_INDEX_THEMES)
    if not parcours or not catalogue:
        return ("index-lisibles", False,
                "index illisible : " + str(CHEMIN_INDEX_PARCOURS) + " ou "
                + str(CHEMIN_INDEX_THEMES)), ["index de parcours illisible"]

    ecarts = []
    catalogue_noms = themes_du_catalogue(catalogue)
    routes = routes_du_parcours(parcours)

    orphelins = [nom for nom in catalogue_noms if nom not in routes]
    controler("themes-routes", not orphelins,
              (str(len(catalogue_noms)) + " theme(s) au catalogue, " + str(len(routes))
               + " route(s)") if not orphelins
              else "JAMAIS ROUTES : " + ", ".join(orphelins))
    if orphelins:
        ecarts.append("themes jamais routes : " + ", ".join(orphelins))

    mortes = [nom for nom in routes if nom not in catalogue_noms]
    controler("routes-vivantes", not mortes,
              "chaque route vise un theme du catalogue" if not mortes
              else "ROUTES MORTES : " + ", ".join(mortes))
    if mortes:
        ecarts.append("routes mortes : " + ", ".join(mortes))

    doublons_catalogue = sorted({n for n in catalogue_noms if catalogue_noms.count(n) > 1})
    doublons_routes = sorted({n for n in routes if routes.count(n) > 1})
    controler("sans-doublon", not doublons_catalogue and not doublons_routes,
              "catalogue et parcours sans doublon"
              if not doublons_catalogue and not doublons_routes
              else "DOUBLONS : catalogue " + str(doublons_catalogue)
                   + " ; parcours " + str(doublons_routes))
    if doublons_catalogue or doublons_routes:
        ecarts.append("doublons : " + str(doublons_catalogue + doublons_routes))

    introuvables = [nom for nom, fichier in fichiers_du_catalogue(catalogue)
                    if resoudre_fichier(matrix, fichier) is None]
    controler("fichiers-existants", not introuvables,
              "chaque theme du catalogue a son fichier" if not introuvables
              else "FICHIERS INTROUVABLES : " + ", ".join(introuvables))
    if introuvables:
        ecarts.append("fichiers de theme introuvables : " + ", ".join(introuvables))

    return ("themes-routes", not ecarts, "croisement des deux index"), ecarts


def controler_autotest():
    """Le croisement se PIEGE (lecon L-032) : trois cobayes en dossier jetable."""
    racine = Path(tempfile.mkdtemp(prefix="verifier-parcours-autotest-"))
    base = racine / DOSSIER_THEMES
    base.mkdir(parents=True, exist_ok=True)

    def poser(nom_theme, fichier):
        (base / fichier).write_text("{}\n", encoding="utf-8")

    def ecrire_index(noms, routes):
        (racine / CHEMIN_INDEX_THEMES).write_text(
            json.dumps({"themes": [{"nom": n, "fichier": f} for n, f in noms]}),
            encoding="utf-8")
        (racine / CHEMIN_INDEX_PARCOURS).write_text(
            json.dumps({"parcours": [{"theme": r} for r in routes]}), encoding="utf-8")

    epreuves = []
    try:
        poser("ALPHA", "theme-alpha.json")
        poser("BETA", "theme-beta.json")
        ecrire_index([("ALPHA", "theme-alpha.json"), ("BETA", "theme-beta.json")],
                     ["ALPHA", "BETA"])
        _, ecarts = controler_parcours(racine)
        epreuves.append(("cobaye complet ACCEPTE", not ecarts))

        ecrire_index([("ALPHA", "theme-alpha.json"), ("BETA", "theme-beta.json")], ["ALPHA"])
        _, ecarts = controler_parcours(racine)
        epreuves.append(("theme ORPHELIN ACCUSE", len(ecarts) == 1 and "BETA" in ecarts[0]))

        ecrire_index([("ALPHA", "theme-alpha.json")], ["ALPHA", "FANTOME"])
        _, ecarts = controler_parcours(racine)
        epreuves.append(("route MORTE ACCUSEE", len(ecarts) == 1 and "FANTOME" in ecarts[0]))
    finally:
        shutil.rmtree(racine, ignore_errors=True)

    reussies = sum(1 for _, ok in epreuves if ok)
    detail = ("piege (" + str(reussies) + "/3)" if reussies == len(epreuves)
              else "rate : " + ", ".join(nom for nom, ok in epreuves if not ok))
    return ("autotest-croisement", reussies == len(epreuves), detail)


def main():
    parser = argparse.ArgumentParser(description="Garde : tout theme pret est route, toute route mene")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2

    resultats = []
    ecarts_nommes = []

    resultat, ecarts = controler_parcours(matrix)
    resultats.append(resultat)
    ecarts_nommes.extend(ecarts)
    resultats.append(controler_autotest())

    print("VERIFIER PARCOURS -- un theme ecrit doit etre un theme ROUTE")
    if any(not ok for _, ok, _ in resultats) or ecarts_nommes:
        print("\nVERDICT KO : un theme pret n'est pas route, ou une route ne mene nulle part"
              " (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : le catalogue et le parcours se correspondent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
