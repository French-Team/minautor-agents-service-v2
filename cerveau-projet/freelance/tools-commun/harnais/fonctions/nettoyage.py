# -*- coding: utf-8 -*-
"""fonctions/nettoyage.py - COMPENSATION : le harnais corrige les erreurs
de l agent sans qu il ait a y penser (decision utilisateur 2026-08-25).

L agent oublie de supprimer son dossier tmp-<agent> en fin de mission ?
Le harnais le detecte et le NETTOIE (avec un message clair). Les erreurs
de l agent sont COMPENSEES par le harnais, jamais laissees en suspens.

Regles :
  - Un dossier tmp-<agent>/ a la racine est LEGITIME pendant la mission.
  - En fin de mission (APRES l execution), il DOIT etre supprime.
  - Le harnais detecte les tmp-* residuels et les signale/nettoye selon
    la config (nettoyage_auto: true = suppression, false = signalement).
"""

import os
import re
import sys

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)


def detecter_residus(tmp_dir_actuel=None):
    """Detecter les dossiers tmp-* residuels a la racine du workspace.

    Retourne la liste des dossiers tmp-* (hors celui de la mission
    courante, s il est passe en tmp_dir_actuel).
    """
    residus = []
    try:
        entrees = os.listdir(RACINE)
    except OSError:
        return residus
    for nom in entrees:
        if re.match(r"^tmp-[A-Za-z0-9_-]+$", nom) and \
                os.path.isdir(os.path.join(RACINE, nom)):
            if tmp_dir_actuel and os.path.abspath(
                    os.path.join(RACINE, nom)) == \
                    os.path.abspath(tmp_dir_actuel):
                continue
            residus.append(nom)
    return sorted(residus)


def nettoyer(agent="", auto=True, tmp_dir_actuel=None):
    """Compenser : nettoyer les dossiers tmp-* residuels.

    Retourne (nettoyes, signales) : (listes de noms).
    auto=True  -> suppression (compensation)
    auto=False -> signalement seul (l agent decide)
    """
    residus = detecter_residus(tmp_dir_actuel=tmp_dir_actuel)
    nettoyes, signales = [], []
    for nom in residus:
        chemin = os.path.join(RACINE, nom)
        try:
            if auto:
                # suppression recursive (compensation de l oubli)
                for r, _, fichiers in os.walk(chemin, topdown=False):
                    for f in fichiers:
                        os.remove(os.path.join(r, f))
                    try:
                        os.rmdir(r)
                    except OSError:
                        pass
                try:
                    os.rmdir(chemin)
                except OSError:
                    pass
                if not os.path.exists(chemin):
                    nettoyes.append(nom)
                else:
                    signales.append(nom)
            else:
                signales.append(nom)
        except OSError:
            signales.append(nom)
    return nettoyes, signales


def rapport_compensation(nettoyes, signales):
    """Message clair du harnais sur la compensation effectuee."""
    lignes = []
    if nettoyes:
        lignes.append("COMPENSATION : %d dossier(s) tmp-* oublie(s) "
                      "NETTOYE(S) par le harnais : %s"
                      % (len(nettoyes), ", ".join(nettoyes)))
    if signales:
        lignes.append("SIGNALE : %d dossier(s) tmp-* restant(s) (suppression "
                      "impossible ou auto=False) : %s"
                      % (len(signales), ", ".join(signales)))
    return lignes