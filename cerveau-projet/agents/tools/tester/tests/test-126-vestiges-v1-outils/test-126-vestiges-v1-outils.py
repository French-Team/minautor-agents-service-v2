#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-126-vestiges-v1-outils.py

PISTAGE DES VESTIGES V1 (migration v1->v2, decision utilisateur 2026-09-05) :
seul l ARBRE v2 (arbre-<agent>.json + themes + fins) doit rester. Les outils
v1 centres sur les parcours (guider-parcours, editer-parcours, generateurs-
carte, generateurs-case, migrer-cases-relecture, detecter-cablages-manquants,
cartographier-parcours, valider-case) ont ete ARCHIVES dans
archive-outils-v1-parcours-2026-09-05/ et RETIRES du catalogue.

Ce test PISTE les vestiges : si un outil archive est de retour dans tools/,
s il reste un parcours-*.json v1 quelque part, ou si une structure v2
(arbre-*.json, theme-*.json, fins.json) reference encore un outil archive
ou un token de guidage v1 (guider-parcours, parcours-demarrage), le test
ECHOUE : c est un vestige a purger.

Points verifies :
  1. Les 8 outils v1 sont ABSENTS de tools/ (bien archives).
  2. Les 8 outils v1 sont PRESENTS dans archive-outils-v1-parcours-2026-09-05/.
  3. Aucun parcours-*.json v1 ne subsiste (agents/*/parcours/).
  4. Catalogue : 165 commandes, aucun outil archive present, version 0.2.21.
  5. REVERSE : zero reference aux outils archives / tokens v1 dans les
     structures v2 (arbre-*.json, theme-*.json, fins.json).
  6. La table d habilitation (agents/habilitation/) ne reference aucun outil
     archive ni guider-parcours.
  7. Normes : ASCII strict + LF pur sur les fichiers crees ici.
Tags: vestiges, v1, migration, reverse, garde-fou
"""
import glob
import io
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

AGENTS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
TOOLS = os.path.join(AGENTS, "tools")
ARCHIVE = os.path.join(AGENTS, "archive-outils-v1-parcours-2026-09-05")
CATALOGUE = os.path.join(TOOLS, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
HABILITATION = os.path.join(AGENTS, "habilitation")

OUTILS_ARCHIVES = [
    "guider-parcours", "editer-parcours", "generateurs-carte",
    "generateurs-case", "migrer-cases-relecture",
    "detecter-cablages-manquants", "cartographier-parcours", "valider-case",
]
TOKENS_V1 = ["guider-parcours", "parcours-demarrage"]

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test vestiges v1 : outils archives + parcours v1 ===")

    # 1. Les 8 outils ABSENTS de tools/
    presents = []
    for o in OUTILS_ARCHIVES:
        hits = glob.glob(os.path.join(TOOLS, "**", o), recursive=True)
        if hits:
            presents.append("%s:%s" % (o, os.path.basename(os.path.dirname(hits[0]))))
    verifier("1. 8 outils v1 ABSENTS de tools/", not presents,
             "presents: %s" % ", ".join(presents))

    # 2. Les 8 outils PRESENTS dans l archive
    absents_archive = [o for o in OUTILS_ARCHIVES
                       if not os.path.isdir(os.path.join(ARCHIVE, o))]
    verifier("2. 8 outils v1 PRESENTS dans l archive", not absents_archive,
             "manquants: %s" % ", ".join(absents_archive))

    # 3. Aucun parcours-*.json v1 ne subsiste
    vestiges = glob.glob(os.path.join(AGENTS, "*", "parcours", "parcours-*.json"))
    verifier("3. zero parcours-*.json v1 (agents/*/parcours/)", not vestiges,
             "vestiges: %s" % ", ".join(vestiges))

    # 4. Catalogue : 165 commandes, aucun outil archive, version 0.2.21
    with io.open(CATALOGUE, encoding="utf-8") as fh:
        cat = json.load(fh)
    noms = [c["nom"] for c in cat["commandes"]]
    dans_cat = [o for o in OUTILS_ARCHIVES if o in noms]
    ok_cat = (len(noms) == 165 and cat.get("version") == "0.2.21"
              and not dans_cat)
    verifier("4. catalogue 165, v0.2.21, sans outils archives", ok_cat,
             "nb=%d version=%s dans_cat=%s"
             % (len(noms), cat.get("version"), ", ".join(dans_cat)))

    # 5. REVERSE : zero reference outils archives / tokens v1 dans les
    # structures v2 (arbre-*.json, theme-*.json, fins.json)
    structures = glob.glob(os.path.join(AGENTS, "*", "parcours", "*.json"))
    structures = [s for s in structures if os.path.basename(s) != "arbre-.json"]
    refs = []
    for s in structures:
        base = os.path.basename(s)
        if not (base.startswith("arbre-") or base.startswith("theme-")
                or base == "fins.json"):
            continue
        try:
            contenu = io.open(s, encoding="utf-8", errors="replace").read()
        except IOError:
            continue
        for token in OUTILS_ARCHIVES + TOKENS_V1:
            if token in contenu:
                refs.append("%s:%s" % (base, token))
    verifier("5. zero reference v1 dans les structures v2", not refs,
             "refs: %s" % ", ".join(sorted(set(refs))[:10]))

    # 6. Table d habilitation : aucun outil archive ni guider-parcours
    refs_hab = []
    if os.path.isdir(HABILITATION):
        for f in sorted(os.listdir(HABILITATION)):
            if not f.endswith(".json"):
                continue
            with io.open(os.path.join(HABILITATION, f), encoding="utf-8") as fh:
                data = json.load(fh)
            for o in data.get("outils", []):
                if o in OUTILS_ARCHIVES or o == "guider-parcours":
                    refs_hab.append("%s:%s" % (f, o))
    verifier("6. table d habilitation sans outils v1", not refs_hab,
             "refs: %s" % ", ".join(sorted(set(refs_hab))[:10]))

    # 7. Normes : ASCII strict + LF pur sur ce fichier
    verifier("7. ASCII strict (ce test)", ascii_count(os.path.abspath(__file__)) == 0)
    verifier("7b. LF pur (ce test)", crlf_count(os.path.abspath(__file__)) == 0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())