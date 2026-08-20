#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-098-historique-format-garde-fou.py
GARDE-FOU : le format des blocs de AGENTS-historique.md (v0.5.15, demande
utilisateur 2026-08-19 "historique super lisible"). Chaque entree est un
bloc lisible :

  #>
  ### <span style="color:#...">2026-08-19 17:56</span> - <span style="color:#...">Cerberus</span>
  | 2026-08-19 17:56 | session-llm-1 | Cerberus | Mission : ... |
  ###> <continuations...>

Contraintes verrouillees :
  - la ligne de table '| date | session | agent | ...' reste le format
    MACHINE intact (parseurs lire-activite-recente, evaluer-processus)
  - le repere '###' est juste AU-DESSUS de sa table, avec la MEME date et
    le MEME agent
  - la couleur du repere = couleur fixe de l agent (COULEURS_PAR_AGENT du
    .py de activer-agent-principal, extraite par regex)
  - les lignes entre deux blocs ne sont que '#>' (bordure) ou '###>'
    (continuation) - aucune ligne orpheline
  - ordre decroissant des dates (plus recentes en haut)
  - lire-activite-recente fonctionne sur le fichier (rc=0)
  - ASCII strict (les couleurs sont des spans HTML ASCII)

Invariants verifies :
  1. Chaque table a son repere '###' juste au-dessus, date/agent coherents.
  2. La couleur du repere correspond a la couleur fixe de l agent.
  3. Aucune ligne orpheline entre les blocs (seulement '#>' / '###>').
  4. Dates en ordre decroissant (plus recente en haut).
  5. lire-activite-recente --nombre 3 : rc=0.
  6. ASCII strict sur tout le fichier.
  7. Preuve negative : un bloc a date incoherente est detecte (copie).

Tags: residus, garde-fou, preuve-negative, traces
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

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

HISTORIQUE = os.path.join(PROJECT_ROOT, "AGENTS-historique.md")
ACTIVER_PY = os.path.join(TOOLS_DIR, "activer", "activer-agent-principal",
                          "activer-agent-principal.py")
LIRE_ACTIVITE_PY = os.path.join(TOOLS_DIR, "lire", "lire-activite-recente",
                                "lire-activite-recente.py")

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
                                      timeout=timeout)


