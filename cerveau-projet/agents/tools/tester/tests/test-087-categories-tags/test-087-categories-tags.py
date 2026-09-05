#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-087-categories-tags.py
Tags: garde-fou, anti-recurrence, outil
GARDE-FOU : chaque test-0XX de la non-regression doit porter un bloc 'Tags:'
(dans sa docstring ou son en-tete de commentaires) permettant la
categorisation par le lanceur (--tags / --categorie, demande utilisateur
2026-08-16). Les tags doivent appartenir a la taxonomie de
categories-tests.json (noms de categories + tags definis + tags specifiques
documentes).

Contexte :
  - Vulcain a cree la mecanique : le lanceur v0.5.7 lit le bloc 'Tags:' de
    chaque test, categories-tests.json definit les categories (securite,
    conventions, agents, outils, registre-traces, performance,
    anti-recurrence).
  - Morpheus a tague les 84 tests. Ce garde-fou verrouille l etat et
    previent la recurrence (un nouveau test sans Tags: serait KO).

Invariants verifies :
  1. Chaque test-0XX a un bloc 'Tags:' (docstring ou commentaire).
  2. Chaque bloc contient au moins 1 tag.
  3. Chaque tag appartient a la taxonomie autorisee (categories-tests.json
     + tags specifiques documentes).
  4. Preuve negative : une copie sans bloc Tags: est DETECTEE puis SUPPRIMEE.
  5. Normes : ASCII strict + LF pur.
