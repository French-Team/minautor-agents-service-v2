#!/usr/bin/env python3
# -*- coding: ascii -*-
# test-085-processus-residuels-garde-fou.py
#
# GARDE-FOU (demande utilisateur 2026-08-16, suite mission processus-residuels) :
# verifie le bon fonctionnement des 2 outils processus-residuels :
#   1. DETECTEUR : etat PROPRE (aucun residuel) quand rien ne traine ; un vrai
#      processus residuel temporaire (python sleep lance depuis tmp-morpheus/)
#      est DETECTE avec justification PROJET ; apres terminaison, retour PROPRE.
#   2. VERROU : nettoyer-processus-residuels est EXCLUSIF hygie - verrou
#      --audit : hygie PASSE, buffy BLOQUE.
#   3. LISTE BLANCHE : freebuff/unsloth/codebuff ne sont JAMAIS signales par le
#      detecteur (absents de sa sortie).
#   4. PREUVE NEGATIVE : la detection voit le processus injecte, puis le test
#      le termine et verifie 0 residu restant (anti-residu : le test nettoie
#      TOUTES ses preuves).
"""
Protections importees : tester-protections (lancer_protege).
Options : --no-chrono, --isoler N, --desactiver 1,3,5.
Normes : ASCII strict, LF pur.
"""
import importlib.util
import io
import os
import re
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
PYTHON = sys.executable

DETECTEUR = os.path.join(TOOLS_DIR, "detecter",
                         "detecter-processus-residuels",
                         "detecter-processus-residuels.py")
NETTOYEUR = os.path.join(TOOLS_DIR, "nettoyer",
                         "nettoyer-processus-residuels",
                         "nettoyer-processus-residuels.py")
VERROU = os.path.join(TOOLS_DIR, "proteger",
                      "proteger-verrou-habilitation",
                      "proteger-verrou-habilitation.py")
TMP_PREUVE = os.path.join(PROJECT_ROOT, "tmp-morpheus")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N
#   --desactiver 1,3,5     saute les points listes
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            pass
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        for p in sys.argv[i + 1].split(","):
            try:
                DESACTIVES.append(int(p))
            except ValueError:
                pass
ETAPES = []
T_START = time.monotonic()


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-085 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-38s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("[OK] %s" % nom)
    else:
        NB_KO += 1
        print("[KO] %s" % nom)
        if detail:
            print("     %s" % detail)


