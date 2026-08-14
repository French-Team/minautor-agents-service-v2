#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-055-coherence-regle-indice-outil.py
GARDE-FOU ANTI-RECURRENCE : la COHERENCE REGLE / INDICE OUTIL sur toutes les
cartes de decision (parcours JSON des agents).

Contexte (2026-08-15) :
  - L ecart carte vulcain c4 a revele un trou dans les garde-fous : la case
    c4 contenait une REGLE (indice type "regle") ordonnant l usage de
    outil-template mais AUCUN indice outil correspondant dans la case ->
    evaluer-processus signalait OUTIL_HORS_CARTE a chaque usage declare.
  - La correction (Buffy) a ajoute l indice outil dans la MEME case : la
    convention est donc le NIVEAU CASE - une regle qui ordonne l usage d un
    outil doit porter l indice outil dans la meme case (l agent y trouve le
    chemin vers la doc).
  - Sonde reelle (Cerberus) : 52 mentions d outils dans les textes de regles
    des 13 cartes, dont 6 SANS indice outil dans la meme case (etat
    initial) : buffy c10c generateurs-case, clio c20 valider-conformite-
    ascii, janus c16 changer-statut, vulcain c2 verifier-systeme, vulcain
    c7 corriger-symboles + combos-moteur. Ce test les DETECTE (preuve
    reelle de detection) ; Buffy les corrige ensuite.

REGLE VERIFIEE :
  Pour chaque parcours (13 agents), chaque case, chaque indice de type
  "regle" : tout nom d outil canonique mentionne dans le texte de la regle
  (frontiere de mot) doit avoir un indice de type "outil" (nom identique)
  dans la MEME case. Sinon -> KO (agent, case, outil).

LISTE CANONIQUE DES OUTILS :
  noms du catalogue generateurs-commande (catalogue-commandes.json, champ
  "nom") + outil-template (le template de creation, hors catalogue car ce
  n est pas une commande - protocole-outils).

Invariants verifies :
  1. Liste canonique : outil-template inclus (hors catalogue)
  2. Liste canonique : >= 150 outils du catalogue charges
  3. Detection : 0 incoherence regle/indice outil sur les 13 cartes
     (KO sur l etat initial : 6 ecarts - preuve reelle de detection)
  4. Preuve de detection (synthetique permanente) : les 6 outils connus
     sont dans la liste canonique et detectables (independante de l etat
     reel des cartes)
  5. Preuve positive : vulcain c4 (regle outil-template + indice outil) OK
  6. Preuve negative logique : regle mentionnant un outil SANS indice dans
     une structure synthetique -> detectee
  7. Preuve positive logique : regle mentionnant un outil AVEC indice dans
     une structure synthetique -> non detectee
  8. Fantomes : 0 indice avec nom sans type sur les 13 cartes (etat propre)
  9. Preuve negative fantome : indice {nom} sans type -> detecte
     (structure synthetique)
  10. Preuve positive fantome : indice {nom, type outil} -> non detecte
      (structure synthetique)
  11. ASCII strict : 0 non-ASCII (test + catalogue)
  12. LF pur : 0 CRLF (test + catalogue)

INDICES FANTOMES (lecon c10c, 2026-08-15) :
  Un indice avec champ nom mais SANS champ type est un FANTOME : invisible
  pour la detection (type=='outil') et pour evaluer-processus. La case
  buffy c10c portait un indice generateurs-case sans type - c est la
  cause racine du KO test-016 (plus de 3 indices apres ajout d un doublon).
  La correction : type:'outil' ajoute a l indice d origine. Ce test verifie
  qu aucun fantome ne subsiste sur les 13 cartes.
