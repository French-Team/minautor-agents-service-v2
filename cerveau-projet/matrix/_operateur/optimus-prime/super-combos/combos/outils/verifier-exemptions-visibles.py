#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-exemptions-visibles.py -- Garde : une exemption MUETTE est un angle mort

Pourquoi (2026-09-13, MO-075 / EO-103) : `corriger-ascii` ecartait EN SILENCE
tout fichier de contenu hors du champ de reecriture -- les BDD sous etalon
`.sha256` et tous les journaux `.jsonl` -- sans jamais dire qu'il excluait. Le
rapport laissait donc croire que le scan couvrait tout : mesure, 545 fichiers
reecrivables contre 577 vus (577 pour garde-ascii) ; l'angle mort de 32 fichiers
etait invisible. La reparation : l'exemption est NOMMEE (une fonction de
classement) et RAPPORTEE (chaque fichier + son motif), sans qu'aucun d'eux ne
soit reecrit.

Ce garde exige que l'exemption reste VISIBLE. Il est BLOQUANT : sans lui, une
refonte peut remettre l'exclusion muette et personne ne s'en plaindra -- c'est
precisement l'etat qui a vecu jusqu'a EO-103.

CE QU'IL NE FAIT PAS : il ne lance AUCUNE application (`--appliquer`) et n'ecrit
RIEN : il lit le classement, l'interroge sur le disque, et relit le rapport.

Usage: python verifier-exemptions-visibles.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine ou outil introuvable.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# --- REFERENCES (aucune valeur en dur ailleurs que dans cette table) ---------
OUTIL = ("matrice", "data", "outils", "corriger-ascii")
SUFFIXE_ETALON = ".sha256"
EXTENSION_JOURNAL = ".jsonl"
# MO-102 (P5 de la revue MO-098) : le plafond d'un sous-processus est LU chez
# son proprietaire (data/commun/lancement.py), jamais recopie ici.

RESULTATS = []


def trouver_matrix(racine):
    """Retourne le dossier matrix/, ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / "matrice").is_dir():
            return candidat
    return None


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)


def main():
    parser = argparse.ArgumentParser(description="Garde : l'exemption de reecriture est visible")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2
    # data/commun sur sys.path (motif M-076) : le plafond d'un sous-processus a
    # son domicile unique (lancement.py), il n'est jamais recopie ici.
    sys.path.insert(0, str(matrix / "matrice" / "data" / "commun"))
    outil = matrix.joinpath(*OUTIL)
    if not (outil / "main.py").is_file():
        print("Outil introuvable : " + str(outil))
        return 2

    print("VERIFIER EXEMPTIONS VISIBLES -- une exemption muette est un angle mort")

    sys.path.insert(0, str(outil))
    try:
        import constants
        from corriger import fonctions as corriger_fonctions
    except Exception as erreur:  # noqa: BLE001 -- on AVOUE l'echec, on ne plante pas
        print("ECART : outil illisible : " + str(erreur))
        return 1

    ecarts = []

    # 0. Le classement EXISTE (l'exemption est nommee, pas un `continue` muet).
    classer = getattr(corriger_fonctions, "classer_fichiers_cibles", None)
    controler("classement", callable(classer),
              "classer_fichiers_cibles presente" if callable(classer) else "ABSENTE")
    if not callable(classer):
        return 1

    cibles, exemptes = classer()
    noms_cibles = set(cibles)
    noms_exemptes = [chemin for chemin, _ in exemptes]

    # 1. Les deux familles sont DISJOINTES et MOTIVEES (et le motif est verifie
    #    sur le disque, pas cru sur parole).
    controler("disjoints", not (noms_cibles & set(noms_exemptes)),
              str(len(cibles)) + " cibles, " + str(len(exemptes)) + " exemptes")
    if noms_cibles & set(noms_exemptes):
        ecarts.append("un fichier est a la fois cible et exempte")
    justifiees = all(
        os.path.exists(chemin + SUFFIXE_ETALON) or chemin.endswith(EXTENSION_JOURNAL)
        for chemin in noms_exemptes
    )
    controler("motifs-reels", justifiees, "chaque exempte a son motif sur le disque")
    if not justifiees:
        ecarts.append("une exemption n'est pas justifiee par le disque")
    motifs = sorted({motif for _, motif in exemptes})
    controler("deux-motifs", len(motifs) == 2, " | ".join(motifs) if motifs else "aucun")
    if len(motifs) != 2:
        ecarts.append("les deux motifs d'exemption ne sont pas tous declares")

    # 2. La chaine d'ECRITURE ne voit que des cibles : aucun exempte ne peut etre
    #    reecrit par construction (preuve structurelle, insensible aux ecrivains
    #    concurrents d'un journal vivant).
    vus = {chemin for chemin, _ in corriger_fonctions.collecter_ecarts()}
    controler("chaine-ecriture", vus.issubset(noms_cibles),
              str(len(vus)) + " fichier(s) rendus par le scan des cibles")
    if not vus.issubset(noms_cibles):
        ecarts.append("la chaine d'ecriture a vu un fichier hors des cibles")

    # 3. Le RAPPORT REEL nomme chaque exempte (l'exemption est VISIBLE).
    from lancement import delai_sous_processus  # data/commun installe par main()
    passe = subprocess.run(
        [sys.executable, str(outil / "main.py"), "corriger"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=delai_sous_processus(),
    )
    sortie = (passe.stdout or "") + (passe.stderr or "")
    absents = [chemin for chemin in noms_exemptes if chemin not in sortie]
    controler("rapport-nomme-tout",
              not absents and passe.returncode == 0,
              str(len(noms_exemptes) - len(absents)) + "/" + str(len(noms_exemptes))
              + " nommes (code " + str(passe.returncode) + ")")
    if absents:
        ecarts.append(str(len(absents)) + " exempte(s) non nomme(s) dans le rapport")

    # 4. AUTO-TEST : l'ANCIENNE regle (etalon et journal ecartes en silence) ne
    #    nommait AUCUN exempte -- si elle les nommait, ce controle ne prouverait
    #    rien (lecon L-032 : un controle qu'on ne peut pas pieger ne prouve rien).
    anciennes = []
    for dossier in constants.DOSSIERS_CIBLES:
        if not dossier.exists():
            continue
        for racine, dossiers, fichiers in os.walk(dossier):
            dossiers[:] = [d for d in dossiers if d not in constants.DOSSIERS_EXCLUS]
            for nom in fichiers:
                if not nom.endswith(constants.EXTENSIONS_CIBLES):
                    continue
                if nom.endswith(constants.SUFFIXES_EXCLUS):
                    continue
                chemin = os.path.join(racine, nom)
                if os.path.exists(chemin + SUFFIXE_ETALON):
                    continue
                anciennes.append(chemin)
    muettes = [chemin for chemin in noms_exemptes if chemin in set(anciennes)]
    controler("autotest-muet", not muettes,
              str(len(noms_exemptes)) + " exemptes, " + str(len(muettes))
              + " vus par l'ancienne regle (elle etait muette)")
    if muettes:
        ecarts.append("l'ancienne regle n'etait pas muette : le controle ne prouve rien (L-032)")

    for ecart in ecarts:
        print("ECART : " + ecart)
    echecs = [nom for nom, ok, _ in RESULTATS if not ok]
    if ecarts or echecs:
        print("")
        print("VERDICT KO : l'exemption de reecriture n'est plus visible.")
        return 1
    print("")
    print("VERDICT OK : les exemptes sont nommes, motives et rapportes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
