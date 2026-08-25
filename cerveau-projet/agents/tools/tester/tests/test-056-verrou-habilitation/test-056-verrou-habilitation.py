#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-056-verrou-habilitation.py
GARDE-FOU : l outil proteger-verrou-habilitation (verrou d habilitation)
bloque l utilisation d un outil par un agent NON habilite (demande
utilisateur 2026-08-15 : verrou DIRECT bloquant + --agent obligatoire).

v0.2.0 (2026-08-15, demande utilisateur "flicage") : le verrou verifie en
plus l IDENTITE REELLE de l appelant (agent actif de la session lu dans
AGENTS.md) et journalise lui-meme chaque usage :
  - usage AUTORISE  -> registre-usages-outils.jsonl (mode verrou-auto)
  - tentative BLOQUEE -> registre-tentatives-bloquees.jsonl (espionnage)

v0.2.1 (2026-08-16, demande utilisateur "cle exclusive morpheus") : le verrou
verifie la CIBLE (--cible <chemin>) : toute modification d un fichier de test
(chemin contenant tester/tests/) est EXCLUSIVE a morpheus (regle immuable
SEUL MORPHEUS ECRIT LES TESTS), meme si l outil est dans la carte d un autre
agent. Preuve : buffy -> editer-fichier sur tester/tests/ = BLOQUE, morpheus
meme cible = OK.
  - usage AUTORISE  -> registre-usages-outils.jsonl (mode verrou-auto)
  - tentative BLOQUEE -> registre-tentatives-bloquees.jsonl (espionnage)
Les preuves de TABLE passent en --audit (table d habilitation pure, sans
identite reelle) ; une preuve d IDENTITE REELLE adaptative verifie que
l agent reel de la session ouvre (outil de sa carte) et qu un autre agent
est BLOQUE (usurpation), quel que soit l agent qui lance ce test.

Contexte :
  - Les regles de gouvernance exclusives (regles-groupes-agents.md) : seul
    janus lance la non-regression, seul hygie supprime, seul morpheus ecrit
    les tests, seul clio met a jour le README.
  - Les garde-fous existants verifient ces regles APRES coup (test-035/037/
    045 : cartes + registre). Le verrou les applique AVANT coup : au moment
    ou l agent appelle l outil, il doit prouver son habilitation (--agent)
    ET etre l agent reel de la session.
  - SOURCE DE VERITE : les cartes de decision (indices outil des parcours)
    + la table '## Sessions connues' d AGENTS.md (agent actif reel).
    Aucune liste en dur dans l outil : si une carte evolue, le verrou suit.
  - Verdict : rc=0 OK (verrou ouvert) / rc=1 BLOQUE (verrou ferme, avec la
    liste des habilites + la commande d activation, OU usurpation
    d identite) / rc=2 erreur d usage (--agent manquant, agent inconnu).

Invariants verifies :
  1. L outil existe, se compile, --version affiche v0.2.1
  2. Table (--audit) POSITIVE : janus -> tester-lancer-non-regression rc=0
  3. Table (--audit) NEGATIVE : cerberus -> tester-lancer-non-regression
     rc=1 ET message : agent habilite (janus) + commande d activation
  4. Table (--audit) Exclusivite suppression : hygie rc=0, cerberus rc=1
  5. --agent manquant -> rc=2 (le verrou refuse sans identite)
  6. Table (--audit) : outil non assigne -> rc=1 (alerte declaration)
  7. IDENTITE REELLE POSITIVE : l agent reel de la session + un outil de
     SA carte -> rc=0 (sans --audit)
  8. IDENTITE REELLE NEGATIVE : un AUTRE agent -> rc=1 BLOQUE
     (usurpation d identite, meme s il est habilite pour un autre outil)
  9. AUTO-JOURNALISATION : un usage autorise ajoute une entree verrou-auto
     au registre-usages ; une tentative bloquee ajoute une entree au
     registre-tentatives-bloquees
  10. Normes : ASCII strict + LF pur (outil + doc + test)
Tags: securite, verrou, habilitation, garde-fou
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

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

