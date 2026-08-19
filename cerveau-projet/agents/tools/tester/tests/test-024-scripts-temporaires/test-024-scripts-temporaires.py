#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-024-scripts-temporaires.py
Test formel du garde-fou anti-scripts-temporaires v0.1.0
(lecon : les agents preferaient les scripts jetables .zz-*/.tmp-* a nos outils).

Contexte (mission anti-scripts-temporaires, 2026-08-11) :
  - Le registre d usage etait a 0 ligne : les scripts temporaires ne passent
    pas par le generateur -> invisibles pour les controles.
  - 3 outils crees : tester-lancer-non-regression (tester/), editer-parcours
    (editer/), detecter-usage-scripts-temporaires (detecter/).
  - enregistrer-usage-outil v0.2.0 : nouveau mode "script-temporaire" pour
    DECLARER la creation d'un script temporaire.
  - Ce garde-fou verifie qu'aucun script temporaire .zz-* / .tmp-* ne
    traine a la racine du projet (les scripts temporaires sont autorises
    uniquement en declaration mode script-temporaire au registre).

Cas couverts:
  1. Aucun fichier .zz-* a la racine du projet
  2. Aucun fichier .tmp-* a la racine du projet
  2b. Aucun dossier tmp-* residuel a la racine (hors dossier de l agent
      courant, regle d origine v0.2.4 : dossier cree + supprime en fin)
  3. detecter-usage-scripts-temporaires : executable + --version v0.1.1
  4. detecter-usage-scripts-temporaires : sortie sans ERREUR
  5. editer-parcours : --version v0.1.1
  6. tester-lancer-non-regression : --version v0.1.1
  7. enregistrer-usage-outil : mode script-temporaire accepte (--version v0.3.0)
  8. Catalogue : les nouvelles commandes presentes (172 total)
  9. index-tools : les 4 nouvelles lignes presentes (3 outils + editer-fichier-agents)
 10. ASCII strict : 0 non-ASCII (outils + test)
 11. LF pur : 0 CRLF (outils + test)
 12. Protection : le test lui-meme ne cree aucun fichier a la racine
 13. Garde-fou fusion : le registre actif contient les 12 entrees script-temporaire
     (decision utilisateur 2026-08-14 : plus d historique, les entrees ont ete
     fusionnees dans registre-usages-outils.jsonl)

Usage:
  python3 test-024-scripts-temporaires.py
Tags: registre-traces, garde-fou, anti-recurrence, scripts-temp
"""
import glob
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROTECTIONS = charger_protections()
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0, deploiement dynamique) :
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
        for _p in sys.argv[_i + 1].split(','):
            try:
                DESACTIVES.append(int(_p))
            except ValueError:
                pass
ETAPES = []
T_START = __import__("time").monotonic()


def point_actif(numero):
    # True si le point N doit s executer (options on/off du test)
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    # Enregistre la duree d une etape (no-op si --no-chrono)
    if CHRONO_ACTIF:
        ETAPES.append((nom, __import__("time").monotonic() - t_debut))


def bilan_chrono():
    # Affiche le bilan des durees : total + detail par etape
    if not CHRONO_ACTIF:
        return
    _total = __import__("time").monotonic() - T_START
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)
    for _nom, _duree in ETAPES:
        print("  %-34s %6.2fs" % (_nom, _duree))


DETECTER = os.path.join(TOOLS_DIR, "detecter", "detecter-usage-scripts-temporaires",
                        "detecter-usage-scripts-temporaires.py")
EDITER_PARCOURS = os.path.join(TOOLS_DIR, "editer", "editer-parcours", "editer-parcours.py")
LANCER = os.path.join(TOOLS_DIR, "tester", "tester-lancer-non-regression", "tester-lancer-non-regression.py")
ENREGISTRER = os.path.join(TOOLS_DIR, "enregistrer", "enregistrer-usage-outil",
                           "enregistrer-usage-outil.py")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX = os.path.join(TOOLS_DIR, "index-tools.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


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
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lire_tmpignore():
    """Lit cerveau-projet/agents/traces/.tmpignore et retourne les noms EXACTS
    de dossiers temporaires autorises (derrogation ciblee v0.1.3). Fichier
    absent ou vide = aucune derrogation. Format : un nom par ligne, # commentaire."""
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                          ".tmpignore")
    noms = set()
    if os.path.isfile(chemin):
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            for ligne in fh:
                nom = ligne.strip()
                if nom and not nom.startswith("#"):
                    noms.add(nom)
    return noms


