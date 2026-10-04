#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-flux2.py -- Garde Flux 2 pour Optimus Prime

Verifie qu'Optimus ne travaille QUE dans le Flux 2 (maintenance).
Detecte toute violation du perimetre Flux 2.

LA FENETRE EST CELLE DU ROUND FLUX 2, PAS CELLE DU JOUR (reparation MO-449).
Un fichier interdit modifie AVANT l ouverture du round Flux 2 en cours vient
d un AUTRE flux (le cameleon, Flux 1) : il est EPARGNE. Un fichier interdit
modifie PENDANT le round vient du Flux 2 : il est ACCUSE. Faute de borne de
round lisible, on retombe sur MINUIT (fenetre conservatrice) et on le DIT.

Usage : python garde-flux2.py [--racine <path>] [--verbose] [--strict]
        python garde-flux2.py --auto-test
  code 0 = Flux 2 respecte, code 1 = violation detectee.
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, time


# Zones autorisees pour Optimus (Flux 2)
ZONES_AUTORISEES = [
    "cerveau-projet/matrix/",  # Perimetre d'ecriture principal
    "cerveau-projet/matrix/_operateur/",  # Zone operateurs
    "cerveau-projet/matrix/_operateur/optimus-prime/",  # Zone Optimus
    "cerveau-projet/matrix/matrice/",  # Zone Matrice (lecture seule)
    "cerveau-projet/matrix/matrice/data/",  # BDD (lecture seule)
    "cerveau-projet/matrix/matrice/routines/",  # Routines (lecture seule)
    "cerveau-projet/matrix/matrice/pilote/",  # Pilote (lecture seule)
    "cerveau-projet/matrix/matrice/intercom/",  # Intercom (ecriture limitez)
]

# Zones interdites pour Optimus (Flux 1 - Cameleon)
ZONES_INTERDITES = [
    "cerveau-projet/matrix/matrice/pilote/file-missions.json",  # File du cameleon
    "cerveau-projet/matrix/matrice/pilote/entonnoir-files.json",  # Entonnoir du cameleon
    "cerveau-projet/matrix/matrice/pilote/main.py",  # Pilote du cameleon
    "cerveau-projet/agents/",  # Agents v1/v2
    "cerveau-projet/freelance/",  # Agents freelance
    "cerveau-projet/matrix/_operateur/cameleon/",  # Zone cameleon
]

# Fichiers temporaires autorises
FICHIERS_TEMPORAIRES = [
    ".tmp",
    ".bak",
    ".pid",
]

# Journal qui porte les ouvertures de round du Flux 2 (chemin relatif a la racine).
CHEMIN_SUIVI_FLUX2 = "cerveau-projet/matrix/matrice/data/suivi-optimus.jsonl"

# Actions qui OUVRENT un round Flux 2 dans le journal.
ACTIONS_OUVERTURE_ROUND = ("debut", "prise")

# Format d horodatage du journal Flux 2.
FORMAT_HORODATAGE = "%Y-%m-%d %H:%M:%S"

# La racine matrix/ se DETECTE par marqueur stable (convention 1.3 : aucun
# parents[N] nu -- MO-088). On remonte jusqu'a retrouver matrice/data/commun.
BORNES_REMONTEE = 12
_courant = Path(__file__).resolve().parent
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    _courant = None
RACINE_MATRICE = _courant


def borne_du_round_flux2(racine):
    """Retourne (borne, source) : ouverture du round Flux 2 EN COURS.

    Lit le journal Flux 2 (suivi-optimus) et retient la DERNIERE ouverture de
    round du jour (action 'debut' ou 'prise'). Retourne (None, raison) si le
    journal est absent/illisible ou ne porte aucune ouverture aujourd hui.
    """
    chemin = racine / CHEMIN_SUIVI_FLUX2
    if not chemin.exists():
        return None, "journal Flux 2 absent"
    aujourd_hui = datetime.now().date()
    borne = None
    try:
        with open(chemin, "r", encoding="utf-8") as flux:
            for ligne in flux:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    entree = json.loads(ligne)
                except ValueError:
                    continue
                if entree.get("action") not in ACTIONS_OUVERTURE_ROUND:
                    continue
                try:
                    quand = datetime.strptime(str(entree.get("date", "")), FORMAT_HORODATAGE)
                except ValueError:
                    continue
                if quand.date() != aujourd_hui:
                    continue
                if borne is None or quand > borne:
                    borne = quand
    except OSError:
        return None, "journal Flux 2 illisible"
    if borne is None:
        return None, "aucune ouverture de round aujourd hui"
    return borne, "ouverture du round Flux 2 en cours"


