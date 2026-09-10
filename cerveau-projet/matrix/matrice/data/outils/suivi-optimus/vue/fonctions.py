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
    """Compose UNE ligne d'un tableau d'action (heure en premier)."""
    detail = echapper_pipe(evenement.get("detail", ""))[:200]
    mission = echapper_pipe(evenement.get("mission", "") or "-")
    portes = ", ".join(evenement.get("portes", ())) if evenement.get("portes") else "-"
    fichiers = ", ".join(evenement.get("fichiers", ())) if evenement.get("fichiers") else "-"
    duree = evenement.get("duree_s") or "-"
    # Separation date et heure pour affichage : heure en premier
    date_complete = evenement.get("date", "")
    heure = ""
    if date_complete and " " in date_complete:
        heure = date_complete.split(" ")[1]
        date_complete = date_complete.split(" ")[0]
    return "| " + " | ".join([
        echapper_pipe(heure or "-"),
        echapper_pipe(date_complete or "-"),
        mission,
        detail,
        portes,
        fichiers,
        str(duree),
    ]) + " |"


def composer_section(action, evenements):
    """Compose UNE section dediee (un tableau par action).
    Limite l'affichage aux 10 dernieres evenements.
    """
    lignes = ["## Action : " + action, ""]
    if not evenements:
        return lignes + ["(aucun evenement)", ""]
    # Limite aux 10 dernieres evenements (tri chronologique inverse).
    evenements_triees = sorted(evenements, key=lambda e: e.get("date", ""), reverse=True)
    evenements_limites = evenements_triees[:10]
    lignes += [
        "| Heure | Date | Mission | Detail | Portes | Fichiers | Duree |",
        "|---|---|---|---|---|---|---|",
    ]
    for evenement in evenements_limites:
        lignes.append(composer_ligne(evenement))
    if len(evenements) > 10:
        lignes.append("")
        lignes.append("*" + str(len(evenements) - 10) + " evenement(s) supplementaire(s) non affiches (voir data/suivi-optimus.jsonl).")
    return lignes + [""]


def composer_vue(evenements, actions, inbox_evenements=None):
    """Retourne les lignes du fichier markdown (entete + tableau recaps + sections par action).

    Ordre ferme des sections : celui des actions (constants.ACTIONS).
    Chaque section est un TABLEAU dedie a SON action, present meme vide.
    Tableau recapitulatif : derniere mise a jour, total evenements, missions en attente, missions finies.
    """
    par_action = {action: [] for action in actions}
    for evenement in evenements:
        par_action.setdefault(evenement.get("action", "?"), []).append(evenement)

    # Derniere mise a jour : date de la derniere action ( premiere entree en ordre chronologique inverse )
    derniere_date = ""
    if evenements:
        dates = [e.get("date", "") for e in evenements if e.get("date")]
        if dates:
            derniere_date = max(dates)

    # Missions en attente (dans l'inbox mais pas encore synchronisees).
    missions_en_attente = []
    if inbox_evenements:
        for ev in inbox_evenements:
            typ = ev.get("type", "")
            if typ not in ("fin-mission", "retour-lot"):
                continue
            mission = ev.get("mission", "")
            if typ == "retour-lot":
                lot = ev.get("lot", [])
                missions_en_attente.extend(lot)
            elif mission:
                missions_en_attente.append(mission)

    # Missions finies (dans le suivi-optimus).
    missions_finies = set()
    for evenement in evenements:
        mission = evenement.get("mission", "")
        if mission:
            missions_finies.add(mission)

    lignes = [
        "# Suivi d'optimus-prime (v3)",
        "",
        "",
        "| Derniere mise a jour | Total evenements | Missions en attente | Missions finies |",
        "|---|---|---|---|",
        "| " + (derniere_date or "-") + " | " + str(len(evenements)) + " | " + str(len(missions_en_attente)) + " | " + str(len(missions_finies)) + " |",
        "",
        "> VISUEL GENERE depuis data/suivi-optimus.jsonl -- jamais edite a la main.",
        "> Regenerer : python3 matrice/data/outils/suivi-optimus/main.py vue",
        "> Etancheite : le cameleon n'accede JAMAIS a cette trace (zone suivi-optimus).",
        "> optimus reste INVISIBLE de la Matrice : pas d'encart dans le journal",
        "> multi-encarts, SON fichier est la seule vue de son travail.",
        "",
        "Flux : optimus (via l'outil suivi-optimus) -> data/suivi-optimus.jsonl -> VUE lecture seule",
        "",
    ]
    for action in actions:
        lignes.extend(composer_section(action, par_action[action]))
    return lignes