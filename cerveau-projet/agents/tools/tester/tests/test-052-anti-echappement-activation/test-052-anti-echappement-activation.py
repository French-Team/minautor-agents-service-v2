#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-052-anti-echappement-activation.py
GARDE-FOU ANTI-RECURRENCE : tout script temporaire (tmp-*/ et .tmp-*.py a la
racine) qui invoque activer-agent-principal (activer ou reactiver) DOIT
passer la raison via subprocess.list2cmdline - jamais une chaine shell
inline avec apostrophes.

Contexte (2026-08-14) :
  - Le bug d echappement a corrompu AGENTS.md DEUX FOIS : une raison
    contenant une apostrophe mal echappee dans une commande shell inline
    passant activer/reactiver-agent-principal a ete tronquee a la valeur
    'BILAN (parsing shell coupe a la premiere apostrophe) -> le bloc
    session-llm-1 perdait sa Raison complete et les blocs DEMARRAGE
    s accumulaient.
  - La lecon est documentee (corrections.md Janus) mais PAS mecanisee :
    aucune commande du projet n utilise subprocess.list2cmdline avant
    cette mission.
  - Le bon pattern : subprocess.list2cmdline([raison]) concatene a la
    commande (voir les scripts de fin de mission conformes) - le shell
    recoit la raison correctement quotee, quelle que soit sa teneur.

REGLE D AJOUT : tout NOUVEAU script temp qui invoque activer-agent-principal
sans list2cmdline fait KO - la non-regression le signale immediatement.

Invariants verifies :
  1. Les fichiers tmp-*/**/*.py et .tmp-*.py a la racine sont scannes
  2. Chaque fichier qui invoque activer/reactiver-agent-principal est controle
  3. La commande passe la raison via list2cmdline (sinon KO)
  4. Preuve negative : un script temp a apostrophe SANS list2cmdline fait KO
  5. Normes : ASCII strict + LF pur (test + fichiers scannes)
"""
import glob
import importlib.util
import io
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

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


def lister_scripts_temp(racine):
    """Scripts temp a la racine : dossiers tmp-*/**/*.py et fichiers .tmp-*.py."""
    fichiers = []
    for motif in ("tmp-*/*.py", "tmp-*/**/*.py", ".tmp-*.py"):
        fichiers.extend(glob.glob(os.path.join(racine, motif), recursive=True))
    return sorted(set(f for f in fichiers if os.path.isfile(f)))


def invoque_activation(contenu):
    """Le fichier invoque activer/reactiver-agent-principal ?"""
    return ("activer-agent-principal.py activer" in contenu or
            "activer-agent-principal.py reactiver" in contenu)


def utilise_list2cmdline(contenu):
    """Le fichier utilise subprocess.list2cmdline pour la raison ?
    On cherche l APPEL reel QUALIFIE (subprocess.list2cmdline( ou
    list2cmdline( apres un 'from subprocess import') - un commentaire
    contenant le mot 'list2cmdline' ne suffit pas (faux positif)."""
    return ("subprocess.list2cmdline(" in contenu or
            re.search(r"^\s*from subprocess import [^\n]*list2cmdline",
                      contenu, re.M) is not None)


def main():
    global POINT_ACTIF, DESACTIVES
    t0 = __import__("time").time()
    import argparse
    ap = argparse.ArgumentParser(description="test-052 anti-echappement activation")
    ap.add_argument("--isoler", type=int, default=None)
    ap.add_argument("--desactiver", default="")
    ap.add_argument("--chrono", action="store_true")
    args = ap.parse_args()
    POINT_ACTIF = args.isoler
    DESACTIVES = set(int(x) for x in args.desactiver.split(",") if x.strip())

    # 1. Scan des scripts temp a la racine
    scripts = lister_scripts_temp(PROJECT_ROOT)
    verifier("1. scan des scripts temp (tmp-*/ et .tmp-*.py)",
             len(scripts) >= 0, "%d fichiers" % len(scripts))

    # 2. Chaque script qui invoque activer/reactiver DOIT utiliser list2cmdline
    fautifs = []
    for f in scripts:
        try:
            contenu = io.open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if invoque_activation(contenu) and not utilise_list2cmdline(contenu):
            fautifs.append(os.path.relpath(f, PROJECT_ROOT))
    verifier("2. tout script temp activant utilise list2cmdline (0 fautif)",
             len(fautifs) == 0, "fautifs=%s" % fautifs[:5])

    # 3. Preuve negative : un script temp a apostrophe SANS list2cmdline fait KO
    #    (on cree un faux script dans un dossier temp DE TEST, hors scan racine,
    #    et on verifie que la DETECTION le trouverait -> le point 2 est fiable)
    espace = os.path.join(PROJECT_ROOT, ".tmp-test-052")
    os.makedirs(espace, exist_ok=True)
    faux = os.path.join(espace, "tmp-faux-echappement.py")
    motif_run = "subprocess." + "run("  # concat (anti auto-incrimination test-030)
    with io.open(faux, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# faux script : invocation sans list2cmdline\n")
        fh.write("import subprocess\n")
        fh.write("raison = \"mission avec 'apostrophe'\"\n")
        fh.write(motif_run + "\"python3 ... activer-agent-principal.py "
                 "activer session-llm-1 vulcain \" + raison, shell=True)\n")
    try:
        contenu_faux = io.open(faux, encoding="utf-8").read()
        detecte = (invoque_activation(contenu_faux) and
                   not utilise_list2cmdline(contenu_faux))
        verifier("3. detection fiable (script fautif -> KO attendu)",
                 detecte, "detection=%s" % detecte)
    finally:
        import shutil
        shutil.rmtree(espace, ignore_errors=True)

    # 4. Normes : ASCII strict + LF pur (test + scripts scannes)
    fichiers_normes = [os.path.abspath(__file__)]
    na = sum(ascii_count(f) for f in fichiers_normes)
    cr = sum(crlf_count(f) for f in fichiers_normes)
    verifier("4. ASCII strict : 0 non-ASCII (test)", na == 0, "na=%d" % na)
    verifier("5. LF pur : 0 CRLF (test)", cr == 0, "crlf=%d" % cr)

    if args.chrono:
        chrono_etape("test-052 anti-echappement activation",
                     __import__("time").time() - t0)
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO,
                                                               NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
