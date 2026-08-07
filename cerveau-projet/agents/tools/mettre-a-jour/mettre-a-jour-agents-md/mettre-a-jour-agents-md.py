#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
mettre-a-jour-agents-md.py

Outil pour modifier AGENTS.md de maniere fiable lors des activations
et reactivations d'agents.

Actions:
  activer  <agent> <raison> [mission]   - Activer un agent
  reactiver <raison> <agent_precedent>  - Reactiver Cerberus
  aide                                  - Afficher cette aide

Proprietaire : Vulcain
Version : 0.2.0-py
Statut : prepare
"""

import io
import os
import re
import sys
from datetime import datetime

VERSION = "0.2.0-py"
STATUT = "prepare"

AGENTS_FILE = "AGENTS.md"
AGENTS_HISTORIQUE = "AGENTS-historique.md"
CERBERUS_FICHE = "cerveau-projet/agents/cerberus/cerberus.md"
MAX_ENTREES_HISTORIQUE = 150

ROLES = {
    "cerberus": "Gardien de l'entree -- analyse et active les agents",
    "buffy": "Developpeur principal -- contenu et structures",
    "atlas": "Explorateur -- recherche et decouverte",
    "janus": "Controleur des statuts -- validation et verification",
    "vulcain": "Constructeur d'outils -- creation et developpement",
    "athena": "Redactrice de pense-betes -- transformation des demandes",
    "morpheus": "Testeur -- validation des outils et des tests",
    "promethee": "Redacteur de specs -- specification technique",
    "minerve": "Redactrice de todos -- organisation des taches",
    "clio": "Muse de l'histoire -- mise a jour du README",
}


def get_agent_role(agent):
    """Retourner le role d'un agent (casse insensible)."""
    return ROLES.get(agent.lower(), "Agent inconnu")


def verifier_ascii(chaine):
    """Retourner True si la chaine est 100% ASCII."""
    return all(ord(c) < 128 for c in chaine)


def verifier_fichier_ascii(fichier):
    """Verifier qu'un fichier entier est ASCII. Afficher les lignes concernees."""
    nb = 0
    try:
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            for i, ligne in enumerate(fh, 1):
                for ch in ligne:
                    if ord(ch) > 127:
                        nb += 1
                        print("  Ligne %d: caractere non-ASCII U+%04X" % (i, ord(ch)))
                        break
    except IOError:
        pass
    return nb == 0


