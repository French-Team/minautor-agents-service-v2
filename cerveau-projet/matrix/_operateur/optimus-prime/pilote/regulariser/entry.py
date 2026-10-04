"""Categorie regulariser : la file dit terminee une mission dont le journal porte la fin.

MO-461 / EO-433. Interface entre main.py et les fonctions simples
(regulariser/fonctions.py).

CE QUE CE VERBE NE FAIT PAS, et c est delibere : il ne CREE aucune mission, il
n ECRIT aucune fin au journal et il ne touche pas a la mission EN COURS. Il
CONSTATE une fin qui vit deja dans le journal -- c est ce qui le separe d
`enregistrer` (qui cree la mission et la fin) et de `fin` (qui close le round
OUVERT). C est cette etroitesse qui rend la preuve possible : le controle de
coherence doit continuer d ACCUSER une mission terminee dans la file sans fin au
journal, et rien ici ne peut l en empecher.
"""
from commun import charger_file, extraire_options
from regulariser.fonctions import regulariser_mission

NOMS_OPTIONS = ("id", "motif")


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    identifiant = (options.get("id") or "").strip().upper()
    motif = (options.get("motif") or "").strip()
    if not identifiant:
        print('Usage : python main.py regulariser --id MO-00X --motif "..."')
        print("        Le --id est celui d une mission de la FILE ; le motif est"
              " OBLIGATOIRE : une regularisation se TRACE, jamais muette.")
        return 2
    return regulariser_mission(charger_file, identifiant, motif)