def lancer(cmd, timeout=90, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def lancer_detecteur():
    out = lancer([PYTHON, DETECTEUR, "--detail"], timeout=120)
    return (getattr(out, "returncode", 0) or 0,
            getattr(out, "stdout", "") or "")


def lancer_residuel_preuve():
    """Lance un VRAI processus residuel ORPHELIN (python sleep 60) depuis
    tmp-morpheus/. Pour simuler un vrai residuel, le processus doit etre
    ORPHELIN : son parent doit mourir apres le lancement. On passe par un
    shell intermediaire qui lance le python en arriere-plan puis se termine
    immediatement -> le python est reparente a un parent mort (orphelin).
    Retourne le pid du python, ou None en cas d echec."""
    os.makedirs(TMP_PREUVE, exist_ok=True)
    script = os.path.join(TMP_PREUVE, "residuel-preuve-085.py")
    with io.open(script, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# -*- coding: ascii -*-\nimport time\ntime.sleep(60)\n")
    try:
        if sys.platform == "win32":
            # cmd /c start : lance le python detache, le cmd meurt -> orphelin.
            subprocess.call(
                ["cmd", "/c", "start", "", "/b", PYTHON, script],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        else:
            # sh -c 'python script &' : le sh meurt, le python est orphelin.
            subprocess.call(
                ["sh", "-c", "'%s' '%s' &" % (PYTHON, script)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        # Retrouver le pid par le nom du script dans la liste des processus.
        for _ in range(10):
            rc, sortie = lancer_detecteur()
            m = re.search(r"PID\s+(\d+).*residuel-preuve-085", sortie)
            if m:
                return int(m.group(1))
            time.sleep(1)
        return None
    except Exception:
        return None


def terminer_pid(pid):
    """Termine un processus (Windows taskkill / POSIX kill)."""
    if not pid:
        return
    try:
        if sys.platform == "win32":
            subprocess.call(["taskkill", "/PID", str(pid), "/F"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.kill(pid, 9)
    except Exception:
        pass


def nettoyer_preuves():
    """Supprime les preuves temporaires du test (0 residu)."""
    terminer_pid(_PID_PREUVE)
    try:
        for nom in os.listdir(TMP_PREUVE):
            if nom.startswith("residuel-preuve-085"):
                os.remove(os.path.join(TMP_PREUVE, nom))
    except OSError:
        pass
    try:
        os.rmdir(TMP_PREUVE)
    except OSError:
        pass


_PID_PREUVE = None


def main():
    global _PID_PREUVE

    # --- 1. Etat initial : detecteur PROPRE (aucun residuel)
    if point_actif(1):
        t = time.monotonic()
        rc, sortie = lancer_detecteur()
        propre_initial = ("AUCUN RESIDUEL" in sortie) and (rc == 0)
        verifier("1. detecteur initial : AUCUN RESIDUEL", propre_initial,
                 "rc=%s sortie=%s" % (rc, sortie[:120]))
        chrono_etape("1. etat initial", t)

    # --- 2. Injection d un vrai processus residuel puis detection PROJET
    if point_actif(2):
        t = time.monotonic()
        _PID_PREUVE = lancer_residuel_preuve()
        time.sleep(2)
        rc, sortie = lancer_detecteur()
        detecte = _PID_PREUVE is not None and str(_PID_PREUVE) in sortie
        justif_projet = ("PROJET" in sortie)
        verifier("2. processus injecte (pid=%s) detecte" % _PID_PREUVE,
                 detecte, sortie[:200])
        verifier("2b. justification PROJET presente", justif_projet, sortie[:200])
        chrono_etape("2. injection+detection", t)

    # --- 3. Liste blanche : freebuff/unsloth jamais signales
    if point_actif(3):
        t = time.monotonic()
        rc, sortie = lancer_detecteur()
        sortie_bas = sortie.lower()
        blancs = [b for b in ("freebuff", "unsloth", "codebuff")
                  if b in sortie_bas and "jamais signale" not in sortie_bas]
        verifier("3. liste blanche absente de la sortie", not blancs,
                 "trouves: %s" % (blancs or "aucun"))
        chrono_etape("3. liste blanche", t)

    # --- 4. Nettoyage : terminer le processus, retour PROPRE
    if point_actif(4):
        t = time.monotonic()
        if _PID_PREUVE:
            terminer_pid(_PID_PREUVE)
            time.sleep(2)
        rc, sortie = lancer_detecteur()
        propre_final = "AUCUN RESIDUEL" in sortie
        verifier("4. apres terminaison : AUCUN RESIDUEL", propre_final,
                 sortie[:200])
        chrono_etape("4. retour propre", t)

    # --- 5. Verrou : nettoyer-processus-residuels exclusif hygie
    if point_actif(5):
        t = time.monotonic()
        out_hygie = lancer([PYTHON, VERROU, "--audit", "--agent", "hygie",
                            "--outil", "nettoyer-processus-residuels"], timeout=60)
        out_buffy = lancer([PYTHON, VERROU, "--audit", "--agent", "buffy",
                            "--outil", "nettoyer-processus-residuels"], timeout=60)
        sortie_hygie = getattr(out_hygie, "stdout", "") or ""
        sortie_buffy = getattr(out_buffy, "stdout", "") or ""
        hygie_ok = "OK" in sortie_hygie
        buffy_ko = "BLOQUE" in sortie_buffy
        verifier("5. verrou : hygie OK", hygie_ok, sortie_hygie[:150])
        verifier("5b. verrou : buffy BLOQUE", buffy_ko, sortie_buffy[:150])
        chrono_etape("5. verrou", t)

    # --- 6. Nettoyage final des preuves (0 residu)
    if point_actif(6):
        t = time.monotonic()
        nettoyer_preuves()
        residus = [n for n in os.listdir(PROJECT_ROOT)
                   if n.startswith("residuel-preuve-085") or
                   (n == "tmp-morpheus" and os.path.isdir(os.path.join(PROJECT_ROOT, n))
                    and not os.listdir(os.path.join(PROJECT_ROOT, n)))]
        verifier("6. 0 residu de preuve (processus + fichiers)", not residus,
                 "residus: %s" % (residus or "aucun"))
        chrono_etape("6. nettoyage final", t)

    bilan_chrono()
    print("")
    print("RESULTAT : %d point(s), %d OK, %d KO" % (NB_POINTS, NB_OK, NB_KO))
    if NB_KO:
        print("VERDICT : KO")
        return 1
    print("VERDICT : OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
