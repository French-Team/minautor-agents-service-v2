"""Le TRANSPORT d'une liste : un contrat, UN domicile, pour TOUTES les listes.

Une liste (fichiers, portes, tags, zones d'un perimetre) ne traverse pas une
ligne de commande : elle est JOINTE en une chaine par celui qui appelle,
TRANSPORTEE en argument (ou ecrite dans une variable), puis RECOUPEE par celui
qui la recoit. Les deux bouts doivent employer le MEME caractere -- sinon la
liste se coupe ailleurs qu'ou elle a ete jointe, en silence, et la trace (ou la
variable) enregistre des faits FAUX.

Le defaut repare (friction 72, MO-149) : le caractere etait ecrit EN DUR chez le
joignant (pilote/commun.py, --fichiers et --portes) ET chez chaque coupant
(suivi-optimus/noter, lire/lire), le seul lien entre eux etant un COMMENTAIRE.
Mesure du 2026-09-16 : un nom de fichier qui CONTENAIT le caractere est arrive a
la trace coupe en DEUX faux fichiers, sans un mot. La friction 73 (MO-150) a
generalise : le MEME caractere etait recopie chez ONZE portes de BDD (les tags)
et dans le perimetre-cameleon (une liste de CHEMINS).

Ici vivent les DEUX moities du contrat (M-076, une seule maison par idee) :
`joindre_liste` et `decouper_liste`. Aucun consommateur ne redevine la forme
(L-100/L-102 : une forme recopiee derive en silence).

Deux regles, non negociables :

- une valeur qui CONTIENT le separateur ne peut pas voyager : elle est REFUSEE
  et NOMMEE plutot que jointe en silence (un join silencieux fabrique des faits
  faux) ;
- le refus n'est JAMAIS bloquant pour la mission : l'appelant poursuit sans la
  liste fautive, et le DIT (une trace incomplete se dit, elle ne se tait pas).
"""

SEPARATEUR_LISTE = ","


def nom_transportable(valeur):
    """Rend (True, "") si la valeur peut voyager, (False, raison) sinon.

    Un nom qui porte le separateur serait coupe en deux par celui qui le recoit :
    il est refuse AVANT le transport, et la raison NOMME la valeur (une exemption
    ou un refus muet est un angle mort).
    """
    texte = str(valeur)
    if SEPARATEUR_LISTE in texte:
        return False, ("nom contenant le separateur de transport (" +
                       SEPARATEUR_LISTE + ") : " + texte)
    return True, ""


def noms_refuses(valeurs):
    """Les valeurs d'une liste qui ne peuvent pas voyager (dans leur ordre)."""
    refuses = []
    for valeur in (valeurs or ()):
        transportable, raison = nom_transportable(valeur)
        if not transportable:
            refuses.append(raison)
    return refuses


def partager_liste(valeurs):
    """Separe une liste en (transportables, refuses) -- les valeurs brutes.

    Sert a l'appelant qui doit DIRE ce qu'il n'a pas pu transmettre : refuser
    une valeur sans la nommer serait un refus muet, et un refus muet se lit
    comme une reussite.
    """
    transportables = []
    refuses = []
    for valeur in (valeurs or ()):
        if nom_transportable(valeur)[0]:
            transportables.append(str(valeur))
        else:
            refuses.append(str(valeur))
    return transportables, refuses


def joindre_liste(valeurs):
    """Joint une liste pour le transport. Rend (chaine, refus).

    `refus` est la liste des raisons pour lesquelles la liste N'A PAS ete jointe
    (vide quand tout a voyage). Un seul nom fautif suffit : on ne joint JAMAIS
    une liste dont un membre serait coupe -- celui qui recoit ne saurait pas le
    voir, l'information serait perdue au transport.
    """
    refuses = noms_refuses(valeurs)
    if refuses:
        return "", refuses
    return SEPARATEUR_LISTE.join(str(valeur) for valeur in (valeurs or ())), []


def decouper_liste(chaine):
    """Recoupe une chaine transportee : le pendant EXACT de `joindre_liste`.

    Garde la forme attendue par les portes ("a, b" -> ["a", "b"], chaine vide ->
    liste vide) : le separateur, lui, ne vient que d'ici.
    """
    if not chaine:
        return []
    return [morceau.strip() for morceau in chaine.split(SEPARATEUR_LISTE)
            if morceau.strip()]
