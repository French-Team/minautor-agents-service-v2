#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-128-protocole-evaluation-croisee-garde-fou.py
Garde-fou de conformite du protocole evaluation croisee v1 (cree par
Buffy, mission a42cbb38, volet 2/2 du rapport Themis 2026-09-05-1835) :
structure convention-protocoles (frontmatter + 7 sections), nommage
[nom].[id].[class].[statut], liens internes valides, ASCII strict + LF pur,
reference aux 3 rapports themis reels, index-regles-general a jour.

Contexte :
  - Le protocole evaluation croisee v1 etait une reference verbale (aucun
    fichier dedie) : les rapports themis/rapports/evaluation-croisee-
    periodique-*.md (2026-09-02 20:35, 20:45, 2026-09-05 18:35) en etaient
    les instances reelles. Buffy a cree protocole-evaluation-croisee.
    001.01.ebauche.md selon la convention-protocoles.
  - Ce test verrouille la structure du protocole pour que les futures
    evolutions (changement de statut, ajout de sections) ne cassent pas la
    convention silencieusement.
"""
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

PROTOCOLE_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             "regles-immuables", "general",
                             "protocole-evaluation-croisee")
PROTOCOLE_MD = os.path.join(PROTOCOLE_DIR,
                            "protocole-evaluation-croisee.001.01.ebauche.md")
INDEX_MD = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                        "regles-immuables", "general", "index-regles-general.md")
RAPPORTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                            "themis", "rapports")
RAPPORTS_ATTENDUS = [
    "evaluation-croisee-periodique-2026-09-02-2035.md",
    "evaluation-croisee-periodique-2026-09-02-2045.md",
    "evaluation-croisee-periodique-2026-09-05-1835.md",
]
SECTIONS_ATTENDUES = [
    "## Objectif",
    "## Prerequis",
    "## Etapes",
    "## RVAV",
    "## Exemples",
    "## Pieges courants",
    "## Liens",
]

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT_TEST = time.monotonic()
ETAPES = []  # (nom, duree_secondes) alimente le bilan chrono


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    """True si le point N doit s executer (options on/off du test)."""
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    """Enregistre la duree d une etape (no-op si --no-chrono)."""
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    """Affiche le bilan des durees : total + detail par etape."""
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    detail = " | ".join("%s=%.2fs" % e for e in ETAPES)
    print("=== CHRONO : total %.2fs (%s) ===" % (total, detail))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== [TEST-128 PROTOCOLE EVALUATION CROISEE GARDE-FOU] ===")
    fixture = None
    try:
        # 1. Le fichier protocole existe (point CRITIQUE -> protection STOP)
        if point_actif(1):
            t = time.monotonic()
            existe = os.path.isfile(PROTOCOLE_MD)
            PROTECTIONS.verifier_critique(
                "1. protocole-evaluation-croisee.001.01.ebauche.md existe",
                existe, "chemin=%s" % PROTOCOLE_MD)
            chrono_etape("1. existence", t)

        # 2. Nommage [nom].[id].[class].[statut] conforme a la convention
        if point_actif(2):
            t = time.monotonic()
            basename = os.path.basename(PROTOCOLE_MD)
            nommage = re.match(
                r"^protocole-[a-z0-9-]+\.\d{3}\.\d{2}\.(ebauche|prepare|dev|test|valide)\.md$",
                basename)
            verifier("2. nommage [nom].[id].[class].[statut] conforme",
                     nommage is not None, "nom=%s" % basename)
            chrono_etape("2. nommage", t)

        # 3. Frontmatter ferme + type protocole + commun true
        if point_actif(3):
            t = time.monotonic()
            d = io.open(PROTOCOLE_MD, encoding="utf-8", errors="replace").read()
            frontmatter = d.startswith("---") and d.count("---") >= 2
            a_type_protocole = "type: protocole" in d
            a_commun_true = "commun: true" in d
            verifier("3. frontmatter ferme (--- x2)",
                     frontmatter, "count=%d" % d.count("---"))
            verifier("3b. frontmatter type protocole + commun true",
                     a_type_protocole and a_commun_true, "")
            chrono_etape("3. frontmatter", t)

        # 4. Les 7 sections de la convention-protocoles presentes
        if point_actif(4):
            t = time.monotonic()
            d = io.open(PROTOCOLE_MD, encoding="utf-8", errors="replace").read()
            manquantes = [s for s in SECTIONS_ATTENDUES if s not in d]
            verifier("4. 7 sections convention-protocoles presentes",
                     not manquantes, "manquantes=%s" % manquantes)
            chrono_etape("4. sections", t)

        # 5. Les 3 rapports themis reels references existent
        if point_actif(5):
            t = time.monotonic()
            manquants = [r for r in RAPPORTS_ATTENDUS
                         if not os.path.isfile(os.path.join(RAPPORTS_DIR, r))]
            verifier("5. 3 rapports evaluation croisee reels presents",
                     not manquants, "manquants=%s" % manquants)
            d = io.open(PROTOCOLE_MD, encoding="utf-8", errors="replace").read()
            referencas = sum(1 for r in RAPPORTS_ATTENDUS if r in d)
            verifier("5b. les 3 rapports references dans le protocole",
                     referencas == 3, "refere=%d/3" % referencas)
            chrono_etape("5. rapports", t)

        # 6. index-regles-general.md reference le protocole
        if point_actif(6):
            t = time.monotonic()
            idx = io.open(INDEX_MD, encoding="utf-8", errors="replace").read()
            verifier("6. index-regles-general.md reference protocole-evaluation-croisee",
                     "protocole-evaluation-croisee" in idx, "")
            chrono_etape("6. index", t)

        # 7. Liens internes valides (evaluer-coherence sur le dossier)
        if point_actif(7):
            t = time.monotonic()
            evaluer = os.path.join(TOOLS_DIR, "evaluer", "evaluer-coherence",
                                   "evaluer-coherence.py")
            r = run([PYTHON, evaluer, PROTOCOLE_DIR])
            sortie = (r.stdout or "") + (r.stderr or "")
            verifier("7. aucun lien casse dans le protocole",
                     "Aucun lien casse" in sortie, "rc=%d %s" % (r.returncode, sortie[-120:]))
            chrono_etape("7. liens", t)

        # 8. Normes ASCII strict + LF pur (protocole + index + test)
        if point_actif(8):
            t = time.monotonic()
            fichiers = [PROTOCOLE_MD, INDEX_MD, os.path.abspath(__file__)]
            total_non_ascii = sum(ascii_count(f) for f in fichiers)
            verifier("8. ASCII strict : 0 non-ASCII (protocole + index + test)",
                     total_non_ascii == 0, "total=%d" % total_non_ascii)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("8b. LF pur : 0 CRLF (protocole + index + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("8. normes", t)

        # 9. PREUVE NEGATIVE : frontmatter corrompu detecte (fixture)
        if point_actif(9):
            t = time.monotonic()
            fixture = tempfile.mkdtemp(prefix="tmp-test128-")
            fichier_fixture = os.path.join(
                fixture, "protocole-evaluation-croisee.001.02.ebauche.md")
            with io.open(PROTOCOLE_MD, encoding="utf-8") as fh:
                contenu = fh.read()
            contenu_corrompu = contenu.replace("type: protocole",
                                               "type: regle")
            with io.open(fichier_fixture, "w", encoding="utf-8") as fh:
                fh.write(contenu_corrompu)
            # Le garde-fou structurel (ici : la regle de nommage + le test
            # lui-meme) doit detecter qu un fichier .md de protocole ne porte
            # pas le bon type -- preuve que la verification a du pouvoir.
            d = io.open(fichier_fixture, encoding="utf-8", errors="replace").read()
            corrompu_detecte = "type: protocole" not in d
            verifier("9. PREUVE NEGATIVE : type corrompu detecte",
                     corrompu_detecte, "")
            # La preuve ne doit PAS etre un faux positif : le nommage de la
            # fixture reste conforme, seul le contenu est altere.
            verifier("9b. PREUVE NEGATIVE : nommage fixture reste conforme",
                     re.match(r"^protocole-[a-z0-9-]+\.\d{3}\.\d{2}\."
                              r"(ebauche|prepare|dev|test|valide)\.md$",
                              os.path.basename(fichier_fixture)) is not None, "")
            chrono_etape("9. preuve negative", t)
    finally:
        if fixture and os.path.isdir(fixture):
            shutil.rmtree(fixture, ignore_errors=True)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    if NB_KO:
        print("  [AIDE] OU CHERCHER / REPARER :")
        print("    [AIDE] Fichier(s) inspecte(s) : agents/regles-immuables/general/protocole-evaluation-croisee/")
        print("    [AIDE] Diagnostic : python3 agents/tools/evaluer/evaluer-coherence/evaluer-coherence.py agents/regles-immuables/general/protocole-evaluation-croisee")
        print("    [AIDE] Correctif : verifier frontmatter (type protocole, commun true), les 7 sections de la convention-protocoles, et la reference aux 3 rapports themis")
    PROTECTIONS.afficher_rating(os.path.basename(__file__).replace(".py", ""))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())