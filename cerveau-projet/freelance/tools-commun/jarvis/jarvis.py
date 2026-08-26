#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
JARVIS -- Outil de communication inter-agents (v2 freelance)

POINT D'ENTREE UNIQUEMENT (protocole 14) : parsing CLI + dispatch.
Toute la logique vit dans fonctions/ (une tache par module) :
    core.py         primitives (chemins, JSONL, agents D15)
    historique.py   ecriture AGENTS-historique-v2.md (fichier v2 separe)
    messages.py     envoyer / lire / recu / acquitter / lister / bloques
    activations.py  activer + maj bloc session AGENTS.md
    files.py        files d'attente + stop-dev (protocole 13 v2)

Usage:
    python3 jarvis.py --help

Proprietaire : Vision (perimetre JARVIS)
Version : 0.11.0 (chaine de demarrage/arret - mission [AT-1] 2026-08-23 :
demarrage = tic routines + DEFCON + files + operationnel ; arret = resume)
"""

import argparse
import os as _os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "fonctions"))

# HARNAIS (PROTOCOLE 21) : l outil s auto-verifie en debut de traitement.
sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                 "..", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
    _CHEMIN_OUTIL = _os.path.dirname(_os.path.abspath(__file__))
except ImportError:
    verifier_outil = None

from messages import cmd_envoyer, cmd_lire, cmd_recu, cmd_acquitter, \
    cmd_lister, cmd_bloques
from activations import cmd_activer
from historique import cmd_historiser
from files import cmd_mettre_en_attente, cmd_file, cmd_reprendre, cmd_stop_dev
from defcon import cmd_defcon, cmd_changer_defcon
from verifier import cmd_verifier
from classeur_v2 import cmd_classeur
from routines import cmd_routines_etat
from demarrage import cmd_demarrage, cmd_arret
from relais import relayer_vers_stark
from missions import lancer as lancer_missions_fichier


def construire_parser():
    parser = argparse.ArgumentParser(description="JARVIS -- Communication inter-agents")
    subparsers = parser.add_subparsers(dest="commande", help="Commande")

    # envoyer
    p_env = subparsers.add_parser("envoyer", help="Envoyer un message")
    p_env.add_argument("--de", required=True, help="Expediteur")
    p_env.add_argument("--vers", required=True, help="Destinataire")
    p_env.add_argument("--priorite", type=int, default=3, choices=range(1, 6), help="Priorite (1-5)")
    p_env.add_argument("--objet", required=True, help="Objet du message")
    p_env.add_argument("--corps", required=True, help="Corps du message")
    p_env.add_argument("--session", default="", help="Session (pour historiser le bon Nom LLM)")
    p_env.add_argument("--activer", action="store_true",
                       help="Le message declenche l'activation du destinataire (le round continue)")
    p_env.add_argument("--type", dest="type_action", default="R", choices=["R", "IR"],
                       help="Type d'intervention : R (round) ou IR (inter-round)")
    p_env.add_argument("--sans-historique", dest="sans_historique", action="store_true",
                       help="Ne pas ecrire dans l'historique (messages techniques/test)")

    # recu (v0.5.0)
    p_recu = subparsers.add_parser("recu",
                                   help="Lire + acquitter tout en un appel (fluidite)")
    p_recu.add_argument("--agent", required=True, help="Agent")

    # lire
    p_lire = subparsers.add_parser("lire", help="Lire les messages en attente")
    p_lire.add_argument("--agent", required=True, help="Agent")

    # acquitter
    p_acq = subparsers.add_parser("acquitter", help="Acquitter un message")
    p_acq.add_argument("--agent", required=True, help="Agent")
    p_acq.add_argument("--id", required=True, help="ID du message")

    # lister
    p_list = subparsers.add_parser("lister", help="Lister les messages")
    p_list.add_argument("--agent", required=True, help="Agent")
    p_list.add_argument("--tous", action="store_true", help="Inclure les messages lus")

    # bloques
    subparsers.add_parser("bloques", help="Lister les agents bloques")

    # activer
    p_act = subparsers.add_parser("activer", help="Activer un agent via JARVIS")
    p_act.add_argument("--agent", required=True, help="Agent a activer")
    p_act.add_argument("--session", required=True, help="Session cible (convention session-llm-N)")
    p_act.add_argument("--mission", required=True, help="Mission de l agent")
    p_act.add_argument("--de", default="jarvis",
                        help="Expediteur (defaut: jarvis - SEUL JARVIS "
                             "active, meme quand la demande vient de stark)")

    # historiser
    p_hist = subparsers.add_parser("historiser", help="Enregistrer dans l'historique")
    p_hist.add_argument("--agent", required=True, help="Agent")
    p_hist.add_argument("--raison", required=True, help="Raison de l'action")
    p_hist.add_argument("--type", default="R", help="Type: R=Round, IR=Inter-round")
    p_hist.add_argument("--session", default="", help="Session (pour lire le Nom LLM dans AGENTS.md)")

    # files d'attente (protocole 13 v2 - 6 declencheurs)
    p_meatt = subparsers.add_parser(
        "mettre-en-attente",
        help="placer une mission en file selon le declencheur")
    p_meatt.add_argument("--mission", required=True, help="Mission en cours")
    p_meatt.add_argument("--contexte", default="", help="Contexte de reprise")
    p_meatt.add_argument("--niveau", default=None,
                         choices=["attente", "attention", "urgent"],
                         help="[attente]=file normale / [attention]=SUIVANTE / [urgent]=PRIORITAIRE")
    p_meatt.add_argument("--file", default=None,
                         choices=["file-attente", "file-asap"],
                         help="(compat) file cible si --niveau absent")
    p_meatt.add_argument("--agent", default="", help="Agent porteur (optionnel)")

    subparsers.add_parser("file", help="Lister les files d'attente")

    p_rep = subparsers.add_parser(
        "reprendre",
        help="Reprendre la mission la plus prioritaire (PRIORITAIRE > SUIVANTE > EN_ATTENTE)")
    p_rep.add_argument("--file", default=None,
                       choices=["file-attente", "file-asap"],
                       help="(option) restreindre a une seule file")

    p_stop = subparsers.add_parser(
        "stop-dev",
        help="[stop] DEFCON 5 : arret complet du dev, gel de toutes les missions")
    p_stop.add_argument("--raison", required=True, help="Raison de l'arret")

    # missions serie/parallel (demande utilisateur)
    p_lm = subparsers.add_parser(
        "lancer-missions",
        help="Lancer des missions en SERIE (controle) ou PARALLEL (sans collision)")
    p_lm.add_argument("--fichier", required=True,
                      help="Scenario JSON {session, mode: serie|parallel, missions:[{agent, mission}]}")

    # defcon (protocole 15)
    subparsers.add_parser("defcon", help="Afficher l'etat DEFCON courant")
    p_d = subparsers.add_parser(
        "changer-defcon",
        help="Descendre d'un niveau (5->4->3->2, transitions legales uniquement)")
    p_d.add_argument("--niveau", required=True, type=int, choices=[4, 3, 2])
    p_d.add_argument("--commentaire", default="", help="Contexte du changement")

    # routines EDITH (protocole 16 volet 4)
    subparsers.add_parser("routines-etat",
                          help="Etat des routines (derniere execution / intervalle)")

    # chaine de demarrage / arret propre (mission [AT-1] 2026-08-23)
    p_dem = subparsers.add_parser(
        "demarrage",
        help="Chaine de demarrage : tic routines + DEFCON + files + operationnel")
    p_dem.add_argument("--session", default="session-freelance",
                       help="Session (encart AGENTS-historique-v2 cible)")
    p_arr = subparsers.add_parser(
        "arret",
        help="Extinction propre : resume de session + historisation")
    p_arr.add_argument("--session", default="session-freelance",
                       help="Session (encart AGENTS-historique-v2 cible)")

    # verifier-coherence (mecanisme de validation automatique 2026-08-25)
    subparsers.add_parser(
        "verifier-coherence",
        help="Verifier la coherence d AGENTS.md contre les fichiers reels (arbres v2, fiches, corrections, jarvis-data, Sessions)")

    # classeur v2 (BDD SQLite, freelance/classeur/ - decision utilisateur
    # 2026-08-25 : la v2 a son propre classeur, stockage/consultation rapides)
    p_cl = subparsers.add_parser(
        "classeur",
        help="Classeur v2 (BDD SQLite) : variable-set/get/list, session-set/get/list, agent-set/get/list, etat, exporter")
    p_cl.add_argument("classeur_cmd", nargs="?", default="",
                      help="Sous-commande (variable-set, session-set, agent-set, etat...)")
    p_cl.add_argument("nom", nargs="?", default="", help="Nom (variable/session/agent/champ)")
    p_cl.add_argument("valeur", nargs="?", default="", help="Valeur (variable-set / utilisateur-set)")
    p_cl.add_argument("--source", default="jarvis", help="Source de la variable")
    p_cl.add_argument("--id", dest="id_llm", default="", help="Id LLM (session-set)")
    p_cl.add_argument("--agent", default="", help="Agent (session-set)")
    p_cl.add_argument("--statut", default="", help="Statut (agent-set)")
    p_cl.add_argument("--mission", default="", help="Mission (agent-set)")

    return parser


def main():
    if verifier_outil is not None:
        verifier_outil(_CHEMIN_OUTIL, agent="jarvis")
    # v0.9.2 (protocole 16) : routines executees a chaque invocation -
    # plus de processus d'arriere-plan : jarvis EST le planificateur.
    try:
        from routines import executer_routines
        executer_routines()
    except Exception:
        pass
    # v0.12.0 (decision utilisateur) : JARVIS POUSSE vers stark les
    # messages du hub qui lui sont destines - stark ne vient plus lire,
    # jarvis transmet.
    try:
        relayer_vers_stark()
    except Exception:
        pass
    parser = construire_parser()
    args = parser.parse_args()

    if args.commande == "envoyer":
        cmd_envoyer(args)
    elif args.commande == "lire":
        cmd_lire(args)
    elif args.commande == "acquitter":
        cmd_acquitter(args)
    elif args.commande == "recu":
        cmd_recu(args)
    elif args.commande == "mettre-en-attente":
        cmd_mettre_en_attente(args)
    elif args.commande == "file":
        cmd_file(args)
    elif args.commande == "reprendre":
        cmd_reprendre(args)
    elif args.commande == "stop-dev":
        cmd_stop_dev(args)
    elif args.commande == "lancer-missions":
        import json as _json
        print(_json.dumps(lancer_missions_fichier(args.fichier),
                          ensure_ascii=True, indent=2))
    elif args.commande == "defcon":
        cmd_defcon(args)
    elif args.commande == "changer-defcon":
        cmd_changer_defcon(args)
    elif args.commande == "routines-demarrer":
        print("[ROUTINES] v0.9.2 : plus de serveur - les routines tournent a chaque invocation de jarvis.")
    elif args.commande == "routines-arreter":
        print("[ROUTINES] v0.9.2 : plus de serveur a arreter.")
    elif args.commande == "routines-etat":
        cmd_routines_etat()
    elif args.commande == "demarrage":
        cmd_demarrage(args)
    elif args.commande == "arret":
        cmd_arret(args)
    elif args.commande == "verifier-coherence":
        cmd_verifier(args)
    elif args.commande == "classeur":
        cmd_classeur(args)
    elif args.commande == "lister":
        cmd_lister(args)
    elif args.commande == "activer":
        cmd_activer(args)
    elif args.commande == "bloques":
        cmd_bloques(args)
    elif args.commande == "historiser":
        cmd_historiser(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
