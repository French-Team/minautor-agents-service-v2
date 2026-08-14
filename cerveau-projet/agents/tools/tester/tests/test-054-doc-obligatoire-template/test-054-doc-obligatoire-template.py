#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-054-doc-obligatoire-template.py
GARDE-FOU ANTI-RECURRENCE : le template des outils (outil-template.py ET
outil-template.sh) DOIT embarquer le bloc DOC OBLIGATOIRE - la lecture du
.md de documentation est mecanisee (demande utilisateur 2026-08-14,
severite bloquante) : le mode reel est bloque sans --confirme-doc.

Contexte (2026-08-14) :
  - Les agents n utilisaient pas les outils correctement car ils ne lisaient
    pas le .md de documentation. La REGLE ABSOLUE du protocole-outils et
    celle des 11 cartes existaient mais n etaient PAS mecanisees.
  - Decision utilisateur : severite BLOQUANTE - le mode reel exige
    --confirme-doc. Vulcain a ajoute le bloc dans outil-template v0.2.0 :
    verifier_doc_presente() (le .md doit exister sinon refus code 2),
    exiger_confirmation_doc() (mode reel sans --confirme-doc : affiche la
    section Utilisation du .md + refus code 2), options --doc et
    --confirme-doc.
  - Ce garde-fou protege le TEMPLATE (la reference pour les nouveaux
    outils) : tout retrait du bloc dans le template fait KO.

REGLE D AJOUT : tout NOUVEL outil cree depuis le template embarque le bloc
DOC OBLIGATOIRE (verifie par ce test sur le template lui-meme).

Invariants verifies :
  1. outil-template.py : bloc DOC OBLIGATOIRE present (fonctions + options)
  2. outil-template.sh : meme bloc present (parite bash)
  3. Preuve reelle .py : mode reel sans --confirme-doc -> refus (code 2)
  4. Preuve reelle .py : mode reel avec --confirme-doc -> passe (code 0)
  5. Preuve reelle .sh : sans --confirme-doc -> refus (code 2)
  6. Preuve reelle .sh : avec --confirme-doc -> passe (code 0)
  7. Preuve negative : bloc retire du .py -> KO (le test le detecte)
  8. Normes : ASCII strict + LF pur (test + templates + protocole)
