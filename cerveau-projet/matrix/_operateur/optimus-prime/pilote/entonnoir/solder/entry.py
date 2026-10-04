"""Categorie solder : SOLDER un item deja satisfait, AVEC sa PREUVE (MO-423).

Interface entre main.py et les fonctions simples (solder/fonctions.py).
"""
from stockage import charger_entonnoir, enregistrer_entonnoir, verifier_famille
from solder.fonctions import solder_item


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


NOMS_OPTIONS = ("id", "preuve", "motif")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = options.get("id", "")
    if not identifiant:
        print('Usage : python main.py solder --id EO-XXX --preuve "fichier:ligne | mesure"')
        print("  (l item sort de l entonnoir AVEC sa preuve, au lieu de naitre en mission)")
        return 2
    code, message = verifier_famille(identifiant)
    if code != 0:
        print(message)
        return code
    etat = charger_entonnoir()
    code, message = solder_item(etat, identifiant, options.get("preuve", ""),
                                options.get("motif", ""))
    if code == 0:
        enregistrer_entonnoir(etat)
    print(message)
    return code
