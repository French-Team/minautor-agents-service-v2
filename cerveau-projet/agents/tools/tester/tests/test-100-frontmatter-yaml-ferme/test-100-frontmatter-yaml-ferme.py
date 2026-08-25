#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-100-frontmatter-yaml-ferme.py

GARDE-FOU : tout fichier .md commencant par un frontmatter YAML (---) doit
avoir sa cloture (---). Un frontmatter non ferme rend le fichier illisible
dans les previews markdown (erreur "Failed to parse frontmatter: Implicit
keys need to be on a single line").

Contexte (2026-08-24, incident preview utilisateur) : les rapports Themis
(bilan-strategique-v1, comparatif-v1-v2, synthese-v1-pour-v2) avaient un
frontmatter YAML NON FERME (il manquait le '---' de cloture apres les cles).
Aucun outil de validation existant ne verifiait la cloture : le defaut etait
invisible pour la non-regression et ne se manifestait que dans le preview de
l utilisateur. Ce test verrouille la cloture pour que plus aucun fichier .md
du projet ne puisse porter un frontmatter ouvert sans etre signale.

Invariants verifies :
  1. Tout fichier .md commencant par '---' a bien sa cloture '---' (le
     frontmatter est un bloc ferme) - sur TOUT le projet. Le contenu du
     bloc n est pas verifie (un frontmatter avec seulement des commentaires
     ou des block scalars est volontairement accepte : le projet ne parse
     jamais ces en-tetes en YAML strict).
  2. Preuve negative : un fichier .md a frontmatter ouvert (sans cloture)
     est detecte (puis supprime proprement).

Perimetre : tous les .md sous PROJECT_ROOT sauf .git/ et workspace/.
Tags: frontmatter, yaml, markdown, garde-fou, preview
"""
import importlib.util
import io
import os
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")

EXCLUSIONS = (".git", "workspace", "__pycache__", "node_modules")

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
    print("=== CHRONO test (total %.1fs) ===" % total)
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


def lister_fichiers_md(racine):
    """Lister tous les fichiers .md sous racine, hors exclusions."""
    resultat = []
    for dossier, sous_dossiers, fichiers in os.walk(racine):
        sous_dossiers[:] = [d for d in sous_dossiers
                            if d not in EXCLUSIONS]
        for fichier in fichiers:
            if fichier.endswith(".md"):
                resultat.append(os.path.join(dossier, fichier))
    return sorted(resultat)


def frontmatter_ferme(chemin):
    """Verifie qu un fichier .md a un frontmatter YAML ferme s il en a un.

    Retourne (ok, message) :
      - ok=True  : pas de frontmatter, ou frontmatter ouvert ET ferme.
      - ok=False : le fichier commence par '---' mais la cloture manque
                   (ou le bloc est vide/mal forme).
    """
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            lignes = fh.read().splitlines()
    except OSError as exc:
        return False, "lecture impossible: %s" % exc

    if not lignes:
        return True, "fichier vide (pas de frontmatter)"
    if not lignes[0].strip() == "---":
        return True, "pas de frontmatter"

    # Le fichier commence par '---' : il faut une cloture '---'.
    # On cherche la prochaine ligne '---' apres la premiere.
    for i in range(1, len(lignes)):
        if lignes[i].strip() == "---":
            # Cloture trouvee (le contenu du bloc n est pas verifie : un
            # frontmatter avec seulement des commentaires est valide).
            return True, "frontmatter ferme (ligne %d)" % (i + 1)

    return False, "frontmatter OUVERT (cloture '---' manquante)"


def main():
    t0 = time.monotonic()
    print("=== test-100 : frontmatter YAML ferme sur tous les .md ===")

    # 1. Tout fichier .md commencant par '---' a sa cloture
    t_debut = time.monotonic()
    md_files = lister_fichiers_md(PROJECT_ROOT)
    non_conformes = []
    nb_avec_frontmatter = 0
    for chemin in md_files:
        ok, message = frontmatter_ferme(chemin)
        if not ok:
            relatif = os.path.relpath(chemin, PROJECT_ROOT)
            non_conformes.append("%s: %s" % (relatif, message))
        else:
            if message.startswith("frontmatter"):
                nb_avec_frontmatter += 1
    verifier("1. tout .md avec frontmatter a sa cloture '---' (%d .md, %d "
             "avec frontmatter)" % (len(md_files), nb_avec_frontmatter),
             not non_conformes, "non conformes=%s" % non_conformes[:8])
    chrono_etape("1. cloture frontmatter", t_debut)

    # 2. Preuve negative : un frontmatter ouvert est detecte
    t_debut = time.monotonic()
    preuve_ok = False
    tmpdir = tempfile.mkdtemp(prefix="test-100-")
    try:
        egare = os.path.join(tmpdir, "frontmatter-ouvert.md")
        with io.open(egare, "w", encoding="ascii", newline="\n") as fh:
            fh.write("---\nidentite:\n  nom: test\n# titre sans cloture\n")
        ok, message = frontmatter_ferme(egare)
        preuve_ok = (not ok) and "OUVERT" in message
    finally:
        if os.path.isdir(tmpdir):
            import shutil
            shutil.rmtree(tmpdir)
    verifier("3. preuve negative : frontmatter ouvert detecte", preuve_ok,
             "frontmatter ouvert non detecte")
    chrono_etape("3. preuve negative", t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
