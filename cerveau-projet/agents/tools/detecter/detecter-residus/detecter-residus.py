#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-residus.py
#
# Detecte les RESIDUS du workspace, compartimente par ZONE (demande
# utilisateur 2026-08-13, agent Hygie) :
#   - zone cerveau-projet : scanne le dossier cerveau-projet/
#   - zone workspace      : scanne la racine du workspace (futur dossier
#                           workspace/ + racine du projet)
#   - zone tous           : les deux zones
#
# Types de residus detectes :
#   TEMP        : scripts/dossiers temporaires (tmp-*/.zz-*/.tmp-*) a la
#                 racine (fichiers et dossiers)
#   VERSION     : fichiers de version semver a la racine (0.2.1, v0.2.6...)
#   SAUVEGARDE  : fichiers de sauvegarde (*.bak, *~, *.orig)
#   RAPPORT_EGARE : fichiers de rapport/audit/controle egare a la racine ou
#                 hors des dossiers de rapport des agents
#   CACHE       : dossiers __pycache__ et fichiers .pyc (residus de compilation)
#
# Sortie : par zone, liste des residus classes par type + compteur + verdict
# (0 residu = PROPRE, sinon RESIDUS DETECTES avec nombre). Resume global si
# plusieurs zones.
#
# Options :
#   --zone <cerveau-projet|workspace|tous>  Zone a scanner (defaut: tous)
#   --detail       Detail complet (type de chaque residu)
#   --rapport <fichier>  Ecrit le rapport markdown
#   --verbose      Affiche les details
#   --version      Affiche la version
#
# Usage:
#   python3 detecter-residus.py --tous
#   python3 detecter-residus.py --zone cerveau-projet --detail
#   python3 detecter-residus.py --rapport rapport-residus.md
#
# Version : 0.1.1
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
import json
import os
import re
import sys
from datetime import datetime

VERSION = "0.1.2"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


PATTERN_SEMVER = re.compile(r"^v?\d+\.\d+(\.\d+)?([._-].*)?$")


def est_fichier_temp(nom):
    base = os.path.basename(nom)
    return base.startswith(".tmp-") or base.startswith(".zz-")


def est_dossier_temp(nom):
    base = os.path.basename(nom)
    return base.startswith("tmp-") or base.startswith(".tmp-") or base.startswith(".zz-")


def est_version_racine(nom):
    base = os.path.basename(nom)
    racine = os.path.splitext(base)[0]
    return bool(PATTERN_SEMVER.match(racine)) and len(racine) < 12


def est_sauvegarde(nom):
    return nom.endswith(".bak") or nom.endswith("~") or nom.endswith(".orig") or nom.endswith(".backup")


def est_rapport_egare(racine, chemin_rel, nom):
    """Rapport/audit/controle egare a la racine du workspace (hors dossier
    de rapport d un agent) ou a la racine du projet.

    v0.1.2 : la legitimite est decidee par le DOSSIER PARENT IMMEDIAT
    (rapports/controles/...), pas par le premier segment du chemin : dans
    la zone cerveau-projet les rapports des agents vivent dans
    agents/*/rapports/ et agents/*/controles/ et sont LEGITIMES."""
    base = os.path.basename(nom)
    if not (base.startswith("rapport-") or base.startswith("rapports-")
            or base.startswith("audit-") or base.startswith("controle-")):
        return False
    if not nom.endswith((".md", ".txt", ".json")):
        return False
    # a la racine du projet (rel = nom) -> egare
    if os.sep not in chemin_rel:
        return True
    # dans un dossier de rapport legitime (parent immediat) -> non
    parent = os.path.basename(os.path.dirname(chemin_rel))
    if parent in ("rapports", "controles", "rapport", "controle"):
        return False
    return True


