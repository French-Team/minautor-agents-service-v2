#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-115-verifier-flux-securite-r7-garde-fou.py
GARDE-FOU : la regle R7 de verifier-flux-securite (v0.2.2, fix mission
31fe865e) respecte le modele aero sans faux positif sur le largage.

Contexte (fix v0.2.2, 2026-09-02) :
  - R7 exige qu apres le FIN d un agent, le prochain evenement soit
    l aeroport (oracle/pilote). L ancien scan (0.2.1) SAUTAIT la
    coordination (oracle/pilote/cerberus) : apres une fin il passait
    par-dessus les lignes 'RECUPERE: X' + 'DEBUT: RETOUR X' et tombait
    sur l agent LARGUE par le pilote -> FLUX KO a tort (ex: FIN vulcain
    15:03:35 -> morpheus ACTIF 15:05:51).
  - Fix : le scan s arrete au premier evenement non-routine/non-citation.
    Aeroport (oracle/pilote) = OK ; Cerberus = OK seulement en
    atterrissage terminal (rien ne redecoule au-dessus) ; un agent
    METIER direct apres une fin (sans passage par l aeroport) = violation.

Invariants verifies :
  1. verifier-flux-securite.py existe, compile, --version v0.2.2
  2. VIOLATION : FIN vulcain directement suivi d un agent metier (buffy
     ACTIF, sans ligne aeroport entre) -> FLUX KO avec message R7
  3. LARGAGE NORMAL : FIN vulcain -> pilote RECUPERE + oracle DEBUT
     RETOUR -> largage buffy -> FLUX OK (le faux positif 0.2.1 ne revient
     pas)
  4. FIN en tete de tableau (rien de plus recent) -> FLUX OK
  5. Cerberus TERMINAL (derniere entree, rien ne redecoule) -> FLUX OK
  6. Cerberus NON terminal (un agent redecoule au-dessus) -> R7 KO
  7. Purge : aucun fichier temporaire laisse
  8. Normes : ASCII strict + LF pur (outil + test)
