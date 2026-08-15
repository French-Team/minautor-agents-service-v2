#!/usr/bin/env python3
# -*- coding: ascii -*-
# proteger-modifier-marbre.py
#
# MODIFICATION DU MARBRE : le SEUL outil autorise a mettre a jour les
# empreintes du manifeste marbre.json. Exige une AUTORISATION EXPLICITE
# de l utilisateur (--autorisation). Sans elle, aucune modification n est
# possible : le marbre est immuable pour les agents.
#
# Flux (protocole-securite-marbre.md) :
#   1. Un agent a besoin de modifier une zone protegee -> il s ARRETE
#   2. Le GARDIEN propose la modification (raison + impact)
#   3. L UTILISATEUR valide explicitement
#   4. Le gardien execute :
#      proteger-modifier-marbre --zone <nom> --raison <...> --autorisation <UTILISATEUR>
#   5. L empreinte est mise a jour + journalisee dans marbre-log.jsonl
#
# Usage :
#   python3 proteger-modifier-marbre.py --zone <nom> --raison <texte> --autorisation <cle>
#   python3 proteger-modifier-marbre.py --log                     (historique des modifications)
#
# Options :
#   --zone <nom>        : zone a re-empreinter (obligatoire avec --raison)
#   --raison <texte>    : justification de la modification (obligatoire)
#   --autorisation <cle> : preuve d autorisation de l utilisateur (OBLIGATOIRE)
#   --log               : afficher l historique des modifications du marbre
#   --version
#
# Codes de sortie :
#   0 : OK - marbre mis a jour et journalise
#   1 : BLOQUE - autorisation absente ou zone inconnue
#   2 : erreur d utilisation
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (proteger-).
# =============================================================================
"""
proteger-modifier-marbre.py
proteger-modifier-marbre

Usage:
  proteger-modifier-marbre.py [OPTIONS]
"""

import argparse
import datetime
import importlib.util
import io
import json
import os
import sys

VERSION = "0.1.1"


def empreinte_fichier_lock(chemin):
    """Empreinte SHA-256 normalisee du FICHIER CARTE COMPLET (LF + rstrip),
    strictement identique a celle d editer-parcours (cartes-lock.json).
    La porte du marbre modifie une case -> la carte complete change -> il
    faut resynchroniser l empreinte du fichier dans cartes-lock.json, sinon
    l anti-contournement (barrage n3) bloque toute modification ulterieure
    (lecon 2026-08-16 : reconstruction c10 sans resync lock).
    """
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
        texte = fh.read().replace("\r\n", "\n").replace("\r", "\n")
    texte = "\n".join(l.rstrip() for l in texte.split("\n"))
    import hashlib
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def chemin_lock_cartes(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "regles-immuables",
                        "marbre", "cartes-lock.json")


