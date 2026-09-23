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
from archiver.fonctions import (
    chemin_archive, motif_forme, origine_complete, relatif_matrice,
)
from cible import arbres_matrice, resoudre_dans_matrice


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


# --- LA BORNE SE MESURE DES DEUX COTES (P2, MO-309) -------------------------

def familles_sur_disque(depart):
    """{famille: [chemins]} des points de restauration PRESENTS sur le disque.

    P2, validee par le createur le 2026-09-20 (rapport-revision-MO-305, section 3) :
    "hors la DERNIERE copie par famille (N=1), les points de restauration AGES
    sortent du disque vers l archive ; ils ne reviennent que par restaurer".

    Le registre peut dire N=1 pendant que le DISQUE en porte trois : ce sont deux
    mesures differentes, et c est le DISQUE que les deux portes de revert lisent.
    La borne se mesure donc des deux cotes, et les DEUX exces sont nommes.
    """
    motif = motif_forme()
    if motif is None:
        return {}
    base_archive, _, _ = chemin_archive(depart)
    familles = {}
    for base in arbres_matrice(depart):
        for chemin in base.rglob("*"):
            if not chemin.is_file() or "__pycache__" in chemin.parts:
                continue
            if not motif.search(chemin.name):
                continue
            if base_archive == chemin or base_archive in chemin.parents:
                continue
            relatif = relatif_matrice(chemin, depart)
            cle = origine_complete(relatif)
            familles.setdefault(cle, []).append(relatif)
    return familles


def etat_disque_familles(entrees, depart):
    """(ecarts, transitoires) : les familles qui portent PLUS D UN point sur le disque.

    Une famille qui en porte DEUX n est pas forcement fautive : une ECRITURE vient
    de naitre (la porte `ecrire` cree un point a CHAQUE passage) et le point AGE
    part a la PROCHAINE cloture -- le balayage est le juge, et l acte suit. Compter
    ce transitoire comme un ecart ferait crier le controle pendant une operation
    saine, et un controle qui crie a tort ne garde plus rien (doctrine de cette
    famille : le compte des points en attente est une INFORMATION, pas un ecart).

    L ECART est celui que la chaine a FINI de juger : aucune piece de la famille n
    attend (point SANS decision, ou acte `archiver` en attente) et le disque porte
    pourtant ENCORE plus d un point. C est la masse qui ne repart pas -- la reponse
    directe au V1 de la revision (1191 points .bak mesures).
    """
    par_source = {}
    for entree in entrees:
        cle = str(entree.get("source", "")).replace("\\", "/").strip("/").lower()
        if cle:
            par_source[cle] = entree
    familles = familles_sur_disque(depart)
    ecarts = {}
    transitoires = {}
    for nom, chemins in sorted(familles.items()):
        if len(chemins) <= 1:
            continue
        en_attente = False
        for chemin in sorted(chemins):
            entree = par_source.get(str(chemin).replace("\\", "/").strip("/").lower())
            if entree is None or entree.get("statut") in ("propose", "classe"):
                en_attente = True
                break
            if entree.get("statut") == "decide" and entree.get("verdict") == "archiver":
                en_attente = True
                break
        if en_attente:
            transitoires[nom] = sorted(chemins)
        else:
            ecarts[nom] = sorted(chemins)
    return ecarts, transitoires


def points_en_place_absents(entrees, motif, depart):
    """[(famille, id, source)] des points EN PLACE dont le FICHIER a disparu.

    Une place VIDE est une declaration que le disque ne soutient plus : le compte
    des points EN PLACE la compte comme tenue alors qu il n y a plus rien a
    restaurer. C est une DETTE nommee, jamais un exces -- l exces, lui, est un
    point DE TROP a la meme place. Confondre les deux ferait crier le controle
    pendant qu un fichier change forme, et un controle qui crie a tort ne garde
    plus rien (doctrine de cette famille).
    """
    absents = []
    for entree in entrees:
        if not en_place(entree):
            continue
        source = str(entree.get("source", ""))
        if not source or not motif.search(source.split("/")[-1]):
            continue
        chemin, _ = resoudre_dans_matrice(source, depart)
        if chemin is None or not chemin.is_file():
            absents.append((origine_complete(source), str(entree.get("id", "")), source))
    return absents
