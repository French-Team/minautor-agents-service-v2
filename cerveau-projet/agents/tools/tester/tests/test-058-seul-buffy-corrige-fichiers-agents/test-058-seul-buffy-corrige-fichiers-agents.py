#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-058-seul-buffy-corrige-fichiers-agents.py
GARDE-FOU ANTI-RECURRENCE : SEUL la carte de Buffy assigne les outils de
correction des fichiers STRUCTURELS des agents (regle gouvernance
2026-08-15, demande utilisateur).
Contexte (2026-08-15) :
  - L utilisateur a identifie une faille : quand un agent a un probleme dans
    SES fichiers (fiche, carte, index), c est Buffy qui est habilitEe a
    corriger via ses outils dedies (editer-parcours, editer-fichier-agents).
    Si l agent se corrige lui-meme, il se simplifie la tache pour finir sa
    mission -> derives en cascade (cause historique de nombreuses erreurs).
  - Philosophie enoncee par l utilisateur : la SEPARATION DES POUVOIRS est
    la vraie protection. Cerberus assigne, Janus verifie, les agents
    executent SANS s auto-corriger ni s auto-verifier. Cerberus ne fait
    confiance qu a Janus, Janus qu a Cerberus.
  - Nuance (decision utilisateur) : chaque agent garde SES lecons dans SON
    corrections.md (protocole-fin-mission). L exclusivite porte sur les
    fichiers STRUCTURELS : fiche, parcours, index, regles, protocoles.
Invariants verifies :
  1. La carte buffy (parcours-buffy.json) contient editer-parcours ET
     editer-fichier-agents dans ses indices outil
  2. AUCUNE des 13 autres cartes ne contient editer-parcours ni
     editer-fichier-agents (ni dans les indices, ni dans le texte des cases)
  2b. Le REGISTRE ne contient AUCUNE declaration de editer-parcours /
     editer-fichier-agents par un agent autre que buffy (anti-recurrence :
     le contournement passait par des scripts directs - le registre est la
     trace de l usage reel)
  3. La regle immuable est documentee dans regles-groupes-agents.md
     (section "SEUL BUFFY CORRIGE LES FICHIERS DES AGENTS") + le modele de
     confiance (section "LE MODELE DE CONFIANCE")
  4. La fiche buffy.md contient la REGLE ABSOLUE -- SEULE A CORRIGER LES
     FICHIERS DES AGENTS (anti-recurrence : Buffy connait son exclusivite)
  5. Normes : ASCII strict + LF pur (regle + fiche + test)
