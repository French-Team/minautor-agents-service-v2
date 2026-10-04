#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesurer-lecons.py -- Mesure et critere de PERTINENCE des lecons injectees.

MISSION (EO-398 / MO-446, demande createur 2026-09-24) : la selection des lecons
injectees (EO-270) est PLEINE (mesure MO-395 : 22 injectees / 119 ecartees, plafond
6000 tokens ATTEINT). Il faut (1) MESURER ce qui est vraiment lu, (2) un critere de
PERTINENCE mesurable par les mots du SUJET, (3) le couplage avec les SEGMENTS.

CE QUE CET OUTIL MESURE, et rien d autre :
  - le PROFIL du corpus : chaque tag et sa FREQUENCE. Un tag present partout
    (`porte` 20, `garde` 20) n informe rien ; un tag rare informe beaucoup. C est
    la matiere du critere.
  - la selection ACTUELLE (COMPTE des tags presents dans le sujet) contre un
    critere IDF (SOMME des poids des tags presents) : le meme sujet, deux
    selections -- c est l AVANT/APRES demande.
  - le COUPLAGE : le vocabulaire du SUJET (mission) et celui des SEGMENTS se
    SOMMENT avant de scorer (le segment dit OU on en est, la lecon CE QU on a appris).

MODES :
  critere                      profil du corpus (N lecons, tags, frequences, poids IDF)
  mesurer --mots "a,b,c"       pertinentes (score > 0) vs endormies (score = 0)
  avant-apres --mots "a,b,c"   ordre des lecons du sujet par COMPTE vs par IDF
  auto-test                    cobaye (l IDF mord) + contre-temoin (le compte epargne)

OPTIONS : --mots (vocabulaire du sujet, separe par des virgules), --lecons <chemin>,
          --segments <chemin> (vocabulaire des segments, additionne), --plafond-nombre N
Usage :
  python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/mesurer-lecons.py critere
  python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/mesurer-lecons.py mesurer --mots "lecons,injection,plafond"
  python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/mesurer-lecons.py avant-apres --mots "seuil,garde,porte" [--plafond-nombre 30]
  python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/mesurer-lecons.py auto-test

CODES RETOUR : 0 = OK, 2 = refus nomme.

