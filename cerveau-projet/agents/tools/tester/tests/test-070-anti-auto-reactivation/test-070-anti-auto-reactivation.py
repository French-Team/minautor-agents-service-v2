#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-070-anti-auto-reactivation.py
GARDE-FOU : aucune fin de carte ne doit reactiver l agent SUR LUI-MEME
(auto-reactivation = boucle infinie qui stoppe le round) ni afficher une
incoherence message/commande (message dit X, commande reactiver vise Y).

Contexte (mission 2026-08-16) :
  - Le bug argus c29e a revele que la commande reactiver session-llm-1
    '<raison>' argus reactivait ARGUS SUR LUI-MEME au lieu de cerberus,
    pendant que le message disait "signaler a Cerberus".
    Resultat : boucle infinie, le round ne repart jamais.
  - La correction (Buffy) a transforme c29e (reactiver cerberus) mais on
    veut empecher la recurrence : le scan manuel de 93 fins prend < 1s,
    on le mechanise.

Invariants verifies :
  1. Chaque carte a un message reactiver coherent : si le message contient
     'Cerberus' ou 'cerberus', la cible de reactiver est cerberus
     (et inversement : cible cerberus -> message le mentionne).
  2. Aucune auto-reactivation : reactiver session-llm-1 ... <agent> ne vise
     JAMAIS l agent de la carte elle-meme.
  3. Les fins 'FIN - Activer X' contiennent activer (jamais reactiver) vers
     un agent AUTRE que soi.
  4. Preuve negative : une copie de carte avec auto-reactivation injectee
     est DETECTEE par le scan interne (injection detectee), puis SUPPRIMEE
     (0 residu en fin de test).
  5. Normes : ASCII strict + LF pur (fichiers de test + parcours).
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
NB_POINTS = 7


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
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def analyser_fin(agent, cid, c):
    """Analyse une case de fin : retourne la liste des problemes detectes.

    Retourne une liste de tuples (type, detail) :
      - AUTO_REACTIVATION : reactiver vise l agent lui-meme
      - INCOHERENCE_MESSAGE : message mentionne Cerberus mais cible != cerberus
      - FIN_ACTIVER_REACTIVER : fin 'Activer X' contient reactiver
    """
    problemes = []
    msg = c.get("message", "")
    titre = c.get("titre", "")

    # Commande reactiver session-llm-1 '<raison>' <agent>
    m_react = re.search(r"reactiver\s+session-llm-1\s+[^ ]+\s+(\w+)", msg)
    if m_react:
        cible = m_react.group(1)
        if cible == agent:
            problemes.append(("AUTO_REACTIVATION",
                              "%s %s : reactiver vise %s (soi-meme)" %
                              (agent, cid, cible)))
        # Coherence message/commande : si le message dit Cerberus...
        if "erberus" in msg and cible != "cerberus":
            problemes.append(("INCOHERENCE_MESSAGE",
                              "%s %s : message dit Cerberus mais cible=%s" %
                              (agent, cid, cible)))
        if "erberus" not in msg and cible == "cerberus":
            problemes.append(("INCOHERENCE_MESSAGE",
                              "%s %s : cible cerberus mais message ne le dit pas" %
                              (agent, cid)))

    # Fin 'FIN - Activer X' : ne doit PAS contenir une COMMANDE reactiver
    # (le mot 'reactiver' peut apparaitre dans une explication de regle,
    #  ex: 'PAS reactiver - reactiver ramene toujours a Cerberus')
    if titre.startswith("FIN - Activer") or titre.startswith("FIN - ACTIVER"):
        if re.search(r"reactiver\s+session-llm-1", msg):
            problemes.append(("FIN_ACTIVER_REACTIVER",
                              "%s %s : fin Activer contient commande reactiver" %
                              (agent, cid)))

    return problemes


def scanner_toutes_les_cartes(racine_parcours):
    """Scanne toutes les cartes et retourne la liste des problemes."""
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
            if c.get("type") != "fin":
                continue
            problemes.extend(analyser_fin(agent, cid, c))
    return problemes


