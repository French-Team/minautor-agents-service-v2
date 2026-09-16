#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
espion-activite-optimus.py -- File, frictions actives, verrous (M-111)

Signale : missions en attente (journal), frictions actives (bdd),
verrous BDD non liberes. L espion SIGNALE, il ne repare jamais.

Le vocabulaire des STATUTS n'est PAS recopie ici : il vient des DOMICILES des
outils concernes (bdd-frictions, bdd-modifs), la ou le schema les declare
(MO-128). Une valeur recopiee dans l'espion serait une copie de plus, que
personne ne mettrait a jour (lecons L-100/L-102).
Usage: python espion-activite-optimus.py (code 0 = RAS, 1 = a signaler)
"""

import sys
import json
import sqlite3
import importlib.util
from pathlib import Path


BASE = Path(__file__).resolve().parent
# L espion vit dans la zone : remonter jusqu a matrix/ puis matrice/data.
RACINE_MATRIX = next(p for p in [BASE, *BASE.parents] if p.name == "matrix")
DATA = RACINE_MATRIX / "matrice" / "data"

# Les OUTILS dont l'espion lit les BDD.
OUTILS = (RACINE_MATRIX / "_operateur" / "optimus-prime" / "super-combos"
          / "combos" / "outils")


def charger_vocabulaire(nom_outil, nom_module):
    """Le vocabulaire d'un outil, charge par son CHEMIN.

    Les dossiers d'outils portent un tiret (ils ne sont pas des packages) :
    c'est le meme chargement que celui de leur porte (importlib + spec).

    Retourne None si le domicile est introuvable ou illisible : l'espion
    SIGNALE (voir main), il ne devine JAMAIS un vocabulaire.
    """
    chemin = OUTILS / nom_outil / "fonctions" / nom_module
    if not chemin.is_file():
        return None
    try:
        spec = importlib.util.spec_from_file_location(
            nom_outil.replace("-", "_"), str(chemin))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError):
        return None
    return module


VOCABULAIRE_FRICTIONS = charger_vocabulaire("bdd-frictions", "bdd_frictions.py")
VOCABULAIRE_MODIFS = charger_vocabulaire("bdd-modifs", "bdd_modifs.py")


def journal_attente():
    crees, terminees = [], set()
    try:
        # Correction MO-032 : journal OPTIMUS dedie (l espion lisait celui du cameleon).
        lignes = (DATA / "historiques-missions-optimus.jsonl").read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            e = json.loads(ligne)
        except ValueError:
            continue
        if e.get("type") == "mission-creee" and e.get("id"):
            crees.append(e["id"])
        elif e.get("type") == "mission-terminee" and e.get("id"):
            terminees.add(e["id"])
    return [i for i in crees if i not in terminees]


def frictions_actives():
    """Frictions au statut ACTIF (celui du domicile bdd-frictions).

    Retourne -1 si la BDD ou son vocabulaire manque : l'appelant le DIT au lieu
    d'annoncer un zero rassurant.
    """
    if VOCABULAIRE_FRICTIONS is None:
        return -1
    db = DATA / "frictions.db"
    if not db.is_file():
        return -1
    with sqlite3.connect(db) as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM frictions WHERE statut = ?",
            (VOCABULAIRE_FRICTIONS.STATUT_ACTIVE,),
        ).fetchone()[0]


def verrous():
    """Verrous non liberes (statut du domicile bdd-modifs), ou [] si indisponible."""
    if VOCABULAIRE_MODIFS is None:
        return []
    db = DATA / "modifications.db"
    if not db.is_file():
        return []
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT fichier, date FROM modifications WHERE statut = ?",
            (VOCABULAIRE_MODIFS.STATUT_VERROUILLE,),
        ).fetchall()
    return [(r["fichier"], r["date"]) for r in rows]


def main():
    alertes = []
    # Un vocabulaire de statuts ABSENT se SIGNALE : sans lui l'espion ne peut
    # pas interroger la BDD, et un zero silencieux se lirait comme une BDD saine
    # (lecon L-100 : une reponse vide doit dire ce qu'elle a cherche).
    domiciles = (("bdd-frictions", VOCABULAIRE_FRICTIONS),
                 ("bdd-modifs", VOCABULAIRE_MODIFS))
    manquants = [nom for nom, vocabulaire in domiciles if vocabulaire is None]
    if manquants:
        alertes.append("vocabulaire de statuts introuvable (domicile illisible ou deplace) : "
                       + ", ".join(manquants))
    attente = journal_attente()
    if attente:
        alertes.append(f"missions en attente ({len(attente)}): {', '.join(attente)}")
    actives = frictions_actives()
    if actives and actives > 0:
        alertes.append(f"frictions actives non qualifiees : {actives}")
    for f, d in verrous():
        alertes.append(f"verrou non libere : {f} (depuis {d})")
    if alertes:
        print(f"ACTIVITE : {len(alertes)} signalement(s) :")
        for a in alertes:
            print(f"  - {a}")
        return 1
    print("Activite Optimus saine : file vide, 0 friction active, 0 verrou.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