LE PLAFOND N EST PAS RECOPIE : `--plafond-nombre` est un parametre, dont le domicile
est PLAFOND_LEGONS_NOMBRE (pilote/injection/fonctions.py). L outil MESURE la
selection, il ne remplace pas le moteur -- une mesure ne se prend pas pour le juge.
"""

import json
import math
import os
import re
import sys
from pathlib import Path

ENCODAGE = "utf-8"
LONGUEUR_MIN_MOT = 4
SEPARATEUR_VIRGULE = ","
PLAFOND_NOMBRE_DEFAUT = 30  # domicile : PLAFOND_LEGONS_NOMBRE (pilote/injection)
CHEMIN_LECONS_DEFAUT = "matrice/data/lecons.json"
CHEMIN_SEGMENTS_DEFAUT = "_operateur/optimus-prime/raisonnement/segments.json"


def racine_matrice():
    """La racine de la Matrice : le premier ancetre nomme matrix depuis ce fichier."""
    base = Path(__file__).resolve().parent
    for candidat in [base, *base.parents]:
        if candidat.name == "matrix":
            return candidat
    return base


def resoudre(chemin):
    """Un chemin relatif se resout depuis la racine de la Matrice."""
    chemin = str(chemin)
    if os.path.isabs(chemin):
        return Path(chemin)
    return racine_matrice() / chemin


def charger_lecons(chemin):
    """Les lecons du corpus, ou (None, motif) NOMME si illisible (jamais un faux vide)."""
    chemin = resoudre(chemin)
    if not chemin.is_file():
        return None, "corpus INTROUVABLE : " + str(chemin)
    try:
        with open(str(chemin), "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
    except (OSError, ValueError) as erreur:
        return None, "corpus ILLISIBLE : " + str(erreur)[:80]
    lecons = donnees.get("lecons", []) if isinstance(donnees, dict) else donnees
    if not isinstance(lecons, list):
        return None, "corpus MAL FORME : la cle `lecons` n est pas une liste"
    return lecons, None


def vocabulaire(texte):
    """Les mots d un texte, meme regle que le moteur : >= LONGUEUR_MIN_MOT lettres."""
    mots = set()
    for mot in re.split(r"[^0-9A-Za-z_]+", str(texte or "").lower()):
        if len(mot) >= LONGUEUR_MIN_MOT:
            mots.add(mot)
    return mots


def vocabulaire_des_mots(mots):
    """Le vocabulaire depuis une liste separee par des virgules."""
    texte = " ".join(str(mots or "").split(SEPARATEUR_VIRGULE))
    return vocabulaire(texte)


def vocabulaire_des_segments(chemin):
    """Le vocabulaire des SEGMENTS (couplage) : set(), motif si absent, jamais bloquant."""
    chemin = resoudre(chemin)
    if not chemin.is_file():
        return set(), "segments ABSENTS (couplage non applique) : " + str(chemin)
    try:
        with open(str(chemin), "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
    except (OSError, ValueError) as erreur:
        return set(), "segments ILLISIBLES : " + str(erreur)[:80]
    morceaux = []
    segments = donnees.get("segments", []) if isinstance(donnees, dict) else donnees
    if isinstance(segments, list):
        for segment in segments:
            if isinstance(segment, dict):
                for cle in ("sujet", "but", "nom", "texte", "resume", "contenu"):
                    morceaux.append(str(segment.get(cle, "")))
            else:
                morceaux.append(str(segment))
    return vocabulaire(" ".join(morceaux)), None


def frequences(lecons):
    """Nombre de lecons ou apparait chaque tag (document frequency)."""
    compte = {}
    for lecon in lecons:
        tags = lecon.get("tags") or []
        if not isinstance(tags, list):
            continue
        for tag in set(str(t).lower() for t in tags):
            compte[tag] = compte.get(tag, 0) + 1
    return compte


def poids_idf(lecons):
    """Poids d information de chaque tag : log(N / df), jamais negatif.

    Un tag present dans TOUTES les lecons vaut 0 (il ne distingue rien) ; un tag
    present dans une seule vaut log(N), le maximum. C est le critere mesurable
    demande : la pertinence d une lecon se pese par la RARETE de ce qu elle partage
    avec le sujet.
    """
    total = max(1, len(lecons))
    compte = frequences(lecons)
    poids = {}
    for tag, df in compte.items():
        poids[tag] = max(0.0, math.log(float(total) / float(max(1, df))))
    return poids


def tags_presents(lecon, vocab):
    tags = lecon.get("tags") or []
    if not isinstance(tags, list):
        return []
    return [str(t).lower() for t in tags if str(t).lower() in vocab]


def score_compte(lecon, vocab):
    """Le critere ACTUEL : nombre de tags presents dans le sujet (EO-270)."""
    return float(len(tags_presents(lecon, vocab)))


def score_idf(lecon, vocab, poids):
    """Le critere PROPOSE : somme des poids des tags presents dans le sujet."""
    return float(sum(poids.get(tag, 0.0) for tag in tags_presents(lecon, vocab)))


def _date(lecon):
    return str(lecon.get("date", "")) + str(lecon.get("id", ""))


def ordonner(lecons, score_fn):
    """Les lecons CLASSEES : score decroissant, puis date/id (recence) decroissante."""
    rangees = sorted(lecons, key=_date, reverse=True)
    rangees.sort(key=lambda l: -score_fn(l))
    return rangees


def selectionner(lecons, score_fn, plafond_nombre):
    """Les lecons retenues au plafond (la premiere passe toujours, regle EO-270)."""
    return ordonner(lecons, score_fn)[:max(1, int(plafond_nombre))]


def mode_critere(chemin_lecons):
    lecons, erreur = charger_lecons(chemin_lecons)
    if erreur:
        print("REFUS : " + erreur, file=sys.stderr)
        return 2
    poids = poids_idf(lecons)
    compte = frequences(lecons)
    communs = sorted(compte.items(), key=lambda x: (-x[1], x[0]))[:10]
    rares = sorted(compte.items(), key=lambda x: (x[1], x[0]))[:10]
    print("Corpus : " + str(len(lecons)) + " lecons, " + str(len(compte))
          + " tags distincts")
    print("Tags COMMUNS (faible pouvoir : presents partout) :")
    for tag, df in communs:
        print("  " + tag + " : df=" + str(df) + " idf=" + ("%.3f" % poids[tag]))
    print("Tags RARES (fort pouvoir : distinguent une lecon) :")
    for tag, df in rares:
        print("  " + tag + " : df=" + str(df) + " idf=" + ("%.3f" % poids[tag]))
    print("Lecture : le critere ACTUEL compte les tags (`porte` + `garde` = 2) sans")
    print("voir que ces deux-la ne distinguent presque rien. Le critere IDF pese la")
    print("RARETE : un tag rare partage avec le sujet vaut plus que trois tags communs.")
    return 0


def _sujet(mots, chemin_segments):
    """Le vocabulaire du sujet : mots du --mots + vocabulaire des SEGMENTS (couplage)."""
    vocab = vocabulaire_des_mots(mots)
    vocab_segments, avertissement = vocabulaire_des_segments(chemin_segments)
    return vocab | vocab_segments, bool(vocab_segments), avertissement


def mode_mesurer(chemin_lecons, mots, chemin_segments):
    lecons, erreur = charger_lecons(chemin_lecons)
    if erreur:
        print("REFUS : " + erreur, file=sys.stderr)
        return 2
    vocab, avec_segments, avertissement = _sujet(mots, chemin_segments)
    if avertissement:
        print("(" + avertissement + ")")
    if not vocab:
        print("REFUS : aucun mot de sujet (--mots vide) -- rien a mesurer.",
              file=sys.stderr)
        return 2
    pertinentes = [l for l in lecons if score_compte(l, vocab) > 0]
    endormies = [l for l in lecons if score_compte(l, vocab) == 0]
    print("Sujet : " + str(len(vocab)) + " mot(s)"
          + (" dont segments" if avec_segments else ""))
    print("  pertinentes (score > 0) : " + str(len(pertinentes)) + " sur "
          + str(len(lecons)))
    print("  endormies  (score = 0) : " + str(len(endormies)))
    print("Lecture : les ENDORMIES sont injectees par RECENCE seule, sans partager un")
    print("seul mot avec le sujet -- c est la part que le critere de pertinence doit")
    print("renvoyer au corpus pour faire de la place aux lecons du sujet.")
    return 0


def mode_avant_apres(chemin_lecons, mots, chemin_segments, plafond_nombre):
    lecons, erreur = charger_lecons(chemin_lecons)
    if erreur:
        print("REFUS : " + erreur, file=sys.stderr)
        return 2
    vocab, avec_segments, avertissement = _sujet(mots, chemin_segments)
    if avertissement:
        print("(" + avertissement + ")")
    if not vocab:
        print("REFUS : aucun mot de sujet (--mots vide) -- rien a mesurer.",
              file=sys.stderr)
        return 2
    poids = poids_idf(lecons)
    pertinentes_avant = [l for l in ordonner(lecons, lambda l: score_compte(l, vocab))
                         if score_compte(l, vocab) > 0][:plafond_nombre]
    pertinentes_apres = [l for l in ordonner(lecons, lambda l: score_idf(l, vocab, poids))
                         if score_idf(l, vocab, poids) > 0][:plafond_nombre]
    ids_avant = [str(l.get("id", "?")) for l in pertinentes_avant]
    ids_apres = [str(l.get("id", "?")) for l in pertinentes_apres]
    print("Sujet : " + str(len(vocab)) + " mot(s)"
          + (" dont segments" if avec_segments else ""))
    print("AVANT (compte de tags), ordre des lecons du sujet : "
          + (", ".join(ids_avant) if ids_avant else "aucune"))
    print("APRES (poids IDF), ordre des lecons du sujet    : "
          + (", ".join(ids_apres) if ids_apres else "aucune"))
    changes = []
    for position, identifiant in enumerate(ids_apres):
        if identifiant in ids_avant and ids_avant.index(identifiant) != position:
            changes.append(identifiant + " " + str(ids_avant.index(identifiant) + 1)
                           + "->" + str(position + 1))
    entrees = [i for i in ids_apres if i not in ids_avant]
    sorties = [i for i in ids_avant if i not in ids_apres]
    print("PRIORISEES par l IDF (position avancee) : "
          + (", ".join(changes) if changes else "aucune"))
    print("ENTREES (IDF seul) : " + (", ".join(entrees) if entrees else "aucune")
          + " | SORTIES (compte seul) : " + (", ".join(sorties) if sorties else "aucune"))
    print("Lecture : a sujet egal, l IDF fait MONTER les lecons qui partagent les tags")
    print("les plus RARES -- celles qui parlent vraiment du sujet -- au lieu de celles")
    print("qui partagent le plus de tags communs.")
    return 0


def mode_auto_test():
    echecs = []

    def verifier(nom, condition, detail):
        print(("PASS" if condition else "FAIL") + " : " + nom + " -- " + detail)
        if not condition:
            echecs.append(nom)

    # Corpus factice : `commun`/`commun2` sont partages par beaucoup, `rare` par UNE
    # seule lecon, `ubiquitaire` par TOUTES (il ne distingue donc rien).
    lecons = [
        {"id": "A", "date": "2026-01-01", "tags": ["commun", "commun2", "ubiquitaire"]},
        {"id": "B", "date": "2026-01-02", "tags": ["rare", "ubiquitaire"]},
        {"id": "C", "date": "2026-01-03", "tags": ["commun", "commun2", "ubiquitaire"]},
        {"id": "D", "date": "2026-01-04", "tags": ["commun", "commun2", "ubiquitaire"]},
        {"id": "E", "date": "2026-01-05", "tags": ["commun", "ubiquitaire"]},
        {"id": "F", "date": "2026-01-06", "tags": ["commun", "ubiquitaire"]},
        {"id": "G", "date": "2026-01-07", "tags": ["commun2", "ubiquitaire"]},
        {"id": "H", "date": "2026-01-08", "tags": ["ubiquitaire"]},
    ]
    poids = poids_idf(lecons)
    vocab = {"commun", "commun2", "rare"}
    ids_compte = [l["id"] for l in ordonner(lecons, lambda l: score_compte(l, vocab))]
    ids_idf = [l["id"] for l in ordonner(lecons, lambda l: score_idf(l, vocab, poids))]
    verifier("contre-temoin (le compte epargne)",
             ids_compte.index("A") < ids_compte.index("B"),
             "le compte met A(2 tags) avant B(1) : " + str(ids_compte))
    verifier("cobaye (l IDF mord)",
             ids_idf.index("B") < ids_idf.index("A"),
             "l IDF met B(tag rare) avant A : " + str(ids_idf))
    verifier("tag ubiquitaire = 0", poids["ubiquitaire"] <= 0.0001,
             "idf(ubiquitaire) = " + ("%.3f" % poids["ubiquitaire"]))
    maximum = math.log(len(lecons))
    verifier("tag rare = max", abs(poids["rare"] - maximum) < 0.0001,
             "idf(rare) = " + ("%.3f" % poids["rare"]))
    hors = {"id": "Z", "tags": ["alpha", "beta"]}
    verifier("hors sujet = 0", score_compte(hors, vocab) == 0
             and score_idf(hors, vocab, poids) == 0.0,
             "une lecon sans tag du sujet reste a 0")
    if echecs:
        print("AUTO-TEST EN ECHEC : " + ", ".join(echecs))
        return 2
    print("AUTO-TEST VERT : l IDF mord sur le rare, le compte epargne le commun.")
    return 0


def _extraire_options(arguments):
    options = {"mots": "", "lecons": CHEMIN_LECONS_DEFAUT,
               "segments": CHEMIN_SEGMENTS_DEFAUT,
               "plafond-nombre": PLAFOND_NOMBRE_DEFAUT}
    i = 0
    while i < len(arguments):
        jeton = arguments[i]
        if jeton in ("--mots", "--lecons", "--segments", "--plafond-nombre"):
            if i + 1 >= len(arguments):
                raise ValueError("option " + jeton + " sans valeur")
            options[jeton[2:]] = arguments[i + 1]
            i += 2
        else:
            raise ValueError("option inconnue " + jeton
                             + " (attendu : --mots | --lecons | --segments | --plafond-nombre)")
    return options


def mode_emploi():
    print(__doc__.strip())
    return 0


def main():
    arguments = sys.argv[1:]
    if not arguments or arguments[0] in ("-h", "--aide", "aide"):
        return mode_emploi()
    mode = arguments[0]
    try:
        options = _extraire_options(arguments[1:])
    except ValueError as erreur:
        print("REFUS : " + str(erreur), file=sys.stderr)
        return 2
    if mode == "critere":
        return mode_critere(options["lecons"])
    if mode == "mesurer":
        return mode_mesurer(options["lecons"], options["mots"], options["segments"])
    if mode == "avant-apres":
        try:
            plafond = int(options["plafond-nombre"])
        except ValueError:
            print("REFUS : --plafond-nombre attend un entier.", file=sys.stderr)
            return 2
        return mode_avant_apres(options["lecons"], options["mots"],
                                options["segments"], plafond)
    if mode == "auto-test":
        return mode_auto_test()
    print("REFUS : mode inconnu '" + mode
          + "' (attendu : critere | mesurer | avant-apres | auto-test).", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