def lire_fichier(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def extraire_couleurs_par_agent():
    """Couleurs fixes par agent depuis COULEURS_PAR_AGENT du .py (regex)."""
    texte = lire_fichier(ACTIVER_PY)
    m = re.search(r"COULEURS_PAR_AGENT\s*=\s*\{(.*?)\n\}", texte, re.DOTALL)
    couleurs = {}
    if m:
        for nom, hexa in re.findall(r'^\s*"([a-z-]+)":\s*"#([0-9a-f]{6})"',
                                    m.group(1), re.MULTILINE):
            couleurs[nom] = "#" + hexa
    return couleurs


def analyser_blocs(texte):
    """Analyse les blocs de l historique.

    Retourne (problemes, tables) : probleme = (ligne, message) ; tables =
    liste de dicts {date, session, agent, repere_date, repere_agent,
    couleur, en_tete} pour chaque ligne de table.
    """
    lignes = texte.split("\n")
    problemes = []
    tables = []
    for i, ligne in enumerate(lignes):
        # v0.5.15 : table = '| <span>agent</span> | heure | date | session | ...'
        if not ligne.startswith("| <span"):
            continue
        parties = ligne.split("|")
        if len(parties) < 6:
            problemes.append((i, "table malformee: %r" % ligne[:60]))
            continue
        magent_tab = re.search(r"<span style=\"color:(#[0-9a-f]{6})\">([^<]+)</span>",
                               parties[1])
        couleur = magent_tab.group(1) if magent_tab else ""
        agent = magent_tab.group(2) if magent_tab else parties[1].strip()
        heure = parties[2].strip()
        date = parties[3].strip()
        session = parties[4].strip()
        repere_date = repere_agent = ""
        en_tete = False
        if i >= 1 and lignes[i - 1].startswith("### <span"):
            repere = lignes[i - 1]
            mdate = re.search(r">(\d{4}-\d{2}-\d{2} \d{2}:\d{2})</span>", repere)
            magent = re.search(r"- <span style=\"color:(#[0-9a-f]{6})\">([^<]+)</span>",
                               repere)
            if mdate:
                repere_date = mdate.group(1)
            if magent:
                repere_agent = magent.group(2)
        else:
            problemes.append((i, "table sans repere '###' au-dessus"))
        if repere_date and repere_date != (date + " " + heure):
            problemes.append((i, "date repere '%s' != table '%s %s'"
                             % (repere_date, date, heure)))
        if repere_agent and repere_agent != agent:
            problemes.append((i, "agent repere '%s' != table '%s'"
                             % (repere_agent, agent)))
        if i >= 2 and lignes[i - 2].strip() == "#>":
            en_tete = True
        tables.append({"date": date, "session": session, "agent": agent,
                       "repere_date": repere_date, "repere_agent": repere_agent,
                       "couleur": couleur, "en_tete": en_tete, "ligne": i})
    # lignes orphelines ENTRE les blocs (l entete avant la 1re table est
    # libre : frontmatter, intro, etc.)
    positions_tables = [t["ligne"] for t in tables]
    premier = min(positions_tables) if positions_tables else None
    for i, ligne in enumerate(lignes):
        if premier is not None and i < premier:
            continue  # entete libre
        if ligne.startswith("| <span") or ligne.startswith("### <span"):
            continue
        if ligne.strip() in ("#>", "") or ligne.startswith("###>"):
            continue
        problemes.append((i, "ligne orpheline: %r" % ligne[:60]))
    return problemes, tables


def main():
    t0 = time.monotonic()
    print("=== test-098 : format des blocs de AGENTS-historique (v0.5.15) ===")

    if not os.path.isfile(HISTORIQUE):
        print("=== RESULTAT : 0 OK / 1 KO (historique absent) ===")
        return 1
    texte = lire_fichier(HISTORIQUE)

    # 1. Chaque table a son repere '###' au-dessus, date/agent coherents
    t_debut = time.monotonic()
    problemes, tables = analyser_blocs(texte)
    structure_ko = [p for p in problemes if "date" in p[1] or "agent" in p[1]
                    or "sans repere" in p[1] or "malformee" in p[1]]
    verifier("1. chaque table a son repere '###' coherent (%d tables)"
             % len(tables), not structure_ko,
             "ko=%s" % structure_ko[:4])
    chrono_etape("1. repere ### coherent", t_debut)

    # 2. Couleur du repere = couleur fixe de l agent
    t_debut = time.monotonic()
    couleurs = extraire_couleurs_par_agent()
    mauvaise_couleur = []
    for t in tables:
        attendue = couleurs.get(t["agent"].lower(), "#334155")
        if t["couleur"] and t["couleur"] != attendue:
            mauvaise_couleur.append("%s ligne %d: %s != %s"
                                    % (t["agent"], t["ligne"], t["couleur"],
                                       attendue))
    verifier("2. couleur du repere = couleur fixe de l agent (%d agents)"
             % len(couleurs), not mauvaise_couleur,
             "ko=%s" % mauvaise_couleur[:4])
    chrono_etape("2. couleurs par agent", t_debut)

    # 3. Aucune ligne orpheline entre les blocs
    t_debut = time.monotonic()
    orphelines = [p for p in problemes if "orpheline" in p[1]]
    verifier("3. 0 ligne orpheline entre les blocs (seulement '#>' / '###>')",
             not orphelines, "ko=%s" % orphelines[:4])
    chrono_etape("3. lignes orphelines", t_debut)

    # 4. Dates en ordre decroissant (plus recente en haut)
    t_debut = time.monotonic()
    dates = [t["date"] for t in tables]
    decroissant = all(dates[j] >= dates[j + 1] for j in range(len(dates) - 1))
    verifier("4. dates en ordre decroissant (%d entrees)" % len(dates),
             decroissant)
    chrono_etape("4. ordre decroissant", t_debut)

    # 5. lire-activite-recente fonctionne sur le fichier
    t_debut = time.monotonic()
    r = run([PYTHON, LIRE_ACTIVITE_PY, "--nombre", "3"])
    verifier("5. lire-activite-recente --nombre 3 : rc=0", r.returncode == 0,
             "rc=%d %s" % (r.returncode, (r.stderr or "")[:80]))
    chrono_etape("5. lire-activite-recente", t_debut)

    # 6. ASCII strict sur tout le fichier
    t_debut = time.monotonic()
    non_ascii = sum(1 for c in texte if ord(c) > 127)
    verifier("6. ASCII strict : 0 non-ASCII", non_ascii == 0,
             "non_ascii=%d" % non_ascii)
    chrono_etape("6. ASCII", t_debut)

    # 7. Preuve negative : un bloc a date incoherente est detecte (copie)
    t_debut = time.monotonic()
    preuve_ok = False
    espace = tempfile.mkdtemp(prefix="tmp-test098-")
    try:
        copie = os.path.join(espace, "historique.md")
        lignes = texte.split("\n")
        # casser la date de la 2e table (sans toucher a son repere)
        for i, l in enumerate(lignes):
            if l.startswith("| <span") and i > 0 and lignes[i - 1].startswith("###"):
                # | <span...>agent</span> | heure | date | session | ...
                m = re.match(r"(\| <span[^>]*>[^<]*</span> \| )"
                             r"(\d{2}:\d{2})( \| )(\d{4}-\d{2}-\d{2})",
                             l)
                if m:
                    lignes[i] = (m.group(1) + "00:00" + m.group(3)
                                 + "2020-01-01" + l[len(m.group(0)):])
                    break
        with io.open(copie, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lignes))
        texte_copie = lire_fichier(copie)
        problemes_copie, _ = analyser_blocs(texte_copie)
        preuve_ok = any("date repere" in p[1] for p in problemes_copie)
    finally:
        shutil.rmtree(espace, ignore_errors=True)
    verifier("7. preuve negative : date table != repere detectee",
             preuve_ok, "incoherence non detectee")
    chrono_etape("7. preuve negative", t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
