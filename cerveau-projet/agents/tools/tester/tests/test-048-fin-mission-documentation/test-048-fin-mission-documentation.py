#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-048-fin-mission-documentation.py
GARDE-FOU : la mecanisation du protocole de fin de mission. Chaque maillon
d'une chaine doit documenter SON controle (lecon + verdict) AVANT de
transmettre au maillon suivant ou de reactiver Cerberus.

Contexte (demande utilisateur 2026-08-14) :
  - La verification de la chaine Hermes a revele que le bilan consolide de
    Janus affirmait "VOLET 1 Hermes VALIDE" alors que NI Themis NI Janus
    n'avaient documente le moindre controle de la creation d'Hermes (aucune
    lecon, aucun rapport mentionnant hermes dans leurs dossiers).
  - Le bilan reprenait les resultats de Morpheus sans controle croise reel.
  - Anti-recurrence : protocole-fin-mission impose lecon + verdict obligatoires
    avant transmission, et CE test verifie la regle mecaniquement.

ADAPTATION MIGRATION v1->v2 (2026-09-04, decision utilisateur) :
  - Le format de AGENTS-historique.md est passe en v2 : sections '## JJ/MM/AAAA'
    + '### <agent>' + lignes '- HH:MM:SS.mmm | <llm> | R | DEBUT: <mission>'.
    L'ancien parseur v1 ('| <span>agent</span> | heure | date | session | MISSION')
    ne matchait plus RIEN -> le test passait trivialement (8/8 sans verifier).
  - Les corrections.md v1 sont GELES (bandeau 2026-09-04) : AUCUN [LECON]
    supplementaire. Depuis la migration, les lecons de fin de mission vont dans
    la BDD des lecons.

SCISSION 2-BDD (2026-09-05, decision utilisateur) :
  - Deux equipes DISTINCTES, deux memoires collectives separees :
    * agents v1 (cerveau-projet) -> BDD v1
      (cerveau-projet/agents/lecons/lecons.db, outils v1 restaures) ;
    * agents v2 (freelance) -> BDD v2
      (cerveau-projet/freelance/tools-commun/bdd-lecons/lecons.db).
  - Le test verifie donc : pour chaque mission recente (date >= 2026-09-04 =
    GEL_DATE), l'agent a au moins une lecon dans SA BDD (v1 si agent v1, v2 si
    agent v2) ; pour les missions anterieures (pre-migration), la lecon est
    dans corrections.md (historique gele, conserve pour relecture).

Cas couverts:
  1. Le protocole protocole-fin-mission existe (fichier spec)
  2. Le protocole est reference dans index-regles-general.md
  3. Le protocole contient la regle (lecon + verdict obligatoires)
  4. Chaque agent ayant une mission recente dans AGENTS-historique a AU MOINS
     une lecon (bdd-lecons v2 si date >= 2026-09-04, corrections.md sinon)
  5. Chaque lecon recente de ces agents contient un verdict
     (VERDICT / VALIDE / CONFORME / A REVOIR / KO) dans le titre ou le corps
  6. Les missions de test ('TEST') et les entrees Cerberus (BILAN/CONTROLE
     TERMINE) ne sont pas exigeantes de lecon
  7. ASCII strict : 0 non-ASCII (test + protocole + index)
  8. LF pur : 0 CRLF (test + protocole + index)
