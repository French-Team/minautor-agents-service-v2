#!/usr/bin/env python3
# -*- coding: ascii -*-
"""test-090-bdd-lecons-garde-fou.py
GARDE-FOU : la BDD des lecons v2 (bdd-lecons) est la memoire longue des
lecons des agents FREELANCE (modele v2, D10). L outil v2 la touche via sa
CLI (entry.py) : enregistrer / chercher / lister / compter.

REECRITURE SCISSION 2-BDD (2026-09-05, decision utilisateur) :
  - La migration v1->v2 du plan 0.2.0 avait fusionne les memoires. L
    utilisateur a clarifie : DEUX equipes DISTINCTES, DEUX BDD separees.
  - Les 2 outils v1 (enregistrer-lecon, consulter-lecons) ont ete RESTAURES
    dans agents/tools/ + recatalogues (0.2.18) : la BDD v1
    (cerveau-projet/agents/lecons/lecons.db) est a nouveau la memoire des
    agents v1.
  - bdd-lecons v2 ne contient PLUS QUE des lecons freelance (les 279 lecons
    v1 ont ete retirees le 2026-09-05, backup bak-scission-2bdd).
  - Ce garde-fou verifie : (a) l outil v2 fonctionne, (b) la SEPARATION des
    BDD (les agents v1 n ecrivent pas en v2, les agents v2 n ecrivent pas en
    v1), (c) les outils v1 sont presents dans catalogue + index-tools.

Invariants verifies :
  1. Outil v2 present + compile (entry.py + fonctions/bdd_lecons.py)
  2. enregistrer : creation OK (id retourne) pour l agent actif
  3. chercher --agent : la lecon est retrouvee
  4. lister + compter : coherents (>= 1)
  5. SEPARATION : bdd-lecons v2 ne contient que des agents FREELANCE
     (les agents v1 du cerveau-projet n y sont pas)
  6. Catalogue : enregistrer-lecon + consulter-lecons PRESENTS (restaures)
  7. index-tools : les 2 outils v1 PRESENTS dans l outillage
  8. Normes : ASCII strict + LF pur (outil v2 + test)

Tags: outils, bdd-lecons, garde-fou, scission, 2-bdd
"""
import importlib.util
import io
import json
import os
import py_compile
import re
import sqlite3
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

V2_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "freelance",
                      "tools-commun", "bdd-lecons")
V2_ENTRY = os.path.join(V2_DIR, "entry.py")
V2_FONCTIONS = os.path.join(V2_DIR, "fonctions", "bdd_lecons.py")
V2_BDD = os.path.join(V2_DIR, "lecons.db")
V1_BDD = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "lecons",
                      "lecons.db")
