"""Categorie definir : cree OU met a jour l'encart session-matrix (idempotent)."""
from commun import (
    charger_texte,
    composer_bloc,
    ecrire_texte,
    garde_structurelle,
    remplacer_ou_inserer_bloc,
    trouver_agents_md,
)
from commun import extraire_options

NOMS_OPTIONS = ("nom-llm", "agent", "raison")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    nom_llm = options.get("nom-llm", "")
    agent = options.get("agent", "")
    raison = options.get("raison", "")
    if not nom_llm or not agent or not raison:
        print('Usage : python main.py definir --nom-llm <id> --agent <nom> --raison "..."')
        return 2

    chemin = trouver_agents_md()
    texte_avant = charger_texte(chemin)

    bloc = composer_bloc(nom_llm, agent, raison)
    texte_apres = remplacer_ou_inserer_bloc(texte_avant, bloc)

    # Garde structurelle : hors du bloc delimite, RIEN ne doit bouger.
    if not garde_structurelle(texte_avant, texte_apres):
        print("REFUS : la garde a detecte une modification hors du bloc delimite -- rien n'est ecrit.")
        return 1

    empreinte = ecrire_texte(chemin, texte_apres)
    print(
        "Encart session-matrix pose (nom-llm : " + nom_llm + ", agent : " + agent
        + ") -- empreinte AGENTS.md : " + empreinte[:16] + "..."
    )
    return 0