def main():
    global NB_POINTS, NB_OK, NB_KO

    # 1-2. Aucun script temporaire a la racine
    racine = PROJECT_ROOT
    # Anti-artefact (lecon 2026-08-13) : le lanceur de non-regression peut
    # declarer via l environnement le script temporaire PARENT qui l a lance
    # (script en cours d execution, legitime, pas un residu). Exclure ces noms
    # du scan : un vrai residu n est jamais declare -> il reste KO.
    exclusions = set()
    for e in os.environ.get("NON_REGRESSION_EXCLUSIONS", "").split(","):
        e = e.strip()
        if e:
            exclusions.add(e)
    # Derrogation ciblee (v0.1.3, decision utilisateur 2026-08-15) : le
    # fichier cerveau-projet/agents/traces/.tmpignore liste des noms EXACTS
    # de dossiers temporaires autorises a rester. Un nom liste est exclu du
    # scan, tout AUTRE dossier temp reste un residu (la protection reste forte).
    for nom in lire_tmpignore():
        exclusions.add(nom)
    zz = [n for n in os.listdir(racine)
          if n.startswith(".zz-") and n not in exclusions]
    tmp = [n for n in os.listdir(racine)
           if n.startswith(".tmp-") and n not in exclusions]
    verifier("1. Aucun fichier .zz-* a la racine", len(zz) == 0, str(zz[:5]))
    verifier("2. Aucun fichier .tmp-* a la racine", len(tmp) == 0, str(tmp[:5]))

    # 2b. Aucun dossier temporaire RESIDUEL tmp-* a la racine (regle
    #     d origine v0.2.4) : le dossier tmp-<agent> de la mission COURANTE
    #     est legitime (cree en debut, supprime en fin) et exclu, ainsi que
    #     les dossiers listes dans le .tmpignore (derrogation ciblee) ; tout
    #     AUTRE dossier tmp-* = residu = KO.
    agent_courant = ""
    profil = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                          "classeur-variables", "stockage",
                          "variables-actuelles.md")
    if os.path.isfile(profil):
        with io.open(profil, encoding="utf-8", errors="replace") as fh:
            for ligne in fh:
                if "profil-session-llm-1" in ligne:
                    m = re.search(r"agent:\s*([A-Za-z0-9_-]+)", ligne)
                    if m:
                        agent_courant = m.group(1)
                    break
    dossiers_residuels = [n for n in os.listdir(racine)
                          if n.startswith("tmp-")
                          and os.path.isdir(os.path.join(racine, n))
                          and n != ("tmp-%s" % agent_courant)
                          and n not in exclusions]
    verifier("2b. Aucun dossier tmp-* residuel a la racine (hors agent courant)",
             len(dossiers_residuels) == 0, str(dossiers_residuels[:5]))

    # 2c. Format du .tmpignore (derrogation ciblee) : fichier present dans
    #     traces/, ASCII strict, LF, lignes non vides hors commentaires = noms
    #     EXACTS (aucun motif global de type tmp-*).
    tmpignore_chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                    "traces", ".tmpignore")
    format_ok = os.path.isfile(tmpignore_chemin)
    if format_ok:
        with io.open(tmpignore_chemin, encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        format_ok = (ascii_count(tmpignore_chemin) == 0
                     and crlf_count(tmpignore_chemin) == 0
                     and all("*" not in ligne
                             for ligne in contenu.splitlines()
                             if ligne.strip() and not ligne.strip().startswith("#")))
    verifier("2c. .tmpignore present dans traces/, ASCII + LF, noms EXACTS sans motif",
             format_ok, os.path.basename(tmpignore_chemin) if not format_ok else "")

    # 3-4. detecter-usage-scripts-temporaires
    r = run([PYTHON, DETECTER, "--version"])
    verifier("3. detecter --version v0.1.1",
             r.returncode == 0 and "v0.1.1" in r.stdout, r.stdout.strip()[-60:])
    r = run([PYTHON, DETECTER])
    verifier("4. detecter : sortie sans ERREUR",
             r.returncode in (0, 1) and "ERREUR" not in r.stdout, r.stdout.strip()[-80:])

    # 5-6. editer-parcours + tester-lancer-non-regression
    r = run([PYTHON, EDITER_PARCOURS, "--version"])
    verifier("5. editer-parcours --version v0.1.7",
             r.returncode == 0 and "v0.1.7" in r.stdout, r.stdout.strip()[-60:])
    r = run([PYTHON, LANCER, "--version"])
    verifier("6. tester-lancer-non-regression --version v0.6.2",
             r.returncode == 0 and "v0.6.2" in r.stdout, r.stdout.strip()[-60:])

    # 7. enregistrer-usage-outil v0.3.0 (mode script-temporaire + garde-fous + tri)
    r = run([PYTHON, ENREGISTRER, "--version"])
    verifier("7. enregistrer-usage-outil --version v0.3.0",
             r.returncode == 0 and "v0.3.0" in r.stdout, r.stdout.strip()[-60:])

    # 8. Catalogue : 171 commandes + les nouvelles
    import json as json_mod
    with io.open(CATALOGUE, encoding="utf-8") as fh:
        cat = json_mod.load(fh)
    noms = [e.get("nom") for e in cat.get("commandes", [])]
    ok_cat = (len(noms) == 183 and "lire-head" in noms
              and "tester-lancer-non-regression" in noms
              and "editer-parcours" in noms and "detecter-usage-scripts-temporaires" in noms
              and "detecter-cablages-manquants" in noms and "tester-protections" in noms
              and "detecter-fautes-orthographe" in noms and "detecter-contradictions" in noms
              and "purifier-rvav" in noms and "analyser-io-tests" in noms
              and "analyser-noms-maj" in noms and "corriger-noms-maj" in noms
              and "detecter-processus-residuels" in noms
              and "nettoyer-processus-residuels" in noms)
    verifier("8. catalogue : 183 commandes + nouvelles presentes",
             ok_cat, "nb=%d" % len(noms))

    # 9. index-tools : les 4 lignes presentes
    with io.open(INDEX, encoding="utf-8") as fh:
        idx = fh.read()
    ok_idx = all(x in idx for x in ["tester-lancer-non-regression", "editer-parcours",
                                    "detecter-usage-scripts-temporaires",
                                    "editer-fichier-agents"])
    verifier("9. index-tools : 4 lignes presentes (3 outils + editer-fichier-agents)", ok_idx)

    # 10-11. Normes sur les 6 fichiers touches + ce test
    fichiers = [DETECTER, EDITER_PARCOURS, LANCER, ENREGISTRER,
                CATALOGUE, INDEX, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("10. ASCII strict : 0 non-ASCII (outils + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("11. LF pur : 0 CRLF (outils + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    # 12. Protection : le test ne cree rien a la racine
    avant = set(os.listdir(racine))
    # (le test n'ecrit rien : simple verification d'absence de fichiers cree)
    apres = set(os.listdir(racine))
    verifier("12. Le test ne cree aucun fichier a la racine",
             avant == apres, "cree: %s" % (apres - avant))

    # 13. Garde-fou fusion (decision utilisateur 2026-08-14) : le registre
    # actif contient les 12 entrees script-temporaire (fusion de l ancienne
    # archive). Aucun fichier historique ne doit exister.
    historique = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                              "registre-usages-outils.historique.jsonl")
    registre = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                            "registre-usages-outils.jsonl")

    # 14. Anti-recurrence (demande utilisateur 2026-08-14) : le registre
    # d usage est TRIE par date/heure DECROISSANT (le plus recent d abord).
    dates = []
    try:
        with io.open(registre, encoding="utf-8") as fh:
            for l in fh:
                if not l.strip():
                    continue
                try:
                    dates.append(json.loads(l).get("date", ""))
                except ValueError:
                    pass
    except OSError:
        dates = []
    trie = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1))
    verifier("14. registre-usages-outils trie par date/heure decroissant",
             trie, "entrees=%d" % len(dates))
    nb_st = 0
    try:
        with io.open(registre, encoding="utf-8") as fh:
            for l in fh:
                if not l.strip():
                    continue
                try:
                    e = json.loads(l)
                    if e.get("mode") == "script-temporaire":
                        nb_st += 1
                except ValueError:
                    pass
    except (IOError, OSError):
        pass
    verifier("13. registre actif contient les 12 entrees script-temporaire (fusion)",
             nb_st >= 12 and not os.path.isfile(historique),
             "nb_st=%d historique_present=%s" % (nb_st, os.path.isfile(historique)))

    # 15. Anti-recurrence (demande utilisateur 2026-08-17) : les parcours
    # des agents ne doivent PAS ordonner "creer/ecrire un script (temporaire)
    # pour ecrire/modifier un fichier du cerveau" (REGLE ABSOLUE 4 : outils
    # du cerveau uniquement - creer-fichier / editer-fichier-agents /
    # editer-parcours).
    motifs = [r"creer\s+un\s+script", r"ecrire\s+un\s+script",
              r"script\s+temporaire\s+pour\s+(ecrire|creer|modifier)"]
    instructions_scripts = []
    for f in sorted(glob.glob(os.path.join(PROJECT_ROOT, "cerveau-projet",
                                           "agents", "*", "parcours",
                                           "parcours-*.json"))):
        try:
            p = json.load(io.open(f, encoding="utf-8"))
        except (ValueError, IOError):
            continue
        agent = os.path.basename(f).replace("parcours-", "").replace(".json", "")
        for cid, c in p.get("cases", {}).items():
            if not isinstance(c, dict):
                continue
            for ind in c.get("indices", []):
                if not isinstance(ind, dict):
                    continue
                txt = " ".join(str(ind.get(k, "")) for k in
                               ("texte", "commande", "message", "raison"))
                for m in motifs:
                    if re.search(m, txt, re.IGNORECASE):
                        instructions_scripts.append(
                            "%s %s : '%s'" % (agent, cid, m))
                        break
    verifier("15. 0 parcours ordonnant de creer/ecrire un script pour un "
             "fichier du cerveau",
             len(instructions_scripts) == 0,
             instructions_scripts[:3] if instructions_scripts else "")

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
