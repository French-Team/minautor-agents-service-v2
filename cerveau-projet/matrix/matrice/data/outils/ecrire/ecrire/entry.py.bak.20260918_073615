"""Categorie ecrire : orchestre la creation/remplacement/ajout atomique.

Interface entre main.py et les fonctions simples (ecrire/fonctions.py).
"""
from commun import extraire_options
from ecrire.fonctions import executer_ecrire

NOMS_OPTIONS = ("fichier", "contenu", "contenu-fichier", "mode")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    fichier = options.get("fichier", "")
    contenu = options.get("contenu", "")
    contenu_fichier = options.get("contenu-fichier", "")
    mode = options.get("mode", "remplacer").strip() or "remplacer"

    if not fichier:
        print("Usage : python main.py ecrire --fichier <chemin> --contenu \"<texte|@fichier>\" [--mode creer|remplacer|ajouter]")
        print("       python main.py ecrire --fichier <chemin> --contenu-fichier <chemin-source> [--mode ...]")
        print("Modes : creer (refuse si existe), remplacer (defaut), ajouter (concatene)")
        print("Anti-heredoc : --contenu @cerveau-projet/matrix/matrice/tmp/source.txt")
        return 2
    if not contenu and not contenu_fichier:
        print("Usage : python main.py ecrire --fichier <chemin> --contenu \"...\" ou --contenu-fichier <chemin>")
        return 2
    if contenu and contenu_fichier:
        print("REFUS : --contenu et --contenu-fichier exclusifs (un seul).")
        return 2
    return executer_ecrire(fichier, contenu, contenu_fichier, mode)
