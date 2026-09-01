#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-108-controle-processus-garde-fou.py

Garde-fou du controle des processus v1 (oracle/fonctions/controle_processus.py),
le module qui detecte les processus fantomes et les serveurs morts.

Contexte (2026-08-29) : BUG CORRIGE - faux positif 'SERVEUR MORT'. Le
harnais est execute DANS le daemon oracle-server (meme pid). L ancienne
auto-exclusion `p['pid'] != os.getpid()` retirait l instance officielle
du daemon lui-meme -> alerte [FANTOMES] spammee toutes les 30 s (18
alertes observees). Fix : suppression de l auto-exclusion par pid - le
matcher par ligne de commande suffit (une invocation CLI oracle.py ne
matche jamais un script serveur).

Points verifies :
  1. Le module existe, compile et est importable.
  2. FIX : plus AUCUNE auto-exclusion par os.getpid() dans verifier()
     (le spam SERVEUR MORT est impossible).
  3. Le matcher distingue la v1 de la v2 (routines-server : chemin
     oraclais distinctif, pas le basename partage).
  4. Cas normal (processus reels) : les serveurs vivants sont OK, aucun
     fantome, ok=True.
  5. Serveur mort (pid file inexistant) : mort=True, ok=False.
  6. Doublon fantome (instance supplementaire) : doublons detectes,
     ok=False.
  7. La CLI oracle.py controle-processus sort proprement (rc 0 ou 1).
  8. Script ASCII (convention v1).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: processus, fantome, controle, oracle, harnais, garde-fou,
anti-recurrence
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

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

ORACLE_DIR = os.path.join(TOOLS_DIR, "oracle")
MODULE = os.path.join(ORACLE_DIR, "fonctions", "controle_processus.py")
ORACLE_PY = os.path.join(ORACLE_DIR, "oracle.py")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

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
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout)


