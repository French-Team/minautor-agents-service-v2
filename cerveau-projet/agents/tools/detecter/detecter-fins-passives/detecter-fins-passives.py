#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-fins-passives.py
# Detecte les fins PASSIVES dans les arbres v2 des agents
# (cerveau-projet/agents/*/parcours/fins.json + theme-*.json).
# Norme : modele aero (decision 2026-08-30) - chaque fin porte
# action=reactiver, cible=oracle et la commande reactiver-fin
# --cible oracle ; une fin passive ('action=procedure' sans commande,
# formulation 'attend le retour') COUPE la chaine du round.
#
# Version : 0.1.0
# Statut : prepare
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe
# du dossier de categorie (detecter-).
# ============================================================

"""
detecter-fins-passives.py
detecter-fins-passives

Usage:
  detecter-fins-passives.py [OPTIONS]
"""

import argparse
import io
import json
import os
import sys

VERSION = "0.1.0"
STATUT = "prepare"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    chemin = os.path.abspath(script_path)
    nom_fichier = os.path.splitext(os.path.basename(chemin))[0]
    dossier = os.path.basename(os.path.dirname(chemin))
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(_couleur("ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
                       % (nom_fichier, prefixe), "rouge"), file=sys.stderr)
        sys.exit(1)


# Formulations passives qui COUPENT la chaine (Pattern 5, spec-guider-parcours).
# Inspirees de generateurs-case (_FORMULATIONS_PASSIVES) appliquees aux fins v2.
FORMULATIONS_PASSIVES = (
    "attend le retour",
    "attends la suite",
    "attend la suite",
    "j attends",
    "je reste en attente",
    "en attente du retour",
)

# Fins systeme : action=redirection, legitimes (retour racine interne),
# ne sont PAS des fins de mise au repos. Mais si un THEME pointe vers
# fin-theme, la cloture est passive => signale.
FIN_THEME = "fin-theme"

# Types bloquants (PASSIF : coupe la chaine) vs information (INFO :
# delegation/redirection legitime a migrer mais non bloquante).
TYPES_BLOQUANTS = (
    "FINS_JSON_INVALIDE",
    "STRUCTURE_FINS",
    "FIN_MALFORMEE",
    "FIN_THEME_NON_REDIRECTION",
    "FIN_SANS_ACTION",
    "PROCEDURE_SANS_COMMANDE",
    "REDIRECTION_SANS_CIBLE",
    "CIBLE_NON_ORACLE",
    "COMMANDE_SANS_REACTIVER_FIN",
    "ACTION_INCONNUE",
    "FORMULATION_PASSIVE",
    "THEME_FINIT_SUR_FIN_THEME",
    "THEME_FIN_INCONNUE",
)


def est_bloquant(type_p):
    return type_p in TYPES_BLOQUANTS


def trouver_racine_projet():
    courant = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, "AGENTS.md")):
            return courant
        parent = os.path.dirname(courant)
        if parent == courant:
            return None
        courant = parent


