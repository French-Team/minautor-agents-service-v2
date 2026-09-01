#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-070-anti-auto-reactivation.py
GARDE-FOU : TOUTES les cases de carte (pas seulement les fins) doivent
respecter la regle de reactivation :
  - La commande `reactiver session-llm-1 <raison> <agent>` ramene TOUJOURS
    a Cerberus (le 3e argument est informatif, pas la cible).
  - Aucune auto-reactivation : reactiver ne vise JAMAIS l agent de la carte
    elle-meme (boucle infinie qui stoppe le round).
  - Aucune forme fautive : 'reactiver X' avec X != cerberus, ou
    'me/le/la reactiverai(ez)' / 'me/le/la REACTIVE' visant un agent
    autre que Cerberus (sauf explications correctes : 'PAS reactiver',
    'reactiver ramene toujours a Cerberus', '(commande activer)').
  - Coherence message/commande (message dit Cerberus mais cible != cerberus).

Contexte (mission 2026-08-16, suite) :
  - Le bug argus c29e a revele que la commande reactiver session-llm-1
    '<raison>' argus reactivait ARGUS SUR LUI-MEME au lieu de cerberus.
  - La premiere version de ce garde-fou ne scannait QUE les cases de type
    'fin' : toutes les mentions fautives dans les cases action/regle
    echappaient au scan (cerberus c12b 'reactiver Buffy', argus c29a
    'il me reactivera', les boucles KO Janus/Themis 'je le/la reactiverai',
    'Themis me REACTIVE', etc.).
  - Buffy a corrige 31 cases fautives (11 parcours, bumps + fiches
    Pattern 14). Ce garde-fou etendu scannent TOUTES les cases pour
    empecher la recurrence.

Invariants verifies :
  1. Scan complet (TOUTES les cases des 15 parcours) : 0 auto-reactivation.
  2. Scan complet : 0 commande reactiver avec cible != cerberus.
  3. Scan complet : 0 forme fautive (conjuguees + present REACTIVE)
     visant un agent autre que Cerberus.
  4. Scan complet : 0 incoherence message/commande.
  5. Les fins 'FIN - Activer X' ne contiennent jamais une commande reactiver.
  5b. Les fins 'FIN - Reactiver Cerberus' n existent que chez janus (REGLE
      IMMUABLE JANUS : les agents cerveau-projet activent JANUS en fin).
  6. Preuve negative : injection d'une violation (commande reactiver cible
     non-cerberus + forme 'me REACTIVE' + auto-reactivation + fin Reactiver
     hors janus) DETECTEE puis copie SUPPRIMEE.
  7. Normes : ASCII strict + LF pur (test + parcours).
Tags: agents, parcours, garde-fou, anti-recurrence
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
PARCOURS_GLOB = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "*",
                             "parcours", "parcours-*.json")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 13


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-070 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-120:]))


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()

# Motifs de detection
M_CMD = re.compile(r"reactiver\s+session-llm-1\s+[^\s]+\s+(\w+)",
                   re.IGNORECASE)
M_FORME = re.compile(r"(?:me|le|la|te)\s+reactiverai\w*|"
                     r"(?:il|elle)\s+me\s+reactivera\w*", re.IGNORECASE)
M_PRESENT = re.compile(r"(?:me|le|la)\s+RE-?ACTIVE\b", re.IGNORECASE)
M_FIN_ACTIVER = re.compile(r"reactiver\s+session-llm-1", re.IGNORECASE)


def texte_case(c):
    """Concatene les champs texte d'une case (message, titre, regle)."""
    return " ".join(str(c.get(k, "")) for k in
                    ("message", "titre", "indice_regle", "indice_outil"))


