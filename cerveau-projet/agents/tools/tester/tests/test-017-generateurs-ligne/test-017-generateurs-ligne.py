#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-017-generateurs-ligne.py
Test formel de l'outil generateurs-ligne v0.3.0 (categorie generateurs/).

Outil teste (cerveau-projet/agents/tools/generateurs/generateurs-ligne/):
  .py + .sh (wrapper pur exec python3) + .md + spec/ + gabarits-ligne.json
  Ajoute une LIGNE (chemin de bout en bout) a une carte de decision via des
  gabarits de groupes de cases (configs EXTERNALISEES dans gabarits-ligne.json,
  extensibles via ajouter-config). Verifie la carte Atlas avant edition
  (existence + mtime), dry/wet pour valider.

Cas couverts:
  1. --version py/sh identiques v0.3.0 (parite)
  2. --aide : 6 sous-commandes (verifier, lister-configs, config, ajouter, ajouter-config, copier)
  3. verifier : carte A JOUR (existence + mtime recent)
  4. verifier : carte ABSENTE -> CARTE A REGENERER
  5. verifier : carte PERIMEE (mtime plus ancien que le parcours)
  6. lister-configs : 4 configs lues depuis gabarits-ligne.json
  7. config <nom> : detail du gabarit
  8. ajouter config defaut --dry-run : aucune modification
  9. ajouter config defaut (wet) : bloc cree + branche ajoutee + CONFORME
 10. ajouter config-1 (wet) : deviation + rejoint (Pattern 7)
 11. ajouter config-2 (wet) : controle RVAV OUI/NON
 12. ajouter config-3 (wet) : action simple, enchainement
 13. ajouter SANS carte a jour : BLOQUE + invite a activer Atlas
 14. ajouter --force : passe outre le blocage carte
 15. ids conformes c<numero>[a-z]? (aucun point)
 16. Protection : aucun fichier residuel dans le workspace apres les tests
 17. ajouter-config --dry-run : config test simulee, JSON inchange
 18. ajouter-config (wet) : config ajoutee, lister-configs la liste, JSON trie
 19. ajouter --config <nouvelle config> : bloc reel CONFORME
 20. gabarit invalide rejete (branche unique) + nom deja existant rejete sans --force
 21. nettoyage : gabarits-ligne.json restaure a 4 configs
 22. ASCII strict : 0 non-ASCII (5 fichiers outils + test)

Usage:
  python3 test-017-generateurs-ligne.py
Tags: outils, generateurs, ligne
"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

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


OUTIL_DIR = os.path.join(TOOLS_DIR, "generateurs", "generateurs-ligne")
OUTIL_PY = os.path.join(OUTIL_DIR, "generateurs-ligne.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "generateurs-ligne.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "generateurs-ligne.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-generateurs-ligne.001.01.ebauche.md")
OUTIL_GABARITS = os.path.join(OUTIL_DIR, "gabarits-ligne.json")
PARCOURS_SRC = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "buffy",
                            "parcours", "parcours-buffy.json")
VALIDER_CASE = os.path.join(TOOLS_DIR, "valider", "valider-case", "valider-case.py")

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