def resynchroniser_lock_carte(racine, zone):
    """Apres mise a jour d une zone CASE de carte (marbre), resynchronise
    l empreinte du fichier carte complet dans cartes-lock.json. Les zones
    non-case (fichier entier, marqueurs, regles) ne touchent pas une carte :
    rien a synchroniser.
    """
    if zone.get("type") != "case":
        return 0
    chemin_lock = chemin_lock_cartes(racine)
    if not os.path.isfile(chemin_lock):
        return 0
    relatif = zone["fichier"].replace("\\", "/")
    chemin_carte = os.path.join(racine, relatif)
    if not os.path.isfile(chemin_carte):
        return 0
    try:
        with io.open(chemin_lock, "r", encoding="utf-8") as fh:
            lock = json.load(fh)
    except (ValueError, IOError):
        return 0
    lock.setdefault("cartes", {})[relatif] = empreinte_fichier_lock(chemin_carte)
    with io.open(chemin_lock, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(lock, fh, ensure_ascii=True, indent=1)
        fh.write("\n")
    print("    resynchronise cartes-lock.json : %s" % relatif)
    return 1


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(d, "AGENTS.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            sys.exit("racine projet introuvable (AGENTS.md introuvable en remontant)")
        d = parent


def chemin_manifeste(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "regles-immuables",
                        "marbre", "marbre.json")


def chemin_log(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "regles-immuables",
                        "marbre", "marbre-log.jsonl")


def charger_verrou():
    """Importer les fonctions de calcul d empreinte depuis proteger-verrou-marbre."""
    racine = racine_projet()
    chemin = os.path.join(racine, "cerveau-projet", "agents", "tools", "proteger",
                          "proteger-verrou-marbre", "proteger-verrou-marbre.py")
    spec = importlib.util.spec_from_file_location("proteger_verrou_marbre", chemin)
    if spec is None or spec.loader is None:
        sys.exit("[ERREUR] Outil proteger-verrou-marbre introuvable : %s" % chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def afficher_log(racine):
    chemin = chemin_log(racine)
    if not os.path.isfile(chemin):
        print("Aucune modification du marbre journalisee (marbre-log.jsonl absent)")
        return 0
    lignes = []
    with io.open(chemin, "r", encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if ligne:
                try:
                    lignes.append(json.loads(ligne))
                except ValueError:
                    pass
    if not lignes:
        print("Aucune modification du marbre journalisee")
        return 0
    print("Historique des modifications du marbre (%d) :" % len(lignes))
    for entree in lignes[-20:]:
        print("  %s | %-24s | %s | autorise par: %s" % (
            entree.get("date", "?"), entree.get("zone", "?"),
            (entree.get("raison", "") or "")[:60], entree.get("autorise_par", "?")))
    return 0


def main():
    parser = argparse.ArgumentParser(description="Modification du marbre (protocole a autorisation utilisateur)")
    parser.add_argument("--zone", type=str, default="", help="Zone a re-empreinter")
    parser.add_argument("--raison", type=str, default="", help="Justification de la modification")
    parser.add_argument("--autorisation", type=str, default="", help="Preuve d autorisation de l utilisateur (OBLIGATOIRE)")
    parser.add_argument("--log", action="store_true", help="Afficher l historique des modifications")
    parser.add_argument("--version", action="version", version="proteger-modifier-marbre v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = racine_projet()

    if args.log:
        return afficher_log(racine)

    if not args.zone or not args.raison:
        parser.print_help()
        return 2

    if not args.autorisation:
        print("[BLOQUE] Autorisation utilisateur manquante : le marbre est IMMUABLE pour les agents.")
        print("  Le gardien propose, l UTILISATEUR valide, puis :")
        print("  proteger-modifier-marbre --zone %s --raison \"...\" --autorisation <cle>" % args.zone)
        return 1

    chemin = chemin_manifeste(racine)
    with io.open(chemin, "r", encoding="utf-8") as fh:
        manifeste = json.load(fh)

    zone = manifeste["zones"].get(args.zone)
    if zone is None:
        print("[ERREUR] Zone inconnue : %s" % args.zone)
        print("Zones protegees : %s" % ", ".join(sorted(manifeste["zones"])))
        return 2

    verrou = charger_verrou()
    try:
        nouvelle = verrou.empreinte_zone(zone, racine)
    except (ValueError, IOError) as e:
        print("[BLOQUE] Impossible de calculer l empreinte de la zone %s : %s" % (args.zone, e))
        return 1

    ancienne = zone.get("empreinte", "")
    if nouvelle == ancienne:
        print("[OK] Zone %s : contenu inchange (empreinte identique), rien a mettre a jour" % args.zone)
        return 0

    zone["empreinte"] = nouvelle
    zone["modifie_le"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    zone["raison_modification"] = args.raison

    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifeste, fh, ensure_ascii=True, indent=1)
        fh.write("\n")

    entree = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "zone": args.zone,
        "raison": args.raison,
        "autorise_par": args.autorisation,
        "ancienne_empreinte": ancienne,
        "nouvelle_empreinte": nouvelle,
    }
    with io.open(chemin_log(racine), "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entree, ensure_ascii=True) + "\n")

    # FIX v0.1.1 (2026-08-16, enquete Buffy) : une zone CASE de carte modifie
    # le fichier carte complet -> resynchroniser cartes-lock.json, sinon
    # l anti-contournement bloque les modifications ulterieures.
    resynchroniser_lock_carte(racine, zone)

    print("[OK] Marbre mis a jour : %s (autorisation: %s)" % (args.zone, args.autorisation))
    print("    ancienne : %s" % ancienne[:16])
    print("    nouvelle : %s" % nouvelle[:16])
    print("    journalise dans marbre-log.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
