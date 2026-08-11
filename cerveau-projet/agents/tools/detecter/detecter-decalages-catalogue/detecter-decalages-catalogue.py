#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-decalages-catalogue.py
# Compare CHAQUE entree du catalogue du generateur a l interface reelle de son
# outil (--aide puis --help en fallback) pour garantir 0 decalage modele/interface.
# Cree par Vulcain le 2026-08-09 (institutionnalisation du scan ecrit par Atlas).
# v0.1.1 : section COMBOS ajoutee (garde-fou des cles des definitions-combo vs
# catalogue, anti-recurrence du KO test-003, spec-combos-moteur v0.2.1).
# Version : 0.1.1
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
detecter-decalages-catalogue.py

Detecte les decalages entre le catalogue du generateur (catalogue-commandes.json)
et les interfaces reelles des outils (options --aide/--help).

Depuis la v0.1.1, il scanne AUSSI les definitions-combo (combos/*/definition-
combo.json) : les cles des entrees des cases generateur doivent correspondre
EXACTEMENT aux parametres du catalogue (spec-combos-moteur v0.2.1).

Usage:
  detecter-decalages-catalogue.py [--sortie CHEMIN] [--version]

Options:
  --sortie CHEMIN   Chemin du rapport genere (defaut: rapport-detecter-decalages-catalogue-<date>.md
                    dans le dossier courant)
  --version         Afficher la version
  --aide            Afficher cette aide
"""
import glob
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime

VERSION = "0.1.1"
COMBOS_GLOBE = "cerveau-projet/agents/tools/combos/*/definition-combo.json"
CATALOGUE = "cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json"
TIMEOUT = 8
# detecter-decalages-catalogue.py est a: cerveau-projet/agents/tools/detecter/detecter-decalages-catalogue/
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))


def extraire_options(aide):
    """Extrait les options longues (--xxx) de l aide, en excluant les generiques."""
    opts = set(re.findall(r"--[a-z][a-z0-9-]*", aide))
    opts.discard("--help")
    opts.discard("--aide")
    opts.discard("--version")
    return opts


def flags_du_modele(modele):
    """Extrait les flags en dur du modele (ex: --agent) et les placeholders {cle}."""
    flags = set(re.findall(r"--[a-z][a-z0-9-]*", modele))
    placeholders = set(re.findall(r"\{([a-z_0-9]+)\}", modele))
    return flags, placeholders


def lancer_aide(interpreteur, script):
    """Lance le script avec --aide puis --help. Retourne (aide, err, reconnue)."""
    chemin = os.path.join(RACINE, script)
    if not os.path.isfile(chemin):
        return None, "SCRIPT ABSENT: %s" % script, False
    for flag in ("--aide", "--help"):
        try:
            cmd = [interpreteur, chemin, flag]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
            sortie = (r.stdout or "") + (r.stderr or "")
            reconnue = ("Option inconnue" not in sortie
                        and "unrecognized arguments" not in sortie
                        and ("usage" in sortie.lower() or "Options" in sortie or "--" in sortie))
            if reconnue:
                return sortie, None, True
        except subprocess.TimeoutExpired:
            return None, "TIMEOUT (interactif ?)", False
        except OSError as e:
            return None, "OSERROR: %s" % e, False
    return None, "PAS D AIDE RECONNUE (--aide et --help rejetes ou sortie vide)", False


def analyser_combos():
    """GARDE-FOU v0.1.1 : verifie les cles des cases generateur des definitions-
    combo contre le catalogue. Retourne (problemes, nb_combos)."""
    with io.open(os.path.join(RACINE, CATALOGUE), encoding="utf-8") as fh:
        cat = json.load(fh)
    commandes = {e["nom"]: e for e in cat["commandes"]}
    probleme = []
    nb_combos = 0
    for p in sorted(glob.glob(os.path.join(RACINE, COMBOS_GLOBE))):
        nb_combos += 1
        try:
            with io.open(p, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError) as exc:
            probleme.append((os.path.basename(os.path.dirname(p)), "?", "JSON INVALIDE: %s" % exc))
            continue
        nom = d.get("combo", {}).get("nom", "?")
        for cid, case in d.get("cases", {}).items():
            if case.get("type") != "generateur":
                continue
            cible = case.get("catalogue")
            entrees = case.get("entrees") or {}
            if cible not in commandes:
                probleme.append((nom, cid, "catalogue '%s' absent du catalogue de commandes" % cible))
                continue
            parametres = commandes[cible].get("parametres", [])
            cles_cat = [pp.get("cle") for pp in parametres]
            oblig = [pp.get("cle") for pp in parametres if pp.get("obligatoire")]
            inconnues = sorted(set(entrees.keys()) - set(cles_cat))
            for cle in inconnues:
                probleme.append((nom, cid, "cle '%s' hors catalogue (attendu: %s)" % (cle, ", ".join(cles_cat))))
            manquantes = sorted(set(oblig) - set(entrees.keys()))
            for cle in manquantes:
                probleme.append((nom, cid, "parametre obligatoire '%s' manquant" % cle))
    return probleme, nb_combos