def run(cmd, timeout=90):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def creer_parcours_test(tmp, nom="scenario-ajout"):
    """Copie un parcours reel dans un SOUS-DOSSIER dedie de tmp et fabrique
    une carte a jour dans CE dossier (isole les scenarios entre eux)."""
    sous = os.path.join(tmp, nom)
    os.makedirs(sous, exist_ok=True)
    dst = os.path.join(sous, "parcours-test.json")
    shutil.copy(PARCOURS_SRC, dst)
    with io.open(dst, encoding="utf-8") as fh:
        d = json.load(fh)
    agent = d["parcours"]["agent"]
    carto = os.path.join(sous, "cartographie-%s.md" % agent)
    with io.open(carto, "w", encoding="utf-8") as fh:
        fh.write("# Cartographie factice de test\n")
    m_parc = os.path.getmtime(dst)
    os.utime(carto, (m_parc + 5, m_parc + 5))
    return dst, carto


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-017-")
    try:
        print("=== Test formel generateurs-ligne v0.3.0 ===")

        # 1. Parite --version
        r_py = run([PYTHON, OUTIL_PY, "--version"])
        r_sh = run(["bash", OUTIL_SH, "--version"])
        verifier("1. --version py/sh identiques v0.3.0",
                 r_py.returncode == 0 and r_sh.returncode == 0
                 and "v0.3.0" in r_py.stdout
                 and r_py.stdout.strip() == r_sh.stdout.strip(),
                 "py=%r sh=%r" % (r_py.stdout.strip(), r_sh.stdout.strip()))

        # 2. --aide : sous-commandes racine + options des sous-parsers
        r_aide = run([PYTHON, OUTIL_PY, "--aide"])
        r_add_help = run([PYTHON, OUTIL_PY, "ajouter", "--help"])
        r_acfg_help = run([PYTHON, OUTIL_PY, "ajouter-config", "--help"])
        r_cop_help = run([PYTHON, OUTIL_PY, "copier", "--help"])
        verifier("2a. --aide affiche les 6 sous-commandes",
                 r_aide.returncode == 0
                 and all(opt in r_aide.stdout for opt in
                         ("verifier", "lister-configs", "config", "ajouter",
                          "ajouter-config", "copier")),
                 r_aide.stdout.strip()[-150:])
        verifier("2d. copier --help affiche --source/--mode/--branche",
                 r_cop_help.returncode == 0
                 and "--source" in r_cop_help.stdout
                 and "--mode" in r_cop_help.stdout
                 and "--branche" in r_cop_help.stdout,
                 r_cop_help.stdout.strip()[-150:])
        verifier("2b. ajouter --help affiche --dry-run et --force",
                 r_add_help.returncode == 0
                 and "--dry-run" in r_add_help.stdout
                 and "--force" in r_add_help.stdout,
                 r_add_help.stdout.strip()[-150:])
        verifier("2c. ajouter-config --help affiche --description et --gabarit",
                 r_acfg_help.returncode == 0
                 and "--description" in r_acfg_help.stdout
                 and "--gabarit" in r_acfg_help.stdout,
                 r_acfg_help.stdout.strip()[-150:])

        # 3. verifier : carte A JOUR
        dst, carto = creer_parcours_test(tmp, "scenario-verifier")
        r_ver = run([PYTHON, OUTIL_PY, "verifier", dst])
        verifier("3. verifier : carte A JOUR (existence + mtime)",
                 r_ver.returncode == 0 and "CARTE A JOUR" in r_ver.stdout,
                 r_ver.stdout.strip()[:120])

        # 4. verifier : carte ABSENTE (dossier distinct)
        tmp_abs = os.path.join(tmp, "scenario-abs")
        os.makedirs(tmp_abs)
        dst2 = os.path.join(tmp_abs, "parcours-abs.json")
        shutil.copy(PARCOURS_SRC, dst2)
        r_abs = run([PYTHON, OUTIL_PY, "verifier", dst2])
        verifier("4. verifier : carte ABSENTE -> CARTE A REGENERER",
                 r_abs.returncode == 1 and "CARTE A REGENERER" in r_abs.stdout
                 and "cartographie-" in r_abs.stdout,
                 r_abs.stdout.strip()[:120])

        # 5. verifier : carte PERIMEE (dossier distinct, mtime plus ancien)
        tmp_per = os.path.join(tmp, "scenario-perime")
        os.makedirs(tmp_per)
        dst3 = os.path.join(tmp_per, "parcours-perime.json")
        shutil.copy(PARCOURS_SRC, dst3)
        with io.open(dst3, encoding="utf-8") as fh:
            d3 = json.load(fh)
        agent3 = d3["parcours"]["agent"]
        carto3 = os.path.join(tmp_per, "cartographie-%s.md" % agent3)
        with io.open(carto3, "w", encoding="utf-8") as fh:
            fh.write("# carto perimee\n")
        m_parc3 = os.path.getmtime(dst3)
        os.utime(carto3, (m_parc3 - 100, m_parc3 - 100))  # plus ancienne
        r_per = run([PYTHON, OUTIL_PY, "verifier", dst3])
        verifier("5. verifier : carte PERIMEE -> CARTE A REGENERER",
                 r_per.returncode == 1 and "CARTE A REGENERER" in r_per.stdout,
                 r_per.stdout.strip()[:120])

        # 6. lister-configs : 4 configs lues depuis gabarits-ligne.json
        r_list = run([PYTHON, OUTIL_PY, "lister-configs"])
        gab_json = json.load(io.open(OUTIL_GABARITS, encoding="utf-8"))
        verifier("6. lister-configs : 4 configs depuis gabarits-ligne.json",
                 r_list.returncode == 0
                 and all(c in r_list.stdout for c in
                         ("defaut", "config-1", "config-2", "config-3"))
                 and set(gab_json["gabarits"].keys()) >= {"defaut", "config-1",
                                                           "config-2", "config-3"},
                 r_list.stdout.strip()[:120])

        # 7. config <nom>
        r_cfg = run([PYTHON, OUTIL_PY, "config", "config-1"])
        verifier("7. config config-1 : detail du gabarit (deviation + rejoint)",
                 r_cfg.returncode == 0 and "DEVIATION" in r_cfg.stdout
                 and "REJOINT" in r_cfg.stdout,
                 r_cfg.stdout.strip()[:120])

        # 8-12. Scenarios d'ajout : UN SOUS-DOSSIER PROPRE par config
        #       (la carte a jour est recreee dans chaque dossier -> isole)
        dst8, _carto8 = creer_parcours_test(tmp, "scenario-defaut")
        nb_avant = len(json.load(io.open(dst8, encoding="utf-8"))["cases"])
        r_dry = run([PYTHON, OUTIL_PY, "ajouter", dst8, "--config", "defaut",
                     "--point-attache", "c1", "--reponse", "ligne",
                     "--rejoint", "c8", "--dry-run"])
        nb_apres = len(json.load(io.open(dst8, encoding="utf-8"))["cases"])
        verifier("8. ajouter --dry-run : DRY-RUN affiche, aucun fichier modifie",
                 r_dry.returncode == 0 and "DRY-RUN" in r_dry.stdout
                 and nb_avant == nb_apres,
                 "avant=%d apres=%d | %s" % (nb_avant, nb_apres, r_dry.stdout.strip()[-120:]))

        # 9. ajouter config defaut (wet) : bloc + branche + CONFORME
        r_wet = run([PYTHON, OUTIL_PY, "ajouter", dst8, "--config", "defaut",
                     "--point-attache", "c1", "--reponse", "ligne",
                     "--rejoint", "c8"], timeout=120)
        d_apres = json.load(io.open(dst8, encoding="utf-8"))
        nouvelles = [k for k in d_apres["cases"] if k not in json.load(
            io.open(PARCOURS_SRC, encoding="utf-8"))["cases"]]
        branche_ligne = any(b.get("reponse") == "ligne"
                            for b in d_apres["cases"]["c1"].get("branches", []))
        verifier("9a. ajouter defaut (wet) : bloc cree (4 cases) + validation",
                 r_wet.returncode == 0 and "[OK]" in r_wet.stdout
                 and len(nouvelles) == 4,
                 "nouvelles=%s | %s" % (nouvelles, r_wet.stdout.strip()[-120:]))
        verifier("9b. Branche 'ligne' ajoutee sur c1",
                 branche_ligne, str(d_apres["cases"]["c1"].get("branches")))
        verifier("9c. Validation auto : CONFORME (0 erreur)",
                 "[OK] valider-case : conforme" in r_wet.stdout and "erreurs: 0" in r_wet.stdout,
                 r_wet.stdout.strip()[-120:])

        # 10. ajouter config-1 (wet) : deviation + rejoint
        #    point d attache : c0 (action avec suivant, depuis la migration
        #    relecture c0b est devenue une question sans suivant)
        dst10, _c10 = creer_parcours_test(tmp, "scenario-config1")
        d_base = json.load(io.open(dst10, encoding="utf-8"))
        r_c1 = run([PYTHON, OUTIL_PY, "ajouter", dst10, "--config", "config-1",
                    "--point-attache", "c0"], timeout=120)
        d_c1 = json.load(io.open(dst10, encoding="utf-8"))
        nouvelles1 = [k for k in d_c1["cases"] if k not in d_base["cases"]]
        verifier("10a. ajouter config-1 : 5 cases (decision + deviation + rejoint)",
                 r_c1.returncode == 0 and len(nouvelles1) == 5,
                 "nouvelles=%s | %s" % (nouvelles1, r_c1.stdout.strip()[-120:]))
        verifier("10b. Suivant de c0 recable vers la 1re case de la ligne",
                 d_c1["cases"]["c0"].get("suivant") != "c0b",
                 "suivant=%s" % d_c1["cases"]["c0"].get("suivant"))
        verifier("10c. config-1 : CONFORME",
                 "[OK] valider-case : conforme" in r_c1.stdout, r_c1.stdout.strip()[-120:])

        # 11. ajouter config-2 (wet) : controle RVAV
        dst11, _c11 = creer_parcours_test(tmp, "scenario-config2")
        d_base = json.load(io.open(dst11, encoding="utf-8"))
        r_c2 = run([PYTHON, OUTIL_PY, "ajouter", dst11, "--config", "config-2",
                    "--point-attache", "c1", "--reponse", "rvav",
                    "--rejoint", "c8"], timeout=120)
        d_c2 = json.load(io.open(dst11, encoding="utf-8"))
        nouvelles2 = [k for k in d_c2["cases"] if k not in d_base["cases"]]
        verifier("11a. ajouter config-2 : 4 cases (controle RVAV)",
                 r_c2.returncode == 0 and len(nouvelles2) == 4,
                 "nouvelles=%s | %s" % (nouvelles2, r_c2.stdout.strip()[-120:]))
        verifier("11b. config-2 : CONFORME",
                 "[OK] valider-case : conforme" in r_c2.stdout, r_c2.stdout.strip()[-120:])

        # 12. ajouter config-3 (wet) : action simple
        dst12, _c12 = creer_parcours_test(tmp, "scenario-config3")
        d_base = json.load(io.open(dst12, encoding="utf-8"))
        r_c3 = run([PYTHON, OUTIL_PY, "ajouter", dst12, "--config", "config-3",
                    "--point-attache", "c0"], timeout=120)
        d_c3 = json.load(io.open(dst12, encoding="utf-8"))
        nouvelles3 = [k for k in d_c3["cases"] if k not in d_base["cases"]]
        verifier("12a. ajouter config-3 : 2 cases (action + rejoint)",
                 r_c3.returncode == 0 and len(nouvelles3) == 2,
                 "nouvelles=%s | %s" % (nouvelles3, r_c3.stdout.strip()[-120:]))
        verifier("12b. config-3 : CONFORME",
                 "[OK] valider-case : conforme" in r_c3.stdout, r_c3.stdout.strip()[-120:])

        # 13. ajouter SANS carte a jour : BLOQUE + invite Atlas (dossier propre)
        tmp_bloc = os.path.join(tmp, "scenario-bloque")
        os.makedirs(tmp_bloc)
        dst_bloc = os.path.join(tmp_bloc, "parcours-bloque.json")
        shutil.copy(PARCOURS_SRC, dst_bloc)
        r_bloc = run([PYTHON, OUTIL_PY, "ajouter", dst_bloc, "--config", "defaut"])
        verifier("13. ajouter sans carte : BLOQUE + invite a activer Atlas",
                 r_bloc.returncode != 0 and "CARTE A REGENERER" in r_bloc.stdout
                 and "Atlas" in r_bloc.stdout,
                 r_bloc.stdout.strip()[:150])

        # 14. ajouter --force : passe outre
        r_force = run([PYTHON, OUTIL_PY, "ajouter", dst_bloc, "--config",
                       "config-3", "--point-attache", "c0", "--force"],
                      timeout=120)
        verifier("14. --force passe outre le blocage carte",
                 r_force.returncode == 0 and "[OK]" in r_force.stdout,
                 r_force.stdout.strip()[:150])

        # 15. ids conformes c<numero>[a-z]? (verifie sur les 4 scenarios d ajout)
        mauvais_ids = []
        for f in (dst8, dst10, dst11, dst12):
            d_fin = json.load(io.open(f, encoding="utf-8"))
            mauvais_ids += [k for k in d_fin["cases"]
                            if "." in k or not k.startswith("c")]
        verifier("15. Ids des cases conformes c<numero>[a-z]? (aucun point)",
                 not mauvais_ids, "; ".join(mauvais_ids[:5]))

        # 16. ajouter-config : dry-run puis wet avec un gabarit externe de test
        #     (config-4 : decision + 2 branches + rejoint, structure JSON externe)
        gabarit_test = os.path.join(tmp, "gabarit-config-4.json")
        with io.open(gabarit_test, "w", encoding="ascii") as fh:
            json.dump({"cases": [
                {"suffixe": "", "type": "question", "titre": "CHOIX A FAIRE ?",
                 "branches": [["OUI", ".1"], ["NON", ".2"]], "suivant": None},
                {"suffixe": ".1", "type": "action", "titre": "Choix A",
                 "branches": [], "suivant": "REJOINT"},
                {"suffixe": ".2", "type": "action", "titre": "Choix B",
                 "branches": [], "suivant": "REJOINT"},
                {"suffixe": "REJOINT", "type": "action",
                 "titre": "REJOINT - retour au flux principal",
                 "branches": [], "suivant": "REJOINT"},
            ]}, fh, ensure_ascii=True, indent=2)
        r_acfg_dry = run([PYTHON, OUTIL_PY, "ajouter-config", "config-4",
                          "--description", "Config 4 de test (decision binaire)",
                          "--gabarit", gabarit_test, "--dry-run"])
        nb_gab_avant = len(json.load(io.open(OUTIL_GABARITS, encoding="utf-8"))["gabarits"])
        verifier("16a. ajouter-config --dry-run : DRY-RUN affiche, JSON inchange",
                 r_acfg_dry.returncode == 0 and "DRY-RUN" in r_acfg_dry.stdout
                 and "config-4" in r_acfg_dry.stdout and nb_gab_avant == 4,
                 r_acfg_dry.stdout.strip()[-150:])

        # 16b. ajouter-config (wet)
        r_acfg_wet = run([PYTHON, OUTIL_PY, "ajouter-config", "config-4",
                          "--description", "Config 4 de test (decision binaire)",
                          "--gabarit", gabarit_test])
        gab_apres = json.load(io.open(OUTIL_GABARITS, encoding="utf-8"))
        verifier("16b. ajouter-config (wet) : [OK] + config-4 presente (5 configs, JSON trie)",
                 r_acfg_wet.returncode == 0 and "OK" in r_acfg_wet.stdout
                 and "config-4" in gab_apres["gabarits"]
                 and len(gab_apres["gabarits"]) == 5
                 and list(gab_apres["gabarits"].keys()) == sorted(gab_apres["gabarits"].keys()),
                 r_acfg_wet.stdout.strip()[-150:])
        verifier("16c. lister-configs affiche maintenant 5 configs (dont config-4)",
                 "config-4" in run([PYTHON, OUTIL_PY, "lister-configs"]).stdout,
                 run([PYTHON, OUTIL_PY, "lister-configs"]).stdout.strip()[:120])

        # 16d. ajouter --config config-4 : bloc reel CONFORME
        dst16, _c16 = creer_parcours_test(tmp, "scenario-config4")
        d_base = json.load(io.open(dst16, encoding="utf-8"))
        r_c4 = run([PYTHON, OUTIL_PY, "ajouter", dst16, "--config", "config-4",
                    "--point-attache", "c1", "--reponse", "cfg4",
                    "--rejoint", "c8"], timeout=120)
        d_c4 = json.load(io.open(dst16, encoding="utf-8"))
        nouvelles4 = [k for k in d_c4["cases"] if k not in d_base["cases"]]
        verifier("16d. ajouter --config config-4 : bloc cree (4 cases) + CONFORME",
                 r_c4.returncode == 0 and len(nouvelles4) == 4 and "[OK] valider-case : conforme" in r_c4.stdout,
                 "nouvelles=%s | %s" % (nouvelles4, r_c4.stdout.strip()[-150:]))

        # 16e. gabarit invalide (branche unique) rejete
        gabarit_inv = os.path.join(tmp, "gabarit-invalide.json")
        with io.open(gabarit_inv, "w", encoding="ascii") as fh:
            json.dump({"cases": [
                {"suffixe": "", "type": "question", "titre": "CHOIX ?",
                 "branches": [["OUI", ".1"]], "suivant": None},
                {"suffixe": "REJOINT", "type": "action", "titre": "REJOINT",
                 "branches": [], "suivant": "REJOINT"},
            ]}, fh, ensure_ascii=True)
        r_inv = run([PYTHON, OUTIL_PY, "ajouter-config", "config-5",
                     "--description", "Config invalide", "--gabarit", gabarit_inv])
        verifier("16e. gabarit invalide (branche unique) rejete",
                 r_inv.returncode != 0
                 and "au moins 2 branches" in (r_inv.stdout + r_inv.stderr),
                 (r_inv.stdout + r_inv.stderr).strip()[-150:])

        # 16f. nom deja existant rejete sans --force
        r_conf = run([PYTHON, OUTIL_PY, "ajouter-config", "config-4",
                      "--description", "Doublon", "--gabarit", gabarit_test])
        verifier("16f. config-4 deja existante : rejetee sans --force",
                 r_conf.returncode != 0
                 and "existe deja" in (r_conf.stdout + r_conf.stderr),
                 (r_conf.stdout + r_conf.stderr).strip()[-150:])

        # 16g. nettoyage : retirer config-4 -> gabarits-ligne.json restaure a 4 configs
        del gab_apres["gabarits"]["config-4"]
        with io.open(OUTIL_GABARITS, "w", encoding="ascii", newline="\n") as fh:
            json.dump(gab_apres, fh, ensure_ascii=True, indent=2)
            fh.write("\n")
        verifier("16g. nettoyage : gabarits-ligne.json restaure a 4 configs",
                 len(json.load(io.open(OUTIL_GABARITS, encoding="utf-8"))["gabarits"]) == 4,
                 "nb=%d" % len(json.load(io.open(OUTIL_GABARITS, encoding="utf-8"))["gabarits"]))

        # 17. copier : detection du groupe depuis une case source (mode complet)
        #     Preparation : ajouter une ligne config-1 (deviation) sur c10b
        dst17, _c17 = creer_parcours_test(tmp, "scenario-copier")
        r_prep = run([PYTHON, OUTIL_PY, "ajouter", dst17, "--config", "config-1",
                      "--point-attache", "c10b", "--reponse", "ligneA",
                      "--rejoint", "c11"], timeout=120)
        d_prep = json.load(io.open(dst17, encoding="utf-8"))
        source = None
        for k, c in d_prep["cases"].items():
            for b in c.get("branches", []):
                if b.get("reponse") == "ligneA":
                    source = b["vers"]
        verifier("17a. preparation : ligne config-1 creee + case source identifiee",
                 r_prep.returncode == 0 and source is not None,
                 "source=%s | %s" % (source, r_prep.stdout.strip()[-80:]))

        # 17b. copier --dry-run
        nb_avant = len(json.load(io.open(dst17, encoding="utf-8"))["cases"])
        r_cop_dry = run([PYTHON, OUTIL_PY, "copier", dst17, "--source", source,
                         "--mode", "complet", "--point-attache", "c10c",
                         "--reponse", "ligneB", "--rejoint", "c11", "--dry-run"])
        nb_apres = len(json.load(io.open(dst17, encoding="utf-8"))["cases"])
        verifier("17b. copier --dry-run : DRY-RUN affiche, aucun fichier modifie",
                 r_cop_dry.returncode == 0 and "DRY-RUN" in r_cop_dry.stdout
                 and nb_avant == nb_apres,
                 "avant=%d apres=%d | %s" % (nb_avant, nb_apres, r_cop_dry.stdout.strip()[-100:]))

        # 17c. copier (wet) : clone de 4 cases + CONFORME + ids sans doublon
        r_cop = run([PYTHON, OUTIL_PY, "copier", dst17, "--source", source,
                     "--mode", "complet", "--point-attache", "c10c",
                     "--reponse", "ligneB", "--rejoint", "c11"], timeout=120)
        d_cop = json.load(io.open(dst17, encoding="utf-8"))
        nouvelles_cop = [k for k in d_cop["cases"] if k not in d_prep["cases"]]
        verifier("17c. copier (wet) : [OK] + clone de 4 cases + CONFORME",
                 r_cop.returncode == 0 and "[OK]" in r_cop.stdout
                 and len(nouvelles_cop) == 4 and "[OK] valider-case : conforme" in r_cop.stdout,
                 "nouvelles=%s | %s" % (nouvelles_cop, r_cop.stdout.strip()[-120:]))
        verifier("17d. copier : ids conformes c<numero>[a-z]? sans doublon",
                 all("." not in k and k.startswith("c") for k in nouvelles_cop)
                 and len(set(nouvelles_cop)) == len(nouvelles_cop),
                 str(nouvelles_cop))

        # 17e. copier --config (gabarit) : clone de 4 cases + CONFORME
        d_base17 = json.load(io.open(dst17, encoding="utf-8"))
        r_copcfg = run([PYTHON, OUTIL_PY, "copier", dst17, "--config", "config-2",
                        "--point-attache", "c0b", "--reponse", "rvavB",
                        "--rejoint", "c0c"], timeout=120)
        d_copcfg = json.load(io.open(dst17, encoding="utf-8"))
        nouvelles_cfg = [k for k in d_copcfg["cases"] if k not in d_base17["cases"]]
        verifier("17e. copier --config config-2 : clone de 4 cases + CONFORME",
                 r_copcfg.returncode == 0 and len(nouvelles_cfg) == 4
                 and "[OK] valider-case : conforme" in r_copcfg.stdout,
                 "nouvelles=%s | %s" % (nouvelles_cfg, r_copcfg.stdout.strip()[-120:]))

        # 17f. copier --mode branche (decision du clone) + --mode suite
        dec_cop = None
        for k, c in d_copcfg["cases"].items():
            if "TRAITEMENT PRINCIPAL OU DEVIATION" in c.get("titre", ""):
                dec_cop = k
                break
        r_br = run([PYTHON, OUTIL_PY, "copier", dst17, "--source", dec_cop,
                    "--mode", "branche", "--branche", "OUI", "--point-attache", "c0b",
                    "--reponse", "bOUI", "--rejoint", "c0c", "--dry-run"])
        act_cop = None
        for k, c in d_copcfg["cases"].items():
            if "DEVIATION : workflow secondaire" in c.get("titre", ""):
                act_cop = k
                break
        r_su = run([PYTHON, OUTIL_PY, "copier", dst17, "--source", act_cop,
                    "--mode", "suite", "--point-attache", "c0b",
                    "--reponse", "suiteB", "--rejoint", "c0c", "--dry-run"])
        verifier("17f. copier --mode branche + --mode suite : dry-run OK",
                 r_br.returncode == 0 and "DRY-RUN" in r_br.stdout
                 and r_su.returncode == 0 and "DRY-RUN" in r_su.stdout,
                 "branche=%s suite=%s" % (r_br.stdout.strip()[-60:], r_su.stdout.strip()[-60:]))

        # 17g. copier sans carte a jour : BLOQUE + invite Atlas ; --force passe outre
        tmp_bloc2 = os.path.join(tmp, "scenario-copier-bloque")
        os.makedirs(tmp_bloc2)
        dst_bloc2 = os.path.join(tmp_bloc2, "parcours-copier-bloque.json")
        shutil.copy(PARCOURS_SRC, dst_bloc2)
        r_bloc2 = run([PYTHON, OUTIL_PY, "copier", dst_bloc2, "--source", "c10b",
                       "--mode", "suite"])
        verifier("17g. copier sans carte : BLOQUE + invite Atlas",
                 r_bloc2.returncode != 0 and "CARTE A REGENERER" in r_bloc2.stdout
                 and "Atlas" in r_bloc2.stdout,
                 r_bloc2.stdout.strip()[:120])
        r_force2 = run([PYTHON, OUTIL_PY, "copier", dst_bloc2, "--source", "c10b",
                        "--mode", "suite", "--point-attache", "c10c", "--reponse", "vB",
                        "--rejoint", "c11", "--force"], timeout=120)
        verifier("17h. copier --force : passe outre",
                 r_force2.returncode == 0 and "[OK]" in r_force2.stdout,
                 r_force2.stdout.strip()[:120])

        # 18. Protection : aucun residuel dans le workspace apres les tests
        #     (le test travaille uniquement dans tmp/)
        restants = []
        for root, _dirs, files in os.walk(PROJECT_ROOT):
            if ".git" in root or "test-017" in root:
                continue
            for f in files:
                if f.startswith("cartographie-") or f.startswith("parcours-test"):
                    rel = os.path.relpath(os.path.join(root, f), PROJECT_ROOT)
                    if not rel.startswith(os.path.join("cerveau-projet", "agents",
                                                       "tools", "tester", "tests")):
                        restants.append(rel)
        verifier("20. Protection : aucun fichier residuel dans le workspace",
                 not restants, "; ".join(restants[:5]))

        # 21. ASCII strict : 0 non-ASCII (5 fichiers outils + test)
        total_non_ascii = (ascii_count(OUTIL_PY) + ascii_count(OUTIL_SH)
                           + ascii_count(OUTIL_MD) + ascii_count(OUTIL_SPEC)
                           + ascii_count(OUTIL_GABARITS)
                           + ascii_count(os.path.abspath(__file__)))
        verifier("21. ASCII strict : 0 non-ASCII (5 fichiers outils + test)",
                 total_non_ascii == 0, "total = %d" % total_non_ascii)

        print("")
        bilan_chrono()
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
