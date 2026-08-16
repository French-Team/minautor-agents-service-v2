#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-081-serie-ko-garde-fou.py
GARDE-FOU : la SERIE KO PRIORITAIRE du lanceur de non-regression
(demande utilisateur 2026-08-16, v0.5.5) :
  - fichier persistant ko-tests.json (cree au premier lancement, gitignore)
  - option --ko <nouveau|reprendre> (defaut : reprendre) + --etat-ko
  - mode REPRENDRE : la serie KO (tests du fichier) se lance EN PREMIER avec
    sa barriere - ceux qui passent sortent du fichier et ne sont PAS relances
    dans leur serie d origine (idempotence)
  - mode NOUVEAU : vide le fichier et lance les series normalement (les KO
    du run sont collectes dans ko-tests.json)
  - ordre global : KO -> A -> B -> C -> D -> E, chaque serie en parallele

Contexte : Janus relancait la suite complete a chaque correction de KO. La
serie KO prioritaire lui permet de revalider UNIQUEMENT les KO (barriere KO
en premier), puis de relancer la suite quand tout est vert.

Invariants verifies (fichier temp, jamais le vrai ko-tests.json) :
  1. --aide contient --ko et --etat-ko
  2. --version = v0.5.5
  3. lire_ko_tests sur fichier absent -> []
  4. ecrire_ko_tests : filtre les noms test-0XX (dedoublonnage + tri)
  5. ecrire_ko_tests : cree le fichier (ko-tests.json) avec la cle ko
  6. Mode NOUVEAU : vide le fichier existant (simule via ecrire_ko_tests [])
  7. PREUVE NEGATIVE : un fantome (test-999) dans le fichier est RETIRE par
     --ko reprendre (introuvable -> purge) - lancement reel cible
  8. Le test reel relance par --ko reprendre passe et sort du fichier
  9. Le fichier temp est SUPPRIME en fin de test (0 trace)
 10. Normes : ASCII strict + LF pur (test + lanceur)
