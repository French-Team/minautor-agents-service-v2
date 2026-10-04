#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Garde : la LISTE des maillons d une chaine est-elle ORDONNEE, TYPEE et PROUVABLE ?

Usage : python verifier-maillons.py [--racine <racine>] [--liste <chemin>]

REGLE (lue au domicile, jamais recopiee -- M-076) : le maillon [chaine] du theme
CADRAGE exige < aucun maillon sans PREUVE attendue ni TYPE declare, et jamais sans sa
derniere ligne : LA MISSION >, et il exige que la liste soit un FICHIER DE PILOTAGE
(json) ecrit par un OUTIL -- jamais un texte libre. Le vocabulaire des types est LU dans
sa liste fermee (`pilote/entonnoir/listes.py`), le domicile de la liste est DECLARE plus bas, comme `verifier-chaines.py`
declare le nom de son index : le charger depuis ici demanderait de toucher a sys.path
(le moteur importe le paquet `entonnoir`), une dette que le contrat fondamental chiffre.

CE QUE LA MESURE DU 2026-09-26 A TROUVE (MO-427) : la chaine EXISTAIT, mais comme TEXTE
IMPRIME. Mesure `[???] ... --simuler oui` : sept maillons types et prouvables affiches a
la console, et AUCUN fichier ecrit -- `ls preparation/maillons-cadrage.json` : < No such
file or directory >. Un texte imprime ne se relit nulle part apres le round.

CE QU IL JUGE (six controles) :
  1. la liste est LISIBLE : json objet, cle `maillons` non vide ;
  2. l ORDRE est CONTIGU : 1..N, DANS L ORDRE DU FICHIER -- un trou se lit comme une
     liste complete (le maillon perdu ne crie pas) ;
  3. chaque maillon DECLARE son TYPE, et ce type appartient a la liste FERMEE ;
  4. chaque maillon DECLARE sa PREUVE attendue (et son objectif, et sa case) ;
  5. la DERNIERE LIGNE est la mission (case `mission`) -- une liste sans fin n est pas
     une chaine ;
  6. la PROVENANCE est declaree (version, titre, demande) : une liste qu on ne peut pas
     REJOUER ne peut pas etre refaite, donc elle ne peut pas etre crue.

PREUVE (lecon L-032) : l autotest fait MORDRE le MEME detecteur (type absent, type hors
liste, preuve vide, trou d ordre, derniere ligne qui n est pas la mission, provenance
absente) et il EPARGNE la liste coherente. Le CONTRE-TEMOIN rejoue la lecture d AVANT
(le fichier juge par sa seule cle `maillons`) : sur le MEME cobaye casse, elle ne voit
RIEN -- sans lui, on ne saurait pas que ces controles mesurent quelque chose.

Lecture seule : aucun fichier n est ecrit, aucun etat modifie.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

DOSSIER_PILOTE = ("_operateur", "optimus-prime", "pilote")
CHEMIN_TYPES = ("_operateur", "optimus-prime", "pilote", "entonnoir", "listes.py")
NOM_MODULE_TYPES = "listes_des_types_lues_au_domicile"
NOM_TYPES = "TYPES"
# LE DOMICILE DE LA LISTE est declare ICI, comme `verifier-chaines.py` declare le
# nom de son index : ce garde ne charge PAS le moteur du cadrage (il importe le
# paquet `entonnoir`, donc le charger depuis ici demanderait de toucher a
# sys.path -- dette mesuree par le contrat fondamental). Ce qui est LU au
# domicile, c est le VOCABULAIRE (les types), jamais recopie ; le chemin, lui, se
# verifie par l usage : une liste posee ailleurs n est jamais vue.
DOSSIER_LISTE = ("_operateur", "optimus-prime", "preparation")
NOM_LISTE = "maillons-cadrage.json"
CASE_MISSION = "mission"
CLE_MAILLONS = "maillons"
CLES_PROVENANCE = ("version", "titre", "demande")
CHAMPS_MAILLON = ("ordre", "case", "type", "preuve", "objectif")


