"""Fonctions simples de la categorie reprendre : une seule tache chacune."""
import json

from constants import (
    CHEMIN_BOITE_CAMELEON,
    ENCODAGE,
    MESSAGE_REPRISE,
)
from commun import horodater


def notifier_cameleon(id_mission):
    """Depose UN message de reprise dans la boite cameleon (intercom).

    Etancheite conservee : le cameleon apprend que la maintenance est
    TERMINEE, jamais ce qui s'est passe pendant (zero detail).
    """
    message = {
        "type": "reprise",
        "date": horodater(),
        "mission": id_mission,
        "message": MESSAGE_REPRISE,
    }
    CHEMIN_BOITE_CAMELEON.parent.mkdir(parents=True, exist_ok=True)
    with open(CHEMIN_BOITE_CAMELEON, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(message, ensure_ascii=True) + "\n")


def restaurer_mission(etat, file_missions):
    """Remet la mission en pause a SA place exacte dans la file du pilote.

    Reprise a l'identique : meme mission (statut en-cours), meme position
    chronologique dans la file, memes missions restantes autour d'elle.
    Retourne la file modifiee.
    """
    missions = list(etat.get("file_restante", []))
    position = int(etat.get("position", len(missions)))
    position = max(0, min(position, len(missions)))
    missions.insert(position, etat["mission"])
    file_missions["missions"] = missions
    return file_missions
