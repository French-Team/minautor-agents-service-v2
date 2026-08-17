#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-076-all-mode-par-defaut.py
GARDE-FOU : --all est le MODE PAR DEFAUT de corriger-accents-zones-sensibles
(v0.2.3, demande utilisateur 2026-08-16) - une commande SANS option purge
desormais TOUS les accents (y compris le corps du texte), conformement a la
regle immuable (aucun caractere non-ASCII tolere).

Contexte :
  - La doc disait deja 'le mode standard est --all (regle immuable)' mais le
    defaut de l outil ne l appliquait pas : une commande sans --all
    CONSERVAIT les accents du corps ('Aucune correction necessaire') et
    poussait les agents a corriger a la main (diagnostic Morpheus accents).
  - v0.2.3 : defaut inverse (purge totale sans option) + nouvelle option
    --zones-seules (ancien comportement ponctuel : zones sensibles
    uniquement) + --all conserve (compat, explicite).

Invariants verifies (fichier temp, jamais le vrai registre) :
  1. corriger-accents-zones-sensibles --version = 0.2.3-py
  2. L option --zones-seules est presente dans --aide.
  3. PREUVE RELLE : fichier temp avec accents dans le corps -> lancement
     SANS option = PURGE TOTALE (0 non-ascii restant).
  4. --zones-seules = accents du corps CONSERVES (mode ponctuel).
  5. --all explicite = purge totale (compat, meme comportement que le defaut).
  6. --dry-run = fichier INCHANGE (aucune ecriture).
  7. Le fichier temp est SUPPRIME en fin de test (0 trace).
  8. Normes : ASCII strict + LF pur (test + outil py/sh/md).
Tags: outils, corriger, garde-fou
"""
import importlib.util
import io
import os
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

OUTIL_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                         "corriger", "corriger-accents-zones-sensibles")
OUTIL_PY = os.path.join(OUTIL_DIR, "corriger-accents-zones-sensibles.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "corriger-accents-zones-sensibles.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "corriger-accents-zones-sensibles.md")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 9


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-076 (total %.1fs) ===" % total)
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


def charger_protections():
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tester-protections", "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def run(cmd, timeout=120):
    # PROTECTION : toute execution passe par lancer_protege (jamais de
    # subprocess.run brut - test-030 verifie cette regle).
    try:
        r = PROTECTIONS.lancer_protege(cmd, timeout=timeout,
                                       capture_output=True, text=True)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, "ERREUR: %s" % str(e)[-80:]


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for ch in fh.read() if ord(ch) > 127)


def ecrire_corps(chemin):
    """Fichier avec accents francais dans le corps (le cas qui plantait)."""
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# -*- coding: utf-8 -*-\n")
        fh.write("## [LECON] Test defaut\n")
        fh.write("V\u00e9rification avec accents fran\u00e7ais : "
                 "d\u00e9j\u00e0, \u00e9valuation, v\u00e9rifier.\n")


def main():
    print("=== Garde-fou : --all mode par defaut de corriger-accents-zones-sensibles v0.2.3 ===")

    # 1. Version 0.2.3-py
    t0 = time.monotonic()
    code, out = run([sys.executable, OUTIL_PY, "--version"])
    verifier("1. --version = 0.2.3-py",
             code == 0 and "0.2.3-py" in out, out.strip()[-40:])
    chrono_etape("1. version", t0)

    # 2. Option --zones-seules presente dans --aide
    t0 = time.monotonic()
    code, out = run([sys.executable, OUTIL_PY, "--aide"])
    verifier("2. option --zones-seules presente dans --aide",
             "--zones-seules" in out, out[-160:] if "--zones-seules" not in out else "")
    chrono_etape("2. option --aide", t0)

    tmp = tempfile.mkdtemp(prefix="tmp-test076-")
    try:
        # 3. PREUVE RELLE : sans option = PURGE TOTALE
        t0 = time.monotonic()
        f = os.path.join(tmp, "corps.md")
        ecrire_corps(f)
        avant = compter_non_ascii(f)
        code, out = run([sys.executable, OUTIL_PY, f])
        apres = compter_non_ascii(f)
        verifier("3. sans option = purge totale (6 accents -> 0)",
                 avant == 6 and apres == 0,
                 "avant=%d apres=%d out=%s" % (avant, apres, out[-80:]))
        chrono_etape("3. purge par defaut", t0)

        # 4. --zones-seules = accents du corps CONSERVES
        t0 = time.monotonic()
        f2 = os.path.join(tmp, "corps2.md")
        ecrire_corps(f2)
        code, out = run([sys.executable, OUTIL_PY, f2, "--zones-seules"])
        restants = compter_non_ascii(f2)
        verifier("4. --zones-seules = corps conserve (6 restants)",
                 restants == 6,
                 "restants=%d (attendu 6) out=%s" % (restants, out[-80:]))
        chrono_etape("4. zones-seules", t0)

        # 5. --all explicite = purge totale (compat)
        t0 = time.monotonic()
        f3 = os.path.join(tmp, "corps3.md")
        ecrire_corps(f3)
        code, out = run([sys.executable, OUTIL_PY, f3, "--all"])
        restants = compter_non_ascii(f3)
        verifier("5. --all explicite = purge totale (compat)",
                 restants == 0,
                 "restants=%d (attendu 0)" % restants)
        chrono_etape("5. --all compat", t0)

        # 6. --dry-run = fichier INCHANGE
        t0 = time.monotonic()
        f4 = os.path.join(tmp, "dry.md")
        ecrire_corps(f4)
        avant_b = io.open(f4, "rb").read()
        code, out = run([sys.executable, OUTIL_PY, f4, "--dry-run"])
        apres_b = io.open(f4, "rb").read()
        verifier("6. --dry-run = fichier inchange",
                 avant_b == apres_b, "fichier modifie par dry-run")
        chrono_etape("6. dry-run", t0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("7. fichier temp SUPPRIME en fin de test (0 trace)",
                 not os.path.exists(tmp), "residu : %s" % tmp)
        chrono_etape("7. purge", t0)

    # 8. Normes ASCII + LF (test + outil py/sh/md)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    for f in [os.path.abspath(__file__), OUTIL_PY, OUTIL_SH, OUTIL_MD]:
        d = io.open(f, encoding="utf-8", errors="replace").read()
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("8. normes : 0 non-ASCII (test + outil py/sh/md)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("8b. normes : 0 CRLF (test + outil py/sh/md)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("8. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % (
        "PROPRE (--all par defaut verrouille)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