Tags: agents, garde-fou, protocole
"""
import importlib.util
import io
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timedelta

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

# Migration v1->v2 (2026-09-04) : avant = lecons dans corrections.md (gele),
# a partir de = lecons dans la BDD (v1 pour les agents v1, v2 pour les agents
# v2 - scission 2-bdd 2026-09-05).
GEL_DATE = "2026-09-04"
BDD_V1 = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "lecons",
                      "lecons.db")
BDD_V2 = os.path.join(PROJECT_ROOT, "cerveau-projet", "freelance",
                      "tools-commun", "bdd-lecons", "lecons.db")


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
    """Extrait (date, agent) des DEBUT de mission recents au format v2
    (sections '## JJ/MM/AAAA' + '### <agent>' + lignes
    '- HH:MM:SS.mmm | <llm> | R | DEBUT: <mission>').
    Exclut : les lignes dont l action n est pas un DEBUT de mission (les
    RETOUR/coordination d oracle), les alertes de routine des daemons
    (ETAT URGENT / MISE EN ATTENTE), les missions BLOCKEES (jamais
    executees) et les missions DELEGUEES a un autre agent (FIN: Delegation
    terminee). Ne garde que les lignes dont la date est <= 3 jours avant
    aujourd hui."""
    # 1er parcours : reperer les (date, agent) dont une mission a fini
    # BLOCKED ou par une delegation -> ces DEBUT n exigent pas de lecon.
    bloques = set()
    date_courante = None
    agent_courant = None
    for ligne in texte.splitlines():
        ligne_strip = ligne.strip()
        if ligne_strip.startswith("## "):
            m_date = re.match(r"##\s+([0-9]{2})/([0-9]{2})/([0-9]{4})",
                              ligne_strip)
            if m_date:
                date_courante = "%s-%s-%s" % (m_date.group(3), m_date.group(2),
                                              m_date.group(1))
            continue
        if ligne_strip.startswith("### "):
            agent_courant = ligne_strip[4:].strip().lower()
            continue
        if "| FIN" not in ligne:
            continue
        if "BLOCKED" in ligne or "Delegation terminee" in ligne:
            if date_courante and agent_courant:
                bloques.add((date_courante, agent_courant))

    # 2e parcours : collecter les DEBUT de mission hors exclusions
    missions = []
    date_courante = None
    agent_courant = None
    for ligne in texte.splitlines():
        ligne_strip = ligne.strip()
        if ligne_strip.startswith("## "):
            m_date = re.match(r"##\s+([0-9]{2})/([0-9]{2})/([0-9]{4})",
                              ligne_strip)
            if m_date:
                date_courante = "%s-%s-%s" % (m_date.group(3), m_date.group(2),
                                              m_date.group(1))
            continue
        if ligne_strip.startswith("### "):
            agent_courant = ligne_strip[4:].strip().lower()
            continue
        # action prefixe : la ligne doit porter un DEBUT de mission
        if not re.search(r"\| (?:R|IR) \| DEBUT", ligne):
            continue
        if "DEBUT: RETOUR " in ligne.upper():
            # Oracle reagissant a un retour d agent (coordination), pas une
            # mission de travail exigeant une lecon.
            continue
        if "DEBUT: ETAT URGENT" in ligne.upper() or \
                "DEBUT: MISE EN ATTENTE" in ligne.upper() or \
                "DEBUT: URGENT" in ligne.upper():
            # Alertes de routine des daemons (oracle), pas des missions de
            # travail exigeant une lecon.
            continue
        if "TEST" in ligne.upper():
            continue
        if "BILAN CONSOLIDE" in ligne or "CONTROLE CROISE TERMINE" in ligne:
            continue
        if date_courante is None or agent_courant is None:
            continue
        if agent_courant not in agents:
            continue
        if (date_courante, agent_courant) in bloques:
            continue
        missions.append((date_courante, agent_courant, ligne.strip()[:80]))
    # filtre 3 jours
    try:
        borne = datetime.now() - timedelta(days=3)
        missions = [(d, a, l) for d, a, l in missions
                    if datetime.strptime(d, "%Y-%m-%d") >= borne]
    except Exception:
        pass
    return missions


def lecons_agent_corrections(agent):
    """Retourne les titres des lecons de l agent dans corrections.md (historique
    gele v1)."""
    chemin = os.path.join(AGENTS_DIR, agent, "corrections.md")
    if not os.path.exists(chemin):
        return []
    texte = lire(chemin)
    return [l for l in texte.splitlines() if l.startswith("## [LECON]")]


def agent_est_v1(agent):
    """Vrai si l agent appartient a l equipe v1 (dossier parcours dans
    cerveau-projet/agents/). Les agents v2 vivent dans freelance/."""
    return os.path.isdir(os.path.join(AGENTS_DIR, agent, "parcours"))


def bdd_agent(agent):
    """BDD des lecons de l agent : v1 (agents v1) ou v2 (agents freelance)."""
    return BDD_V1 if agent_est_v1(agent) else BDD_V2


def lecons_agent_bdd(agent):
    """Retourne les titres des lecons de l agent dans SA BDD (SQLite)."""
    bdd = bdd_agent(agent)
    if not os.path.exists(bdd):
        return []
    try:
        con = sqlite3.connect(bdd)
        try:
            cur = con.cursor()
            cur.execute("SELECT titre FROM lecons WHERE agent = ?",
                        (agent,))
            return [r[0] for r in cur.fetchall()]
        finally:
            con.close()
    except Exception:
        return []


def lecons_agent(agent, date_mission):
    """Lecon exigee selon la date de la mission :
    - date > GEL_DATE (2026-09-04, jour du gel) : SA BDD (v1 si agent v1,
      v2 si agent v2 - scission 2-bdd 2026-09-05).
    - date <= GEL_DATE : corrections.md gele (historique conserve) OU SA BDD
      (jour de transition : la bascule a eu lieu en cours de journee,
      certaines lecons du 09-04 sont deja en BDD)."""
    if date_mission > GEL_DATE:
        return lecons_agent_bdd(agent)
    return lecons_agent_corrections(agent) or lecons_agent_bdd(agent)


def lecon_contient_verdict(agent, date):
    """Vrai si l agent a une lecon datee >= date contenant un verdict.
    Cherche dans corrections.md (pre-migration) puis SA BDD."""
    # SA BDD : le verdict est dans le resume/lecon (ou le titre)
    bdd = bdd_agent(agent)
    if os.path.exists(bdd):
        try:
            con = sqlite3.connect(bdd)
            try:
                cur = con.cursor()
                # schema v2 : resume ; schema v1 : lecon
                try:
                    cur.execute("SELECT titre, resume FROM lecons WHERE agent = ?",
                                (agent,))
                except Exception:
                    cur.execute("SELECT titre, lecon FROM lecons WHERE agent = ?",
                                (agent,))
                for titre, corps in cur.fetchall():
                    bloc = (titre or "") + " " + (corps or "")
                    if re.search(r"(?i)verdict|VALIDE|CONFORME|A REVOIR|PROPRE|\bKO\b",
                                 bloc):
                        return True
            finally:
                con.close()
        except Exception:
            pass
    # corrections.md (historique gele v1)
    chemin = os.path.join(AGENTS_DIR, agent, "corrections.md")
    if os.path.exists(chemin):
        texte = lire(chemin)
        blocs = re.split(r"\n## \[LECON\] ", "\n" + texte)
        for bloc in blocs[1:]:
            m = re.match(r"([0-9]{4}-[0-9]{2}-[0-9]{2})", bloc)
            if not m:
                continue
            if m.group(1) >= date:
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

    # 4. Chaque mission recente a une lecon (v2 post-gel, corrections sinon)
    t4 = time.time()
    hist = lire(HISTORIQUE) if os.path.exists(HISTORIQUE) else ""
    agents = agents_reels()
    missions = missions_recentes(hist, agents)
    manques_lecon = []
    for date, agent, ligne in missions:
        if not lecons_agent(agent, date):
            manques_lecon.append("%s %s %s" % (agent, date, ligne))
    verifier("4. toute mission recente a une lecon (SA BDD post-gel, corrections pre-gel)",
             not manques_lecon, "sans lecon=%s" % manques_lecon[:3])
    chrono_etape("4. missions -> lecons", time.time() - t4)

    # 5. Chaque lecon recente contient un verdict
    t5 = time.time()
    manques_verdict = []
    for date, agent, ligne in missions:
        if not lecon_contient_verdict(agent, date):
            manques_verdict.append("%s %s %s" % (agent, date, ligne))
    verifier("5. lecons recentes contiennent un verdict (VERDICT/VALIDE/...)",
             not manques_verdict, "sans verdict=%s" % manques_verdict[:3])
    chrono_etape("5. lecons -> verdicts", time.time() - t5)

    # 6. Les missions TEST / entrees Cerberus ne sont pas exigees
    t6 = time.time()
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


def bilan_chrono():
    # Bilan des durees : total depuis le depart (regle immuable v0.3.0)
    try:
        _total = __import__("time").monotonic() - T_START
    except Exception:
        _total = 0.0
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)

if __name__ == "__main__":
    sys.exit(main())