# -*- coding: ascii -*-
"""fonctions/classeur_v2.py - UNE tache : exposer le classeur v2 (BDD
SQLite, freelance/classeur/) via les sous-commandes jarvis.py.

Sous-commandes :
  classeur variable-set <nom> <valeur> [--source S]
  classeur variable-get <nom>
  classeur variable-list
  classeur session-set <session> [--id ID] [--agent AGENT]
  classeur session-get <session>
  classeur session-list
  classeur agent-set <nom> [--statut S] [--mission M]
  classeur agent-get <nom>
  classeur agent-list
  classeur etat
  classeur exporter

La BDD est le seul stockage : pas de fichier markdown, consultation et
ecriture rapides (SQLite). Carte d identite utilisateur : table reservee.
"""

import json
import os
import sys
from pathlib import Path

# racine projet (P10 : detection via os_path, jamais de ../.. comptes)
_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = Path(trouver_racine(__file__))
CLASSEUR_DIR = RACINE / "cerveau-projet" / "freelance" / "classeur"
sys.path.insert(0, str(CLASSEUR_DIR / "fonctions"))


def _importer():
    """Importer la logique du classeur v2 (module fonctions/classeur.py)."""
    try:
        import classeur as c
        return c
    except ImportError as exc:
        print("[JARVIS] ERREUR: module classeur v2 introuvable : %s" % exc,
              file=sys.stderr)
        sys.exit(2)


def cmd_classeur(args):
    """Dispatcher des sous-commandes classeur (appele depuis jarvis.py)."""
    if not args.classeur_cmd:
        print("[JARVIS] classeur : sous-commandes = variable-set, "
              "variable-get, variable-list, session-set, session-get, "
              "session-list, agent-set, agent-get, agent-list, "
              "utilisateur-set, utilisateur-list, etat, exporter")
        return 0
    c = _importer()
    cmd = args.classeur_cmd
    if cmd == "variable-set":
        c.variable_set(args.nom, args.valeur, source=getattr(args, "source", "jarvis"))
        print("[JARVIS] classeur: variable %s ecrite" % args.nom)
    elif cmd == "variable-get":
        v = c.variable_get(args.nom)
        print(json.dumps(v, ensure_ascii=False) if v else "ABSENTE")
    elif cmd == "variable-list":
        print(json.dumps(c.variable_list(), ensure_ascii=False, indent=1))
    elif cmd == "session-set":
        c.session_set(args.nom, id_llm=getattr(args, "id_llm", ""),
                      agent=getattr(args, "agent", ""))
        print("[JARVIS] classeur: session %s ecrite" % args.nom)
    elif cmd == "session-get":
        s = c.session_get(args.nom)
        print(json.dumps(s, ensure_ascii=False) if s else "ABSENTE")
    elif cmd == "session-list":
        print(json.dumps(c.session_list(), ensure_ascii=False, indent=1))
    elif cmd == "agent-set":
        c.agent_set(args.nom, statut=getattr(args, "statut", ""),
                    mission=getattr(args, "mission", ""))
        print("[JARVIS] classeur: agent %s ecrit" % args.nom)
    elif cmd == "agent-get":
        a = c.agent_get(args.nom)
        print(json.dumps(a, ensure_ascii=False) if a else "ABSENT")
    elif cmd == "agent-list":
        print(json.dumps(c.agent_list(), ensure_ascii=False, indent=1))
    elif cmd == "utilisateur-set":
        c.utilisateur_set(args.nom, args.valeur)
        print("[JARVIS] classeur: champ utilisateur %s ecrit" % args.nom)
    elif cmd == "utilisateur-list":
        print(json.dumps(c.utilisateur_list(), ensure_ascii=False, indent=1))
    elif cmd == "etat":
        print(json.dumps(c.etat_complet(), ensure_ascii=False, indent=1))
    elif cmd == "exporter":
        print(json.dumps(c.exporter_json(), ensure_ascii=False, indent=1))
    else:
        print("[JARVIS] classeur: sous-commande inconnue '%s'" % cmd,
              file=sys.stderr)
        return 2
    return 0