"""
import glob
import importlib.util
import io
import json
import os
import re
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
PARCOURS_GLOB = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "*",
                             "parcours", "parcours-*.json")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0
POINT_ACTIF = None
DESACTIVES = set()

# Les 6 ecarts connus au moment de la creation (etat initial, sonde Cerberus).
# Apres la correction Buffy, ils doivent disparaitre de la detection.
ECARTS_CONNUS = [
    ("buffy", "c10c", "generateurs-case"),
    ("clio", "c20", "valider-conformite-ascii"),
    ("janus", "c16", "changer-statut"),
    ("vulcain", "c2", "verifier-systeme"),
    ("vulcain", "c7", "corriger-symboles"),
    ("vulcain", "c7", "combos-moteur"),
]


def chrono_etape(nom, duree):
    print("  [chrono] %-40s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if POINT_ACTIF is not None and NB_POINTS != POINT_ACTIF:
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


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def charger_outils():
    """Liste canonique : noms du catalogue + outil-template (hors catalogue)."""
    with io.open(CATALOGUE, encoding="utf-8") as fh:
        cat = json.load(fh)
    outils = set(c["nom"] for c in cat["commandes"])
    outils.add("outil-template")
    return outils


def construire_pattern(outils):
    """Tri par longueur decroissante : le nom le plus long gagne si un nom
    est prefixe d un autre. Frontiere de mot [a-z0-9-]."""
    return re.compile(r"(?<![a-z0-9-])(" + "|".join(
        re.escape(o) for o in sorted(outils, key=len, reverse=True)
    ) + r")(?![a-z0-9-])")


def detecter_cases(cases, pattern, outils):
    """Ecarts (cid, outil) d un parcours : outil mentionne dans une regle
    sans indice outil dans la meme case. `outils` sert de reference
    documentaire (tout nom matche est un nom connu)."""
    ecarts = []
    for cid, c in sorted(cases.items()):
        indices = c.get("indices", []) if isinstance(c, dict) else []
        outils_case = set(i.get("nom") for i in indices
                          if i.get("type") == "outil")
        for ind in indices:
            if ind.get("type") != "regle":
                continue
            for m in pattern.findall(ind.get("texte", "")):
                if m not in outils_case:
                    ecarts.append((cid, m))
    return ecarts


def detecter_fantomes(cases):
    """Indices fantomes (cid, nom) : un indice avec champ nom mais SANS champ
    type est invisible pour la detection (type=='outil') et pour
    evaluer-processus - lecon c10c (generateurs-case sans type)."""
    fantomes = []
    for cid, c in sorted(cases.items()):
        indices = c.get("indices", []) if isinstance(c, dict) else []
        for ind in indices:
            if ind.get("nom") and not ind.get("type"):
                fantomes.append((cid, ind.get("nom")))
    return fantomes


def scanner_fantomes():
    """Scan reel : fantomes (agent, cid, nom) sur toutes les cartes."""
    resultats = []
    for pf in sorted(glob.glob(PARCOURS_GLOB)):
        agent = os.path.basename(pf)[len("parcours-"):-len(".json")]
        with io.open(pf, encoding="utf-8") as fh:
            parcours = json.load(fh)
        for cid, nom in detecter_fantomes(parcours.get("cases", {})):
            resultats.append((agent, cid, nom))
    return resultats


def scanner_parcours():
    """Scan reel : ecarts (agent, cid, outil) sur toutes les cartes."""
    outils = charger_outils()
    pattern = construire_pattern(outils)
    resultats = []
    for pf in sorted(glob.glob(PARCOURS_GLOB)):
        agent = os.path.basename(pf)[len("parcours-"):-len(".json")]
        with io.open(pf, encoding="utf-8") as fh:
            parcours = json.load(fh)
        for cid, outil in detecter_cases(parcours.get("cases", {}),
                                         pattern, outils):
            resultats.append((agent, cid, outil))
    return resultats, outils, pattern


def main():
    global POINT_ACTIF, DESACTIVES
    t0 = time.time()
    import argparse
    ap = argparse.ArgumentParser(description="test-055 coherence regle/indice outil")
    ap.add_argument("--isoler", type=int, default=None)
    ap.add_argument("--desactiver", default="")
    ap.add_argument("--chrono", action="store_true")
    args = ap.parse_args()
    POINT_ACTIF = args.isoler
    DESACTIVES = set(int(x) for x in args.desactiver.split(",") if x.strip())

    outils = charger_outils()
    pattern = construire_pattern(outils)

    # 1-2. Liste canonique complete
    verifier("1. liste canonique : outil-template inclus (hors catalogue)",
             "outil-template" in outils)
    verifier("2. liste canonique : >= 150 outils du catalogue charges",
             len(outils) >= 150, "nb=%d" % len(outils))

    # 3. Detection reelle sur les 13 cartes (etat courant)
    ecarts, _, _ = scanner_parcours()
    detail = "; ".join("%s %s -> %s" % e for e in sorted(ecarts))
    verifier("3. coherence regle/indice outil : 0 ecart sur les 13 cartes",
             len(ecarts) == 0, "ecarts=%d : %s" % (len(ecarts), detail))

    # 4. Preuve de detection PERMANENTE (structure synthetique) : les 6
    #    outils qui etaient incoherents doivent etre dans la liste canonique
    #    ET detectables par la mecanique (regle mentionnant l outil sans
    #    indice -> KO). Independante de l etat reel des cartes : la preuve
    #    reste verte meme apres la correction Buffy (point 3).
    trouves = set(ecarts)
    non_detectes = []
    for _, _, outil in ECARTS_CONNUS:
        if outil not in outils:
            non_detectes.append("%s hors liste canonique" % outil)
            continue
        synth = {"x1": {"type": "action", "suivant": "x2",
                         "indices": [{"type": "regle",
                                      "texte": "j utilise TOUJOURS %s pour cette etape" % outil}]}}
        if ("x1", outil) not in detecter_cases(synth, pattern, outils):
            non_detectes.append(outil)
    verifier("4. preuve detection : les %d outils connus sont dans la liste "
             "canonique et detectables" % len(ECARTS_CONNUS),
             len(non_detectes) == 0,
             "non detectes: %s" % (non_detectes if non_detectes else "aucun"))

    # 5. Preuve positive : vulcain c4 (regle outil-template + indice outil)
    verifier("5. preuve positive : vulcain c4 (mention outil-template couverte "
             "par son indice) non signale",
             ("vulcain", "c4", "outil-template") not in trouves,
             "l indice c4 outil-template est present, ne doit PAS etre signale")

    # 6-7. Preuves logiques sur structure synthetique (aucun fichier touche)
    synth_sans = {"x1": {"type": "action", "suivant": "x2",
                         "indices": [{"type": "regle",
                                      "texte": "j utilise TOUJOURS valider-case pour valider"}]}}
    ec = detecter_cases(synth_sans, pattern, outils)
    verifier("6. preuve negative logique : regle sans indice outil -> detectee",
             ("x1", "valider-case") in ec, "ecarts=%s" % ec)

    synth_avec = {"x1": {"type": "action", "suivant": "x2",
                         "indices": [
                             {"type": "regle",
                              "texte": "j utilise TOUJOURS valider-case pour valider"},
                             {"type": "outil", "nom": "valider-case",
                              "chemin": "cerveau-projet/agents/tools/valider/valider-case/"}]}}
    ec = detecter_cases(synth_avec, pattern, outils)
    verifier("7. preuve positive logique : regle avec indice outil -> non detectee",
             len(ec) == 0, "ecarts=%s" % ec)

    # 8. Fantomes : detection reelle (etat actuel propre - 0 fantome)
    fantomes = scanner_fantomes()
    detail_f = "; ".join("%s %s -> %s" % f for f in sorted(fantomes))
    verifier("8. indices fantomes (nom sans type) : 0 sur les 13 cartes",
             len(fantomes) == 0, "fantomes=%d : %s" % (len(fantomes), detail_f))

    # 9-10. Preuves logiques fantomes (structure synthetique, aucun fichier)
    synth_fant = {"x1": {"type": "action", "suivant": "x2",
                          "indices": [{"nom": "valider-case",
                                       "chemin": "cerveau-projet/agents/tools/valider/valider-case/"}]}}
    fg = detecter_fantomes(synth_fant)
    verifier("9. preuve negative fantome : indice {nom} sans type -> detecte",
             ("x1", "valider-case") in fg, "fantomes=%s" % fg)

    synth_fant2 = {"x1": {"type": "action", "suivant": "x2",
                           "indices": [{"type": "outil", "nom": "valider-case",
                                        "chemin": "cerveau-projet/agents/tools/valider/valider-case/"}]}}
    fg = detecter_fantomes(synth_fant2)
    verifier("10. preuve positive fantome : indice {nom, type outil} -> non detecte",
             len(fg) == 0, "fantomes=%s" % fg)

    # 11-12. Normes : ASCII strict + LF pur
    fichiers = [os.path.abspath(__file__), CATALOGUE]
    na = sum(ascii_count(f) for f in fichiers)
    cr = sum(crlf_count(f) for f in fichiers)
    verifier("11. ASCII strict : 0 non-ASCII", na == 0, "na=%d" % na)
    verifier("12. LF pur : 0 CRLF", cr == 0, "crlf=%d" % cr)

    if args.chrono:
        chrono_etape("test-055 coherence regle/indice outil",
                     time.time() - t0)
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
