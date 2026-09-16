#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-roles.py -- Garde : toute mission a un ROLE, et le pilote l'INJECTE.

Pourquoi (revision du 2026-09-14, chantier MAILLON 2/5, demande createur) : le
cameleon recoit UNE personnalite par mission (categorie PERSONNALITE du vivier) ;
Optimus n'en recevait AUCUNE. Ses missions ne portaient qu'un theme de CHANTIER
(REPARATION, OUTIL, PILOTE...) -- le QUOI toucher, jamais le QUI JE SUIS. Et le
catalogue du pilote DERVERSAIT la fiche ENTIERE (220 lignes) au demarrage au lieu
de fournir la conduite au moment ou elle sert.

CE QU'IL EXIGE :
  1. TABLE COMPLETE : chaque type de l'entonnoir (listes.TYPES) a une posture,
     et aucune posture ne designe un type inconnu -- un trou laisserait une
     mission partir sans conduite.
  2. POSTURES REELLES : chaque posture de la table est un theme du VIVIER de
     categorie PERSONNALITE (une posture inventee, ou un theme de CHANTIER
     deguise en posture, est refusee et NOMMEE).
  3. CATALOGUE SERVI : le catalogue declare l'entree `role` en `avant-mission` et
     le MOTEUR la sert pour de vrai (postures presentes dans la sortie).
  4. CONTRAT DES DEUX CHEMINS : l'injection SIMPLE et l'injection de LOT portent
     TOUTES LES DEUX le role -- deux copies d'un mecanisme = un chemin protege et
     l'autre non (c'est exactement le trou qu'on ferme).

L'AUTOTEST le PIEGE (lecon L-032) : une table trouee est ACCUSEE, un theme de
chantier deguise en posture est ACCUSE, une posture inventee est ACCUSEE, une
table complete est ACCEPTEE. Un detecteur jamais vu crier ne prouve rien.

CE QU'IL NE FAIT PAS : lecture seule -- il lit la table, le catalogue et une
sortie du moteur. Il n'ecrit rien et ne lance aucune mission.

Usage: python verifier-roles.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = zone introuvable.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# La table des postures et les types de l'entonnoir : source UNIQUE, lue sur le
# disque (jamais recopiee ici -- deux copies = deux verites, L-035).
FICHIER_TABLE = Path("pilote") / "personnalites.py"
FICHIER_CATALOGUE = Path("pilote") / "injection" / "config.json"
FICHIER_INJECTION = Path("pilote") / "injection" / "fonctions.py"
FICHIER_INJECTER = Path("pilote") / "injection" / "injecter.py"
ID_ENTREE_ROLE = "role"
MARQUEUR_DEUX_CHEMINS = "\"role\": role"
CHEMINS_ATTENDUS = 2

RESULTATS = []


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def trouver_zone(racine):
    """Retourne le dossier _operateur/optimus-prime/, ou None."""
    candidats = [
        racine,
        racine / "cerveau-projet" / "matrix" / "_operateur" / "optimus-prime",
        racine / "_operateur" / "optimus-prime",
    ]
    for candidat in candidats:
        if (candidat / "pilote" / "personnalites.py").is_file():
            return candidat
    return None


def charger_pilote(zone):
    """Importe les modules du pilote (table + porte du vivier). -> (modules, erreur)."""
    pilote = str(zone / "pilote")
    if pilote not in sys.path:
        sys.path.insert(0, pilote)
    try:
        import personnalites  # pose la table ET la verifie au chargement
        from entonnoir.listes import TYPES
    except Exception as erreur:  # un module qui ne se charge pas est DEJA un ecart
        return None, "chargement impossible : " + repr(erreur)
    return {"personnalites": personnalites, "TYPES": TYPES}, None


def table_complete(mapping, types):
    """Types sans posture + postures hors liste. Detecteur PUR (cobaye a l'appui)."""
    sans_posture = [t for t in types if t not in mapping]
    hors_liste = [t for t in mapping if t not in types]
    return sans_posture, hors_liste