# Chemins des fichiers verifies
OUTIL_DIR = os.path.join(TOOLS_DIR, "proteger", "proteger-verrou-habilitation")
OUTIL_PY = os.path.join(OUTIL_DIR, "proteger-verrou-habilitation.py")
OUTIL_MD = os.path.join(OUTIL_DIR, "proteger-verrou-habilitation.md")
TRACES_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces")
REGISTRE_USAGES = os.path.join(TRACES_DIR, "registre-usages-outils.jsonl")
REGISTRE_BLOQUES = os.path.join(TRACES_DIR, "registre-tentatives-bloquees.jsonl")

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
ETAPES = []  # (nom, duree_secondes) alimente le bilan chrono


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    """True si le point N doit s executer (options on/off du test)."""
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    """Enregistre la duree d une etape (no-op si --no-chrono)."""
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    """Affiche le bilan des durees : total + detail par etape."""
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    detail = " | ".join("%s=%.2fs" % e for e in ETAPES)
    print("=== CHRONO : total %.2fs (%s) ===\n" % (total, detail))


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


def agent_actif_reel():
    """Agent actif REEL de la session (meme logique que le verrou v0.2.0) :
    colonne Agent actif de la table '## Sessions connues' d AGENTS.md,
    session la plus recente. Retourne None si indeterminable."""
    chemin = os.path.join(PROJECT_ROOT, "AGENTS.md")
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
    except IOError:
        return None
    m = re.search(r"## Sessions connues\n(.*?)(?=\n## |\Z)", contenu, re.S)
    if not m:
        return None
    lignes = []
    for ligne in m.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("| session-"):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cellules) >= 4:
            lignes.append(cellules)
    if not lignes:
        return None
    lignes.sort(key=lambda c: c[3], reverse=True)
    actif = lignes[0][2].strip()
    return actif if actif and actif != "-" else None


def _lire_table_sessions():
    """Lit la table '## Sessions connues' d AGENTS.md : liste de tuples
    (session, agent_actif, derniere_activite) pour les lignes valides.
    Retourne [] si la table est absente/illisible (preuve sautee)."""
    chemin = os.path.join(PROJECT_ROOT, "AGENTS.md")
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
    except IOError:
        return []
    m = re.search(r"## Sessions connues\n(.*?)(?=\n## |\Z)", contenu, re.S)
    if not m:
        return []
    resultats = []
    for ligne in m.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("| session-"):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cellules) >= 4:
            resultats.append((cellules[0], cellules[2], cellules[3]))
    return resultats


def outil_de_la_carte(agent):
    """Un outil de la carte de l agent (indices type outil)."""
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", agent,
                          "parcours", "parcours-%s.json" % agent)
    try:
        p = json.load(io.open(chemin, encoding="utf-8"))
    except Exception:
        return None
    for cid, case in p.get("cases", {}).items():
        for ind in case.get("indices", []):
            if isinstance(ind, dict) and ind.get("type") == "outil" \
                    and ind.get("nom"):
                return ind["nom"]
    return None


