"""Entree du verbe plan : gestion des todos (Flux 2 seul)."""
import sys
import os

# L-013 : aucun niveau compte a la main. Le dossier de CET outil est celui qui
# porte son commun.py (marqueur) : la remontee est VERIFIEE, jamais supposee (MO-177).
REPERTOIRE_ENTREE = os.path.dirname(os.path.abspath(__file__))
REPERTOIRE_OUTIL = os.path.dirname(REPERTOIRE_ENTREE)
if not os.path.isfile(os.path.join(REPERTOIRE_OUTIL, "commun.py")):
    raise RuntimeError("Dossier de l'outil introuvable depuis " + REPERTOIRE_ENTREE
                       + " : commun.py est absent de " + REPERTOIRE_OUTIL)
sys.path.insert(0, REPERTOIRE_OUTIL)

from commun import extraire_options
from constants import NOMS_OPTIONS_PLAN


def plan(arguments):
    """Verbe plan : --todos <json_list> [--json]
    
    Codes retour :
      0 = succes
      2 = erreur
    """
    options = extraire_options(arguments, NOMS_OPTIONS_PLAN)

    todos_str = options.get("todos", "").strip()
    mode_json = "json" in options

    if not todos_str:
        print("ERREUR : --todos requis. Format JSON liste.")
        print('Usage: plan --todos \'[{"task":"...", "completed":false}]\'')
        return 2

    # Parse JSON
    import json
    try:
        todos = json.loads(todos_str)
    except json.JSONDecodeError as e:
        print("ERREUR : JSON invalide : " + str(e))
        return 2

    if not isinstance(todos, list):
        print("ERREUR : --todos doit etre une liste JSON")
        return 2

    # Affiche le plan
    print("=== PLAN OPTIMUS (Flux 2) ===")
    for i, t in enumerate(todos, 1):
        statut = "[x]" if t.get("completed") else "[ ]"
        task = t.get("task", "sans titre")
        print(f"  {i}. {statut} {task}")
    print("")

    total = len(todos)
    faits = sum(1 for t in todos if t.get("completed"))
    print(f"Total : {total} | Faits : {faits} | Reste : {total - faits}")

    if mode_json:
        print(json.dumps({"total": total, "faits": faits, "reste": total - faits}, indent=2))

    return 0
