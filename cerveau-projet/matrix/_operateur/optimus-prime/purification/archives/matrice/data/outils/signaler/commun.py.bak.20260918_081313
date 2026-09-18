"""Fonctions communes de l'outil signaler : validation, depot inbox Matrice.

Le cameleon depose un signal dans la boite Matrice inbox.
La Matrice le route ensuite vers intercom maintenance (Optimus).
"""
import json
import sys
import time
from pathlib import Path

from constants import (
    BOITE_MATRICE_INBOX,
    ENCODAGE,
    EXPEDITEUR_DEFAUT,
    EXPEDITEURS,
    NIVEAUX,
    RACINE,
)


def valider_signal(outil, niveau, description):
    """Valide qu'un signal est complet et correct.
    Retourne (est_valide, msg_erreur).
    """
    if not outil or not outil.strip():
        return False, "Nom d'outil requis"
    if not niveau or niveau not in NIVEAUX:
        return False, "Niveau requis parmi : " + ", ".join(NIVEAUX.keys())
    if not description or len(description.strip()) < 10:
        return False, "Description requise (min 10 caracteres)"
    return True, ""


def valider_expediteur(expediteur):
    """Valide l'expediteur contre la liste FERMEE ; retourne (valeur, msg_erreur).

    Un expediteur non declare est refuse : le signal doit dire la VERITE sur
    qui parle (un signal de routine n'est pas un signal du cameleon).
    """
    valeur = (expediteur or "").strip() or EXPEDITEUR_DEFAUT
    if valeur not in EXPEDITEURS:
        return EXPEDITEUR_DEFAUT, "Expediteur requis parmi : " + ", ".join(EXPEDITEURS)
    return valeur, ""


def construire_message(outil, niveau, description, mission="", erreur="", expediteur=EXPEDITEUR_DEFAUT):
    """Construit le message JSON du signal.
    Retourne le dict message.
    """
    return {
        "type": "signaler",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "expediteur": expediteur,
        "destinataire": "matrice",
        "outil": outil.strip(),
        "niveau": niveau,
        "niveau_ordre": NIVEAUX[niveau]["ordre"],
        "niveau_desc": NIVEAUX[niveau]["desc"],
        "description": description.strip(),
        "mission": mission.strip() if mission else "",
        "erreur": erreur.strip() if erreur else "",
    }


def deposer_signal(message):
    """Depose le signal dans la boite inbox Matrice.
    Retourne (succes, msg).
    """
    try:
        BOITE_MATRICE_INBOX.parent.mkdir(parents=True, exist_ok=True)
        with open(BOITE_MATRICE_INBOX, "a", encoding=ENCODAGE, newline="\n") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
        return True, ""
    except OSError as e:
        return False, "Erreur depot : " + str(e)


def formater_sortie(message, mode_json=False):
    """Formate la sortie du signal."""
    if mode_json:
        return json.dumps(message, ensure_ascii=False, indent=2)
    else:
        niveau = message["niveau"]
        icon = {"critique": "[!!!]", "haute": "[!!]", "moyenne": "[!]", "basse": "[.]"}.get(niveau, "[-]")
        lignes = [
            f"SIGNAL DEPOTE : {icon} {niveau.upper()}",
            f"  Outil : {message['outil']}",
            f"  Description : {message['description'][:100]}",
        ]
        if message.get("mission"):
            lignes.append(f"  Mission interrompue : {message['mission']}")
        if message.get("erreur"):
            lignes.append(f"  Erreur : {message['erreur'][:100]}")
        lignes.append("")
        lignes.append("Le message a ete depose dans la boite Matrice.")
        lignes.append("La Matrice va le router vers intercom maintenance (Optimus).")
        return "\n".join(lignes)


def extraire_options(arguments, noms_connus):
    """Extrait --nom valeur et flags sans valeur."""
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau.startswith("--") and morceau[2:] in noms_connus:
            nom = morceau[2:]
            if nom in ("json",):
                options[nom] = "1"
                index += 1
            elif index + 1 < len(arguments):
                options[nom] = arguments[index + 1]
                index += 2
            else:
                options[nom] = ""
                index += 1
        else:
            index += 1
    return options
