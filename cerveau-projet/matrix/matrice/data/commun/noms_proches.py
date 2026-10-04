"""noms_proches -- le DOMICILE de la regle < les noms PROCHES d un nom fautif > (MO-468).

POURQUOI CE MODULE EXISTE : la MEME regle vivait en DEUX copies, et les deux ne se
comportaient PAS pareil.
  1. matrice/data/commun/resolution_outils.py -- INCLUSION + PROXIMITE, reparee sous
     MO-367 : elle propose un proche des qu une lettre est oubliee, inseree,
     transposee ou remplacee ;
  2. _operateur/optimus-prime/pilote/injection/modes_emploi.py -- la SOUS-CHAINE seule,
     donc < suivi-optimu > (une lettre oubliee) ne proposait RIEN, alors que
     < suivi-optimus-inconnu > trouvait < suivi-optimus > qui le CONTIENT.
La faute de frappe est le cas ORDINAIRE d un nom inconnu : le refus du pilote se
taisait donc exactement quand l agent en avait besoin, et deux comportements sous un
MEME nom de regle se lisent comme une seule regle (lecon L-029).

LA REGLE VIT ICI, UNE SEULE FOIS (M-076) : les DEUX refuseurs la CONSOMMENT, chacun
avec SON parc (la Matrice d un cote, les racines du pilote de l autre). Ce module ne
connait AUCUN parc : il est PUR -- il propose, il ne devine jamais.
"""
import difflib

# Le seuil de PROXIMITE, declare ici (zero valeur en dur a l usage) : le seuil usuel
# de difflib -- assez haut pour ne pas ramasser n importe quoi, assez bas pour
# attraper une lettre oubliee, transposee ou remplacee.
SEUIL_PROXIMITE = 0.6
# Le NOMBRE de proches qu un refus PROPOSE : la MEME borne pour les deux refuseurs,
# et elle se DIT (un refus qui listerait tout son parc ne serait plus un refus).
NOMBRE_PROCHES = 8


def proches(nom, noms, seuil=SEUIL_PROXIMITE, nombre=NOMBRE_PROCHES):
    """Les noms PROCHES d un nom fautif : par INCLUSION, puis par PROXIMITE.

    L ORDRE est celui de la CERTITUDE : une INCLUSION est une proximite certaine (le
    nom fautif est un prefixe, un suffixe ou un fragment d un nom reel) ; la DISTANCE
    (stdlib difflib) couvre le reste -- la lettre inseree, transposee ou remplacee.
    Les deux se COMPLETENT, aucune n exclut l autre.

    Un nom VIDE ne propose RIEN : la chaine vide est incluse dans TOUS les noms, donc
    sans ce garde un refus listerait tout le parc (le refus deviendrait un annuaire).
    """
    noms = list(noms)
    if not nom:
        return []
    trouves = [candidat for candidat in noms if nom in candidat or candidat in nom]
    for candidat in difflib.get_close_matches(nom, noms, n=nombre, cutoff=seuil):
        if candidat not in trouves:
            trouves.append(candidat)
    return trouves
