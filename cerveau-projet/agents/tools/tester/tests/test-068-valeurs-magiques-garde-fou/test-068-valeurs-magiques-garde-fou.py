#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-068-valeurs-magiques-garde-fou.py
GARDE-FOU : la REGLE D OR anti-valeurs-magiques est gravee dans les regles
globales ET protegee par le marbre, et l outil detecter-donnees-en-dur
detecte les secrets en dur (niveau .env).

Contexte (decision utilisateur 2026-08-16) :
  - Strategie de configuration et elimination des valeurs magiques : le code
    ne doit jamais CONNAITRE les valeurs, il doit savoir OU aller pour les
    trouver. Hierarchie : (1) constante nommee, (2) config.json/YAML,
    (3) .env pour les secrets. Maxime : la logique CONSOMME les variables,
    elle ne les CONTIENT pas.
  - La regle a ete gravee dans regles-general-global.md (zone du MARBRE,
    protegee par empreinte SHA-256, modification via la porte uniquement).
  - detecter-donnees-en-dur v0.1.1 detecte les SECRETS_EN_DUR (api_key,
    password, token) a deplacer dans .env.

Invariants verifies :
  1. La regle est gravee dans regles-general-global.md avec la hierarchie
     (constante, config, .env)
  2. La zone regles-general-global est DANS LE MARBRE (verrou-marbre --tous
     : 0 KO, la zone est listee)
  3. detecter-donnees-en-dur v0.1.1 : --version + SECRETS_EN_DUR detecte
     (preuve : fichier temporaire avec API_KEY -> detecte, os.environ ->
     exclu, placeholder -> exclu)
  4. Normes : ASCII strict + LF pur (outil + test)
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

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

REGLES_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "regles-immuables")
REGLES_GLOBAL = os.path.join(REGLES_DIR, "general", "regles-general-global.md")
DETECT_DIR = os.path.join(TOOLS_DIR, "detecter", "detecter-donnees-en-dur")
DETECT_PY = os.path.join(DETECT_DIR, "detecter-donnees-en-dur.py")
VERROU_PY = os.path.join(TOOLS_DIR, "proteger", "proteger-verrou-marbre",
                         "proteger-verrou-marbre.py")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 4


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-068 (total %.1fs) ===" % total)
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
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def run(cmd, timeout=90):
    try:
        r = PROTECTIONS.lancer_protege(cmd, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, "ERREUR: %s" % str(e)[-80:]


def main():
    print("=== Garde-fou : regle anti-valeurs-magiques (marbre + secrets) ===")

    # 1. Regle gravee dans regles-general-global.md
    t0 = time.monotonic()
    texte = io.open(REGLES_GLOBAL, encoding="utf-8", errors="replace").read()
    a_regle = "Anti-valeurs-magiques" in texte
    a_constante = "CONSTANTE NOMMEE" in texte.upper()
    a_config = "config" in texte.lower()
    a_env = ".env" in texte
    verifier("1. REGLE D OR anti-valeurs-magiques gravee",
             a_regle, "regle absente de regles-general-global.md")
    verifier("1b. hierarchie : constante + config + .env",
             a_constante and a_config and a_env,
             "const=%s config=%s env=%s" % (a_constante, a_config, a_env))
    chrono_etape("1. regle gravee", t0)

    # 2. Zone dans le marbre (verrou --tous : 0 KO + zone listee)
    t0 = time.monotonic()
    code, out = run([PYTHON, VERROU_PY, "--tous", "--verbose"], timeout=60)
    zone_conforme = "regles-general-global" in out and "conforme" in out
    aucun_ko = "[KO]" not in out
    verifier("2. zone regles-general-global DANS LE MARBRE (verrou conforme)",
             code == 0 and zone_conforme and aucun_ko,
             out[-120:] if not (zone_conforme and aucun_ko) else "")
    chrono_etape("2. marbre", t0)

    # 3. detecter-donnees-en-dur v0.1.1 : version + SECRETS_EN_DUR
    t0 = time.monotonic()
    code, out = run([PYTHON, DETECT_PY, "--version"])
    verifier("3. detecter-donnees-en-dur --version v0.1.1",
             code == 0 and "v0.1.1" in out, out.strip()[-40:])
    # preuve reelle : fichier temporaire avec secret + lecture env + placeholder
    tmp = tempfile.mkdtemp(prefix="tmp-test068-")
    try:
        code_test = os.path.join(tmp, "code.py")
        with io.open(code_test, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# -*- coding: ascii -*-\n"
                     "import os\n"
                     "API_KEY = \"sk-1234567890abcdef\"\n"
                     "TOKEN = os.environ.get(\"API_TOKEN\", \"\")\n"
                     "DEMO_KEY = \"exemple\"\n")
        code, out = run([PYTHON, DETECT_PY, code_test], timeout=60)
        a_secret = "SECRETS_EN_DUR" in out and "API_KEY" in out
        a_env_ok = "TOKEN" not in out.split("SECRETS_EN_DUR")[-1].split("COMPTEURS")[0] or "TOKEN" not in out
        verifier("3b. SECRETS_EN_DUR detecte (API_KEY)",
                 a_secret, out[-120:] if not a_secret else "")
        verifier("3c. os.environ exclu (lecture legitime)",
                 "TOKEN = os.environ.get" not in out and "API_TOKEN" not in out,
                 "faux positif sur os.environ")
        verifier("3d. placeholder exclu (exemple)",
                 "DEMO_KEY" not in out, "faux positif sur placeholder")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    chrono_etape("3. secrets", t0)

    # 4. Normes ASCII + LF
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    for f in (DETECT_PY, os.path.abspath(__file__)):
        d = io.open(f, encoding="utf-8", errors="replace").read()
        na_total += sum(1 for c in d if ord(c) > 127)
        crlf_total += d.count("\r")
    verifier("4. ASCII strict : 0 non-ASCII (outil + test)", na_total == 0, "na=%d" % na_total)
    verifier("4b. LF pur : 0 CRLF (outil + test)", crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("4. normes", t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (regle au marbre + secrets detectes)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
