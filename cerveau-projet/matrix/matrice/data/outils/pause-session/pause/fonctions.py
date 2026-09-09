"""Fonctions simples de la categorie pause : une seule tache chacune."""
import json

from constants import (
    CHEMIN_BOITE_CAMELEON,
    ENCODAGE,
    MESSAGE_PAUSE,
    RAISON_NOTIFIEE,
)
from commun import horodater


def notifier_cameleon(id_mission):
    """Depose UN message de pause dans la boite cameleon (intercom).

    Etancheite garantie : le message porte la raison "maintenance", jamais
    l'origine (defcon 5 ou pause manuelle), jamais l'intervention
    user/optimus -- le cameleon ne doit JAMAIS apprendre la raison.
    """
    message = {
        "type": "pause",
        "date": horodater(),
        "mission": id_mission,
        "raison": RAISON_NOTIFIEE,
        "message": MESSAGE_PAUSE,
    }
    CHEMIN_BOITE_CAMELEON.parent.mkdir(parents=True, exist_ok=True)
    with open(CHEMIN_BOITE_CAMELEON, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(message, ensure_ascii=True) + "\n")
