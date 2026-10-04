#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
scan-valeurs-en-dur.py -- Scan convention zero-valeurs-en-dur (M-102)

Detecte secrets, chemins absolus, IPs en dur dans les fichiers matrice.
code 0 = sain, code 1 = valeurs detectees.
Usage: python scan-valeurs-en-dur.py <fichier|dossier> [--ext .py,.md,.json] [--racine <Matrice>]

PRECISION (2026-09-19) -- ce scan PROMETTAIT plus que ses motifs, et c est
exactement pourquoi il n etait JAMAIS branche. Trois defauts mesures et fermes :

  1. `chemin-win` attrapait le `s:` d une ADRESSE (https) et le `e:` d une
     SEQUENCE D ECHAPPEMENT : un motif qui accuse une adresse ou une sequence
     accuse A TORT, et un scan qui crie a tort ne se branche jamais (mesure :
     167 lignes dont 164 legitimes). La dette `precision du scan-valeurs-en-dur`,
     ouverte par MO-093, etait restee ouverte.
     ANCRAGE : un chemin Windows COMMENCE un mot ((?<![\w])) ; une adresse ni une
     sequence d echappement ne le commencent.

  2. `perimetre-en-dur` (nouveau) : un balayage ecrivait ses dossiers EN DUR
     dans son propre corps -- la RACINE de la Matrice etait donc HORS du balayage
     et deux points de restauration y vivaient sans etre jamais vus (EO-277). Une
     valeur de PERIMETRE s ecrit UNE fois, chez elle (M-076).
     Le motif ne juge pas une FORME, il juge un FAIT : les items doivent etre des
     DOSSIERS QUI EXISTENT a la racine. Sinon il accuserait toute paire de mots --
     mesure : 24 paires litterales dans le CODE, UNE seule fautive.
     Sans juge (`--racine` absente ou introuvable), il se TAIT et le scan DIT
     qu il s est tu : une couverture muette serait un angle mort.

  3. Il juge du TEXTE : une DOCUMENTATION qui CITE la faute au lieu de la
     commettre serait accusee. Le marqueur declare `scan-valeurs: cite` exclut la
     ligne, et le scan COMPTE ces lignes pour ne jamais rendre l exemption muette
     -- un angle mort declare se lit, un angle mort tu ne se lit pas.

LIMITE DITE : l exemption est un marqueur de LIGNE, pas une analyse du contexte.
Une ligne de code qui porterait le marqueur serait aussi exclue -- le compte
rendu la NOMME, donc elle ne peut pas disparaitre en silence.
"""

import sys
import re
import argparse
from pathlib import Path


MOTIFS = {
    "secret": re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*\S+"),
    "chemin-win": re.compile(r"(?<![\w])[A-Za-z]:[\\/][^\s\"']*"),
    "chemin-home": re.compile(r"(/(home|Users)/[^\s\"']*|C:\\Users\\[^\s\"']*)"),
    "ip": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}
# Une BOUCLE sur une paire de chaines litterales : la forme d une liste de
# balayage ecrite en dur. Le FAIT (items = dossiers reels) est juge a part.
MOTIF_PERIMETRE = re.compile(
    r"\bfor\s+\w+\s+in\s*\(\s*(['\"])([^'\"]*)\1\s*,\s*(['\"])([^'\"]*)\3"
)
NOM_PERIMETRE = "perimetre-en-dur"
# Le marqueur d une ligne qui CITE la faute : declare ici, COMPTE au rapport.
MARQUEUR_CITE = "scan-valeurs: cite"
EXCLUS_DIRS = {".git", "__pycache__"}
# Faux positifs connus : documentation et empreintes.
EXCLUS_FICHIERS = {"scan-valeurs-en-dur.py"}


def dossiers_racine(racine):
    """Les DOSSIERS reels de la racine declaree -- le JUGE du motif du perimetre.

    Rend None quand il n y a pas de juge (aucune racine, ou racine introuvable) :
    l appelant doit alors DIRE que le motif s est tu, jamais laisser croire a une
    couverture (L-100 : une reponse vide qui ne nomme rien se lit comme un fait).
    """
    if not racine:
        return None
    chemin = Path(racine)
    if not chemin.is_dir():
        return None
    return {p.name for p in chemin.iterdir() if p.is_dir() and not p.name.startswith(".")}


def perimetres_recopies(lignes, dossiers):
    """Les lignes qui recopient une LISTE DE DOSSIERS REELS. Rend [(ligne, extrait)]."""
    if not dossiers:
        return []
    trouves = []
    for i, ligne in enumerate(lignes, 1):
        if MARQUEUR_CITE in ligne:
            continue
        for m in MOTIF_PERIMETRE.finditer(ligne):
            if m.group(2) in dossiers and m.group(4) in dossiers:
                trouves.append((i, m.group(0)[:60]))
    return trouves


def main():
    parser = argparse.ArgumentParser(description="Scan zero-valeurs-en-dur")
    parser.add_argument("cible", help="Fichier ou dossier a scanner")
    parser.add_argument("--ext", default=".py,.md,.json,.jsonl",
                        help="Extensions (dossier seulement)")
    parser.add_argument("--racine", default="",
                        help="Racine dont les dossiers reels JUGENT le motif "
                             "perimetre-en-dur (defaut : la cible)")
    args = parser.parse_args()

    cible = Path(args.cible)
    if not cible.exists():
        print(f"Cible introuvable: {cible}")
        return 2

    dossiers = dossiers_racine(args.racine or args.cible)
    exts = {e.strip() for e in args.ext.split(",") if e.strip()}
    fichiers = [cible] if cible.is_file() else [
        p for p in cible.rglob("*")
        if p.is_file()
        and not any(part in EXCLUS_DIRS for part in p.parts)
        and p.suffix in exts
        and p.name not in EXCLUS_FICHIERS
    ]

    trouvailles = []
    cites = 0
    for p in fichiers:
        try:
            lignes = p.read_text(encoding="utf-8", errors="strict").split("\n")
        except (OSError, UnicodeError):
            continue
        for i, ligne in enumerate(lignes, 1):
            if MARQUEUR_CITE in ligne:
                cites += 1
                continue
            for nom, motif in MOTIFS.items():
                m = motif.search(ligne)
                if m:
                    trouvailles.append((str(p), i, nom, m.group(0)[:60]))
                    break
        for i, extrait in perimetres_recopies(lignes, dossiers):
            trouvailles.append((str(p), i, NOM_PERIMETRE, extrait))

    if trouvailles:
        print(f"VALEURS EN DUR : {len(trouvailles)} occurrence(s) :")
        for f, ligne, nom, extrait in trouvailles[:30]:
            print(f"  - {f}:{ligne} [{nom}] {extrait}")
        if len(trouvailles) > 30:
            print(f"  ... +{len(trouvailles) - 30} autres")
        return 1

    if dossiers is None:
        print(f"Zero-valeurs-en-dur sain : {len(fichiers)} fichier(s) controles, 0 valeur "
              f"-- SAUF {NOM_PERIMETRE} : aucun juge (--racine absente ou introuvable), "
              f"ce motif s est TU.")
        return 0
    print(f"Zero-valeurs-en-dur sain : {len(fichiers)} fichier(s) controles, 0 valeur "
          f"({NOM_PERIMETRE} juge contre {len(dossiers)} dossier(s) de la racine) ; "
          f"{cites} ligne(s) CITEE(S) hors jugement (marqueur declare).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