def analyser_case(agent, cid, c):
    """Analyse UNE case (quel que soit son type) : retourne les problemes.

    Retourne une liste de tuples (type, detail) :
      - AUTO_REACTIVATION : reactiver vise l agent lui-meme
      - REACTIVER_NON_CERBERUS : commande reactiver vise un agent != cerberus
      - FORME_FAUTIVE : forme conjuguee ou present visant un agent != cerberus
      - INCOHERENCE_MESSAGE : message mentionne Cerberus mais cible != cerberus
      - FIN_ACTIVER_REACTIVER : fin 'Activer X' contient commande reactiver
    """
    problemes = []
    msg = c.get("message", "")
    titre = c.get("titre", "")

    # 1. Commande reactiver session-llm-1 '<raison>' <agent>
    m_react = M_CMD.search(msg)
    if m_react:
        cible = m_react.group(1)
        if cible == agent:
            problemes.append(("AUTO_REACTIVATION",
                              "%s %s : reactiver vise %s (soi-meme)" %
                              (agent, cid, cible)))
        if cible != "cerberus":
            problemes.append(("REACTIVER_NON_CERBERUS",
                              "%s %s : commande reactiver cible %s "
                              "(reactiver ramene toujours a Cerberus)" %
                              (agent, cid, cible)))
        if "erberus" in msg and cible != "cerberus":
            problemes.append(("INCOHERENCE_MESSAGE",
                              "%s %s : message dit Cerberus mais cible=%s" %
                              (agent, cid, cible)))
        if "erberus" not in msg and cible == "cerberus":
            problemes.append(("INCOHERENCE_MESSAGE",
                              "%s %s : cible cerberus mais message ne le dit pas" %
                              (agent, cid)))

    # 2. Formes conjuguees fautives : 'me/le/la reactiverai(ez)' ou
    #    'il/elle me reactivera' sans cible Cerberus immediate
    for m in M_FORME.finditer(msg):
        apres = msg[m.end():m.end() + 50]
        if re.search(r"cerberus", apres, re.IGNORECASE):
            continue  # cible Cerberus explicite -> OK
        if re.search(r"PAS reactiver|ramene toujours a Cerberus",
                     msg[max(0, m.start() - 60):m.end() + 120],
                     re.IGNORECASE):
            continue  # explication correcte
        problemes.append(("FORME_FAUTIVE",
                          "%s %s : '%s' vise un agent autre que Cerberus" %
                          (agent, cid, m.group(0))))

    # 3. Present 'me/le/la REACTIVE' (ou RE-ACTIVE) avec cible non Cerberus
    for m in M_PRESENT.finditer(msg):
        apres = msg[m.end():m.end() + 90]
        avant = msg[max(0, m.start() - 70):m.end()]
        if re.search(r"commande activer|PAS reactiver|"
                     r"ramene toujours a Cerberus", apres + avant,
                     re.IGNORECASE):
            continue  # formulation correcte ou explication
        if re.search(r"reactive\s+cerberus", apres, re.IGNORECASE):
            continue  # 'reactivera Cerberus' -> cible Cerberus
        # INTER-ROUND (protocole-fin-mission v0.2.0) : quand une case decrit
        # le protocole inter-round, 'me/le/la REACTIVE' designe l HABILITE qui
        # reactive l APPELANT (moi = l appelant) - ce n est PAS une cible
        # non-Cerberus fautive. Exemption si le contexte immediat mentionne
        # l inter-round (l habilite reactive l appelant, pas un agent tiers).
        if re.search(r"inter-round|inter round|interround",
                     apres + avant, re.IGNORECASE):
            continue  # protocole inter-round : l habilite reactive l appelant
        problemes.append(("FORME_FAUTIVE",
                          "%s %s : '%s' vise un agent autre que Cerberus" %
                          (agent, cid, m.group(0))))

    # 4. Fin 'FIN - Activer X' : ne doit PAS contenir une COMMANDE reactiver
    if titre.startswith("FIN - Activer") or titre.startswith("FIN - ACTIVER"):
        if M_FIN_ACTIVER.search(msg):
            problemes.append(("FIN_ACTIVER_REACTIVER",
                              "%s %s : fin Activer contient commande reactiver" %
                              (agent, cid)))

    # 5. Fin 'FIN - Reactiver Cerberus' : uniquement chez janus (REGLE
    #    IMMUABLE JANUS : les agents cerveau-projet activent JANUS en fin,
    #    pas Cerberus directement - sauf janus qui reactive Cerberus).
    if (titre.startswith("FIN - Reactiver Cerberus") or
            titre.startswith("FIN - REACTIVER Cerberus")):
        if agent != "janus":
            problemes.append(("FIN_REACTIVER_NON_JANUS",
                              "%s %s : fin Reactiver Cerberus hors janus "
                              "(REGLE IMMUABLE JANUS : activer Janus)" %
                              (agent, cid)))

    return problemes


def scanner_toutes_les_cartes(racine_parcours):
    """Scanne TOUTES les cases de toutes les cartes."""
    problemes = []
    for f in sorted(glob.glob(racine_parcours)):
        try:
            p = json.load(io.open(f, encoding="utf-8"))
        except Exception as e:
            problemes.append(("JSON_INVALIDE", "%s : %s" % (f, str(e)[-60:])))
            continue
        parts = f.replace(os.sep, "/").split("/")
        agent = parts[-1].replace("parcours-", "").replace(".json", "")
        for cid, c in p.get("cases", {}).items():
            if not isinstance(c, dict):
                continue
            problemes.extend(analyser_case(agent, cid, c))
    return problemes


