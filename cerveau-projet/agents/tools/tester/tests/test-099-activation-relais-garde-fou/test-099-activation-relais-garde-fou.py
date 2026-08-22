#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-099-activation-relais-garde-fou.py

Test du garde-fou v0.5.22 de activer-agent-principal : activation et relais
des agents (decision utilisateur Option A 2026-08-21, retour Pattern 8 :
l agent suivant active l agent suivant pour continuer la boucle).

Comportements verrouilles (v0.5.22) :
  - Activation depuis Cerberus (aucun agent actif) : autorisee, SANS
    avertissement (cas nominal).
  - Auto-reactivation (meme agent encore actif) : AVERTISSEMENT
    'agent oublie' + AUTORISEE (rc=0).
  - Relais de chaine (agent DIFFERENT encore actif, cible != cerberus) :
    AUTORISE SANS avertissement (rc=0) -- Pattern 8 (v0.5.28).
  - Reactivation de Cerberus : TOUJOURS autorisee (rc=0), sans blocage.
  - --forcer : AVERTISSEMENT 'activation forcee' + autorisee (rc=0),
    option conservee pour compatibilite.
  - Chaine complete bout-en-bout : Cerberus -> buffy -> themis -> janus
    -> Cerberus, tous rc=0 (les fins 'FIN - Activer X' des cartes peuvent
    s executer sans passer par Cerberus).

Contre-exemple (ancien comportement v0.5.19, a ne JAMAIS reintroduire) :
  - Plus AUCUN cas BLOQUER pour une activation directe (agent different).
    Si le blocage revient, la chaine bout-en-bout des cartes casse.

Proprietaire : Morpheus (testeur dedie)
Version : 0.2.1
Tags: securite, blocage, garde-fou, anti-recurrence, agents
"""
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

ACTIVER = os.path.join(TOOLS_DIR, "activer", "activer-agent-principal",
                       "activer-agent-principal.py")
AGENT_MD_TEMPLATE = os.path.join(PROJECT_ROOT, "AGENTS.md")
HISTORIQUE_TEMPLATE = os.path.join(PROJECT_ROOT, "AGENTS-historique.md")
CLASSEUR_TEMPLATE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "classeur-variables", "stockage",
                                 "variables-actuelles.md")

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


def run(cmd, timeout=60):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout)


def reinitialiser_cerberus_actif(agents_file):
    """Reinitialiser la copie de AGENTS.md : session-llm-1 -> Cerberus actif.

    La copie du template porte l ETAT REEL (l agent actif de la session en
    cours). Pour tester les cas nominaux (activation depuis Cerberus), on
    remet le champ **Nom Agent** du bloc session-llm-1 a Cerberus.
    """
    with io.open(agents_file, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()
    pattern = r"(### Session : session-llm-1\n.*?\| \*\*Nom Agent\*\* \| )([^|]+)( \|)"
    nouveau, n = re.subn(pattern, r"\1cerberus\3", contenu, count=1,
                         flags=re.DOTALL)
    if n == 0:
        return False
    with io.open(agents_file, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(nouveau)
    return True


def creer_environnement_test():
    """Creer un environnement de test isole (Cerberus actif au depart)."""
    tmpdir = tempfile.mkdtemp(prefix="test-099-")
    agents_file = os.path.join(tmpdir, "AGENTS.md")
    historique_file = os.path.join(tmpdir, "AGENTS-historique.md")
    classeur_file = os.path.join(tmpdir, "variables-actuelles.md")

    shutil.copy2(AGENT_MD_TEMPLATE, agents_file)
    shutil.copy2(HISTORIQUE_TEMPLATE, historique_file)
    shutil.copy2(CLASSEUR_TEMPLATE, classeur_file)

    if not reinitialiser_cerberus_actif(agents_file):
        print("WARNING : reinitialisation Cerberus actif impossible")

    return tmpdir, agents_file, historique_file, classeur_file


def nettoyer_environnement(tmpdir):
    """Nettoyer l'environnement de test."""
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)


def executer_activer(agents_file, historique_file, classeur_file, args):
    """Executer activer-agent-principal avec un environnement isole."""
    env = os.environ.copy()
    env["AGENTS_FILE"] = agents_file
    env["AGENTS_HISTORIQUE"] = historique_file
    env["CLASSEUR_STOCKAGE"] = classeur_file
    cmd = [PYTHON, ACTIVER] + args
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      env=env, timeout=30)


def point_1_activation_cerberus():
    """1. Activation depuis Cerberus - autorisee sans avertissement."""
    tmpdir, agents_file, historique_file, classeur_file = \
        creer_environnement_test()
    try:
        r = executer_activer(agents_file, historique_file, classeur_file,
                             ["activer", "session-llm-1", "atlas",
                              "Test etape 1"])
        ok = (r.returncode == 0 and "AVERTISSEMENT GARDE-FOU" not in r.stdout
              and "atlas active avec succes" in r.stdout)
        verifier("1. activation depuis Cerberus sans avertissement", ok,
                 "rc=%d %s" % (r.returncode, r.stdout[:150]))
    finally:
        nettoyer_environnement(tmpdir)


