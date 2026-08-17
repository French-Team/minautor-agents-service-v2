#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-022-budget-pondere.py
Test formel du BUDGET PONDERE des indices par case (valider-case v1.1.0).

Contexte (mission 2026-08-11) :
  - Vulcain a implemente le budget pondere des indices (decision utilisateur :
    2 indices courts = 1 indice long) dans valider-case v1.1.0 et
    generateurs-case v0.4.2.
  - Modele : indice COURT (texte <= 100 car. ou sans texte) = poids 0,5 ;
    indice LONG (texte > 100 car.) = poids 1 ; budget 3,0 par case.
  - Texte > 160 car. = plafond absolu d'un indice (inchange, independant).

Ce test verifie la FRONTIERE EXACTE 3,0 avec des cas limites : poids
exactement 3,0 (CONFORME), juste au-dessus 3,5 (A ALLEGER), 4,0 (A ALLEGER),
le plafond absolu 160 car. (signale meme si le poids <= 3,0), les bornes
du seuil court (100 = court, 101 = long) et les indices sans texte
(ref/outil = 0,5).

Cas couverts:
  1. 6 courts (50 car.) = 3,0 -> CONFORME (frontiere exacte)
  2. 3 longs (120 car.) = 3,0 -> CONFORME (frontiere exacte)
  3. 2 longs + 2 courts = 2*1 + 2*0,5 = 3,0 -> CONFORME
  4. 1 long + 4 courts = 1 + 2 = 3,0 -> CONFORME
  5. 5 courts + 1 long = 2,5 + 1 = 3,5 -> A ALLEGER (juste au-dessus)
  6. 3 longs + 1 court = 3 + 0,5 = 3,5 -> A ALLEGER
  7. 4 longs (120 car.) = 4,0 -> A ALLEGER
  8. Plafond absolu : 1 texte 200 car. + 2 courts = 1 + 1 = 2,0 (poids OK)
     mais texte > 160 -> A ALLEGER (plafond independant)
  9. Frontiere du seuil court : 6 x 100 car. exactement = 3,0 CONFORME ;
     4 x 101 car. = 4,0 A ALLEGER
 10. Indices SANS texte (ref/outil) = 0,5 : 6 refs = 3,0 -> CONFORME
 11. Temoin avec outil (commande, sans champ texte) : 6 outil = 3,0 -> CONFORME
 12. ASCII strict : 0 non-ASCII (test + parcours temoins)
 13. LF pur : 0 CRLF

Usage:
  python3 test-022-budget-pondere.py
Tags: conventions, budget, parcours
"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROTECTIONS = charger_protections()
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0, deploiement dynamique) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for _i, _arg in enumerate(sys.argv):
    if _arg == "--isoler" and _i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[_i + 1])
        except ValueError:
            pass
    if _arg == "--desactiver" and _i + 1 < len(sys.argv):
        for _p in sys.argv[_i + 1].split(','):
            try:
                DESACTIVES.append(int(_p))
            except ValueError:
                pass
ETAPES = []
T_START = __import__("time").monotonic()


def point_actif(numero):
    # True si le point N doit s executer (options on/off du test)
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    # Enregistre la duree d une etape (no-op si --no-chrono)
    if CHRONO_ACTIF:
        ETAPES.append((nom, __import__("time").monotonic() - t_debut))


def bilan_chrono():
    # Affiche le bilan des durees : total + detail par etape
    if not CHRONO_ACTIF:
        return
    _total = __import__("time").monotonic() - T_START
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)
    for _nom, _duree in ETAPES:
        print("  %-34s %6.2fs" % (_nom, _duree))


VALIDER_CASE = os.path.join(TOOLS_DIR, "valider", "valider-case", "valider-case.py")

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


