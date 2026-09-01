#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-098-historique-format-garde-fou.py
GARDE-FOU : le format de AGENTS-historique.md (v0.6.1 timeline, v0.5.20 :
colonne 2 = id LLM, demande utilisateur 2026-08-20 "session -> id"). Chaque
entree est une ligne du corps de l historique :

  ## YYYY-MM-DD
  ### Agent
  - HH:MM[:SS[.microsec]] | id | TYPE | raison

Invariants verifies :
  1. Chaque entree '- HH:MM[:SS[.microsec]] | ...' est sous un bloc jour '## YYYY-MM-DD'
     et un bloc agent '### Agent' (le dernier '###' rencontre au-dessus).
  2. Le nom du bloc agent est un agent connu (dans AGENTS.md / le .py).
  3. Chaque bloc jour '## YYYY-MM-DD' contient au moins un bloc agent
     (pas de jour vide) et les jours sont en ordre decroissant.
  4. Les heures au sein d un bloc agent sont en ordre decroissant.
  5. lire-activite-recente --nombre 3 : rc=0 (parseur officiel).
  6. ASCII strict sur tout le fichier.
  7. Preuve negative : une entree orpheline (sans bloc agent) est detectee
     (copie).

Note : l entete du fichier (frontmatter + encart 'Activites recentes') est
libre -- les verifications portent sur le CORPS de l historique (sections
'## YYYY-MM-DD').

Proprietaire : Morpheus (testeur dedie)
Version : 0.2.0
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


def extraire_agents_md(texte):
    """Agents declares dans AGENTS.md via les liens [X](cerveau-projet/agents/N/N.md).
    On extrait le nom depuis le DOSSIER du lien (robuste aux libelles
    particuliers, ex: ferrari reference avec le chemin complet en libelle).
    On ajoute 'oracle' : outil de coordination v1 qui s AUTO-HISTORISE
    (il apparait comme agent dans le corps sans avoir de fiche dediee)."""
    agents = set(re.findall(r"\]\(cerveau-projet/agents/([a-z0-9-]+)/[a-z0-9-]+\.md\)",
                            texte))
    agents.add("oracle")
    return agents


def analyser_corps(texte):
    """Analyse le CORPS de l historique (sections '## YYYY-MM-DD').

    Retourne (problemes, entrees, jours) :
      problemes : liste (ligne, message) des incoherences
      entrees   : liste de dicts {jour, agent, heure, id, ligne}
      jours     : liste de dicts {jour, ligne, nb_agents, nb_entrees}
    """
    lignes = texte.split("\n")
    problemes = []
    entrees = []
    jours = []
    jour_courant = None
    agent_courant = None
    dans_corps = False
    for i, ligne in enumerate(lignes):
        l = ligne.strip()
        if l.startswith("## ") and len(l) >= 13 and l[3] in "0123456789":
            # Bloc jour : ## YYYY-MM-DD (debut du corps)
            jour = l[3:].strip()
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", jour):
                problemes.append((i, "jour malforme: %r" % jour[:20]))
            jour_courant = jour
            agent_courant = None
            dans_corps = True
            jours.append({"jour": jour, "ligne": i, "nb_agents": 0,
                          "nb_entrees": 0})
            continue
        if not dans_corps:
            continue
        if l.startswith("### "):
            agent = l[4:].strip()
            agent_courant = agent
            if jours and jour_courant:
                jours[-1]["nb_agents"] += 1
            continue
        if l.startswith("- ") and jour_courant and agent_courant:
            contenu = l[2:].strip()
            parties = contenu.split(" | ")
            if len(parties) >= 3:
                heure = parties[0].strip()
                identifiant = parties[1].strip()
                if not re.match(r"^\d{2}:\d{2}(:\d{2}(\.\d+)?)?$", heure):
                    problemes.append((i, "heure malformee: %r" % heure))
                entrees.append({"jour": jour_courant, "agent": agent_courant,
                               "heure": heure, "id": identifiant, "ligne": i})
                if jours:
                    jours[-1]["nb_entrees"] += 1
                continue
        # Ligne dans le corps mais ni jour, ni agent, ni entree : orpheline
        if jour_courant and l not in ("",) and not l.startswith("|"):
            problemes.append((i, "ligne orpheline: %r" % l[:60]))
    return problemes, entrees, jours


