#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-046-hermes-fautes.py
GARDE-FOU : l agent Hermes (langue/orthographe) reste conforme et son chariot
detecter-fautes-orthographe reste present et efficace.

Contexte (mission utilisateur 2026-08-14) :
  - Creation de Hermes, agent de la langue (dieu grec de l eloquence) : fiche,
    corrections, parcours v0.1.0, outil detecter-fautes-orthographe v0.1.0.
  - Suite a la faute `enchannements` trouvee dans readme-dev:264 : personne ne
    verifiait l orthographe des fichiers rediges par les agents.
  - Anti-recurrence : toute faute reelle du dictionnaire dans les fichiers
    rediges (hors historique) fait KO ; toute regression de la carte ou de
    l outil fait KO.

Cas couverts:
  1. La fiche hermes.md est CONFORME (verifier-conformite-fiche)
  2. Le parcours hermes est valide (valider-case : 0 erreur)
  3. Le parcours hermes est CONFORME (valider-cartes-decision)
  4. Les 14 parcours existent (glob cerveau-projet/agents/*/parcours/)
  5. L outil detecter-fautes-orthographe est au catalogue generateurs-commande
  6. L outil detecter-fautes-orthographe est dans index-tools.md
  7. Le dictionnaire de l outil ne contient que de VRAIES fautes (fautif != correct)
  8. Aucune faute reelle restante : detecter-fautes-orthographe --tous ne
     signale AUCUNE faute hors historique (AGENTS-historique/AGENTS.md/
     corrections.md documentent les citations de la faute d origine)
  9. ASCII strict : 0 non-ASCII (test + fiche + parcours + outil)
  10. LF pur : 0 CRLF (test + fiche + parcours + outil)
"""
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
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

AGENT_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "hermes")
FICHE = os.path.join(AGENT_DIR, "hermes.md")
PARCOURS = os.path.join(AGENT_DIR, "parcours", "parcours-hermes.json")
OUTIL = os.path.join(TOOLS_DIR, "detecter", "detecter-fautes-orthographe",
                     "detecter-fautes-orthographe.py")
OUTIL_MD = os.path.join(TOOLS_DIR, "detecter", "detecter-fautes-orthographe",
                        "detecter-fautes-orthographe.md")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX_TOOLS = os.path.join(TOOLS_DIR, "index-tools.md")

# Fichiers "historique" qui citent LEGITIMEMENT la faute d origine (lecons,
# missions) : ils ne sont pas des fautes a corriger.
HISTORIQUES = ("AGENTS-historique.md", "corrections.md")

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

    print("=== Test formel hermes-fautes (garde-fou) ===")

    # 1. Fiche conforme
    t1 = time.time()
    r = run([sys.executable,
             os.path.join(TOOLS_DIR, "verifier", "verifier-conformite-fiche",
                          "verifier-conformite-fiche.py"),
             "--agent", "hermes"])
    verifier("1. fiche hermes CONFORME (verifier-conformite-fiche)",
             r is not None and "CONFORME" in r,
             (r or "")[-120:])
    chrono_etape("1. fiche conforme", time.time() - t1)

    # 2. Parcours valide (valider-case)
    t2 = time.time()
    r = run([sys.executable,
             os.path.join(TOOLS_DIR, "valider", "valider-case",
                          "valider-case.py"), PARCOURS])
    verifier("2. parcours hermes valide (valider-case 0 erreur)",
             r is not None and "CONFORME" in r and "erreurs: 0" in r,
             (r or "")[-120:])
    chrono_etape("2. parcours valide", time.time() - t2)

    # 3. Parcours conforme (valider-cartes-decision)
    t3 = time.time()
    r = run([sys.executable,
             os.path.join(TOOLS_DIR, "valider", "valider-cartes-decision",
                          "valider-cartes-decision.py"),
             "--agent", "hermes"])
    verifier("3. parcours hermes CONFORME (valider-cartes-decision)",
             r is not None and "CONFORME" in r,
             (r or "")[-120:])
    chrono_etape("3. parcours conforme", time.time() - t3)

    # 4. Les 14 parcours existent (glob)
    t4 = time.time()
    import glob as _glob
    parcours = sorted(_glob.glob(os.path.join(PROJECT_ROOT,
                                              "cerveau-projet", "agents", "*",
                                              "parcours", "parcours-*.json")))
    verifier("4. 14 parcours existent (glob agents/*/parcours/)",
             len(parcours) == 14, "nb=%d" % len(parcours))
    chrono_etape("4. 14 parcours", time.time() - t4)

    # 5. Outil au catalogue
    t5 = time.time()
    with io.open(CATALOGUE, encoding="utf-8") as fh:
        cat = json.load(fh)
    noms = [e["nom"] for e in cat["commandes"]]
    verifier("5. detecter-fautes-orthographe au catalogue",
             "detecter-fautes-orthographe" in noms)
    chrono_etape("5. catalogue", time.time() - t5)

    # 6. Outil dans index-tools
    t6 = time.time()
    with io.open(INDEX_TOOLS, encoding="utf-8") as fh:
        idx = fh.read()
    verifier("6. detecter-fautes-orthographe dans index-tools",
             "detecter-fautes-orthographe" in idx)
    chrono_etape("6. index-tools", time.time() - t6)

    # 7. Dictionnaire : fautif != correct (pas de faux positif)
    t7 = time.time()
    with io.open(OUTIL, encoding="utf-8") as fh:
        src = fh.read()
    # extraire le bloc FAUTES = { "fautif": "correct", ... }
    m = re.search(r"FAUTES\s*=\s*\{(.*?)\n\}", src, re.S)
    faux_positifs = []
    if m:
        for entree in re.finditer(r'"([^"]+)"\s*:\s*"([^"]+)"', m.group(1)):
            if entree.group(1) == entree.group(2):
                faux_positifs.append(entree.group(1))
    verifier("7. dictionnaire sans faux positif (fautif != correct)",
             not faux_positifs, "faux positifs=%s" % faux_positifs)
    chrono_etape("7. dictionnaire", time.time() - t7)

    # 8. Aucune faute reelle restante : --tous ne signale que l historique
    t8 = time.time()
    r = run([sys.executable, OUTIL, "--tous"])
    sortie = r or ""
    # extraire la liste des fichiers signales (lignes "  <chemin> : N faute(s)")
    lignes = [l for l in sortie.splitlines() if " faute(s)" in l]
    fautes_hors_historique = []
    for l in lignes:
        chemin = l.split(":")[0].strip()
        if any(h in chemin for h in HISTORIQUES):
            continue
        fautes_hors_historique.append(l)
    verifier("8. 0 faute reelle hors historique (detecter --tous)",
             not fautes_hors_historique,
             "restantes=%s" % fautes_hors_historique[:3])
    chrono_etape("8. scan fautes", time.time() - t8)

    # 9. ASCII strict
    t9 = time.time()
    total_na = sum(compter_non_ascii(f) for f in
                   [FICHE, PARCOURS, OUTIL, OUTIL_MD,
                    os.path.abspath(__file__)])
    verifier("9. ASCII strict: 0 non-ASCII (test + fiche + parcours + outil)",
             total_na == 0, "nb=%d" % total_na)
    chrono_etape("9. ASCII", time.time() - t9)

    # 10. LF pur
    t10 = time.time()
    total_crlf = sum(compter_crlf(f) for f in
                     [FICHE, PARCOURS, OUTIL, OUTIL_MD,
                      os.path.abspath(__file__)])
    verifier("10. LF pur: 0 CRLF (test + fiche + parcours + outil)",
             total_crlf == 0, "nb=%d" % total_crlf)
    chrono_etape("10. LF pur", time.time() - t10)

    # --- Bilan chrono global ---
    if "--no-chrono" not in args:
        print("")
        print("=== BILAN CHRONO ===")
        print("test-046-hermes-fautes : total %.2fs" % (time.time() - t0))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1




def bilan_chrono():
    # Bilan des durees : total depuis le depart (regle immuable v0.3.0)
    try:
        _total = __import__("time").monotonic() - T_START
    except Exception:
        _total = 0.0
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)

if __name__ == "__main__":
    sys.exit(main())