"""

import glob
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 7


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-087 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)


def charger_protections():
    """Charge le module tester-protections (bloc standard, modele test-066).
    Ce test n execute aucune commande (lecture seule + copie temp) : la
    ligne PROTECTIONS = charger_protections() suffit au garde-fou test-030
    (bloc standard importe par tous les tests)."""
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tester-protections", "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

TESTS_GLOB = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tests", "test-0*", "test-0*.py")
CATEGORIES_PATH = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                               "tools", "tester", "tester-lancer-non-regression",
                               "categories-tests.json")

# Tags specifiques documentes (hors taxonomie des categories mais legitimes)
TAGS_SPECIFIQUES = set([
    "evaluer", "moteur", "cartographier", "guider", "valider", "spec",
    "ligne", "scripts-temp", "series", "coherence", "protections", "readme",
    "residus", "outils-externes", "protocole", "entonnoir", "triplet",
    "registre", "analyse", "compartimentation", "rating", "profils",
    "exclusivites", "purifier", "bumper", "valeurs-magiques", "lecons",
    "relecture", "relancer-ko", "corriger", "troncatures", "amelioration",
    "nommage", "fiches", "environnement", "ko", "workspace", "regles",
    "processus", "detecter", "hermes", "hygie", "clio", "buffy", "cerberus",
    "janus", "morpheus", "chrono", "pool", "workers", "marbre", "verrou",
    "habilitation", "anti-contournement", "ascii", "lf", "template", "budget",
    "parcours", "garde-fou", "anti-recurrence", "preuve-negative", "perf",
    "duree", "reference-temps", "combos", "generateurs", "outil", "catalogue",
    "recherches", "fraicheur", "web",
    # Tags des tests v2 + migration (2026-09-05) : ajoutes a la taxonomie
    # car les tests 100-126 (pilote, routines, vigie, notation, vestiges v1,
    # bdd-lecons...) portent des tags specifiques legitimes.
    "vestiges", "vestiges-v1", "v1", "v2", "migration", "reverse",
    "arbres-v2", "modele-aero", "format-v2", "bdd-lecons", "scission",
    "2-bdd", "frontmatter", "yaml", "markdown", "preview", "agents-md",
    "verifier-coherence", "vigie", "round", "oracle", "pilote", "notation",
    "routine", "anti-inondation", "evaluation", "routines", "surveillance",
    "flux", "sante", "encart", "live", "vigie-perimetre", "compteur",
    "tokens", "entree", "sortie", "fantome", "controle", "harnais",
    "relais", "hub", "corruption", "jsonl", "fiche", "d17", "d6", "d7",
    "etat-carte", "anti-redemarrage", "detecter-fins-passives",
    "anti-heredoc", "formulaire", "executer-formulaire", "injection-outil",
    "p2", "r7", "etats", "colonne-etat", "file", "files", "classification",
    "ordre-importance", "flux-mot", "declencheurs", "theme", "fin-oracle",
    "consommateur", "lister-flags", "flags", "dry-run",
    "valider-cartes-decision", "arbre", "terminer", "mission",
    "notification", "gel", "corrections.md", "anti-regression", "fixture",
    "idempotence",
])


def lire_tags(chemin):
    """Lit le bloc Tags: (docstring 'Tags:' ou commentaire '# Tags:')."""
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            tete = fh.read(4096)
    except (IOError, OSError):
        return []
    m = re.search(r"^#?\s*Tags:\s*(.+)$", tete, re.M)
    if not m:
        return []
    return [t.strip().lower() for t in m.group(1).split(",") if t.strip()]


def charger_taxonomie():
    """Retourne l ensemble des tags autorises (categories + tags + specifiques)."""
    autorises = set()
    try:
        with io.open(CATEGORIES_PATH, encoding="utf-8") as fh:
            cat = json.load(fh)
        for nom, tags in cat.get("categories", {}).items():
            autorises.add(nom)
            autorises.update(tags)
    except (IOError, OSError, ValueError):
        pass
    autorises |= TAGS_SPECIFIQUES
    return autorises


def main():
    print("=== Garde-fou : Tags de categorisation sur tous les tests ===")

    # 1. tous les tests ont un bloc Tags
    t0 = time.monotonic()
    tests = sorted(glob.glob(TESTS_GLOB))
    sans_tags = [os.path.basename(t) for t in tests if not lire_tags(t)]
    verifier("1. %d tests : chacun a un bloc Tags:" % len(tests),
             len(sans_tags) == 0, sans_tags[:5] if sans_tags else "")
    chrono_etape("1. scan Tags", t0)

    # 2. chaque bloc a au moins 1 tag
    t0 = time.monotonic()
    vides = [os.path.basename(t) for t in tests
             if len(lire_tags(t)) == 0]
    verifier("2. chaque bloc Tags: non vide", len(vides) == 0,
             vides[:5] if vides else "")
    chrono_etape("2. blocs non vides", t0)

    # 3. tags dans la taxonomie
    t0 = time.monotonic()
    autorises = charger_taxonomie()
    invalides = []
    for t in tests:
        for tag in lire_tags(t):
            if tag not in autorises:
                invalides.append("%s:%s" % (os.path.basename(t), tag))
    verifier("3. %d tags autorises (taxonomie categories-tests.json)" % len(autorises),
             len(invalides) == 0, invalides[:5] if invalides else "")
    chrono_etape("3. taxonomie", t0)

    # 4. categories-tests.json valide + couvre les categories
    t0 = time.monotonic()
    try:
        with io.open(CATEGORIES_PATH, encoding="utf-8") as fh:
            cat = json.load(fh)
        noms = sorted(cat.get("categories", {}).keys())
        verifier("4. categories-tests.json valide (%d categories: %s)" %
                 (len(noms), ", ".join(noms)), len(noms) >= 5, noms)
    except (IOError, OSError, ValueError) as e:
        verifier("4. categories-tests.json valide", False, str(e)[-80:])
    chrono_etape("4. categories json", t0)

    # 5. preuve negative : copie sans Tags detectee puis supprimee
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test087-")
    try:
        src = None
        for f in glob.glob(TESTS_GLOB):
            if "test-057-marbre-garde-fou" in f:
                src = f
                break
        if src is None:
            verifier("5. preuve negative : source trouvee", False,
                     "test-057 introuvable")
        else:
            d = io.open(src, encoding="utf-8").read()
            d2 = re.sub(r"^#?\s*Tags:.*$\n", "", d, count=1, flags=re.M)
            sous = os.path.join(tmp, "test-999-sans-tags.py")
            with io.open(sous, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(d2)
            tags_retires = lire_tags(sous)
            verifier("5. preuve negative : test sans Tags: DETECTE",
                     len(tags_retires) == 0, "tags encore lus: %s" % tags_retires)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("5b. preuve negative : copie SUPPRIMEE (0 trace)",
                 not os.path.exists(tmp), "copie encore presente")
    chrono_etape("5. preuve negative", t0)

    # 6. Normes ASCII + LF (test + tests tagues)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    fichiers = [os.path.abspath(__file__)] + tests
    for f in fichiers:
        try:
            d = io.open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("6. normes : 0 non-ASCII (test + tests tagues)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("6b. normes : 0 CRLF (test + tests tagues)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("6. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" %
          (NB_OK, NB_KO, NB_POINTS))
    bilan_chrono()
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
