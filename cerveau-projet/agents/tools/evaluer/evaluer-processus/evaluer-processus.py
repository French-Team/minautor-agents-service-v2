#!/usr/bin/env python3
# -*- coding: ascii -*-
# evaluer-processus.py
#
# Detecte les DERIVES DE PROCESSUS dans le cerveau-projet (lecon 2026-08-13 :
# 3 derives successives - Morpheus consignes, Cerberus outils hors carte,
# regle de fiche contradictoire). Cet outil croise les cartes (parcours JSON),
# les fiches agents, AGENTS.md et AGENTS-historique.md pour detecter :
#
#   1. FINS DE MISSION ERRONEES : un agent dont la carte impose une fin
#      'Activer Janus' mais dont la derniere mission ecrite (AGENTS.md ou
#      AGENTS-historique) porte 'reactiver Cerberus' en fin de consigne.
#   2. OUTILS HORS CARTE : un agent dont une lecon (corrections.md) declare
#      avoir utilise un outil qui n est assigne dans AUCUNE case de sa carte
#      (croisement indices outil des cartes vs mentions outils des lecons).
#   3. COHERENCE FICHE/CARTE : une regle ABSOLUE de fiche qui contredit la
#      carte (ex : clause 'je reactive Cerberus directement' alors que la
#      carte impose 'Activer Janus').
#
# Usage :
#   python3 evaluer-processus.py
#   python3 evaluer-processus.py --agent morpheus
#   python3 evaluer-processus.py --rapport rapport.md --verbose
#
# Options :
#   --agent <nom>       : restreindre a un agent
#   --rapport <fichier> : ecrit le rapport markdown
#   --verbose           : detail des outils assignes par carte
#   --version
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (evaluer-).
# =============================================================================
import argparse
import io
import json
import os
import re
import sys

VERSION = "0.1.0"

# Agents du cerveau-projet (famille cerveau-projet : cercles de controle).
AGENTS_CERVE = ["cerberus", "buffy", "vulcain", "morpheus", "janus",
                "atlas", "themis", "clio"]


