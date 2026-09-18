"""Categorie ecrire : orchestre la creation/remplacement/ajout atomique.

Interface entre main.py et les fonctions simples (ecrire/fonctions.py).
"""
from commun import decoder_contenu_base64, extraire_options, refuser_options_sans_valeur
from constants import NOMS_OPTIONS_ECRIRE
from ecrire.fonctions import executer_ecrire

NOMS_OPTIONS = NOMS_OPTIONS_ECRIRE

# Le contenu a UNE SEULE source (EO-156, etendu MO-173) : la PRESENCE de l option
# fait foi, jamais sa verite -- sinon une valeur vide passerait pour une absence.
SOURCES_CONTENU = ("contenu", "contenu-fichier", "contenu-base64")
USAGE = chr(10).join([
    "Usage : python main.py ecrire --fichier <chemin> ( --contenu <texte|@fichier> | --contenu-fichier <source> | --contenu-base64 <blob> ) [--mode creer|remplacer|ajouter]",
    "Modes : creer (refuse si existe), remplacer (defaut), ajouter (concatene)",
    "Anti-heredoc : --contenu @cerveau-projet/matrix/matrice/tmp/source.txt",
    "Contenu fortement quote (antislash, triples guillemets imbriques) : passer par --contenu-base64 -- transport SANS echappement",
])


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    code = refuser_options_sans_valeur(options)
    if code:
        return code
    fichier = options.get("fichier", "")
    mode = options.get("mode", "remplacer").strip() or "remplacer"
    if not fichier:
        print(USAGE)
        return 2

    sources = [nom for nom in SOURCES_CONTENU if nom in options]
    if len(sources) > 1:
        print("REFUS : --" + " et --".join(sources) + " sont EXCLUSIFS : le contenu a UNE seule source.")
        return 2
    if not sources:
        print(USAGE)
        return 2

    contenu = options.get("contenu", "")
    contenu_fichier = options.get("contenu-fichier", "")
    if "contenu-base64" in options:
        # Transport SANS echappement (MO-173) : le blob ne porte ni guillemet, ni
        # antislash, ni saut de ligne -- aucune couche traversee ne peut le
        # deformer. La porte decode, valide, et refuse NOMMEMENT.
        code, contenu = decoder_contenu_base64(options.get("contenu-base64", ""))
        if code:
            print(contenu)
            return code
    if not contenu and not contenu_fichier:
        print("REFUS : le contenu resolu est VIDE -- ecrire un fichier vide est une INTENTION, jamais un oubli :"
              " une source videe en silence se lirait pas de contenu (EO-156).")
        return 2
    return executer_ecrire(fichier, contenu, contenu_fichier, mode)
