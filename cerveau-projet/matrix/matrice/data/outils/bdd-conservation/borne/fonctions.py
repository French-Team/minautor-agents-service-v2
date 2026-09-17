"""Fonctions metier du CONTROLE DE LA BORNE (un seul point EN PLACE par famille).

EO-152 (mission MO-165). Mesure MO-164 : 16 points `STRUCTUREL` en trop dans 10
familles sur 88, et la case 8 de la suite (`controler-archives`) restait VERTE.
Elle n'avait pas tort : elle mesure la PERTE (`archive + actif = origine`), et rien
n'avait ete perdu. Ce qui manquait etait une AUTRE question : la BORNE.

La doctrine est celle de la contre-analyse N=1 (MO-156) : une famille de points de
restauration ne garde EN PLACE que son PLUS RECENT -- celui que les deux portes de
revert servent encore ; tout point REMPLACE part a l'archive. Deux points EN PLACE
dans la meme famille veulent donc dire qu'un point DEPASSE garde sa place, et
l'actif grandit d'un point a chaque ecriture.

CE QUI COMPTE COMME "EN PLACE" est mesure, jamais suppose : un point est EN PLACE
quand il est DECIDE et CONSERVE. Un point archive a quitte sa place, et un point
DECIDE `archiver` est sur le depart (l'attente entre le balayage et la rotation est
NORMALE : ce sont deux gestes distincts). Compter ceux-la ferait crier le controle
pendant une operation saine -- un controle qui crie a tort ne garde plus rien.
"""
from archiver.fonctions import origine_complete


def familles(entrees, motif):
    """L'ensemble des familles de points de restauration DECLAREES dans la BDD."""
    noms = set()
    for entree in entrees:
        source = str(entree.get("source", "")).replace("\\", "/")
        if source and motif.search(source.split("/")[-1]):
            noms.add(origine_complete(source))
    return noms


def _grouper(entrees, motif, predicat):
    """{famille: [ids]} des entrees de la famille qui satisfont `predicat`."""
    groupes = {}
    for entree in entrees:
        source = str(entree.get("source", "")).replace("\\", "/")
        if not source or not motif.search(source.split("/")[-1]):
            continue
        if not predicat(entree):
            continue
        groupes.setdefault(origine_complete(source), []).append(str(entree.get("id", "")))
    return groupes


def en_place(entree):
    """Un point EN PLACE : il est DECIDE et CONSERVE."""
    return (entree.get("statut") == "decide"
            and entree.get("verdict") == "conserver")


def en_attente(entree):
    """Un point DECIDE `archiver` : sa place est encore prise, l'ACTE reste a jouer."""
    return (entree.get("statut") == "decide"
            and entree.get("verdict") == "archiver")


def compter_en_place(entrees, motif):
    """Le nombre de points EN PLACE, toutes familles confondues."""
    return sum(len(ids) for ids in _grouper(entrees, motif, en_place).values())


def familles_en_exces(entrees, motif):
    """{famille: [ids]} des familles qui portent PLUS D'UN point EN PLACE.

    C'est la BORNE : rendu vide, elle tient. Chaque famille de la liste est un
    ecart NOMME, avec ses identifiants -- un controle qui dit "il y a un exces"
    sans dire OU oblige a refaire la mesure a la main.
    """
    groupes = _grouper(entrees, motif, en_place)
    return {famille: ids for famille, ids in sorted(groupes.items()) if len(ids) > 1}


def points_en_attente(entrees, motif):
    """[(famille, id)] des points DECIDES `archiver` que l'ACTE n'a pas encore joues.

    Mesure d'INFORMATION : elle ne fait pas echouer le controle. L'attente est
    normale entre le balayage et la rotation ; elle devient anormale quand elle
    survit a une cloture, et ce compte est la pour le montrer.
    """
    groupes = _grouper(entrees, motif, en_attente)
    return [(famille, identifiant)
            for famille, ids in sorted(groupes.items()) for identifiant in ids]
