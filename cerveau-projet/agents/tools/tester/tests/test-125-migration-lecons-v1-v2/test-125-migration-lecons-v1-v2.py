#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-125-migration-lecons-v1-v2.py
TEST DE LA MIGRATION v1->v2 (migration v1->v2, mission 85b4545d D.3) :
fixture lecons.db v1 -> bdd-lecons v2 via la commande migrer-v1.
Verifie comptage, doublons, mapping et rejeu idempotent (PAC-8).

NOTE SCISSION 2-BDD (2026-09-05, decision utilisateur) : la fusion v1->v2
a ete ANNULEE - les lecons v1 vivent dans lecons.db v1 (jamais en v2). Ce
test est CONSERVE comme preuve historique de la mecanique migrer-v1 (il
tourne sur une copie isolee, jamais contre la vraie BDD). La commande
migrer-v1 ne doit plus etre utilisee en production.

Approche : copie de l outil bdd-lecons (avec os_path + harnais) dans un
repertoire temporaire pour ne JAMAIS toucher la vraie BDD v2, puis
execution de migrer-v1 contre une fixture v1 dediee (5 lecons couvrant les
cas limites : titre vide, verdict vide, champs mission/outils).

Points verifies :
  1. fixture v1 : 5 lecons creees (dont 1 titre vide + 1 verdict vide)
  2. migrer-v1 : 5/5 importees (aucune perte, PAC-7)
  3. Rejeu : 0 lecon supplementaire (idempotent, PAC-8)
  4. Comptage cible : 5 lecons en v2, 0 doublon
  5. Mapping : titre/agent/date conserves, verdict+mission+outils fusionnes
     dans resume (format parseable, PAC-7)
  6. Titre vide derive de la lecon (titre_auto) - pas de perte
  7. Source = 'v1-lecons.db' sur les 5 lecons migrees
  8. Normes : ASCII strict + LF pur (test + fixture + outils copies)

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: migration, bdd-lecons, fixture, idempotence, garde-fou
"""
import io
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_COMMUN = os.path.join(PROJECT_ROOT, "cerveau-projet", "freelance",
                            "tools-commun")
BDD_LECONS = os.path.join(TOOLS_COMMUN, "bdd-lecons")
PYTHON = sys.executable

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


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def compter_crlf(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lire(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def creer_fixture_v1(chemin):
    """Fixture lecons.db v1 : 5 lecons couvrant les cas limites."""
    if os.path.exists(chemin):
        os.remove(chemin)
    con = sqlite3.connect(chemin)
    try:
        con.executescript("""