def ajouter_historique(timestamp, agent, raison):
    """Ajouter une ligne dans l'historique (en haut du tableau, max 150)."""
    if not os.path.isfile(AGENTS_HISTORIQUE):
        print("ERREUR: Le fichier %s n'existe pas" % AGENTS_HISTORIQUE)
        return 1

    nouvelle_ligne = "| %s | %s | %s |" % (timestamp, agent, raison)

    # VERIFICATION ASCII PRE-ECRITURE (lecon permanente)
    if not verifier_ascii(nouvelle_ligne):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - ecriture historique REFUSEE")
        return 1

    with io.open(AGENTS_HISTORIQUE, "r", encoding="utf-8", errors="replace") as fh:
        lignes = fh.readlines()

    # Inserer la ligne en haut du tableau (apres la ligne de separation)
    sortie = []
    insere = False
    compteur = 0
    for ligne in lignes:
        if re.match(r"^\s*\|?---", ligne) and not insere:
            sortie.append(ligne)
            sortie.append(nouvelle_ligne + "\n")
            insere = True
            compteur += 1
            continue
        if re.match(r"^\| 20[0-9][0-9]-", ligne):
            if compteur < MAX_ENTREES_HISTORIQUE:
                sortie.append(ligne)
                compteur += 1
            continue
        sortie.append(ligne)

    with io.open(AGENTS_HISTORIQUE, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(sortie)

    # VERIFICATION ASCII POST-ECRITURE
    if not verifier_fichier_ascii(AGENTS_HISTORIQUE):
        print("WARNING: Caracteres non-ASCII presents dans %s (voir lignes ci-dessus)" % AGENTS_HISTORIQUE)

    print("Historique mis a jour dans %s" % AGENTS_HISTORIQUE)
    return 0


def remplacer_champ(contenu, champ, valeur):
    """Remplacer la valeur d'un champ **Champ** | valeur dans AGENTS.md."""
    pattern = r"(\*\*%s\*\* \| )[^|]*" % re.escape(champ)
    return re.sub(pattern, r"\g<1>" + valeur, contenu)


def activer_agent(agent, raison, mission=None):
    """Activer un agent : mettre a jour AGENTS.md + historique."""
    # VERIFICATION ASCII PREVENTIVE
    if not verifier_ascii(raison):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - activation REFUSEE")
        return 1

    if not os.path.isfile(AGENTS_FILE):
        print("ERREUR: Le fichier %s n'existe pas" % AGENTS_FILE)
        return 1

    date = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    role = get_agent_role(agent)

    with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()

    contenu = remplacer_champ(contenu, "Nom", agent)
    contenu = remplacer_champ(contenu, "Role", role)
    contenu = remplacer_champ(contenu, "Derniere mise a jour", date)
    contenu = remplacer_champ(contenu, "Active par", "Cerberus (automatique)")
    contenu = remplacer_champ(contenu, "Raison", raison)

    with io.open(AGENTS_FILE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)

    ajouter_historique(timestamp, agent, raison)
    print("Agent %s active avec succes" % agent)
    return 0


def reactiver_cerberus(raison, agent_precedent):
    """Reactiver Cerberus : mettre a jour AGENTS.md + historique."""
    # VERIFICATION ASCII PREVENTIVE
    if not verifier_ascii(raison):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - reactivation REFUSEE")
        return 1

    if not os.path.isfile(AGENTS_FILE):
        print("ERREUR: Le fichier %s n'existe pas" % AGENTS_FILE)
        return 1

    if not os.path.isfile(CERBERUS_FICHE):
        print("ERREUR: Le fichier %s n'existe pas" % CERBERUS_FICHE)
        return 1

    # Lire la fiche de Cerberus (verification de presence)
    print("Lecture de %s..." % CERBERUS_FICHE)
    with io.open(CERBERUS_FICHE, "r", encoding="utf-8", errors="replace") as fh:
        fh.read()

    date = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    role = get_agent_role("Cerberus")

    with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()

    contenu = remplacer_champ(contenu, "Nom", "Cerberus")
    contenu = remplacer_champ(contenu, "Role", role)
    contenu = remplacer_champ(contenu, "Derniere mise a jour", date)
    contenu = remplacer_champ(contenu, "Active par", "%s (retour de mission)" % agent_precedent)
    contenu = remplacer_champ(contenu, "Raison", raison)

    with io.open(AGENTS_FILE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)

    ajouter_historique(timestamp, "Cerberus", raison)
    print("Cerberus reactive avec succes")
    return 0


def afficher_aide():
    print("Usage: mettre-a-jour-agents-md.py <action> [parametres]")
    print("")
    print("Actions disponibles:")
    print("  activer <agent> <raison> [mission]  - Activer un agent")
    print("  reactiver <raison> <agent_precedent> - Reactiver Cerberus")
    print("  aide                               - Afficher cette aide")
    print("")
    print("Exemples:")
    print('  mettre-a-jour-agents-md.py activer Buffy "Mission correction" "Mettre a jour demarrer.md"')
    print('  mettre-a-jour-agents-md.py reactiver "Mission terminee" Buffy')


def main(argv):
    if not argv:
        afficher_aide()
        return 0

    action = argv[0]

    if action in ("aide", "--help", "-h"):
        afficher_aide()
        return 0

    if action == "--version":
        print("mettre-a-jour-agents-md v%s (%s)" % (VERSION, STATUT))
        return 0

    if action == "activer":
        if len(argv) < 3:
            print("ERREUR: Parametres manquants pour l'action 'activer'")
            afficher_aide()
            return 1
        agent = argv[1]
        raison = argv[2]
        mission = argv[3] if len(argv) > 3 else None
        return activer_agent(agent, raison, mission)

    if action == "reactiver":
        if len(argv) < 3:
            print("ERREUR: Parametres manquants pour l'action 'reactiver'")
            afficher_aide()
            return 1
        raison = argv[1]
        agent_precedent = argv[2]
        return reactiver_cerberus(raison, agent_precedent)

    print("ERREUR: Action inconnue '%s'" % action)
    afficher_aide()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
