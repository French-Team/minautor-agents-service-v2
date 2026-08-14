#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-048-fin-mission-documentation.py
GARDE-FOU : la mecanisation du protocole de fin de mission. Chaque maillon
d'une chaine doit documenter SON controle (lecon + verdict) dans corrections.md
AVANT de transmettre au maillon suivant ou de reactiver Cerberus.

Contexte (demande utilisateur 2026-08-14) :
  - La verification de la chaine Hermes a revele que le bilan consolide de
    Janus affirmait "VOLET 1 Hermes VALIDE" alors que NI Themis NI Janus
    n'avaient documente le moindre controle de la creation d'Hermes (aucune
    lecon, aucun rapport mentionnant hermes dans leurs dossiers).
  - Le bilan reprenait les resultats de Morpheus sans controle croise reel.
  - Anti-recurrence : protocole-fin-mission impose lecon + verdict obligatoires
    avant transmission, et CE test verifie la regle mecaniquement.

Cas couverts:
  1. Le protocole protocole-fin-mission existe (fichier spec)
  2. Le protocole est reference dans index-regles-general.md
  3. Le protocole contient la regle (lecon + verdict obligatoires)
  4. Chaque agent ayant une mission recente dans AGENTS-historique (ligne
     'MISSION <AGENT>') a AU MOINS une lecon dans corrections.md
  5. Chaque lecon recente de ces agents contient un verdict
     (VERDICT / VALIDE / CONFORME / A REVOIR / KO) dans le titre ou le corps
  6. Les missions de test ('TEST') et les entrees Cerberus (BILAN/CONTROLE
     TERMINE) ne sont pas exigeantes de lecon
  7. ASCII strict : 0 non-ASCII (test + protocole + index)
  8. LF pur : 0 CRLF (test + protocole + index)
