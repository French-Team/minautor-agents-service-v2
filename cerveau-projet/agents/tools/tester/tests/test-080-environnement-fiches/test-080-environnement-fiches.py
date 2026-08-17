#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-080-environnement-fiches.py
GARDE-FOU : la section `## Environnement de travail (Systeme)` est presente
dans le template fiche-agent-template.md ET dans CHACUNE des 15 fiches
agents, generee par verifier-systeme --bloc-fiche <agent> (v0.2.3).

Contexte (demande utilisateur 2026-08-16) : chaque fiche agent doit
contenir les infos de l environnement reel (OS, shell, langages, racine
projet) pour que l agent sache toujours sur quel systeme il travaille et
n oublie jamais les differences Windows vs Linux. Vulcain a ajoute
verifier-systeme --bloc-fiche (v0.2.3), Buffy a ajoute la section au
template et aux 15 fiches.

Invariants verifies :
  1. verifier-systeme --version = 0.2.3 (py + sh parite)
  2. --bloc-fiche cerberus genere ## Environnement de travail + Windows
  3. Le template fiche-agent-template.md contient la section
  4. CHACUNE des 15 fiches contient la section + Windows + Differences
  5. La section est AVANT ## Limites dans chaque fiche
  6. verifier-conformite-fiche --tous = 11 CONFORME (verdict via subprocess)
  7. Normes : ASCII strict + LF pur (test + verifier-systeme py/sh/md)
  8. Aucun residu temp dans le workspace
