#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-046-compartimentation-residus.py
GARDE-FOU : la compartimentation de detecter-residus reste etanche et sans
double comptage.

Contexte (mission utilisateur 2026-08-13) :
  - detecter-residus v0.1.2 a ete corrige apres un test reel de
    compartimentation : (a) classification RAPPORT_EGARE par DOSSIER PARENT
    immediat (les 171 rapports legitimes des agents etaient classes a tort),
    (b) deduplication des fichiers de la racine (double comptage elimine).
  - Anti-recurrence : toute regression de la compartimentation (chevauchement
    de zones, double comptage, rapports legitimes reclasses a tort) fait KO.

Cas couverts:
  1. Zone `workspace` ne voit QUE ses residus (et JAMAIS ceux de
     cerveau-projet/) - compartimentation etanche
  2. Zone `cerveau-projet` ne voit QUE ses residus (et JAMAIS ceux de
     workspace/) - compartimentation etanche
  3. Un fichier de la racine est compte UNE SEULE fois (deduplication)
  4. Un rapport dans un dossier parent `controles` est LEGITIME (pas de
     RAPPORT_EGARE) - correctif v0.1.2
  5. `--tous` voit les deux zones sans chevauchement
  6. Nettoyage garanti : 0 residu factice restant meme en cas d echec
  7. ASCII strict : 0 non-ASCII (test)
  8. LF pur : 0 CRLF (test)
