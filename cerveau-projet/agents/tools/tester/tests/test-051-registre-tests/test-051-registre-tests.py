#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-051-registre-tests.py
GARDE-FOU : le registre-tests (trace des lancements de tests par les agents)
existe et fonctionne. Le lanceur tester-lancer-non-regression v0.3.1 journalise
CHAQUE test execute dans cerveau-projet/agents/traces/registre-tests.jsonl
(date, agent, serie, test, verdict, duree) quand --agent est fourni - et
UNIQUEMENT dans ce cas. Le registre-tests est DISTINCT de
registre-usages-outils.jsonl (jamais melanges).

Contexte (demande utilisateur 2026-08-14) : comme le registre-usages-outils
trace l utilisation des outils, chaque lancement de tests par un agent doit
laisser une trace dans un registre dedie. La mission a ete realisee par
Vulcain (outil v0.3.1) puis verifiee ici.

Cas couverts:
  1. Le lanceur est v0.3.1 (--version)
  2. L aide contient l option --agent
  3. Le registre-tests est DISTINCT de registre-usages-outils (chemins differents)
  4. PREUVE REELLE positive : run --series a --agent X -> des entrees creees
     avec le bon agent et la bonne serie
  5. PREUVE REELLE negative : run sans --agent -> AUCUNE nouvelle entree
  6. Les entrees ont les champs attendus (date, agent, serie, test, verdict, duree)
  7. Normes : ASCII strict + LF pur (test + lanceur + registre)
"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

LANCER = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression",
                      "tester-lancer-non-regression.py")
TRACES = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces")
REG_TESTS = os.path.join(TRACES, "registre-tests.jsonl")
REG_USAGES = os.path.join(TRACES, "registre-usages-outils.jsonl")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
POINT_ACTIF = None
DESACTIVES = set()


def chrono_etape(nom, duree):
    print("  [chrono] %-40s %.2fs" % (nom, duree))


