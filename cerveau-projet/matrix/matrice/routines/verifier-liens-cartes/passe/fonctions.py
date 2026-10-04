"""Passe de la routine verifier-liens-cartes -- LE GRAPHE DES LIENS DES CARTES.

Ce que la passe MESURE, et rien d autre :
  1. la FORME canonique des liens declares (un chemin depuis la racine des
     documents, jamais un nom seul ni un chemin absolu) ;
  2. la cible EXISTE-t-elle (un lien mort est un voisin disparu) ;
  3. le lien est-il EGOcentrique (un document qui se nomme lui-meme) ;
  4. le lien est-il RECIPROQUE (si A nomme B, B nomme-t-il A) -- c est le controle
     que le GARDE des cartes ne fait PAS (lui juge la forme, la mort et l
     egocentrisme, EO-347), et c est celui qui sert : retrouver les fichiers
     CONNECTES a celui qu on doit modifier ;
  5. la COUVERTURE : combien de cartes declarent des liens (mesure du 2026-09-23 :
     113 cartes, ZERO lien declare -- le mecanisme existait, personne ne s en
     servait).

RIEN N EST DEVINE : la grammaire des cartes (matrice/data/commun/carte_identite.py)
et la forme des chemins de la Matrice (matrice/data/commun/cible.py) restent a leur
DOMICILE ; la passe les CONSOMME (M-076, L-029).
"""
import json
import os
from datetime import datetime

from battement import ajouter_passe, lire_anneau
from carte_identite import carte_de_fichier, liens_de_carte
from cible import forme_canonique
from constants import (
    CHEMIN_ETAT,
    CHEMIN_RAPPORT,
    CLE_ANNEAU_PASSES,
    ENCODAGE_ETAT,
    EXTENSION_DOCUMENT,
    FORMAT_HORODATAGE,
    NOM_RAPPORT,
    PASSES_GARDEES_ETAT,
    RACINE_DOCUMENTS,
    ZONES_IGNOREES,
)

CLE_CANONIQUE = "canonique"
CLE_MORT = "mort"
CLE_EGOCENTRIQUE = "egocentrique"
CLE_SANS_RETOUR = "sans-retour"
MESSAGE_MAX_ANOMALIES = 8


def chemin_canonique(chemin, racine):
    """Le chemin canonique d un document : RELATIF a la racine des documents.

    C est la forme que les cartes doivent ecrire, et c est aussi celle que le
    moteur de recherche et la BDD des modifications emploient : une seule forme
    de chemin dans toute la Matrice.
    """
    return str(chemin.relative_to(racine)).replace("\\", "/")


def documents():
    """Les documents du corpus, hors zones ignorees et hors points de restauration."""
    trouves = []
    for chemin in sorted(RACINE_DOCUMENTS.rglob("*" + EXTENSION_DOCUMENT)):
        if ".bak" in chemin.name:
            continue
        texte = "/" + str(chemin).replace("\\", "/") + "/"
        if any(zone in texte for zone in ZONES_IGNOREES):
            continue
        trouves.append(chemin)
    return trouves


def cible_du_lien(lien, racine):
    """Le fichier vise par un lien canonique, ou None (lien mort)."""
    candidat = racine / lien
    return candidat if candidat.is_file() else None


