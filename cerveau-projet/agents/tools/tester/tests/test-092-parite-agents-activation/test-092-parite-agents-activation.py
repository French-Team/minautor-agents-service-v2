#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-092-parite-agents-activation.py
GARDE-FOU : parite entre la liste des agents d AGENTS.md et le dictionnaire
AGENTS de activer-agent-principal (py + sh). Tout agent declare doit etre
ACTIVABLE ; tout agent activable doit etre declare.

Contexte (lecons 2026-08-16 Argus v0.5.8 + 2026-08-18 Chiron v0.5.12) :
  - 2 agents ont ete crees (argus, chiron) mais OUBLIES dans le dictionnaire
    AGENTS du .py et/ou les case statements du .sh : ils etaient INACTIVABLES
    (activer-agent-principal repondait 'Agent inconnu').
  - AUCUN test ne verifiait cette parite -> l oubli n etait detecte qu a
    l activation reelle. Ce garde-fou institutionnalise la verification :
    chaque non-regression compare AGENTS.md (source de verite) au .py et au
    .sh, dans les DEUX sens (agent declare absent de l outil = KO ; agent
    de l outil absent d AGENTS.md = agent mort = KO).

Invariants verifies :
  1. Source de verite : AGENTS.md contient les liens [X](cerveau-projet/agents/N/)
  2. Parite .py : tout agent d AGENTS.md est dans le dictionnaire AGENTS
  3. Parite .sh : tout agent d AGENTS.md est dans les 3 fonctions
     (get_agent_role, get_agent_fiche, get_agent_corrections)
  4. Reciproque .py : aucun agent du dictionnaire hors AGENTS.md (pas d agent mort)
  5. Reciproque .sh : aucun agent des case statements hors AGENTS.md
  6. Parite py/sh : les ensembles .py et .sh sont identiques
  7. PREUVE NEGATIVE : copie du .py avec un agent retire -> la detection
     signale le manque (KO sur copie = le garde-fou fonctionne)
  8. Normes : ASCII 0 + LF pur (py, sh, md de l outil + ce test)

EXEMPTIONS (points 4/5) : stark (agent v2, fiche sous freelance/, non couvert
par l extraction v1 d AGENTS.md) et ferrari (agent CONFIDENTIEL, seul Cerberus
le connait, absent volontairement d AGENTS.md par decision utilisateur).

Usage:
  python3 test-092-parite-agents-activation.py