def racine_projet():
    """Remonte jusqu'au dossier racine (contenant AGENTS.md)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def charger_parcours(racine, agent):
    chemin = os.path.join(racine, "cerveau-projet", "agents", agent,
                          "parcours", "parcours-%s.json" % agent)
    if not os.path.isfile(chemin):
        return None
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def outils_de_la_carte(parcours):
    """Tous les outils assignes dans les indices des cases de la carte."""
    outils = set()
    for c in parcours.get("cases", {}).values():
        for ind in c.get("indices", []):
            if isinstance(ind, dict) and ind.get("type") == "outil" and ind.get("nom"):
                outils.add(ind["nom"])
    return outils


def fins_de_la_carte(parcours):
    """Retourne (a_activer_janus, a_reactiver_cerberus) booleens selon les
    messages des cases de type fin."""
    a_janus = False
    a_reactiver = False
    for c in parcours.get("cases", {}).values():
        if c.get("type") != "fin":
            continue
        msg = c.get("message", "")
        titre = c.get("titre", "")
        if "Activer Janus" in titre or "activer session-llm-1 janus" in msg:
            a_janus = True
        if "Reactiver Cerberus" in titre or "reactiver session-llm-1" in msg:
            a_reactiver = True
    return a_janus, a_reactiver


def dernieres_missions_agent(racine, agent):
    """Dernieres missions ecrites pour cet agent dans AGENTS.md + historique.
    Retourne une liste de (source, texte)."""
    resultats = []
    for nom_fichier in ["AGENTS.md", "AGENTS-historique.md"]:
        chemin = os.path.join(racine, nom_fichier)
        if not os.path.isfile(chemin):
            continue
        try:
            with io.open(chemin, encoding="utf-8", errors="replace") as fh:
                txt = fh.read()
        except (IOError, OSError):
            continue
        # Blocs de missions : | date | session | agent | MISSION ... |
        motif = re.compile(
            r"\| [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9:]{5} \| [a-z0-9-]+ \| %s \| MISSION([^|\n]*)" % agent)
        for m in motif.finditer(txt):
            resultats.append((nom_fichier, m.group(1).strip()))
    return resultats


def detecter_fins_erronees(racine):
    """Pour chaque agent dont la carte impose Activer Janus, verifier que la
    derniere mission ecrite ne porte pas reactiver Cerberus en fin."""
    problemes = []
    for agent in AGENTS_CERVE:
        parcours = charger_parcours(racine, agent)
        if not parcours:
            continue
        a_janus, a_reactiver = fins_de_la_carte(parcours)
        if not a_janus:
            continue
        missions = dernieres_missions_agent(racine, agent)
        if not missions:
            continue
        # On examine la mission la PLUS RECENTE (derniere du fichier principal)
        # et les 3 dernieres toutes sources confondues (recence croissante).
        dernieres = missions[-3:]
        for source, texte in dernieres:
            if "reactiver cerberus" in texte.lower() and "activer janus" not in texte.lower():
                problemes.append({
                    "type": "FIN_MISSION_ERRONEE",
                    "agent": agent,
                    "source": source,
                    "detail": "carte impose Activer Janus mais mission portant "
                              "reactiver Cerberus : %s..." % texte[:120],
                })
    return problemes


def outils_p0_de_la_fiche(racine, agent):
    """Outils de base (P0) declares dans la fiche de l agent : disponibles
    dans toutes les missions, donc non signales hors carte."""
    chemin = os.path.join(racine, "cerveau-projet", "agents", agent,
                          "%s.md" % agent)
    if not os.path.isfile(chemin):
        return set()
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            fiche = fh.read()
    except (IOError, OSError):
        return set()
    # Section '## Outils de base' (le titre reel contient '(P0)')
    m = re.search(r"^## Outils de base.*?$(.*?)(?=^## )", fiche,
                  re.MULTILINE | re.DOTALL)
    if not m:
        return set()
    return set(re.findall(r"`([a-z]+-[a-z0-9-]+)`", m.group(1)))


def usages_registre(racine):
    """Lit le registre JSONL et retourne {agent: [outils,...]}."""
    chemin = os.path.join(racine, "cerveau-projet", "agents", "traces",
                          "registre-usages-outils.jsonl")
    usages = {}
    if not os.path.isfile(chemin):
        return usages
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    d = json.loads(ligne)
                except ValueError:
                    continue
                agent = d.get("agent", "")
                outil = d.get("outil", "")
                if agent and outil:
                    usages.setdefault(agent, []).append(outil)
    except (IOError, OSError):
        pass
    return usages


def detecter_outils_hors_carte(racine):
    """Croise les usages DECLARES au registre (source fiable des outils
    reellement utilises par chaque agent) vs les outils assignes aux cartes
    et les outils P0 de la fiche : un usage declare hors carte et hors P0
    est une derive (lecon Cerberus 2026-08-13 : outils de test utilises hors
    carte). Les lecons (corrections.md) ne sont PAS une source : elles
    mentionnent les outils des autres agents et des audits (bruit)."""
    problemes = []
    usages = usages_registre(racine)
    for agent in AGENTS_CERVE:
        parcours = charger_parcours(racine, agent)
        if not parcours:
            continue
        outils_carte = outils_de_la_carte(parcours)
        outils_p0 = outils_p0_de_la_fiche(racine, agent)
        autorises = outils_carte | outils_p0
        for outil in sorted(set(usages.get(agent, []))):
            if outil in autorises:
                continue
            # activer-agent-principal et enregistrer-usage-outil sont
            # transverses (cycle Cerberus + trace), jamais hors carte.
            if outil in ("activer-agent-principal", "enregistrer-usage-outil"):
                continue
            problemes.append({
                "type": "OUTIL_HORS_CARTE",
                "agent": agent,
                "source": "registre-usages-outils.jsonl",
                "detail": "usage declare de '%s' au registre mais absent des "
                          "indices outil de la carte (%d assignes) et des "
                          "outils P0 de la fiche" % (outil, len(outils_carte)),
            })
    return problemes


def detecter_coherence_fiche_carte(racine):
    """Une regle ABSOLUE de fiche ne doit pas contredire la carte : si la
    carte impose Activer Janus, la fiche ne doit pas ordonner de reactiver
    Cerberus directement en fin de mission."""
    problemes = []
    for agent in AGENTS_CERVE:
        parcours = charger_parcours(racine, agent)
        if not parcours:
            continue
        a_janus, _ = fins_de_la_carte(parcours)
        if not a_janus:
            continue
        chemin_fiche = os.path.join(racine, "cerveau-projet", "agents", agent,
                                    "%s.md" % agent)
        if not os.path.isfile(chemin_fiche):
            continue
        try:
            with io.open(chemin_fiche, encoding="utf-8", errors="replace") as fh:
                fiche = fh.read()
        except (IOError, OSError):
            continue
        clause_reactiver = re.search(
            r"je [a-z ]*reactiver cerberus [a-z ]*directement", fiche, re.IGNORECASE)
        if clause_reactiver:
            problemes.append({
                "type": "COHERENCE_FICHE_CARTE",
                "agent": agent,
                "source": "%s.md" % agent,
                "detail": "regle de fiche ordonne reactiver Cerberus alors "
                          "que la carte impose Activer Janus : %s..."
                          % clause_reactiver.group(0),
            })
    return problemes


def afficher(problemes, verbose=False):
    if not problemes:
        print("SYNTHESE : 0 probleme de processus detecte")
        return
    par_type = {}
    for p in problemes:
        par_type.setdefault(p["type"], []).append(p)
    for t, liste in sorted(par_type.items()):
        print("== %s : %d ==" % (t, len(liste)))
        for p in liste:
            print("  %s (%s) : %s" % (p["agent"], p["source"], p["detail"][:100]))
            if verbose:
                print("    -> %s" % p["detail"])
    print("")
    print("SYNTHESE : %d problemes de processus detectes" % len(problemes))


def ecrire_rapport(chemin, problemes):
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport evaluer-processus\n\n")
        fh.write("**Date** : %s | **Problemes** : %d\n\n" % (
            __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
            len(problemes)))
        if not problemes:
            fh.write("Aucun probleme de processus detecte.\n")
            return
        par_type = {}
        for p in problemes:
            par_type.setdefault(p["type"], []).append(p)
        for t, liste in sorted(par_type.items()):
            fh.write("## %s (%d)\n\n" % (t, len(liste)))
            for p in liste:
                fh.write("- **%s** (%s) : %s\n" % (p["agent"], p["source"],
                                                   p["detail"]))
            fh.write("\n")
    print("Rapport ecrit : %s" % os.path.abspath(chemin))


def main():
    parser = argparse.ArgumentParser(prog="evaluer-processus",
                                     description="Detecte les derives de processus (fins, outils, coherence fiche/carte)")
    parser.add_argument("--agent", default="", help="Restreindre a un agent")
    parser.add_argument("--rapport", default="", help="Chemin du rapport markdown")
    parser.add_argument("--verbose", action="store_true", help="Detail complet")
    parser.add_argument("--version", action="version",
                        version="evaluer-processus v%s" % VERSION)
    args = parser.parse_args()

    racine = racine_projet()
    problemes = (detecter_fins_erronees(racine)
                 + detecter_outils_hors_carte(racine)
                 + detecter_coherence_fiche_carte(racine))
    if args.agent:
        problemes = [p for p in problemes if p["agent"] == args.agent]
    afficher(problemes, verbose=args.verbose)
    if args.rapport:
        ecrire_rapport(args.rapport, problemes)
    return 1 if problemes else 0


if __name__ == "__main__":
    sys.exit(main())
