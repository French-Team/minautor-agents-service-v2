#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-recherche.py -- Garde : le pilote INJECTE la question de recherche.

Pourquoi (EO-131, demande createur du 2026-09-16) : MO-138 a rendu le moteur de
recherche CAPABLE (zone de l'operateur ouverte par une option explicite, recherche
par NOM de fichier, promesse de la route /chercher tenue par le code) ; il restait
a le rendre REFLEXE. Un moteur qu'il faut penser a lancer est un moteur eteint :
la MEMOIRE du projet ne sert que si quelqu'un pose la question.

CE QU'IL EXIGE :
  1. UN SEUL DOMICILE : la derivation de la question vit dans le module PARTAGE
     (data/commun/recherche_mission.py) -- et nulle part ailleurs. Deux copies
     divergeraient : l'une poserait une question utile, l'autre du bruit (L-029).
  2. MODULE SAIN : le vocabulaire des mots vides est TRIE et sans doublon, et la
     derivation est DETERMINISTE (memes donnees -> meme question : c'est ce qui la
     rend testable, donc piegeable).
  3. DEUX FLUX, DEUX CHEMINS : l'injection SIMPLE et l'injection de LOT portent le
     champ `recherche`, chez Optimus (Flux 2) ET chez le cameleon (Flux 1) -- un
     chemin laisse sans question est un flux ou l'agent improvise.
  4. INVISIBILITE (L-016) : le gabarit du Flux 1 ne porte JAMAIS l'option qui
     ouvre une zone interne -- le Flux 2 la porte, lui.
  5. QUESTION UTILE : sur les sujets REELS du brin, la question derivee n'est
     jamais vide et ne contient aucun mot vide.

