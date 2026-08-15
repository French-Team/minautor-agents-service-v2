#!/usr/bin/env python3
# -*- coding: ascii -*-
# proteger-verrou-marbre.py
#
# VERROU DU MARBRE : verifie l integrite des zones protegees du noyau
# (Constitution + cases critiques des cartes). Toute divergence entre le
# contenu reel et l empreinte enregistree (marbre.json) est une VIOLATION.
#
# Le marbre est le principe "graver dans le marbre" : certaines regles et
# cases sont immuables et ne peuvent etre modifiees SANS passer par le
# protocole de securite (protocole-securite-marbre.md) qui exige une
# autorisation explicite de l UTILISATEUR (via proteger-modifier-marbre).
# Ce verrou s applique AVANT l action (les outils du noyau l appellent
# avant d ecrire) et APRES (garde-fou test-057 dans la non-regression).
#
# Usage :
#   python3 proteger-verrou-marbre.py --tous
#   python3 proteger-verrou-marbre.py --zone <nom>
#   python3 proteger-verrou-marbre.py --agent <nom>
#   python3 proteger-verrou-marbre.py --empreinte <nom>   (hash actuel, lecture seule)
#   python3 proteger-verrou-marbre.py --liste
#
# Options :
#   --tous          : verifier toutes les zones du manifeste
#   --zone <nom>    : verifier une zone precise
#   --agent <nom>   : verifier les zones d un agent (prefixe <agent>.)
#   --empreinte <nom> : afficher l empreinte actuelle d une zone (lecture seule)
#   --liste         : lister les zones protegees et leur raison
#   --verbose       : detail du verdict
#   --version
#
# Codes de sortie :
#   0 : OK - toutes les zones demandees sont conformes (marbre intact)
#   1 : BLOQUE - au moins une zone diverge (marbre brise)
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
import argparse
import hashlib
import io
import json
import os
import sys

VERSION = "0.1.0"


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


def normaliser(texte):
    """Normaliser pour une empreinte stable (LF, pas d espace en fin de ligne)."""
    texte = texte.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(l.rstrip() for l in texte.split("\n"))


def sha(texte):
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def empreinte_fichier(chemin):
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
        return sha(normaliser(fh.read()))


def empreinte_marqueurs(chemin, debut, fin):
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
        contenu = normaliser(fh.read())
    d = contenu.find(debut)
    f = contenu.find(fin)
    if d == -1 or f == -1 or f <= d:
        raise ValueError("marqueurs introuvables dans %s" % chemin)
    zone = contenu[d + len(debut):f]
    return sha(zone)


def empreinte_case(chemin, cid):
    with io.open(chemin, "r", encoding="utf-8") as fh:
        donnees = json.load(fh)
    case = donnees.get("cases", {}).get(cid)
    if case is None:
        raise ValueError("case %s introuvable dans %s" % (cid, chemin))
    return sha(json.dumps(case, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


def empreinte_zone(zone, racine):
    fichier = zone["fichier"]
    chemin = os.path.join(racine, fichier) if not os.path.isabs(fichier) else fichier
    typ = zone.get("type", "fichier")
    if typ == "case":
        return empreinte_case(chemin, zone["cid"])
    if typ == "marqueurs":
        return empreinte_marqueurs(chemin, zone["marqueur_debut"], zone["marqueur_fin"])
    return empreinte_fichier(chemin)


def charger_manifeste(racine):
    chemin = chemin_manifeste(racine)
    if not os.path.isfile(chemin):
        sys.exit("[BLOQUE] Manifeste du marbre introuvable : %s (le marbre doit exister)" % chemin)
    with io.open(chemin, "r", encoding="utf-8") as fh:
        return json.load(fh)


def verifier(manifeste, racine, nom):
    zone = manifeste["zones"].get(nom)
    if zone is None:
        return None
    try:
        actuel = empreinte_zone(zone, racine)
    except (ValueError, IOError) as e:
        return ("IMPRECISABLE", "erreur: %s" % e, zone.get("empreinte", ""))
    if actuel == zone.get("empreinte"):
        return ("OK", "", zone.get("empreinte", ""))
    return ("DIVERGE", actuel, zone.get("empreinte", ""))


def main():
    parser = argparse.ArgumentParser(description="Verrou du marbre : integrite des zones protegees")
    parser.add_argument("--tous", action="store_true", help="Verifier toutes les zones")
    parser.add_argument("--zone", type=str, default="", help="Verifier une zone (nom exact)")
    parser.add_argument("--agent", type=str, default="", help="Verifier les zones d un agent (prefixe <agent>.)")
    parser.add_argument("--empreinte", type=str, default="", help="Afficher l empreinte actuelle d une zone")
    parser.add_argument("--liste", action="store_true", help="Lister les zones protegees")
    parser.add_argument("--verbose", action="store_true", help="Detail du verdict")
    parser.add_argument("--version", action="version", version="proteger-verrou-marbre v%s" % VERSION)
    args = parser.parse_args()

    racine = racine_projet()
    manifeste = charger_manifeste(racine)
    zones = manifeste["zones"]

    if args.liste:
        for nom in sorted(zones):
            z = zones[nom]
            print("%-28s %-10s %s" % (nom, z.get("type", "fichier"), z.get("raison", "")))
        return 0

    if args.empreinte:
        z = zones.get(args.empreinte)
        if z is None:
            print("[ERREUR] Zone inconnue : %s" % args.empreinte)
            return 2
        try:
            print(empreinte_zone(z, racine))
        except (ValueError, IOError) as e:
            print("[ERREUR] %s" % e)
            return 2
        return 0

    if args.zone:
        noms = [args.zone]
    elif args.agent:
        prefixe = args.agent + "."
        noms = sorted(n for n in zones if n.startswith(prefixe))
    elif args.tous:
        noms = sorted(zones)
    else:
        parser.print_help()
        return 2

    divergences = []
    for nom in noms:
        verdict = verifier(manifeste, racine, nom)
        if verdict is None:
            print("[AVERTISSEMENT] Zone inconnue : %s" % nom)
            continue
        etat, detail, attendu = verdict
        if etat == "OK":
            if args.verbose:
                print("[OK] %s : conforme" % nom)
        else:
            divergences.append((nom, etat, detail))
            print("[BLOQUE] %s : %s" % (nom, etat))
            if args.verbose:
                print("   attendu  : %s" % attendu)
                print("   actuel   : %s" % detail)

    if divergences:
        print("")
        print("== MARBRE BRISE : %d zone(s) modifiee(s) sans protocole ==" % len(divergences))
        print("Toute modification du marbre exige :")
        print("  proteger-modifier-marbre --zone <nom> --raison <...> --autorisation UTILISATEUR")
        print("Protocole : cerveau-projet/agents/regles-immuables/general/protocole-securite-marbre.md")
        return 1
    if args.verbose:
        print("Marbre intact : %d zone(s) conforme(s)" % len(noms))
    return 0


if __name__ == "__main__":
    sys.exit(main())
