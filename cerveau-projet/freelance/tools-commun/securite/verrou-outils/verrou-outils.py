#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
verrou-outils.py

Verrou sur les outils - securite v2. S'appelle AVANT d'utiliser un outil
ou un combo protege. Il APPLIQUE la decision du lecteur-de-carte (le
lecteur DECIDE, le verrou APPLIQUE) et trace TOUT acces dans un journal.

Actions:
  controler --agent <agent> --cible <chemin|nom> [--type outil|combo]
  lister
  aide

Proprietaire : Forge
Version : 0.1.0
Statut : actif
"""

import json
import os
import subprocess
import sys
from datetime import datetime

VERSION = "0.1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get(
    "VERROUS_DATA", os.path.join(BASE_DIR, "verrous-data.json"))
LECTEUR = os.environ.get(
    "LECTEUR_CARTE",
    os.path.join(BASE_DIR, "..", "lecteur-de-carte", "lecteur-de-carte.py"))


def charger_donnees():
    if not os.path.isfile(DATA_FILE):
        print("ERREUR: fichier de donnees introuvable: %s" % DATA_FILE)
        sys.exit(2)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (ValueError, OSError) as e:
        print("ERREUR: fichier de donnees invalide: %s" % e)
        sys.exit(2)


def normaliser(cible):
    """Chemin -> cle de verrous-data.json (separateurs /)."""
    return cible.replace("\\", "/")


def trouver_regle(donnees, cible):
    for motif, regle in donnees.get("proteges", {}).items():
        m = motif.replace("\\", "/")
        if m.endswith("*") and cible.startswith(m[:-1]):
            return motif, regle
        if m == cible:
            return motif, regle
    return None, None


def tracer(donnees, agent, cible, verdict, raison=""):
    journal = donnees.get("journal", "")
    if not journal or donnees.get("tracer", "tout") == "aucun":
        return
    if journal != "tout" and donnees.get("tracer") == "refus" and verdict == "ACCEDE":
        return
    chemin = os.path.join(BASE_DIR, journal)
    entree = {
        "date": datetime.now().isoformat(),
        "agent": agent,
        "cible": cible,
        "verdict": verdict,
        "raison": raison,
    }
    try:
        with open(chemin, "a", encoding="utf-8") as f:
            f.write(json.dumps(entree, ensure_ascii=True) + "\n")
    except OSError as e:
        print("AVERTISSEMENT: trace impossible: %s" % e)


def interroger_lecteur(agent, cible, type_cible):
    cmd = [sys.executable, LECTEUR, "verifier",
           "--agent", agent, "--cible", cible, "--type", type_cible]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode == 0


def controler(agent, cible, type_cible):
    donnees = charger_donnees()
    cible = normaliser(cible)
    motif, regle = trouver_regle(donnees, cible)

    if regle is None:
        tracer(donnees, agent, cible, "REFUSE", "cible non protegee/inconnue")
        print("REFUSE: '%s' n'est pas dans le registre des proteges" % cible)
        return 1

    # Habilitation exclusive (ex: Vision sur JARVIS)
    unique = regle.get("habilite_unique")
    if unique and agent != unique:
        tracer(donnees, agent, cible, "REFUSE",
               "habilitation exclusive: %s" % unique)
        print("REFUSE: '%s' est reserve a '%s' (exclusivite)" % (motif, unique))
        return 1

    # Liste d'habilites explicite : elle fait foi (pas de lecteur)
    habilites = regle.get("habilites")
    if habilites is not None:
        if agent in habilites:
            tracer(donnees, agent, cible, "ACCEDE", "liste d'habilites")
            print("OUVERT: acces accorde a '%s' pour '%s'" % (cible, agent))
            return 0
        tracer(donnees, agent, cible, "REFUSE", "hors liste d'habilites")
        print("REFUSE: '%s' requiert une carte specifique" % motif)
        return 1

    # Decision finale par le lecteur de carte
    # (nom sans extension : les cartes designent les outils par leur nom)
    nom_court = os.path.basename(cible)
    for ext in (".py", ".sh", ".json", ".md"):
        if nom_court.endswith(ext):
            nom_court = nom_court[: -len(ext)]
            break
    if interroger_lecteur(agent, nom_court, type_cible):
        tracer(donnees, agent, cible, "ACCEDE")
        print("OUVERT: acces accorde a '%s' pour '%s'" % (cible, agent))
        return 0
    tracer(donnees, agent, cible, "REFUSE", "carte refusee par le lecteur")
    print("REFUSE: carte refusee par le lecteur-de-carte")
    return 1


def lister():
    donnees = charger_donnees()
    print("Cibles protegees (%d):" % len(donnees.get("proteges", {})))
    for motif, regle in donnees.get("proteges", {}).items():
        extra = ""
        if regle.get("habilite_unique"):
            extra = " [EXCLUSIF: %s]" % regle["habilite_unique"]
        elif regle.get("habilites"):
            extra = " [%s]" % ", ".join(regle["habilites"])
        print("  %s (%s)%s" % (motif, regle.get("niveau", "?"), extra))
    return 0


def aide():
    print("verrou-outils v%s" % VERSION)
    print("Usage:")
    print("  verrou-outils.py controler --agent <agent> --cible <chemin|nom> "
          "[--type outil|combo]")
    print("  verrou-outils.py lister")
    print("Donnees: verrous-data.json (D15) | Journal: %s"
          % charger_donnees().get("journal", "-"))
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("aide", "--help", "-h"):
        sys.exit(aide())
    action = args[0]
    opts = {"--agent": None, "--cible": None, "--type": "outil"}
    i = 1
    while i < len(args):
        if args[i] in opts and i + 1 < len(args):
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            i += 1
    if action == "controler":
        if not opts["--agent"] or not opts["--cible"]:
            print("ERREUR: --agent et --cible obligatoires")
            sys.exit(2)
        sys.exit(controler(opts["--agent"], opts["--cible"], opts["--type"]))
    if action == "lister":
        sys.exit(lister())
    print("ERREUR: action inconnue '%s'" % action)
    sys.exit(aide())


if __name__ == "__main__":
    main()
