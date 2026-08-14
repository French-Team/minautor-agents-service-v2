#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-050-triplet-outils-temporaires.py
GARDE-FOU : le triplet (protections + options on/off + chrono) est generalise
dans les OUTILS TEMPORAIRES. generateurs-outil-temporaire v0.2.1 genere des
scripts qui embarquent le meme triplet que le template-test v0.3.0.

Contexte (demande utilisateur 2026-08-14 "generaliser les protections et les
chrono dans les outils temporaires") :
  - Avant : le template genere etait un simple main() sans protections ni
    chrono - un script temporaire pouvait tourner sans dry-run, sans options
    on/off, sans mesure de duree.
  - Maintenant : generateurs-outil-temporaire v0.2.1 integre le triplet + le
    bloc DECLARATION USAGES dans
    le template genere (verifier_nommage, --dry-run, --isoler, --desactiver,
    --no-chrono, chrono_etape, bilan_chrono).
  - Le protocole-creation-scripts-temporaires v0.2.6 impose la REGLE TRIPLET :
    un outil temporaire SANS triplet doit etre regenere avec le generateur.

Cas couverts:
  1. Le generateur est v0.2.1 (--version)
  2. Le template dans le code contient point_actif / chrono_etape / bilan_chrono
  3. Le template contient les options --isoler / --desactiver / --no-chrono / --dry-run
  4. PREUVE REELLE : generation d un outil temporaire -> le script genere
     embarque le triplet et s execute (chrono affiche)
  5. --dry-run du script genere : aucune action reelle
  6. --isoler N du script genere : fonction isolee
  7. --no-chrono du script genere : chrono coupe
  8. Le protocole-creation-scripts-temporaires contient la REGLE TRIPLET (v0.2.6)
  9. La doc du generateur est v0.2.1 + mentionne le triplet
  10. Normes : ASCII strict + LF pur (test + generateur + protocole)
  11. PARITE .sh v0.2.1 : le wrapper bash embarque le meme triplet dans son template
  14. Le squelette .py contient le bloc DECLARATION USAGES (declarer_usages +
      AGENT + appel enregistrer-usage-outil) - anti-recurrence registre a 0 ligne
  15. PARITE .sh : le wrapper bash embarque le bloc DECLARATION USAGES
  16. Le protocole v0.2.7 impose la declaration des usages (section dediee)
  17. Nettoyage : le test ne laisse AUCUNE preuve tmp-t050-preuve au registre
  12. PARITE REELLE : le script genere par le .sh est identique a celui du .py
      (hors date) - la garantie triplet vaut aussi cote bash.
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


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

GEN_PY = os.path.join(TOOLS_DIR, "generateurs", "generateurs-outil-temporaire",
                      "generateurs-outil-temporaire.py")
GEN_SH = os.path.join(TOOLS_DIR, "generateurs", "generateurs-outil-temporaire",
                      "generateurs-outil-temporaire.sh")
GEN_MD = os.path.join(TOOLS_DIR, "generateurs", "generateurs-outil-temporaire",
                      "generateurs-outil-temporaire.md")
PROTOCOLE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                         "regles-immuables", "general",
                         "protocole-creation-scripts-temporaires",
                         "protocole-creation-scripts-temporaires.001.01.ebauche.md")

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