def verifier(nom, ok, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if POINT_ACTIF is not None and NB_POINTS != POINT_ACTIF:
        return
    if NB_POINTS in DESACTIVES:
        print("  [DESACTIVE] %s" % nom)
        return
    if ok:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(commande):
    res = PROTECTIONS.lancer_protege(commande, timeout=180)
    return res.stdout if res is not None else ""


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def compter_crlf(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def nb_entrees(chemin):
    if not os.path.isfile(chemin):
        return 0
    return sum(1 for l in io.open(chemin, encoding="utf-8") if l.strip())


def main():
    global POINT_ACTIF, DESACTIVES
    t0 = time.time()
    import argparse
    ap = argparse.ArgumentParser(description="test-051 registre-tests")
    ap.add_argument("--isoler", type=int, default=None)
    ap.add_argument("--desactiver", default="")
    ap.add_argument("--chrono", action="store_true")
    args = ap.parse_args()
    POINT_ACTIF = args.isoler
    DESACTIVES = set(int(x) for x in args.desactiver.split(",") if x.strip())

    # 1. Version du lanceur
    out = run([sys.executable, LANCER, "--version"])
    verifier("1. lanceur v0.3.1 (--version)", "v0.3.1" in out, out.strip())

    # 2. Option --agent dans l aide
    out = run([sys.executable, LANCER, "--help"])
    verifier("2. option --agent dans l aide", "--agent" in out and
             "registre-tests" in out, out.strip()[:80])

    # 3. Registre-tests DISTINCT de registre-usages-outils
    distinct = (REG_TESTS != REG_USAGES and
                os.path.dirname(REG_TESTS) == os.path.dirname(REG_USAGES))
    verifier("3. registre-tests distinct de registre-usages-outils",
             distinct, "%s vs %s" % (REG_TESTS, REG_USAGES))

    # 4-6. Preuves reelles : run --series a avec et sans --agent
    avant = nb_entrees(REG_TESTS)
    nom_tmp = "tmp-t051"
    out = run([sys.executable, LANCER, "--series", "a", "--agent", nom_tmp,
               "--journal", "--tests", "test-001"])
    apres = nb_entrees(REG_TESTS)
    ok = apres > avant
    detail = "avant=%d apres=%d" % (avant, apres)
    if ok:
        # verifier l entree de l agent de test (le registre est trie
        # decroissant : la derniere ligne est la plus ANCIENNE)
        lignes = [l for l in io.open(REG_TESTS, encoding="utf-8") if l.strip()]
        entrees = [json.loads(l) for l in lignes]
        trouves = [e for e in entrees if e.get("agent") == nom_tmp]
        if trouves:
            e = trouves[0]  # la plus recente (tri decroissant)
            champs = all(k in e for k in
                         ("date", "agent", "serie", "test", "verdict", "duree"))
            ok = (e.get("serie") == "a" and champs)
            detail = "entree agent=%s serie=%s" % (e.get("agent"),
                                                   e.get("serie"))
        else:
            ok = False
            detail = "aucune entree de l agent %s" % nom_tmp
    verifier("4. run --agent cree des entrees dans registre-tests", ok, detail)

    # 5. Preuve negative : run SANS --agent -> aucune nouvelle entree
    avant = nb_entrees(REG_TESTS)
    out = run([sys.executable, LANCER, "--series", "a", "--journal",
               "--tests", "test-001"])
    apres = nb_entrees(REG_TESTS)
    verifier("5. run sans --agent : aucune nouvelle entree",
             apres == avant, "avant=%d apres=%d" % (avant, apres))

    # 6. Les champs des entrees (verifies au point 4 pour la derniere entree)
    verifier("6. entrees avec champs (date/agent/serie/test/verdict/duree)", True)

    # 7. Registre-tests trie decroissant par date (anti-regression du tri)
    lignes = [l for l in io.open(REG_TESTS, encoding="utf-8") if l.strip()]
    dates = []
    for l in lignes:
        try:
            dates.append(json.loads(l).get("date", ""))
        except ValueError:
            continue
    trie = dates == sorted(dates, reverse=True)
    verifier("7. registre-tests trie decroissant par date", trie,
             "%d entrees" % len(dates))

    # 8. Nettoyage : le test NE DOIT PAS laisser ses preuves tmp-t051 dans le
    # registre (artefact a chaque run, decouverte Janus 2026-08-14 : 5 entrees
    # par non-regression). On reecrit le registre sans les lignes de l agent
    # de test, en preservant le tri decroissant (regle v0.3.1) et le LF pur.
    # Detection par json.loads (robuste au format espaces/sans espaces).
    lignes = [l for l in io.open(REG_TESTS, encoding="utf-8") if l.strip()]

    def est_preuve(l):
        try:
            return json.loads(l).get("agent") == nom_tmp
        except ValueError:
            return False

    gardees = [l for l in lignes if not est_preuve(l)]
    if len(gardees) != len(lignes):
        with io.open(REG_TESTS, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(gardees) + ("\n" if gardees else ""))
    apres_nettoyage = sum(1 for l in io.open(REG_TESTS, encoding="utf-8")
                          if l.strip() and est_preuve(l))
    verifier("8. le test nettoie ses preuves tmp-t051 (0 restante)",
             apres_nettoyage == 0, "restantes=%d" % apres_nettoyage)

    # 9-10. Normes
    fichiers = [os.path.abspath(__file__), LANCER]
    na = sum(compter_non_ascii(f) for f in fichiers)
    cr = sum(compter_crlf(f) for f in fichiers)
    verifier("9. ASCII strict : 0 non-ASCII (test + lanceur)", na == 0,
             "na=%d" % na)
    verifier("10. LF pur : 0 CRLF (test + lanceur)", cr == 0, "crlf=%d" % cr)

    if args.chrono:
        chrono_etape("test-051 registre-tests", time.time() - t0)
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO,
                                                               NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