def evaluer(racine, strict=False, verbose=False):
    """Juge le perimetre Flux 2 et retourne (code, sortie).

    code 0 = perimetre respecte, code 1 = violation. La fenetre de jugement est
    celle du round Flux 2 en cours ; faute de borne, minuit (conservateur).
    """
    violations = []
    avertissements = []
    lignes = []

    borne, source = borne_du_round_flux2(racine)
    if borne is None:
        borne = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        lignes.append("FENETRE : aucune borne de round (" + source + ") -- repli MINUIT (conservateur).")
    else:
        lignes.append("FENETRE : " + source + " (" + borne.strftime(FORMAT_HORODATAGE) + ").")

    # Verifier les zones interdites
    for zone in ZONES_INTERDITES:
        zone_path = racine / zone
        if zone_path.exists():
            if zone_path.is_file():
                # Verifier si le fichier a ete modifie pendant le round Flux 2
                try:
                    mtime = datetime.fromtimestamp(zone_path.stat().st_mtime)
                    if mtime >= borne:
                        violations.append("FICHIER INTERDIT MODIFIE PENDANT LE ROUND FLUX 2: " + zone)
                except OSError:
                    pass
            else:
                # Verifier si le dossier contient des fichiers modifies pendant le round
                try:
                    for f in zone_path.rglob("*"):
                        if f.is_file():
                            try:
                                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                                if mtime >= borne:
                                    violations.append("FICHIER INTERDIT MODIFIE: " + str(f.relative_to(racine)))
                            except OSError:
                                pass
                except PermissionError:
                    pass

    # Verifier les fichiers hors perimetre
    try:
        for f in racine.rglob("*"):
            if f.is_file():
                # Ignorer les fichiers temporaires
                if f.suffix in FICHIERS_TEMPORAIRES:
                    continue

                # Ignorer les dossiers techniques
                if any(part.startswith(".") or part == "__pycache__" for part in f.parts):
                    continue

                # Verifier si le fichier est dans une zone autorisee
                rel = f.relative_to(racine)
                dans_zone_autorisee = False
                for zone in ZONES_AUTORISEES:
                    try:
                        rel.relative_to(zone)
                        dans_zone_autorisee = True
                        break
                    except ValueError:
                        continue

                if not dans_zone_autorisee:
                    # Verifier si le fichier a ete modifie pendant le round Flux 2
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime)
                        if mtime >= borne:
                            if strict:
                                violations.append("FICHIER HORS ZONE MODIFIE (STRICT): " + str(rel))
                            else:
                                avertissements.append("FICHIER HORS ZONE MODIFIE: " + str(rel))
                    except OSError:
                        pass
    except PermissionError:
        pass

    # Afficher les resultats
    if violations:
        lignes.append("VIOLATIONS FLUX 2 DETECTEES:")
        for v in violations:
            lignes.append("  - " + v)
        lignes.append("Total: " + str(len(violations)) + " violation(s)")
        return 1, "\n".join(lignes)

    if avertissements and verbose:
        lignes.append("AVERTISSEMENTS (fichiers hors zone modifies):")
        for a in avertissements:
            lignes.append("  - " + a)
        lignes.append("Total: " + str(len(avertissements)) + " avertissement(s)")

    lignes.append("FLUX 2 RESPECTE: Aucune violation detectee.")
    return 0, "\n".join(lignes)


