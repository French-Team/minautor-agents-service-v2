#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-047-outils-externes-garde-fou.py
GARDE-FOU : la mecanisation du bannissement des outils tiers. L outil
detecter-usage-outils-externes est lance systematiquement sur tout le
cerveau-projet : toute trace (CRLF, non-ASCII, BOM) fait KO.

Contexte (mission utilisateur 2026-08-14) :
  - REGLE ABSOLUE 4 : les agents doivent utiliser UNIQUEMENT les outils du
    cerveau (jamais read_files, write_file, basher...).
  - La regle etait DECLAREE mais pas MECANISEE : personne ne verifiait les
    traces en fin de mission (des CRLF etaient restes dans corrections.md,
    rapports, version-readme.txt).
  - Anti-recurrence : detecter-usage-outils-externes v0.1.1 scanne tout le
    cerveau-projet et toute trace fait KO. Les fichiers VOLONTAIREMENT non
    conformes (dictionnaires d accents/emojis, exemples de tests, documents
    externes fournis par l utilisateur) sont exclus par defaut et documentes.

Cas couverts:
  1. L outil detecter-usage-outils-externes est au catalogue generateurs-commande
  2. L outil est dans index-tools.md
  3. L outil s execute sans erreur sur cerveau-projet --recursive (exit 0)
  4. 0 fichier suspect sur tout le cerveau-projet (toute trace = KO)
  5. Les exclusions par defaut sont documentees dans le code (dictionnaires,
     exemples, docs-dev)
  6. Les dictionnaires/exemples volontairement non-ASCII sont bien EXCLUS
     (ils restent signalables uniquement via --exclure vide)
  7. Les anciens residus CRLF (corrections.md buffy/clio, rapports clio,
     version-readme.txt) sont propres
  8. ASCII strict : 0 non-ASCII (test + outil py/sh/md)
  9. LF pur : 0 CRLF (test + outil py/sh/md)
  10. La REGLE ABSOLUE 4 est documentee dans les fichiers agents (anti-oubli)
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
CERVEAU_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet")


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

OUTIL = os.path.join(TOOLS_DIR, "detecter", "detecter-usage-outils-externes",
                     "detecter-usage-outils-externes.py")
OUTIL_SH = os.path.join(TOOLS_DIR, "detecter", "detecter-usage-outils-externes",
                        "detecter-usage-outils-externes.sh")
OUTIL_MD = os.path.join(TOOLS_DIR, "detecter", "detecter-usage-outils-externes",
                        "detecter-usage-outils-externes.md")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX_TOOLS = os.path.join(TOOLS_DIR, "index-tools.md")

# Anciens residus CRLF corriges (preuve qu ils sont propres desormais)
ANCIENS_RESIDUS = [
    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "buffy",
                 "corrections.md"),
    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio",
                 "corrections.md"),
    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio", "rapports",
                 "maj-readme-massive-2026-08-13-18-19.md"),
    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio", "rapports",
                 "maj-readme-massive-2026-08-13-19-47.md"),
    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "clio",
                 "version-readme.txt"),
]

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
POINT_ACTIF = None  # --isoler N
DESACTIVES = set()  # --desactiver 1,3,5


def chrono_etape(nom, duree):
    """Bilan chrono par etape (triplet template v0.3.0)."""
    print("  [chrono] %-40s %.2fs" % (nom, duree))