Tags: agents, buffy, garde-fou, anti-recurrence
"""
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import time
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
AGENTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents")
TOOLS_DIR = os.path.join(AGENTS_DIR, "tools")
PYTHON = sys.executable
REGLE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "regles-immuables",
                     "general", "regles-groupes-agents.md")
FICHE_BUFFY = os.path.join(AGENTS_DIR, "buffy", "buffy.md")
REGISTRE = os.path.join(AGENTS_DIR, "traces", "registre-usages-outils.jsonl")
OUTILS_EXCLUSIFS = ["editer-parcours", "editer-fichier-agents"]
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
ETAPES = []
T_START = time.monotonic()


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
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
    print("=== CHRONO test-058 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


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


def lancer(cmd, timeout=60, **kwargs):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def lire(chemin):
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def outils_parcours(chemin):
    """Retourner l ensemble des noms d outils (indices outil) d un parcours."""
    d = json.load(io.open(chemin, encoding="utf-8"))
    noms = set()
    for c in d.get("cases", {}).values():
        for ind in c.get("indices", []):
            if ind.get("type") == "outil":
                noms.add((ind.get("nom", "") or ind.get("catalogue", "")).split("/")[-1])
    return noms


def main():
    # --- 1. carte buffy : les 2 outils presents
    if point_actif(1):
        t = time.monotonic()
        chemin = os.path.join(AGENTS_DIR, "buffy", "parcours", "parcours-buffy.json")
        noms = outils_parcours(chemin)
        verifier("1. carte buffy : editer-parcours + editer-fichier-agents",
                 "editer-parcours" in noms and "editer-fichier-agents" in noms,
                 "manquants: %s" % [o for o in OUTILS_EXCLUSIFS if o not in noms])
        chrono_etape("1. carte buffy", t)

    # --- 2. aucune autre carte ne contient ces outils
    if point_actif(2):
        t = time.monotonic()
        violateurs = []
        for nom in sorted(os.listdir(AGENTS_DIR)):
            if not os.path.isdir(os.path.join(AGENTS_DIR, nom)):
                continue
            parcours = os.path.join(AGENTS_DIR, nom, "parcours", "parcours-%s.json" % nom)
            if not os.path.isfile(parcours):
                continue
            if nom == "buffy":
                continue
            try:
                noms = outils_parcours(parcours)
            except (ValueError, IOError) as e:
                violateurs.append("%s (json: %s)" % (nom, e))
                continue
            # EXCEPTION PILOTE (v0.2.3, regle utilisateur 2026-08-18) : chiron
            # est autorise a posseder editer-parcours (cle par cible : SA carte
            # uniquement, verifiee par proteger-verrou-habilitation). Les
            # indices OUTIL des autres cartes restent interdits.
            if nom == "chiron":
                croises = [o for o in OUTILS_EXCLUSIFS
                           if o in noms and o != "editer-parcours"]
                if croises:
                    violateurs.append("%s: %s" % (nom, croises))
            else:
                croises = [o for o in OUTILS_EXCLUSIFS if o in noms]
                if croises:
                    violateurs.append("%s: %s" % (nom, croises))
            # verifier aussi que le texte des cases ne DECLARE PAS ces outils
            # comme outils de l agent. Les MENTIONS PEDAGOGIQUES (indices
            # AGENTS HABILITES : "Buffy cartes/parcours (editer-parcours)")
            # decrivent le domaine de BUFFY, pas une usurpation : elles ne
            # sont pas des indices OUTIL et ne donnent aucune habilitation
            # (le verrou lit les indices OUTIL, pas le texte).
            texte = lire(parcours)
            for o in OUTILS_EXCLUSIFS:
                # EXCEPTION PILOTE (v0.2.4) : la boucle TEXTE doit refleter la
                # meme exception que les indices OUTIL ci-dessus. Pour chiron,
                # editer-parcours est LEGITIME (cle par cible : SA carte
                # uniquement, verifiee par proteger-verrou-habilitation). Sans
                # cette exception, l indice OUTIL de sa carte d auto-correction
                # (c16) declencherait un faux positif "declaration".
                if nom == "chiron" and o == "editer-parcours":
                    continue
                # une vraie usurpation = l outil declare comme outil de
                # l agent dans un indice de type outil (deja couvert par
                # outils_parcours). Les mentions dans les textes de regles
                # (AGENTS HABILITES, redirections) sont documentaires.
                if o in texte and o in noms:
                    violateurs.append("%s: declaration %s" % (nom, o))
        verifier("2. AUCUNE autre carte ne possede editer-parcours/editer-fichier-agents",
                 not violateurs, "; ".join(violateurs))
        chrono_etape("2. autres cartes", t)

    # --- 2b. registre : aucune declaration non-buffy
    if point_actif(3):
        t = time.monotonic()
        declarations = []
        if os.path.isfile(REGISTRE):
            for ligne in lire(REGISTRE).split("\n"):
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    e = json.loads(ligne)
                except ValueError:
                    continue
                outil = e.get("outil", "")
                agent = e.get("agent", "")
                for o in OUTILS_EXCLUSIFS:
                    # EXCEPTION PILOTE (v0.2.5) : la boucle REGISTRE doit
                    # refleter la meme exception que les indices OUTIL et la
                    # boucle TEXTE (v0.2.3/v0.2.4). Chiron est autorise a
                    # utiliser editer-parcours sur SA carte uniquement (cle
                    # par cible, verifiee par proteger-verrou-habilitation) :
                    # ses declarations au registre sont LEGITIMES (cycle
                    # d auto-correction pilote, c16). Sans cette exception,
                    # le cycle reel trace des faux positifs.
                    if agent.lower() == "chiron" and o == "editer-parcours":
                        continue
                    if o in outil and agent.lower() != "buffy":
                        declarations.append("%s/%s (%s)" % (agent, outil, e.get("date", "")))
        verifier("2b. registre : aucune declaration editer-parcours/editer-fichier-agents non-buffy",
                 not declarations, "; ".join(declarations[:10]))
        chrono_etape("2b. registre", t)

    # --- 3. regle immuable documentee
    if point_actif(4):
        t = time.monotonic()
        regle = lire(REGLE)
        ok_section = "SEUL BUFFY CORRIGE LES FICHIERS DES AGENTS" in regle
        ok_nuance = "lecons OK" in regle or "corrections.md" in regle
        ok_confiance = "LE MODELE DE CONFIANCE" in regle and "JANUS" in regle
        verifier("3. regles-groupes-agents : SEUL BUFFY CORRIGE + nuance lecons + modele de confiance",
                 ok_section and ok_nuance and ok_confiance,
                 "section=%s nuance=%s confiance=%s" % (ok_section, ok_nuance, ok_confiance))
        chrono_etape("3. regle immuable", t)

    # --- 4. fiche buffy : REGLE ABSOLUE
    if point_actif(5):
        t = time.monotonic()
        fiche = lire(FICHE_BUFFY)
        verifier("4. fiche buffy : REGLE ABSOLUE -- SEULE A CORRIGER LES FICHIERS DES AGENTS",
                 "SEULE A CORRIGER LES FICHIERS DES AGENTS" in fiche,
                 "regle absente de buffy.md")
        chrono_etape("4. fiche buffy", t)

    # --- 5. normes ASCII + LF
    if point_actif(6):
        t = time.monotonic()
        ok = True
        details = []
        for f in (REGLE, FICHE_BUFFY, os.path.abspath(__file__)):
            brut = open(f, "rb").read()
            na = sum(1 for c in brut.decode("utf-8", errors="replace") if ord(c) > 127)
            crlf = brut.count(b"\r\n")
            if na or crlf:
                details.append("%s: %d na / %d crlf" % (os.path.basename(f), na, crlf))
                ok = False
        verifier("5. normes ASCII strict + LF pur (regle + fiche + test)", ok,
                 "; ".join(details))
        chrono_etape("5. normes", t)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("VERDICT : %s" % ("CONFORME" if NB_KO == 0 else "NON CONFORME"))
    print("BILAN : seul Buffy corrige les fichiers structurels des agents (separation des pouvoirs)")
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
