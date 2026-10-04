"""Categorie passerelle : orchestre la lecture et l'extraction des demandes du canal.

Interface entre main.py et les fonctions simples (passerelle/fonctions.py).
DEUX gestes, et le premier ne peut rien casser : `lire` ne fait que DIRE, et
`extraire` est DRY par defaut (sans `--appliquer`, RIEN n est ecrit).
"""
from passerelle.fonctions import diagnostiquer, extraire

USAGE = (
    "    python main.py passerelle lire\n"
    "                                       (LIT le canal du user et DIT tout : head, demandes,\n"
    "                                       etats, crochets, anomalies -- AUCUNE ecriture)\n"
    "    python main.py passerelle extraire [--rang N | --tout] [--appliquer]\n"
    "                                       (DEPOSE un item par la porte de l entonnoir, ARCHIVE\n"
    "                                       les mots EXACTS du user au journal du canal, puis\n"
    "                                       RETIRE la demande du canal. DRY par defaut : sans\n"
    "                                       --appliquer, RIEN n est ecrit -- le canal est ecrit\n"
    "                                       par le user EN CONTINU)\n"
)

VERBES = {"lire": diagnostiquer, "extraire": extraire}


def executer(arguments):
    """Route les verbes de la porte `passerelle` (lire, extraire).

    `arguments` porte le NOM de la commande EN TETE : c est la convention du pilote
    (chaque categorie recoit les arguments entiers, comme `file` et `charger`), et
    s en ecarter rendait la porte MUETTE -- elle imprimait son usage au lieu
    d agir (mesure de ce round).
    """
    reste = list(arguments)
    if reste and reste[0] == "passerelle":
        reste = reste[1:]
    if not reste:
        print(USAGE)
        return 0
    fonction = VERBES.get(reste[0])
    if fonction is None:
        print("REFUS : verbe inconnu (" + reste[0] + "). Verbes : "
              + ", ".join(sorted(VERBES)) + ".")
        print(USAGE)
        return 2
    return fonction(reste[1:])
