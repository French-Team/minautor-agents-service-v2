#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-124-gel-corrections-v1-garde-fou.py
GARDE-FOU ANTI-REGRESSION DU GEL (migration v1->v2, mission 85b4545d D.2) :
les corrections.md v1 (22 agents) sont GELES depuis le 2026-09-04 (bandeau
"MEMOIRE GELEE le 2026-09-04" pose par Buffy, mission bd89c8d9 B.1).
AUCUN [LECON] supplementaire ne doit etre ajoute : les nouvelles lecons vont
dans bdd-lecons v2 (outil v2, E2).

Points verifies :
  1. Les 22 corrections.md v1 portent le bandeau de gel
     ("MEMOIRE GELEE le 2026-09-04")
  2. Aucune lecon [LECON] datee APRES le 2026-09-04 (ecriture post-gel)
  3. Le bandeau est place AVANT les lecons (en tete, apres frontmatter)
  4. Normes : ASCII strict + LF pur (test + corrections.md geles)
  5. PREUVE NEGATIVE : un fichier temporaire avec [LECON] post-gel est
     detecte (verifie que la detection fonctionne)

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: gel, migration, corrections.md, garde-fou, anti-regression
"""
import io
import os
import re
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")

GEL_BANDEAU = "MEMOIRE GELEE le 2026-09-04"
GEL_DATE = "2026-09-04"

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


def corrections_v1():
    """Liste des corrections.md v1 (agents ayant un dossier parcours v1)."""
    resultat = []
    for nom in sorted(os.listdir(AGENTS_DIR)):
        chemin = os.path.join(AGENTS_DIR, nom, "corrections.md")
        if os.path.isfile(chemin):
            resultat.append(chemin)
    return resultat


def detecter_post_gel(texte):
    """Retourne la liste des dates [LECON] posterieures au gel (2026-09-04)."""
    dates = re.findall(r"##\s*\[LECON\]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", texte)
    return [d for d in dates if d > GEL_DATE]


def main():
    global NB_POINTS, NB_OK, NB_KO, POINT_ACTIF, DESACTIVES
    t0 = time.time()

    args = [a for a in sys.argv[1:]]
    for i, a in enumerate(args):
        if a == "--isoler" and i + 1 < len(args):
            POINT_ACTIF = int(args[i + 1])
        if a == "--desactiver" and i + 1 < len(args):
            DESACTIVES = set(int(x) for x in args[i + 1].split(","))

    print("=== Test formel gel-corrections-v1 (anti-regression du gel 2026-09-04) ===")

    fichiers = corrections_v1()

    # 1. Bandeau de gel present sur tous les corrections.md v1
    t1 = time.time()
    sans_bandeau = []
    for f in fichiers:
        texte = lire(f)
        if GEL_BANDEAU not in texte:
            sans_bandeau.append(os.path.relpath(f, PROJECT_ROOT))
    verifier("1. bandeau gel present dans les %d corrections.md v1" % len(fichiers),
             not sans_bandeau, "sans bandeau=%s" % sans_bandeau[:3])
    chrono_etape("1. bandeaux", time.time() - t1)

    # 2. Aucune lecon [LECON] datee apres le gel (ecriture post-gel)
    t2 = time.time()
    post_gel = []
    for f in fichiers:
        texte = lire(f)
        for d in detecter_post_gel(texte):
            post_gel.append("%s %s" % (os.path.relpath(f, PROJECT_ROOT), d))
    verifier("2. aucun [LECON] date apres 2026-09-04 (ecriture post-gel interdite)",
             not post_gel, "post-gel=%s" % post_gel[:3])
    chrono_etape("2. lecons post-gel", time.time() - t2)

    # 3. Bandeau place AVANT les lecons (en tete, apres frontmatter)
    t3 = time.time()
    bandeau_tardif = []
    for f in fichiers:
        texte = lire(f)
        idx_bandeau = texte.find(GEL_BANDEAU)
        idx_lecon = texte.find("[LECON]")
        if idx_bandeau == -1:
            continue
        if idx_lecon != -1 and idx_lecon < idx_bandeau:
            bandeau_tardif.append(os.path.relpath(f, PROJECT_ROOT))
    verifier("3. bandeau place AVANT les lecons [LECON]",
             not bandeau_tardif, "bandeau tardif=%s" % bandeau_tardif[:3])
    chrono_etape("3. position bandeau", time.time() - t3)

    # 4. PREUVE NEGATIVE : un [LECON] post-gel est detecte
    t4 = time.time()
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False,
                                      encoding="ascii")
    try:
        tmp.write("> %s\n\n## [LECON] 2026-09-05 -- ecriture interdite\n")
        tmp.close()
        detecte = detecter_post_gel(lire(tmp.name))
        verifier("4. preuve negative : [LECON] 2026-09-05 detecte comme post-gel",
                 detecte == ["2026-09-05"], "detecte=%s" % detecte)
    finally:
        os.unlink(tmp.name)
    chrono_etape("4. preuve negative", time.time() - t4)

    # 5. Normes : ASCII strict sur le test + le bandeau de gel ; LF pur sur
    # test + corrections.md. NB : le CONTENU des corrections.md v1 est un
    # historique GELE (conserve tel quel) - un accent pre-existant (ex:
    # buffy) n est pas une regression. Seul le bandeau doit rester ASCII.
    t5 = time.time()
    total_na = compter_non_ascii(os.path.abspath(__file__))
    for f in fichiers:
        texte = lire(f)
        idx = texte.find(GEL_BANDEAU)
        if idx != -1:
            # 60 premiers caracteres du bandeau
            total_na += sum(1 for ch in texte[idx:idx + 60] if ord(ch) > 127)
    verifier("5. ASCII strict: test + bandeau de gel (0 non-ASCII)",
             total_na == 0, "nb=%d" % total_na)
    chrono_etape("5. ASCII", time.time() - t5)

    t6 = time.time()
    total_crlf = compter_crlf(os.path.abspath(__file__))
    for f in fichiers:
        total_crlf += compter_crlf(f)
    verifier("6. LF pur: 0 CRLF (test + corrections.md v1)",
             total_crlf == 0, "nb=%d" % total_crlf)
    chrono_etape("6. LF pur", time.time() - t6)

    if "--no-chrono" not in args:
        print("")
        print("=== BILAN CHRONO ===")
        print("test-124-gel-corrections-v1 : total %.2fs" % (time.time() - t0))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())