def main():
    global POINT_ACTIF, DESACTIVES
    t0 = time.time()
    import argparse
    ap = argparse.ArgumentParser(description="test-050 triplet outils temporaires")
    ap.add_argument("--isoler", type=int, default=None)
    ap.add_argument("--desactiver", default="")
    ap.add_argument("--chrono", action="store_true")
    args = ap.parse_args()
    POINT_ACTIF = args.isoler
    DESACTIVES = set(int(x) for x in args.desactiver.split(",") if x.strip())

    dossier_test = tempfile.mkdtemp(prefix="tmp-test050-", dir=PROJECT_ROOT)

    # 1. Version du generateur
    out = run([sys.executable, GEN_PY, "--version"])
    ok = "0.2.1" in out
    verifier("1. generateurs-outil-temporaire v0.2.1 (--version)", ok, out.strip())

    # 2-3. Template dans le code source
    code = io.open(GEN_PY, encoding="utf-8", errors="replace").read()
    fonctions = ["def point_actif", "def chrono_etape", "def bilan_chrono",
                 "def verifier_nommage"]
    ok = all(f in code for f in fonctions)
    verifier("2. template : point_actif + chrono_etape + bilan_chrono + verifier_nommage", ok)
    options = ["--isoler", "--desactiver", "--no-chrono", "--dry-run"]
    ok = all(o in code for o in options)
    verifier("3. template : options --isoler/--desactiver/--no-chrono/--dry-run", ok)

    # 4. PREUVE REELLE : generer un outil temporaire et verifier le script genere
    nom = "tmp-t050-preuve"
    chemin_gen = os.path.join(dossier_test, nom + ".py")
    cmd = [sys.executable, GEN_PY, "--nom", "t050-preuve",
           "--description", "preuve triplet", "--dossier", dossier_test, "--force"]
    out = run(cmd)
    # le generateur ajoute tmp- au nom -> tmp-t050-preuve.py
    chemin_gen = os.path.join(dossier_test, "tmp-t050-preuve.py")
    ok = os.path.isfile(chemin_gen)
    if ok:
        contenu = io.open(chemin_gen, encoding="utf-8", errors="replace").read()
        ok = all(f in contenu for f in ["def point_actif", "def chrono_etape",
                                        "def bilan_chrono", "DRY_RUN",
                                        "DESACTIVES", "ISOLE"])
    verifier("4. script genere : triplet embarque (preuve reelle)", ok, chemin_gen)

    # 4b. Renseigner AGENT dans le script genere (le bloc DECLARATION USAGES
    # refuse de s executer sinon - lecon 2026-08-14) avant les executions 5/7.
    if os.path.isfile(chemin_gen):
        contenu = io.open(chemin_gen, encoding="utf-8", errors="replace").read()
        contenu = contenu.replace('AGENT = "a-completer"', 'AGENT = "test-050"')
        io.open(chemin_gen, "w", encoding="ascii", newline="\n").write(contenu)

    # 5. Execution du script genere (chrono affiche)
    if os.path.isfile(chemin_gen):
        out = run([sys.executable, chemin_gen])
        ok = "CHRONO" in out and "logique a completer" in out
        verifier("5. script genere : execution + bilan chrono", ok, out.strip()[:120])

    # 6. --dry-run du script genere
    if os.path.isfile(chemin_gen):
        out = run([sys.executable, chemin_gen, "--dry-run"])
        ok = "DRY-RUN" in out and "aucune action" in out
        verifier("6. script genere : --dry-run (aucune action)", ok, out.strip()[:80])

    # 7. --no-chrono du script genere
    if os.path.isfile(chemin_gen):
        out = run([sys.executable, chemin_gen, "--no-chrono"])
        ok = "CHRONO" not in out and "logique a completer" in out
        verifier("7. script genere : --no-chrono (chrono coupe)", ok, out.strip()[:80])

    # 8. Protocole : REGLE TRIPLET
    try:
        proto = io.open(PROTOCOLE, encoding="utf-8").read()
        ok = "REGLE TRIPLET" in proto and "0.2.6" in proto
        verifier("8. protocole-creation-scripts-temporaires : REGLE TRIPLET (v0.2.6)", ok)
    except OSError as e:
        verifier("8. protocole-creation-scripts-temporaires : REGLE TRIPLET", False, str(e))

    # 9. Doc du generateur v0.2.1 + triplet
    try:
        md = io.open(GEN_MD, encoding="utf-8").read()
        ok = "0.2.1" in md and "TRIPLET" in md
        verifier("9. doc generateur : v0.2.1 + TRIPLET documente", ok)
    except OSError as e:
        verifier("9. doc generateur : v0.2.1 + TRIPLET", False, str(e))

    # 10. Normes
    fichiers = [os.path.abspath(__file__), GEN_PY, GEN_SH, PROTOCOLE]
    na = sum(compter_non_ascii(f) for f in fichiers)
    cr = sum(compter_crlf(f) for f in fichiers)
    verifier("10. ASCII strict : 0 non-ASCII (test + generateurs + protocole)", na == 0, "na=%d" % na)
    verifier("11. LF pur : 0 CRLF (test + generateurs + protocole)", cr == 0, "crlf=%d" % cr)

    # 11. PARITE .sh : le wrapper bash embarque le triplet + version 0.2.1
    sh_src = io.open(GEN_SH, encoding="utf-8", errors="replace").read()
    triplet_sh = ["def point_actif", "def chrono_etape", "def bilan_chrono",
                  "def verifier_nommage", "--isoler", "--desactiver"]
    ok = ("0.2.1" in sh_src and all(f in sh_src for f in triplet_sh))
    verifier("12. parite .sh : v0.2.1 + triplet dans le template bash", ok)

    # 12. PARITE REELLE : scripts generes identiques (.py vs .sh, hors date)
    dossier_sh = os.path.join(dossier_test, "sh")
    dossier_py = os.path.join(dossier_test, "py")
    os.makedirs(dossier_sh)
    os.makedirs(dossier_py)
    cmd_sh = ["bash", GEN_SH, "--nom", "parite", "--description", "parite triplet",
              "--dossier", dossier_sh, "--force"]
    cmd_py = [sys.executable, GEN_PY, "--nom", "parite", "--description", "parite triplet",
              "--dossier", dossier_py, "--force"]
    run(cmd_sh)
    run(cmd_py)
    f_sh = os.path.join(dossier_sh, "tmp-parite.py")
    f_py = os.path.join(dossier_py, "tmp-parite.py")
    ok = os.path.isfile(f_sh) and os.path.isfile(f_py)
    detail = ""
    if ok:
        c_sh = io.open(f_sh, encoding="utf-8", errors="replace").read()
        c_py = io.open(f_py, encoding="utf-8", errors="replace").read()
        # hors date (ligne Cree)
        sans_date = lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("Cree :"))
        if sans_date(c_sh) != sans_date(c_py):
            ok = False
            detail = "contenus differents"
        else:
            detail = "scripts generes identiques"
    verifier("13. parite reelle : script genere .sh == script genere .py (hors date)", ok, detail)

    # 14. DECLARATION USAGES dans le squelette .py (anti-recurrence registre
    # a 0 ligne - lecon 2026-08-14 : 3 missions sans aucune declaration)
    code_gen = io.open(GEN_PY, encoding="utf-8", errors="replace").read()
    bloc_decl = ["def declarer_usage", "def declarer_usages",
                 'AGENT = "a-completer"', "enregistrer-usage-outil",
                 "declarer_usages()"]
    ok = all(f in code_gen for f in bloc_decl)
    verifier("14. squelette .py : bloc DECLARATION USAGES", ok)

    # 15. PARITE .sh : le wrapper bash embarque aussi le bloc DECLARATION
    sh_src = io.open(GEN_SH, encoding="utf-8", errors="replace").read()
    ok = all(f in sh_src for f in ["def declarer_usages",
                                   'AGENT = "a-completer"'])
    verifier("15. parite .sh : bloc DECLARATION USAGES dans le template bash", ok)

    # 16. Protocole v0.2.7 : section declaration des usages
    try:
        proto = io.open(PROTOCOLE, encoding="utf-8").read()
        ok = "La declaration des usages" in proto and "0.2.7" in proto
        verifier("16. protocole v0.2.7 : declaration usages imposee", ok)
    except OSError as e:
        verifier("16. protocole v0.2.7 : declaration usages imposee", False, str(e))

    # 17. Nettoyage : le test NE DOIT PAS laisser ses preuves tmp-t050-preuve
    # dans le registre-usages (le script genere avec AGENT declare au registre).
    # Meme regle que test-051 : detection par json.loads + tri preserve.
    REG_USAGES = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                              "traces", "registre-usages-outils.jsonl")
    lignes = [l for l in io.open(REG_USAGES, encoding="utf-8") if l.strip()]

    def est_preuve(l):
        try:
            return "tmp-t050-preuve" in json.loads(l).get("outil", "")
        except ValueError:
            return False

    gardees = [l for l in lignes if not est_preuve(l)]
    if len(gardees) != len(lignes):
        with io.open(REG_USAGES, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(gardees) + ("\n" if gardees else ""))
    restantes = sum(1 for l in io.open(REG_USAGES, encoding="utf-8")
                    if l.strip() and est_preuve(l))
    verifier("17. le test nettoie ses preuves tmp-t050-preuve (0 restante)",
             restantes == 0, "restantes=%d" % restantes)

    shutil.rmtree(dossier_test, ignore_errors=True)

    if args.chrono:
        chrono_etape("test-050 triplet outils temporaires", time.time() - t0)
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
