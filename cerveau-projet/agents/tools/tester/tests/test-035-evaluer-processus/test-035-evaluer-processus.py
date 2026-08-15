#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-035-evaluer-processus.py
GARDE-FOU : evaluer-processus detecte les derives de processus (fins de
mission erronees, outils hors carte, coherence fiche/carte) et le cerveau
est SAIN (0 probleme).

Contexte (2026-08-13, mission Themis axe C, Vulcain) :
  - Les derives successives (Morpheus consignes, Cerberus outils hors carte,
    regle de fiche contradictoire) ont montre qu un audit de processus est
    necessaire AVANT chaque validation.
  - Vulcain a cree evaluer-processus v0.2.0 qui croise les cartes (JSON), les
    fiches, AGENTS.md / AGENTS-historique.md et le REGISTRE des usages
    (source fiable, pas les lecons qui sont du bruit).
  - Les cartes morpheus/vulcain/janus ont ete corrigees (indices outils
    manquants ajoutes) pour rendre le cerveau sain.

Invariants verifies :
  1. L outil existe et compile
  2. --agent morpheus : 0 probleme (sain)
  3. --agent cerberus : 0 probleme (sain)
  4. Scan global (sans --agent) : 0 probleme
  5. --rapport ecrit un rapport markdown
  6. DECLARATION_FAUTIVE : un outil EXCLUSIF declare au registre par un
     agent non proprietaire est signale comme declaration fautive (et PAS
     comme OUTIL_HORS_CARTE) - lecon test-037 round profils
  7. Un outil exclusif declare par SON proprietaire reste sain
  8. Normes : ASCII strict + LF pur (outil + test)

v0.1.3 (2026-08-16) : evaluer-processus distingue DECLARATION_FAUTIVE
(usage registre d un outil verrouille par un agent non habilite - a
retirer du registre) de OUTIL_HORS_CARTE (outil partage manquant dans la
carte - a ajouter).
"""
import importlib.util
import io
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

OUTIL = os.path.join(TOOLS_DIR, "evaluer", "evaluer-processus",
                     "evaluer-processus.py")
REGISTRE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "traces",
                        "registre-usages-outils.jsonl")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


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


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def lancer(extra_args):
    """Lance l outil SOUS PROTECTION et retourne (code, stdout)."""
    proc = PROTECTIONS.lancer_protege(
        [PYTHON, OUTIL] + extra_args,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=PROJECT_ROOT, timeout=120,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-035 : evaluer-processus (garde-fou derives de processus) ===")
    try:
        # 1. L outil existe et compile
        verifier("1. Outil present", os.path.isfile(OUTIL), OUTIL)
        rc = PROTECTIONS.lancer_protege(
            [PYTHON, "-m", "py_compile", OUTIL], cwd=PROJECT_ROOT).returncode
        verifier("1b. Compilation OK", rc == 0, "rc=%d" % rc)

        # 2-4. Le cerveau est sain : 0 probleme partout
        for agent in ["morpheus", "cerberus"]:
            code, out = lancer(["--agent", agent])
            propre = out.strip()
            sain = ("0 probleme" in propre and code == 0)
            verifier("2. --agent %s : 0 probleme (rc=0)" % agent,
                     sain, "rc=%d out=%s" % (code, propre[-60:]))

        code, out = lancer([])
        sain_global = ("0 probleme" in out and code == 0)
        verifier("3. Scan global : 0 probleme (rc=0)",
                 sain_global, "rc=%d out=%s" % (code, out.strip()[-60:]))

        # 5. --rapport ecrit un rapport markdown
        rapport = os.path.join(PROJECT_ROOT, ".tmp-test-035-rapport.md")
        if os.path.isfile(rapport):
            os.remove(rapport)
        code, out = lancer(["--agent", "morpheus", "--rapport", rapport])
        ecrit = os.path.isfile(rapport)
        contenu_ok = False
        if ecrit:
            with io.open(rapport, encoding="utf-8", errors="replace") as fh:
                contenu_ok = "Rapport" in fh.read()
            os.remove(rapport)
        verifier("4. --rapport ecrit un rapport markdown",
                 ecrit and contenu_ok, "rc=%d ecrit=%s" % (code, ecrit))

        # 5. DECLARATION_FAUTIVE : outil exclusif declare par un non-
        # proprietaire (lecon test-037, demande utilisateur 2026-08-16).
        # On simule une entree registre fautive TEMPORAIRE (cerberus ->
        # tester-lancer-non-regression, exclusif janus), on verifie que
        # evaluer-processus la signale DECLARATION_FAUTIVE (et PAS
        # OUTIL_HORS_CARTE), puis on retire l entree en try/finally.
        import datetime as _dt035
        jour = _dt035.date.today().strftime("%Y-%m-%d")
        faux = {"date": jour + " 12:00:00", "agent": "cerberus",
                "outil": "tester-lancer-non-regression", "mode": "direct",
                "commande": "", "contexte": "TEST-035 preuve (a retirer)"}
        try:
            with io.open(REGISTRE, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(faux, ensure_ascii=True) + "\n")
            code, out = lancer([])
            fautive = "DECLARATION_FAUTIVE" in out
            pas_hors_carte = "OUTIL_HORS_CARTE" not in out
            verifier("5. DECLARATION_FAUTIVE detectee (outil exclusif par "
                     "non-proprietaire)",
                     fautive and pas_hors_carte and code == 1,
                     "rc=%d fautive=%s hors_carte=%s" %
                     (code, fautive, pas_hors_carte))
        finally:
            lignes = io.open(REGISTRE, encoding="utf-8").readlines()
            garde = [l for l in lignes if "TEST-035 preuve" not in l]
            with io.open(REGISTRE, "w", encoding="utf-8",
                         newline="\n") as fh:
                fh.writelines(garde)

        # 6. Un outil exclusif declare par SON proprietaire reste sain :
        # janus -> tester-lancer-non-regression est legitime (sa carte le
        # contient), evaluer-processus ne doit RIEN signaler.
        code, out = lancer(["--agent", "janus"])
        sain_janus = ("0 probleme" in out and code == 0)
        verifier("6. Outil exclusif par son proprietaire : sain (rc=0)",
                 sain_janus, "rc=%d out=%s" % (code, out.strip()[-60:]))
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    # 7. Normes ASCII strict + LF pur (outil + test)
    fichiers = [OUTIL, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("7. ASCII strict : 0 non-ASCII (outil + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("8. LF pur : 0 CRLF (outil + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
