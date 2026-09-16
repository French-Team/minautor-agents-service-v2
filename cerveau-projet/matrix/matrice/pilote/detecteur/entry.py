"""Categorie detecteur : detection de mots-cles et lancement du pilote Optimus."""

import importlib.util
from pathlib import Path

# Le detecteur est un SCRIPT autonome au nom TIRE : detecteur-mots-cles.py.
# Un nom de module Python ne peut pas porter de tiret, donc l'import classique
# `from detecteur_mots_cles import ...` etait IMPOSSIBLE et faisait planter le
# pilote des son import (Flux 1 entierement rompu -- attrape par
# lanceur-non-regression-flux, maillon PILOTE). Correction : chargement du
# script PAR CHEMIN, sans le renommer (son nom est cite dans ses propres
# exemples d'usage et dans les docs de la Matrice).
CHEMIN_DETECTEUR = Path(__file__).resolve().parent.parent / "detecteur-mots-cles.py"
NOM_MODULE = "detecteur_mots_cles"


def charger_detecteur():
    """Charge detecteur-mots-cles.py par son chemin et retourne le module.

    Le script est garde par `if __name__ == "__main__"` : le charger n'execute
    rien. Une erreur de chargement est ICI une erreur d'import legitime (le
    pilote doit le dire, pas mourir en silence).
    """
    specification = importlib.util.spec_from_file_location(NOM_MODULE, CHEMIN_DETECTEUR)
    if specification is None or specification.loader is None:
        raise ImportError("detecteur introuvable : " + str(CHEMIN_DETECTEUR))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


_DETECTEUR = charger_detecteur()
detecter_mot_cle = _DETECTEUR.detecter_mot_cle
lister_mots_cles = _DETECTEUR.lister_mots_cles
traiter_mot_cle = _DETECTEUR.traiter_mot_cle


def executer(arguments):
    """Executer une commande de detection."""
    # Parser les arguments
    texte = None
    lister = False
    
    for i, arg in enumerate(arguments):
        if arg == "--texte" and i + 1 < len(arguments):
            texte = arguments[i + 1]
        elif arg == "mots-cles":
            lister = True
    
    if lister or not texte:
        lister_mots_cles()
        return 0
    
    # Detecter les mots-cles
    mots_cles = detecter_mot_cle(texte)
    
    if not mots_cles:
        print("Aucun mot-cle detecte dans le texte.")
        return 0
    
    print(f"Mots-cles detectes : {len(mots_cles)}")
    print()
    
    # Traiter chaque mot-cle
    for mc in mots_cles:
        traiter_mot_cle(mc["mot_cle"], mc["config"], texte)
        print()
    
    return 0
