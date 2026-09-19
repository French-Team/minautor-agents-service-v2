"""Le DOMICILE de l'INTERPRETEUR Python des sous-processus.

Probleme (mesure du 2026-09-19) : le flux dependait d'un interpreteur DECLARE
NULLE PART. `chemin_python()` rendait l'executable du processus courant
(sys.executable) depuis une copie PRIVEE de `routines/veille-flux/constants.py`,
et son seul consommateur etait le module voisin. Deux questions n'avaient donc
aucune reponse ecrite : QUEL interpreteur, et OU se decide-t-il.

Ce module est ce domicile UNIQUE (M-076 : une valeur, une maison ; L-029 : deux
copies divergent en silence). Il lit la declaration dans le CLASSEUR DES
VARIABLES de la Matrice (porte `bdd-variables`), cle `interpreteur-python` :

  - valeur absente, vide ou `auto` -> l'interpreteur du processus courant ;
  - chemin ABSOLU                   -> tel quel, s'il EXISTE ;
  - chemin RELATIF                  -> ancre sur la racine de la Matrice
                                       (moteur partage cible.py), s'il EXISTE.

Regle L-006 : un chemin DECLARE est VERIFIE avant d'etre rendu. Un interpreteur
declare et INTROUVABLE est un REFUS NOMME (ValueError), jamais un repli
silencieux sur sys.executable : une valeur fausse mais qui marche ne crie pas
(lecon du 2026-09-16), et le flux tournerait avec un interpreteur que personne
n'a choisi. Un classeur ABSENT ou ILLISIBLE, lui, n'est pas un refus : c'est un
motif NOMME, et le repli reste l'interpreteur courant -- qui est VRAI, lui.

Ce module n'INSTALLE rien : il ne copie aucun interpreteur dans le depot (un
binaire de centaines de Mo dans un depot texte, gele et jamais patche, serait un
second domicile pour le meme objet). Pour utiliser un interpreteur local ou
embarque, il suffit de DECLARER son chemin par la porte de la BDD des
variables : zero binaire commite, une seule maison pour la decision.

LIMITE ASSUMEE (deposee en item, pas corrigee ici) : la lecture du classeur
(parcours de la liste `variables` sur la cle) est RECOPIEE chez quatre autres
consommateurs (les deux pilotes pour `defcon`, `data/commun/invisibilite.py`).
Un lecteur PARTAGE du classeur est la suite ; ce module ne l'invente pas a sa
place.
"""
import json
import sys
from pathlib import Path

from cible import racine_matrice

# La cle du CLASSEUR DES VARIABLES (porte bdd-variables) qui porte la decision.
CLE_INTERPRETEUR = "interpreteur-python"

# La valeur declaree qui veut dire "l'interpreteur du processus courant".
VALEUR_AUTO = "auto"

# Le classeur, chez son domicile (data/classeur-variables.json, depuis data/commun).
NOM_CLASSEUR = "classeur-variables.json"
CHEMIN_CLASSEUR = Path(__file__).resolve().parent.parent / NOM_CLASSEUR

# Repli quand l'interpreteur courant n'a pas de chemin (embarque sans
# sys.executable) : un nom, jamais un chemin devine.
NOM_INTERPRETEUR_REPLI = "python"


def lire_declaration(chemin_classeur=None):
    """(valeur, motif) : ce que le classeur DECLARE, ou (None, motif) s'il se tait.

    Une absence de declaration n'est PAS une erreur de ce module ; mais elle se
    DIT (un silence se lirait comme "interpreteur declare", ce qui n'est pas la
    meme chose).
    """
    chemin = Path(chemin_classeur) if chemin_classeur is not None else CHEMIN_CLASSEUR
    if not chemin.is_file():
        return None, "aucune declaration (classeur absent : " + str(chemin) + ")"
    try:
        donnees = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, ValueError) as erreur:
        return None, ("aucune declaration (classeur illisible, "
                      + type(erreur).__name__ + " : " + str(chemin) + ")")
    variables = donnees.get("variables") if isinstance(donnees, dict) else None
    if not isinstance(variables, list):
        return None, "aucune declaration (classeur sans liste `variables`)"
    for variable in variables:
        if not isinstance(variable, dict) or variable.get("cle") != CLE_INTERPRETEUR:
            continue
        valeur = variable.get("valeur")
        if valeur is None or not str(valeur).strip():
            return None, "cle " + CLE_INTERPRETEUR + " declaree VIDE"
        return str(valeur).strip(), "declare : " + str(valeur).strip()
    return None, "cle " + CLE_INTERPRETEUR + " non declaree"


def interpreteur_courant():
    """L'interpreteur du processus courant (sys.executable), ou son nom de repli."""
    return sys.executable or NOM_INTERPRETEUR_REPLI


def resoudre(chemin_classeur=None, depart=None):
    """(chemin, motif) : l'interpreteur a utiliser ET le pourquoi, en clair.

    Le motif est rendu pour que l'appelant puisse le DIRE (un choix d'interpreteur
    qui ne s'explique pas est un choix invisible). Leve ValueError sur une
    declaration INTROUVABLE : refus NOMME, jamais un repli muet.
    """
    valeur, motif = lire_declaration(chemin_classeur)
    if valeur is None or valeur.lower() == VALEUR_AUTO:
        return interpreteur_courant(), motif + " -> interpreteur du processus courant"
    chemin = Path(valeur)
    if not chemin.is_absolute():
        chemin = racine_matrice(depart if depart is not None else __file__) / chemin
    if not chemin.is_file():
        raise ValueError(
            "REFUS : interpreteur DECLARE introuvable -- cle " + CLE_INTERPRETEUR
            + " = `" + valeur + "` ; essaye " + str(chemin)
            + " (un chemin relatif s'ancre sur la racine de la Matrice). "
            "Corrige la declaration par la porte de la BDD des variables "
            "(`bdd-variables definir --cle " + CLE_INTERPRETEUR
            + " --valeur <chemin|" + VALEUR_AUTO + ">`), ou retire-la."
        )
    return str(chemin), motif + " -> " + str(chemin)


def chemin_python(chemin_classeur=None, depart=None):
    """L'interpreteur a lancer pour un sous-processus (la raison n'est pas rendue).

    Signature COMPATIBLE avec la fonction privee qu'elle remplace : sans argument,
    elle rend le MEME resultat qu'avant quand aucune declaration n'existe
    (non-regression du flux). Les deux arguments existent pour les cobayes, qui
    eprouvent une declaration sans toucher au classeur de service.
    """
    return resoudre(chemin_classeur, depart)[0]