def scanner_zone(racine, zone):
    """Detecte les residus d une zone. Retourne {type: [chemins]}.

    COMPARTIMENTATION STRICTE (v0.1.1, mission utilisateur 2026-08-13) :
      - zone cerveau-projet : scanne UNIQUEMENT cerveau-projet/
      - zone workspace      : scanne la racine + le dossier workspace/ mais
        JAMAIS cerveau-projet/ (ni caches, ni residus internes)
    Chaque zone ne voit que SES residus : aucun chevauchement, aucun double
    comptage entre les deux zones."""
    resultats = {}
    EXCLUS = {".git", "__pycache__"}

    def ajouter(type_res, rel):
        # v0.1.2 : deduplication par chemin - un fichier de la racine est
        # traite une fois au niveau racine ET une fois par os.walk (dirpath
        # == racine) : sans garde, double comptage des residus de la racine.
        if rel in resultats.get(type_res, []):
            return
        resultats.setdefault(type_res, []).append(rel)

    def est_cache_dir(nom):
        return nom == "__pycache__" or nom.endswith(".pyc")

    if zone == "cerveau-projet":
        base = os.path.join(racine, "cerveau-projet")
        if not os.path.isdir(base):
            return resultats
        # scan complet de cerveau-projet : fichier par fichier
        for dirpath, dossiers, fichiers in os.walk(base):
            dossiers[:] = [d for d in dossiers
                           if not est_dossier_temp(d) and d not in EXCLUS]
            for nom in fichiers:
                chemin = os.path.join(dirpath, nom)
                rel = os.path.relpath(chemin, racine)
                if est_fichier_temp(nom):
                    ajouter("TEMP", rel)
                elif est_sauvegarde(nom):
                    ajouter("SAUVEGARDE", rel)
                elif est_rapport_egare(racine, rel, nom):
                    ajouter("RAPPORT_EGARE", rel)
                elif est_cache_dir(nom):
                    ajouter("CACHE", rel)
            if "__pycache__" in dossiers:
                rel = os.path.relpath(os.path.join(dirpath, "__pycache__"), racine)
                ajouter("CACHE", rel)
        return resultats

    # --- zone workspace (ou la partie workspace de "tous") : la racine ---
    #     SAUF cerveau-projet/ (jamais scanne ici) et les dossiers temp
    #     de mission (le dossier parent est deja signale comme TEMP).
    # 1. Niveau racine : fichiers et dossiers directs
    try:
        noms = sorted(os.listdir(racine))
    except OSError:
        return resultats
    for nom in noms:
        chemin = os.path.join(racine, nom)
        rel = os.path.relpath(chemin, racine)
        if os.path.isdir(chemin):
            if est_dossier_temp(nom):
                ajouter("TEMP", rel)
        else:
            if est_fichier_temp(nom):
                ajouter("TEMP", rel)
            elif est_version_racine(nom):
                ajouter("VERSION", rel)
            elif est_sauvegarde(nom):
                ajouter("SAUVEGARDE", rel)
            elif est_rapport_egare(racine, rel, nom):
                ajouter("RAPPORT_EGARE", rel)
            elif est_cache_dir(nom):
                ajouter("CACHE", rel)

    # 2. Scan recursif : workspace/ (residus internes) + caches de la racine
    #    (__pycache__/.pyc) - cerveau-projet/ et .git/ JAMAIS traverses.
    for dirpath, dossiers, fichiers in os.walk(racine):
        # prune : jamais dans cerveau-projet, .git, les dossiers temp de
        # mission (signales comme TEMP au niveau racine), les caches
        dossiers[:] = [d for d in dossiers
                       if d != "cerveau-projet"
                       and d != ".git"
                       and not est_dossier_temp(d)
                       and d != "__pycache__"]
        for nom in fichiers:
            chemin = os.path.join(dirpath, nom)
            rel = os.path.relpath(chemin, racine)
            if est_fichier_temp(nom):
                ajouter("TEMP", rel)
            elif est_version_racine(nom) and os.sep in rel:
                ajouter("VERSION", rel)
            elif est_sauvegarde(nom):
                ajouter("SAUVEGARDE", rel)
            elif est_rapport_egare(racine, rel, nom):
                ajouter("RAPPORT_EGARE", rel)
            elif est_cache_dir(nom):
                ajouter("CACHE", rel)
        if "__pycache__" in dossiers:
            rel = os.path.relpath(os.path.join(dirpath, "__pycache__"), racine)
            ajouter("CACHE", rel)

    return resultats


def main():
    parser = argparse.ArgumentParser(
        description="Detecte les residus du workspace, compartimente par zone")
    parser.add_argument("--zone", choices=["cerveau-projet", "workspace", "tous"],
                        default="tous", help="Zone a scanner (defaut: tous)")
    parser.add_argument("--tous", action="store_true",
                        help="Scanner les deux zones (alias de --zone tous)")
    parser.add_argument("--sans-cache", action="store_true",
                        help="Ignorer les caches de compilation (__pycache__/.pyc) - les caches se regenerent a chaque execution")
    parser.add_argument("--detail", action="store_true", help="Detail par type")
    parser.add_argument("--rapport", type=str, default="", help="Chemin du rapport markdown")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version",
                        version="detecter-residus v%s" % VERSION)
    args = parser.parse_args()

    racine = racine_projet()
    zone_choisie = "tous" if args.tous else args.zone
    zones = ["cerveau-projet", "workspace"] if zone_choisie == "tous" else [zone_choisie]

    print(_couleur("=== detecter-residus v%s : scan des residus par zone ===" % VERSION, "bleu"))
    print("Racine : %s" % racine)
    print("Date   : %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")

    total = 0
    resume = []
    details_par_zone = {}

    for zone in zones:
        resultats = scanner_zone(racine, zone)
        if args.sans_cache:
            resultats.pop("CACHE", None)
        nb = sum(len(v) for v in resultats.values())
        total += nb
        details_par_zone[zone] = resultats
        print(_couleur("--- Zone : %s ---" % zone, "bleu"))
        if nb == 0:
            print("  [OK] Aucun residu detecte")
        else:
            print("  %d residu(s) detecte(s)" % nb)
            for type_res in sorted(resultats):
                print("    - %s (%d) : %s" % (
                    type_res, len(resultats[type_res]),
                    "; ".join(resultats[type_res][:5])))
                if len(resultats[type_res]) > 5:
                    print("      ... (%d autres)" % (len(resultats[type_res]) - 5))
        resume.append((zone, nb))
        print("")

    print(_couleur("=== RESUME ===", "bleu"))
    for zone, nb in resume:
        print("  %-14s : %d residu(s)" % (zone, nb))
    verdict = "PROPRE" if total == 0 else "RESIDUS DETECTES"
    print("")
    print(_couleur("  Verdict : %s (%d residu(s) au total)" % (verdict, total),
                   "vert" if total == 0 else "rouge"))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport : detection des residus\n\n")
            fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("Verdict : %s (%d residu(s))\n\n" % (verdict, total))
            for zone, resultats in details_par_zone.items():
                fh.write("## Zone : %s\n\n" % zone)
                if not any(resultats.values()):
                    fh.write("Aucun residu detecte.\n\n")
                    continue
                for type_res in sorted(resultats):
                    fh.write("### %s (%d)\n\n" % (type_res, len(resultats[type_res])))
                    for rel in resultats[type_res]:
                        fh.write("- %s\n" % rel)
                    fh.write("\n")
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