Tags: conventions, fiches, environnement, garde-fou
"""
import importlib.util
import io
import os
import shutil
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

AGENTS = ['cerberus', 'buffy', 'vulcain', 'morpheus', 'janus', 'themis',
          'atlas', 'clio', 'hygie', 'argus', 'hermes', 'athena',
          'promethee', 'minerve', 'gardien']
TEMPLATE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                        "fiche-agent-template.md")
VERIF_SYS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                         "verifier", "verifier-systeme", "verifier-systeme.py")
VERIF_SYS_SH = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                            "verifier", "verifier-systeme", "verifier-systeme.sh")
VERIF_SYS_MD = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                            "verifier", "verifier-systeme", "verifier-systeme.md")
CONFORME = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                        "verifier", "verifier-conformite-fiche",
                        "verifier-conformite-fiche.py")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 11


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-080 (total %.1fs) ===" % total)
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
    print("=== Garde-fou : section Environnement de travail dans les fiches agents ===")

    # 1. verifier-systeme --version = 0.2.3 (py)
    t0 = time.monotonic()
    code, out = run([sys.executable, VERIF_SYS, "--version"])
    verifier("1. verifier-systeme --version = 0.2.3 (py)",
             code == 0 and "0.2.3" in out, out.strip()[-40:])
    chrono_etape("1. version py", t0)

    # 2. Parite .sh
    t0 = time.monotonic()
    code, out = run(["bash", VERIF_SYS_SH, "--version"])
    verifier("2. parite .sh verifier-systeme 0.2.3",
             code == 0 and "0.2.3" in out, out.strip()[-40:])
    chrono_etape("2. version sh", t0)

    # 3. --bloc-fiche cerberus genere le bloc attendu
    t0 = time.monotonic()
    code, out = run([sys.executable, VERIF_SYS, "--bloc-fiche", "cerberus"])
    verifier("3. --bloc-fiche genere Environnement + Windows + Racine projet",
             code == 0 and "## Environnement de travail (Systeme)" in out
             and "Windows" in out and "Racine projet" in out
             and "Differences Windows vs Linux" in out,
             "rc=%d" % code)
    chrono_etape("3. bloc-fiche", t0)

    # 4. Template : section presente
    t0 = time.monotonic()
    tpl = io.open(TEMPLATE, encoding="utf-8", errors="replace").read()
    verifier("4. template contient la section Environnement",
             "## Environnement de travail (Systeme)" in tpl
             and "verifier-systeme --bloc-fiche" in tpl, "")
    chrono_etape("4. template", t0)

    # 5. Chaque fiche : section + Windows + Differences
    t0 = time.monotonic()
    manquantes = []
    for agent in AGENTS:
        fiche = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             agent, agent + ".md")
        if not os.path.exists(fiche):
            manquantes.append(agent + " (introuvable)")
            continue
        d = io.open(fiche, encoding="utf-8", errors="replace").read()
        if ("## Environnement de travail (Systeme)" not in d
                or "Windows" not in d
                or "Differences Windows vs Linux" not in d):
            manquantes.append(agent)
    verifier("5. les 15 fiches contiennent la section + Windows + Differences",
             not manquantes, "manquantes=%s" % manquantes[:5])
    chrono_etape("5. fiches", t0)

    # 6. Section AVANT ## Limites dans chaque fiche
    t0 = time.monotonic()
    mauvais_ordre = []
    for agent in AGENTS:
        fiche = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             agent, agent + ".md")
        if not os.path.exists(fiche):
            continue
        d = io.open(fiche, encoding="utf-8", errors="replace").read()
        pos_env = d.find("## Environnement de travail (Systeme)")
        pos_lim = d.find("## Limites")
        if pos_env < 0 or (pos_lim >= 0 and pos_env > pos_lim):
            mauvais_ordre.append(agent)
    verifier("6. section Environnement AVANT ## Limites (15 fiches)",
             not mauvais_ordre, "mauvais=%s" % mauvais_ordre[:5])
    chrono_etape("6. ordre", t0)

    # 7. verifier-conformite-fiche --tous = 11 CONFORME
    t0 = time.monotonic()
    code, out = run([sys.executable, CONFORME, "--tous"])
    verifier("7. verifier-conformite-fiche --tous : 11 CONFORME",
             code == 0 and "11 CONFORME" in out and "ECARTS" in out,
             "rc=%d out=%s" % (code, out[-80:]))
    chrono_etape("7. conformite", t0)

    # 8. Normes ASCII : test + verifier-systeme py/sh/md + template
    t0 = time.monotonic()
    fichiers = [os.path.abspath(__file__), VERIF_SYS, VERIF_SYS_SH, VERIF_SYS_MD,
                TEMPLATE]
    na_total = sum(compter_non_ascii(f) for f in fichiers)
    verifier("8. normes : 0 non-ASCII (test + verifier-systeme + template)",
             na_total == 0, "non-ascii=%d" % na_total)
    chrono_etape("8. normes ascii", t0)

    # 9. Normes LF
    t0 = time.monotonic()
    crlf_total = 0
    for f in fichiers:
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("9. normes : 0 CRLF (test + verifier-systeme + template)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("9. normes lf", t0)

    # 10. Normes des 15 fiches (ASCII + LF)
    t0 = time.monotonic()
    na_fiches = 0
    crlf_fiches = 0
    for agent in AGENTS:
        fiche = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                             agent, agent + ".md")
        if not os.path.exists(fiche):
            continue
        na_fiches += compter_non_ascii(fiche)
        b = io.open(fiche, "rb").read()
        crlf_fiches += b.count(b"\r\n")
    verifier("10. normes 15 fiches : 0 non-ASCII + 0 CRLF",
             na_fiches == 0 and crlf_fiches == 0,
             "na=%d crlf=%d" % (na_fiches, crlf_fiches))
    chrono_etape("10. normes fiches", t0)

    # 11. Aucun residu temp du test dans le workspace
    t0 = time.monotonic()
    residus = [n for n in os.listdir(PROJECT_ROOT)
               if n.startswith("tmp-test080-")]
    verifier("11. 0 residu tmp-test080 dans le workspace", not residus,
             "residus=%s" % residus)
    chrono_etape("11. residus", t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % (
        "PROPRE (environnement de travail verrouille dans les fiches)"
        if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