def run(cmd, timeout=60):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def fabriquer_parcours(tmp, indices, nom):
    """Parcours minimal : c0 (question) -> c1 (action avec indices) -> c9 (fin)."""
    d = {
        "parcours": {"agent": nom, "version": "0.1.0", "case_depart": "c0"},
        "cases": {
            "c0": {"type": "question", "titre": "Depart", "question": "Tester ?",
                   "branches": [
                       {"reponse": "OUI", "vers": "c1"},
                       {"reponse": "NON", "vers": "c1"}]},
            "c1": {"type": "action", "titre": "Case indices", "indices": indices,
                   "suivant": "c9"},
            "c9": {"type": "fin", "titre": "Fin"},
        },
    }
    p = os.path.join(tmp, nom + ".json")
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(d, fh, ensure_ascii=True, indent=2)
    return p


def verdict_attendu(parcours):
    """Retourne ('CONFORME'|'A ALLEGER', nb_a_alleger) ou None si non lisible."""
    r = run([PYTHON, VALIDER_CASE, parcours, "--dry-run"])
    if r.returncode != 0:
        return None
    if "CONFORME" in r.stdout:
        return ("CONFORME", 0)
    if "A ALLEGER" in r.stdout:
        nb = 0
        if "a alleger:" in r.stdout:
            try:
                nb = int(r.stdout.split("a alleger:")[1].split("|")[0].strip())
            except ValueError:
                nb = -1
        return ("A ALLEGER", nb)
    return None


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-022-")
    try:
        print("=== Test formel budget pondere (frontiere 3,0) ===")

        # 1. 6 courts (50 car.) = 0,5*6 = 3,0 -> CONFORME
        p = fabriquer_parcours(tmp, [{"type": "regle", "texte": "R" * 50} for _ in range(6)], "t6courts")
        v = verdict_attendu(p)
        verifier("1. 6 courts (50 car.) = 3,0 : CONFORME",
                 v is not None and v[0] == "CONFORME" and v[1] == 0, str(v))

        # 2. 3 longs (120 car.) = 1*3 = 3,0 -> CONFORME
        p = fabriquer_parcours(tmp, [{"type": "regle", "texte": "R" * 120} for _ in range(3)], "t3longs")
        v = verdict_attendu(p)
        verifier("2. 3 longs (120 car.) = 3,0 : CONFORME",
                 v is not None and v[0] == "CONFORME" and v[1] == 0, str(v))

        # 3. 2 longs + 2 courts = 2*1 + 2*0,5 = 3,0 -> CONFORME
        ind = [{"type": "regle", "texte": "R" * 120} for _ in range(2)] + \
              [{"type": "regle", "texte": "R" * 50} for _ in range(2)]
        p = fabriquer_parcours(tmp, ind, "t2l2c")
        v = verdict_attendu(p)
        verifier("3. 2 longs + 2 courts = 3,0 : CONFORME",
                 v is not None and v[0] == "CONFORME" and v[1] == 0, str(v))

        # 4. 1 long + 4 courts = 1 + 4*0,5 = 3,0 -> CONFORME
        ind = [{"type": "regle", "texte": "R" * 120}] + \
              [{"type": "regle", "texte": "R" * 50} for _ in range(4)]
        p = fabriquer_parcours(tmp, ind, "t1l4c")
        v = verdict_attendu(p)
        verifier("4. 1 long + 4 courts = 3,0 : CONFORME",
                 v is not None and v[0] == "CONFORME" and v[1] == 0, str(v))

        # 5. 5 courts + 1 long = 2,5 + 1 = 3,5 -> A ALLEGER (juste au-dessus)
        ind = [{"type": "regle", "texte": "R" * 50} for _ in range(5)] + \
              [{"type": "regle", "texte": "R" * 120}]
        p = fabriquer_parcours(tmp, ind, "t5c1l")
        v = verdict_attendu(p)
        verifier("5. 5 courts + 1 long = 3,5 : A ALLEGER",
                 v is not None and v[0] == "A ALLEGER" and v[1] >= 1, str(v))

        # 6. 3 longs + 1 court = 3 + 0,5 = 3,5 -> A ALLEGER
        ind = [{"type": "regle", "texte": "R" * 120} for _ in range(3)] + \
              [{"type": "regle", "texte": "R" * 50}]
        p = fabriquer_parcours(tmp, ind, "t3l1c")
        v = verdict_attendu(p)
        verifier("6. 3 longs + 1 court = 3,5 : A ALLEGER",
                 v is not None and v[0] == "A ALLEGER" and v[1] >= 1, str(v))

        # 7. 4 longs (120 car.) = 4,0 -> A ALLEGER
        p = fabriquer_parcours(tmp, [{"type": "regle", "texte": "R" * 120} for _ in range(4)], "t4longs")
        v = verdict_attendu(p)
        verifier("7. 4 longs (120 car.) = 4,0 : A ALLEGER",
                 v is not None and v[0] == "A ALLEGER" and v[1] >= 1, str(v))

        # 8. Plafond absolu : 1 texte 200 car. + 2 courts = 1 + 1 = 2,0 (poids OK)
        #    mais le texte > 160 car. -> TOUJOURS signale -> A ALLEGER
        ind = [{"type": "regle", "texte": "R" * 200}] + \
              [{"type": "regle", "texte": "R" * 50} for _ in range(2)]
        p = fabriquer_parcours(tmp, ind, "tplafond")
        v = verdict_attendu(p)
        verifier("8. Plafond absolu : 1 texte 200 car. + 2 courts = A ALLEGER (texte > 160)",
                 v is not None and v[0] == "A ALLEGER" and v[1] >= 1, str(v))

        # 9a. Frontiere seuil : 6 x 100 car. EXACTEMENT = 6*0,5 = 3,0 -> CONFORME
        p = fabriquer_parcours(tmp, [{"type": "regle", "texte": "R" * 100} for _ in range(6)], "t6x100")
        v = verdict_attendu(p)
        verifier("9a. 6 x 100 car. exactement = 3,0 : CONFORME",
                 v is not None and v[0] == "CONFORME" and v[1] == 0, str(v))

        # 9b. Frontiere seuil : 4 x 101 car. = 4*1 = 4,0 -> A ALLEGER
        p = fabriquer_parcours(tmp, [{"type": "regle", "texte": "R" * 101} for _ in range(4)], "t4x101")
        v = verdict_attendu(p)
        verifier("9b. 4 x 101 car. = 4,0 : A ALLEGER",
                 v is not None and v[0] == "A ALLEGER" and v[1] >= 1, str(v))

        # 10. 6 refs (sans texte) = 6*0,5 = 3,0 -> CONFORME
        ind = [{"type": "ref", "ref": "pattern-%d" % n} for n in (1, 2, 3, 4, 5, 6)]
        p = fabriquer_parcours(tmp, ind, "t6refs")
        v = verdict_attendu(p)
        verifier("10. 6 refs (sans texte) = 3,0 : CONFORME",
                 v is not None and v[0] == "CONFORME" and v[1] == 0, str(v))

        # 11. 6 outil (commande, sans texte) = 6*0,5 = 3,0 -> CONFORME
        ind = [{"type": "outil", "nom": "outil%d" % n, "catalogue": "outil%d" % n,
                "chemin": "chemin/outil%d/" % n, "commande": "python3 outil%d.py" % n}
               for n in range(1, 7)]
        p = fabriquer_parcours(tmp, ind, "t6outils")
        v = verdict_attendu(p)
        verifier("11. 6 outil (sans texte) = 3,0 : CONFORME",
                 v is not None and v[0] == "CONFORME" and v[1] == 0, str(v))

        # 12. ASCII strict : 0 non-ASCII (test + parcours temoins generes)
        total_non_ascii = ascii_count(os.path.abspath(__file__))
        verifier("12. ASCII strict : 0 non-ASCII (test)", total_non_ascii == 0,
                 "total = %d" % total_non_ascii)

        # 13. LF pur : 0 CRLF (test)
        total_crlf = crlf_count(os.path.abspath(__file__))
        verifier("13. LF pur : 0 CRLF (test)", total_crlf == 0,
                 "total = %d" % total_crlf)

        print("")
        bilan_chrono()
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
