#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-049-entonnoir-scripts-temporaires.py
GARDE-FOU : l ENTONNOIR des scripts temporaires. Tout script temporaire
passe par executer-script-temporaire qui NORMALISE (BOM, CRLF, accents),
CONTROLE (compilation) puis EXECUTE - transparent pour l agent.

Contexte (mission utilisateur 2026-08-14 "mission entonnoir") :
  - La boucle ideale du fichier temp : creer -> entonnoir -> executer.
  - L agent ecrit son script avec des accents / retours Windows / BOM sans
    y penser ; l entonnoir le normalise automatiquement avant execution.
  - Si le script est deja conforme, il est execute tel quel (0 modif).
  - Une erreur de syntaxe BLOQUE l execution (CONTROLE KO avant lancement).
  - Le protocole-creation-scripts-temporaires v0.2.5 impose le passage par
    l entonnoir (jamais de python3 direct sur un script de tmp-<agent>/).

Cas couverts:
  1. L outil executer-script-temporaire est au catalogue generateurs-commande
  2. L outil est dans index-tools.md (categorie Executer)
  3. Le protocole-creation-scripts-temporaires mentionne l entonnoir (v0.2.5)
  4. Script sain -> execute tel quel, 0 modification (CONFORME)
  5. Script corrompu (BOM + CRLF + accents) -> normalise puis execute,
     fichier re-ecrit conforme sur disque (preuve reelle)
  6. Erreur de syntaxe -> CONTROLE KO, execution bloquee (rc != 0)
  7. --dry-run : normalise sans ecrire ni executer (fichier inchange)
  8. --version fonctionne
  9. Preuve negative : python3 DIRECT sur un script corrompu laisse la
     non-conformite (pas de normalisation) alors que l entonnoir corrige
  10. ASCII strict : 0 non-ASCII (test + outil py/sh/md + protocole)
  11. LF pur : 0 CRLF (test + outil py/sh/md + protocole)
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

OUTIL = os.path.join(TOOLS_DIR, "executer", "executer-script-temporaire",
                     "executer-script-temporaire.py")
OUTIL_SH = os.path.join(TOOLS_DIR, "executer", "executer-script-temporaire",
                        "executer-script-temporaire.sh")
OUTIL_MD = os.path.join(TOOLS_DIR, "executer", "executer-script-temporaire",
                        "executer-script-temporaire.md")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX_TOOLS = os.path.join(TOOLS_DIR, "index-tools.md")
PROTOCOLE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                         "regles-immuables", "general",
                         "protocole-creation-scripts-temporaires",
                         "protocole-creation-scripts-temporaires.001.01.ebauche.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
POINT_ACTIF = None  # --isoler N
DESACTIVES = set()  # --desactiver 1,3,5


def chrono_etape(nom, duree):
    """Bilan chrono par etape (triplet template v0.3.0)."""
    print("  [chrono] %-40s %.2fs" % (nom, duree))


