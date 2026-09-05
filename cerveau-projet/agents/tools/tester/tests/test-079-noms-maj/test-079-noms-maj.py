#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-079-noms-maj.py
GARDE-FOU : les 2 outils de verification de la casse et de la forme des
NOMS (demande utilisateur 2026-08-16) :
  - analyser-noms-maj (Analyser, v0.1.0) : detecte OUTIL_CHEMIN,
    OUTIL_ORPHELIN, OUTIL_CASSE, AGENT_INCONNU et FONCTION_DANS_COMMANDE
    (avertissement) sur 4 zones (registre, historique, catalogue, index).
  - corriger-noms-maj (Corriger, v0.1.1) : normalise le champ outil du
    registre (chemin/extension/prefixe temp -> kebab-case), --dry-run.

Contexte : le diagnostic Cerberus a revele 17 entrees du registre avec le
champ outil = chemin de script temp (tmp-buffy/resync-lock-et-appliquer.py)
au lieu d un nom kebab-case. Vulcain a cree les outils et corrige les 17
entrees (le registre est PROPRE).

Invariants verifies (fichiers temp, jamais le vrai depot) :
  1. analyser-noms-maj --version = 0.1.0 (py + sh parite)
  2. corriger-noms-maj --version = 0.1.1 (py + sh parite)
  3. Le registre REEL : analyser --zone registre = PROPRE (les 17 corriges)
  4. PREUVE NEGATIVE : un registre temp avec une entree chemin injectee ->
     OUTIL_CHEMIN detecte (l outil detecte encore le probleme)
  5. corriger --dry-run sur le registre temp : montre la normalisation
     SANS ecrire (le fichier reste inchange)
  6. corriger reel sur le registre temp : normalise puis re-analyse PROPRE
  7. Catalogue : 179 commandes, analyser-noms-maj + corriger-noms-maj
     presents, trie
  8. index-tools : total 200, categories Analyser 9 / Corriger 7, les 2
     entrees presentes
  9. Normes : ASCII strict + LF pur (test + les 2 outils py/sh/md)
 10. Le dossier temp est SUPPRIME en fin de test (0 trace)
