"""Point d'entree de la categorie noter de bdd-activites (fiche 5/10)."""
from commun import charger_bdd, enregistrer_bdd, extraire_options
from constants import SECTIONS
from noter.fonctions import deposer_activite, section_connue, separer_tags

NOMS_OPTIONS = ("section", "detail", "tags")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    section = options.get("section", "")
    detail = options.get("detail", "")
    tags = separer_tags(options.get("tags", ""))

    if not section or not detail or not tags:
        print('Usage : python main.py noter --section <nom> --detail "..." --tags "a,b"')
        return 2
    if not section_connue(section):
        print("Section inconnue : " + section + " (sections pre-declarees : " + ", ".join(SECTIONS) + ")")
        return 2

    donnees = charger_bdd()
    entree = deposer_activite(donnees, section, detail, tags)
    empreinte = enregistrer_bdd(donnees)
    print(
        "Activite deposee dans " + section + " (" + entree["date"]
        + ") -- empreinte : " + empreinte[:16] + "..."
    )
    return 0
