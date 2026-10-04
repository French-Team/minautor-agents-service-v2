"""Categorie noter : orchestre l'enregistrement d'un usage d'outil ou de combo.

Interface entre main.py et les fonctions simples (noter/fonctions.py).
"""
from commun import ajouter_ligne, extraire_options
from noter.fonctions import fabriquer_entree, separer_tags

# Espion tokens (E-097) : options optionnelles, jamais requises.
NOMS_OPTIONS = ("outil", "commande", "code", "duree", "detail", "tags",
                "tokens-avant", "tokens-apres")


def lire_entier_option(texte):
    """Retourne l'entier d'une option, ou None si absente ou non numerique."""
    return int(texte) if texte and texte.isdigit() else None


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    outil = options.get("outil", "")
    commande = options.get("commande", "")
    code_texte = options.get("code", "")
    duree_texte = options.get("duree", "")
    detail = options.get("detail", "")
    tags = separer_tags(options.get("tags", ""))

    if not outil or not commande or not code_texte.isdigit() or not tags:
        print('Usage : python main.py noter --outil <nom> --commande <verbe> --code <n> [--duree <ms>] [--tokens-avant <n>] [--tokens-apres <n>] --tags "a,b"')
        return 2

    code = int(code_texte)
    duree = lire_entier_option(duree_texte)
    tokens_avant = lire_entier_option(options.get("tokens-avant", ""))
    tokens_apres = lire_entier_option(options.get("tokens-apres", ""))
    entree = fabriquer_entree(outil, commande, code, duree, detail, tags, tokens_avant, tokens_apres)
    ajouter_ligne(entree)
    print(
        "Usage note : " + entree["outil"] + "/" + entree["commande"]
        + " (code " + str(entree["code"]) + ") -- empreinte non applicable (journal ajout seul)"
    )
    return 0