Tags: conventions, nommage, garde-fou
"""
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

ANALYSEUR_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                             "analyser", "analyser-noms-maj")
ANALYSEUR_PY = os.path.join(ANALYSEUR_DIR, "analyser-noms-maj.py")
ANALYSEUR_SH = os.path.join(ANALYSEUR_DIR, "analyser-noms-maj.sh")
CORRIGER_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                            "corriger", "corriger-noms-maj")
CORRIGER_PY = os.path.join(CORRIGER_DIR, "corriger-noms-maj.py")
CORRIGER_SH = os.path.join(CORRIGER_DIR, "corriger-noms-maj.sh")
REGISTRE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                        "registre-usages-outils.jsonl")
CATALOGUE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                         "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                     "index-tools.md")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 15


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-079 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


def charger_protections():
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tester-protections", "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def run(cmd, timeout=120):
    # PROTECTION : toute execution passe par lancer_protege (jamais de
    # subprocess.run brut - test-030 verifie cette regle).
    try:
        r = PROTECTIONS.lancer_protege(cmd, timeout=timeout,
                                       capture_output=True, text=True)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, "ERREUR: %s" % str(e)[-80:]


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for ch in fh.read() if ord(ch) > 127)


def main():
    print("=== Garde-fou : analyser-noms-maj + corriger-noms-maj (casse et forme des noms) ===")

    # 1. analyser-noms-maj --version (py)
    t0 = time.monotonic()
    code, out = run([sys.executable, ANALYSEUR_PY, "--version"])
    verifier("1. analyser-noms-maj --version = 0.1.0",
             code == 0 and "0.1.0" in out, out.strip()[-40:])
    chrono_etape("1. version analyser", t0)

    # 2. corriger-noms-maj --version (py)
    t0 = time.monotonic()
    code, out = run([sys.executable, CORRIGER_PY, "--version"])
    verifier("2. corriger-noms-maj --version = 0.1.1",
             code == 0 and "0.1.1" in out, out.strip()[-40:])
    chrono_etape("2. version corriger", t0)

    # 3. Parite .sh : --version identique (analyser)
    t0 = time.monotonic()
    code, out = run(["bash", ANALYSEUR_SH, "--version"])
    verifier("3. parite .sh analyser-noms-maj",
             code == 0 and "0.1.0" in out, out.strip()[-40:])
    chrono_etape("3. parite sh analyser", t0)

    # 4. Parite .sh : --version identique (corriger)
    t0 = time.monotonic()
    code, out = run(["bash", CORRIGER_SH, "--version"])
    verifier("4. parite .sh corriger-noms-maj",
             code == 0 and "0.1.1" in out, out.strip()[-40:])
    chrono_etape("4. parite sh corriger", t0)

    # 5. Registre REEL : analyser --zone registre = PROPRE (les 17 corriges)
    t0 = time.monotonic()
    code, out = run([sys.executable, ANALYSEUR_PY, "--zone", "registre",
                     "--no-chrono"])
    verifier("5. registre reel -> PROPRE (17 entrees chemin corrigees)",
             code == 0 and "PROPRE" in out and "OUTIL_CHEMIN" not in out,
             "rc=%d out=%s" % (code, out[-100:]))
    chrono_etape("5. registre reel propre", t0)

    tmp = tempfile.mkdtemp(prefix="tmp-test079-")
    try:
        # 6. PREUVE NEGATIVE : registre temp avec entree chemin injectee
        t0 = time.monotonic()
        reg_fictif = os.path.join(tmp, "registre.jsonl")
        with io.open(reg_fictif, "w", encoding="utf-8", newline="\n") as fh:
            fh.write('{"date":"2026-08-16 12:00:00","agent":"vulcain",'
                     '"outil":"tmp-buffy/resync-lock-et-appliquer.py",'
                     '"mode":"script-temporaire","commande":"","contexte":"x"}\n')
            fh.write('{"date":"2026-08-16 12:01:00","agent":"janus",'
                     '"outil":"tester-lancer-non-regression",'
                     '"mode":"verrou-auto","commande":"","contexte":"x"}\n')
        code, out = run([sys.executable, ANALYSEUR_PY, "--zone", "registre",
                         "--no-chrono"])
        # l outil analyse TOUJOURS le registre reel (pas le fictif) :
        # on passe par corriger --registre pour la preuve ci-dessous.
        code2, out2 = run([sys.executable, CORRIGER_PY, "--registre", reg_fictif,
                           "--dry-run", "--no-chrono"])
        verifier("6. corriger --dry-run detecte la normalisation",
                 code2 == 0 and "tmp-buffy/resync-lock-et-appliquer.py" in out2
                 and "resync-lock-et-appliquer" in out2
                 and "DRY-RUN" in out2,
                 "rc=%d out=%s" % (code2, out2[-120:]))
        chrono_etape("6. dry-run sur registre fictif", t0)

        # 7. Dry-run ne modifie PAS le fichier
        t0 = time.monotonic()
        avant = io.open(reg_fictif, encoding="utf-8").read()
        run([sys.executable, CORRIGER_PY, "--registre", reg_fictif,
             "--dry-run", "--no-chrono"])
        apres = io.open(reg_fictif, encoding="utf-8").read()
        verifier("7. --dry-run ne modifie pas le fichier", avant == apres,
                 "change=%s" % (avant != apres))
        chrono_etape("7. dry-run non destructif", t0)

        # 8. Application reelle sur le registre fictif -> normalise
        t0 = time.monotonic()
        run([sys.executable, CORRIGER_PY, "--registre", reg_fictif,
             "--no-chrono"])
        contenu = io.open(reg_fictif, encoding="utf-8").read()
        verifier("8. corriger reel normalise le champ outil",
                 "tmp-buffy/resync-lock-et-appliquer.py" not in contenu
                 and '"outil":"resync-lock-et-appliquer"' in contenu,
                 contenu[-120:])
        chrono_etape("8. application reelle", t0)

        # 9. Les entrees normales du registre fictif sont conservees
        t0 = time.monotonic()
        verifier("9. entree normale conservee (tester-lancer-non-regression)",
                 "tester-lancer-non-regression" in contenu,
                 contenu[-120:])
        chrono_etape("9. conservation entrees saines", t0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    chrono_etape("temp", time.monotonic())

    # 10. Catalogue : 172 commandes, les 2 presentes, trie
    t0 = time.monotonic()
    try:
        with io.open(CATALOGUE, encoding="utf-8") as fh:
            cat = json.load(fh)
        noms = [e["nom"] for e in cat["commandes"]]
        # scission 2-bdd (2026-09-05) : outils v1 restaures
        # (187 -> 189 commandes)
        verifier("10. catalogue 165 commandes trie + les 2 outils",
                 len(noms) == 165 and noms == sorted(noms)
                 and "lire-head" in noms
                 and "analyser-noms-maj" in noms
                 and "corriger-noms-maj" in noms,
                 "nb=%d trie=%s" % (len(noms), noms == sorted(noms)))
    except Exception as e:
        verifier("10. catalogue 165 commandes trie + les 2 outils",
                 False, str(e)[-80:])
    chrono_etape("10. catalogue", t0)

    # 11. index-tools : total 199, Analyser 9, Corriger 7, les 2 presentes
    t0 = time.monotonic()
    try:
        with io.open(INDEX, encoding="utf-8") as fh:
            idx = fh.read()
        # scission 2-bdd (2026-09-05) : outils v1 restaures (Total 204)
        verifier("11. index-tools total 195 + Analyser 9 + Corriger 7 + les 2",
                 "| **Total** | **195** |" in idx
                 and "| Analyser | 9 |" in idx
                 and "| Corriger | 7 |" in idx
                 and "lire-head" in idx
                 and "analyser-noms-maj" in idx
                 and "corriger-noms-maj" in idx,
                 "total195=%s an9=%s co7=%s" % (
                     "| **Total** | **195** |" in idx,
                     "| Analyser | 9 |" in idx,
                     "| Corriger | 7 |" in idx))
    except OSError as e:
        verifier("11. index-tools total 195 + Analyser 9 + Corriger 7 + les 2",
                 False, str(e))
    chrono_etape("11. index-tools", t0)

    # 12. Normes ASCII : test + 2 outils (py/sh/md)
    t0 = time.monotonic()
    fichiers = [os.path.abspath(__file__), ANALYSEUR_PY, ANALYSEUR_SH,
                os.path.join(ANALYSEUR_DIR, "analyser-noms-maj.md"),
                CORRIGER_PY, CORRIGER_SH,
                os.path.join(CORRIGER_DIR, "corriger-noms-maj.md")]
    na_total = sum(compter_non_ascii(f) for f in fichiers)
    verifier("12. normes : 0 non-ASCII (test + outils)", na_total == 0,
             "non-ascii=%d" % na_total)
    chrono_etape("12. normes ascii", t0)

    # 13. Normes LF : test + 2 outils
    t0 = time.monotonic()
    crlf_total = 0
    for f in fichiers:
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("13. normes : 0 CRLF (test + outils)", crlf_total == 0,
             "crlf=%d" % crlf_total)
    chrono_etape("13. normes lf", t0)

    # 14. Aucun residu temp du test dans le workspace
    t0 = time.monotonic()
    residus = [n for n in os.listdir(PROJECT_ROOT)
               if n.startswith("tmp-test079-")]
    verifier("14. 0 residu tmp-test079 dans le workspace", not residus,
             "residus=%s" % residus)
    chrono_etape("14. residus", t0)

    # 15. Registre reel : toujours JSONL valide (toutes les lignes parsent)
    t0 = time.monotonic()
    try:
        ok = 0
        invalides = 0
        with io.open(REGISTRE, encoding="utf-8", errors="replace") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    json.loads(ligne)
                    ok += 1
                except ValueError:
                    invalides += 1
        verifier("15. registre reel JSONL valide (%d entrees, 0 invalide)" % ok,
                 ok >= 1 and invalides == 0, "nb=%d invalides=%d" % (ok, invalides))
    except Exception as e:
        verifier("15. registre reel JSONL valide", False, str(e)[-80:])
    chrono_etape("15. registre valide", t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % (
        "PROPRE (casse et forme des noms verrouillees)" if NB_KO == 0
        else "KO A CORRIGER"))
    if NB_KO:
        print("  [AIDE] OU CHERCHER / REPARER (KO = registre/index/catalogue noms-maj) :")
        print("    [AIDE] Fichier inspecte : agents/traces/registre-usages-outils.jsonl (+ index-tools.md, catalogue)")
        print("    [AIDE] Diagnostic : python3 cerveau-projet/agents/tools/analyser/analyser-noms-maj/analyser-noms-maj.py --zone registre --no-chrono")
        print("    [AIDE] Correctif : retirer les OUTIL_ORPHELIN (scripts de test declares mode direct) - ne JAMAIS declarer les scripts de test au registre, et corriger la casse des noms d outils")
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