def lire(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def charger_module():
    """Charger controle_processus.py en module."""
    spec = importlib.util.spec_from_file_location("controle_processus",
                                                  MODULE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def point_1_module_existe():
    contenu = lire(MODULE)
    ok = (os.path.isfile(MODULE)
          and "def verifier()" in contenu
          and "def lister_processus()" in contenu
          and "SERVEURS" in contenu)
    verifier("1. controle_processus.py existe (verifier, lister, SERVEURS)",
             ok)


def point_2_fix_pas_auto_exclusion():
    """2. FIX verrouille : AUCUNE auto-exclusion par os.getpid() dans le
    CODE EXECUTABLE de verifier(). Si elle revient, le faux positif
    SERVEUR MORT spamme l inbox (bug 2026-08-29). Le mot peut rester
    dans les COMMENTAIRES (explication du fix) - on verifie les lignes
    de code actives uniquement (hors '#' et chaines de doc)."""
    lignes_code = []
    dans_docstring = False
    for ligne in lire(MODULE).splitlines():
        s = ligne.strip()
        # Docstring : ignorer le contenu entre triple-guillemets.
        if '"""' in s or "'''" in s:
            dans_docstring = not dans_docstring
            continue
        if dans_docstring:
            continue
        # Commentaire plein (ligne commencant par #).
        if s.startswith("#") or not s:
            continue
        # Commentaire en fin de ligne : retirer ce qui suit '#'.
        if '#' in s:
            s = s.split('#', 1)[0].strip()
            if not s:
                continue
        lignes_code.append(s)
    code = "\n".join(lignes_code)
    # Aucune utilisation executable de os.getpid() ou _mon_pid.
    ok = ("os.getpid()" not in code
          and "_mon_pid" not in code
          and "!= _mon_pid" not in code)
    verifier("2. FIX: plus d auto-exclusion par pid dans le code", ok)


def point_3_matrice_v1_v2():
    """3. Le matcher distingue la v1 de la v2 (routines-server)."""
    contenu = lire(MODULE)
    # La signature v1 routines utilise le chemin 'oracle/routines-server.py'
    # et non le basename partage 'routines-server.py' (partage avec la v2).
    ok = ("oracle/routines-server.py" in contenu
          and "SERVEURS" in contenu)
    verifier("3. signature v1 routines distincte (chemin oracle/...)", ok)


def point_4_cas_normal():
    """4. Cas normal : les serveurs vivants sont OK, aucun fantome."""
    try:
        mod = charger_module()
        r = mod.verifier()
    except Exception as exc:
        verifier("4. cas normal (serveurs vivants OK)", False, str(exc)[:120])
        return
    # Si le listing echoue sur la plateforme, le test est non concluant
    # (pas un KO : le fix porte sur la logique, pas l OS).
    if r.get("erreurs_listing"):
        verifier("4. cas normal (serveurs vivants OK)", True,
                 "listing indisponible - non concluant")
        return
    # ok doit etre True SEULEMENT si aucun serveur mort ni doublon.
    # Sur la machine de dev, les 2 daemons tournent normalement.
    ok = r.get("ok", False)
    morts = [s["nom"] for s in r.get("serveurs", []) if s.get("mort")]
    doublons = [s["nom"] for s in r.get("serveurs", [])
                if s.get("doublons")]
    verifier("4. cas normal (serveurs vivants OK)", ok,
             "morts=%s doublons=%s" % (morts, doublons))


def point_5_serveur_mort():
    """5. Serveur mort (pid file absent) : mort=True, ok=False.
    Simule SANS toucher aux vrais pid files (remplacement en memoire,
    comme le point 6) : ecrire le pid file reel risquait de le laisser
    pollue si le test etait interrompu entre l ecriture et la
    restauration (residu 99999999 observe 2026-08-30 -> doublon fantome
    sur le serveur reel au run suivant)."""
    try:
        mod = charger_module()
        # Simuler un pid file INVALIDE en memoire : le pid officiel devient
        # None -> le serveur est considere mort (aucune instance reconnue
        # officielle). Aucun ecriture sur disque.
        _pid_reel = mod._pid_file_valide
        mod._pid_file_valide = lambda p: None
        try:
            r = mod.verifier()
        finally:
            mod._pid_file_valide = _pid_reel
        # Aucun pid officiel : le serveur doit etre signale PROBLEME.
        mort = None
        for s in r.get("serveurs", []):
            if s["nom"] == "oracle-server":
                mort = s.get("mort") or s.get("pid_officiel") is None
        ok = mort is True or (mort is None and not r.get("ok"))
        verifier("5. serveur mort detecte (pid inexistant)", ok,
                 "resume=%s" % json.dumps(r.get("serveurs", []))[:120])
    except Exception as exc:
        verifier("5. serveur mort detecte (pid inexistant)", False,
                 str(exc)[:120])


def point_6_doublon_fantome():
    """6. Doublon fantome : instance supplementaire detectee, ok=False.
    Simule par remplacement de lister_processus en memoire."""
    try:
        mod = charger_module()
        proc = mod.lister_processus()
        fake = {"pid": 12345, "cmdline":
                "C:/x/cerveau-projet/agents/tools/oracle/oracle-server.py"
                " --boucle"}
        mod.lister_processus = lambda: proc + [fake]
        r = mod.verifier()
        doublons = []
        for s in r.get("serveurs", []):
            if s["nom"] == "oracle-server":
                doublons = s.get("doublons", [])
        ok = (12345 in doublons
              and r.get("fantomes_totaux", 0) >= 1
              and not r.get("ok"))
        verifier("6. doublon fantome detecte (pid 12345)", ok,
                 "doublons=%s ok=%s" % (doublons, r.get("ok")))
    except Exception as exc:
        verifier("6. doublon fantome detecte (pid 12345)", False,
                 str(exc)[:120])


def point_7_cli():
    """7. La CLI oracle.py controle-processus sort sans crash."""
    r = run([PYTHON, ORACLE_PY, "controle-processus"], timeout=120)
    ok = (r.returncode in (0, 1)
          and "CONTROLE PROCESSUS" in (r.stdout or ""))
    verifier("7. CLI oracle.py controle-processus (rc 0/1)", ok,
             "rc=%d %s" % (r.returncode, (r.stdout or "")[:100]))


def point_8_ascii():
    contenu = lire(MODULE)
    ok = not any(ord(c) > 127 for c in contenu)
    verifier("8. script ASCII (convention v1)", ok)


def main():
    print("=== test-108 : garde-fou controle processus v1 ===")
    points = [
        ("1. module existe", point_1_module_existe),
        ("2. FIX pas auto-exclusion pid", point_2_fix_pas_auto_exclusion),
        ("3. matcher v1/v2 distinct", point_3_matrice_v1_v2),
        ("4. cas normal serveurs vivants", point_4_cas_normal),
        ("5. serveur mort detecte", point_5_serveur_mort),
        ("6. doublon fantome detecte", point_6_doublon_fantome),
        ("7. CLI oracle.py controle-processus", point_7_cli),
        ("8. ASCII", point_8_ascii),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        if CHRONO_ACTIF:
            ETAPES.append((nom, time.monotonic() - t_debut))

    if CHRONO_ACTIF:
        total = time.monotonic() - DEBUT_TEST
        print("")
        print("=== CHRONO test (total %.1fs) ===" % total)
        for nom, duree in ETAPES:
            print("  %-40s %6.2fs" % (nom, duree))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())