CREATE TABLE lecons (
  id INTEGER PRIMARY KEY,
  date TEXT, agent TEXT, domaine TEXT, tags TEXT,
  titre TEXT, lecon TEXT, mission TEXT, outils TEXT, verdict TEXT
);
""")
        lecons = [
            ("2026-08-01", "buffy", "migration", "v2", "Lecon A",
             "Contenu A", "M1", "outil1", "OK"),
            ("2026-08-02", "vulcain", "outil", "v1", "Lecon B",
             "Contenu B", "M2", "outil2", "VALIDE"),
            ("2026-08-03", "morpheus", "test", "", "Lecon C",
             "Contenu C", "M3", "", "A REVOIR"),
            ("2026-08-04", "hygie", "nettoyage", "", "",
             "Contenu D sans titre", "M4", "", ""),
            ("2026-08-05", "janus", "controle", "v1", "Lecon E",
             "Contenu E", "", "", ""),
        ]
        con.executemany(
            "INSERT INTO lecons (date,agent,domaine,tags,titre,lecon,"
            "mission,outils,verdict) VALUES (?,?,?,?,?,?,?,?,?)", lecons)
        con.commit()
        return con.execute("SELECT COUNT(*) FROM lecons").fetchone()[0]
    finally:
        con.close()


def preparer_outil_copie(tmp):
    """Copie bdd-lecons + os_path + harnais dans tmp (arborescence relative
    conservee), BDD v2 vierge."""
    cible = os.path.join(tmp, "tools-commun")
    os.makedirs(cible, exist_ok=True)
    for sous in ("bdd-lecons", "os_path", "harnais"):
        src = os.path.join(TOOLS_COMMUN, sous)
        shutil.copytree(src, os.path.join(cible, sous))
    for racine, dossiers, fichiers in os.walk(cible):
        if "__pycache__" in racine:
            shutil.rmtree(racine)
            continue
    bdd = os.path.join(cible, "bdd-lecons")
    for f in ("lecons.db", "lecons.db.bak-2026-09-04", "bdd-lecons.db",
              "bdd-lecons.md.bak"):
        p = os.path.join(bdd, f)
        if os.path.exists(p):
            os.remove(p)
    return os.path.join(bdd, "entry.py")


def run(commande):
    res = subprocess.run(commande, capture_output=True, text=True, timeout=120)
    return (res.stdout or "") + (res.stderr or "")


def main():
    global NB_POINTS, NB_OK, NB_KO, POINT_ACTIF, DESACTIVES
    t0 = time.time()

    args = [a for a in sys.argv[1:]]
    for i, a in enumerate(args):
        if a == "--isoler" and i + 1 < len(args):
            POINT_ACTIF = int(args[i + 1])
        if a == "--desactiver" and i + 1 < len(args):
            DESACTIVES = set(int(x) for x in args[i + 1].split(","))

    print("=== Test migration lecons v1 -> v2 (fixture + idempotence) ===")

    tmp = tempfile.mkdtemp(prefix="tmp-test125-")
    try:
        fixture = os.path.join(tmp, "fixture-v1.db")
        nb_source = creer_fixture_v1(fixture)

        # 1. fixture creee
        t1 = time.time()
        verifier("1. fixture lecons.db v1 creee (5 lecons, cas limites inclus)",
                 nb_source == 5, "nb=%d" % nb_source)
        chrono_etape("1. fixture v1", time.time() - t1)

        entry = preparer_outil_copie(tmp)

        # 2. migration 5/5
        t2 = time.time()
        out1 = run([PYTHON, entry, "migrer-v1", "--chemin", fixture])
        ok1 = ("5 lecons importees" in out1 and "source=5, cible=5" in out1)
        verifier("2. migrer-v1 : 5/5 importees (aucune perte)",
                 ok1, out1[-160:])
        chrono_etape("2. migration", time.time() - t2)

        # 3. rejeu idempotent
        t3 = time.time()
        out2 = run([PYTHON, entry, "migrer-v1", "--chemin", fixture])
        ok2 = "0 lecons importees" in out2
        verifier("3. rejeu : 0 lecon supplementaire (idempotent PAC-8)",
                 ok2, out2[-160:])
        chrono_etape("3. rejeu", time.time() - t3)

        # 4. comptage cible + doublons
        t4 = time.time()
        bdd_v2 = os.path.join(os.path.dirname(entry), "lecons.db")
        con = sqlite3.connect(bdd_v2)
        try:
            nb_cible = con.execute("SELECT COUNT(*) FROM lecons").fetchone()[0]
            nb_doublons = con.execute(
                "SELECT COUNT(*) FROM (SELECT agent, titre, date, COUNT(*) c "
                "FROM lecons GROUP BY agent, titre, date HAVING c > 1)"
            ).fetchone()[0]
        finally:
            con.close()
        verifier("4. comptage cible : 5 lecons en v2, 0 doublon",
                 nb_cible == 5 and nb_doublons == 0,
                 "cible=%d doublons=%d" % (nb_cible, nb_doublons))
        chrono_etape("4. comptage", time.time() - t4)

        # 5. mapping : verdict/mission/outils fusionnes dans resume
        t5 = time.time()
        con = sqlite3.connect(bdd_v2)
        try:
            con.row_factory = sqlite3.Row
            r = con.execute(
                "SELECT * FROM lecons WHERE agent='vulcain' AND "
                "titre='Lecon B'").fetchone()
            ok5 = r is not None and "[verdict: VALIDE]" in (r["resume"] or "") \
                and "[mission: M2]" in (r["resume"] or "") \
                and "[outils: outil2]" in (r["resume"] or "")
            detail5 = "" if ok5 else ("resume=%r" % (r["resume"] if r else None))
        finally:
            con.close()
        verifier("5. mapping : verdict+mission+outils conserves dans resume (PAC-7)",
                 ok5, detail5)
        chrono_etape("5. mapping", time.time() - t5)

        # 6. titre vide derive (titre_auto) - pas de perte
        t6 = time.time()
        con = sqlite3.connect(bdd_v2)
        try:
            con.row_factory = sqlite3.Row
            r = con.execute(
                "SELECT * FROM lecons WHERE agent='hygie'").fetchone()
            ok6 = r is not None and r["titre"] \
                and ("Contenu D" in (r["resume"] or ""))
        finally:
            con.close()
        verifier("6. titre vide derive de la lecon (titre_auto), contenu conserve",
                 ok6)
        chrono_etape("6. titre auto", time.time() - t6)

        # 7. source = v1-lecons.db
        t7 = time.time()
        con = sqlite3.connect(bdd_v2)
        try:
            nb_src = con.execute(
                "SELECT COUNT(*) FROM lecons WHERE source='v1-lecons.db'"
            ).fetchone()[0]
        finally:
            con.close()
        verifier("7. source 'v1-lecons.db' sur les 5 lecons migrees",
                 nb_src == 5, "nb=%d" % nb_src)
        chrono_etape("7. source", time.time() - t7)

        # 8. normes ASCII/LF (test + outils copies .py/.md - la fixture .db
        # est BINAIRE SQLite, hors perimetre ASCII)
        t8 = time.time()
        fichiers_normes = [os.path.abspath(__file__), entry]
        for racine, dossiers, fichiers in os.walk(
                os.path.join(tmp, "tools-commun", "bdd-lecons")):
            for f in fichiers:
                if f.endswith((".py", ".md")):
                    fichiers_normes.append(os.path.join(racine, f))
        total_na = sum(compter_non_ascii(f) for f in fichiers_normes
                       if os.path.exists(f))
        verifier("8. ASCII strict: 0 non-ASCII (test + fixture + outils)",
                 total_na == 0, "nb=%d" % total_na)
        chrono_etape("8. ASCII", time.time() - t8)

        t9 = time.time()
        total_crlf = sum(compter_crlf(f) for f in fichiers_normes
                         if os.path.exists(f))
        verifier("9. LF pur: 0 CRLF (test + fixture + outils)",
                 total_crlf == 0, "nb=%d" % total_crlf)
        chrono_etape("9. LF pur", time.time() - t9)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if "--no-chrono" not in args:
        print("")
        print("=== BILAN CHRONO ===")
        print("test-125-migration-lecons-v1-v2 : total %.2fs"
              % (time.time() - t0))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())