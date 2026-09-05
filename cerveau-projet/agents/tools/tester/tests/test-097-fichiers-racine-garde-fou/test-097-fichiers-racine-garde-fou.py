#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-097-fichiers-racine-garde-fou.py
GARDE-FOU : la racine du projet ne contient QUE les entrees autorisees
(liste blanche). Toute entree non autorisee a la racine (fichier egare,
dossier residuel) est signalee en KO.

Contexte (2026-08-19, demande utilisateur) : detecter-decalages-catalogue
creait son rapport a la RACINE du projet (chemin relatif par defaut dans le
CWD). Le rapport egare est reste INVISIBLE pour la non-regression : aucun
garde-fou ne verifiait le contenu de la racine. Correctif Vulcain v0.2.3 :
sortie par defaut dans cerveau-projet/agents/vulcain/rapports/. Ce test
verrouille la racine pour que plus aucun fichier ne puisse s y egare sans
etre signale.

Liste blanche (fichiers) : AGENTS.md, AGENTS-historique.md, README.md,
demarrer.md, .gitignore, .gitattributes, .tmpignore, COMMENT-DEMARRER.md
(note personnelle de l utilisateur, ajoutee a la liste blanche le 2026-08-19)
Liste blanche (dossiers) : .git, cerveau-projet, workspace, tmp-* (missions), backup-* (backups de session)

Invariants verifies :
  1. Chaque entree a la racine appartient a la liste blanche (0 entree
     non autorisee) - y compris pendant les missions (tmp-*, workspace/).
  2. Les fichiers cles du projet sont presents (AGENTS.md, README.md,
     demarrer.md, cerveau-projet/).
  3. Preuve negative : un fichier egare a la racine est detecte (puis
     supprime proprement).

Tags: residus, workspace, garde-fou, preuve-negative
"""
import importlib.util
import io
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")

# Liste blanche stricte : la racine ne doit JAMAIS contenir autre chose.
FICHIERS_AUTORISES = frozenset([
    "AGENTS.md",
    "AGENTS-historique.md",
    "AGENTS-activite-recente.md",
    "USER-DEMANDES.md",
    # Fichiers v2 SEPARES (decision utilisateur 2026-08-26 : la v2 est
    # l evolution de la v1, chaque session a SES fichiers avec SON format)
    "AGENTS-historique-v2.md",
    "AGENTS-activite-recente-v2.md",
    "README.md",
    "demarrer.md",
    ".gitignore",
    ".gitattributes",
    ".tmpignore",
    # Note personnelle de l utilisateur (autorisee explicitement, 2026-08-19)
    "COMMENT-DEMARRER.md",
])
DOSSIERS_AUTORISES = frozenset([
    ".git",
    "cerveau-projet",
    "workspace",
    # Outil exclusif de demarrage du LLM (ni v1, ni v2) - racine
    "outils-llm",
])
PREFIXES_DOSSIERS_AUTORISES = ("tmp-", "backup-")  # missions (tmp-) + backups de session (backup-2026*, commites)

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
ETAPES = []


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    print("")
    print("=== CHRONO test (total %.1fs) ====" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def entrees_non_autorisees(racine):
    """Retourne la liste des entrees de la racine hors liste blanche."""
    egarees = []
    try:
        entrees = os.listdir(racine)
    except OSError as exc:
        return ["<listdir impossible: %s>" % exc]
    for entree in sorted(entrees):
        chemin = os.path.join(racine, entree)
        if os.path.isdir(chemin):
            if entree in DOSSIERS_AUTORISES:
                continue
            if entree.startswith(PREFIXES_DOSSIERS_AUTORISES):
                continue
            egarees.append(entree + "/ (dossier)")
        else:
            if entree in FICHIERS_AUTORISES:
                continue
            egarees.append(entree)
    return egarees


def main():
    t0 = time.monotonic()
    print("=== test-097 : aucun fichier egare a la racine du projet ===")

    # 1. Chaque entree a la racine appartient a la liste blanche
    t_debut = time.monotonic()
    egarees = entrees_non_autorisees(PROJECT_ROOT)
    verifier("1. 0 entree non autorisee a la racine (liste blanche)",
             not egarees, "egarees=%s" % egarees[:8])
    chrono_etape("1. liste blanche racine", t_debut)

    # 2. Les fichiers cles du projet sont presents
    t_debut = time.monotonic()
    manquants = [f for f in ("AGENTS.md", "README.md", "demarrer.md")
                 if not os.path.isfile(os.path.join(PROJECT_ROOT, f))]
    if not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
        manquants.append("cerveau-projet/")
    verifier("2. fichiers cles presents (AGENTS.md, README.md, demarrer.md, "
             "cerveau-projet/)", not manquants, "manquants=%s" % manquants)
    chrono_etape("2. fichiers cles", t_debut)

    # 3. Preuve negative : un fichier egare a la racine est detecte
    t_debut = time.monotonic()
    egare = os.path.join(PROJECT_ROOT, "fichier-egare-test-097.tmp")
    preuve_ok = False
    try:
        with io.open(egare, "w", encoding="ascii", newline="\n") as fh:
            fh.write("artefact de test\n")
        detectes = entrees_non_autorisees(PROJECT_ROOT)
        preuve_ok = "fichier-egare-test-097.tmp" in detectes
    finally:
        if os.path.isfile(egare):
            os.remove(egare)
    verifier("3. preuve negative : fichier egare a la racine detecte",
             preuve_ok, "fichier egare non detecte")
    chrono_etape("3. preuve negative", t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