def main():
    print("=== Garde-fou : anti-auto-reactivation des fins de cartes ===")

    # 1. Scan de toutes les cartes : 0 auto-reactivation
    t0 = time.monotonic()
    problemes = scanner_toutes_les_cartes(PARCOURS_GLOB)
    auto = [p for p in problemes if p[0] == "AUTO_REACTIVATION"]
    verifier("1. scan complet : 0 auto-reactivation",
             len(auto) == 0,
             auto[:3] if auto else "")
    chrono_etape("1. scan auto-reactivation", t0)

    # 2. 0 incoherence message/commande
    t0 = time.monotonic()
    incoherents = [p for p in problemes if p[0] == "INCOHERENCE_MESSAGE"]
    verifier("2. scan complet : 0 incoherence message/commande",
             len(incoherents) == 0,
             incoherents[:3] if incoherents else "")
    chrono_etape("2. scan incoherence", t0)

    # 3. Les fins 'FIN - Activer X' n'utilisent jamais reactiver
    t0 = time.monotonic()
    fin_activer = [p for p in problemes if p[0] == "FIN_ACTIVER_REACTIVER"]
    verifier("3. fins 'FIN - Activer X' : jamais de reactiver",
             len(fin_activer) == 0,
             fin_activer[:3] if fin_activer else "")
    chrono_etape("3. scan fins Activer", t0)

    # 4. Preuve negative : injection d'une auto-reactivation detectee
    t0 = time.monotonic()
    tmp = tempfile.mkdtemp(prefix="tmp-test070-")
    try:
        # Copier le parcours cerberus et injecter une auto-reactivation
        src = None
        for f in glob.glob(PARCOURS_GLOB):
            if "parcours-cerberus.json" in f:
                src = json.load(io.open(f, encoding="utf-8"))
                break
        if src is None:
            verifier("4. preuve negative : copie trouvee", False, "parcours cerberus introuvable")
        else:
            cible_case = None
            for cid, c in src["cases"].items():
                if isinstance(c, dict) and c.get("type") == "fin":
                    cible_case = cid
                    break
            if cible_case is None:
                verifier("4. preuve negative : case fin trouvee", False, "aucune fin")
            else:
                src["cases"][cible_case]["message"] = (
                    "Je signale a Cerberus : python3 outil.py reactiver "
                    "session-llm-1 '<raison>' cerberus.")
                # injection d une auto-reactivation dans une copie nommee
                # parcours-cerberus.json pour simuler la carte de cerberus
                sous = os.path.join(tmp, "parcours-cerberus.json")
                with io.open(sous, "w", encoding="utf-8", newline="\n") as fh:
                    json.dump(src, fh, ensure_ascii=True, indent=1)
                # scanner la copie avec le meme agent (cerberus)
                problemes_copie = []
                p = json.load(io.open(sous, encoding="utf-8"))
                for cid2, c2 in p["cases"].items():
                    if isinstance(c2, dict) and c2.get("type") == "fin":
                        problemes_copie.extend(analyser_fin("cerberus", cid2, c2))
                # la fin modifiee ne doit PAS etre une auto-reactivation
                # (cible cerberus == agent cerberus) -> detecter ce cas aussi
                auto_copie = [x for x in problemes_copie
                              if x[0] == "AUTO_REACTIVATION"]
                # ajouter une vraie auto-reactivation (cible argus dans carte argus)
                sous2 = os.path.join(tmp, "parcours-argus.json")
                p2 = json.load(io.open(
                    os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "argus", "parcours", "parcours-argus.json"),
                    encoding="utf-8"))
                for cid2, c2 in p2["cases"].items():
                    if isinstance(c2, dict) and c2.get("type") == "fin":
                        c2["message"] = ("reactiver session-llm-1 "
                                         "'<raison>' argus.")
                with io.open(sous2, "w", encoding="utf-8", newline="\n") as fh:
                    json.dump(p2, fh, ensure_ascii=True, indent=1)
                p3 = json.load(io.open(sous2, encoding="utf-8"))
                problemes2 = []
                for cid3, c3 in p3["cases"].items():
                    if isinstance(c3, dict) and c3.get("type") == "fin":
                        problemes2.extend(analyser_fin("argus", cid3, c3))
                auto2 = [x for x in problemes2 if x[0] == "AUTO_REACTIVATION"]
                verifier("4. preuve negative : auto-reactivation injectee DETECTEE",
                         len(auto2) > 0,
                         auto2[:2] if auto2 else "non detectee")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("4b. preuve negative : copie SUPPRIMEE (0 trace)",
                 not os.path.exists(tmp), "copie encore presente")
    chrono_etape("4. preuve negative", t0)

    # 5. Normes ASCII + LF (test + parcours modifies)
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
    verifier("5. normes : 0 non-ASCII (test + parcours)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("5b. normes : 0 CRLF (test + parcours)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("5. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" %
          (NB_OK, NB_KO, NB_POINTS))
    bilan_chrono()
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