"""
import importlib.util
import io
import os
import sys

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

DETECTEUR = os.path.join(TOOLS_DIR, "detecter", "detecter-residus",
                         "detecter-residus.py")

# --- Residus factices poses par le test (nettoyage try/finally garanti) ---
RESIDUS_WORKSPACE = [
    "workspace/.tmp-factice-046.py",       # TEMP
    "workspace/0.1.9",                     # VERSION (semver)
    "workspace/rapport-egare-factice.md",  # RAPPORT_EGARE (racine workspace)
    "workspace/sous-dossier/note.bak",     # SAUVEGARDE (recursif)
]
RESIDUS_CERVEAU = [
    "cerveau-projet/agents/tools/.tmp-factice-interne-046.py",  # TEMP interne
]
RAPPORT_RACINE = "rapport-factice-046.md"   # a la RACINE (deduplication)
RAPPORT_LEGITIME = "workspace/controles/rapport-factice-legitime-046.md"

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


def creer_residus():
    """Pose les residus factices (contenu ASCII, LF)."""
    for rel in RESIDUS_WORKSPACE + RESIDUS_CERVEAU + [RAPPORT_RACINE,
                                                      RAPPORT_LEGITIME]:
        chemin = os.path.join(PROJECT_ROOT, rel)
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# factice 046\n")


def nettoyer_residus():
    """Retire les residus factices et les dossiers devenus vides."""
    for rel in RESIDUS_WORKSPACE + RESIDUS_CERVEAU + [RAPPORT_RACINE,
                                                      RAPPORT_LEGITIME]:
        chemin = os.path.join(PROJECT_ROOT, rel)
        if os.path.isfile(chemin):
            os.remove(chemin)
    for d in ("workspace/sous-dossier", "workspace/controles"):
        chemin = os.path.join(PROJECT_ROOT, d)
        try:
            os.rmdir(chemin)
        except OSError:
            pass


def lancer_zone(zone):
    """Lance detecter-residus sur une zone (--detail --sans-cache)."""
    try:
        r = PROTECTIONS.lancer_protege(
            [sys.executable, DETECTEUR, "--zone", zone, "--detail", "--sans-cache"],
            timeout=60)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return "ERREUR: %s" % e


def main():
    print("=== test-046 : garde-fou compartimentation detecter-residus ===")

    # --- ETAPE PREPARATOIRE : poser les residus factices ---
    creer_residus()
    tout_pose = all(os.path.isfile(os.path.join(PROJECT_ROOT, rel))
                    for rel in RESIDUS_WORKSPACE + RESIDUS_CERVEAU
                    + [RAPPORT_RACINE, RAPPORT_LEGITIME])
    verifier("0. Residus factices poses (preparation)", tout_pose)
    if not tout_pose:
        nettoyer_residus()
        print("  (abandon : les residus factices n ont pas pu etre poses)")
        return 1

    try:
        out_w = lancer_zone("workspace")
        out_c = lancer_zone("cerveau-projet")
        out_t = lancer_zone("tous")

        # --- 1. COMPARTIMENTATION : zone workspace ---
        # voit SES residus
        ok_ws_voit = all(os.path.basename(rel) in out_w
                         for rel in RESIDUS_WORKSPACE)
        verifier("1a. Zone workspace voit ses 4 residus factices",
                 ok_ws_voit,
                 "absents=%s" % [os.path.basename(r) for r in RESIDUS_WORKSPACE
                                 if os.path.basename(r) not in out_w])
        # voit le rapport de la racine (zone workspace = racine + workspace/)
        verifier("1b. Zone workspace voit le rapport factice de la racine",
                 "rapport-factice-046" in out_w)
        # ne voit PAS le residu interne de cerveau-projet
        verifier("1c. Zone workspace NE VOIT PAS le residu de cerveau-projet",
                 ".tmp-factice-interne-046" not in out_w,
                 "chevauchement: cerveau-projet vu par workspace")

        # --- 2. COMPARTIMENTATION : zone cerveau-projet ---
        verifier("2a. Zone cerveau-projet voit son residu factice interne",
                 ".tmp-factice-interne-046" in out_c)
        ok_cp_ignore = all(os.path.basename(rel) not in out_c
                           for rel in RESIDUS_WORKSPACE + [RAPPORT_RACINE])
        verifier("2b. Zone cerveau-projet NE VOIT PAS les residus workspace/racine",
                 ok_cp_ignore,
                 "vus=%s" % [os.path.basename(r) for r in RESIDUS_WORKSPACE
                             + [RAPPORT_RACINE] if os.path.basename(r) in out_c])

        # --- 3. DEDUPLICATION : le rapport de la racine compte UNE seule fois ---
        occurrences = out_w.count("rapport-factice-046.md")
        verifier("3. Deduplication : rapport racine compte 1 fois", occurrences == 1,
                 "occurrences=%d" % occurrences)

        # --- 4. CLASSIFICATION : rapport dans un dossier parent `controles` ---
        verifier("4. Rapport dans `controles` est LEGITIME (pas RAPPORT_EGARE)",
                 "rapport-factice-legitime-046" not in out_w,
                 "rapport legitime classe a tort en egare")

        # --- 5. --tous : voit les deux zones ---
        verifier("5a. --tous voit le residu de cerveau-projet",
                 ".tmp-factice-interne-046" in out_t)
        verifier("5b. --tous voit les residus de workspace",
                 all(os.path.basename(rel) in out_t
                     for rel in RESIDUS_WORKSPACE),
                 "absents=%s" % [os.path.basename(r) for r in RESIDUS_WORKSPACE
                                 if os.path.basename(r) not in out_t])
    finally:
        # --- 6. NETTOYAGE GARANTI ---
        nettoyer_residus()
        restants = [rel for rel in RESIDUS_WORKSPACE + RESIDUS_CERVEAU
                    + [RAPPORT_RACINE, RAPPORT_LEGITIME]
                    if os.path.exists(os.path.join(PROJECT_ROOT, rel))]
        verifier("6. Nettoyage : 0 residu factice restant", len(restants) == 0,
                 "restants=%s" % restants)

    # --- 7-8. NORMES ---
    verifier("7. ASCII strict : 0 non-ASCII (test)", ascii_count(__file__) == 0)
    verifier("8. LF pur : 0 CRLF (test)", crlf_count(__file__) == 0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
