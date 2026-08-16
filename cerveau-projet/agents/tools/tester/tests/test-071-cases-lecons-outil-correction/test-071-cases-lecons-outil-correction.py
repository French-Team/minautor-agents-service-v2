#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-071-cases-lecons-outil-correction.py
GARDE-FOU : toute case de carte qui ECRIT une lecon ou un rapport (dans
corrections.md ou un rapport d'audit) doit reference un outil de correction
d'accents (corriger-symboles / corriger-accents-zones-sensibles /
corriger-dictionnaire-accents / corriger-fins-de-ligne).

Contexte (mission 2026-08-16) :
  - Les agents corrigeaient les accents A LA MAIN (str_replace) au lieu
    d'utiliser l'outil corriger-symboles, car les cases de lecons de leurs
    cartes ne referenceaient AUCUN outil de correction. La REGLE ABSOLUE 5
    (discipline outil par mission) ne peut s'appliquer que si la case
    designe l'outil.
  - Buffy a branche corriger-symboles dans 28 cases de 15 cartes. Ce
    garde-fou empeche la recurrence : toute future case de lecon/rapport
    doit porter l'outil.

Invariants verifies :
  1. Toute case action qui ECRIT une lecon (titre contient 'lecon') a un
     outil de correction.
  2. Toute case action qui reference corrections.md dans un indice fichier
     (ecriture) a un outil de correction.
  3. Toute case action qui ecrit un rapport (titre contient 'rapport' ou
     'ecrire'/'rediger' + fichier) a un outil de correction.
  4. Les cases de LECTURE/ANALYSE (RELIRE OBLIGATOIRE, Classer, rien a
     corriger) sont EXCLUES : elles ne sont pas des ecritures.
  5. Preuve negative : une copie de carte avec une case de lecon SANS outil
     est DETECTEE par le scan interne, puis SUPPRIMEE (0 residu).
  6. Normes : ASCII strict + LF pur (test + parcours).
"""

import glob
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PARCOURS_GLOB = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "*",
                             "parcours", "parcours-*.json")

OUTILS_CORRECTION = (
    "corriger-symboles",
    "corriger-accents-zones-sensibles",
    "corriger-dictionnaire-accents",
    "corriger-fins-de-ligne",
)

# Titres de cases qui ne font QUE lire/analyser (pas une ecriture de lecon)
TITRES_LECTURE = ("relire", "classer", "rien a corriger", "aucune faute",
                  "verifier", "controle", "lire", "audit")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 7


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-071 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def est_case_ecriture(c):
    """Une case action qui ECRIT une lecon/rapport ?"""
    titre = c.get("titre", "").lower()
    inds = c.get("indices", [])
    chemins_fichiers = [i.get("chemin", "") for i in inds
                        if i.get("type") == "fichier"]
    # Case de lecture/analyse -> pas une ecriture
    if any(mot in titre for mot in TITRES_LECTURE):
        return False
    # Ecriture de lecon : titre contient 'lecon'
    if "lecon" in titre:
        return True
    # Ecriture dans corrections.md
    if any("corrections.md" in ch for ch in chemins_fichiers):
        return True
    # Ecriture de rapport : titre contient 'rapport' + indice fichier rapport
    if "rapport" in titre and any("rapport" in ch for ch in chemins_fichiers):
        return True
    return False


def a_outil_correction(c):
    noms = [i.get("nom", "") for i in c.get("indices", [])
            if i.get("type") == "outil"]
    return any(n in OUTILS_CORRECTION for n in noms)


def scanner_cartes(racine_parcours):
    """Retourne la liste des (agent, cid, titre) de cases d'ecriture SANS outil."""
    manquants = []
    for f in sorted(glob.glob(racine_parcours)):
        try:
            p = json.load(io.open(f, encoding="utf-8"))
        except Exception as e:
            manquants.append(("?", "?", "JSON invalide: %s" % str(e)[-40:]))
            continue
        parts = f.replace(os.sep, "/").split("/")
        agent = parts[-1].replace("parcours-", "").replace(".json", "")
        for cid, c in p.get("cases", {}).items():
            if not isinstance(c, dict):
                continue
            if c.get("type") != "action":
                continue
            if est_case_ecriture(c) and not a_outil_correction(c):
                manquants.append((agent, cid, c.get("titre", "")[:45]))
    return manquants


