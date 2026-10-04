"""Categorie editer : orchestre le remplacement atomique d'une occurrence exacte.

Interface entre main.py et les fonctions simples (editer/fonctions.py).
"""
from commun import (decoder_contenu_base64, extraire_options,
                    refuser_options_sans_valeur)
from constants import NOMS_OPTIONS_EDITER
from editer.fonctions import executer_editer

NOMS_OPTIONS = NOMS_OPTIONS_EDITER

# Les TROIS transports d UN texte, par cote (l ancien et le nouveau) : EN LIGNE
# (--ancien), par FICHIER (--ancien-fichier), ou en BASE64 (--ancien-base64).
# POURQUOI LE BASE64 (MO-376) : sans lui, un texte portant un accent, un accent
# grave ou un guillemet etait MANGE par la chaine (shell, coquille) et il fallait
# fabriquer des fichiers de travail OLD/NEW -- des jetables qui n ont plus de raison
# d etre. Le DECODAGE est celui de --contenu-base64 (commun.py) : UN SEUL domicile
# pour le transport sans echappement (M-076).
COTES = ("ancien", "nouveau")


def resoudre_cote(options, cote):
    """(code, texte, bit_exact) pour UN cote : un seul transport, jamais deux.

    Rend (0, texte, True) pour le transport BASE64 (les octets demandes, sans
    heuristique) ; (0, "", False) pour les transports historiques (en ligne ou par
    fichier), que `executer_editer` resout comme avant ; (2, message, False) si deux
    transports sont fournis ENSEMBLE -- un melange silencieux ferait gagner l un des
    deux sans le dire.
    """
    fournis = [nom for nom in (cote, cote + "-fichier", cote + "-base64")
               if options.get(nom, "")]
    if len(fournis) > 1:
        return 2, ("REFUS : --" + " et --".join(fournis)
                   + " sont EXCLUSIFS : un seul transport par cote."), False
    blob = options.get(cote + "-base64", "")
    if blob:
        code, texte = decoder_contenu_base64(blob)
        return code, texte, True
    return 0, "", False


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    code = refuser_options_sans_valeur(options)
    if code:
        return code
    fichier = options.get("fichier", "")
    ancien = options.get("ancien", "")
    nouveau = options.get("nouveau", "")
    ancien_fichier = options.get("ancien-fichier", "")
    nouveau_fichier = options.get("nouveau-fichier", "")
    bit_exacts = False

    # Les transports BASE64 sont resolus ICI, une fois, et leur verdict est DIT :
    # c est ce qui rend l ecriture bit-exacte (aucune heuristique en aval).
    for cote in COTES:
        code_cote, texte, est_base64 = resoudre_cote(options, cote)
        if code_cote != 0:
            print(texte)
            return code_cote
        if est_base64:
            bit_exacts = True
            if cote == "ancien":
                ancien, ancien_fichier = texte, ""
            else:
                nouveau, nouveau_fichier = texte, ""

    if not fichier:
        print("Usage : python main.py editer --fichier <chemin> --ancien \"<old>\" --nouveau \"<new>\"")
        print("       python main.py editer --fichier <chemin> --ancien-fichier <chemin> --nouveau-fichier <chemin>")
        print("Anti-heredoc : --ancien @cerveau-projet/matrix/matrice/tmp/old.txt")
        print("Bit-exact : --ancien-base64 <blob> --nouveau-base64 <blob> (transport SANS echappement : accents, guillemets)")
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
    return executer_editer(fichier, ancien, nouveau, ancien_fichier, nouveau_fichier,
                           bit_exacts)