L'AUTOTEST le PIEGE (lecon L-032) : un sujet fait de mots vides rend une question
VIDE (et c'est ACCUSE comme tel), un sujet reel rend une question UTILE, et le
vocabulaire DECLARE est bien celui qui filtre (on lui retire un mot : la question
change). Un detecteur jamais vu crier ne prouve rien.

CE QU'IL NE FAIT PAS : lecture seule -- il lit le module, les injections, les
constantes et le brin. Il n'ecrit rien et ne lance aucune mission.

Usage: python verifier-recherche.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = zone introuvable.
"""

import argparse
import json
import sys
from pathlib import Path

# Les domiciles : declares UNE fois, jamais recopies dans la logique.
FICHIER_MODULE = Path("matrice") / "data" / "commun" / "recherche_mission.py"
FICHIER_INJECTION_OPTIMUS = (Path("_operateur") / "optimus-prime" / "pilote"
                             / "injection" / "fonctions.py")
FICHIER_INJECTION_CAMELEON = Path("matrice") / "pilote" / "injection" / "fonctions.py"
FICHIER_CONSTANTES_OPTIMUS = (Path("_operateur") / "optimus-prime" / "pilote"
                              / "constants.py")
FICHIER_CONSTANTES_CAMELEON = Path("matrice") / "pilote" / "constants.py"
FICHIER_BRIN = (Path("_operateur") / "optimus-prime" / "pilote"
                / "entonnoir-files-optimus.json")

# Le marqueur du champ dans l'injection : le texte EXACT que la logique ecrit.
# Deux chemins par flux (mission simple + lot) : c'est le trou qu'on ferme.
MARQUEUR_CHAMP = "\"recherche\": preparer_recherche_mission(mission),"
CHEMINS_ATTENDUS = 2
# Le vocabulaire des mots vides est declare dans UN fichier de la zone.
MARQUEUR_VOCABULAIRE = "MOTS_VIDES = ("
DOMICILES_ATTENDUS = 1
# Un GARDE NE S'AUDITE PAS : ce fichier cite le marqueur dans une CHAINE (il
# doit bien le nommer pour le chercher) -- se compter comme une copie rendrait le
# garde fou (bdd-usages exclut aussi sa propre notation, OUTIL_EXCLU : L-029).
# Les ZONES JETABLES sont HORS CHAMP : un cobaye de la zone tmp pose un exemplaire
# du module pour l'eprouver (le cobaye de MO-141 le fait), et le compter comme une
# COPIE rendrait le garde fou -- un garde qui crie sur son propre cobaye est un
# garde qu'on desactive. Les points de restauration (.py.bak) ne sont pas des .py.
PREFIXE_ZONE_JETABLE = "tmp-"
DOSSIERS_IGNORES = ("__pycache__",)
# L'option qui ouvre une zone interne : Flux 2 oui, Flux 1 jamais (L-016).
OPTION_OUVERTURE = "--prive"

# Sujets de repli si le brin est absent (aucun acces disque exige).
SUJETS_REPLI = (
    {"theme": "PILOTE", "objectif": "Reparer la trace de la purge des zones jetables"},
    {"theme": "OUTIL", "objectif": "Reparer le moteur de recherche et sa route"},
)

RESULTATS = []


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def trouver_racine(racine):
    """Retourne le dossier matrix/ (celui qui porte `matrice` et `_operateur`), ou None."""
    candidats = [
        racine,
        racine / "cerveau-projet" / "matrix",
        racine / "matrix",
    ]
    for candidat in candidats:
        if (candidat / FICHIER_MODULE).is_file():
            return candidat
    return None


def charger_module(racine):
    """Importe le module PARTAGE par son chemin reel. -> (module, erreur)."""
    dossier = str((racine / FICHIER_MODULE).parent)
    if dossier not in sys.path:
        sys.path.insert(0, dossier)
    try:
        import recherche_mission
    except Exception as erreur:  # un module qui ne se charge pas est DEJA un ecart
        return None, repr(erreur)
    return recherche_mission, None


def est_en_champ(chemin, racine):
    """Vrai si le fichier est du CODE de la zone (hors garde, zones jetables, caches)."""
    try:
        parties = chemin.relative_to(racine).parts
    except ValueError:
        return False
    if parties[-1] == Path(__file__).name:
        return False
    for partie in parties[:-1]:
        if partie in DOSSIERS_IGNORES or partie.startswith(PREFIXE_ZONE_JETABLE):
            return False
    return True


def compter_occurrences(chemins, motif):
    """Nombre d'occurrences du motif, tous fichiers confondus."""
    total = 0
    for chemin in chemins:
        if chemin.is_file():
            total += chemin.read_text(encoding="utf-8", errors="replace").count(motif)
    return total


def question_inutile(question, module):
    """Vrai si la question porte un mot vide ou est vide (detecteur PUR)."""
    if not question:
        return True
    return any(mot in module.MOTS_VIDES for mot in question.split())


def main():
    parser = argparse.ArgumentParser(description="Garde : question de recherche injectee")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    racine = trouver_racine(Path(arguments.racine).resolve())
    if racine is None:
        print("Zone matrix/ introuvable sous " + str(arguments.racine))
        return 2

    module, erreur = charger_module(racine)
    if module is None:
        print("REFUS : le module partage de la recherche ne se charge pas -- " + str(erreur))
        return 1

    ecarts_nommes = []

    # 1. UN SEUL DOMICILE : la derivation n'est ecrite qu'une fois.
    domiciles = [chemin for chemin in racine.rglob("*.py")
                 if est_en_champ(chemin, racine)
                 and MARQUEUR_VOCABULAIRE in chemin.read_text(encoding="utf-8",
                                                             errors="replace")]
    controler("domicile-unique",
              len(domiciles) == DOMICILES_ATTENDUS,
              str(len(domiciles)) + " fichier(s) declarent le vocabulaire (attendu : "
              + str(DOMICILES_ATTENDUS) + ")"
              if len(domiciles) == DOMICILES_ATTENDUS
              else "COPIES : " + ", ".join(str(c) for c in domiciles))
    if len(domiciles) != DOMICILES_ATTENDUS:
        ecarts_nommes.append("derivation recopiee dans "
                             + str(len(domiciles)) + " fichier(s)")

    # 2. MODULE SAIN : vocabulaire trie, sans doublon, derivation deterministe.
    trie = list(module.MOTS_VIDES) == sorted(module.MOTS_VIDES)
    doublons = len(module.MOTS_VIDES) - len(set(module.MOTS_VIDES))
    controler("vocabulaire-sain", trie and doublons == 0,
              str(len(module.MOTS_VIDES)) + " mot(s) vide(s), tries et sans doublon"
              if trie and doublons == 0
              else "TRIE=" + str(trie) + ", DOUBLONS=" + str(doublons))
    if not (trie and doublons == 0):
        ecarts_nommes.append("vocabulaire des mots vides non trie ou en doublon")

    sujet_temoin = {"theme": "PILOTE", "objectif": "purge zone temporaire du pilote"}
    deterministe = module.deriver_question(sujet_temoin) == module.deriver_question(sujet_temoin)
    controler("derivation-deterministe", deterministe,
              "memes donnees -> meme question"
              if deterministe else "DEUX REPONSES DIFFERENTES pour le meme sujet")
    if not deterministe:
        ecarts_nommes.append("derivation non deterministe")

    # 3. DEUX FLUX, DEUX CHEMINS : le champ est porte partout.
    par_flux = (
        ("optimus", racine / FICHIER_INJECTION_OPTIMUS),
        ("cameleon", racine / FICHIER_INJECTION_CAMELEON),
    )
    for nom_flux, chemin in par_flux:
        occurrences = compter_occurrences([chemin], MARQUEUR_CHAMP)
        controler("deux-chemins-" + nom_flux, occurrences >= CHEMINS_ATTENDUS,
                  str(occurrences) + " chemin(s) d'injection portent la question"
                  if occurrences >= CHEMINS_ATTENDUS
                  else "SEULEMENT " + str(occurrences) + " sur " + str(CHEMINS_ATTENDUS)
                  + " -- un chemin sans question est un flux ou l'agent improvise")
        if occurrences < CHEMINS_ATTENDUS:
            ecarts_nommes.append("chemins d'injection sans question (" + nom_flux + ") : "
                                 + str(occurrences) + "/" + str(CHEMINS_ATTENDUS))

    # 4. INVISIBILITE : le Flux 1 ne porte jamais l'option d'ouverture (L-016).
    source_cameleon = racine / FICHIER_CONSTANTES_CAMELEON
    fuite = (OPTION_OUVERTURE in source_cameleon.read_text(encoding="utf-8", errors="replace")
             if source_cameleon.is_file() else False)
    controler("invisibilite-cameleon", not fuite,
              "le gabarit du Flux 1 ne porte AUCUNE option d'ouverture"
              if not fuite else "FUITE : le Flux 1 porte " + OPTION_OUVERTURE + " (L-016)")
    if fuite:
        ecarts_nommes.append("le gabarit du Flux 1 ouvre une zone interne (L-016)")

    source_optimus = racine / FICHIER_CONSTANTES_OPTIMUS
    ouvert = (OPTION_OUVERTURE in source_optimus.read_text(encoding="utf-8", errors="replace")
              if source_optimus.is_file() else False)
    controler("zone-operateur-ouverte", ouvert,
              "le gabarit du Flux 2 ouvre SA zone (il ne la cherche pas a l'aveugle)"
              if ouvert else "le Flux 2 n'ouvre PAS sa zone : ses fichiers restent invisibles")
    if not ouvert:
        ecarts_nommes.append("le gabarit du Flux 2 n'ouvre pas la zone de l'operateur")

    # 5. QUESTION UTILE sur les sujets REELS du brin.
    sujets = list(SUJETS_REPLI)
    source_brin = racine / FICHIER_BRIN
    origine = "brin REEL"
    if source_brin.is_file():
        try:
            donnees = json.loads(source_brin.read_text(encoding="utf-8"))
            brin = donnees.get("brin", [])
            if brin:
                sujets = [{"theme": item.get("theme", ""),
                           "objectif": item.get("objectif", "")} for item in brin]
        except (OSError, ValueError):
            origine = "brin illisible -- repli"
    inutiles = [(s["theme"], module.deriver_question(s))
                for s in sujets if question_inutile(module.deriver_question(s), module)]
    vides = [t for t, q in inutiles if not q]
    bruyantes = [t for t, q in inutiles if q]
    controler("question-utile", not inutiles,
              str(len(sujets)) + " sujet(s) " + origine + " -> question utile partout"
              if not inutiles
              else ("QUESTIONS VIDES : " + ", ".join(vides) if vides else "")
              + (" ; QUESTIONS BRUYANTES : " + ", ".join(bruyantes) if bruyantes else ""))
    if inutiles:
        ecarts_nommes.append("question vide ou bruyante sur un sujet reel")

    # 6. AUTOTEST : le detecteur doit etre VU crier (L-032).
    epreuves = []
    sujet_vide = {"theme": "BDD", "objectif": "demande createur : revision verifier"}
    epreuves.append(("sujet de mots vides -> question VIDE et ACCUSEE",
                     module.deriver_question(sujet_vide) == ""
                     and question_inutile(module.deriver_question(sujet_vide), module)))
    epreuves.append(("sujet reel -> question UTILE et ACCEPTEE",
                     not question_inutile(module.deriver_question(sujet_temoin), module)))
    # Le vocabulaire DECLARE est bien celui qui filtre : en retirant un mot, il
    # reapparait dans la question -- preuve que la logique le LIT, pas le copie.
    sauvegarde = module.MOTS_VIDES
    try:
        module.MOTS_VIDES = tuple(m for m in sauvegarde if m != "createur")
        avec_trou = module.deriver_question(sujet_vide)
    finally:
        module.MOTS_VIDES = sauvegarde
    epreuves.append(("vocabulaire DECLARE : un mot retire reapparait dans la question",
                     "createur" in avec_trou and module.deriver_question(sujet_vide) == ""))
    # Le bloc injecte ne fabrique JAMAIS une commande sur une question vide.
    bloc_vide = module.preparer_recherche(sujet_vide, "python3 x rechercher --requete \"{question}\"")
    epreuves.append(("question vide -> AUCUNE commande fabriquee",
                     bloc_vide.get("commande") == "" and bool(bloc_vide.get("avertissement"))))
    bloc_plein = module.preparer_recherche(sujet_temoin, "python3 x rechercher --requete \"{question}\"")
    epreuves.append(("question utile -> commande prete (le marqueur est remplace)",
                     "{question}" not in bloc_plein.get("commande", "")
                     and module.deriver_question(sujet_temoin) in bloc_plein.get("commande", "")))
    reussies = sum(1 for _, ok in epreuves if ok)
    controler("autotest-recherche", reussies == len(epreuves),
              "piege (" + str(reussies) + "/" + str(len(epreuves)) + ")"
              if reussies == len(epreuves)
              else "rate : " + ", ".join(nom for nom, ok in epreuves if not ok))
    if reussies != len(epreuves):
        ecarts_nommes.append("autotest de la recherche rate")

    print("VERIFIER RECHERCHE -- un moteur qu'il faut penser a lancer est un moteur eteint")
    if ecarts_nommes or any(not ok for _, ok, _ in RESULTATS):
        print("\nVERDICT KO : la question de recherche n'est pas derivee, portee ou utile (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : une seule derivation, deux flux, deux chemins par flux -- et la question est utile.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