def autres_agents():
    """Liste des agents connus (hors hygienes du test)."""
    resultats = []
    if os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")):
        for nom in sorted(os.listdir(os.path.join(PROJECT_ROOT,
                                                  "cerveau-projet", "agents"))):
            if os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet",
                                          "agents", nom, "parcours")):
                resultats.append(nom)
    return resultats


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Test formel verrou-habilitation v0.2.1 ===")
    try:
        # 1. L outil existe + compile + version
        if point_actif(1):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "--version"])
            verifier("1. --version affiche v0.4.2",
                     "v0.4.2" in r.stdout, r.stdout.strip())
            chrono_etape("1. version", t)

        # 2. Table (--audit) POSITIVE : janus -> non-regression (seul habilite)
        if point_actif(2):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "--agent", "janus",
                     "--outil", "tester-lancer-non-regression", "--audit"])
            ok = (r.returncode == 0 and "OK" in r.stdout
                  and "habilite" in r.stdout)
            verifier("2. TABLE janus -> non-regression : verrou OUVERT (rc=0)",
                     ok, "rc=%s %s" % (r.returncode, r.stdout.strip()))
            chrono_etape("2. table positive", t)

        # 3. Table (--audit) NEGATIVE : cerberus -> non-regression
        if point_actif(3):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "--agent", "cerberus",
                     "--outil", "tester-lancer-non-regression", "--audit"])
            sortie = r.stdout + r.stderr
            ok = (r.returncode == 1 and "BLOQUE" in sortie
                  and "janus" in sortie and "activer" in sortie)
            verifier("3. TABLE cerberus -> non-regression : FERME (rc=1) + "
                     "commande d activation", ok, r.stdout.strip())
            chrono_etape("3. table negative", t)

        # 3b. LISTE BLANCHE DEVELOPPEUR (v0.2.2, utilisateur 2026-08-16) :
        # vulcain (constructeur du lanceur) VALIDE ses modifications sans
        # attendre janus ; morpheus reste BLOQUE (liste stricte).
        if point_actif("3b"):
            t = time.monotonic()
            r_v = run([PYTHON, OUTIL_PY, "--agent", "vulcain",
                       "--outil", "tester-lancer-non-regression", "--audit"])
            ok_v = (r_v.returncode == 0 and "liste blanche developpeur" in r_v.stdout)
            verifier("3b. VULCAIN -> non-regression : OUVERT (rc=0, liste "
                     "blanche developpeur)", ok_v, r_v.stdout.strip())
            r_m = run([PYTHON, OUTIL_PY, "--agent", "morpheus",
                       "--outil", "tester-lancer-non-regression", "--audit"])
            ok_m = (r_m.returncode == 1 and "BLOQUE" in r_m.stdout)
            verifier("3c. MORPHEUS -> non-regression : FERME (rc=1, liste "
                     "stricte : seul vulcain dev)", ok_m, r_m.stdout.strip())
            chrono_etape("3b/3c. liste blanche developpeur", t)

        # 4. Table (--audit) Exclusivite suppression : hygie OK, cerberus BLOQUE
        if point_actif(4):
            t = time.monotonic()
            r_hygie = run([PYTHON, OUTIL_PY, "--agent", "hygie",
                           "--outil", "supprimer-fichier", "--audit"])
            r_cerb = run([PYTHON, OUTIL_PY, "--agent", "cerberus",
                          "--outil", "supprimer-fichier", "--audit"])
            ok = (r_hygie.returncode == 0 and "OK" in r_hygie.stdout
                  and r_cerb.returncode == 1 and "BLOQUE" in
                  (r_cerb.stdout + r_cerb.stderr) and "hygie" in
                  (r_cerb.stdout + r_cerb.stderr))
            verifier("4. TABLE hygie supprime (rc=0) / cerberus BLOQUE (rc=1, "
                     "message -> hygie)", ok,
                     "hygie=%s cerb=%s" % (r_hygie.returncode,
                                           r_cerb.returncode))
            chrono_etape("4. exclusivite suppression", t)

        # 5. --agent manquant : rc=2 (le verrou refuse sans identite)
        if point_actif(5):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "--outil", "tester-lancer-non-regression"])
            ok = r.returncode == 2 and "OBLIGATOIRE" in (r.stdout + r.stderr)
            verifier("5. --agent manquant : refus rc=2 (--agent obligatoire)",
                     ok, "rc=%s" % r.returncode)
            chrono_etape("5. agent manquant", t)

        # 6. Table (--audit) : outil non assigne -> rc=1 (alerte declaration)
        if point_actif(6):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "--agent", "janus",
                     "--outil", "outil-inexistant", "--audit"])
            sortie = r.stdout + r.stderr
            ok = r.returncode == 1 and "AUCUNE carte" in sortie
            verifier("6. TABLE outil non assigne : alerte rc=1 (declaration "
                     "manquante)", ok, r.stdout.strip())
            chrono_etape("6. outil non assigne", t)

        # 7-8. IDENTITE REELLE (v0.2.0) : adaptatif a l agent actif de la
        # session. L agent reel + un outil de sa carte -> rc=0 ; un AUTRE
        # agent -> rc=1 BLOQUE (usurpation), meme s il est habilite ailleurs.
        actif = agent_actif_reel()
        agents_connus = autres_agents()
        outil_actif = outil_de_la_carte(actif) if actif else None
        autre_agent = None
        if actif and agents_connus:
            for nom in agents_connus:
                if nom.lower() != actif.lower():
                    autre_agent = nom
                    break

        if point_actif(7):
            t = time.monotonic()
            if actif and outil_actif:
                r = run([PYTHON, OUTIL_PY, "--agent", actif,
                         "--outil", outil_actif])
                ok = (r.returncode == 0 and "OK" in r.stdout)
                verifier("7. IDENTITE REELLE : l agent actif '%s' + outil de "
                         "sa carte (%s) -> OUVERT (rc=0)"
                         % (actif, outil_actif), ok,
                         "rc=%s %s" % (r.returncode, r.stdout.strip()))
            else:
                verifier("7. IDENTITE REELLE : agent actif indeterminable "
                         "(preuve sautee)", True)
            chrono_etape("7. identite positive", t)

        if point_actif(8):
            t = time.monotonic()
            if actif and autre_agent and outil_actif:
                r = run([PYTHON, OUTIL_PY, "--agent", autre_agent,
                         "--outil", outil_actif])
                sortie = r.stdout + r.stderr
                ok = (r.returncode == 1 and "BLOQUE" in sortie
                      and "usurpation" in sortie.lower()
                      and actif in sortie)
                verifier("8. IDENTITE REELLE : '%s' (session sur %s) -> FERME "
                         "(rc=1, usurpation d identite)"
                         % (autre_agent, actif), ok, r.stdout.strip())
            else:
                verifier("8. IDENTITE REELLE : contexte indeterminable "
                         "(preuve sautee)", True)
            chrono_etape("8. identite negative", t)

        # 8b. MULTI-SESSIONS (v0.4.2) : trouver_session_agent retourne la
        # session la PLUS RECENTE portant l agent (colonne Derniere activite
        # de la table '## Sessions connues'), pas le premier bloc AGENTS.md.
        # Anti-recurrence du bug detecte par Janus (D6) : quand 2 sessions
        # portent le meme agent actif (ex: morpheus dans llm-1 et llm-4),
        # la commande suggeree par le verrou doit viser la session de
        # l appelant (la plus recente).
        if point_actif(8):
            t = time.monotonic()
            try:
                spec_v = importlib.util.spec_from_file_location(
                    "verrou_habilitation", OUTIL_PY)
                mod_v = importlib.util.module_from_spec(spec_v)
                spec_v.loader.exec_module(mod_v)
                mod_v.detecter_racine()
                table_sessions = _lire_table_sessions()
                ok_8b = True
                detail = ""
                if not table_sessions:
                    verifier("8b. trouver_session_agent : table absente "
                             "(preuve sautee)", True)
                else:
                    # Pour chaque agent, la resolution doit retourner SA
                    # session la plus recente (max Derniere activite).
                    # Un agent peut apparaitre dans plusieurs sessions : seule
                    # la plus recente est attendue.
                    max_par_agent = {}
                    for session, agent_actif, activite in table_sessions:
                        if agent_actif in ("-", ""):
                            continue
                        actuel = max_par_agent.get(agent_actif)
                        if actuel is None or activite > actuel[1]:
                            max_par_agent[agent_actif] = (session, activite)
                    for agent_actif, (session_att, activite) in \
                            sorted(max_par_agent.items()):
                        resolu = mod_v.trouver_session_agent(agent_actif)
                        if resolu != session_att:
                            ok_8b = False
                            detail += "%s(%s)->%s attendu %s; " % (
                                agent_actif, activite, resolu, session_att)
                    verifier("8b. trouver_session_agent : chaque agent resout "
                             "vers SA session la plus recente (v0.4.2)",
                             ok_8b, detail or "toutes resolutions exactes")
            except Exception as e:
                verifier("8b. trouver_session_agent (v0.4.2)", False,
                         "exception: %s" % e)
            chrono_etape("8b. session la plus recente", t)

        # 9. AUTO-JOURNALISATION (v0.2.0) : l outil signale lui-meme son
        # usage. Le point 7 (usage autorise) a du ajouter une entree
        # verrou-auto au registre-usages ; le point 8 (tentative usurpee) une
        # entree au registre-tentatives-bloquees.
        if point_actif(9):
            t = time.monotonic()
            auto_ok = False
            if actif and outil_actif and os.path.isfile(REGISTRE_USAGES):
                with io.open(REGISTRE_USAGES, encoding="utf-8",
                             errors="replace") as fh:
                    for ligne in fh:
                        try:
                            e = json.loads(ligne)
                        except ValueError:
                            continue
                        if e.get("mode") == "verrou-auto" \
                                and e.get("agent", "").lower() == actif.lower() \
                                and e.get("outil") == outil_actif:
                            auto_ok = True
                            break
            verifier("9. AUTO-JOURNALISATION : usage autorise '%s -> %s' "
                     "journalise (mode verrou-auto)"
                     % (actif, outil_actif), auto_ok,
                     "registre=%s" % REGISTRE_USAGES)
            bloque_ok = False
            if actif and autre_agent and outil_actif \
                    and os.path.isfile(REGISTRE_BLOQUES):
                with io.open(REGISTRE_BLOQUES, encoding="utf-8",
                             errors="replace") as fh:
                    for ligne in fh:
                        try:
                            e = json.loads(ligne)
                        except ValueError:
                            continue
                        if e.get("mode") == "verrou-bloque" \
                                and e.get("outil") == outil_actif:
                            bloque_ok = True
                            break
            verifier("9b. AUTO-JOURNALISATION : tentative '%s' journalisee au "
                     "registre-tentatives-bloquees"
                     % (autre_agent or "?"), bloque_ok,
                     "registre=%s" % REGISTRE_BLOQUES)
            chrono_etape("9. auto-journalisation", t)

        # 10. Normes (ASCII strict + LF pur) sur les fichiers concernes
        if point_actif(10):
            t = time.monotonic()
            fichiers = [OUTIL_PY, OUTIL_MD, os.path.abspath(__file__)]
            total_non_ascii = sum(ascii_count(f) for f in fichiers)
            verifier("10. ASCII strict : 0 non-ASCII (outil + doc + test)",
                     total_non_ascii == 0, "total=%d" % total_non_ascii)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("10b. LF pur : 0 CRLF (outil + doc + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("10. normes", t)

        # 11. CLE EXCLUSIVE MORPHEUS (v0.2.1) : toute modification d un
        # fichier de test (tester/tests/) est EXCLUSIVE a morpheus, meme si
        # l outil est dans la carte d un autre agent.
        if point_actif(11):
            t = time.monotonic()
            cible_test = os.path.join("cerveau-projet", "agents", "tools",
                                      "tester", "tests", "test-050-triplet-outils-temporaires",
                                      "test-050-triplet-outils-temporaires.py")
            r_buffy = run([PYTHON, OUTIL_PY, "--agent", "buffy",
                           "--outil", "editer-fichier", "--cible", cible_test,
                           "--audit"])
            sortie = r_buffy.stdout + r_buffy.stderr
            ok = (r_buffy.returncode == 1 and "EXCLUSIVE a morpheus" in sortie
                  and "morpheus" in sortie)
            verifier("11. CLE EXCLUSIVE : buffy -> editer-fichier sur test = "
                     "BLOQUE (rc=1, exclusif morpheus)", ok,
                     r_buffy.stdout.strip())
            r_morph = run([PYTHON, OUTIL_PY, "--agent", "morpheus",
                           "--outil", "editer-fichier", "--cible", cible_test,
                           "--audit"])
            ok2 = (r_morph.returncode == 0 and "OK" in r_morph.stdout
                   and "cle exclusive" in r_morph.stdout)
            verifier("11b. CLE EXCLUSIVE : morpheus meme cible = OUVERT (rc=0)",
                     ok2, r_morph.stdout.strip())
            r_normal = run([PYTHON, OUTIL_PY, "--agent", "buffy",
                            "--outil", "editer-fichier",
                            "--cible", "cerveau-projet/agents/README.md",
                            "--audit"])
            ok3 = (r_normal.returncode == 0 and "OK" in r_normal.stdout)
            verifier("11c. cible NON-test : buffy -> editer-fichier = OUVERT "
                     "(carte, pas de zone protegee)", ok3, r_normal.stdout.strip())
            chrono_etape("11. cle exclusive", t)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
