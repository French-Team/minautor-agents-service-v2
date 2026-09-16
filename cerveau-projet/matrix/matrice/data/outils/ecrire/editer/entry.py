"""Categorie editer : orchestre le remplacement atomique d'une occurrence exacte.

Interface entre main.py et les fonctions simples (editer/fonctions.py).
"""
from commun import extraire_options
from editer.fonctions import executer_editer

NOMS_OPTIONS = ("fichier", "ancien", "nouveau", "ancien-fichier", "nouveau-fichier")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    fichier = options.get("fichier", "")
    ancien = options.get("ancien", "")
    nouveau = options.get("nouveau", "")
    ancien_fichier = options.get("ancien-fichier", "")
    nouveau_fichier = options.get("nouveau-fichier", "")

    if not fichier:
        print("Usage : python main.py editer --fichier <chemin> --ancien \"<old>\" --nouveau \"<new>\"")
        print("       python main.py editer --fichier <chemin> --ancien-fichier <chemin> --nouveau-fichier <chemin>")
        print("Anti-heredoc : --ancien @cerveau-projet/matrix/matrice/tmp/old.txt")
        return 2
    # Au moins un ancien et un nouveau (meme vide nouveau autorise)
    if not ancien and not ancien_fichier:
        print("REFUS : --ancien ou --ancien-fichier requis.")
        return 2
    if ancien and ancien_fichier:
        print("REFUS : --ancien et --ancien-fichier exclusifs.")
        return 2
    if nouveau_fichier and "nouveau" in options and options["nouveau"]:
        # Si nouveau-fichier fourni, on ignore nouveau direct si vide ?
        pass
    if nouveau_fichier and ancien and nouveau and nouveau_fichier:
        # Les deux nouveaux fournis -> exclusif
        if options.get("nouveau", "") and options.get("nouveau-fichier", ""):
            print("REFUS : --nouveau et --nouveau-fichier exclusifs.")
            return 2
    return executer_editer(fichier, ancien, nouveau, ancien_fichier, nouveau_fichier)