def verifier(nom, ok, detail=""):
    """Point de verification : marqueur [OK]/[KO] + compteurs."""
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
    """Executer une commande sans bloquer (protection anti-blocage)."""
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
    ap = argparse.ArgumentParser(description="test-049 entonnoir scripts temporaires")
    ap.add_argument("--isoler", type=int, default=None)
    ap.add_argument("--desactiver", default="")
    ap.add_argument("--chrono", action="store_true")
    args = ap.parse_args()
    POINT_ACTIF = args.isoler
    DESACTIVES = set(int(x) for x in args.desactiver.split(",") if x.strip())

    dossier_test = tempfile.mkdtemp(prefix="tmp-test049-", dir=PROJECT_ROOT)

    # 1. Catalogue
    try:
        with io.open(CATALOGUE, encoding="utf-8") as fh:
            cat = json.load(fh)
        noms = [e["nom"] for e in cat["commandes"]]
        entree = next((e for e in cat["commandes"] if e["nom"] == "executer-script-temporaire"), None)
        ok = entree is not None and entree.get("script", "").endswith("executer-script-temporaire.py")
        verifier("1. executer-script-temporaire au catalogue (155)", ok, "trouvee=%s" % (entree is not None))
    except Exception as e:
        verifier("1. executer-script-temporaire au catalogue (155)", False, str(e))

    # 2. index-tools
    try:
        with io.open(INDEX_TOOLS, encoding="utf-8") as fh:
            idx = fh.read()
        ok = "### Executer" in idx and "executer-script-temporaire" in idx
        verifier("2. index-tools : categorie Executer + outil", ok)
    except OSError as e:
        verifier("2. index-tools : categorie Executer + outil", False, str(e))

    # 3. Protocole : mention de l entonnoir
    try:
        with io.open(PROTOCOLE, encoding="utf-8") as fh:
            proto = fh.read()
        ok = "executer-script-temporaire" in proto and "ENTONNOIR" in proto
        verifier("3. protocole-creation-scripts-temporaires : entonnoir impose", ok)
    except OSError as e:
        verifier("3. protocole-creation-scripts-temporaires : entonnoir impose", False, str(e))

    # 4. Script sain -> CONFORME + execution (0 modification)
    sain = os.path.join(dossier_test, "sain.py")
    with io.open(sain, "w", encoding="ascii", newline="\n") as fh:
        fh.write('# -*- coding: ascii -*-\nprint("SORTIE_SAIN_OK")\n')
    avant = open(sain, "rb").read()
    out = run(["python3", OUTIL, sain])
    apres = open(sain, "rb").read()
    ok = "SORTIE_SAIN_OK" in out and "CONFORME" in out and avant == apres
    verifier("4. script sain : CONFORME + execute, 0 modification", ok)

    # 5. Script corrompu -> normalise puis execute, re-ecrit conforme
    corrompu = os.path.join(dossier_test, "corrompu.py")
    contenu = 'print("d\u00e9j\u00e0 vu -- retours windows")\n'
    brut = b"\xef\xbb\xbf" + contenu.replace("\n", "\r\n").encode("utf-8")
    with open(corrompu, "wb") as fh:
        fh.write(brut)
    out = run(["python3", OUTIL, corrompu])
    lire = io.open(corrompu, encoding="utf-8", errors="replace").read()
    ok = ("deja vu" in out and "BOM" in out and "CRLF" in out
          and "ACCENTS" in out and "CONTROLE OK" in out
          and compter_non_ascii(corrompu) == 0
          and compter_crlf(corrompu) == 0)
    verifier("5. script corrompu : normalise + execute + fichier conforme", ok)

    # 6. Erreur de syntaxe -> CONTROLE KO, execution bloquee
    ko = os.path.join(dossier_test, "ko.py")
    with io.open(ko, "w", encoding="ascii", newline="\n") as fh:
        fh.write('print("debut")\nif True print("erreur syntaxe")\n')
    res = PROTECTIONS.lancer_protege(["python3", OUTIL, ko], timeout=120)
    sortie = (res.stdout or "") if res is not None else ""
    ok = "CONTROLE KO" in sortie and "bloquee" in sortie
    verifier("6. erreur de syntaxe : CONTROLE KO, execution bloquee", ok)

    # 7. --dry-run : normalise sans ecrire ni executer
    dry = os.path.join(dossier_test, "dry.py")
    with open(dry, "wb") as fh:
        fh.write(b'print("a") # d\xc3\xa9j\xc3\xa0\n')  # accents reels en UTF-8
    avant = open(dry, "rb").read()
    out = run(["python3", OUTIL, "--dry-run", dry])
    apres = open(dry, "rb").read()
    ok = "DRY-RUN" in out and "ACCENTS" in out and avant == apres
    verifier("7. --dry-run : aucun ecriture ni execution", ok)

    # 8. --version
    out = run(["python3", OUTIL, "--version"])
    ok = "executer-script-temporaire" in out and "0.1.2" in out
    verifier("8. --version", ok)

    # 9. Preuve negative : python3 direct ne normalise PAS
    direct = os.path.join(dossier_test, "direct.py")
    contenu = 'print("\u00e9\u00e9\u00e9 -- test direct")\n'
    brut = b"\xef\xbb\xbf" + contenu.replace("\n", "\r\n").encode("utf-8")
    with open(direct, "wb") as fh:
        fh.write(brut)
    res = PROTECTIONS.lancer_protege(["python3", direct], timeout=60)
    # python3 sous Windows tolere souvent UTF-8 + CRLF : le script s execute
    # mais le FICHIER reste non conforme (BOM + CRLF + accents).
    reste = (compter_non_ascii(direct) > 0 or compter_crlf(direct) > 0
             or open(direct, "rb").read().startswith(b"\xef\xbb\xbf"))
    out = run(["python3", OUTIL, direct])  # l entonnoir, lui, corrige
    ok = reste and compter_non_ascii(direct) == 0 and compter_crlf(direct) == 0
    verifier("9. preuve negative : direct laisse la non-conformite, entonnoir corrige", ok,
             "reste_non_conforme=%s" % reste)

    # 9b. CONTROLE TRIPLET (lecon 2026-08-15 : un script de mission ecrit a
    # la main SANS triplet - dry-run/wet, options, chrono - doit etre
    # SIGNALE par l entonnoir, pas execute en silence).
    sans_triplet = os.path.join(dossier_test, "sans-triplet.py")
    with io.open(sans_triplet, "w", encoding="ascii", newline="\n") as fh:
        fh.write('print("bonjour")\n')
    res = PROTECTIONS.lancer_protege(["python3", OUTIL, sans_triplet], timeout=60)
    sortie = (res.stdout or "") if res is not None else ""
    verifier("9b. script SANS triplet -> entonnoir signale [TRIPLET] WARNING",
             "TRIPLET" in sortie and "WARNING" in sortie, sortie[-150:])
    # script avec triplet -> aucun warning
    avec_triplet = os.path.join(dossier_test, "avec-triplet.py")
    with io.open(avec_triplet, "w", encoding="ascii", newline="\n") as fh:
        fh.write('import sys\nCHRONO_ACTIF = "--no-chrono" not in sys.argv\n'
                 'def chrono_etape(a, b): pass\ndef bilan_chrono(): pass\n'
                 'parser.add_argument("--dry-run")  # protection\n'
                 'parser.add_argument("--isoler")  # options on/off\n'
                 'parser.add_argument("--desactiver")  # options on/off\n'
                 'print("ok")\n')
    res2 = PROTECTIONS.lancer_protege(["python3", OUTIL, avec_triplet], timeout=60)
    sortie2 = (res2.stdout or "") if res2 is not None else ""
    verifier("   script AVEC triplet -> aucun warning", "TRIPLET" not in sortie2,
             sortie2[-150:])

    # 10-11. Normes ASCII + LF
    fichiers = [OUTIL, OUTIL_SH, OUTIL_MD, os.path.abspath(__file__), PROTOCOLE]
    na = sum(compter_non_ascii(f) for f in fichiers)
    cr = sum(compter_crlf(f) for f in fichiers)
    verifier("10. ASCII strict : 0 non-ASCII (outil + test + protocole)", na == 0, "na=%d" % na)
    verifier("11. LF pur : 0 CRLF (outil + test + protocole)", cr == 0, "crlf=%d" % cr)

    # Nettoyage
    shutil.rmtree(dossier_test, ignore_errors=True)

    if args.chrono:
        chrono_etape("test-049 entonnoir", time.time() - t0)
    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