def main():
    parser = argparse.ArgumentParser(description="Garde : role de mission pose et injecte")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    racine = Path(arguments.racine).resolve()
    zone = trouver_zone(racine)
    if zone is None:
        print("Zone optimus-prime introuvable sous " + str(racine))
        return 2

    modules, erreur = charger_pilote(zone)
    if modules is None:
        print("REFUS : la table des roles ne se charge pas -- " + str(erreur))
        return 1

    personnalites = modules["personnalites"]
    types = modules["TYPES"]
    ecarts_nommes = []

    # 1. TABLE COMPLETE (detecteur pur, puis sur la table REELLE).
    sans_posture, hors_liste = table_complete(personnalites.POSTURE_PAR_TYPE, types)
    controler(
        "table-complete",
        not sans_posture and not hors_liste,
        str(len(types)) + " type(s), chacun a une posture" if not sans_posture and not hors_liste
        else ("types SANS posture : " + ", ".join(sans_posture)
              + (" ; " if sans_posture and hors_liste else "")
              + ("types HORS LISTE : " + ", ".join(hors_liste) if hors_liste else "")),
    )
    if sans_posture or hors_liste:
        ecarts_nommes.append("table des roles trouee : "
                             + ", ".join(sans_posture + hors_liste))

    # 2. POSTURES REELLES (chaque posture est une PERSONNALITE du vivier).
    fautives = []
    for type_cible in sorted(personnalites.POSTURE_PAR_TYPE):
        posture = personnalites.POSTURE_PAR_TYPE[type_cible]
        code, canonique, message = personnalites.valider_posture(posture)
        if code != 0:
            fautives.append(type_cible + " -> " + posture + " (" + (message or "refusee par la porte") + ")")
        elif message:
            fautives.append(type_cible + " -> " + posture + " (" + message + ")")
    controler(
        "postures-reelles",
        not fautives,
        "les " + str(len(personnalites.POSTURE_PAR_TYPE)) + " postures sont au vivier (categorie PERSONNALITE)"
        if not fautives else "POSTURES FAUTIVES : " + " ; ".join(fautives),
    )
    if fautives:
        ecarts_nommes.append("postures fautives : " + " ; ".join(fautives))

    # 3. CATALOGUE SERVI : declare ET servi pour de vrai par le moteur.
    catalogue = zone / FICHIER_CATALOGUE
    declaree = False
    if catalogue.is_file():
        try:
            donnees = json.loads(catalogue.read_text(encoding="utf-8"))
            declaree = any(entree.get("id") == ID_ENTREE_ROLE
                           for entree in donnees.get("injections", {}).get("avant-mission", []))
        except (OSError, ValueError):
            declaree = False
    controler("catalogue-declare", declaree,
              "l'entree `role` est declaree en avant-mission" if declaree
              else "l'entree `" + ID_ENTREE_ROLE + "` MANQUE au catalogue (" + str(catalogue) + ")")
    if not declaree:
        ecarts_nommes.append("catalogue sans entree `role`")

    servie = False
    detail_service = "moteur non lance"
    if declaree:
        moteur = zone / FICHIER_INJECTER
        resultat = subprocess.run([sys.executable, str(moteur), "avant-mission"],
                                  capture_output=True, text=True, cwd=str(zone / "pilote"))
        sortie = resultat.stdout + resultat.stderr
        postures = sorted(personnalites.POSTURE_PAR_TYPE.values())
        manquantes = [p for p in postures if "\"" + p + "\"" not in sortie]
        servie = resultat.returncode == 0 and not manquantes
        detail_service = ("le moteur sert les " + str(len(postures)) + " postures"
                          if servie else "NON SERVIE (code " + str(resultat.returncode) + ")"
                          + (" -- absentes : " + ", ".join(manquantes) if manquantes else ""))
    controler("catalogue-servi", servie, detail_service)
    if not servie:
        ecarts_nommes.append("catalogue non servi : " + detail_service)

    # 4. CONTRAT DES DEUX CHEMINS : simple ET lot portent le role.
    source = zone / FICHIER_INJECTION
    occurrences = 0
    if source.is_file():
        occurrences = source.read_text(encoding="utf-8").count(MARQUEUR_DEUX_CHEMINS)
    controler("deux-chemins-portent-le-role", occurrences >= CHEMINS_ATTENDUS,
              str(occurrences) + " chemin(s) d'injection porte(nt) le role"
              if occurrences >= CHEMINS_ATTENDUS
              else "SEULEMENT " + str(occurrences) + " chemin(s) sur " + str(CHEMINS_ATTENDUS)
              + " -- un chemin laisse sans role est une mission sans conduite")
    if occurrences < CHEMINS_ATTENDUS:
        ecarts_nommes.append("chemins d'injection sans role : " + str(occurrences)
                             + "/" + str(CHEMINS_ATTENDUS))

    # 5. AUTOTEST : le detecteur et la porte doivent etre VUS crier (L-032).
    epreuves = []
    epreuves.append(("table complete ACCEPTEE",
                     table_complete(dict(personnalites.POSTURE_PAR_TYPE), types) == ([], [])))
    trouee = dict(personnalites.POSTURE_PAR_TYPE)
    trouee.pop(types[0], None)
    epreuves.append(("table TROUEE ACCUSEE",
                     table_complete(trouee, types)[0] == [types[0]]))
    invente = dict(personnalites.POSTURE_PAR_TYPE)
    invente[types[0]] = "POSTURE-INVENTEE"
    inventees = [t for t in invente
                 if personnalites.valider_posture(invente[t])[0] != 0]
    epreuves.append(("posture INVENTEE ACCUSEE", types[0] in inventees))
    # Un theme de CHANTIER (categorie SYSTEME) ne doit jamais passer pour une posture.
    code_chantier, _, message_chantier = personnalites.valider_posture("REPARATION")
    epreuves.append(("theme de CHANTIER refuse comme posture",
                     code_chantier != 0 and "PERSONNALITE" in (message_chantier or "")))
    reussies = sum(1 for _, ok in epreuves if ok)
    controler("autotest-roles", reussies == len(epreuves),
              "piege (" + str(reussies) + "/" + str(len(epreuves)) + ")" if reussies == len(epreuves)
              else "rate : " + ", ".join(nom for nom, ok in epreuves if not ok))
    if reussies != len(epreuves):
        ecarts_nommes.append("autotest des roles rate")

    print("VERIFIER ROLES -- une mission sans posture improvise sa conduite")
    if ecarts_nommes or any(not ok for _, ok, _ in RESULTATS):
        print("\nVERDICT KO : le role d'une mission n'est pas pose, reel, servi ou porte (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : chaque type a une posture reelle du vivier, et le pilote l'injecte sur ses deux chemins.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