def main():
    print("=== Garde-fou : anti-auto-reactivation (TOUTES les cases) ===")

    # 1. Scan complet : 0 auto-reactivation
    t0 = time.monotonic()
    problemes = scanner_toutes_les_cartes(PARCOURS_GLOB)
    auto = [p for p in problemes if p[0] == "AUTO_REACTIVATION"]
    verifier("1. scan complet : 0 auto-reactivation",
             len(auto) == 0, auto[:3] if auto else "")
    chrono_etape("1. scan auto-reactivation", t0)

    # 2. 0 commande reactiver avec cible != cerberus
    t0 = time.monotonic()
    non_cerberus = [p for p in problemes if p[0] == "REACTIVER_NON_CERBERUS"]
    verifier("2. scan complet : 0 reactiver cible non-Cerberus",
             len(non_cerberus) == 0,
             non_cerberus[:3] if non_cerberus else "")
    chrono_etape("2. scan reactiver non-cerberus", t0)

    # 3. 0 forme fautive (conjuguees + present)
    t0 = time.monotonic()
    formes = [p for p in problemes if p[0] == "FORME_FAUTIVE"]
    verifier("3. scan complet : 0 forme fautive (me/le/la reactivera/REACTIVE)",
             len(formes) == 0, formes[:3] if formes else "")
    chrono_etape("3. scan formes fautives", t0)

    # 4. 0 incoherence message/commande
    t0 = time.monotonic()
    incoherents = [p for p in problemes if p[0] == "INCOHERENCE_MESSAGE"]
    verifier("4. scan complet : 0 incoherence message/commande",
             len(incoherents) == 0,
             incoherents[:3] if incoherents else "")
    chrono_etape("4. scan incoherence", t0)

    # 5. Les fins 'FIN - Activer X' n'utilisent jamais reactiver
    t0 = time.monotonic()
    fin_activer = [p for p in problemes if p[0] == "FIN_ACTIVER_REACTIVER"]
    verifier("5. fins 'FIN - Activer X' : jamais de reactiver",
             len(fin_activer) == 0,
             fin_activer[:3] if fin_activer else "")
    chrono_etape("5. scan fins Activer", t0)

    # 5b. Les fins 'FIN - Reactiver Cerberus' n'existent que chez janus
    t0 = time.monotonic()
    fin_reactiver = [p for p in problemes if p[0] == "FIN_REACTIVER_NON_JANUS"]
    verifier("5b. fins 'FIN - Reactiver Cerberus' : uniquement janus",
             len(fin_reactiver) == 0,
             fin_reactiver[:3] if fin_reactiver else "")
    chrono_etape("5b. scan fins Reactiver", t0)

    # 6. Preuve negative : injections detectees puis copie supprimee
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test070-")
    try:
        # 6a. Injection 1 : commande reactiver cible non-cerberus
        #     (copie de la carte argus)
        src = json.load(io.open(
            os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "argus",
                         "parcours", "parcours-argus.json"),
            encoding="utf-8"))
        for cid2, c2 in src["cases"].items():
            if isinstance(c2, dict):
                c2["message"] = (c2.get("message", "") + " "
                                 "reactiver session-llm-1 '<raison>' atlas.")
        sous1 = os.path.join(tmp, "parcours-argus.json")
        with io.open(sous1, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(src, fh, ensure_ascii=True, indent=1)
        p1 = json.load(io.open(sous1, encoding="utf-8"))
        prob1 = []
        for cid3, c3 in p1["cases"].items():
            if isinstance(c3, dict):
                prob1.extend(analyser_case("argus", cid3, c3))
        detect1 = [x for x in prob1
                   if x[0] == "REACTIVER_NON_CERBERUS"]
        verifier("6a. preuve negative : reactiver cible non-cerberus "
                 "injecte DETECTE",
                 len(detect1) > 0,
                 detect1[:2] if detect1 else "non detecte")

        # 6b. Injection 2 : forme presente 'me REACTIVE' (cible Themis)
        #     dans une copie de la carte janus
        src2 = json.load(io.open(
            os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "janus",
                         "parcours", "parcours-janus.json"),
            encoding="utf-8"))
        for cid4, c4 in src2["cases"].items():
            if isinstance(c4, dict):
                c4["message"] = (c4.get("message", "") + " "
                                 "A SA fin, Themis me REACTIVE avec son "
                                 "rapport.")
        sous2 = os.path.join(tmp, "parcours-janus.json")
        with io.open(sous2, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(src2, fh, ensure_ascii=True, indent=1)
        p2 = json.load(io.open(sous2, encoding="utf-8"))
        prob2 = []
        for cid5, c5 in p2["cases"].items():
            if isinstance(c5, dict):
                prob2.extend(analyser_case("janus", cid5, c5))
        detect2 = [x for x in prob2 if x[0] == "FORME_FAUTIVE"]
        verifier("6b. preuve negative : forme 'me REACTIVE' injectee DETECTEE",
                 len(detect2) > 0,
                 detect2[:2] if detect2 else "non detectee")

        # 6c. Injection 3 : auto-reactivation (cible soi-meme)
        src3 = json.load(io.open(
            os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "argus",
                         "parcours", "parcours-argus.json"),
            encoding="utf-8"))
        for cid6, c6 in src3["cases"].items():
            if isinstance(c6, dict):
                c6["message"] = (c6.get("message", "") + " "
                                 "reactiver session-llm-1 '<raison>' argus.")
        sous3 = os.path.join(tmp, "parcours-argus.json")
        with io.open(sous3, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(src3, fh, ensure_ascii=True, indent=1)
        p3 = json.load(io.open(sous3, encoding="utf-8"))
        prob3 = []
        for cid7, c7 in p3["cases"].items():
            if isinstance(c7, dict):
                prob3.extend(analyser_case("argus", cid7, c7))
        detect3 = [x for x in prob3 if x[0] == "AUTO_REACTIVATION"]
        verifier("6c. preuve negative : auto-reactivation injectee DETECTEE",
                 len(detect3) > 0,
                 detect3[:2] if detect3 else "non detectee")

        # 6d. Injection 4 : fin 'Reactiver Cerberus' hors janus (buffy)
        #     -> doit etre signalee FIN_REACTIVER_NON_JANUS.
        src4 = json.load(io.open(
            os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "buffy",
                         "parcours", "parcours-buffy.json"),
            encoding="utf-8"))
        for cid8, c8 in src4["cases"].items():
            if isinstance(c8, dict) and c8.get("type") == "fin":
                c8["titre"] = "FIN - Reactiver Cerberus"
                break
        sous4 = os.path.join(tmp, "parcours-buffy.json")
        with io.open(sous4, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(src4, fh, ensure_ascii=True, indent=1)
        p4 = json.load(io.open(sous4, encoding="utf-8"))
        prob4 = []
        for cid9, c9 in p4["cases"].items():
            if isinstance(c9, dict):
                prob4.extend(analyser_case("buffy", cid9, c9))
        detect4 = [x for x in prob4 if x[0] == "FIN_REACTIVER_NON_JANUS"]
        verifier("6d. preuve negative : fin Reactiver hors janus injectee DETECTEE",
                 len(detect4) > 0,
                 detect4[:2] if detect4 else "non detectee")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("6e. preuve negative : copie SUPPRIMEE (0 trace)",
                 not os.path.exists(tmp), "copie encore presente")
    chrono_etape("6. preuves negatives", t0)

    # 7. Normes ASCII + LF (test + parcours modifies)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    fichiers = [os.path.abspath(__file__)]
    fichiers.extend(sorted(glob.glob(PARCOURS_GLOB)))
    for f in fichiers:
        try:
            d = io.open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("7. normes : 0 non-ASCII (test + parcours)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("7b. normes : 0 CRLF (test + parcours)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("7. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" %
          (NB_OK, NB_KO, NB_POINTS))
    if NB_KO:
        print("  [AIDE] OU CHERCHER / REPARER (KO = fin/forme de reactivation fautive) :")
        print("    [AIDE] Fichiers inspectes : agents/*/parcours/parcours-*.json (cases c14/c20 par ex)")
        print("    [AIDE] Diagnostic : lire le detail du KO (FIN_REACTIVER_NON_JANUS / FORME_FAUTIVE / REACTIVER_NON_CERBERUS) qui cite la case incriminee")
        print("    [AIDE] Correctif : seul janus a des fins 'FIN - Reactiver Cerberus' ; reformuler 'me/le/la REACTIVE' hors Cerberus ; les autres agents activent janus / suivent leur carte")
    bilan_chrono()
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