def analyser():
    with io.open(os.path.join(RACINE, CATALOGUE), encoding="utf-8") as fh:
        cat = json.load(fh)
    commandes = cat["commandes"]
    resultats = {"conformes": [], "decalages": [], "non_testables": [], "alertes": []}
    for e in commandes:
        nom = e.get("nom", "?")
        modele = e.get("modele", "")
        script = e.get("script", "")
        interpreteur = e.get("interpreteur", "python3")
        placeholders_cat = set(p["cle"] for p in e.get("parametres", []) if p.get("obligatoire"))
        placeholders_modele = set(re.findall(r"\{([a-z_0-9]+)\}", modele))
        manquants_oblig = sorted(placeholders_cat - placeholders_modele)
        if manquants_oblig:
            resultats["alertes"].append((nom, "placeholder obligatoire absent du modele: %s" % manquants_oblig))
        aide, err, reconnue = lancer_aide(interpreteur, script) if script else (None, "PAS DE SCRIPT", False)
        if err or not reconnue:
            resultats["non_testables"].append((nom, err or "AIDE NON RECONNUE", script))
            continue
        options_reelles = extraire_options(aide)
        flags_modele, _ = flags_du_modele(modele)
        manquants = sorted(f for f in flags_modele if f not in options_reelles)
        if manquants:
            md_chemin = os.path.join(RACINE, os.path.dirname(script), os.path.basename(os.path.dirname(script)) + ".md")
            md_ok = os.path.isfile(md_chemin)
            resultats["decalages"].append((nom, modele, manquants, options_reelles, script, md_ok))
        else:
            resultats["conformes"].append((nom, script))
    return resultats


def formater(resultats, total, problemes_combos, nb_combos):
    L = []
    L.append("# Scan Systematique du Catalogue vs Interfaces Reelles")
    L.append("")
    L.append("**Date** : %s | **Catalogue** : v%s | **Entrees** : %d" % (
        datetime.now().strftime("%Y-%m-%d %H:%M"), "?", total))
    L.append("")
    L.append("## COMBOS (garde-fou v0.1.1 : cles des cases generateur vs catalogue)")
    L.append("")
    L.append("| Combos scannes | %d |" % nb_combos)
    L.append("| Problemes de cles | %d |" % len(problemes_combos))
    L.append("")
    if problemes_combos:
        for nom, cid, msg in problemes_combos:
            L.append("- **%s** [%s] : %s" % (nom, cid, msg))
        L.append("")
    else:
        L.append("Aucun probleme de cles detecte (toutes les entrees correspondent au catalogue).")
        L.append("")
    L.append("")
    nb = len(resultats["conformes"])
    nb_dec = len(resultats["decalages"])
    nb_nt = len(resultats["non_testables"])
    L.append("## Synthese")
    L.append("")
    L.append("| Classe | Nombre |")
    L.append("|---|---|")
    L.append("| CONFORME | %d |" % nb)
    L.append("| DECALAGE | %d |" % nb_dec)
    L.append("| NON TESTABLE | %d |" % nb_nt)
    L.append("")
    L.append("## DECALAGES (%d)" % nb_dec)
    L.append("")
    if resultats["decalages"]:
        for nom, modele, manquants, options, script, md_ok in resultats["decalages"]:
            L.append("- **%s** : modele `%s` | flags absents de l aide: %s" % (nom, modele, manquants))
            L.append("  - outil: %s | .md present: %s" % (script, "OUI" if md_ok else "NON"))
            L.append("  - options reelles: %s" % sorted(options))
            L.append("")
    else:
        L.append("Aucun decalage detecte.")
        L.append("")
    L.append("## NON TESTABLES (%d)" % nb_nt)
    L.append("")
    if resultats["non_testables"]:
        for nom, raison, script in resultats["non_testables"]:
            L.append("- **%s** : %s (%s)" % (nom, raison, script))
        L.append("")
    else:
        L.append("Aucun non testable.")
        L.append("")
    L.append("## Alertes (placeholder obligatoire absent du modele)")
    L.append("")
    if resultats["alertes"]:
        for nom, msg in resultats["alertes"]:
            L.append("- **%s** : %s" % (nom, msg))
        L.append("")
    else:
        L.append("Aucune alerte.")
        L.append("")
    L.append("## Conformes (%d)" % nb)
    L.append("")
    for nom, script in sorted(resultats["conformes"]):
        L.append("- %s" % nom)
    L.append("")
    return "\n".join(L)


def main(argv):
    sortie = None
    for a in argv:
        if a in ("--aide", "--help", "-h"):
            print(__doc__)
            return 0
        if a == "--version":
            print("detecter-decalages-catalogue v%s (prepare)" % VERSION)
            return 0
        if a == "--sortie":
            continue
        if a.startswith("--sortie="):
            sortie = a.split("=", 1)[1]
        elif sortie is None and a.startswith("--"):
            # prochain argument = valeur de --sortie
            pass
    if "--sortie" in argv:
        idx = argv.index("--sortie")
        if idx + 1 < len(argv):
            sortie = argv[idx + 1]
    if sortie is None:
        sortie = "rapport-detecter-decalages-catalogue-%s.md" % datetime.now().strftime("%Y-%m-%d")
    resultats = analyser()
    problemes_combos, nb_combos = analyser_combos()
    rapport = formater(resultats, len(resultats["conformes"]) + len(resultats["decalages"]) + len(resultats["non_testables"]),
                       problemes_combos, nb_combos)
    with io.open(sortie, "w", encoding="utf-8", newline="") as fh:
        fh.write(rapport)
    print("RAPPORT ECRIT: %s" % os.path.abspath(sortie))
    print("SYNTHESE: %d conformes / %d decalages / %d non testables / %d alertes / COMBOS: %d scannes, %d problemes" % (
        len(resultats["conformes"]), len(resultats["decalages"]),
        len(resultats["non_testables"]), len(resultats["alertes"]),
        nb_combos, len(problemes_combos)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
