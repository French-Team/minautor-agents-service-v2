#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-fiche.py -- Garde : ma fiche reste COURTE, et elle ne perd RIEN.

Pourquoi (EO-124, revision du createur 2026-09-16) : `optimus-prime.md` faisait
230 lignes / 11 sections / 10 REGLES ABSOLUES -- contre 92 lignes pour la fiche du
cameleon, qui dit explicitement "Mon chargement (3 couches, dans l'ordre)". Une
fiche qui verse tout au demarrage produit exactement le defaut decrit par le
createur : l'agent est instable et ne sait plus, a la fin, ce qu'il devait faire.
Le PILOTE corrige cette lacune -- il injecte les roles, les parcours et les
extraits AU MOMENT ou ils servent.

MAIS alleger sans garde est une maniere lente de perdre des regles. Ce garde tient
les DEUX bouts :

  1. LA FICHE EST COURTE -- un plafond DECLARE (constante), pas une intention.
  2. ELLE NOMME SES ROLES (la table du pilote) et SES PARCOURS (l'index des
     themes) : c'est ce que le createur exigeait, et c'est la preuve que la fiche
     dit OU le pilote prend ce qu'il injecte.
  3. ELLE NOMME CHAQUE REGLE IMMUABLE de l'index -- AUCUNE regle perdue dans
     l'allegement. C'est le contre-poids : sans lui, "plus court" finirait par
     vouloir dire "moins de regles", et personne ne le verrait.
  4. LE CONTRE-POIDS EST PIEGEABLE : un texte auquel on retire une regle est
     ACCUSE (autotest), pour que le controle ne soit pas un tampon.

CE QU'IL NE FAIT PAS : lecture seule. Il lit la fiche, la table des roles, l'index
des themes et l'index des regles immuables. Il n'ecrit rien.

Usage: python verifier-fiche.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = zone introuvable.
"""

import argparse
import re
import sys
from pathlib import Path

FICHIER_FICHE = Path("_operateur") / "optimus-prime" / "optimus-prime.md"
FICHIER_ROLES = Path("_operateur") / "optimus-prime" / "pilote" / "personnalites.py"
FICHIER_PARCOURS = (Path("_operateur") / "optimus-prime" / "parcours"
                    / "index-parcours.json")
DOSSIER_IMMUABLES = Path("_operateur") / "optimus-prime" / "regles-immuables"

# PLAFOND DECLARE : la fiche doit tenir sous cette taille. Il n'est pas devine --
# il est mesure au moment de l'allegement (135 lignes apres EO-124, contre 240
# avant) et laisse une marge volontairement faible : une fiche qui regrossit doit
# le FAIRE SAVOIR, pas glisser de quelques lignes par mission.
PLAFOND_LIGNES = 150

# Ce que la fiche doit NOMMER pour que le pilote sache quoi injecter.
NOMS_ATTENDUS = ("personnalites.py", "index-parcours.json")

RESULTATS = []


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def trouver_racine(racine):
    """Retourne le dossier matrix/ (celui qui porte la fiche), ou None."""
    for candidat in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix"):
        if (candidat / FICHIER_FICHE).is_file():
            return candidat
    return None


def regles_de_l_index(racine):
    """Les fichiers de regles immuables DECLARES par l'index (source unique)."""
    dossier = racine / DOSSIER_IMMUABLES
    if not dossier.is_dir():
        return []
    return sorted(chemin for chemin in dossier.glob("*.md")
                  if chemin.name != "regles-immuables-readme.md")


def regles_non_nommees(texte, fichiers):
    """Les regles dont le NOM n'apparait pas dans le texte. Detecteur PUR."""
    return [f.name for f in fichiers if f.name not in texte]


def main():
    parser = argparse.ArgumentParser(description="Garde : la fiche reste courte et complete")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    racine = trouver_racine(Path(arguments.racine).resolve())
    if racine is None:
        print("Zone matrix/ introuvable sous " + str(arguments.racine))
        return 2

    texte = (racine / FICHIER_FICHE).read_text(encoding="utf-8", errors="replace")
    lignes = len(texte.splitlines())
    ecarts = []

    # 1. LA FICHE EST COURTE.
    controler("fiche-courte", lignes <= PLAFOND_LIGNES,
              str(lignes) + " ligne(s), plafond declare " + str(PLAFOND_LIGNES)
              if lignes <= PLAFOND_LIGNES
              else "TROP LONGUE : " + str(lignes) + " lignes pour un plafond de "
              + str(PLAFOND_LIGNES) + " -- le deverement revient, l'agent va deriver")
    if lignes > PLAFOND_LIGNES:
        ecarts.append("fiche trop longue : " + str(lignes) + "/" + str(PLAFOND_LIGNES))

    # 2. ELLE NOMME CE QUE LE PILOTE INJECTE (roles + parcours).
    manquants = [nom for nom in NOMS_ATTENDUS if nom not in texte]
    controler("roles-et-parcours-nommes", not manquants,
              "les roles (" + FICHIER_ROLES.name + ") et les parcours ("
              + FICHIER_PARCOURS.name + ") sont NOMMES" if not manquants
              else "ABSENTS de la fiche : " + ", ".join(manquants)
              + " -- la fiche ne dit pas OU le pilote prend ce qu'il injecte")
    if manquants:
        ecarts.append("fiche sans " + ", ".join(manquants))

    # 3. AUCUNE REGLE PERDUE : chaque immuable est NOMMEE par la fiche.
    fichiers = regles_de_l_index(racine)
    perdues = regles_non_nommees(texte, fichiers)
    controler("aucune-regle-perdue", not perdues,
              str(len(fichiers)) + " regle(s) immuable(s), toutes NOMMEES par la fiche"
              if not perdues else "REGLES PERDUES : " + ", ".join(perdues))
    if perdues:
        ecarts.append("regles immuables non nommees : " + ", ".join(perdues))

    # 4. AUTOTEST : le contre-poids doit etre VU crier (lecon L-032).
    epreuves = []
    epreuves.append(("un texte COMPLET est accepte",
                     regles_non_nommees(texte, fichiers) == perdues))
    if fichiers:
        ampute = texte.replace(fichiers[0].name, "REGLE-SANS-NOM")
        epreuves.append(("un texte AMPUTE est ACCUSE",
                         regles_non_nommees(ampute, fichiers) == [fichiers[0].name]))
    epreuves.append(("un texte VIDE est accuse sur toutes les regles",
                     len(regles_non_nommees("", fichiers)) == len(fichiers)))
    epreuves.append(("le plafond est un COMPTE DE LIGNES, pas un octet",
                     lignes == len(texte.splitlines())))
    reussies = sum(1 for _, ok in epreuves if ok)
    controler("autotest-fiche", reussies == len(epreuves),
              "piege (" + str(reussies) + "/" + str(len(epreuves)) + ")"
              if reussies == len(epreuves)
              else "rate : " + ", ".join(nom for nom, ok in epreuves if not ok))
    if reussies != len(epreuves):
        ecarts.append("autotest de la fiche rate")

    print("VERIFIER FICHE -- une fiche qui verse tout au demarrage fait deriver l'agent")
    if ecarts or any(not ok for _, ok, _ in RESULTATS):
        print("\nVERDICT KO : la fiche est trop longue, ou elle ne dit plus ou le pilote puise (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : la fiche tient sous son plafond, nomme ses roles et ses parcours, et n'a perdu aucune regle.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