def mesurer():
    """Retourne (comptes, anomalies) : le graphe des liens, sans rien ecrire."""
    racine = RACINE_DOCUMENTS
    tous = documents()
    cartes = []
    for chemin in tous:
        carte = carte_de_fichier(chemin)
        if carte is not None:
            cartes.append((chemin, liens_de_carte(carte)))
    comptes = {
        "documents": len(tous),
        "cartes": len(cartes),
        "cartes_avec_liens": 0,
        "liens": 0,
        "fautifs": 0,
        "morts": 0,
        "egocentriques": 0,
        "cibles_sans_carte": 0,
        "reciproques": 0,
        "sans_retour": 0,
    }
    anomalies = []
    for chemin, liens in cartes:
        if liens:
            comptes["cartes_avec_liens"] += 1
        source = chemin_canonique(chemin, racine)
        for lien in liens:
            comptes["liens"] += 1
            if forme_canonique(lien, chemin) != lien:
                comptes["fautifs"] += 1
                anomalies.append((CLE_CANONIQUE, source, lien))
                continue
            if lien == source:
                comptes["egocentriques"] += 1
                anomalies.append((CLE_EGOCENTRIQUE, source, lien))
                continue
            cible = cible_du_lien(lien, racine)
            if cible is None:
                comptes["morts"] += 1
                anomalies.append((CLE_MORT, source, lien))
                continue
            carte_cible = carte_de_fichier(cible)
            if carte_cible is None:
                # Un fichier SANS carte (un .py, un document muet) ne peut PAS
                # rendre un lien : la reciprocite n est exigible qu entre DOCUMENTS
                # qui portent une carte. On le COMPTE -- on ne le condamne pas.
                comptes["cibles_sans_carte"] += 1
                continue
            retours = liens_de_carte(carte_cible)
            if source in retours:
                comptes["reciproques"] += 1
            else:
                comptes["sans_retour"] += 1
                anomalies.append((CLE_SANS_RETOUR, source, lien))
    return comptes, anomalies


def messages_de_passe(comptes, anomalies):
    """Le resume (TOUJOURS) puis les anomalies BORNEES : une veille qui crie tout ne se lit plus."""
    messages = [
        "cartes " + str(comptes["cartes"]) + "/" + str(comptes["documents"])
        + " | avec liens " + str(comptes["cartes_avec_liens"])
        + " | liens " + str(comptes["liens"])
        + " | reciproques " + str(comptes["reciproques"])
        + " | cibles sans carte " + str(comptes["cibles_sans_carte"])
        + " | sans retour " + str(comptes["sans_retour"])
        + " | morts " + str(comptes["morts"])
        + " | fautifs " + str(comptes["fautifs"])
        + " | egocentriques " + str(comptes["egocentriques"]),
    ]
    for etat, source, lien in anomalies[:MESSAGE_MAX_ANOMALIES]:
        messages.append(etat + " : " + source + " -> " + lien)
    reste = len(anomalies) - MESSAGE_MAX_ANOMALIES
    if reste > 0:
        messages.append("... et " + str(reste) + " autre(s) anomalie(s) : voir " + NOM_RAPPORT)
    return messages


def ecrire_rapport(comptes, anomalies):
    """Ecrit le RAPPORT (la memoire longue de la passe) : atomique, JSON stable."""
    donnees = {
        "type": "rapport-liens",
        "date": datetime.now().strftime(FORMAT_HORODATAGE),
        "comptes": comptes,
        "anomalies": [{"etat": etat, "source": source, "lien": lien}
                      for etat, source, lien in anomalies],
    }
    temporaire = CHEMIN_RAPPORT.with_name(CHEMIN_RAPPORT.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE_ETAT, newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_RAPPORT))
    return CHEMIN_RAPPORT


def passer():
    """UNE passe de la routine : retourne (nombre, messages).

    `nombre` = les liens analyses (0 est un compte LEGITIME : un corpus sans lien
    declare est un fait, pas un silence -- le rapport le dit).
    """
    comptes, anomalies = mesurer()
    ecrire_rapport(comptes, anomalies)
    return comptes["liens"], messages_de_passe(comptes, anomalies)


def publier_passe(nombre, messages):
    """Ecrit l'ETAT COURT de la passe : ce que la routine a fait, et QUAND.

    Le battement REEL d'une routine est un ETAT, pas une histoire : il s'ecrit
    ici, a CHAQUE passe et ECRASE. C'est ce que lit `verifier-cadence`, qui le
    compare a la cadence DECLAREE. Meme contrat que suivi-sync : l'anneau borne
    vient du moteur PARTAGE `data/commun/battement.py` (L-029).
    """
    passe = datetime.now().strftime(FORMAT_HORODATAGE)
    donnees = {
        "type": "passe",
        "date": passe,
        "traitees": nombre,
        "messages": len(messages or []),
        CLE_ANNEAU_PASSES: ajouter_passe(lire_anneau(CHEMIN_ETAT, CLE_ANNEAU_PASSES),
                                         passe, PASSES_GARDEES_ETAT),
    }
    temporaire = CHEMIN_ETAT.with_name(CHEMIN_ETAT.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE_ETAT, newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_ETAT))
    return CHEMIN_ETAT
