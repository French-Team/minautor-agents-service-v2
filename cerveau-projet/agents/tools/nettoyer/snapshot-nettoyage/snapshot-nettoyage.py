#!/usr/bin/env python3
# -*- coding: ascii -*-
# snapshot-nettoyage.py
#
# Outil de SNAPSHOT de l etat du workspace avant nettoyage (agent Hygie).
# Un snapshot est la PREUVE de tracabilite : il montre ce qui etait present
# (inventaire des fichiers) avant toute suppression.
#
# Sous-commandes :
#   creer     : prend un snapshot de l etat actuel du workspace (inventaire
#               des fichiers : chemin + taille + hash md5) dans le dossier
#               dedie de l agent (cerveau-projet/agents/hygie/snapshots/)
#               sous le nom snapshot-<date>.json
#   consulter : affiche le snapshot le plus recent (etat avant le dernier
#               nettoyage) - consulte a chaque nettoyage
#   rotation  : supprime les snapshots de plus de 7 jours (regle utilisateur)
#   liste     : liste les snapshots existants
#
# Options communes :
#   --version
#
# Usage:
#   python3 snapshot-nettoyage.py creer
#   python3 snapshot-nettoyage.py consulter
#   python3 snapshot-nettoyage.py rotation
#   python3 snapshot-nettoyage.py liste
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (nettoyer-).
# =============================================================================
import argparse
import hashlib
import io
import json
import os
import sys
from datetime import datetime, timedelta

VERSION = "0.1.0"
STATUT = "ebauche"
ROTATION_JOURS = 7

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


def dossier_snapshots(racine):
    d = os.path.join(racine, "cerveau-projet", "agents", "hygie", "snapshots")
    return d


def hash_fichier(chemin):
    try:
        h = hashlib.md5()
        with open(chemin, "rb") as fh:
            for bloc in iter(lambda: fh.read(65536), b""):
                h.update(bloc)
        return h.hexdigest()
    except OSError:
        return ""


def inventaire(racine):
    """Inventaire des fichiers du workspace : chemin relatif + taille + hash."""
    fichiers = []
    zones = ["cerveau-projet", ""]
    for zone in zones:
        base = os.path.join(racine, zone) if zone else racine
        if not os.path.isdir(base):
            continue
        for dirpath, dossiers, noms in os.walk(base):
            dossiers[:] = [d for d in dossiers
                           if not d.startswith("tmp-")
                           and not d.startswith(".tmp-")
                           and not d.startswith(".zz-")
                           and d != "__pycache__"]
            for nom in noms:
                if nom.endswith(".pyc"):
                    continue
                chemin = os.path.join(dirpath, nom)
                rel = os.path.relpath(chemin, racine)
                try:
                    taille = os.path.getsize(chemin)
                except OSError:
                    taille = 0
                fichiers.append({
                    "chemin": rel,
                    "taille": taille,
                    "hash": hash_fichier(chemin),
                })
    fichiers.sort(key=lambda f: f["chemin"])
    return fichiers


def lister_snapshots(dossier):
    if not os.path.isdir(dossier):
        return []
    return sorted(f for f in os.listdir(dossier)
                  if f.startswith("snapshot-") and f.endswith(".json"))


def sous_commande_creer(racine):
    dossier = dossier_snapshots(racine)
    if not os.path.isdir(dossier):
        os.makedirs(dossier)
    date = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    nom = "snapshot-%s.json" % date
    chemin = os.path.join(dossier, nom)

    fichiers = inventaire(racine)
    snap = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "zone": "tous",
        "nb_fichiers": len(fichiers),
        "rotation_jours": ROTATION_JOURS,
        "fichiers": fichiers,
        "suppressions": [],
        "verdict": "SNAPSHOT PRIS",
    }
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(snap, fh, ensure_ascii=True, indent=1)
        fh.write("\n")

    print(_couleur("=== snapshot-nettoyage : snapshot pris ===", "bleu"))
    print("  Fichier : %s" % chemin)
    print("  Date    : %s" % snap["date"])
    print("  Fichiers inventories : %d" % len(fichiers))
    print(_couleur("  Verdict : SNAPSHOT PRIS (preuve de tracabilite)", "vert"))
    return 0


def sous_commande_consulter(racine):
    dossier = dossier_snapshots(racine)
    snaps = lister_snapshots(dossier)
    print(_couleur("=== snapshot-nettoyage : consulter le snapshot precedent ===", "bleu"))
    if not snaps:
        print("  Aucun snapshot existant (premier nettoyage).")
        return 0
    dernier = snaps[-1]
    chemin = os.path.join(dossier, dernier)
    with io.open(chemin, encoding="utf-8") as fh:
        snap = json.load(fh)
    print("  Snapshot precedent : %s" % dernier)
    print("  Date               : %s" % snap.get("date", "?"))
    print("  Fichiers           : %d" % snap.get("nb_fichiers", len(snap.get("fichiers", []))))
    suppr = snap.get("suppressions", [])
    print("  Suppressions       : %d" % len(suppr))
    for s in suppr[:10]:
        print("     - %s (%s)" % (s.get("chemin", "?"), s.get("justification", "?")))
    if len(suppr) > 10:
        print("     ... (%d autres)" % (len(suppr) - 10))
    print("  Verdict precedent  : %s" % snap.get("verdict", "?"))
    return 0


def sous_commande_rotation(racine):
    dossier = dossier_snapshots(racine)
    snaps = lister_snapshots(dossier)
    seuil = datetime.now() - timedelta(days=ROTATION_JOURS)
    supprimes = []
    for nom in snaps:
        try:
            date_part = nom[len("snapshot-"):-len(".json")]
            d = datetime.strptime(date_part, "%Y-%m-%d-%H%M%S")
        except ValueError:
            continue
        if d < seuil:
            os.remove(os.path.join(dossier, nom))
            supprimes.append(nom)
    print(_couleur("=== snapshot-nettoyage : rotation %d jours ===" % ROTATION_JOURS, "bleu"))
    print("  Snapshots existants : %d" % len(snaps))
    if supprimes:
        print("  Supprimes (age > %d j) : %s" % (ROTATION_JOURS, ", ".join(supprimes)))
    else:
        print("  Aucun snapshot a supprimer (tous sous %d jours)." % ROTATION_JOURS)
    return 0


def sous_commande_liste(racine):
    dossier = dossier_snapshots(racine)
    snaps = lister_snapshots(dossier)
    print(_couleur("=== snapshot-nettoyage : liste des snapshots ===", "bleu"))
    if not snaps:
        print("  Aucun snapshot.")
        return 0
    for nom in snaps:
        chemin = os.path.join(dossier, nom)
        try:
            taille = os.path.getsize(chemin)
        except OSError:
            taille = 0
        print("  - %s (%d octets)" % (nom, taille))
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Snapshot de l etat du workspace avant nettoyage (agent Hygie)")
    parser.add_argument("commande", choices=["creer", "consulter", "rotation", "liste"],
                        help="Sous-commande a executer")
    parser.add_argument("--version", action="version",
                        version="snapshot-nettoyage v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = racine_projet()

    if args.commande == "creer":
        return sous_commande_creer(racine)
    if args.commande == "consulter":
        return sous_commande_consulter(racine)
    if args.commande == "rotation":
        return sous_commande_rotation(racine)
    return sous_commande_liste(racine)


if __name__ == "__main__":
    sys.exit(main())
