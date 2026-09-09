"""Categorie noter : orchestre l'enregistrement d'un usage d'outil ou de combo.

Interface entre main.py et les fonctions simples (noter/fonctions.py).
"""
from commun import ajouter_ligne, extraire_options
from noter.fonctions import fabriquer_entree, separer_tags

NOMS_OPTIONS = ("outil", "commande", "code", "duree", "detail", "tags")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    outil = options.get("outil", "")
    commande = options.get("commande", "")
    code_texte = options.get("code", "")
    duree_texte = options.get("duree", "")
    detail = options.get("detail", "")
    tags = separer_tags(options.get("tags", ""))

    if not outil or not commande or not code_texte.isdigit() or not tags:
        print('Usage : python main.py noter --outil <nom> --commande <verbe> --code <n> [--duree <ms>] --tags "a,b"')
        return 2

    code = int(code_texte)
    duree = int(duree_texte) if duree_texte.isdigit() else None
    entree = fabriquer_entree(outil, commande, code, duree, detail, tags)
    ajouter_ligne(entree)
    print(
        "Usage note : " + entree["outil"] + "/" + entree["commande"]
        + " (code " + str(entree["code"]) + ") -- empreinte non applicable (journal ajout seul)"
    )
    return 0