def _poser_mtime(chemin, quand):
    """Pose la date de modification d un fichier (pour le cobaye)."""
    import os
    horodatage = quand.timestamp()
    os.utime(str(chemin), (horodatage, horodatage))


def _zone_jetable():
    """Zone jetable du projet (tmp-optimus), ou None si la racine est introuvable."""
    if RACINE_MATRICE is None:
        return None
    return RACINE_MATRICE / "_operateur" / "optimus-prime" / "tmp-optimus"


def auto_test():
    """Rejoue le cobaye de la FENETRE : les deux polarites + le repli.

    Rouge sur une ecriture Flux 2 (pendant le round), epargne sur une ecriture
    Flux 1 (avant le round), et repli conservateur (minuit) sans borne lisible.
    """
    import shutil
    import tempfile

    epreuves = 0
    reussies = 0
    zone = _zone_jetable()
    if zone is None:
        print("AUTO-TEST FENETRE : IMPOSSIBLE -- racine matrix/ introuvable.")
        return 1
    zone.mkdir(parents=True, exist_ok=True)
    base = Path(tempfile.mkdtemp(prefix="cobaye-gardeflux2-", dir=str(zone)))
    try:
        matrice = base / "cerveau-projet" / "matrix" / "matrice"
        (matrice / "data").mkdir(parents=True)
        (matrice / "pilote").mkdir(parents=True)
        interdit = matrice / "pilote" / "entonnoir-files.json"
        interdit.write_text("{}\n", encoding="utf-8")
        journal = matrice / "data" / "suivi-optimus.jsonl"
        aujourd_hui = datetime.now().date()
        ouverture = datetime.combine(aujourd_hui, time(8, 0, 0))

        # Cas 1 : ecriture Flux 2 (PENDANT le round) -> ROUGE
        journal.write_text(
            json.dumps({"date": ouverture.strftime(FORMAT_HORODATAGE),
                        "mission": "MO-999", "action": "debut", "detail": "cobaye"}) + "\n",
            encoding="utf-8")
        _poser_mtime(interdit, datetime.combine(aujourd_hui, time(9, 0, 0)))
        code, _ = evaluer(base)
        epreuves += 1
        if code == 1:
            reussies += 1
            print("  cobaye ecriture-flux2 (apres le round) : OK -- ACCUSE")
        else:
            print("  cobaye ecriture-flux2 (apres le round) : ECHEC -- epargne a tort")

        # Cas 2 : ecriture Flux 1 (AVANT le round) -> EPARGNE
        _poser_mtime(interdit, datetime.combine(aujourd_hui, time(7, 0, 0)))
        code, _ = evaluer(base)
        epreuves += 1
        if code == 0:
            reussies += 1
            print("  cobaye ecriture-flux1 (avant le round) : OK -- EPARGNE")
        else:
            print("  cobaye ecriture-flux1 (avant le round) : ECHEC -- accuse a tort")

        # Cas 3 : aucune borne de round -> repli minuit (conservateur) -> ROUGE
        journal.write_text("", encoding="utf-8")
        _poser_mtime(interdit, datetime.combine(aujourd_hui, time(7, 0, 0)))
        code, _ = evaluer(base)
        epreuves += 1
        if code == 1:
            reussies += 1
            print("  cobaye sans borne de round : OK -- ACCUSE (fenetre conservatrice)")
        else:
            print("  cobaye sans borne de round : ECHEC -- epargne sans borne")
    finally:
        shutil.rmtree(str(base), ignore_errors=True)

    print("AUTO-TEST FENETRE : " + str(reussies) + "/" + str(epreuves) + " epreuve(s) OK")
    return 0 if reussies == epreuves else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Garde Flux 2 pour Optimus")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--strict", action="store_true", help="Mode strict (toute modification = violation)")
    parser.add_argument("--auto-test", action="store_true", help="Rejouer le cobaye de la fenetre de round")
    args = parser.parse_args(argv)

    if args.auto_test:
        return auto_test()

    code, sortie = evaluer(Path(args.racine).resolve(), args.strict, args.verbose)
    print(sortie)
    return code


if __name__ == "__main__":
    sys.exit(main())
