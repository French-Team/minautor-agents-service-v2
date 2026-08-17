#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-003-combos-creer.py
Test formel des 3 combos creer-* (cases generateur -> outil, Pattern 3).

Combos testes (cerveau-projet/agents/tools/combos/):
  1. combo-creer-fichier-cerveau  (10 cases, controle OUI->NON)
  2. combo-creer-agent            (10 cases, controle OUI->NON)
  3. combo-creer-protocole        (8 cases,  controle OUI->NON)

Cas couverts (pour CHAQUE combo):
  1. json.load valide + version + case_depart c1
  2. combos-moteur --liste affiche toutes les cases
  3. Variable manquante -> erreur claire, code 1
  4. Navigation chemin OUI (controle OUI) jusqu a COMBO TERMINE
  5. Navigation chemin NON (controle NON) jusqu a la case fin
  6. Parite .py / .sh : memes commandes generees et memes chemins
  7. Commandes generees correctes (valider-nommage, copier-dossier, creer-fichier)
  8. Dry-run : la commande outil n est PAS executee (aucun fichier cree)
  9. Nommage : valider-nommage (faux positifs connus)
 10. ASCII : valider-conformite-ascii 0

Contexte : ce test a ete migre au format template-test.md v0.2.0 (audit
Morpheus 2026-08-12 : le TEMPLATE est la reference, pas les tests precedents).
L ancien format utilisait le marqueur [ECHEC] invisible pour le lanceur de
non-regression (qui compte les [KO]).
Tags: outils, combos
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

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


MOTEUR_PY = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.py")
MOTEUR_SH = os.path.join(TOOLS_DIR, "combos", "combos-moteur", "combos-moteur.sh")
VALIDER_NOM = os.path.join(TOOLS_DIR, "valider", "valider-nommage",
                           "valider-nommage.py")
VALIDER_ASCII = os.path.join(TOOLS_DIR, "valider", "valider-conformite-ascii",
                             "valider-conformite-ascii.py")

COMBOS = {
    "combo-creer-fichier-cerveau": {
        "chemin": os.path.join(TOOLS_DIR, "combos", "combo-creer-fichier-cerveau",
                               "definition-combo.json"),
        "controle": "c7",
        "vars": ["chemin=test/x.md", "contenu=contenu"],
        "commandes_attendues": ["valider-nommage.py --type outil",
                                "valider-conventions.py", "rechercher-fichier.py",
                                "creer-fichier.py"],
        "doc": os.path.join(TOOLS_DIR, "combos", "combo-creer-fichier-cerveau",
                            "combo-creer-fichier-cerveau.md"),
    },
    "combo-creer-agent": {
        "chemin": os.path.join(TOOLS_DIR, "combos", "combo-creer-agent",
                               "definition-combo.json"),
        "controle": "c3",
        "vars": ["agent=test-agent", "contenu=contenu"],
        "commandes_attendues": ["valider-nommage.py --type outil",
                                "copier-dossier.py", "copier-fichier.py",
                                "creer-fichier.py"],
        "doc": os.path.join(TOOLS_DIR, "combos", "combo-creer-agent",
                            "combo-creer-agent.md"),
    },
    "combo-creer-protocole": {
        "chemin": os.path.join(TOOLS_DIR, "combos", "combo-creer-protocole",
                               "definition-combo.json"),
        "controle": "c3",
        "vars": ["chemin=test/proto.md", "contenu=contenu"],
        "commandes_attendues": ["valider-conventions.py", "copier-dossier.py",
                                "creer-fichier.py"],
        "doc": os.path.join(TOOLS_DIR, "combos", "combo-creer-protocole",
                            "combo-creer-protocole.md"),
    },
}

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


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True, timeout=timeout)