def trouver_matrix(racine):
    """Le dossier matrix/, ou None (jamais une supposition)."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / DOSSIER_PILOTE[0] / DOSSIER_PILOTE[1]).is_dir():
            return candidat
    return None


def charger_module(chemin, nom):
    """Charge un module par son CHEMIN de fichier (aucun sys.path touche)."""
    specification = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def lire_types(matrix):
    """(types, avis) : la liste FERMEE des types, lue chez elle (M-076)."""
    chemin = matrix.joinpath(*CHEMIN_TYPES)
    if not chemin.is_file():
        return (), "domicile des types INTROUVABLE : " + str(chemin)
    try:
        types = tuple(getattr(charger_module(chemin, NOM_MODULE_TYPES), NOM_TYPES))
    except Exception as erreur:  # noqa: BLE001
        return (), ("domicile des types ILLISIBLE (" + type(erreur).__name__ + " : "
                    + str(erreur)[:60] + ")")
    if not types:
        return (), "liste des types VIDE : " + str(chemin)
    return types, ""


def chemin_liste(matrix):
    """Le chemin de la liste, au domicile DECLARE ci-dessus."""
    return matrix.joinpath(*DOSSIER_LISTE).joinpath(NOM_LISTE)


def charger_liste(chemin):
    """(donnees, avis) : le contenu du fichier, ou la raison NOMMEE de son absence."""
    if not chemin.is_file():
        return None, ("la liste n EXISTE PAS (" + str(chemin) + ") -- la chaine est"
                      " restee un TEXTE : le maillon [chaine] exige un FICHIER ecrit"
                      " par un OUTIL")
    try:
        return json.loads(chemin.read_text(encoding="utf-8")), ""
    except (OSError, ValueError) as erreur:
        return None, "liste ILLISIBLE (" + type(erreur).__name__ + " : " + str(erreur)[:60] + ")"


def controler_liste(donnees, types):
    """Le DETECTEUR PUR : rend la liste des ecarts NOMMES (aucune impression)."""
    ecarts = []
    if not isinstance(donnees, dict):
        return ["la liste n est pas un objet json"]
    for cle in CLES_PROVENANCE:
        if not str(donnees.get(cle) or "").strip():
            ecarts.append("provenance INCOMPLETE : le champ " + repr(cle) + " est vide"
                          " (une liste qu on ne peut pas rejouer ne peut pas etre refaite)")
    maillons = donnees.get(CLE_MAILLONS)
    if not isinstance(maillons, list) or not maillons:
        return ecarts + ["AUCUN maillon : la cle " + repr(CLE_MAILLONS) + " est absente"
                         " ou vide -- une chaine vide s afficherait comme une chaine"]
    ordres = [m.get("ordre") if isinstance(m, dict) else None for m in maillons]
    attendus = list(range(1, len(maillons) + 1))
    if ordres != attendus:
        ecarts.append("ORDRE NON CONTIGU : " + repr(ordres) + " (attendu " + repr(attendus)
                      + ") -- un trou se lit comme une liste complete")
    for rang, maillon in enumerate(maillons, 1):
        if not isinstance(maillon, dict):
            ecarts.append("maillon " + str(rang) + " : ce n est pas un objet")
            continue
        etiquette = "maillon " + str(rang) + " (" + str(maillon.get("case") or "?") + ")"
        for champ in CHAMPS_MAILLON:
            if not str(maillon.get(champ, "")).strip():
                ecarts.append(etiquette + " : " + champ.upper() + " absent")
        type_declare = str(maillon.get("type") or "").strip()
        if type_declare and type_declare not in types:
            ecarts.append(etiquette + " : TYPE HORS LISTE (" + type_declare
                          + ") -- types fermes : " + ", ".join(types))
    dernier = maillons[-1]
    case_derniere = str((dernier or {}).get("case") or "").strip() if isinstance(dernier, dict) else ""
    if case_derniere != CASE_MISSION:
        ecarts.append("la DERNIERE LIGNE n est pas la mission (case " + repr(case_derniere)
                      + " au lieu de " + repr(CASE_MISSION) + ") -- une liste sans fin"
                      " n est pas une chaine")
    return ecarts


def lecture_d_avant(donnees):
    """CONTRE-TEMOIN (L-032) : la lecture MUETTE qui ne juge que la cle `maillons`."""
    if not isinstance(donnees, dict):
        return []
    return [] if isinstance(donnees.get(CLE_MAILLONS), list) and donnees.get(CLE_MAILLONS) else ["vide"]


def controler(nom, condition, detail=""):
    """Affiche et retourne un controle, au format des autres gardes."""
    print(("[OK] " if condition else "[KO] ") + nom + " : " + detail)
    return condition


def maillon(ordre, case, typ, preuve="p", objectif="o"):
    return {"ordre": ordre, "case": case, "type": typ, "preuve": preuve, "objectif": objectif}


def liste_coherente():
    return {"version": 1, "titre": "Cobaye", "demande": "demande de cobaye",
            "source": "createur",
            "maillons": [maillon(1, "manques", "audit"), maillon(2, "chaine", "doc"),
                         maillon(3, CASE_MISSION, "reparation")]}


def controler_autotest(types):
    """Le garde se PIEGE (L-032) : cobayes EN MEMOIRE, rien n ecrit sur le disque."""
    epreuves = []
    sain = liste_coherente()
    cas = [("coherente-NON-accusee", sain, False),
           ("type-absent-accuse", _variante(0, "type", ""), True),
           ("type-hors-liste-accuse", _variante(0, "type", "ZZ-BIDON"), True),
           ("preuve-vide-accusee", _variante(1, "preuve", ""), True),
           ("objectif-vide-accuse", _variante(1, "objectif", ""), True),
           ("ordre-troue-accuse", _ordre_casse(), True),
           ("derniere-ligne-hors-mission-accusee", _derniere_cassee(), True),
           ("provenance-vide-accusee", _provenance_videe(), True)]
    for nom, donnees, doit_mordre in cas:
        ecarts = controler_liste(donnees, types)
        epreuves.append((nom, bool(ecarts) == doit_mordre,
                         ("accuse : " + " ; ".join(ecarts)[:90]) if ecarts else "silence"))
    cassee = _variante(0, "type", "")
    muette = lecture_d_avant(cassee)
    ecarts = controler_liste(cassee, types)
    epreuves.append(("contre-temoin-lecture-d-avant-AVEUGLE",
                     not muette and bool(ecarts),
                     "lecture d avant : " + (repr(muette) if muette else "RIEN")
                     + " | lecture d apres : " + str(len(ecarts)) + " ecart(s)"))
    return epreuves


def _variante(rang, champ, valeur):
    donnees = liste_coherente()
    donnees[CLE_MAILLONS][rang][champ] = valeur
    return donnees


def _ordre_casse():
    donnees = liste_coherente()
    donnees[CLE_MAILLONS][1]["ordre"] = 9
    return donnees


def _derniere_cassee():
    donnees = liste_coherente()
    donnees[CLE_MAILLONS][-1]["case"] = "depot"
    return donnees


def _provenance_videe():
    donnees = liste_coherente()
    donnees["titre"] = ""
    return donnees


def main():
    parser = argparse.ArgumentParser(description="Garde : la liste des maillons est ordonnee, typee et prouvable")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--liste", default="", help="Chemin d une liste a juger (defaut: son domicile declare)")
    arguments = parser.parse_args()
    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2
    types, avis_types = lire_types(matrix)
    if avis_types:
        print("KO    types-lus-au-domicile : " + avis_types)
        return 1
    chemin = chemin_liste(matrix)
    if arguments.liste:
        chemin = Path(arguments.liste)
    print("DECLARATION LUE AU DOMICILE : types " + ", ".join(types)
          + " | liste " + str(chemin))
    donnees, avis = charger_liste(chemin)
    tenu = True
    if avis:
        tenu = controler("liste-ecrite-par-un-outil", False, avis)
        ecarts = []
    else:
        ecarts = controler_liste(donnees, types)
        tenu &= controler("liste-ordonnee-typee-prouvable", not ecarts,
                          "aucun ecart -- " + str(len(donnees.get(CLE_MAILLONS, [])))
                          + " maillon(s), derniere ligne : la mission"
                          if not ecarts else " ; ".join(ecarts[:8]))
    autotest = controler_autotest(types)
    reussies = sum(1 for _, ok, _ in autotest if ok)
    detail_autotest = ("piege (" + str(reussies) + "/" + str(len(autotest)) + ")"
                       if reussies == len(autotest)
                       else "rate : " + ", ".join(nom for nom, ok, _ in autotest if not ok))
    print("[--] autotest-maillons : " + detail_autotest)
    print("VERIFIER MAILLONS -- une liste sans ordre, sans type ou sans preuve n a aucune verite")
    if not tenu or reussies != len(autotest):
        print("")
        print("VERDICT KO : la liste des maillons n est pas ordonnee, typee et prouvable (ou le garde ne sait plus mordre).")
        return 1
    print("")
    print("VERDICT OK : la liste est ecrite, ordonnee, chaque maillon type et prouvable, derniere ligne la mission.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