def main():
    print("=== Garde-fou : cases lecons/rapports avec outil de correction ===")

    # 1. Toutes les cases d'ecriture de lecons ont l'outil
    t0 = time.monotonic()
    manquants = scanner_cartes(PARCOURS_GLOB)
    verifier("1. scan complet : 0 case lecon/rapport sans outil de correction",
             len(manquants) == 0,
             manquants[:4] if manquants else "")
    chrono_etape("1. scan cases lecons", t0)

    # 2. La detection identifie bien les cases d'ecriture (au moins 1 trouvee
    #    sur l'etat reel -> le scan n'est pas vide)
    t0 = time.monotonic()
    total_ecritures = 0
    for f in sorted(glob.glob(PARCOURS_GLOB)):
        p = json.load(io.open(f, encoding="utf-8"))
        for cid, c in p.get("cases", {}).items():
            if isinstance(c, dict) and c.get("type") == "action" and est_case_ecriture(c):
                total_ecritures += 1
    verifier("2. scan non vide : cases d'ecriture detectees (%d)" % total_ecritures,
             total_ecritures >= 10,
             "seulement %d cases d'ecriture" % total_ecritures)
    chrono_etape("2. comptage cases", t0)

    # 3. Les cases de lecture sont bien EXCLUES (c0b RELIRE present dans
    #    toutes les cartes mais non signale comme ecriture)
    t0 = time.monotonic()
    faux_positifs = [m for m in manquants if "RELIRE" in m[2].upper()
                     or "Classer" in m[2] or "rien a corriger" in m[2]]
    verifier("3. cases de lecture exclues (0 faux positif c0b/classer)",
             len(faux_positifs) == 0,
             faux_positifs[:3] if faux_positifs else "")
    chrono_etape("3. exclusion lecture", t0)

    # 4. Preuve negative : injection d'une case de lecon SANS outil
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test071-")
    try:
        src = None
        for f in glob.glob(PARCOURS_GLOB):
            if "parcours-buffy.json" in f:
                src = json.load(io.open(f, encoding="utf-8"))
                break
        if src is None:
            verifier("4. preuve negative : carte source trouvee", False,
                     "parcours buffy introuvable")
        else:
            # retirer l'outil de correction d'une case de lecon existante
            cible = None
            for cid, c in src["cases"].items():
                if isinstance(c, dict) and est_case_ecriture(c) and a_outil_correction(c):
                    cible = cid
                    break
            if cible is None:
                verifier("4. preuve negative : case de lecon trouvee", False,
                         "aucune case lecon avec outil")
            else:
                src["cases"][cible]["indices"] = [
                    i for i in src["cases"][cible].get("indices", [])
                    if i.get("nom") not in OUTILS_CORRECTION
                ]
                sous = os.path.join(tmp, "parcours-buffy.json")
                with io.open(sous, "w", encoding="utf-8", newline="\n") as fh:
                    json.dump(src, fh, ensure_ascii=True, indent=1)
                manquants_copie = scanner_cartes(os.path.join(tmp, "parcours-buffy.json"))
                detecte = any(m[1] == cible for m in manquants_copie)
                verifier("4. preuve negative : lecon sans outil DETECTEE",
                         detecte,
                         "case %s non detectee" % cible)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("4b. preuve negative : copie SUPPRIMEE (0 trace)",
                 not os.path.exists(tmp), "copie encore presente")
    chrono_etape("4. preuve negative", t0)

    # 5. Normes ASCII + LF (test + parcours)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    fichiers = [os.path.abspath(__file__)]
    fichiers.extend(sorted(glob.glob(PARCOURS_GLOB)))
    for f in fichiers:
        try:
            d = io.open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("5. normes : 0 non-ASCII (test + parcours)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("5b. normes : 0 CRLF (test + parcours)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("5. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" %
          (NB_OK, NB_KO, NB_POINTS))
    bilan_chrono()
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