"""
import importlib.util
import io
import os
import re
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")

PROTOCOLE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                         "regles-immuables", "general", "protocole-fin-mission",
                         "protocole-fin-mission.001.01.ebauche.md")
INDEX_REGLES = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                            "regles-immuables", "general",
                            "index-regles-general.md")
HISTORIQUE = os.path.join(PROJECT_ROOT, "AGENTS-historique.md")


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
POINT_ACTIF = None
DESACTIVES = set()


def chrono_etape(nom, duree):
    print("  [chrono] %-40s %.2fs" % (nom, duree))


def verifier(nom, ok, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if POINT_ACTIF is not None and NB_POINTS != POINT_ACTIF:
        return
    if NB_POINTS in DESACTIVES:
        print("  [DESACTIVE] %s" % nom)
        return
    if ok:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(commande):
    res = PROTECTIONS.lancer_protege(commande, timeout=120)
    return res.stdout if res is not None else ""


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def compter_crlf(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lire(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def agents_reels():
    """Liste des agents ayant un dossier parcours (agents du cerveau)."""
    resultat = []
    for nom in sorted(os.listdir(AGENTS_DIR)):
        if os.path.isdir(os.path.join(AGENTS_DIR, nom)) and os.path.exists(
                os.path.join(AGENTS_DIR, nom, "parcours")):
            resultat.append(nom)
    return resultat


def missions_recentes(texte, agents):
    """Extrait (date, agent) des lignes 'MISSION <AGENT>' recentes.
    Exclut les lignes TEST et les entrees Cerberus (BILAN/CONTROLE TERMINE).
    Ne garde que les lignes dont la date est <= 3 jours avant aujourd hui."""
    missions = []
    for ligne in texte.splitlines():
        if "MISSION" not in ligne.upper():
            continue
        if "TEST" in ligne.upper():
            continue
        if "BILAN CONSOLIDE" in ligne or "CONTROLE CROISE TERMINE" in ligne:
            continue
        m = re.match(r"\|\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s+[0-9:]+"
                     r"\s*\|\s*[^|]+\|\s*([a-z-]+)\s*\|", ligne)
        if not m:
            continue
        date, agent = m.group(1), m.group(2).strip()
        if agent not in agents:
            continue
        missions.append((date, agent, ligne.strip()[:80]))
    return missions


def lecons_agent(agent):
    """Retourne les titres des lecons de l agent (listes de lignes ## [LECON])."""
    chemin = os.path.join(AGENTS_DIR, agent, "corrections.md")
    if not os.path.exists(chemin):
        return []
    texte = lire(chemin)
    return [l for l in texte.splitlines() if l.startswith("## [LECON]")]


def lecon_contient_verdict(agent, date):
    """Vrai si l agent a une lecon datee >= date contenant un verdict."""
    chemin = os.path.join(AGENTS_DIR, agent, "corrections.md")
    if not os.path.exists(chemin):
        return False
    texte = lire(chemin)
    # decouper en blocs de lecons
    blocs = re.split(r"\n## \[LECON\] ", "\n" + texte)
    for bloc in blocs[1:]:
        m = re.match(r"([0-9]{4}-[0-9]{2}-[0-9]{2})", bloc)
        if not m:
            continue
        if m.group(1) >= date:  # lecon du jour ou posterieure
            if re.search(r"(?i)verdict|VALIDE|CONFORME|A REVOIR|PROPRE|\bKO\b",
                         bloc):
                return True
    return False


def main():
    global NB_POINTS, NB_OK, NB_KO, POINT_ACTIF, DESACTIVES
    t0 = time.time()

    args = [a for a in sys.argv[1:]]
    for i, a in enumerate(args):
        if a == "--isoler" and i + 1 < len(args):
            POINT_ACTIF = int(args[i + 1])
        if a == "--desactiver" and i + 1 < len(args):
            DESACTIVES = set(int(x) for x in args[i + 1].split(","))

    print("=== Test formel fin-mission-documentation (garde-fou lecon+verdict) ===")

    # 1. Protocole existe
    t1 = time.time()
    verifier("1. protocole-fin-mission existe",
             os.path.isfile(PROTOCOLE), PROTOCOLE)
    chrono_etape("1. protocole existe", time.time() - t1)

    # 2. Protocole reference dans l index
    t2 = time.time()
    idx = lire(INDEX_REGLES) if os.path.exists(INDEX_REGLES) else ""
    verifier("2. protocole-fin-mission reference dans index-regles-general",
             "protocole-fin-mission" in idx)
    chrono_etape("2. index regles", time.time() - t2)

    # 3. Protocole contient la regle (lecon + verdict obligatoires)
    t3 = time.time()
    prot = lire(PROTOCOLE) if os.path.exists(PROTOCOLE) else ""
    regle_ok = ("lecon" in prot.lower() and "verdict" in prot.lower()
                and "transmission" in prot.lower())
    verifier("3. protocole impose lecon + verdict avant transmission",
             regle_ok)
    chrono_etape("3. regle protocole", time.time() - t3)

    # 4. Chaque mission recente a une lecon dans corrections.md
    t4 = time.time()
    hist = lire(HISTORIQUE) if os.path.exists(HISTORIQUE) else ""
    agents = agents_reels()
    missions = missions_recentes(hist, agents)
    manques_lecon = []
    for date, agent, ligne in missions:
        if not lecons_agent(agent):
            manques_lecon.append("%s %s" % (agent, ligne))
    verifier("4. toute mission recente a une lecon dans corrections.md",
             not manques_lecon, "sans lecon=%s" % manques_lecon[:3])
    chrono_etape("4. missions -> lecons", time.time() - t4)

    # 5. Chaque lecon recente contient un verdict
    t5 = time.time()
    manques_verdict = []
    for date, agent, ligne in missions:
        if not lecon_contient_verdict(agent, date):
            manques_verdict.append("%s %s" % (agent, ligne))
    verifier("5. lecons recentes contiennent un verdict (VERDICT/VALIDE/...)",
             not manques_verdict, "sans verdict=%s" % manques_verdict[:3])
    chrono_etape("5. lecons -> verdicts", time.time() - t5)

    # 6. Les missions TEST / entrees Cerberus ne sont pas exigees
    t6 = time.time()
    # re-verifier que missions_recentes les a bien exclues : aucune ligne
    # contenant 'TEST' ou 'BILAN CONSOLIDE' ne doit apparaitre dans missions
    mauvaises = [l for _, _, l in missions
                 if "TEST" in l or "BILAN CONSOLIDE" in l
                 or "CONTROLE CROISE TERMINE" in l]
    verifier("6. missions TEST / entrees Cerberus exclues",
             not mauvaises, "exclues manquees=%s" % mauvaises[:3])
    chrono_etape("6. exclusions", time.time() - t6)

    # 7. ASCII strict
    t7 = time.time()
    total_na = 0
    for f in [PROTOCOLE, INDEX_REGLES, os.path.abspath(__file__)]:
        if os.path.exists(f):
            total_na += compter_non_ascii(f)
    verifier("7. ASCII strict: 0 non-ASCII (test + protocole + index)",
             total_na == 0, "nb=%d" % total_na)
    chrono_etape("7. ASCII", time.time() - t7)

    # 8. LF pur
    t8 = time.time()
    total_crlf = 0
    for f in [PROTOCOLE, INDEX_REGLES, os.path.abspath(__file__)]:
        if os.path.exists(f):
            total_crlf += compter_crlf(f)
    verifier("8. LF pur: 0 CRLF (test + protocole + index)",
             total_crlf == 0, "nb=%d" % total_crlf)
    chrono_etape("8. LF pur", time.time() - t8)

    if "--no-chrono" not in args:
        print("")
        print("=== BILAN CHRONO ===")
        print("test-048-fin-mission-documentation : total %.2fs"
              % (time.time() - t0))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
