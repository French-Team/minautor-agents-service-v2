"""Entree du verbe comparer : options -> sujet -> rapport.

Role : ORCHESTRER. Les regles de forme ne vivent pas ici : elles viennent du
domicile partage (carte_identite.py) et du modele de reference.
"""
# commun D ABORD : son bloc de lancement pose data/commun sur le chemin avant
# tout import du domicile partage (l ordre des imports tue en silence).
from commun import CLE_SANS_VALEUR, extraire_options
from constants import CHOIX_MODELE, CODE_REFUS, MODELE_DEFAUT

from comparer.fonctions import comparer_corpus, comparer_fichier

NOMS_CONNUS = ("fichier", "dans", "modele")
DRAPEAUX = ("corpus",)


def executer_verbe(arguments):
    """Parse, choisit le sujet (une carte OU le corpus), puis rend le rapport."""
    options = extraire_options(arguments, NOMS_CONNUS, drapeaux=DRAPEAUX,
                               outil="carte-comparer")
    sans_valeur = options.get(CLE_SANS_VALEUR)
    if sans_valeur:
        print("REFUS : option privee de valeur : "
              + ", ".join("--" + nom for nom in sans_valeur))
        return CODE_REFUS
    a_fichier = bool(options.get("fichier"))
    a_dans = bool(options.get("dans"))
    a_corpus_explicite = "corpus" in options
    if a_fichier and (a_corpus_explicite or a_dans):
        print("REFUS : --fichier et --corpus (ou --dans) sont EXCLUSIFS :"
              " une carte, ou TOUT le corpus.")
        return CODE_REFUS
    if not a_fichier and not a_corpus_explicite and not a_dans:
        # SUJET PAR DEFAUT : sans rien, comparer rend l inventaire du CORPUS
        # (la racine matrix/) -- c est ce que le combo CV-008 appelle, et un
        # appel oublieux ne peut rien casser : l outil est lecture seule.
        print("AUCUN SUJET DONNE : corpus par defaut (racine matrix/)"
              " -- --fichier <chemin> pour UNE carte, --dans pour un perimetre.")
        a_corpus_explicite = True
    modele = (options.get("modele") or MODELE_DEFAUT).strip().lower()
    if modele not in CHOIX_MODELE:
        print("REFUS : --modele inconnu : " + modele
              + " (connus : " + ", ".join(CHOIX_MODELE) + ")")
        return CODE_REFUS
    options["modele"] = modele
    if a_fichier:
        return comparer_fichier(options)
    return comparer_corpus(options)
