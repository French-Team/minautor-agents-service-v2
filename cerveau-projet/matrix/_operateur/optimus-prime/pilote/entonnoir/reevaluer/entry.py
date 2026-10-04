"""Categorie reevaluer : REJOUER l auto-validation d'un item sur son texte
courant (EO-491).

Interface entre main.py et les fonctions simples (reevaluer/fonctions.py).
"""
from reevaluer.fonctions import reevaluer_item
from stockage import charger_entonnoir, enregistrer_entonnoir, verifier_famille


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


NOMS_OPTIONS = ("id", "forcer")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    if not identifiant:
        print('Usage : python main.py reevaluer --id EO-XXX [--forcer]')
        print("  Rejoue l evaluateur d auto-validation sur le TEXTE COURANT de l item,")
        print("  ecrit les axes et le verdict, et DIT combien d axes ont bouge.")
        print("  Sans texte change depuis le vote : rien n est reecrit (0 axe bouge).")
        print("  --forcer : rejoue meme sur un item depose avant le marqueur de rejeu.")
        return 2
    code, message = verifier_famille(identifiant)
    if code != 0:
        print(message)
        return code
    etat = charger_entonnoir()
    forcer = "--forcer" in arguments or options.get("forcer", "") in ("1", "oui", "vrai")
    code, message, ecrit = reevaluer_item(etat, identifiant, forcer)
    if ecrit:
        enregistrer_entonnoir(etat)
    print(message)
    return code