def charger_json(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            return json.load(fh)
    except (OSError, IOError, ValueError):
        return None


# Actions LEGITIMES hors modele aero reactiver (a ne PAS signaler comme passives) :
#   - "redirection" : reprise interne (retour a une case du parcours) -- NB : une
#     redirection SANS champ vers OU vers une case inexistante est un trou.
#   - "activer" : delegation directe a un autre agent (ancien modele chaine
#     bout-en-bout, Pattern 8 pre-aero) -- signaltee en INFO, pas en PASSIF.
# Dans le modele aero (decision 2026-08-30) TOUTE fin va vers ORACLE et le
# pilote decide ; les actions activer/redirection sont des vestiges a migrer,
# mais elles ne COUPENT pas la chaine (elles l orientent).
ACTIONS_LEGITIMES_NON_AERO = ("redirection", "activer")


def est_passif(nom_fin, spec, problemes, agent):
    """Analyse une fin NON-systeme. Retourne True si elle est passive
    (coupe la chaine), False si elle est une delegation/redirection
    legitime (a migrer mais pas bloquante). Ajoute les problemes."""
    action = spec.get("action", "")
    titre = spec.get("titre", "")

    # Action ABSENTE : fin coquille -> passive
    if not action:
        problemes.append((agent, "FIN_SANS_ACTION", nom_fin))
        return True

    # action=procedure sans commande : passive (ne fait rien)
    if action == "procedure":
        commande = spec.get("commande", "")
        if not commande:
            problemes.append((agent, "PROCEDURE_SANS_COMMANDE", nom_fin))
            return True
        # procedure AVEC commande : relais actif, non passif
        return False

    # redirection/activer : delegation legitime non-aero (INFO non bloquante)
    if action in ACTIONS_LEGITIMES_NON_AERO:
        if action == "redirection":
            vers = spec.get("vers", "")
            if not vers:
                problemes.append((agent, "REDIRECTION_SANS_CIBLE", nom_fin))
                return True
        return False

    # reactiver : doit viser oracle avec reactiver-fin. EXCEPTION
    # DOCUMENTEE (decision utilisateur 2026-09-02) : la fin-coordination
    # de l aeroport ORACLE atterrit sur CERBERUS avec le bilan consolide
    # (fin de round - Cerberus point de depart/arrivee).
    if action == "reactiver":
        cible = spec.get("cible", "")
        if cible != "oracle":
            if (agent == "oracle" and nom_fin == "fin-coordination"
                    and cible == "cerberus"):
                return False  # EXCEPTION fin de round oracle -> cerberus
            problemes.append((agent, "CIBLE_NON_ORACLE",
                              "%s (cible=%s)" % (nom_fin, cible or "ABSENT")))
            return True
        commande = spec.get("commande", "")
        if "reactiver-fin" not in commande:
            problemes.append((agent, "COMMANDE_SANS_REACTIVER_FIN", nom_fin))
            return True
        return False

    # Action inconnue : passive (on ne sait pas quoi faire)
    problemes.append((agent, "ACTION_INCONNUE",
                      "%s (action=%s)" % (nom_fin, action)))
    return True


def analyser_fins(chemin_fins):
    """Analyse un fichier fins.json. Retourne la liste des problemes :
    chaque probleme = (agent, type, detail)."""
    problemes = []
    donnees = charger_json(chemin_fins)
    if donnees is None:
        agent = os.path.basename(os.path.dirname(os.path.dirname(chemin_fins)))
        problemes.append((agent, "FINS_JSON_INVALIDE", os.path.basename(chemin_fins)))
        return problemes

    agent = os.path.basename(os.path.dirname(os.path.dirname(chemin_fins)))
    fins = donnees.get("fins", {})
    if not isinstance(fins, dict):
        problemes.append((agent, "STRUCTURE_FINS", "cle 'fins' absente ou non dict"))
        return problemes

    for nom_fin, spec in fins.items():
        if not isinstance(spec, dict):
            problemes.append((agent, "FIN_MALFORMEE", nom_fin))
            continue

        # fin-theme (redirection interne) : toleree telle quelle
        if nom_fin == FIN_THEME:
            if spec.get("action") != "redirection":
                problemes.append((agent, "FIN_THEME_NON_REDIRECTION",
                                  "%s (action=%s)" % (nom_fin,
                                                       spec.get("action", ""))))
            continue

        est_passif(nom_fin, spec, problemes, agent)

        # Formulations passives dans description/titre (quel que soit le type)
        zone = " ".join([str(spec.get("titre", "")),
                          str(spec.get("description", ""))])
        for phrase in FORMULATIONS_PASSIVES:
            if phrase in zone:
                problemes.append((agent, "FORMULATION_PASSIVE",
                                  "%s : '%s'" % (nom_fin, phrase)))
                break

    # References des themes vers fins.json : un theme qui pointe vers
    # fin-theme cloture passivement (retour racine au lieu de la fin active).
    dossier_parcours = os.path.dirname(chemin_fins)
    for nom_fichier in sorted(os.listdir(dossier_parcours)):
        if not (nom_fichier.startswith("theme-") and nom_fichier.endswith(".json")):
            continue
        theme = charger_json(os.path.join(dossier_parcours, nom_fichier))
        if theme is None:
            continue
        fin = theme.get("fin")
        if not isinstance(fin, dict):
            continue
        case = fin.get("case", "")
        if case == FIN_THEME:
            problemes.append((agent, "THEME_FINIT_SUR_FIN_THEME",
                              "%s -> %s" % (nom_fichier, FIN_THEME)))
        elif case and case not in fins:
            problemes.append((agent, "THEME_FIN_INCONNUE",
                              "%s -> %s (absente de fins.json)" % (nom_fichier, case)))

    return problemes


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Detecte les fins passives dans les arbres v2 des agents.")
    parser.add_argument("cible", nargs="?", default=None,
                        help="Dossier des agents (defaut: cerveau-projet/agents)")
    parser.add_argument("--agents", nargs="*", default=None,
                        help="Limiter aux agents listes (ex: --agents cerberus argus)")
    parser.add_argument("--json", action="store_true",
                        help="Sortie JSON (machine)")
    parser.add_argument("--version", action="version",
                        version="detecter-fins-passives " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args(argv)

    racine = trouver_racine_projet()
    if racine is None:
        print("[ERREUR] Racine du projet introuvable", file=sys.stderr)
        return 2
    agents_dir = args.cible or os.path.join(racine, "cerveau-projet", "agents")
    if not os.path.isdir(agents_dir):
        print("[ERREUR] Dossier agents introuvable : %s" % agents_dir, file=sys.stderr)
        return 2

    selection = set(args.agents) if args.agents else None
    problemes = []
    for nom_agent in sorted(os.listdir(agents_dir)):
        dossier_agent = os.path.join(agents_dir, nom_agent)
        if not os.path.isdir(dossier_agent):
            continue
        if nom_agent.startswith(".") or nom_agent in ("tools", "lecons", "traces",
                                                      "classeur-variables", "conventions",
                                                      "regles-immuables", "philosophie"):
            continue
        if selection is not None and nom_agent not in selection:
            continue
        chemin_fins = os.path.join(dossier_agent, "parcours", "fins.json")
        if os.path.isfile(chemin_fins):
            problemes.extend(analyser_fins(chemin_fins))

    # Tri par agent puis type
    problemes.sort(key=lambda p: (p[0], p[1], p[2]))

    if args.json:
        print(json.dumps({"version": VERSION, "problemes": [
            {"agent": a, "type": t, "detail": d, "bloquant": est_bloquant(t)}
            for (a, t, d) in problemes
        ]}, ensure_ascii=True))
        return 1 if problemes else 0

    for agent, type_p, detail in problemes:
        if est_bloquant(type_p):
            print(_couleur("[PASSIF] %s | %s | %s" % (agent, type_p, detail), "rouge"))
        else:
            print(_couleur("[INFO]   %s | %s | %s" % (agent, type_p, detail), "jaune"))

    n_agents = len([a for a in os.listdir(agents_dir)
                    if os.path.isdir(os.path.join(agents_dir, a))
                    and not a.startswith(".")])
    nb_passifs = sum(1 for (_, t, _) in problemes if est_bloquant(t))
    print("")
    print("=== RESUME fins-passives ===")
    print("Agents analyses : %d" % n_agents)
    print("Problemes        : %d (dont %d PASSIFS bloquants)" % (len(problemes), nb_passifs))
    if nb_passifs:
        print("VERDICT : fins PASSIVES detectees (%d) - la chaine peut s arreter" % nb_passifs)
        print("Correction recommandee : action=reactiver + cible=oracle + commande reactiver-fin <agent> --cible oracle (modele aero)")
        print("Les [INFO] sont des fins de delegation/redirection legitimes a migrer vers le modele aero (non bloquantes).")
        return 1
    if problemes:
        print("VERDICT : aucune fin PASSIVE - seules des fins de delegation/redirection a migrer en modele aero ([INFO])")
        return 0
    print("VERDICT : aucune fin passive - toutes les fins suivent le modele aero reactiver-fin")
    return 0


if __name__ == "__main__":
    verifier_nommage(__file__)
    sys.exit(main())