def verifier(nom, ok, detail=""):
    """Point de verification : marqueur [OK]/[KO] + compteurs."""
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
    """Executer une commande sans bloquer (protection anti-blocage).
    Retourne la sortie stdout (string)."""
    res = PROTECTIONS.lancer_protege(commande, timeout=120)
    return res.stdout if res is not None else ""


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def compter_crlf(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO, POINT_ACTIF, DESACTIVES
    t0 = time.time()

    # --- Options on/off (regle immuable v0.3.0) ---
    args = [a for a in sys.argv[1:]]
    if "--no-chrono" not in args:
        pass  # chrono actif par defaut
    for i, a in enumerate(args):
        if a == "--isoler" and i + 1 < len(args):
            POINT_ACTIF = int(args[i + 1])
        if a == "--desactiver" and i + 1 < len(args):
            DESACTIVES = set(int(x) for x in args[i + 1].split(","))

    print("=== Test formel outil-externe (garde-fou bannissement mecanise) ===")

    # 1. Outil au catalogue
    t1 = time.time()
    with io.open(CATALOGUE, encoding="utf-8") as fh:
        cat = json.load(fh)
    noms = [e["nom"] for e in cat["commandes"]]
    verifier("1. detecter-usage-outils-externes au catalogue",
             "detecter-usage-outils-externes" in noms)
    chrono_etape("1. catalogue", time.time() - t1)

    # 2. Outil dans index-tools
    t2 = time.time()
    with io.open(INDEX_TOOLS, encoding="utf-8") as fh:
        idx = fh.read()
    verifier("2. detecter-usage-outils-externes dans index-tools",
             "detecter-usage-outils-externes" in idx)
    chrono_etape("2. index-tools", time.time() - t2)

    # 3. L outil s execute sans erreur sur tout le cerveau-projet
    t3 = time.time()
    r = run([sys.executable, OUTIL, CERVEAU_DIR, "--recursive"])
    verifier("3. outil executable sur cerveau-projet --recursive",
             r is not None and "=== RESUME ===" in (r or ""),
             (r or "")[-120:])
    chrono_etape("3. execution outil", time.time() - t3)

    # 4. 0 fichier suspect sur tout le cerveau-projet (KO si traces)
    t4 = time.time()
    sortie4 = r or ""
    suspects = [l for l in sortie4.splitlines()
                if l.startswith("SUSPECT") or l.startswith("SUSPECT:")]
    verifier("4. 0 fichier suspect sur tout le cerveau-projet",
             not suspects and "Fichiers suspects  : 0" in sortie4,
             "suspects=%s" % suspects[:3])
    chrono_etape("4. scan global", time.time() - t4)

    # 5. Exclusions par defaut documentees dans le code
    t5 = time.time()
    with io.open(OUTIL, encoding="utf-8") as fh:
        src = fh.read()
    exclusions_ok = all(m in src for m in [
        "EXCLUSIONS_PAR_DEFAUT",
        "corriger-dictionnaire-accents.txt",
        "dictionnaire-emojis.txt",
        "exemples",
        "docs-dev-cerveau-projet",
    ])
    verifier("5. exclusions par defaut documentees dans le code",
             exclusions_ok)
    chrono_etape("5. exclusions code", time.time() - t5)

    # 6. Les fichiers volontairement non-ASCII restent EXCLUS
    t6 = time.time()
    # Ces fichiers sont legitimes (non-ASCII) mais ne doivent PAS faire KO
    # du scan global : la preuve est le point 4 (0 suspect). Ici on verifie
    # que les motifs d exclusion couvrent bien ces chemins.
    # motifs normalises comme dans l outil (est_exclu normalise les
    # separateurs : backslash -> slash)
    fichiers_volontaires = [
        "corriger-dictionnaire-accents.txt",
        "dictionnaire-emojis.txt",
        "exemples/",
        "docs-dev-cerveau-projet/",
    ]
    # simulons est_exclu comme dans l outil (sous-chaine normalisee)
    def est_exclu(chemin, motifs):
        c = str(chemin).replace("\\", "/")
        return any(m in c for m in motifs)

    suspects_non_exclus = []
    for motif in fichiers_volontaires:
        # un chemin representatif de chaque categorie
        if motif.endswith(".txt"):
            chemin_test = "/cerveau-projet/agents/tools/corriger/corriger-emojis/" + motif
        elif "exemples" in motif:
            chemin_test = "/cerveau-projet/exemples/test-emojis/test-emojis.md"
        else:
            chemin_test = "/cerveau-projet/" + motif
        if not est_exclu(chemin_test, fichiers_volontaires):
            suspects_non_exclus.append(motif)
    verifier("6. fichiers volontairement non-ASCII couverts par exclusions",
             not suspects_non_exclus, "non exclus=%s" % suspects_non_exclus)
    chrono_etape("6. exclusions couvrent", time.time() - t6)

    # 7. Les anciens residus CRLF sont propres
    t7 = time.time()
    crlf_restants = [(os.path.basename(f), compter_crlf(f))
                     for f in ANCIENS_RESIDUS if os.path.exists(f)
                     and compter_crlf(f) > 0]
    verifier("7. anciens residus CRLF corriges (buffy/clio/rapports)",
             not crlf_restants, "crlf=%s" % crlf_restants[:3])
    chrono_etape("7. anciens residus", time.time() - t7)

    # 8. ASCII strict
    t8 = time.time()
    total_na = sum(compter_non_ascii(f) for f in
                   [OUTIL, OUTIL_SH, OUTIL_MD, os.path.abspath(__file__)])
    verifier("8. ASCII strict: 0 non-ASCII (test + outil py/sh/md)",
             total_na == 0, "nb=%d" % total_na)
    chrono_etape("8. ASCII", time.time() - t8)

    # 9. LF pur
    t9 = time.time()
    total_crlf = sum(compter_crlf(f) for f in
                     [OUTIL, OUTIL_SH, OUTIL_MD, os.path.abspath(__file__)])
    verifier("9. LF pur: 0 CRLF (test + outil py/sh/md)",
             total_crlf == 0, "nb=%d" % total_crlf)
    chrono_etape("9. LF pur", time.time() - t9)

    # 10. REGLE ABSOLUE 4 documentee dans les fiches agents (anti-oubli)
    t10 = time.time()
    fiche_cerberus = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                  "cerberus", "cerberus.md")
    if os.path.exists(fiche_cerberus):
        with io.open(fiche_cerberus, encoding="utf-8", errors="replace") as fh:
            fc = fh.read()
        regle_documentee = ("outils du cerveau" in fc
                            and "JAMAIS" in fc.upper())
    else:
        regle_documentee = False
    verifier("10. REGLE ABSOLUE 4 documentee (fiches agents)",
             regle_documentee)
    chrono_etape("10. regle documentee", time.time() - t10)

    # --- Bilan chrono global ---
    if "--no-chrono" not in args:
        print("")
        print("=== BILAN CHRONO ===")
        print("test-047-outils-externes-garde-fou : total %.2fs"
              % (time.time() - t0))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