Tags: outils, verifier, garde-fou, modele-aero, r7
"""
import importlib.util
import io
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

VFS_DIR = os.path.join(TOOLS_DIR, "verifier", "verifier-flux-securite")
VFS_PY = os.path.join(VFS_DIR, "verifier-flux-securite.py")

# Dossier temporaire (protocole scripts temp)
TMP = os.path.join(PROJECT_ROOT, "tmp-test115")
FIXTURE = os.path.join(TMP, "activite-recente.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
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
T_START = time.monotonic()
ETAPES = []


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
    print("=== CHRONO test-115 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s" % nom)
        if detail:
            print("       %s" % detail)


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def ascii_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            return sum(1 for c in fh.read() if ord(c) > 127)
    except IOError:
        return -1


def crlf_count(chemin):
    if not os.path.isfile(chemin):
        return -1
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


HDR = ("| Grade | Agent | Defcon | Executeur | Etat | Secteur | Raison "
       "| Heure | id | Type |\n"
       "|-------|-------|--------|-----------|------|---------|--------"
       "|-------|----|------|\n")


def _ligne(agent, etat, heure, raison="x"):
    """Une ligne du tableau (format reel, colonnes alignees)."""
    return ("| Special | %-10s | 4 | Oracle | %-6s | General | %s | %s "
            "| glm5 | R |" % (agent, etat, raison, heure))


def executer_verifier(fixture):
    """Charge verifier-flux-securite sur une fixture (env pointe AVANT import).

    La variable AGENTS_ACTIVITE_RECENTE est lue par le module au moment de
    son IMPORT (constante module) : il faut la positionner dans os.environ
    AVANT exec_module, puis la restaurer pour ne pas polluer la suite.
    """
    ancien = os.environ.get("AGENTS_ACTIVITE_RECENTE")
    os.environ["AGENTS_ACTIVITE_RECENTE"] = fixture
    try:
        spec = importlib.util.spec_from_file_location("vfs_fixture", VFS_PY)
        v = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(v)
        return v
    finally:
        if ancien is None:
            os.environ.pop("AGENTS_ACTIVITE_RECENTE", None)
        else:
            os.environ["AGENTS_ACTIVITE_RECENTE"] = ancien


def creer_fixture(corps):
    """Cree la fixture avec frontmatter + en-tete + tableau + corps donne."""
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP, exist_ok=True)
    contenu = ("---\nidentite:\n  nom: \"Activites recentes\"\n"
               "  type: \"tableau\"\n  appartient_a: commun\n"
               "  commun: true\n---\n\n## Activites recentes -- session-admin\n\n"
               + HDR + corps)
    with io.open(FIXTURE, "w", encoding="ascii", newline="\n") as fh:
        fh.write(contenu + ("\n" if not contenu.endswith("\n") else ""))
    return FIXTURE


def nettoyer_test():
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== test-115 : R7 verifier-flux-securite sans faux positif largage ===")
    try:
        # 1. Outil existe, compile, --version v0.2.2
        if point_actif(1):
            t0 = time.monotonic()
            ok_compile = os.path.isfile(VFS_PY)
            if ok_compile:
                r = lancer([PYTHON, "-m", "py_compile", VFS_PY], timeout=60)
                ok_compile = r.returncode == 0
            r2 = lancer([PYTHON, VFS_PY, "--version"], timeout=60)
            ok = (ok_compile and r2.returncode == 0 and "0.2.2" in r2.stdout)
            verifier("1. verifier-flux-securite existe, compile, version 0.2.2",
                     ok, "rc=%d" % r2.returncode)
            chrono_etape("1. outil", t0)

        # 2. VIOLATION : fin -> agent metier direct (sans aeroport) -> KO R7
        if point_actif(2):
            t0 = time.monotonic()
            corps = "\n".join([
                _ligne("buffy", "ACTIF", "15:10:00.000"),
                _ligne("vulcain", "FIN", "15:05:00.000", "FIN: FIN VULCAIN"),
            ])
            fixture = creer_fixture(corps)
            v = executer_verifier(fixture)
            ok, erreurs = v.verifier_flux()
            r7 = [e for e in erreurs if e.startswith("R7:")]
            verifier("2. VIOLATION fin->metier direct: FLUX KO + message R7",
                     (not ok) and len(r7) >= 1 and "vulcain" in r7[0]
                     and "buffy" in r7[0],
                     "ok=%s errs=%d r7=%s"
                     % (ok, len(erreurs), r7[0][:80] if r7 else "aucune"))
            chrono_etape("2. violation", t0)

        # 3. LARGAGE NORMAL : fin -> RECUPERE + RETOUR oracle -> largage buffy
        #    -> FLUX OK (regression du faux positif 0.2.1)
        if point_actif(3):
            t0 = time.monotonic()
            corps = "\n".join([
                _ligne("buffy", "ACTIF", "15:12:00.000"),
                _ligne("pilote", "ACTIF", "15:05:01.000", "RECUPERE: vulcain"),
                _ligne("oracle", "DEBUT", "15:05:00.500",
                       "DEBUT: RETOUR VULCAIN"),
                _ligne("vulcain", "FIN", "15:05:00.000", "FIN: FIN VULCAIN"),
            ])
            fixture = creer_fixture(corps)
            v = executer_verifier(fixture)
            ok, erreurs = v.verifier_flux()
            verifier("3. LARGAGE fin->aeroport->agent: FLUX OK (0.2.1 ne revient pas)",
                     ok and len(erreurs) == 0, "ok=%s errs=%d" % (ok, len(erreurs)))
            chrono_etape("3. largage normal", t0)

        # 4. FIN en tete de tableau (rien de plus recent) -> FLUX OK
        if point_actif(4):
            t0 = time.monotonic()
            corps = "\n".join([
                _ligne("vulcain", "FIN", "15:05:00.000", "FIN: FIN VULCAIN"),
            ])
            fixture = creer_fixture(corps)
            v = executer_verifier(fixture)
            ok, erreurs = v.verifier_flux()
            verifier("4. FIN en tete de tableau: FLUX OK",
                     ok and len(erreurs) == 0, "ok=%s" % ok)
            chrono_etape("4. fin en tete", t0)

        # 5. Cerberus TERMINAL (derniere entree, rien ne redecoule) -> OK
        if point_actif(5):
            t0 = time.monotonic()
            corps = "\n".join([
                _ligne("cerberus", "ACTIF", "15:20:00.000", "ACCUEIL"),
                _ligne("vulcain", "FIN", "15:05:00.000", "FIN: FIN VULCAIN"),
            ])
            fixture = creer_fixture(corps)
            v = executer_verifier(fixture)
            ok, erreurs = v.verifier_flux()
            verifier("5. Cerberus TERMINAL (derniere entree): FLUX OK",
                     ok and len(erreurs) == 0, "ok=%s errs=%d" % (ok, len(erreurs)))
            chrono_etape("5. cerberus terminal", t0)

        # 6. Cerberus NON terminal (un agent redecoule au-dessus) -> R7 KO
        if point_actif(6):
            t0 = time.monotonic()
            corps = "\n".join([
                _ligne("buffy", "ACTIF", "15:25:00.000"),
                _ligne("cerberus", "ACTIF", "15:20:00.000", "ACCUEIL"),
                _ligne("vulcain", "FIN", "15:05:00.000", "FIN: FIN VULCAIN"),
            ])
            fixture = creer_fixture(corps)
            v = executer_verifier(fixture)
            ok, erreurs = v.verifier_flux()
            r7 = [e for e in erreurs if e.startswith("R7:")]
            verifier("6. Cerberus NON terminal (agent redecoule): R7 KO",
                     (not ok) and len(r7) >= 1 and "Cerberus" in r7[0],
                     "ok=%s r7=%s" % (ok, r7[0][:90] if r7 else "aucune"))
            chrono_etape("6. cerberus non terminal", t0)

        # 7. Purge : aucun fichier temporaire laisse
        if point_actif(7):
            t0 = time.monotonic()
            nettoyer_test()
            verifier("7. purge : aucun residu (tmp-test115 absent)",
                     not os.path.isdir(TMP))
            chrono_etape("7. purge", t0)

        # 8. Normes ASCII + LF pur (outil + test)
        if point_actif(8):
            t0 = time.monotonic()
            fichiers = [os.path.abspath(__file__), VFS_PY]
            total_na = sum(max(ascii_count(f), 0) for f in fichiers)
            total_crlf = sum(max(crlf_count(f), 0) for f in fichiers)
            verifier("8. ASCII strict : 0 non-ASCII (outil + test)",
                     total_na == 0, "nb=%d" % total_na)
            verifier("9. LF pur : 0 CRLF (outil + test)",
                     total_crlf == 0, "nb=%d" % total_crlf)
            chrono_etape("8. normes", t0)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1
        nettoyer_test()
    except Exception as e:
        print("  [KO] EXCEPTION : %s" % e)
        NB_KO += 1
        nettoyer_test()

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % ("PROPRE (R7 conforme modele aero)" if NB_KO == 0
                                    else "KO (R7 non conforme)"))
    return 1 if NB_KO > 0 else 0


if __name__ == "__main__":
    sys.exit(main())