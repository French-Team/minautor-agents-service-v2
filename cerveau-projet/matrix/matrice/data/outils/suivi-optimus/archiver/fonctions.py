"""Fonctions simples de la categorie archiver : une seule tache chacune.

Le journal suivi-optimus est la trace d'OPTMUS. Il a RECEMPORTE le 2026-09-12
les missions du cameleon (M-XXX) et des libelles d'entonnoir (E-089,
AUDIT-NEMESIS) : 184 evenements qui ne concernent pas Optimus et qui faussent
ses compteurs (la vue, le croisement file <-> journal).

On ne SUPPRIME pas : on ARCHIVE. Meme discipline que MO-023 (fins orphelines
archivees a part) et MO-029 (rotation avec plafond) : un journal d'historique
perd sa valeur si l'on efface ce qu'il contient au lieu de le deplacer.
"""
import json
import os

from constants import ENCODAGE


def separer(evenements, prefixe):
    """Separe (dans le perimetre, hors perimetre) selon le prefixe de mission.

    Un evenement SANS mission (ou avec un champ mission non textuel) est
    hors perimetre : le journal ne note QUE des missions d'optimus.
    """
    dedans, dehors = [], []
    for evenement in evenements:
        mission = evenement.get("mission")
        if isinstance(mission, str) and mission.startswith(prefixe):
            dedans.append(evenement)
        else:
            dehors.append(evenement)
    return dedans, dehors


def signature(evenement):
    """Signature d'un evenement pour l'archive : tout SAUF sa date.

    Un evenement REIMPORTE (par le garde anti-doublon de suivi-sync) ne differe
    de l'original que par sa DATE -- verifie en reel sur M-001 : meme mission,
    meme theme, meme action, meme detail, memes listes. La date est donc exclue
    de la signature, sinon re-archiver remplirait l'archive de jumeaux.
    """
    return json.dumps(
        {cle: valeur for cle, valeur in evenement.items() if cle != "date"},
        ensure_ascii=True,
        sort_keys=True,
    )


def indexer_doublons(evenements, actions_singulieres):
    """Separe (gardes, doublons) pour les actions a UN SEUL evenement par mission.

    Une mission a UN debut et UNE fin : tout evenement suivant pour la meme
    (mission, action) est un DOUBLON. Le PREMIER (ordre du journal) fait foi --
    c'est le fait d'origine, les suivants sont des copies accidentelles.

    Les autres actions (porte, depot, decision, decouverte, bilan) se repetent
    legitimement : le filtre ne les touche jamais.
    """
    vus = set()
    gardes, doublons = [], []
    for evenement in evenements:
        action = evenement.get("action")
        mission = evenement.get("mission")
        if action in actions_singulieres and isinstance(mission, str) and mission:
            cle = (mission, action)
            if cle in vus:
                doublons.append(evenement)
                continue
            vus.add(cle)
        gardes.append(evenement)
    return gardes, doublons


def ajouter_archive(chemin, evenements):
    """AJOUTE a l'archive ce qui n'y est pas deja (append, LF forces).

    Append (jamais d'ecrasement) : deux archivages successifs s'ajoutent au lieu
    de se remplacer. Le dedoublonnage (MO-052) evite d'ecrire deux fois le meme
    evenement quand il a ete reimporte entre deux archivages.
    Retourne le nombre d'evenements REELLEMENT ecrits (les jumeaux sont comptes 0).
    """
    connues = set()
    if chemin.exists():
        try:
            lignes = chemin.read_text(encoding=ENCODAGE).splitlines()
        except OSError:
            lignes = []
        for ligne in lignes:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                connues.add(signature(json.loads(ligne)))
            except json.JSONDecodeError:
                continue
    ecrits = 0
    with open(str(chemin), "a", encoding=ENCODAGE, newline="\n") as flux:
        for evenement in evenements:
            empreinte = signature(evenement)
            if empreinte in connues:
                continue
            connues.add(empreinte)
            flux.write(json.dumps(evenement, ensure_ascii=True) + "\n")
            ecrits += 1
    return ecrits


def reecrire(chemin, evenements):
    """Reecrit un journal de facon ATOMIQUE (tmp + remplacement, LF forces).

    Ecriture atomique : le journal n'est jamais vu a moitie ecrit (lecon M-018).
    """
    temporaire = chemin.with_name(chemin.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE, newline="\n") as flux:
        for evenement in evenements:
            flux.write(json.dumps(evenement, ensure_ascii=True) + "\n")
    os.replace(str(temporaire), str(chemin))
