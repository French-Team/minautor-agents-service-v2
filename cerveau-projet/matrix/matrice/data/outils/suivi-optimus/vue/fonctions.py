"""Fonctions simples de la categorie vue : une seule tache chacune.

Decision createur (2026-09-09) : la vue est organisee en TABLEAUX DEDIES
par action (jamais a la suite) -- le createur suit TOUTES les actions
d'optimus-prime a des emplacements precis. optimus reste invisible : pas
d'encart dans journal-multi-encarts.md, SON fichier est la seule vue.
"""


def echapper_pipe(texte):
    """Echappe les barres verticales pour garder le tableau markdown intact."""
    return str(texte).replace("|", "\\|")


def composer_ligne(evenement):
    """Compose UNE ligne d'un tableau d'action."""
    detail = echapper_pipe(evenement.get("detail", ""))[:200]
    mission = echapper_pipe(evenement.get("mission", "") or "-")
    portes = ", ".join(evenement.get("portes", ())) if evenement.get("portes") else "-"
    fichiers = ", ".join(evenement.get("fichiers", ())) if evenement.get("fichiers") else "-"
    duree = evenement.get("duree_s") or "-"
    return "| " + " | ".join([
        echapper_pipe(evenement.get("date", "?")),
        mission,
        detail,
        portes,
        fichiers,
        str(duree),
    ]) + " |"


def composer_section(action, evenements):
    """Compose UNE section dediee (un tableau par action)."""
    lignes = ["## Action : " + action, ""]
    if not evenements:
        return lignes + ["(aucun evenement)", ""]
    lignes += [
        "| Date | Mission | Detail | Portes | Fichiers | Duree |",
        "|---|---|---|---|---|---|",
    ]
    for evenement in evenements:
        lignes.append(composer_ligne(evenement))
    return lignes + [""]


def composer_vue(evenements, actions):
    """Retourne les lignes du fichier markdown (entete + sections par action).

    Ordre ferme des sections : celui des actions (constants.ACTIONS).
    Chaque section est un TABLEAU dedie a SON action, present meme vide.
    """
    par_action = {action: [] for action in actions}
    for evenement in evenements:
        par_action.setdefault(evenement.get("action", "?"), []).append(evenement)

    lignes = [
        "# Suivi d'optimus-prime (v3)",
        "",
        "> VISUEL GENERE depuis data/suivi-optimus.jsonl -- jamais edite a la main.",
        "> Regenerer : python3 matrice/data/outils/suivi-optimus/main.py vue",
        "> Etancheite : le cameleon n'accede JAMAIS a cette trace (zone suivi-optimus).",
        "> optimus reste INVISIBLE de la Matrice : pas d'encart dans le journal",
        "> multi-encarts, SON fichier est la seule vue de son travail.",
        "",
        "Flux : optimus (via l'outil suivi-optimus) -> data/suivi-optimus.jsonl -> VUE lecture seule",
        "",
        "Total : " + str(len(evenements)) + " evenement(s)",
        "",
    ]
    for action in actions:
        lignes.extend(composer_section(action, par_action[action]))
    return lignes