#!/usr/bin/env python3
# -*- coding: ascii -*-
# rotation.py -- ROTATION DES INBOX (decision utilisateur 2026-08-29)
#
# Les routines et les envois Oracle ecrivaient en APPEND dans les fichiers
# inbox/*.jsonl SANS jamais purger : les messages s accumulaient (40+ dans
# cerberus.jsonl, memes sujets repetes par vigie-perimetre/notation/...).
# Personne ne les lisait et personne n en tenait compte.
#
# Ce module centralise l ECRITURE des inbox avec ROTATION : on ne garde que
# les MAX_MESSAGES (5) messages les plus recents du fichier jsonl. Les plus
# anciens sont retires (les nouveaux remplacent les anciens).
#
# Utilise par :
#   - oracle.py        : cmd_envoyer + _envoyer_direct
#   - routines/*.py    : vigie-perimetre, notation, sante, vigie-round,
#                        verifier-statuts (ecritures inbox directes)
#
# Compatibilite : ASCII + LF, stdlib uniquement (aucun import v1/v2).
#
# Version : 0.1.0
# Statut : ebauche

import json
import os
from pathlib import Path

MAX_MESSAGES = 5


def ajouter_message(inbox_dir, agent, message):
    """Ecrire un message dans l inbox de l agent en ne gardant que les
    MAX_MESSAGES messages les plus recents.

    inbox_dir : dossier inbox (Path) ; agent : nom du destinataire ;
    message   : dict JSON du message (de, vers, objet, corps, lu...).

    La rotation : lire les lignes existantes, ajouter le nouveau message,
    ne garder que les MAX_MESSAGES dernieres. Les plus anciennes sont
    retirees (le nouveau message REMPLACE le plus ancien).
    """
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    cible = inbox_dir / ("%s.jsonl" % agent)

    lignes = []
    if cible.is_file():
        try:
            lignes = [l.rstrip("\n") for l in cible.read_text(encoding="utf-8").splitlines()
                      if l.strip()]
        except (ValueError, OSError):
            lignes = []

    # Ajouter le nouveau message (serialise ASCII-compatible).
    lignes.append(json.dumps(message, ensure_ascii=False))

    # Rotation : ne garder que les MAX_MESSAGES plus recents.
    if len(lignes) > MAX_MESSAGES:
        lignes = lignes[-MAX_MESSAGES:]

    try:
        with open(cible, "w", encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
        return True
    except OSError:
        return False


def compter(inbox_dir, agent):
    """Nombre de messages actuellement dans l inbox d un agent."""
    inbox_dir = Path(inbox_dir)
    cible = inbox_dir / ("%s.jsonl" % agent)
    if not cible.is_file():
        return 0
    try:
        return sum(1 for l in cible.read_text(encoding="utf-8").splitlines() if l.strip())
    except (ValueError, OSError):
        return 0
