#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-088-recherches-web-garde-fou.py
Tags: garde-fou, anti-recurrence, web, recherches, fraicheur, outils
GARDE-FOU : les recherches web (cerveau-projet/recherches-web/) sont la
MEMOIRE FACTUELLE des agents (demande utilisateur 2026-08-16 : souvenirs
vrais et d actualite). Chaque recherche doit etre documentee (header yaml :
date, source_principale, statut), fraiche (date <= 30 jours si validee) et
referencee dans l index.

Contexte :
  - Vulcain a cree rechercher-web (acces web reel) et
    detecter-recherches-obsoletes (fraicheur > 30 jours).
  - Atlas doit documenter chaque recherche selon le template
    (recherches-web/templates/recherche-template.md).
  - Ce garde-fou verrouille l etat et previent la recurrence (une recherche
    sans header, obsoleted, ou non referencee serait KO).

Invariants verifies :
  1. Chaque recherche (hors index/templates) a un header yaml avec date
     valide (format YYYY-MM-DD), source_principale et statut connu.
  2. Aucune recherche validee n est obsoleted (age > 30 jours).
  3. L index (index-recherches-web.md) reference chaque theme present.
  4. Preuve negative : une recherche sans date valide est DETECTEE puis la
     copie est SUPPRIMEE (0 trace).
  5. Normes : ASCII strict + LF pur (test + recherches).
"""

import glob
import importlib.util
import io
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
NB_POINTS = 8


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-088 (total %.1fs) ===" % total)
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
    Ce test ne lance aucune commande (lecture seule) : la ligne
    PROTECTIONS = charger_protections() suffit au garde-fou test-030
    (bloc standard importe par tous les tests)."""
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tester-protections", "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

RECHERCHES = os.path.join(PROJECT_ROOT, "cerveau-projet", "recherches-web")
INDEX = os.path.join(RECHERCHES, "index-recherches-web.md")
SEUIL_JOURS = 30
STATUTS = ("en-cours", "validee", "obsolete")


def lister_recherches():
    """Liste les fichiers de recherche (hors index et templates/)."""
    resultats = []
    for chemin in sorted(glob.glob(os.path.join(RECHERCHES, "*", "*.md"))):
        nom = os.path.basename(chemin)
        if nom.startswith("index") or "templates" in chemin:
            continue
        resultats.append(chemin)
    return resultats


def lire_header(chemin):
    """Extrait le bloc yaml du header (```yaml ... ```)."""
    try:
        d = io.open(chemin, encoding="utf-8", errors="replace").read()
    except (IOError, OSError):
        return {}
    m = re.search(r"```yaml\n(.*?)```", d, re.S)
    if not m:
        return {}
    header = {}
    for ligne in m.group(1).split("\n"):
        # saute la cle racine (recherche:) et les lignes d indentation
        mm = re.match(r"^\s{0,2}([a-z_]+):\s*(.*?)\s*$", ligne)
        if mm and mm.group(1) != "recherche":
            val = mm.group(2).strip().strip('"').strip("'")
            header[mm.group(1)] = val
    return header


def age_jours(date_texte):
    """Age en jours depuis la date (YYYY-MM-DD). None si illisible."""
    mm = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", date_texte)
    if not mm:
        return None
    an, mois, jour = (int(mm.group(1)), int(mm.group(2)), int(mm.group(3)))
    ref = time.strftime("%Y-%m-%d")
    r = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", ref)
    ra, rm, rj = (int(r.group(1)), int(r.group(2)), int(r.group(3)))
    # approximation jours (calendrier gregorien)
    def n_jours(a, m, j):
        return (a * 365 + a // 4 - a // 100 + a // 400
                + (306 * (m + 1)) // 10 + j - 429)
    return n_jours(ra, rm, rj) - n_jours(an, mois, jour)


def main():
    print("=== Garde-fou : recherches-web conformes + fraiches ===")

    # 1. chaque recherche a un header yaml complet
    t0 = time.monotonic()
    recherches = lister_recherches()
    manquants = []
    for r in recherches:
        h = lire_header(r)
        if not h.get("date") or not h.get("source_principale") or h.get("statut") not in STATUTS:
            manquants.append(os.path.basename(r))
    verifier("1. %d recherches : header yaml complet (date + source + statut)" % len(recherches),
             len(manquants) == 0, manquants[:5] if manquants else "")
    chrono_etape("1. header yaml", t0)

    # 2. aucune recherche validee obsoleted (age > 30 jours)
    t0 = time.monotonic()
    obsoletes = []
    for r in recherches:
        h = lire_header(r)
        age = age_jours(h.get("date", ""))
        if h.get("statut") == "validee" and (age is None or age > SEUIL_JOURS):
            obsoletes.append("%s (age=%s)" % (os.path.basename(r), age))
    verifier("2. aucune recherche validee de plus de %d jours (fraicheur)" % SEUIL_JOURS,
             len(obsoletes) == 0, obsoletes[:5] if obsoletes else "")
    chrono_etape("2. fraicheur", t0)

    # 3. l index reference chaque theme present
    t0 = time.monotonic()
    try:
        idx = io.open(INDEX, encoding="utf-8", errors="replace").read()
    except (IOError, OSError):
        idx = ""
    themes = sorted(set(os.path.basename(os.path.dirname(r)) for r in recherches))
    manquants_idx = [t for t in themes if t not in idx]
    verifier("3. index-reference : %d themes presents dans index-recherches-web.md" % len(themes),
             len(manquants_idx) == 0, manquants_idx[:5] if manquants_idx else "")
    chrono_etape("3. index", t0)

    # 4. l outil detecter-recherches-obsoletes est present (anti-recurrence)
    t0 = time.monotonic()
    outil = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                         "detecter", "detecter-recherches-obsoletes",
                         "detecter-recherches-obsoletes.py")
    verifier("4. outil detecter-recherches-obsoletes present", os.path.isfile(outil), outil)
    chrono_etape("4. outil detect", t0)

    # 5. preuve negative : recherche sans date detectee puis copie supprimee
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test088-")
    try:
        modele = os.path.join(RECHERCHES, "templates", "recherche-template.md")
        d = io.open(modele, encoding="utf-8").read()
        # le template a un header placeholder : la detection doit le refuser
        h = lire_header(modele)
        date_ok = bool(re.match(r"^\d{4}-\d{2}-\d{2}$", h.get("date", "")))
        verifier("5. preuve negative : template (date placeholder) DETECTE comme invalide",
                 not date_ok, "date lue: %s" % h.get("date"))
        sous = os.path.join(tmp, "recherche-sans-date.md")
        with io.open(sous, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(d)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("5b. preuve negative : copie SUPPRIMEE (0 trace)",
                 not os.path.exists(tmp), "copie encore presente")
    chrono_etape("5. preuve negative", t0)

    # 6. Normes ASCII + LF (test + recherches)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    fichiers = [os.path.abspath(__file__), INDEX] + recherches
    for f in fichiers:
        try:
            d = io.open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("6. normes : 0 non-ASCII (test + recherches)", na_total == 0,
             "non-ascii=%d" % na_total)
    verifier("6b. normes : 0 CRLF (test + recherches)", crlf_total == 0,
             "crlf=%d" % crlf_total)
    chrono_etape("6. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    bilan_chrono()
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