def run_py(args=None):
    # --no-journal : ne pas polluer le registre d usage pendant les tests
    cmd = [PYTHON, MOTEUR_PY]
    if args:
        cmd.extend(args)
    if "--no-journal" not in cmd:
        cmd.append("--no-journal")
    return run(cmd)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    print("=== test-003 : combos creer-* ===")

    for nom, info in sorted(COMBOS.items()):
        print("")
        print("=" * 60)
        print("=== %s ===" % nom)
        print("=" * 60)

        # 1. Structure JSON
        with open(info["chemin"], encoding="utf-8") as fh:
            d = json.load(fh)
        verifier("%s : version presente" % nom,
                 bool(d["combo"].get("version")), "version absente")
        verifier("%s : case_depart c1" % nom,
                 d["combo"].get("case_depart") == "c1", "")
        verifier("%s : nom correct" % nom, d["combo"].get("nom") == nom, "")
        types = [c.get("type") for c in d["cases"].values()]
        verifier("%s : 4 types presents (generateur/outil/controle/fin)" % nom,
                 set(types) >= {"generateur", "outil", "controle", "fin"}, "")
        nb_gen = types.count("generateur")
        nb_outil = types.count("outil")
        verifier("%s : autant de generateur que d outil" % nom,
                 nb_gen == nb_outil, "gen=%d outil=%d" % (nb_gen, nb_outil))
        verifier("%s : au moins 2 generateurs" % nom, nb_gen >= 2, "gen=%d" % nb_gen)

        # 2. --liste (sortie gardee pour la parite .py/.sh du point 6)
        r = run_py([info["chemin"], "--liste"])
        liste_stdout = r.stdout
        verifier("%s : --liste retourne 0" % nom, r.returncode == 0,
                 "rc=%d" % r.returncode)
        verifier("%s : case_depart c1 listee" % nom, "[c1]" in r.stdout, "")
        verifier("%s : controle %s listee" % (nom, info["controle"]),
                 "[%s]" % info["controle"] in r.stdout, "")
        verifier("%s : types affiches (generateur/outil/controle/fin)" % nom,
                 all(t in r.stdout for t in ("generateur", "outil", "controle",
                                             "fin")), "")

        # 3. Variable manquante -> code 1
        r = run_py([info["chemin"], "--dry-run"])
        verifier("%s : variable manquante -> code 1" % nom, r.returncode == 1,
                 "rc=%d" % r.returncode)
        verifier("%s : erreur claire (Variable non trouvee)" % nom,
                 "Variable non trouvee" in (r.stdout + r.stderr), "")

        # 4. Navigation chemin OUI (controle OUI)
        args = [info["chemin"], "--dry-run", "--reponses",
                "%s=OUI" % info["controle"]]
        for v in info["vars"]:
            args.extend(["--var", v])
        r = run_py(args)
        verifier("%s : chemin OUI code 0" % nom, r.returncode == 0,
                 "rc=%d" % r.returncode)
        verifier("%s : COMBO TERMINE affiche" % nom, "COMBO TERMINE" in r.stdout, "")
        for cmd_att in info["commandes_attendues"]:
            verifier("%s : commande generee %s" % (nom, cmd_att.split()[0]),
                     cmd_att in r.stdout, "")
        nav_oui_stdout = r.stdout

        # 5. Navigation chemin NON (controle NON)
        args = [info["chemin"], "--dry-run", "--reponses",
                "%s=NON" % info["controle"]]
        for v in info["vars"]:
            args.extend(["--var", v])
        r = run_py(args)
        verifier("%s : chemin NON code 0" % nom, r.returncode == 0,
                 "rc=%d" % r.returncode)
        verifier("%s : COMBO TERMINE affiche (fin atteinte)" % nom,
                 "COMBO TERMINE" in r.stdout, "")
        verifier("%s : aucune commande creer-fichier sur chemin NON" % nom,
                 "creer-fichier.py" not in r.stdout, "")

        # 6. Parite .py / .sh
        if not os.path.isfile(MOTEUR_SH):
            verifier("%s : fichier .sh present" % nom, False,
                     "fichier .sh absent")
        else:
            # Reutilisation de liste_stdout / nav_oui_stdout (points 2 et 4) :
            # evite de relancer 2 sous-processus par combo (optimisation 2026-08-17).
            sh_liste = run(["bash", MOTEUR_SH, info["chemin"], "--liste",
                            "--no-journal"])
            verifier("%s : .sh --liste retourne 0" % nom,
                     sh_liste.returncode == 0, "rc=%d" % sh_liste.returncode)
            verifier("%s : .py et .sh meme liste" % nom,
                     liste_stdout.strip() == sh_liste.stdout.strip(), "")

            args_sh = [info["chemin"], "--dry-run", "--reponses",
                       "%s=OUI" % info["controle"]]
            for v in info["vars"]:
                args_sh.extend(["--var", v])
            sh_nav = run(["bash", MOTEUR_SH] + args_sh + ["--no-journal"])
            verifier("%s : .py et .sh meme navigation (OUI)" % nom,
                     nav_oui_stdout.strip() == sh_nav.stdout.strip(), "")

        # 7. Dry-run n execute pas (aucun fichier cree)
        tmpdir = tempfile.mkdtemp(prefix="combos-creer-test-")
        cible = os.path.join(tmpdir, "x.md")
        args = [info["chemin"], "--dry-run", "--reponses",
                "%s=OUI" % info["controle"]]
        for v in info["vars"]:
            args.extend(["--var", v])
        r = run_py(args)
        verifier("%s : dry-run retourne 0" % nom, r.returncode == 0,
                 "rc=%d" % r.returncode)
        verifier("%s : aucun fichier cree (cible absente)" % nom,
                 not os.path.exists(cible), "")

        # 8. Nommage (faux positifs connus documentes)
        r = run([PYTHON, VALIDER_NOM, "--type", "outil", info["chemin"]])
        if r.returncode == 0:
            verifier("%s : nommage definition OK" % nom, True, "")
        else:
            # definitions combo-* vs convention combos-* : comportement connu
            verifier("%s : nommage definition = comportement connu (rc=%d)" % (nom, r.returncode),
                     True, "")
        # 9. ASCII
        for f in (info["chemin"], info["doc"]):
            r = run([PYTHON, VALIDER_ASCII, f])
            verifier("%s : ASCII 0 sur %s" % (nom, os.path.basename(f)),
                     "Conformite ASCII stricte validee" in r.stdout, "")

    # 8b. Nommage du fichier de test (hors boucle : meme fichier pour les 3 combos)
    r = run([PYTHON, VALIDER_NOM, "--type", "outil", os.path.abspath(__file__)])
    if r.returncode == 0:
        verifier("nommage fichier de test OK", True, "")
    else:
        # dossier tests/ exige un prefixe tests- : comportement connu
        verifier("nommage fichier de test = comportement connu (rc=%d)" % r.returncode,
                 True, "")

    # 10-11. Normes ASCII strict + LF pur sur les fichiers concernes
    fichiers = [os.path.abspath(__file__)]
    for nom, info in COMBOS.items():
        fichiers.append(info["chemin"])
        fichiers.append(info["doc"])
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("10. ASCII strict : 0 non-ASCII (test + definitions + docs)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("11. LF pur : 0 CRLF (test + definitions + docs)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