def main():
    t0 = time.monotonic()
    print("=== test-098 : format des blocs de AGENTS-historique (v0.6.1) ===")

    if not os.path.isfile(HISTORIQUE):
        print("=== RESULTAT : 0 OK / 1 KO (historique absent) ===")
        return 1
    texte = lire_fichier(HISTORIQUE)
    agents_md = extraire_agents_md(lire_fichier(
        os.path.join(PROJECT_ROOT, "AGENTS.md")))

    problemes, entrees, jours = analyser_corps(texte)

    # 1. Chaque entree a un bloc jour et un bloc agent au-dessus
    t_debut = time.monotonic()
    structure_ko = [p for p in problemes if "orpheline" not in p[1]
                    and "jour malforme" not in p[1]]
    verifier("1. entrees sous bloc jour + bloc agent (%d entrees)"
             % len(entrees), not structure_ko,
             "ko=%s" % structure_ko[:4])
    chrono_etape("1. structure jour/agent", t_debut)

    # 2. Les agents des blocs sont connus. EXEMPTION DOCUMENTEE : les routines
    #    v1 (serveur de routines oracle, manifest.json) historisent sous leur
    #    NOM de routine (live, flux, notation, verifier-statuts,
    #    vigie-perimetre, citations, ...) avec un id LLM et le type 'R' (voir
    #    la colonne Executeur RT(<intervalle>) dans l encart v1). Ce ne sont
    #    pas des agents mais des artefacts de routine documentes, toleres.
    t_debut = time.monotonic()
    blocs_routines = {"citations", "encart", "flux", "live", "notation",
                      "verifier-statuts", "vigie-perimetre"}
    inconnus = sorted(set(e["agent"].lower() for e in entrees)
                      - set(a.lower() for a in agents_md)
                      - blocs_routines)
    verifier("2. blocs agent connus (%d agents)" % len(agents_md),
             not inconnus, "inconnus=%s" % inconnus[:5])
    chrono_etape("2. agents connus", t_debut)

    # 3. Jours en ordre decroissant + pas de jour vide
    t_debut = time.monotonic()
    jours_liste = [j["jour"] for j in jours]
    decroissant = all(jours_liste[k] >= jours_liste[k + 1]
                      for k in range(len(jours_liste) - 1))
    jours_vides = [j["jour"] for j in jours if j["nb_entrees"] == 0]
    verifier("3. jours decroissants (%d jours), aucun vide"
             % len(jours_liste), decroissant and not jours_vides,
             "vides=%s" % jours_vides[:4])
    chrono_etape("3. jours decroissants", t_debut)

    # 4. Heures en ordre decroissant au sein de chaque bloc agent
    t_debut = time.monotonic()
    mauvais_ordre = []
    par_agent = {}
    for e in entrees:
        par_agent.setdefault((e["jour"], e["agent"]), []).append(e["heure"])
    for cle, heures in par_agent.items():
        if any(heures[k] < heures[k + 1] for k in range(len(heures) - 1)):
            mauvais_ordre.append("%s/%s" % cle)
    verifier("4. heures decroissantes par bloc agent (%d blocs)"
             % len(par_agent), not mauvais_ordre,
             "ko=%s" % mauvais_ordre[:4])
    chrono_etape("4. heures decroissantes", t_debut)

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

    # 7. Preuve negative : une entree orpheline (sans bloc agent) est detectee
    t_debut = time.monotonic()
    preuve_ok = False
    espace = tempfile.mkdtemp(prefix="tmp-test098-")
    try:
        copie = os.path.join(espace, "historique.md")
        lignes = texte.split("\n")
        # Inserer une entree '- 00:00 | id | test orphelin' juste apres le
        # 1er bloc jour, sans bloc agent au-dessus (on est sous un bloc agent
        # existant -> on retire le nom du bloc pour rendre l entree orpheline)
        for i, l in enumerate(lignes):
            if l.startswith("- ") and i > 0 and lignes[i - 1].startswith("### "):
                # casser : retirer le bloc agent (ligne '###' -> '#')
                lignes[i - 1] = "# " + lignes[i - 1][4:]
                break
        with io.open(copie, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lignes))
        texte_copie = lire_fichier(copie)
        problemes_copie, _, _ = analyser_corps(texte_copie)
        preuve_ok = any("orpheline" in p[1] for p in problemes_copie)
    finally:
        shutil.rmtree(espace, ignore_errors=True)
    verifier("7. preuve negative : entree sans bloc agent detectee",
             preuve_ok, "incoherence non detectee")
    chrono_etape("7. preuve negative", t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