Tags: registre-traces, garde-fou-agent, anti-recurrence, garde-fou
"""
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

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
for _i, _arg in enumerate(sys.argv):
    if _arg == "--isoler" and _i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[_i + 1])
        except ValueError:
            pass
    if _arg == "--desactiver" and _i + 1 < len(sys.argv):
        for _p in sys.argv[_i + 1].split(","):
            try:
                DESACTIVES.append(int(_p))
            except ValueError:
                pass

ETAPES = []
T_START = time.monotonic()


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
    _total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)
    for _nom, _duree in ETAPES:
        print("  %-34s %6.2fs" % (_nom, _duree))


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


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
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


# Chemins des fichiers verifies
ACTIVER_DIR = os.path.join(TOOLS_DIR, "activer", "activer-agent-principal")
ACTIVER_PY = os.path.join(ACTIVER_DIR, "activer-agent-principal.py")
ACTIVER_SH = os.path.join(ACTIVER_DIR, "activer-agent-principal.sh")
ACTIVER_MD = os.path.join(ACTIVER_DIR, "activer-agent-principal.md")
AGENTS_MD = os.path.join(PROJECT_ROOT, "AGENTS.md")

# EXEMPTIONS (agents volontairement absents d AGENTS.md, points 4/5) :
#   - stark : agent v2 (freelance) -- present dans le dictionnaire pour activer
#     la session-freelance, mais sa fiche est sous cerveau-projet/freelance/,
#     non couverte par l extraction v1 d AGENTS.md (KO preexistant documente).
#   - ferrari : agent CONFIDENTIEL (decision utilisateur 2026-08-25) -- seul
#     Cerberus le connait, volontairement INVISIBLE des agents v2, donc absent
#     d AGENTS.md par conception (inactivable autrement).
EXEMPTIONS_MORTS = {"stark", "ferrari"}

# Liste attendue (source de verite = liens AGENTS.md). Ce n est PAS un pin
# dur : le test extrait les agents depuis AGENTS.md et compare aux outils.
# Cette liste sert de garde-fou minimal (si AGENTS.md etait vide ou corrompu,
# la source de verite ne doit pas rendre le test vert a tort).
AGENTS_ATTENDUS = [
    "argus", "athena", "atlas", "buffy", "cerberus", "chiron", "clio",
    "gardien", "hermes", "hygie", "janus", "minerve", "morpheus",
    "promethee", "themis", "vulcain",
]


def extraire_agents_md(chemin):
    """Agents declares dans AGENTS.md via les liens [X](cerveau-projet/agents/N/)."""
    agents = set()
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            texte = fh.read()
    except IOError:
        return agents
    for m in re.finditer(r"\[[A-Za-z]+\]\(cerveau-projet/agents/([a-z-]+)/", texte):
        agents.add(m.group(1))
    return agents


def extraire_agents_py(chemin):
    """Agents du dictionnaire AGENTS = { ... } du .py."""
    agents = set()
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            texte = fh.read()
    except IOError:
        return agents
    m = re.search(r"AGENTS\s*=\s*\{(.*?)\n\}", texte, re.DOTALL)
    if not m:
        return agents
    for k in re.findall(r'^\s*"([a-z-]+)":', m.group(1), re.MULTILINE):
        agents.add(k)
    return agents


def extraire_agents_sh(chemin):
    """Agents des case statements des 3 fonctions du .sh (role, fiche, corrections).
    Exclut les COMMANDES du .sh (sidentifier/activer/reactiver/sessions) qui
    sont aussi des case statements mais ne sont pas des agents."""
    agents = set()
    COMMANDES_SH = frozenset(["sidentifier", "activer", "reactiver", "sessions"])
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            texte = fh.read()
    except IOError:
        return agents
    for m in re.finditer(r'"([A-Za-z]+)"\|"[a-z-]+"\)', texte):
        nom = m.group(1).lower()
        if nom not in COMMANDES_SH:
            agents.add(nom)
    return agents


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== [test-092 PARITE AGENTS <-> ACTIVATION] ===")
    try:
        # 1. Source de verite : AGENTS.md + liste attendue
        if point_actif(1):
            t = time.monotonic()
            agents_md = extraire_agents_md(AGENTS_MD)
            manquants_attendu = sorted(set(AGENTS_ATTENDUS) - agents_md)
            verifier(
                "1. AGENTS.md contient les 16 agents attendus (source de verite)",
                len(manquants_attendu) == 0,
                "manquants=%s nb=%d" % (manquants_attendu, len(agents_md)))
            chrono_etape("1. source verite", t)

        # 2. Parite .py : tout agent d AGENTS.md est dans le dictionnaire
        if point_actif(2):
            t = time.monotonic()
            agents_md = extraire_agents_md(AGENTS_MD)
            agents_py = extraire_agents_py(ACTIVER_PY)
            manquants = sorted(agents_md - agents_py)
            verifier(
                "2. .py : tout agent d AGENTS.md est dans le dictionnaire AGENTS",
                len(manquants) == 0,
                "manquants=%s py=%d" % (manquants, len(agents_py)))
            chrono_etape("2. parite py", t)

        # 3. Parite .sh : tout agent d AGENTS.md est dans les case statements
        if point_actif(3):
            t = time.monotonic()
            agents_md = extraire_agents_md(AGENTS_MD)
            agents_sh = extraire_agents_sh(ACTIVER_SH)
            manquants = sorted(agents_md - agents_sh)
            verifier(
                "3. .sh : tout agent d AGENTS.md est dans les case statements",
                len(manquants) == 0,
                "manquants=%s sh=%d" % (manquants, len(agents_sh)))
            chrono_etape("3. parite sh", t)

        # 4. Reciproque .py : aucun agent mort (hors AGENTS.md)
        if point_actif(4):
            t = time.monotonic()
            agents_md = extraire_agents_md(AGENTS_MD)
            agents_py = extraire_agents_py(ACTIVER_PY)
            morts = sorted((agents_py - agents_md) - EXEMPTIONS_MORTS)
            verifier(
                "4. .py : aucun agent mort (dictionnaire hors AGENTS.md)",
                len(morts) == 0,
                "morts=%s" % morts)
            chrono_etape("4. reciproque py", t)

        # 5. Reciproque .sh : aucun agent mort
        if point_actif(5):
            t = time.monotonic()
            agents_md = extraire_agents_md(AGENTS_MD)
            agents_sh = extraire_agents_sh(ACTIVER_SH)
            morts = sorted((agents_sh - agents_md) - EXEMPTIONS_MORTS)
            verifier(
                "5. .sh : aucun agent mort (case statements hors AGENTS.md)",
                len(morts) == 0,
                "morts=%s" % morts)
            chrono_etape("5. reciproque sh", t)

        # 6. Parite py/sh : ensembles identiques
        if point_actif(6):
            t = time.monotonic()
            agents_py = extraire_agents_py(ACTIVER_PY)
            agents_sh = extraire_agents_sh(ACTIVER_SH)
            diff = sorted(agents_py ^ agents_sh)
            verifier(
                "6. parite py/sh : memes ensembles d agents",
                len(diff) == 0,
                "diff=%s py=%d sh=%d" % (diff, len(agents_py), len(agents_sh)))
            chrono_etape("6. parite py/sh", t)

        # 7. PREUVE NEGATIVE : copie du .py avec un agent retire -> detection KO
        if point_actif(7):
            t = time.monotonic()
            espace = tempfile.mkdtemp(prefix="tmp-test092-")
            try:
                copie = os.path.join(espace, "copie.py")
                with io.open(ACTIVER_PY, encoding="utf-8", errors="replace") as fh:
                    texte = fh.read()
                # retire l entree 'atlas' du dictionnaire (preuve : la
                # detection doit le reperer comme manquant)
                texte_sans_atlas = re.sub(
                    r'\s*"atlas": \(.*?\),\n', "", texte, count=1,
                    flags=re.MULTILINE | re.DOTALL)
                if texte_sans_atlas == texte:
                    verifier("7. PREUVE NEGATIVE : retrait atlas reussi (fiabilite du test)",
                             False, "motif atlas introuvable dans le .py")
                else:
                    with io.open(copie, "w", encoding="utf-8", newline="\n") as fh:
                        fh.write(texte_sans_atlas)
                    agents_copie = extraire_agents_py(copie)
                    detecte = "atlas" not in agents_copie
                    agents_md = extraire_agents_md(AGENTS_MD)
                    manquants = sorted(agents_md - agents_copie)
                    # La detection parite detecte-t-elle le manque ?
                    ok_detect = detecte and "atlas" in manquants
                    verifier(
                        "7. PREUVE NEGATIVE : agent retire du .py est DETECTE manquant",
                        ok_detect,
                        "atlas_dans_copie=%s manquants=%s" % (
                            "atlas" in agents_copie, manquants))
            finally:
                shutil.rmtree(espace, ignore_errors=True)
            chrono_etape("7. preuve negative", t)

        # 8. Normes : ASCII 0 + LF pur (outil + ce test)
        if point_actif(8):
            t = time.monotonic()
            fichiers = [ACTIVER_PY, ACTIVER_SH, ACTIVER_MD,
                        os.path.abspath(__file__)]
            total_non_ascii = sum(ascii_count(f) for f in fichiers)
            verifier("8. ASCII strict : 0 non-ASCII (outil + test)",
                     total_non_ascii == 0, "total=%d" % total_non_ascii)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("8b. LF pur : 0 CRLF (outil + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("8. normes", t)

    except PROTECTIONS.ArretProtection as _e:
        print("  [STOP] protection declenchee : %s" % _e)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