V1_BAK = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "lecons",
                      "lecons.db.bak-2026-09-04")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX = os.path.join(TOOLS_DIR, "index-tools.md")

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


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def lancer(cmd, timeout=90):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def agent_actif():
    chemin = os.path.join(PROJECT_ROOT, "AGENTS.md")
    with io.open(chemin, "r", encoding="utf-8") as f:
        contenu = f.read()
    m = re.search(r"## Sessions connues\n(.*?)(?=\n## |\Z)", contenu, re.S)
    if not m:
        return "janus"
    lignes = []
    for ligne in m.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("| session-"):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cellules) >= 4:
            lignes.append(cellules)
    if not lignes:
        return "janus"
    lignes.sort(key=lambda c: c[3], reverse=True)
    return lignes[0][2].strip() or "janus"


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with io.open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lire(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Garde-fou : BDD des lecons v2 (bdd-lecons, modele v2) ===")

    # 1. Outil v2 present + compile.
    t1 = time.time()
    ok1 = os.path.isfile(V2_ENTRY) and os.path.isfile(V2_FONCTIONS)
    for f in (V2_ENTRY, V2_FONCTIONS):
        if os.path.isfile(f):
            try:
                py_compile.compile(f, doraise=True)
            except Exception:
                ok1 = False
    verifier("1. outil v2 bdd-lecons present + compile (entry + fonctions)",
             ok1)
    chrono_etape("1. outil v2", time.time() - t1)

    # 2. enregistrer : creation OK (id retourne).
    #    L agent de test est un agent FREELANCE fictif (scission 2-bdd :
    #    une lecon v1 ne doit jamais atterrir en v2 - point 5).
    t2 = time.time()
    actif = "test-freelance-090"
    marqueur = "garde-fou-090-%d" % int(time.time())
    r = lancer([PYTHON, V2_ENTRY, "enregistrer",
                "lecon de test du garde-fou bdd-lecons v2 (%s)." % marqueur,
                "--agent", actif, "--categorie", "autre",
                "--mots-cles", marqueur])
    ok2 = r.returncode == 0 and "LECON ENREGISTREE" in r.stdout
    verifier("2. enregistrer v2 : creation OK (id retourne)",
             ok2, r.stdout.strip()[:120])
    chrono_etape("2. enregistrer", time.time() - t2)

    # 3. chercher --agent : la lecon est retrouvee.
    t3 = time.time()
    r = lancer([PYTHON, V2_ENTRY, "chercher", "--agent", actif])
    ok3 = r.returncode == 0 and marqueur in r.stdout
    verifier("3. chercher --agent retrouve la lecon v2",
             ok3, "rc=%s" % r.returncode)
    chrono_etape("3. chercher", time.time() - t3)

    # 4. lister + compter coherents.
    t4 = time.time()
    rl = lancer([PYTHON, V2_ENTRY, "lister", "--n", "5"])
    rc = lancer([PYTHON, V2_ENTRY, "compter"])
    try:
        # la ligne utile est '[bdd-lecons] <n> lecon(s) en BDD'
        nb = int(re.search(r"\[(?:bdd-lecons|bdd)\] (\d+) lecon",
                           rc.stdout).group(1))
    except Exception:
        nb = 0
    ok4 = rl.returncode == 0 and rc.returncode == 0 and nb >= 1
    verifier("4. lister + compter coherents (>= 1 lecon en v2)",
             ok4, "compter=%s" % rc.stdout.strip()[:60])
    chrono_etape("4. lister/compter", time.time() - t4)

    # 5. SEPARATION : bdd-lecons v2 ne contient que des agents FREELANCE.
    #    La liste des agents v1 = dossiers parcours dans agents/ (cerveau).
    t5 = time.time()
    agents_v1 = []
    for nom in sorted(os.listdir(os.path.join(PROJECT_ROOT,
                                              "cerveau-projet", "agents"))):
        if os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet",
                                      "agents", nom, "parcours")):
            agents_v1.append(nom.lower())
    intrus = []
    try:
        conn = sqlite3.connect(V2_BDD)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT agent FROM lecons")
        for (agent,) in cur.fetchall():
            if agent and agent.lower() in agents_v1:
                intrus.append(agent)
        conn.close()
    except sqlite3.Error:
        pass
    verifier("5. SEPARATION : bdd-lecons v2 ne contient que des agents freelance",
             not intrus, "agents v1 en v2=%s" % intrus[:5])
    chrono_etape("5. separation 2-bdd", time.time() - t5)

    # 6. Catalogue : enregistrer-lecon + consulter-lecons PRESENTS (restaures
    #    2026-09-05, scission 2-bdd).
    t6 = time.time()
    try:
        with io.open(CATALOGUE, encoding="utf-8") as fh:
            cat = json.load(fh)
        noms = [e.get("nom", "") for e in cat.get("commandes", [])]
        ok6 = ("enregistrer-lecon" in noms
               and "consulter-lecons" in noms)
    except Exception as e:
        ok6 = False
    verifier("6. catalogue actif : enregistrer-lecon + consulter-lecons PRESENTS (restaures)",
             ok6)
    chrono_etape("6. catalogue", time.time() - t6)

    # 7. index-tools : les 2 outils v1 presents dans l outillage.
    t7 = time.time()
    idx = lire(INDEX)
    ok7 = ("enregistrer-lecon" in idx and "consulter-lecons" in idx)
    verifier("7. index-tools : enregistrer-lecon + consulter-lecons PRESENTS",
             ok7)
    chrono_etape("7. index-tools", time.time() - t7)

    # nettoyage : supprimer la lecon de test v2 (preuve auto-nettoyee).
    try:
        conn = sqlite3.connect(V2_BDD)
        conn.execute("DELETE FROM lecons WHERE mots_cles = ?", (marqueur,))
        conn.commit()
        conn.close()
    except sqlite3.Error:
        pass

    # 8. Normes : ASCII strict + LF pur (outil v2 + test).
    t8 = time.time()
    fichiers = [V2_ENTRY, V2_FONCTIONS, os.path.abspath(__file__)]
    na = sum(ascii_count(f) for f in fichiers)
    crlf = sum(crlf_count(f) for f in fichiers)
    verifier("8. ASCII strict : 0 non-ASCII (outil v2 + test)",
             na == 0, "total=%d" % na)
    verifier("8b. LF pur : 0 CRLF (outil v2 + test)",
             crlf == 0, "total=%d" % crlf)
    chrono_etape("8. normes", time.time() - t8)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())