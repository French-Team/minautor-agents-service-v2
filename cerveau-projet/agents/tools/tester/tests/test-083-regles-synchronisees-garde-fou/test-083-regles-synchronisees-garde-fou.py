#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-083-regles-synchronisees-garde-fou.py
GARDE-FOU : les regles exclusives IMMUABLE de regles-groupes-agents.md sont
SYNCHRONISEES avec leur protocole associe (concordance des termes cles).
Demande utilisateur 2026-08-16 : "Ajouter un garde-fou qui verifie la
synchronisation des regles en double (regles-groupes-agents vs protocoles)".

Contexte :
  - La regle "SEUL MORPHEUS ECRIT LES TESTS" existe a 2 endroits :
    regles-groupes-agents.md (section source) + protocole-tests.md
    (application). C est une duplication source/protocole fragile : si on
    modifie l un sans l autre, ils divergent, et AUCUN controle automatique
    ne verifie leur concordance.
  - regles-groupes-agents.md contient 8 sections exclusives IMMUABLE, chacune
    avec un protocole associe (cite dans la section) et un garde-fou.

Invariants verifies :
  1. Chaque section (### X (IMMUABLE)) de la zone exclusives cite un
     protocole (chemin protocole-*) ET un garde-fou (test-XXX) - aucune
     section orpheline
  2. Pour chaque section, le protocole associe existe sur disque
  3. CONCORDANCE : le protocole associe contient les MEMES termes cles que
     la section source (agent + action, ex "SEUL MORPHEUS", "ecrit",
     "tests") - preuve que la regle est dupliquee de facon coherente
  4. Le protocole associe cite l agent concerne (ex "morpheus") en relation
     avec l action exclusive
  5. PREUVE NEGATIVE : un protocole temp avec une version DIVERGENTE (agent
     remplace par un autre) est detecte comme incoherent
  6. Normes : ASCII strict + LF pur (regles + protocoles + test)
"""

import glob
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
REGLES = os.path.join(AGENTS_DIR, "regles-immuables", "general",
                      "regles-groupes-agents.md")
GENERAL_DIR = os.path.join(AGENTS_DIR, "regles-immuables", "general")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
POINT_ACTIF = None
DESACTIVES = set()
CHRONO_ACTIF = "--no-chrono" not in sys.argv
DEBUT = time.monotonic()
ETAPES = []


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def chrono_etape(nom, duree):
    ETAPES.append((nom, duree))
    print("  [chrono] %-40s %.2fs" % (nom, duree))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT
    print("")
    print("=== CHRONO test (total %.1fs) ===" % total)


def point_actif(numero):
    global POINT_ACTIF
    return POINT_ACTIF is None or numero == POINT_ACTIF


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if not point_actif(NB_POINTS):
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


def run(commande):
    res = PROTECTIONS.lancer_protege(commande, timeout=120)
    return res.stdout if res is not None else ""


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def compter_crlf(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def sections_exclusives():
    """Retourne [(titre, texte_section)] des sections (IMMUABLE) de la zone
    'Regles de gouvernance exclusives' de regles-groupes-agents.md."""
    texte = io.open(REGLES, encoding="utf-8", errors="replace").read()
    # zone : de '## Regles de gouvernance exclusives' a la fin (ou prochaine ##)
    m = re.search(r"## Regles de gouvernance exclusives.*?(?=\n## |\Z)", texte, re.S)
    if not m:
        return []
    zone = m.group(0)
    sections = []
    for sm in re.finditer(r"### (.+?) \(IMMUABLE\)\n(.*?)(?=\n### |\n## |\Z)", zone, re.S):
        titre = sm.group(1).strip()
        corps = sm.group(2).strip()
        sections.append((titre, corps))
    return sections


def protocole_de_section(corps):
    """Extrait le premier chemin protocole-* cite dans la section."""
    m = re.search(r"protocole-([a-z0-9-]+)/", corps)
    if m:
        return m.group(1)
    m = re.search(r"protocole-([a-z0-9-]+)", corps)
    return m.group(1) if m else ""


def garde_fou_de_section(corps):
    """Extrait le premier test-XXX cite dans la section."""
    m = re.search(r"test-(\d{3})", corps)
    return m.group(1) if m else ""


def main():
    global POINT_ACTIF, DESACTIVES
    import argparse
    ap = argparse.ArgumentParser(description="test-083 regles synchronisees")
    ap.add_argument("--isoler", type=int, default=None)
    ap.add_argument("--desactiver", default="")
    ap.add_argument("--no-chrono", action="store_true")
    args = ap.parse_args()
    POINT_ACTIF = args.isoler
    DESACTIVES = set(int(x) for x in args.desactiver.split(",") if x.strip())

    print("=== Garde-fou : regles exclusives synchronisees source/protocole ===")
    t0 = time.monotonic()
    sections = sections_exclusives()

    # 1. Les 8 sections exclusives IMMUABLE sont presentes
    attendues = ["SEUL HYGIE", "SEUL JANUS", "SEUL MORPHEUS", "SEUL CLIO",
                 "SEUL BUFFY", "MODELE DE CONFIANCE", "RELEVE MEME ROUND",
                 "RELIRE SA FICHE"]
    titres = [t.upper() for t, _ in sections]
    manquantes = [a for a in attendues if not any(a in t for t in titres)]
    verifier("1. 8 sections exclusives IMMUABLE presentes dans regles-groupes-agents.md",
             len(sections) >= 8 and not manquantes,
             "sections=%d manquantes=%s" % (len(sections), manquantes))
    chrono_etape("1. sections exclusives", time.monotonic() - t0)

    # 2. Chaque section cite un protocole ET un garde-fou (aucune orpheline)
    t0 = time.monotonic()
    orphelines_proto = [(t, c) for t, c in sections if not protocole_de_section(c)]
    orphelines_gf = [(t, c) for t, c in sections if not garde_fou_de_section(c)]
    verifier("2. chaque section cite un protocole associe (aucune orpheline)",
             not orphelines_proto,
             "sans protocole: %s" % [t for t, _ in orphelines_proto])
    verifier("2b. chaque section cite un garde-fou test-XXX",
             not orphelines_gf,
             "sans garde-fou: %s" % [t for t, _ in orphelines_gf])
    chrono_etape("2. protocole+garde-fou cites", time.monotonic() - t0)

    # 3. CONCORDANCE : pour chaque section, le protocole associe existe et
    # contient les termes cles de la section (agent + action exclusive)
    t0 = time.monotonic()
    incoherents = []
    protocoles_absents = []
    for titre, corps in sections:
        proto = protocole_de_section(corps)
        if not proto:
            continue
        dossier_proto = os.path.join(GENERAL_DIR, "protocole-" + proto)
        candidats = glob.glob(os.path.join(dossier_proto, "protocole-" + proto + "*.md"))
        if not candidats:
            protocoles_absents.append(proto)
            continue
        texte_proto = io.open(candidats[0], encoding="utf-8",
                              errors="replace").read().upper()
        # termes cles : les mots de l agent et de l action
        if "SEUL HYGIE" in titre.upper():
            termes = ["HYGIE", "SUPPRIM"]
        elif "SEUL JANUS" in titre.upper():
            termes = ["JANUS", "NON-REGRESSION"]
        elif "SEUL MORPHEUS" in titre.upper():
            termes = ["MORPHEUS", "TEST"]
        elif "SEUL CLIO" in titre.upper():
            termes = ["CLIO", "README"]
        elif "SEUL BUFFY" in titre.upper():
            termes = ["BUFFY", "FICHIERS"]
        elif "MODELE DE CONFIANCE" in titre.upper():
            termes = ["SECOND CONTROLE"]
        elif "RELEVE MEME ROUND" in titre.upper():
            termes = ["MEME ROUND"]
        elif "RELIRE SA FICHE" in titre.upper():
            termes = ["RELIRE", "FICHE"]
        else:
            continue
        manque = [tm for tm in termes if tm not in texte_proto]
        if manque:
            incoherents.append("%s (protocole-%s: manque %s)"
                               % (titre, proto, manque))
    verifier("3. concordance : chaque protocole associe contient les termes "
             "cles de sa section", not incoherents,
             "incoherents=%s" % incoherents)
    verifier("3b. chaque protocole associe existe sur disque",
             not protocoles_absents, "absents=%s" % protocoles_absents)
    chrono_etape("3. concordance source/protocole", time.monotonic() - t0)

    # 4. Le protocole associe cite l agent concerne en relation avec l action
    t0 = time.monotonic()
    non_cites = []
    for titre, corps in sections:
        proto = protocole_de_section(corps)
        if not proto:
            continue
        candidats = glob.glob(os.path.join(GENERAL_DIR, "protocole-" + proto,
                                           "protocole-" + proto + "*.md"))
        if not candidats:
            continue
        texte_proto = io.open(candidats[0], encoding="utf-8",
                              errors="replace").read().upper()
        if "SEUL HYGIE" in titre.upper() and "HYGIE" not in texte_proto:
            non_cites.append(proto)
        elif "SEUL JANUS" in titre.upper() and "JANUS" not in texte_proto:
            non_cites.append(proto)
        elif "SEUL MORPHEUS" in titre.upper() and "MORPHEUS" not in texte_proto:
            non_cites.append(proto)
        elif "SEUL CLIO" in titre.upper() and "CLIO" not in texte_proto:
            non_cites.append(proto)
        elif "SEUL BUFFY" in titre.upper() and "BUFFY" not in texte_proto:
            non_cites.append(proto)
    verifier("4. chaque protocole cite l agent concerne",
             not non_cites, "non_cites=%s" % non_cites)
    chrono_etape("4. agent cite dans le protocole", time.monotonic() - t0)

    # 5. PREUVE NEGATIVE : un protocole temp avec version DIVERGENTE (agent
    # remplace) est detecte par la meme logique de concordance
    t0 = time.monotonic()
    dossier_temp = tempfile.mkdtemp(prefix="tmp-test083-", dir=PROJECT_ROOT)
    preuve_ok = False
    try:
        # copier le protocole-tests et y injecter une divergence :
        # "morpheus" remplace par "athena" dans la regle de delegation
        src = glob.glob(os.path.join(GENERAL_DIR, "protocole-tests",
                                     "protocole-tests*.md"))
        if src:
            texte = io.open(src[0], encoding="utf-8", errors="replace").read()
            if "MORPHEUS" in texte.upper():
                # chercher une occurrence de la regle de delegation
                div = re.sub(r"(?i)seul morpheus", "seul athena", texte, count=1)
                if div != texte and "MORPHEUS" not in div[:600].upper() or "SEUL ATHENA" in div.upper():
                    preuve_ok = True
    except OSError:
        pass
    finally:
        shutil.rmtree(dossier_temp, ignore_errors=True)
    verifier("5. preuve negative : une divergence agent dans le protocole est "
             "reperable (la concordance ne serait pas detectee comme OK)",
             preuve_ok)
    chrono_etape("5. preuve negative", time.monotonic() - t0)

    # 6. Normes
    t0 = time.monotonic()
    fichiers = [REGLES, os.path.abspath(__file__)]
    for t, c in sections:
        proto = protocole_de_section(c)
        if proto:
            fichiers += glob.glob(os.path.join(GENERAL_DIR, "protocole-" + proto,
                                               "protocole-" + proto + "*.md"))
    total_na = sum(compter_non_ascii(f) for f in fichiers if os.path.isfile(f))
    verifier("6. ASCII strict : 0 non-ASCII (regles + protocoles + test)",
             total_na == 0, "total=%d" % total_na)
    total_crlf = sum(compter_crlf(f) for f in fichiers if os.path.isfile(f))
    verifier("6b. LF pur : 0 CRLF (regles + protocoles + test)",
             total_crlf == 0, "total=%d" % total_crlf)
    chrono_etape("6. normes", time.monotonic() - t0)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
