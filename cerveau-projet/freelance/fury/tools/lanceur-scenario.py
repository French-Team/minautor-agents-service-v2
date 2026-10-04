#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: fury
#   commun: false
"""
lanceur-scenario.py

Combo de FURY (temps 1-2-3) : declenche un round reel maillon par maillon
via jarvis.py envoyer --activer, collecte les traces, et produit un
rapport machine-lisible : maillons ATTENDUS vs OBSERVES, verdict par
maillon.

LIMITES HONNETES (V1-V4) :
- l outil verifie la PARTIE MECANIQUE : routage des messages (--activer)
  et mises a jour du bloc session AGENTS.md ;
- l INCARNATION LLM de chaque agent (lecture de fiche, travail reel) n est
  pas simulable par script : elle se verifie par les TRACES, jamais ici.

Usage :
  python3 lanceur-scenario.py --scenario <fichier.json>
  python3 lanceur-scenario.py --exemple     (genere un fichier exemple)

Format scenario JSON :
{
  "nom": "mini-round",
  "session": "session-llm-N",
  "maillons": [
    {"de": "stark", "vers": "jarvis"},
    {"de": "jarvis", "vers": "stark"}
  ]
}

Proprietaire : Forge (pour Fury)
Version : 0.1.0
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

VERSION = "0.1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import sys as _sys
_sys.path.insert(0, os.path.join(BASE_DIR, "..", "..",
                                 "tools-commun", "os_path", "fonctions"))
from racine import trouver_racine
RACINE = trouver_racine(__file__)
JARVIS = os.path.join(RACINE, "cerveau-projet", "freelance",
                      "tools-commun", "jarvis", "jarvis.py")
AGENTS_MD = os.path.join(RACINE, "AGENTS.md")


def nom_agent_actif(session):
    """Lire le champ Nom Agent du bloc session dans AGENTS.md."""
    try:
        contenu = open(AGENTS_MD, encoding="utf-8").read()
    except OSError:
        return "?"
    marqueur = f"### Session : {session}"
    i = contenu.find(marqueur)
    if i < 0:
        return "?"
    fin = contenu.find("### Session", i + len(marqueur))
    bloc = contenu[i:fin if fin > 0 else None]
    for ligne in bloc.splitlines():
        if "**Nom Agent**" in ligne:
            parties = [p.strip() for p in ligne.split("|")]
            for j, p in enumerate(parties):
                if p == "**Nom Agent**" and j + 1 < len(parties):
                    return parties[j + 1]
    return "?"


def executer_maillon(de, vers, session, index, type_intervention="R"):
    """Temps 2 : declencher UN maillon du round et collecter les traces."""
    avant = nom_agent_actif(session)
    p = subprocess.run(
        [sys.executable, JARVIS, "envoyer",
         "--de", de, "--vers", vers,
         "--priorite", "3",
         "--objet", f"SCENARIO-TEST maillon {index}: {de}->{vers}",
         "--corps", "message genere automatiquement par lanceur-scenario",
         "--session", session, "--activer", "--type", type_intervention],
        capture_output=True, text=True, cwd=RACINE)
    apres = nom_agent_actif(session)
    id_message = ""
    for ligne in p.stdout.splitlines():
        if ligne.strip().startswith("ID:"):
            id_message = ligne.split("ID:")[1].strip()
    return {
        "maillon": f"{index}. {de} -> {vers}",
        "type": type_intervention,
        "rc": p.returncode,
        "id_message": id_message,
        "agent_avant": avant,
        "agent_apres": apres,
        "verdict": "PASSE" if p.returncode == 0 and apres.lower() == vers
        else "ECHOUE",
        "preuve": f"bloc session: {avant} -> {apres} ; rc={p.returncode}",
    }


def lancer(scenario_path):
    try:
        scenario = json.load(open(scenario_path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {"statut": "ERREUR", "reponse": f"scenario invalide: {e}",
                "date": datetime.now().isoformat(timespec="seconds")}
    nom = scenario.get("nom", "scenario")
    session = scenario.get("session", "")
    if not session:
        return {"statut": "ERREUR", "reponse": "session obligatoire",
                "date": datetime.now().isoformat(timespec="seconds")}
    resultats = []
    for k, m in enumerate(scenario.get("maillons", []), 1):
        resultats.append(executer_maillon(m["de"], m["vers"], session, k,
                                          m.get("type", "R")))
    echoues = [r["maillon"] for r in resultats if r["verdict"] != "PASSE"]
    return {
        "combo": "lanceur-scenario", "version": VERSION,
        "statut": "PASSE" if not echoues else "ECHOUE",
        "scenario": nom, "session": session,
        "maillons_attendus": [f"{m['de']} -> {m['vers']}"
                              for m in scenario.get("maillons", [])],
        "resultats": resultats,
        "limite": ("verification MECANIQUE uniquement (routage + bloc "
                   "session) ; l incarnation LLM se verifie par les traces"),
        "date": datetime.now().isoformat(timespec="seconds"),
    }


def generer_exemple():
    exemple = {
        "nom": "mini-round-exemple",
        "session": "session-llm-2",
        "maillons": [
            {"de": "stark", "vers": "jarvis"},
            {"de": "jarvis", "vers": "stark"},
        ],
    }
    chemin = os.path.join(BASE_DIR, "scenario-exemple.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(exemple, f, ensure_ascii=False, indent=2)
    print(chemin)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Lanceur de scenarios Fury")
    parser.add_argument("--scenario", help="fichier scenario JSON")
    parser.add_argument("--exemple", action="store_true",
                        help="generer un fichier scenario exemple")
    args = parser.parse_args()
    if args.exemple:
        return generer_exemple()
    if not args.scenario:
        parser.print_help()
        return 1
    rapport = lancer(args.scenario)
    print(json.dumps(rapport, ensure_ascii=True, indent=2))
    return 0 if rapport.get("statut") == "PASSE" else 1


if __name__ == "__main__":
    sys.exit(main())
