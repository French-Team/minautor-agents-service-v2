"""Fonctions communes de l'outil maintenir : lecture, tri, traitement.

Optimus lit les signalements, les tri par importance,
et les traite un par un (serie stricte).
"""
import json
import sys
import time
from pathlib import Path

from constants import (
    BOITE_MAINTENANCE_IN,
    BOITE_MAINTENANCE_OUT,
    ENCODAGE,
    HISTORIQUE,
    NIVEAUX,
)


def lire_signalements():
    """Lit tous les signalements non traites de la boite maintenance.
    Retourne liste de dicts, triee par importance (critique en premier).
    """
    if not BOITE_MAINTENANCE_IN.is_file():
        return []

    messages = []
    for ligne in BOITE_MAINTENANCE_IN.read_text(encoding=ENCODAGE, errors="replace").splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            msg = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if msg.get("type") == "signaler" and not msg.get("traite_par_optimus"):
            messages.append(msg)

    # Tri par niveau (critique en premier)
    messages.sort(key=lambda m: m.get("niveau_ordre", 99))
    return messages


def marquer_traite(index):
    """Marque un message comme traite dans l'inbox."""
    if not BOITE_MAINTENANCE_IN.is_file():
        return
    lignes = BOITE_MAINTENANCE_IN.read_text(encoding=ENCODAGE, errors="replace").splitlines()
    if index < len(lignes):
        try:
            msg = json.loads(lignes[index])
            msg["traite_par_optimus"] = True
            msg["traite_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
            lignes[index] = json.dumps(msg, ensure_ascii=False)
            with open(BOITE_MAINTENANCE_IN, "w", encoding=ENCODAGE, newline="\n") as f:
                for l in lignes:
                    f.write(l + "\n")
        except json.JSONDecodeError:
            pass


def enregistrer_traitement(message, action, resultat):
    """Enregistre le traitement dans l'historique."""
    HISTORIQUE.parent.mkdir(parents=True, exist_ok=True)
    entree = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "outil": message.get("outil", "?"),
        "niveau": message.get("niveau", "?"),
        "description": message.get("description", "")[:200],
        "action": action,
        "resultat": resultat,
    }
    with open(HISTORIQUE, "a", encoding=ENCODAGE, newline="\n") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")


def formater_signal(msg, index=None):
    """Formate un signal pour affichage."""
    niveau = msg.get("niveau", "?")
    icon = {"critique": "[!!!]", "haute": "[!!]", "moyenne": "[!]", "basse": "[.]"}.get(niveau, "[-]")
    prefixe = f"  {index}. " if index is not None else "  "
    lignes = [
        f"{prefixe}{icon} {niveau.upper()} | {msg.get('outil', '?')}",
        f"     {msg.get('description', '')[:120]}",
    ]
    if msg.get("mission"):
        lignes.append(f"     Mission : {msg['mission']}")
    if msg.get("erreur"):
        lignes.append(f"     Erreur : {msg['erreur'][:100]}")
    lignes.append(f"     Date : {msg.get('date', '?')}")
    return "\n".join(lignes)


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus, drapeaux=("json", "etat"))


def signaler_inconnues(options, noms_connus, usage):
    """DIT une option inconnue (mot du domicile partage, EO-179) : meme motif que
    la porte rechercher -- l outil dit le PROBLEME et le GESTE (MO-239). Sans cet
    appel, la mesure du 2026-09-19 rendait CODE 0 sur --option-bidon : le resultat
    du DEFAUT, indiscernable d un resultat correct (L-055)."""
    from options import signaler_inconnues as signaler  # domicile partage (EO-179)
    return signaler(options, "maintenir", noms_connus, usage)
