'''Categorie service : le SERVICE du planning des routines (MO-429).

Il gere le PLANNING : il ALLUME individuellement les routines DUES en mode
passe (leur commande vient du planning), il RECOIT leur resultat (code retour,
trace de lancement, passe publiee), il TRANSFORME les ecarts en messages par la
porte UNIQUE signaler -- decisions createur D1 a D5 du 2026-09-26.

Usage :
    python main.py service etat [--racine <matrix>]   (lecture seule)
    python main.py service tour [--racine <matrix>]   (UN tour de service)

Le tour est aussi APPELE par le serveur matrice a chaque cycle de supervision :
le service n a pas sa propre boucle, le resident EST le serveur (D2 : il est le
seul a vivre entre deux passes).
'''
from planning_routines import PlanningIllisible
from service.fonctions import resume_etat, servir_un_tour


def _racine(arguments):
    '''--racine <dossier qui contient matrice/> : un cobaye passe le sien.'''
    for index, morceau in enumerate(arguments):
        if morceau == '--racine' and index + 1 < len(arguments):
            return arguments[index + 1]
    return None


def executer(arguments):
    if not arguments:
        print(__doc__)
        return 2
    racine = _racine(arguments)
    commande = arguments[0]
    try:
        if commande == 'etat':
            for ligne in resume_etat(racine):
                print(ligne)
            return 0
        if commande == 'tour':
            allumages, messages, code = servir_un_tour(racine)
            print('tour de service : ' + str(allumages) + ' allumage(s)')
            for message in messages:
                print('  ' + message)
            if not messages:
                print('  rien a dire ce tour (aucune routine due)')
            return code
    except PlanningIllisible as refus:
        # Un refus de porte se LIT : le service ne devine jamais (L-055).
        print('REFUS : ' + str(refus))
        return 2
    print(__doc__)
    return 2