def point_2_auto_reactivation():
    """2. Auto-reactivation (meme agent) - avertissement + autorisee."""
    tmpdir, agents_file, historique_file, classeur_file = \
        creer_environnement_test()
    try:
        r1 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "atlas",
                               "Test etape 1"])
        r2 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "atlas",
                               "Test etape 2"])
        ok = (r1.returncode == 0 and r2.returncode == 0
              and "AVERTISSEMENT GARDE-FOU (agent oublie)" in r2.stdout)
        verifier("2. auto-reactivation : avertissement + autorisee", ok,
                 "rc2=%d %s" % (r2.returncode, r2.stdout[:150]))
    finally:
        nettoyer_environnement(tmpdir)


def point_3_relais_chaine():
    """3. Relais de chaine (agent different) - autorise (Pattern 8)."""
    tmpdir, agents_file, historique_file, classeur_file = \
        creer_environnement_test()
    try:
        r1 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "atlas",
                               "Test etape 1"])
        r2 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "themis",
                               "Test etape 2"])
        ok = (r1.returncode == 0 and r2.returncode == 0)
        verifier("3. relais de chaine : autorise SANS avertissement (Pattern 8, v0.5.28)",
                 ok, "rc2=%d %s" % (r2.returncode, r2.stdout[:200]))
    finally:
        nettoyer_environnement(tmpdir)


def point_4_reactivation_cerberus():
    """4. Reactivation de Cerberus toujours autorisee."""
    tmpdir, agents_file, historique_file, classeur_file = \
        creer_environnement_test()
    try:
        r1 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "atlas", "Test"])
        r2 = executer_activer(agents_file, historique_file, classeur_file,
                              ["reactiver", "session-llm-1", "Test fin",
                               "atlas"])
        ok = (r1.returncode == 0 and r2.returncode == 0
              and "Cerberus reactive avec succes" in r2.stdout)
        verifier("4. reactivation Cerberus toujours autorisee", ok,
                 "rc2=%d %s" % (r2.returncode, r2.stdout[:150]))
    finally:
        nettoyer_environnement(tmpdir)


def point_5_forcer():
    """5. --forcer conserve (avertissement forcee, compatibilite)."""
    tmpdir, agents_file, historique_file, classeur_file = \
        creer_environnement_test()
    try:
        r1 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "atlas",
                               "Test etape 1"])
        r2 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "themis",
                               "Test forcee", "--forcer"])
        ok = (r1.returncode == 0 and r2.returncode == 0
              and "AVERTISSEMENT GARDE-FOU (activation forcee)" in r2.stdout)
        verifier("5. --forcer : avertissement + autorisee (compatibilite)",
                 ok, "rc2=%d %s" % (r2.returncode, r2.stdout[:150]))
    finally:
        nettoyer_environnement(tmpdir)


def point_6_chaine_complete():
    """6. Chaine complete bout-en-bout (Pattern 8)."""
    tmpdir, agents_file, historique_file, classeur_file = \
        creer_environnement_test()
    try:
        r1 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "buffy",
                               "Test chaine 1"])
        r2 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "themis",
                               "Test chaine 2"])
        r3 = executer_activer(agents_file, historique_file, classeur_file,
                              ["activer", "session-llm-1", "janus",
                               "Test chaine 3"])
        r4 = executer_activer(agents_file, historique_file, classeur_file,
                              ["reactiver", "session-llm-1",
                               "Test chaine fin", "janus"])
        ok = (r1.returncode == 0 and r2.returncode == 0
              and r3.returncode == 0 and r4.returncode == 0
              and "Cerberus reactive avec succes" in r4.stdout)
        verifier("6. chaine complete bout-en-bout : tous rc=0", ok,
                 "rc=%d/%d/%d/%d" % (r1.returncode, r2.returncode,
                                     r3.returncode, r4.returncode))
    finally:
        nettoyer_environnement(tmpdir)


def main():
    print("=== test-099 : Activation et relais des agents "
          "(garde-fou v0.5.22) ===")

    points = [
        ("1. activation depuis Cerberus", point_1_activation_cerberus),
        ("2. auto-reactivation", point_2_auto_reactivation),
        ("3. relais de chaine", point_3_relais_chaine),
        ("4. reactivation Cerberus", point_4_reactivation_cerberus),
        ("5. --forcer", point_5_forcer),
        ("6. chaine complete", point_6_chaine_complete),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        chrono_etape(nom, t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