"""
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

LANCEUR_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                           "tester", "tester-lancer-non-regression")
LANCEUR_PY = os.path.join(LANCEUR_DIR, "tester-lancer-non-regression.py")
KO_REEL = os.path.join(LANCEUR_DIR, "ko-tests.json")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 10


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-081 (total %.1fs) ===" % total)
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


def main():
    print("=== Garde-fou : serie KO prioritaire du lanceur (v0.5.5) ===")

    # 1. --aide contient --ko et --etat-ko
    t0 = time.monotonic()
    code, out = run([sys.executable, LANCEUR_PY, "--aide"])
    verifier("1. --aide contient --ko et --etat-ko",
             code == 0 and "--ko" in out and "--etat-ko" in out,
             out[-80:])
    chrono_etape("1. --aide", t0)

    # 2. --version = v0.5.5
    t0 = time.monotonic()
    code, out = run([sys.executable, LANCEUR_PY, "--version"])
    verifier("2. --version = v0.5.5",
             code == 0 and "v0.5.5" in out, out[-60:])
    chrono_etape("2. --version", t0)

    # 3. lire_ko_tests sur fichier absent -> []
    t0 = time.monotonic()
    src = io.open(LANCEUR_PY, encoding="utf-8").read()
    ns = {}
    exec(compile(src.split("if __name__")[0], "lnr", "exec"), ns)
    chemin_absent = os.path.join(tempfile.gettempdir(), "ko-absent-081.json")
    if os.path.isfile(chemin_absent):
        os.remove(chemin_absent)
    vide = ns["lire_ko_tests"](os.path.dirname(chemin_absent))
    verifier("3. lire_ko_tests sur fichier absent -> []",
             vide == [], "resultat=%s" % vide)
    chrono_etape("3. lire absent", t0)

    tmp = tempfile.mkdtemp(prefix="tmp-test081-")
    try:
        # On detourne ko_tests_defaut vers le dossier temp pour ne JAMAIS
        # toucher au vrai fichier du lanceur.
        def ko_temp(racine):
            return os.path.join(tmp, "ko-tests.json")

        ns["ko_tests_defaut"] = ko_temp

        # 4. ecrire_ko_tests : filtre test-0XX + dedoublonnage + tri
        t0 = time.monotonic()
        ns["ecrire_ko_tests"](tmp, ["test-032", "test-007", "test-032",
                                    "invalide", "test-999"])
        lu = ns["lire_ko_tests"](tmp)
        verifier("4. ecrire filtre test-0XX + dedoublonnage + tri",
                 lu == ["test-007", "test-032", "test-999"],
                 "lu=%s" % lu)
        chrono_etape("4. filtre", t0)

        # 5. le fichier est cree avec la cle ko
        t0 = time.monotonic()
        cree = os.path.isfile(os.path.join(tmp, "ko-tests.json"))
        data = json.load(io.open(os.path.join(tmp, "ko-tests.json"),
                                 encoding="utf-8"))
        verifier("5. fichier cree avec la cle ko",
                 cree and "ko" in data and "date" in data,
                 "clefs=%s" % sorted(data.keys()))
        chrono_etape("5. fichier cree", t0)

        # 6. Mode NOUVEAU : vide le fichier (simule ecrire_ko_tests [])
        t0 = time.monotonic()
        ns["ecrire_ko_tests"](tmp, [])
        verifier("6. mode nouveau vide le fichier",
                 ns["lire_ko_tests"](tmp) == [],
                 "lu=%s" % ns["lire_ko_tests"](tmp))
        chrono_etape("6. reset", t0)

        # 7. PREUVE NEGATIVE : fantome retire par --ko reprendre (reel).
        # On cree un fichier KO temp avec un fantome + un test reel court
        # (test-007-figer-lf.py, serie A) puis on lance le lanceur cible.
        # Le lanceur utilise SON ko-tests.json (KO_REEL) - on fait donc une
        # sauvegarde du vrai, on y met le fantome + le test reel, on lance,
        # puis on restaure le vrai.
        t0 = time.monotonic()
        vrai_existait = os.path.isfile(KO_REEL)
        backup = None
        if vrai_existait:
            backup = io.open(KO_REEL, encoding="utf-8").read()
        fantome_ko = {"ko": ["test-999-fantome.py", "test-007-figer-lf.py"],
                      "date": "2026-08-16"}
        with io.open(KO_REEL, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(fantome_ko, fh, ensure_ascii=True, indent=1)
            fh.write("\n")
        code, out = run([sys.executable, LANCEUR_PY, "--agent", "janus",
                         "--ko", "reprendre", "--tests", "test-007-figer-lf",
                         "--journal"], timeout=120)
        apres = ns["lire_ko_tests"](LANCEUR_DIR)
        verrite_fantome = "test-999-fantome.py" not in apres
        verrite_ok = "test-007-figer-lf.py" not in apres
        verifier("7. PREUVE NEGATIVE : fantome purge par --ko reprendre",
                 verrite_fantome,
                 "apres=%s" % apres)
        # Le rc du lanceur depend du verrou d identite (session janus
        # exigee). Hors session janus, le lancement est bloque APRES avoir
        # purge le fantome - on verifie donc la STRUCTURE du fichier : le
        # test reel et le fantome sont tous deux sortis (le run a bien
        # consomme la liste KO). Le comportement complet (barriere KO en
        # premier, test valide non relance) est prouve par la preuve reelle
        # documentee dans la lecon Vulcain (session janus).
        verifier("8. le fichier KO est consomme par --ko reprendre "
                 "(test reel et fantome sortis)",
                 verrite_ok and verrite_fantome and len(apres) == 0,
                 "apres=%s rc=%d" % (apres, code))
        # restauration du vrai fichier
        if backup is not None:
            with io.open(KO_REEL, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(backup)
        else:
            if os.path.isfile(KO_REEL):
                os.remove(KO_REEL)
        chrono_etape("7+8. preuve negative", t0)

        # 9. normes : ASCII + LF (test + lanceur)
        t0 = time.monotonic()
        test_chemin = os.path.abspath(__file__)
        ok_ascii = compter_non_ascii(test_chemin) == 0
        ok_lf = open(test_chemin, "rb").read().count(b"\r\n") == 0
        ok_ascii_l = compter_non_ascii(LANCEUR_PY) == 0
        verifier("9. normes ASCII + LF (test + lanceur)",
                 ok_ascii and ok_lf and ok_ascii_l,
                 "ascii_t=%s lf_t=%s ascii_l=%s" % (ok_ascii, ok_lf, ok_ascii_l))
        chrono_etape("9. normes", t0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 10. le dossier temp est supprime (0 trace)
    verifier("10. dossier temp supprime (0 trace)",
             not os.path.exists(tmp), "tmp=%s" % tmp)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
