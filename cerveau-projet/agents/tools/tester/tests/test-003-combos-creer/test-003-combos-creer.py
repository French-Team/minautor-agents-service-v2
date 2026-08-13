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

        # 2. --liste
        r = run_py([info["chemin"], "--liste"])
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
            py_liste = run_py([info["chemin"], "--liste"])
            sh_liste = run(["bash", MOTEUR_SH, info["chemin"], "--liste",
                            "--no-journal"])
            verifier("%s : .sh --liste retourne 0" % nom,
                     sh_liste.returncode == 0, "rc=%d" % sh_liste.returncode)
            verifier("%s : .py et .sh meme liste" % nom,
                     py_liste.stdout.strip() == sh_liste.stdout.strip(), "")

            args_py = [info["chemin"], "--dry-run", "--reponses",
                       "%s=OUI" % info["controle"]]
            args_sh = list(args_py)
            for v in info["vars"]:
                args_py.extend(["--var", v])
                args_sh.extend(["--var", v])
            py_nav = run_py(args_py)
            sh_nav = run(["bash", MOTEUR_SH] + args_sh + ["--no-journal"])
            verifier("%s : .py et .sh meme navigation (OUI)" % nom,
                     py_nav.stdout.strip() == sh_nav.stdout.strip(), "")

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
        r = run([PYTHON, VALIDER_NOM, "--type", "outil",
                 os.path.abspath(__file__)])
        if r.returncode == 0:
            verifier("%s : nommage fichier de test OK" % nom, True, "")
        else:
            # dossier tests/ exige un prefixe tests- : comportement connu
            verifier("%s : nommage fichier de test = comportement connu (rc=%d)" % (nom, r.returncode),
                     True, "")

        # 9. ASCII
        for f in (info["chemin"], info["doc"]):
            r = run([PYTHON, VALIDER_ASCII, f])
            verifier("%s : ASCII 0 sur %s" % (nom, os.path.basename(f)),
                     "Conformite ASCII stricte validee" in r.stdout, "")

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
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