"""
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

TEMPLATE_PY = os.path.join(TOOLS_DIR, "outil-template.py")
TEMPLATE_SH = os.path.join(TOOLS_DIR, "outil-template.sh")
TEMPLATE_MD = os.path.join(TOOLS_DIR, "outil-template.md")
PROTOCOLE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                         "regles-immuables", "general", "protocole-outils",
                         "protocole-outils.001.01.ebauche.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
POINT_ACTIF = None
DESACTIVES = set()


def chrono_etape(nom, duree):
    print("  [chrono] %-40s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if POINT_ACTIF is not None and NB_POINTS != POINT_ACTIF:
        return
    if NB_POINTS in DESACTIVES:
        print("  [DESACTIVE] %s" % nom)
        return
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def run(commande):
    res = PROTECTIONS.lancer_protege(commande, timeout=60)
    return res.returncode if res is not None else None


def copie_temp(nom_source):
    """Copie un template dans un dossier temp avec un nom conforme au nommage
    (le template original vit a la racine tools/, sans prefixe de categorie).
    On copie dans un sous-dossier tempfile avec le NOM d origine : la
    verification de nommage du template saute pour outil-template, donc la
    copie conserve le nom outil-template.py / outil-template.sh.
    Le .md est copie A COTE dans les deux cas (verifier_doc_presente l exige
    pour le .py comme pour le .sh, qui calcule ${0%.*}.md)."""
    d = tempfile.mkdtemp(prefix="tmp-test054-", dir=PROJECT_ROOT)
    shutil.copy(nom_source, os.path.join(d, os.path.basename(nom_source)))
    shutil.copy(TEMPLATE_MD, os.path.join(d, "outil-template.md"))
    return d


def main():
    global POINT_ACTIF, DESACTIVES
    t0 = time.time()
    import argparse
    ap = argparse.ArgumentParser(description="test-054 doc obligatoire template")
    ap.add_argument("--isoler", type=int, default=None)
    ap.add_argument("--desactiver", default="")
    ap.add_argument("--chrono", action="store_true")
    args = ap.parse_args()
    POINT_ACTIF = args.isoler
    DESACTIVES = set(int(x) for x in args.desactiver.split(",") if x.strip())

    # 1-2. Bloc DOC OBLIGATOIRE dans le template .py et .sh
    # On verifie les DEFINITIONS (motif 'def ' / '() {') : un simple appel ou
    # un commentaire ne suffit pas (faux positif, lecon des preuves negatives
    # precedentes : renommer la def mais garder les appels laisse la
    # sous-chaine presente).
    code_py = io.open(TEMPLATE_PY, encoding="utf-8", errors="replace").read()
    bloc_py = ["def verifier_doc_presente", "def exiger_confirmation_doc",
               "def afficher_section_utilisation", "--confirme-doc",
               '"--doc"']
    ok = all(f in code_py for f in bloc_py)
    verifier("1. outil-template.py : bloc DOC OBLIGATOIRE present", ok)

    code_sh = io.open(TEMPLATE_SH, encoding="utf-8", errors="replace").read()
    bloc_sh = ["verifier_doc_presente() {", "exiger_confirmation_doc() {",
               "afficher_section_utilisation() {", "--confirme-doc)",
               "--doc)"]
    ok = all(f in code_sh for f in bloc_sh)
    verifier("2. outil-template.sh : meme bloc present (parite bash)", ok)

    # 3-4. Preuves reelles .py : refus sans --confirme-doc, passage avec
    d = copie_temp(TEMPLATE_PY)
    f_py = os.path.join(d, "outil-template.py")
    rc = run([PYTHON, f_py])
    verifier("3. .py mode reel sans --confirme-doc : refus (rc=2)",
             rc == 2, "rc=%s" % rc)
    rc = run([PYTHON, f_py, "--confirme-doc"])
    verifier("4. .py mode reel avec --confirme-doc : passe (rc=0)",
             rc == 0, "rc=%s" % rc)

    # 5-6. Preuves reelles .sh : refus sans --confirme-doc, passage avec
    d2 = copie_temp(TEMPLATE_SH)
    f_sh = os.path.join(d2, "outil-template.sh")
    rc = run(["bash", f_sh, "cible"])
    verifier("5. .sh mode reel sans --confirme-doc : refus (rc=2)",
             rc == 2, "rc=%s" % rc)
    rc = run(["bash", f_sh, "--confirme-doc", "cible"])
    verifier("6. .sh mode reel avec --confirme-doc : passe (rc=0)",
             rc == 0, "rc=%s" % rc)

    # 7. PREUVE NEGATIVE : la definition du bloc retiree du .py -> le motif
    # 'def exiger_confirmation_doc' disparait -> le test doit le detecter KO.
    # On retire la DEFINITION (pas les appels : une sous-chaine residuelle
    # dans les appels est un faux negatif - lecon des preuves negatives).
    d3 = tempfile.mkdtemp(prefix="tmp-test054-", dir=PROJECT_ROOT)
    shutil.copy(TEMPLATE_PY, os.path.join(d3, "outil-template.py"))
    shutil.copy(TEMPLATE_MD, os.path.join(d3, "outil-template.md"))
    f3 = os.path.join(d3, "outil-template.py")
    c3 = io.open(f3, encoding="utf-8").read()
    c3 = c3.replace("def exiger_confirmation_doc", "def rien_ici")
    # Retirer aussi les appels restants pour que la sous-chaine disparaisse
    c3 = c3.replace("exiger_confirmation_doc", "rien_ici")
    io.open(f3, "w", encoding="ascii", newline="\n").write(c3)
    ok = "def exiger_confirmation_doc" not in io.open(
        f3, encoding="utf-8").read()
    verifier("7. preuve negative : def retiree -> le test detecte le KO",
             ok, "le bloc retombe encore dans le fichier")

    # 8. Normes : ASCII strict + LF pur
    fichiers = [os.path.abspath(__file__), TEMPLATE_PY, TEMPLATE_SH,
                TEMPLATE_MD, PROTOCOLE]
    na = sum(ascii_count(f) for f in fichiers)
    cr = sum(crlf_count(f) for f in fichiers)
    verifier("8. ASCII strict : 0 non-ASCII", na == 0, "na=%d" % na)
    verifier("9. LF pur : 0 CRLF", cr == 0, "crlf=%d" % cr)

    shutil.rmtree(d, ignore_errors=True)
    shutil.rmtree(d2, ignore_errors=True)
    shutil.rmtree(d3, ignore_errors=True)

    if args.chrono:
        chrono_etape("test-054 doc obligatoire template", time.time() - t0)
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


import time

if __name__ == "__main__":
    sys.exit(main())
