"""Entree du verbe filtrer : le pilote detecte [mot] et route automatiquement.

Le pilote est un FILTRE ACTIF entre la Matrice et les agents.
Il detecte les demandes a crochets, les route vers la bonne porte,
et gere les taches routinieres que l'agent n'a pas besoin de faire.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commun import extraire_options, horodater

NOMS_OPTIONS = ("message",)

# Liste fermee des mots-crochet reconnus (miroir convention-crochets.md)
CROCHETS = {
    "mission": {"porte": "entonnoir", "action": "deposer", "type": "mission"},
    "audit": {"porte": "entonnoir", "action": "deposer", "type": "audit"},
    "revision": {"porte": "entonnoir", "action": "deposer", "type": "revision"},
    "question": {"porte": "pilote", "action": "lot", "type": "question"},
    "alerte": {"porte": "machine-defcon", "action": "monter", "type": "alerte"},
    "pause": {"porte": "pause-session", "action": "pause", "type": "pause"},
    "bilan": {"porte": "bilan-periode", "action": "bilan", "type": "bilan"},
    "preparation": {"porte": "preparation", "action": "ouvrir", "type": "preparation"},
}

# Detection : [mot] au debut de la ligne
REGEX_CROCHET = re.compile(r"^\[([a-zA-Z0-9_-]+)\]\s*(.*)", re.DOTALL)


def detecter_crochet(message):
    """Detecte un mot-crochet au debut du message.
    Retourne (mot, reste, config) ou (None, message, None) si aucun crochet.
    """
    message = message.strip()
    match = REGEX_CROCHET.match(message)
    if not match:
        return None, message, None

    mot = match.group(1).lower()
    reste = match.group(2).strip()

    if mot in CROCHETS:
        return mot, reste, CROCHETS[mot]

    # Mot inconnu dans la liste fermee
    return mot, reste, None


def executer(arguments):
    """Verbe filtrer : --message <texte> [--json]

    Detecte [mot] et route vers la bonne porte.
    Retourne 0 = route OK, 1 = aucun crochet, 2 = crochet inconnu.
    """
    options = extraire_options(arguments, NOMS_OPTIONS)
    message = options.get("message", "").strip()
    mode_json = "--json" in arguments

    if not message:
        print("Usage : python main.py filtrer --message \"[mission] faire quelque chose\"")
        return 2

    mot, reste, config = detecter_crochet(message)

    if mot is None:
        # Pas de crochet = message normal, pas de routage
        if mode_json:
            import json
            print(json.dumps({"detected": False, "message": message}))
        else:
            print("Aucun crochet detecte. Message normal.")
        return 1

    if config is None:
        # Crochet inconnu
        if mode_json:
            import json
            print(json.dumps({
                "detected": True,
                "mot": mot,
                "known": False,
                "error": "Crochet inconnu : [" + mot + "]. Liste fermee : " + ", ".join(sorted(CROCHETS.keys())),
            }))
        else:
            print("ERREUR : [" + mot + "] non reconnu.")
            print("Liste fermee : " + ", ".join(sorted(CROCHETS.keys())))
        return 2

    # Crochet reconnu = routage
    resultat = {
        "detected": True,
        "mot": mot,
        "known": True,
        "porte": config["porte"],
        "action": config["action"],
        "type": config["type"],
        "reste": reste,
        "date": horodater(),
    }

    if mode_json:
        import json
        print(json.dumps(resultat, ensure_ascii=False, indent=2))
    else:
        print("[" + mot + "] detected -> " + config["porte"] + "/" + config["action"])
        if reste:
            print("  Contenu : " + reste[:120])
        print("  Porte : " + config["porte"])
        print("  Action : " + config["action"])

    return 0
